import mmap
import os
import time

# ANSI colors
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"


def set_oom_score_adj(value):
    try:
        with open(f"/proc/{os.getpid()}/oom_score_adj", "w") as f:
            f.write(str(value))
    except PermissionError:
        print("Setting oom_score_adj requires root permissions.")
        return False
    return True


def memory_runaway():
    print(f"{BOLD}{GREEN}Running MEMORY (unclean GC) — use with extreme caution.{RESET}")
    if not set_oom_score_adj(-1000):
        return

    allocated = []
    while True:
        mem = mmap.mmap(-1, 1024 * 1024 * 1024)
        mem.write(b'\x00' * (1024 * 1024 * 1024))
        allocated.append(mem)
        print(f"Allocated {len(allocated)} GB")
        time.sleep(1)


if __name__ == "__main__":
    memory_runaway()


