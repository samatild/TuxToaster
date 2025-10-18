import os
import subprocess
import threading
from ..assets.simple_term_menu import TerminalMenu
import signal
from time import sleep
from .disk_utils import *


def io_test(directory, temp_file_path):
    dd_command = f"while true; do dd if={temp_file_path} of=/dev/null bs=4K iflag=direct; done"
    dd_process = subprocess.Popen(dd_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while not exit_signal.is_set():
        pass
    dd_process.send_signal(signal.SIGTERM)
    os.remove(temp_file_path)
    os.rmdir(directory)


def run_ioreads():
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
    print("Cooling Down: Sleeping for 5 seconds")
    sleep(5)
    threads = []
    for temp_dir, temp_file_path in temp_file_paths:
        thread = threading.Thread(target=io_test, args=(temp_dir, temp_file_path))
        thread.start()
        threads.append(thread)
        input("""
                            RUNNING
                    DISK IOPS - READS TEST
                                
                    [ Press ENTER to stop. ]

              
                            
================================================================""")
    exit_signal.set()
    for thread in threads:
        thread.join()
    print("IO test stopped.")


