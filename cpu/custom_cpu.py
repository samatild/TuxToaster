# cpu/custom_cpu.py

import subprocess
import os
from multiprocessing import Process, Value
import ctypes
from _simple_term_menu.simple_term_menu import TerminalMenu
import signal
import time

#The initial writes you're observing are likely due to the file system's delayed allocation or write-back caching mechanisms. When you create a large file, the file system might not immediately allocate all the disk blocks for that file. Instead, it may defer the actual disk writes until it's necessary, such as when the file is closed or when the file system cache is flushed.



def stress_specific_core(core_number, stop_flag):
    os.setsid()  # Create new session and set process group
    command = f"taskset -c {core_number} python3 cpu/cpu_stress.py"
    proc = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)
    
    while not stop_flag.value:
        time.sleep(0.1)  # Sleep for a short time to reduce CPU usage

    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)  # Terminate the process group
    

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

    if not selected_cores:  # Check if the tuple is empty
        print("Warning: You must select at least one core. Exiting.")
        return

    processes = []
    for core in selected_cores:
        p = Process(target=stress_specific_core, args=(core, stop_flag))
        p.start()
        processes.append(p)

    try:
        input("""
                            RUNNING
                    CUSTOM CORE STRESS TEST
                                
                    [ Press ENTER to stop. ]

              
                            
================================================================""")
    except KeyboardInterrupt:
        print("Stopping CPU stress test due to keyboard interrupt.")

    stop_flag.value = True
    for p in processes:
        os.killpg(os.getpgid(p.pid), signal.SIGTERM)
    subprocess.run(["pkill", "-f", "cpu_stress.py"])

if __name__ == "__main__":
    run_custom_cores_stress()
