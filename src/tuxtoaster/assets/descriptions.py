def preview_menu(menu_entry):
    descriptions = {
        "CPU": "\033[93mCPU Stress Tests.\033[0m",
        "Memory": "\033[93mMemory overload simulation.\033[0m",
        "Disk": "\033[93mSimulates Disk activity.\033[0m",
        "Network": "\033[93mOverload the network stack.\033[0m",
        "Multiple": "\033[92mUnder developement.\033[0m",
        "About": "\033[96mTux Toaster is an All-in-One benchmark toolkit for Linux.\n\033[96mIt was designed with the scope of bringing simplicity to common workload tests. \n\n\033[91mThe developer is not responsible for any arm that the tool does to your system. \n\033[91mUse at your own risk!!! \n\n\033[92mDeveloped by: Samuel Matildes \n\033[92mProject Page: \033[93mhttps://github.com/samatild/tuxtoaster\033[0m",
        "Exit": "\033[93mGoodbye.\033[0m"
    }
    return descriptions.get(menu_entry, "\033[92mNo description available.\033[0m")

def preview_cpusbumenu(menu_entry):
    descriptions = {
        "Single Core": "\033[93mThis option will stress a single CPU core.\033[0m",
        "All Cores": "\033[93mThis option will stress all available CPU cores.\033[0m",
        "Custom Number of Cores": "\033[93mThis option allows you to specify the number of CPU cores to stress.\033[0m",
        "Back to Main": "\033[93mThis option will take you back to the main menu.\033[0m"
    }
    return descriptions.get(menu_entry, "\033[92mNo description available.\033[0m")

def preview_memsbumenu(menu_entry):
    descriptions = {
        "Single Runaway Thread": "\033[93mTo assess the system's behavior and performance when a \033[0msingle thread goes rogue and starts consuming an excessive amount of memory.\033[0m",
        "Multiple Runaway Threads": "\033[93mTo evaluate the system's capability to handle \033[0mmultiple threads that are consuming memory uncontrollably.\033[0m",
        "Memory spikes": "\033[93mTo understand how the system copes with sudden, large increases in memory usage.\033[0m",
        "Unclean GC": "\033[93mTo evaluate the system's behavior when garbage collection is not properly releasing memory.\n\033[93mThis test has the potential to cause a kernel panic due to uncontrolled memory consumption. \n\033[93mProceed with extreme caution and only run this test in a controlled environment where a system crash is acceptable.\033[0m",
        "Back to Main": "\033[93mThis option will take you back to the main menu.\033[0m"
    }
    return descriptions.get(menu_entry, "\033[92mNo description available.\033[0m")

def preview_disksbumenu(menu_entry):
    descriptions = {
        "IOPS Reads": "\033[93mThis test measures the Input/Output Operations Per Second (IOPS) for read operations on a storage device. \n\033[93mThe block size used for this test is 4KB. \n\033[93mThe objective is to quantify how many read operations the storage system can handle per second under a specific workload.\033[0m",
        "IOPS Writes": "\033[93mSimilar to IOPS Reads, this test focuses on write operations. \n\033[93mIt measures the number of 4KB write operations that can be performed per second. \n\033[93mThis provides an indication of the storage system's write performance.\033[0m",
        "Random IOPS R/W": "\033[93mThis test measures the IOPS for both read and write operations but does so with random access patterns. \n\033[93mThe block size remains at 4KB. \n\033[93mThis test is useful for understanding how a storage system performs under workloads \n\033[93mthat don't follow sequential data access patterns, such as databases.\033[0m",
        "IOPS 50-50 R/W": "\033[93mIn this test, read and write operations are mixed in a 50-50 ratio. The block size is 4KB. \n\033[93mThis test aims to simulate a balanced workload where reads and writes are \n\033[93mequally likely, providing a more comprehensive view of storage performance.\033[0m",
        "Throughput Reads": "\033[93mThis test measures the data transfer rate for read operations in megabytes per second (MB/s). \n\033[93mUnlike IOPS, which counts operations, throughput measures the actual data transferred. \n\033[93mThe block size used for this test is 4096KB (4MB).\033[0m",
        "Throughput Writes": "\033[93mSimilar to Throughput Reads, this test focuses on the data transfer rate for write operations. \n\033[93mThe block size is 4096KB. \n\033[93mThis test quantifies how much data can be written to the storage system per second.\033[0m",
        "Random Throughput R/W": "\033[93mThis test measures the throughput for both read and write operations with random access patterns. \n\033[93mThe block size is 4096KB. \n\033[93mThis test is useful for systems where data access is not sequential and involves large blocks of data, such as in big data analytics.\033[0m",
        "Throughput 50-50 R/W": "\033[93mIn this test, read and write operations are mixed in a 50-50 ratio, and the throughput in MB/s is measured. \n\033[93mThe block size is 4096KB. \n\033[93mThis test aims to simulate a balanced workload in terms of data transfer, \n\033[93mproviding a holistic view of the storage system's capabilities for both read and write operations.\033[0m",
        "Read while write cache is getting flushed": """\033[93mThis test aims to investigate and quantify the impact of file system delayed allocation and write-back caching mechanisms on I/O operations. \n\033[93mThe test focuses on the behavior of initial writes, cache flushing, and transition \n\033[93mto read operations when a large file is created and accessed.\033[0m

        
File Creation Phase       Cache Flush Phase         Transition Point       Read Operations
      |                          |                        |                        |
      |                          |                        |                        |
      |   Inode & Initial        |                        |                        |
      |   Blocks Allocated       |                        |                        |
      |------------------------->|                        |                        |
      |                          |   Deferred Writes      |                        |
      |                          |   Flushed to Disk      |                        |
      |                          |----------------------->|                        |
      |                          |                        |   Write Operations     |
      |                          |                        |   Cease                |
      |                          |                        |----------------------->|
      |                          |                        |                        |
      |                          |                        |                        |
      |                          |                        |                        |
      |                          |                        |                        |
      |                          |                        |                        |
      |                          |                        |                        |
 Simultaneous Reads ------------>|----------------------->|----------------------->|
      |                          |                        |                        |
      |                          |                        |                        |
      |                          |                        |                        |
      |                          |                        |                        |
""",
        "Write on Buffer Cache": "\033[93mThis test aims to investigate Buffer Cache (page cache for IO)\033[0m",
        
        "Back to Main": "\033[93mThis option will take you back to the main menu.\033[0m"
    }
    return descriptions.get(menu_entry, "\033[92mNo description available.\033[0m")

def preview_networksbumenu(menu_entry):
    descriptions = {
        "Network IN (Single)": "\033[93mSingle socket packet receiver against Internet beacon.\033[0m",
        "Network OUT (Single)": "\033[93mSingle socket packet transmiter against Internet beacon.\033[0m",
        "Network IN (Multiple)": "\033[93mMulti socket packet receiver against Internet Beacon. \n\033[93mUser can define custom socket number.\033[0m",
        "Network OUT (Multiple)": "\033[93mMulti socket packet transmitter against Internet Beacon. \n\033[93mUser can define custom socket number.\033[0m",
        "Socket Exhaustion": "\033[93mOpen as many local TCP connections as possible to stress per-process and kernel limits.\033[0m",
        "Simulate Latencies": "\033[92mUnder development.\033[0",
        "Simulate disconnects": "\033[92mUnder development.\033[0",
        "Simulate packet loss": "\033[92mUnder development.\033[0",
        "Back to Main": "\033[93mThis option will take you back to the main menu.\033[0m"
    }
    return descriptions.get(menu_entry, "\033[92mNo description available.\033[0m")


