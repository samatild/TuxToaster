import socket
import threading
import time
import random

# ANSI colors
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"


def run_network_simulate_latency() -> None:
    continue_test = True

    def prompt_exit() -> None:
        nonlocal continue_test
        input("Press ENTER to stop the test.")
        continue_test = False

    def ask_int(prompt: str, default: int) -> int:
        try:
            raw = input(f"{prompt} [{default}]: ").strip()
            return int(raw) if raw else default
        except Exception:
            return default

    def ask_str(prompt: str, default: str) -> str:
        raw = input(f"{prompt} [{default}]: ").strip()
        return raw or default

    print(
        f"{BOLD}{GREEN}Running LATENCY SIMULATOR (TCP proxy) — "
        f"press ENTER to stop.{RESET}"
    )

    target_host = ask_str("Target host", "example.com")
    target_port = ask_int("Target port", 80)
    listen_port = ask_int("Local listen port (0=auto)", 0)
    base_latency_ms = ask_int("Base latency (ms)", 100)
    jitter_ms = ask_int("Jitter (+/-, ms)", 50)

    # Track open sockets for cleanup
    open_sockets = []

    def relay(src: socket.socket, dst: socket.socket, label: str) -> None:
        buf_size = 4096
        while True:
            try:
                data = src.recv(buf_size)
                if not data:
                    break
                # Apply latency + jitter per-chunk
                jitter = random.uniform(-jitter_ms, jitter_ms)
                delay = max(0.0, (base_latency_ms + jitter) / 1000.0)
                time.sleep(delay)
                dst.sendall(data)
            except Exception:
                break

    def handle_client(client_sock: socket.socket) -> None:
        # Connect to target
        try:
            server_sock = socket.create_connection((target_host, target_port))
        except Exception as e:
            print(f"{RED}Connect failed: {e}{RESET}")
            try:
                client_sock.close()
            except Exception:
                pass
            return

        open_sockets.append(server_sock)

        # Start bidirectional relays
        t_up = threading.Thread(
            target=relay, args=(client_sock, server_sock, "c→s"), daemon=True
        )
        t_down = threading.Thread(
            target=relay, args=(server_sock, client_sock, "s→c"), daemon=True
        )
        t_up.start()
        t_down.start()

        # Wait for either direction to end
        t_up.join()
        t_down.join()

        for s in (client_sock, server_sock):
            try:
                s.close()
            except Exception:
                pass

    # Listen socket
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_sock.bind(("127.0.0.1", listen_port))
    listen_sock.listen(128)
    actual_addr = listen_sock.getsockname()
    print(
        f"Listening on {actual_addr[0]}:{actual_addr[1]} → "
        f"{target_host}:{target_port} with ~{base_latency_ms}±{jitter_ms} ms"
    )

    open_sockets.append(listen_sock)

    # Exit thread
    exit_thread = threading.Thread(target=prompt_exit)
    exit_thread.start()

    # Accept loop
    try:
        while continue_test:
            try:
                listen_sock.settimeout(0.5)
                client, _ = listen_sock.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            open_sockets.append(client)
            t = threading.Thread(target=handle_client, args=(client,), daemon=True)
            t.start()
    finally:
        try:
            listen_sock.close()
        except Exception:
            pass

        # Best-effort close
        for s in open_sockets:
            try:
                s.close()
            except Exception:
                pass

    exit_thread.join()

    try:
        input(f"{BOLD}Press ENTER to return to the menu…{RESET}")
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    run_network_simulate_latency()


