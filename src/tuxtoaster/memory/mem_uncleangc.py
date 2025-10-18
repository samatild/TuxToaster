import mmap
import os
import time


def set_oom_score_adj(value):
    try:
        with open(f"/proc/{os.getpid()}/oom_score_adj", "w") as f:
            f.write(str(value))
    except PermissionError:
        print("Setting oom_score_adj requires root permissions.")
        return False
    return True


def memory_runaway():
    if not set_oom_score_adj(-1000):
        return
    allocated = []
    while True:
        mem = mmap.mmap(-1, 1024 * 1024 * 1024)
        mem.write(b'\x00' * (1024 * 1024 * 1024))
        allocated.append(mem)
        print(f"Allocated {len(allocated)} GB")
        time.sleep(1)


