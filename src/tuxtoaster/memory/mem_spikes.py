from multiprocessing import Process, Event
import threading
import time
import mmap
import random
import psutil


def memory_eater(stop_event):
    print("""
          Press ENTER to stop the memory eater.
          """)
    while not stop_event.is_set():
        total_memory = psutil.virtual_memory().total
        mem_to_allocate = int(total_memory * (random.uniform(0.8, 0.99)))
        mem = mmap.mmap(-1, mem_to_allocate)
        mem.write(b'\x00' * mem_to_allocate)
        print(f"\033[A\033[KAllocated {mem_to_allocate / (1024 * 1024 * 1024):.2f} GB", flush=True)
        time.sleep(1)
        mem.close()
        time.sleep(random.uniform(1, 10))


def wait_for_input(stop_event):
    input()
    stop_event.set()


def run_memory_spikes():
    stop_event = Event()
    eater_process = Process(target=memory_eater, args=(stop_event,))
    input_thread = threading.Thread(target=wait_for_input, args=(stop_event,))
    eater_process.start()
    input_thread.start()
    eater_process.join()
    input_thread.join()
    print("Memory eater stopped.")


