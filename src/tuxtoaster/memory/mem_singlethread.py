from multiprocessing import Process, Event
import threading
import mmap
import time


def memory_eater(stop_event):
    allocated = []
    print("""
          Press ENTER to stop the memory eater.
          
          """)
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
    input_thread = threading.Thread(target=wait_for_input, args=(stop_event,))
    eater_process.start()
    input_thread.start()
    eater_process.join()
    input_thread.join()
    print("Memory eater stopped.")


