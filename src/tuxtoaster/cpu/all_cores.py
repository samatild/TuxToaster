import os
from multiprocessing import Process, Value
import ctypes
import time
import sys
import select

# ANSI colors
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"


def cpu_stress_single_core(stop_flag):
    a, b = 0, 1
    while not stop_flag.value:
        a, b = b, a + b


def run_all_cores_stress():
    stop_flag = Value(ctypes.c_bool, False)
    num_cores = os.cpu_count() or 1
    processes = []
    for _ in range(num_cores):
        p = Process(target=cpu_stress_single_core, args=(stop_flag,))
        p.start()
        processes.append(p)

    print(f"{BOLD}{GREEN}Running ALL CORES ({num_cores}) — press ENTER to stop.{RESET}")
    start_time = time.time()
    spinner = "|/-\\"
    try:
        while True:
            ch = spinner[int(time.time() - start_time) % len(spinner)]
            elapsed = int(time.time() - start_time)
            print(
                f"\r{YELLOW}{ch}{RESET} {CYAN}Elapsed:{RESET} {elapsed}s  {CYAN}Workers:{RESET} {len(processes)}",
                end="",
                flush=True,
            )
            # non-blocking check for ENTER
            if sys.stdin in select.select([sys.stdin], [], [], 0.25)[0]:
                _ = sys.stdin.readline()
                break
    except KeyboardInterrupt:
        pass
    finally:
        print(f"\n{RED}Stopping…{RESET}")
        stop_flag.value = True
        for p in processes:
            p.terminate()
        for p in processes:
            p.join()
        print(f"{GREEN}Stopped after {int(time.time() - start_time)}s.{RESET}")
        try:
            input(f"{BOLD}Press ENTER to return to the menu…{RESET}")
        except KeyboardInterrupt:
            pass


