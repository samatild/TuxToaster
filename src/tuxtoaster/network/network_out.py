import socket
import threading
import time
from time import sleep


def run_network_out():
    continue_test = True
    server_ip, server_port = "8.8.8.8", 53
    buffer_size = 4096

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
        bandwidth = (bytes_sent / elapsed_time) / (1024 * 1024)
        print(f"Upload Bandwidth: {bandwidth:.2f} MB/s")
        sleep(3)

    def prompt_exit():
        nonlocal continue_test
        input("Press ENTER to stop the test.")
        continue_test = False

    sender_thread = threading.Thread(target=send_data, args=(server_ip, server_port))
    sender_thread.start()
    exit_thread = threading.Thread(target=prompt_exit)
    exit_thread.start()
    sender_thread.join()
    exit_thread.join()


