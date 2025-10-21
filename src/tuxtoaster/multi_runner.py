import os
import sys
import time
import mmap
import psutil
import random
import shutil
import subprocess
import urllib.request
import threading
import ctypes
from multiprocessing import Process, Event, Value

from .assets.simple_term_menu import TerminalMenu


# ANSI colors
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"


def _cpu_busy_loop(stop_flag: Value) -> None:
    a, b = 0, 1
    while not stop_flag.value:
        a, b = b, a + b


def _cpu_worker(stop_flag: Event) -> None:
    # Spawn one busy process per CPU core
    num_cores = os.cpu_count() or 1
    local_flag = Value(ctypes.c_bool, False)
    procs = []
    for _ in range(num_cores):
        p = Process(target=_cpu_busy_loop, args=(local_flag,))
        p.start()
        procs.append(p)

    try:
        while not stop_flag.is_set():
            time.sleep(0.25)
    finally:
        local_flag.value = True
        for p in procs:
            try:
                p.terminate()
            except Exception:
                pass
        for p in procs:
            try:
                p.join()
            except Exception:
                pass


def _memory_thread(stop_event: threading.Event, allocated, size_mb: int) -> None:
    size_bytes = size_mb * 1024 * 1024
    while not stop_event.is_set():
        if psutil.virtual_memory().available < size_bytes:
            stop_event.set()
            break
        try:
            mem = mmap.mmap(-1, size_bytes)
            mem.write(b"\x00" * size_bytes)
            allocated.append(mem)
        except OSError:
            stop_event.set()
            break
        time.sleep(1)


def _memory_worker(stop_flag: Event, threads: int = 2, chunk_mb: int = 500) -> None:
    stop_event = threading.Event()
    allocated = []
    ts = []
    for _ in range(threads):
        t = threading.Thread(
            target=_memory_thread,
            args=(stop_event, allocated, chunk_mb),
        )
        t.start()
        ts.append(t)

    try:
        while not stop_flag.is_set() and not stop_event.is_set():
            time.sleep(0.5)
    finally:
        stop_event.set()
        for t in ts:
            try:
                t.join()
            except Exception:
                pass


def _network_worker(stop_flag: Event) -> None:
    url = "https://proof.ovh.net/files/100Mb.dat"
    while not stop_flag.is_set():
        try:
            with urllib.request.urlopen(url, timeout=10) as r:
                while not stop_flag.is_set():
                    chunk = r.read(4096)
                    if not chunk:
                        break
        except Exception:
            time.sleep(1)


def _disk_worker(stop_flag: Event) -> None:
    base_dir = "/tmp/tuxtoaster_multi_io"
    os.makedirs(base_dir, exist_ok=True)
    temp_path = os.path.join(base_dir, "tempfile.bin")

    # Ensure file exists to read from
    if not os.path.exists(temp_path):
        try:
            subprocess.run(
                [
                    "dd",
                    "if=/dev/zero",
                    f"of={temp_path}",
                    "bs=4096K",
                    "count=100",
                    "status=none",
                ],
                check=False,
            )
        except Exception:
            pass

    try:
        while not stop_flag.is_set():
            op = random.choice(["read", "write"])
            if op == "read":
                cmd = [
                    "dd",
                    f"if={temp_path}",
                    "of=/dev/null",
                    "bs=4096K",
                    "iflag=direct",
                    "count=100",
                    "status=none",
                ]
            else:
                cmd = [
                    "dd",
                    "if=/dev/zero",
                    f"of={temp_path}",
                    "bs=4096K",
                    "oflag=direct",
                    "count=100",
                    "status=none",
                ]

            try:
                proc = subprocess.Popen(cmd)
                while proc.poll() is None and not stop_flag.is_set():
                    time.sleep(0.2)
                if stop_flag.is_set() and proc.poll() is None:
                    try:
                        proc.terminate()
                    except Exception:
                        pass
            except Exception:
                time.sleep(1)
    finally:
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            if os.path.isdir(base_dir):
                shutil.rmtree(base_dir, ignore_errors=True)
        except Exception:
            pass


def run_multiple() -> None:
    print(f"{BOLD}{GREEN}Multiple selection — press ENTER to stop.{RESET}")

    items = ["CPU", "Memory", "Network", "Disk"]
    menu = TerminalMenu(
        items,
        title="Select resources to stress (SPACE to mark)",
        multi_select=True,
        show_multi_select_hint=True,
        cycle_cursor=True,
        quit_keys=["q", "x", "escape"],
    )
    selected = menu.show()

    if not selected:
        print("No resources selected.")
        return

    stop_flag = Event()

    # Start a prompt thread for ENTER to stop
    def prompt_exit() -> None:
        input("Press ENTER to stop all selected tests.")
        stop_flag.set()

    prompt_thread = threading.Thread(target=prompt_exit)
    prompt_thread.start()

    # Start a thread per selection that spawns a process
    processes = []

    def spawn(target):
        p = Process(target=target, args=(stop_flag,))
        p.start()
        processes.append(p)

    for idx in selected:
        item = items[idx]
        if item == "CPU":
            t = threading.Thread(target=spawn, args=(_cpu_worker,))
        elif item == "Memory":
            t = threading.Thread(target=spawn, args=(_memory_worker,))
        elif item == "Network":
            t = threading.Thread(target=spawn, args=(_network_worker,))
        elif item == "Disk":
            t = threading.Thread(target=spawn, args=(_disk_worker,))
        else:
            continue
        t.start()

    # Wait for stop
    prompt_thread.join()

    # Terminate processes
    for p in processes:
        try:
            p.terminate()
        except Exception:
            pass
    for p in processes:
        try:
            p.join()
        except Exception:
            pass

    try:
        input(f"{BOLD}Press ENTER to return to the menu…{RESET}")
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    run_multiple()


