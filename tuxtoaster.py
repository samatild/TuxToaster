from assets.simple_term_menu import TerminalMenu
from assets.submenus import *
from assets.banner import print_banner
from assets.descriptions import preview_menu
import os
import subprocess
import platform
import sys


def main():
    
    print_banner()

    menu_items = ["CPU", "Memory", "Disk",
                  "Network", "Multiple", "About", "Exit"]
    main_menu = TerminalMenu(
        menu_items,
        title="Main Menu",
        cycle_cursor=True,
        quit_keys=["q", "x", "escape"],
        preview_command=preview_menu,
        preview_size=0.5,
        preview_title="\033[91mDescription\033[0m",
        )

    while True:
        selected_option = main_menu.show()

        if selected_option == 0: 
            cpu_submenu()
        elif selected_option == 1:
            memory_submenu()
        elif selected_option == 2:
            disk_submenu()
        elif selected_option == 3:
            network_submenu()
        elif selected_option == 6:
            os.system('clear')
            exit(0)


if __name__ == "__main__":
    main()
