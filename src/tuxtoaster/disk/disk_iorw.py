import os
import subprocess
import threading
from simple_term_menu import TerminalMenu
import signal
from time import sleep
from .disk_utils import *

# ANSI colors
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"



def io_test(directory, temp_file_path, operation_type):
    if operation_type == "read":
        dd_command = f"while true; do dd if={temp_file_path} of=/dev/null bs=4K iflag=direct status=none; done"
    else:
        dd_command = f"while true; do dd if=/dev/zero of={temp_file_path} bs=4K oflag=direct status=none; done"
    
    dd_process = subprocess.Popen(dd_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
    
    while not exit_signal.is_set():
        pass
    
    os.killpg(os.getpgid(dd_process.pid), signal.SIGTERM)
    os.remove(temp_file_path)


def run_iorw():
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

    print(f"{BOLD}{GREEN}Running DISK IOPS - 50-50 RW — press ENTER to stop.{RESET}")

    selected_mount_points = [list(mount_points.keys())[i] for i in selected_indexes]
    
    threads = []
    for mount_point in selected_mount_points:
        temp_dir = os.path.join(mount_point, "io_test_temp")
        os.makedirs(temp_dir, exist_ok=True)
        
        read_file_path = create_dummy_file_multi(temp_dir, "read_temp_file")
        write_file_path = create_dummy_file_multi(temp_dir, "write_temp_file")
    
    print("Cooling Down: Sleeping for 5 seconds")
    sleep(5)
    
    for mount_point in selected_mount_points:
        read_thread = threading.Thread(target=io_test, args=(temp_dir, read_file_path, "read"))
        write_thread = threading.Thread(target=io_test, args=(temp_dir, write_file_path, "write"))
        
        read_thread.start()
        write_thread.start()
        
        threads.extend([read_thread, write_thread])

    input("Press ENTER to stop.")
    
    exit_signal.set()
    
    for thread in threads:
        thread.join()
    
    print(f"{GREEN}IO test stopped.{RESET}")
    try:
        input(f"{BOLD}Press ENTER to return to the menu…{RESET}")
    except KeyboardInterrupt:
        pass


