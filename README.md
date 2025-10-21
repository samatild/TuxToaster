# Tux Toaster
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
    - Socket Exhaustion — exhaust process/kernel socket resources or reserve port ranges
    - Simulate Latencies — local TCP proxy that adds base latency and jitter
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

### Network: Socket Exhaustion

What it does:
- Opens and holds many sockets until you press Enter, to expose practical limits like per-process file descriptors and ephemeral port exhaustion. Two modes:
  - Connections (default): Starts a local TCP server on 127.0.0.1 and opens as many TCP client connections to it as possible, then keeps them open.
  - Bind listener ports: Binds listening sockets over a port range (on 0.0.0.0) to reserve those ports and block other listeners on the same host.

How to use:
- From the menu: Network → Socket Exhaustion.
- Optionally answer “y” to increase this process open-file limit to the hard limit.
- Choose Mode 1 (connections) or Mode 2 (bind listener ports).
- Press Enter at any time to release all sockets and return to the menu.

Mode details:
- Mode 1 (connections):
  - The tool prints progress every 100 sockets with an approximate open rate.
  - Stops opening when it hits an OS error (e.g., EMFILE or EADDRNOTAVAIL); sockets remain open until you press Enter.
  - Useful to observe ephemeral port exhaustion (Cannot assign requested address) and per-process descriptor limits.
- Mode 2 (bind listener ports):
  - Prompts for a port range (e.g., 1024–65535) and binds on 0.0.0.0 to prevent other processes (e.g., `ncat -l`) from listening on those ports.
  - May require root to bind ports <1024.

Tuning tips (advanced):
- Increase ephemeral port range (temporary):
```bash
sudo sysctl -w net.ipv4.ip_local_port_range="1024 65535"
```
- Add extra loopback IPs to expand source address space (Mode 1):
```bash
sudo ip addr add 127.0.0.2/8 dev lo
sudo ip addr add 127.0.0.3/8 dev lo
```
- Consider IPv6 `::1` to use a separate ephemeral space.
- Raise per-process open file limit (interactive prompt will try to set soft=hard):
```bash
ulimit -n 1048576
```
- For system-wide exhaustion tests, run multiple instances or combine with other processes.

### Network: Simulate Latencies

What it does:
- Runs a local TCP proxy on 127.0.0.1 that relays to a target host:port and injects artificial delay on each chunk with configurable base latency and jitter. Use this to see how added RTT affects interactive protocols and bulk transfers.

How to use:
- From the menu: Network → Simulate Latencies.
- Enter values when prompted:
  - Target host (e.g., `www.google.com`)
  - Target port (e.g., `80`)
  - Local listen port (`0` for auto; the app will print the actual port)
  - Base latency in ms (e.g., `200`)
  - Jitter (+/- ms) (e.g., `50`)
- Point clients to `127.0.0.1:<listen_port>` and preserve the original Host header when needed.
- Press Enter in the app to stop and clean up.

Example towards Google (HTTP):

Start Simulate Latencies with:
- Target host: `www.google.com`
- Target port: `80`
- Local listen port: `46843` (or `0` and note the printed port)
- Base latency: `200`
- Jitter: `50`

Single request via curl (preserving Host):
```bash
curl -H "Host: www.google.com" -s -o /dev/null -w 'connect=%{time_connect}s starttransfer=%{time_starttransfer}s total=%{time_total}s\n' http://127.0.0.1:46843/
```

Sample output:
```text
connect=0.000136s starttransfer=2.147816s total=6.028596s
```

Multiple runs (simple average by eye):
```bash
for i in {1..10}; do
  curl -H "Host: www.google.com" -s -o /dev/null -w '%{time_total}\n' http://127.0.0.1:46843/
done
```

Other useful client tests:
- wget
```bash
wget -S -O /dev/null --header='Host: www.google.com' http://127.0.0.1:46843/
```

- HTTP load (hey)
```bash
hey -n 200 -c 20 -H 'Host: www.google.com' http://127.0.0.1:46843/
```

- iperf3 (through the proxy to a remote server)
1) On a remote box: `iperf3 -s`
2) Run latency sim to `remote:5201`, local listen port `5202`
3) Client:
```bash
iperf3 -c 127.0.0.1 -p 5202 -t 20
```

- SSH (replace with your host)
1) Run latency sim to `your.ssh.host:22`, local listen port `10022`
2) Client:
```bash
ssh -p 10022 user@127.0.0.1
```

- Postgres (replace with your DB)
1) Run latency sim to `db-host:5432`, local listen port `5433`
2) Client:
```bash
psql -h 127.0.0.1 -p 5433 -U myuser mydb
```

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
