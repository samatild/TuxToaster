from multiprocessing import Value, Process
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


def cpu_stress(stop_flag):
    a, b = 0, 1
    while not stop_flag.value:
        a, b = b, a + b


def run_single_core_stress():
    stop_flag = Value(ctypes.c_bool, False)
    p = Process(target=cpu_stress, args=(stop_flag,))
    p.start()

    print(f"{BOLD}{GREEN}Running SINGLE CORE — press ENTER to stop.{RESET}")
    start_time = time.time()
    spinner = "|/-\\"
    try:
        while True:
            ch = spinner[int(time.time() - start_time) % len(spinner)]
            elapsed = int(time.time() - start_time)
            print(
                f"\r{YELLOW}{ch}{RESET} {CYAN}Elapsed:{RESET} {elapsed}s",
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
        p.terminate()
        p.join()
        print(f"{GREEN}Stopped after {int(time.time() - start_time)}s.{RESET}")
        try:
            input(f"{BOLD}Press ENTER to return to the menu…{RESET}")
        except KeyboardInterrupt:
            pass


