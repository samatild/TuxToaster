from .simple_term_menu import TerminalMenu
from ..cpu.single_core import run_single_core_stress
from ..cpu.all_cores import run_all_cores_stress
from ..cpu.custom_cpu import run_custom_cores_stress
from ..memory.mem_singlethread import run_memory_singlethread
from ..memory.mem_multithread import run_memory_multithread
from ..memory.mem_spikes import run_memory_spikes
from ..memory.mem_uncleangc import memory_runaway
from ..disk.disk_ioreads import run_ioreads
from ..disk.disk_iowrites import run_iowrites
from ..disk.disk_iorandomrw import run_iorandom
from ..disk.disk_iorw import run_iorw
from ..disk.disk_bwreads import run_bwreads
from ..disk.disk_bwwrites import run_bwwrites
from ..disk.disk_bwrandomrw import run_bwrandom
from ..disk.disk_bwrw import run_bwrw
from ..disk.disk_cachewriteswarmup import run_cachewriteswarmup
from ..disk.disk_buffcachewrites import run_iobuffwrites
from ..network.network_in import run_network_in
from ..network.network_out import run_network_out
from ..network.network_out_multi import run_network_out_multi_socket
from ..network.network_in_multi import run_network_in_multi_socket
from ..network.network_socket_exhaustion import run_socket_exhaustion
from ..network.network_simulate_latency import run_network_simulate_latency
from .banner import print_banner
from .descriptions import (
    preview_cpusbumenu,
    preview_memsbumenu,
    preview_disksbumenu,
    preview_networksbumenu,
)


def cpu_submenu():
    while True:
        print_banner()
        submenu_items = ["Single Core", "All Cores",
                         "Custom Number of Cores", "Back to Main"]
        submenu = TerminalMenu(submenu_items,
                               title="Main Menu > Cpu Stresser",
                               preview_command=preview_cpusbumenu,
                               preview_size=0.25,
                               preview_title="\033[91mDescription\033[0m"
                               )
        selected_option = submenu.show()
        if selected_option == 0:
            run_single_core_stress()
        elif selected_option == 1:
            run_all_cores_stress()
        elif selected_option == 2:
            run_custom_cores_stress()
        elif selected_option == 3:
            break
        if selected_option is None:
            break


def memory_submenu():
    while True:
        print_banner()
        submenu_items = ["Single Runaway Thread", "Multiple Runaway Threads",
                         "Memory spikes", "Unclean GC", "Back to Main"]
        submenu = TerminalMenu(submenu_items,
                               title="Main Menu > Memory",
                               preview_command=preview_memsbumenu,
                               preview_size=0.25,
                               preview_title="\033[91mDescription\033[0m"
                               )
        selected_option = submenu.show()
        if selected_option == 0:
            run_memory_singlethread()
        elif selected_option == 1:
            run_memory_multithread()
        elif selected_option == 2:
            run_memory_spikes()
        elif selected_option == 3:
            memory_runaway()
        elif selected_option == 4:
            break
        if selected_option is None:
            break


def disk_submenu():
    while True:
        print_banner()
        submenu_items = [
            "IOPS Reads",
            "IOPS Writes",
            "Random IOPS R/W",
            "IOPS 50-50 R/W",
            "Throughput Reads",
            "Throughput Writes",
            "Random Throughput R/W",
            "Throughput 50-50 R/W",
            "Read while write cache is getting flushed",
            "Write on Buffer Cache",
            "Back to Main",
        ]
        submenu = TerminalMenu(submenu_items,
                               title="Main Menu > Disk IO",
                               preview_command=preview_disksbumenu,
                               preview_size=0.75,
                               preview_title="\033[91mDescription\033[0m"
                               )
        selected_option = submenu.show()
        if selected_option == 0:
            run_ioreads()
        elif selected_option == 1:
            run_iowrites()
        elif selected_option == 2:
            run_iorandom()
        elif selected_option == 3:
            run_iorw()
        elif selected_option == 4:
            run_bwreads()
        elif selected_option == 5:
            run_bwwrites()
        elif selected_option == 6:
            run_bwrandom()
        elif selected_option == 7:
            run_bwrw()
        elif selected_option == 8:
            run_cachewriteswarmup()
        elif selected_option == 9:
            run_iobuffwrites()
        elif selected_option == 10:
            break
        if selected_option is None:
            break


def network_submenu():
    while True:
        print_banner()
        submenu_items = [
            "Network IN (Single)",
            "Network OUT (Single)",
            "Network IN (Multiple)",
            "Network OUT (Multiple)",
            "Socket Exhaustion",
            "Simulate Latencies",
            "Back to Main",
        ]
        submenu = TerminalMenu(submenu_items,
                               title="Main Menu > Network",
                               preview_command=preview_networksbumenu,
                               preview_size=0.75,
                               preview_title="\033[91mDescription\033[0m"
                               )
        selected_option = submenu.show()
        if selected_option == 0:
            run_network_in()
        elif selected_option == 1:
            run_network_out()
        elif selected_option == 2:
            run_network_in_multi_socket()
        elif selected_option == 3:
            run_network_out_multi_socket()
        elif selected_option == 4:
            run_socket_exhaustion()
        elif selected_option == 5:
            run_network_simulate_latency()
        elif selected_option == 6:
            break
        if selected_option is None:
            break

