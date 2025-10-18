import os
import subprocess
import threading
from simple_term_menu import TerminalMenu
import signal
from .disk_utils import get_unique_mount_points

# ANSI colors
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"

# The initial writes you're observing are likely due to the file system's delayed allocation or write-back caching mechanisms. When you create a large file, the file system might not immediately allocate all the disk blocks for that file. Instead, it may defer the actual disk writes until it's necessary, such as when the file is closed or when the file system cache is flushed.

# Here's a breakdown of what's likely happening:

# File Creation: When the dd command creates the file, the file system may only allocate the inode and some initial blocks but not immediately write all the data to disk.

# Cache Flush: As the dd command or the file system flushes the cache to disk, you'll see write operations. This is the file system actually allocating the blocks and writing the data.

# Read Operations: Once the file is fully written to disk and the cache is flushed, the subsequent dd read operations will only result in read I/O, as expected.

# Transition: The transition from writes to reads is the point where the file system has completed all deferred writes and has fully allocated the file on disk.



def create_dummy_file(directory):
    temp_file_path = os.path.join(directory, "temp_file")
    print(f"Warming up: Creating dummy file at {temp_file_path}")
    with open(temp_file_path, "wb") as f:
        f.write(b"x" * 1024 * 1024 * 100)
    return temp_file_path


def io_test(directory, temp_file_path):
    # Run dd command to read the file continuously in a loop
    dd_command = f"while true; do dd if={temp_file_path} of=/dev/null bs=4K iflag=direct status=none; done"
    dd_process = subprocess.Popen(dd_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait until the exit signal is set
    while not exit_signal.is_set():
        pass
    
    # Terminate the dd process
    dd_process.send_signal(signal.SIGTERM)
    
    # Cleanup
    os.remove(temp_file_path)
    os.rmdir(directory)


def run_cachewriteswarmup():
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

    print(f"{BOLD}{GREEN}Running DISK READ - CACHE WRITE WARMUP — press ENTER to stop.{RESET}")

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


