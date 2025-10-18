import socket
import threading
import time
global continue_test

# ANSI colors
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"

def run_network_out_multi_socket():
    # Global flag to control the test
    
    continue_test = True

    # Well-known public server (IP, port)
    server_ip, server_port = "8.8.8.8", 53  # Google DNS

    buffer_size = 4096  # 4KB

    # Ask the user for the number of sockets
    num_sockets = int(input("Enter the number of sockets to use: "))

    def send_data(ip, port):
        nonlocal continue_test
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = b"x" * buffer_size
        bytes_sent = 0
        start_time = time.time()

        while continue_test:
            client_socket.sendto(data, (ip, port))
            bytes_sent += len(data)

        elapsed_time = time.time() - start_time
        bandwidth = (bytes_sent / elapsed_time) / (1024 * 1024)  # in MB/s
        print(f"Upload Bandwidth per socket: {bandwidth:.2f} MB/s")

    def prompt_exit():
        nonlocal continue_test
        input("Press ENTER to stop the test.")
        continue_test = False

    print(f"{BOLD}{GREEN}Running NETWORK OUT (multi) — press ENTER to stop.{RESET}")

    # Start multiple sender threads
    sender_threads = []
    for _ in range(num_sockets):
        t = threading.Thread(target=send_data, args=(server_ip, server_port))
        t.start()
        sender_threads.append(t)

    # Start the exit prompt
    exit_thread = threading.Thread(target=prompt_exit)
    exit_thread.start()

    # Wait for threads to complete
    for t in sender_threads:
        t.join()
    exit_thread.join()

    try:
        input(f"{BOLD}Press ENTER to return to the menu…{RESET}")
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    run_network_out_multi_socket()


