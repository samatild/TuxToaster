import subprocess
import os
from multiprocessing import Process, Value
import ctypes
from ..assets.simple_term_menu import TerminalMenu
import signal
import time


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
    subprocess.run(["pkill", "-f", "while True: pass"]) 


