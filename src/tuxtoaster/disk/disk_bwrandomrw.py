import os
import subprocess
import threading
from simple_term_menu import TerminalMenu
import signal
from time import sleep
import random
from .disk_utils import *

# ANSI colors
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"


def io_test(directory, temp_file_path):
    while not exit_signal.is_set():
        operation_type = random.choice(["read", "write"])
        
        if operation_type == "read":
            dd_command = f"dd if={temp_file_path} of=/dev/null bs=4096K iflag=direct count=100 status=none"
        else:
            dd_command = f"dd if=/dev/zero of={temp_file_path} bs=4096K oflag=direct count=100 status=none"
        
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

    print(f"{BOLD}{GREEN}Running DISK THROUGHPUT - RANDOM RW — press ENTER to stop.{RESET}")

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

    input("Press ENTER to stop.")
    
    exit_signal.set()
    
    for thread in threads:
        thread.join()
    
    print(f"{GREEN}IO test stopped.{RESET}")
    try:
        input(f"{BOLD}Press ENTER to return to the menu…{RESET}")
    except KeyboardInterrupt:
        pass


