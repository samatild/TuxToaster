# Tux Toaster
<table>
<tr>
<td><img src="assets/tuxtoaster.png" alt="Tux Toaster Logo" width="300px" /></td>
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

---

## 2. How to Run Tux Toaster

To run Tux Toaster, you'll need to clone the repository and execute the main Python script. Here are the steps:



```bash
# Clone the repository
git clone https://github.com/samatild/tuxtoaster.git

# Navigate to the project directory
cd tuxtoaster

# Run the main Python script
python3 tuxtoaster.py
```
Attention: Tux Toaster requires Python module psutil. If you don't have it installed, run the following command:

```bash
# Install psutil
pip3 install psutil
```

## 3. Available Tests

Tux Toaster offers a variety of tests to stress different system components:

- **CPU**:
  - Single Core
  - All Cores
  - Custom Number of Cores 
- **Memory**: 
  -  Single Runaway Thread
  - Multiple Runaway Threads
  - Memory spikes
  - Unclean GC
- **Disk**:
    - IOPS Reads
    -   IOPS Writes
    -   Random IOPS R/W
    -   IOPS 50-50 R/W
    -   Throughput Reads
    -   Throughput Writes
    -   Random Throughput R/W
    -   Throughput 50-50 R/W
    -   Read while write cache is getting flushed
- **Network**: 
    - Network IN (Single)
    - Network OUT (Single)
    - Network IN (Multiple)
    - Network OUT (Multiple)
    - Socket Exaustion (⚠️Under Developement⚠️)
    - Simulate Latencies (⚠️Under Developement⚠️)
    - Simulate disconnects (⚠️Under Developement⚠️)
    - Simulate packet loss (⚠️Under Developement⚠️)
- **Multiple tests at once**: (⚠️Under Developement⚠️)

---

## 4. Credits

This project menu makes use of the magnific [Simple Term Menu](https://github.com/IngoMeyer441/simple-term-menu) library, which is available under the MIT License.
