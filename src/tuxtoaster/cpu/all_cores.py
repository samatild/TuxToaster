import os
from multiprocessing import Process, Value
import ctypes


def cpu_stress_single_core(stop_flag):
    a, b = 0, 1
    while not stop_flag.value:
        a, b = b, a + b


def run_all_cores_stress():
    stop_flag = Value(ctypes.c_bool, False)
    num_cores = os.cpu_count()
    processes = []
    for _ in range(num_cores):
        p = Process(target=cpu_stress_single_core, args=(stop_flag,))
        p.start()
        processes.append(p)
    try:
        input("""
                            RUNNING
                    ALL CORES STRESS TEST
                                
                    [ Press ENTER to stop. ]

              
                            
================================================================""")
    except KeyboardInterrupt:
        print("Stopping CPU stress test due to keyboard interrupt.")
    stop_flag.value = True
    for p in processes:
        p.terminate()


