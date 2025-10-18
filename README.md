# Tux Toaster
<table>
<tr>
<td><img src="https://raw.githubusercontent.com/samatild/tuxtoaster/main/assets/tuxtoaster.png" alt="Tux Toaster Logo" width="300px" /></td>
<td>

```
████████╗██╗   ██╗██╗  ██╗ 
╚══██╔══╝██║   ██║╚██╗██╔╝ 
   ██║   ██║   ██║ ╚███╔╝  
   ██║   ██║   ██║ ██╔██╗  
   ██║   ╚██████╔╝██╔╝ ██╗ 
   ╚═╝    ╚═════╝ ╚═╝  ╚═╝    
  ████████╗ ██████╗  █████╗ ███████╗████████╗███████╗██████╗ 
  ╚══██╔══╝██╔═══██╗██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗
     ██║   ██║   ██║███████║███████╗   ██║   █████╗  ██████╔╝
     ██║   ██║   ██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗
     ██║   ╚██████╔╝██║  ██║███████║   ██║   ███████╗██║  ██║
     ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝

================================================================
            All-in-one Linux Stress Testing Toolkit
================================================================
```

</td>
</tr>
</table>


## ⚠️ WARNING - RUN AT YOUR OWN RISK!⚠️
Tux Toaster is a workload generator that may harm your Linux system. Run it at your own risk. The developer is not responsible for any damage or data loss that may occur from using this software.

---

## 1. What is Tux Toaster?

Tux Toaster is an all-in-one performance toolkit designed for Linux systems. It triggers various load tests, referred to as "toasters," to help you evaluate the performance and stability of your system.

Project page: [GitHub repository](https://github.com/samatild/tuxtoaster)

---

## 2. Requirements

Tux Toaster targets Linux and relies on a few system tools in addition to Python:

- Python 3.8+ (tested on modern Linux kernels)
- Python package: `psutil` (used by memory tests)
- System utilities: `dd` (coreutils), `lsblk` and `taskset` (util-linux), `pkill` (procps)
- Internet connectivity (network tests use public endpoints)

Optional/privileged:
- Root privileges for the "Unclean GC" runaway memory test to adjust `oom_score_adj`

Install `psutil` if needed:

```bash
pip3 install psutil
```

---

## 3. How to Install and Run

Install from PyPI (recommended):

```bash
pip install tuxtoaster
tuxtoaster
```

### Alternative: Install from source (editable)

```bash
git clone https://github.com/samatild/tuxtoaster.git
cd tuxtoaster
pip install -U pip setuptools wheel
pip install -e .
tuxtoaster
```

### Add install location to PATH

If your shell can't find `tuxtoaster`, add the install directory to PATH:

- System installs (scripts in /usr/local/bin):
```bash
export PATH=/usr/local/bin:$PATH
```

- User installs (scripts in ~/.local/bin):
```bash
export PATH="$HOME/.local/bin:$PATH"
```

To make it persistent (bash):
```bash
echo 'export PATH=/usr/local/bin:$PATH' >> ~/.bashrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

Menu controls (console app):
- Use arrow keys to navigate, Enter to select.
- Many submenus support multi-select; hints are shown in the UI.
- Press `q`, `x`, or `Esc` in a menu to go back.
- During tests, press Enter to stop.

### Menu example

```text
Main Menu
> CPU
  Memory
  Disk
  Network
  Multiple
  About
  Exit

Main Menu > Disk IO
> IOPS Reads
  IOPS Writes
  Random IOPS R/W
  IOPS 50-50 R/W
  Throughput Reads
  Throughput Writes
  Random Throughput R/W
  Throughput 50-50 R/W
  Read while write cache is getting flushed
  Write on Buffer Cache
  Back to Main
```

---

## 4. Available Tests

Tux Toaster offers a variety of tests to stress different system components:

- **CPU**:
  - Single Core
  - All Cores
  - Custom Number of Cores (uses `taskset`; experimental)
- **Memory**: 
  -  Single Runaway Thread
  - Multiple Runaway Threads
  - Memory spikes
  - Unclean GC (requires root to set `oom_score_adj`)
- **Disk**:
    - IOPS Reads (4K, direct I/O)
    - IOPS Writes (4K, direct I/O)
    - Random IOPS R/W (4K, random, direct I/O)
    - IOPS 50-50 R/W (4K, direct I/O)
    - Throughput Reads (4MB, direct I/O)
    - Throughput Writes (4MB, direct I/O)
    - Random Throughput R/W (4MB, random, direct I/O)
    - Throughput 50-50 R/W (4MB, direct I/O)
    - Read while write cache is getting flushed (page cache warm-up then read)
- **Network**: 
    - Network IN (Single) — downloads `https://proof.ovh.net/files/100Mb.dat`
    - Network OUT (Single) — UDP to `8.8.8.8:53`
    - Network IN (Multiple) — N parallel downloads of the OVH file
    - Network OUT (Multiple) — N parallel UDP senders to `8.8.8.8:53`
    - Socket Exhaustion (⚠️ Under development ⚠️)
    - Simulate Latencies (⚠️ Under development ⚠️)
    - Simulate disconnects (⚠️ Under development ⚠️)
    - Simulate packet loss (⚠️ Under development ⚠️)
- **Multiple tests at once**: (⚠️Under Developement⚠️)

---

## 5. Detailed Notes per Category

- **CPU**
  - Single/All Cores spin tight loops to saturate CPU; stop with Enter.
  - Custom Number of Cores pins workloads using `taskset`. This path invokes an internal stress script; consider it experimental.

- **Memory**
  - Single Runaway Thread: allocates 1 GiB chunks repeatedly via anonymous `mmap`; press Enter to stop.
  - Multiple Runaway Threads: user-selectable threads and per-allocation size (MB), stops on low memory; requires `psutil`.
  - Memory spikes: bursts up to ~80–99% of RAM for 1s, pauses 1–10s, repeats.
  - Unclean GC (runaway): attempts to set `oom_score_adj = -1000` (root required) then allocates indefinitely. High risk of system instability.

- **Disk**
  - You select one or more mounted filesystems. For each, the tool creates `io_test_temp/` and a temporary file, runs `dd` loops, and cleans up on stop.
  - IOPS tests use 4K blocks; Throughput tests use 4MB blocks; many use `oflag=direct`/`iflag=direct` to bypass the page cache by design.
  - "Read while write cache is getting flushed" pre-creates a file to demonstrate delayed allocation/cache flush effects before sustained reads.
  - Some filesystems may not support direct I/O on regular files; in that case, `dd` may print errors.

- **Network**
  - IN tests stream a public test object; OUT tests send UDP to a public DNS server. Use responsibly; organizational firewalls may block this traffic.
  - Multi-socket modes prompt for the number of parallel sockets; bandwidth is reported per socket when stopped.

---

## 6. Safety, Cleanup, and Permissions

- This tool intentionally creates heavy load; run in controlled environments.
- Disk tests write temporary files under the selected mount points and delete them on exit.
- Press Enter to stop any running test. If a test becomes unresponsive, you may need to terminate the Python process.
- The Unclean GC test needs root; otherwise it will warn and abort.

---

## 7. Known Limitations

- Several menu items are marked "Under development" and are placeholders.
- The CPU "Custom Number of Cores" mode is experimental and relies on `taskset`; it may require additional internal scripts.
- Direct I/O flags may not be honored on some filesystems or containerized environments.
- Network endpoints (`proof.ovh.net`, `8.8.8.8:53`) may be blocked by your network policy.

---

## 8. Credits

This project menu makes use of the magnific [Simple Term Menu](https://github.com/IngoMeyer441/simple-term-menu) library, which is available under the MIT License.

See `LICENSE` for project licensing details.
