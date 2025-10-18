import os
import subprocess
import threading
from ..assets.simple_term_menu import TerminalMenu
import signal
from time import sleep
import random
from .disk_utils import *


def io_test(directory, temp_file_path):
    while not exit_signal.is_set():
        operation_type = random.choice(["read", "write"])
        if operation_type == "read":
            dd_command = f"dd if={temp_file_path} of=/dev/null bs=4096K iflag=direct count=100"
        else:
            dd_command = f"dd if=/dev/zero of={temp_file_path} bs=4096K oflag=direct count=100"
        dd_process = subprocess.Popen(dd_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
        dd_process.wait()
        if exit_signal.is_set():
            os.killpg(os.getpgid(dd_process.pid), signal.SIGTERM)


def run_bwrandom():
    global exit_signal
    exit_signal = threading.Event()
    mount_points = get_unique_mount_points()
    menu_items = [f"{info['parent_device']} ({info['device_name']})" for mount_point, info in mount_points.items()]
    menu = TerminalMenu(menu_items, title="Select mount points for IO test:", multi_select=True, preselected_entries=[0], quit_keys=["q", "x", "escape"])
    selected_indexes = menu.show()
    if selected_indexes is None:
        print("User chose to quit. Exiting.")
        return
    if len(selected_indexes) == 0:
        print("No mount points selected. Exiting.")
        return
    selected_mount_points = [list(mount_points.keys())[i] for i in selected_indexes]
    temp_file_paths = []
    for mount_point in selected_mount_points:
        temp_dir = os.path.join(mount_point, "io_test_temp")
        os.makedirs(temp_dir, exist_ok=True)
        temp_file_path = create_dummy_file(temp_dir)
        temp_file_paths.append((temp_dir, temp_file_path))
    threads = []
    for temp_dir, temp_file_path in temp_file_paths:
        thread = threading.Thread(target=io_test, args=(temp_dir, temp_file_path))
        thread.start()
        threads.append(thread)
        input("""
                            RUNNING
                DISK THROUGHPUT - RANDOM RW TEST
                                
                    [ Press ENTER to stop. ]

              
                            
================================================================""")
    exit_signal.set()
    for thread in threads:
        thread.join()
    print("IO test stopped.")


