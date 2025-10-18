from multiprocessing import Process, Event
import threading
import mmap
import time
import psutil

# ANSI colors
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"


def memory_eater_thread(stop_event, allocated, size_mb):
    size_bytes = size_mb * 1024 * 1024  # Convert MB to bytes
    while not stop_event.is_set():
        # Check available memory
        available_memory = psutil.virtual_memory().available
        if available_memory < size_bytes:
            print("Low memory. Stopping allocation.")
            stop_event.set()
            break

        try:
            mem = mmap.mmap(-1, size_bytes)
            mem.write(b'\x00' * size_bytes)
            allocated.append(mem)
        except OSError:
            print("Memory allocation failed. Stopping.")
            stop_event.set()
            break

        time.sleep(1)


def memory_eater_multi(stop_event, num_threads, size_mb):
    print(f"{YELLOW}Press ENTER to stop the memory eater.{RESET}")
    allocated = []
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=memory_eater_thread, args=(stop_event, allocated, size_mb))
        t.start()
        threads.append(t)

    while not stop_event.is_set():
        print("\033[A\033[K", end='') 
        print(f"Allocated {len(allocated) * size_mb // 1024} GB with {num_threads} threads", flush=True)
        time.sleep(1)

    # Stop all threads
    for t in threads:
        t.join()

    print("\nMemory eater stopped.")


def wait_for_input(stop_event):
    input()
    stop_event.set()


def run_memory_multithread(num_threads=None, size_mb=None):
    if num_threads is None:
        num_threads = int(input("Enter the number of threads (1-32): "))
    if size_mb is None:
        size_mb = int(input("Enter the size of each allocation in MB: "))
    
    if 1 <= num_threads <= 32:
        stop_event = Event()
        eater_process = Process(target=memory_eater_multi, args=(stop_event, num_threads, size_mb))
        input_thread = threading.Thread(target=wait_for_input, args=(stop_event,))

        print(f"{BOLD}{GREEN}Running MEMORY (multi runaway) — press ENTER to stop.{RESET}")
        eater_process.start()
        input_thread.start()

        eater_process.join()
        input_thread.join()

        print(f"\n{GREEN}Memory eater stopped.{RESET}")
        try:
            input(f"{BOLD}Press ENTER to return to the menu…{RESET}")
        except KeyboardInterrupt:
            pass
    else:
        print("Invalid number of threads. Must be between 1 and 32.")


