from multiprocessing import Process, Event
import threading
import time
import mmap
import random
import psutil

# ANSI colors
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"


def memory_eater(stop_event):
    print(f"{YELLOW}Press ENTER to stop the memory eater.{RESET}")
    while not stop_event.is_set():
        # Get total system memory in bytes
        total_memory = psutil.virtual_memory().total

        # Randomly allocate between 80% to 99% of total memory
        mem_to_allocate = int(total_memory * (random.uniform(0.8, 0.99)))

        # Create a memory-mapped file of the required size
        mem = mmap.mmap(-1, mem_to_allocate)
        mem.write(b'\x00' * mem_to_allocate)

        print(f"\033[A\033[KAllocated {mem_to_allocate / (1024 * 1024 * 1024):.2f} GB", flush=True)

        # Memory spike lasts for 1 second
        time.sleep(1)

        # Close the memory-mapped file to deallocate memory
        mem.close()

        # Wait for a random time between 1 to 10 seconds before the next spike
        time.sleep(random.uniform(1, 10))


def wait_for_input(stop_event):
    input()
    stop_event.set()


def run_memory_spikes():
    stop_event = Event()
    eater_process = Process(target=memory_eater, args=(stop_event,))

    # Using threading for input to keep it in the same process
    input_thread = threading.Thread(target=wait_for_input, args=(stop_event,))

    print(f"{BOLD}{GREEN}Running MEMORY spikes — press ENTER to stop.{RESET}")
    eater_process.start()
    input_thread.start()

    eater_process.join()
    input_thread.join()

    print(f"{GREEN}Memory eater stopped.{RESET}")
    try:
        input(f"{BOLD}Press ENTER to return to the menu…{RESET}")
    except KeyboardInterrupt:
        pass


