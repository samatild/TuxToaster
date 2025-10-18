from multiprocessing import Value, Process
import ctypes


def cpu_stress(stop_flag):
    a, b = 0, 1
    while not stop_flag.value:
        a, b = b, a + b


def run_single_core_stress():
    stop_flag = Value(ctypes.c_bool, False)
    p = Process(target=cpu_stress, args=(stop_flag,))
    p.start()
    try:
        input("""
                            RUNNING
                    SINGLE CORE STRESS TEST
                                
                    [ Press ENTER to stop. ]

              
                            
================================================================""")
    except KeyboardInterrupt:
        print("Stopping CPU stress test due to keyboard interrupt.")
    stop_flag.value = True
    p.terminate()


