import urllib.request
import threading
import time


def run_network_in():
    continue_test = True
    file_url = "https://proof.ovh.net/files/100Mb.dat"

    def download_file(url):
        nonlocal continue_test
        data_received = 0
        start_time = time.time()
        while continue_test:
            with urllib.request.urlopen(url) as response:
                while True:
                    chunk = response.read(4096)
                    if not chunk:
                        break
                    data_received += len(chunk)
        elapsed_time = time.time() - start_time
        bandwidth = (data_received / elapsed_time) / (1024 * 1024)
        print(f"Download Bandwidth: {bandwidth:.2f} MB/s")

    def prompt_exit():
        nonlocal continue_test
        input("Press ENTER to stop the test.")
        continue_test = False

    download_thread = threading.Thread(target=download_file, args=(file_url,))
    download_thread.start()
    exit_thread = threading.Thread(target=prompt_exit)
    exit_thread.start()
    download_thread.join()
    exit_thread.join()


