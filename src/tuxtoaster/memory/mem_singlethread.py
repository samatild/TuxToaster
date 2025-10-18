from multiprocessing import Process, Event
import threading
import mmap
import time

# ANSI colors
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"


def memory_eater(stop_event):
    allocated = []
    print(f"{YELLOW}Press ENTER to stop the memory eater.{RESET}")
    while not stop_event.is_set():
        mem = mmap.mmap(-1, 1024 * 1024 * 1024)
        mem.write(b'\x00' * (1024 * 1024 * 1024))
        allocated.append(mem)
        print("\033[A\033[K", end='')
        print(f"Allocated {len(allocated)} GB", flush=True)
        time.sleep(1)


def wait_for_input(stop_event):
    input()
    stop_event.set()


def run_memory_singlethread():
    stop_event = Event()
    eater_process = Process(target=memory_eater, args=(stop_event,))
    # Using threading for input to keep it in the same process
    input_thread = threading.Thread(target=wait_for_input, args=(stop_event,))

    print(f"{BOLD}{GREEN}Running MEMORY (single runaway) — press ENTER to stop.{RESET}")
    eater_process.start()
    input_thread.start()

    eater_process.join()
    input_thread.join()

    print(f"{GREEN}Memory eater stopped.{RESET}")
    try:
        input(f"{BOLD}Press ENTER to return to the menu…{RESET}")
    except KeyboardInterrupt:
        pass


