import subprocess
import os
from multiprocessing import Process, Value
import ctypes
from simple_term_menu import TerminalMenu
import signal
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


def stress_specific_core(core_number, stop_flag):
    os.setsid()
    command = f"taskset -c {core_number} python3 -c 'while True: pass'"
    proc = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)
    while not stop_flag.value:
        time.sleep(0.1)
    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)


def run_custom_cores_stress():
    stop_flag = Value(ctypes.c_bool, False)
    max_cores = os.cpu_count()
    core_options = [str(i) for i in range(max_cores)]
    menu = TerminalMenu(core_options,
                        title="Select cores to stress (multi-select enabled)",
                        multi_select=True,
                        multi_select_empty_ok=True,
                        preselected_entries=[0],
                        show_multi_select_hint=True)
    selected_cores = menu.show()
    if not selected_cores:
        print("Warning: You must select at least one core. Exiting.")
        return
    processes = []
    for core in selected_cores:
        p = Process(target=stress_specific_core, args=(core, stop_flag))
        p.start()
        processes.append(p)

    print(f"{BOLD}{GREEN}Running CUSTOM CORE(S) — press ENTER to stop.{RESET}")
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
            if sys.stdin in select.select([sys.stdin], [], [], 0.25)[0]:
                _ = sys.stdin.readline()
                break
    except KeyboardInterrupt:
        pass
    finally:
        print(f"\n{RED}Stopping…{RESET}")
        stop_flag.value = True
        for p in processes:
            os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        for p in processes:
            p.join()
        subprocess.run(["pkill", "-f", "while True: pass"]) 
        print(f"{GREEN}Stopped after {int(time.time() - start_time)}s.{RESET}")
        try:
            input(f"{BOLD}Press ENTER to return to the menu…{RESET}")
        except KeyboardInterrupt:
            pass


