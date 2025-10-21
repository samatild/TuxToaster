import socket
import threading
import time
try:
    import resource  # POSIX only
except Exception:  # pragma: no cover - non-POSIX systems
    resource = None  # type: ignore

# ANSI colors
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"


def run_socket_exhaustion():
    continue_test = True

    stats = {
        "opened": 0,
        "start": time.time(),
    }

    # Keep track of client sockets so they remain open
    open_client_sockets = []

    def server_thread_main(listen_sock: socket.socket):
        listen_sock.listen(1024)
        # Accept loop; keep accepted sockets referenced to avoid GC closing
        accepted = []
        while True:
            try:
                client, _ = listen_sock.accept()
                # Set keepalive low-cost options; not strictly required
                try:
                    client.setsockopt(
                        socket.SOL_SOCKET,
                        socket.SO_KEEPALIVE,
                        1,
                    )
                except OSError:
                    pass
                accepted.append(client)
            except OSError:
                # Socket closed during shutdown
                break

        for s in accepted:
            try:
                s.close()
            except OSError:
                pass

    def prompt_exit():
        nonlocal continue_test
        input("Press ENTER to stop the test.")
        continue_test = False

    msg_intro = (
        f"{BOLD}{GREEN}Running SOCKET EXHAUSTION — "
        f"press ENTER to stop.{RESET}"
    )
    print(msg_intro)

    # Optionally raise the soft RLIMIT_NOFILE to the hard limit to allow
    # opening more sockets within this process.
    if resource is not None:
        try:
            answer = input(
                "Increase this process open-file limit to hard limit? "
                "[y/N]: "
            ).strip().lower()
            if answer == "y":
                soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
                resource.setrlimit(resource.RLIMIT_NOFILE, (hard, hard))
                print(
                    "New RLIMIT_NOFILE soft/hard: "
                    f"{resource.getrlimit(resource.RLIMIT_NOFILE)}"
                )
        except Exception as e:  # best-effort; continue on failure
            print(f"{YELLOW}Could not adjust RLIMIT_NOFILE: {e}{RESET}")

    # Choose mode
    print("Select mode: [1] connections (default)  [2] bind listener ports")
    mode = input("Mode [1/2]: ").strip() or "1"

    if mode == "2":
        # Bind many listening sockets across a port range to reserve them
        try:
            start_port = int(input("Start port [1024]: ") or "1024")
            end_port = int(input("End port [12288]: ") or "12288")
        except Exception:
            start_port, end_port = 1024, 12288

        open_listeners = []

        exit_thread = threading.Thread(target=prompt_exit)
        exit_thread.start()

        last_report = 0
        for port in range(start_port, end_port + 1):
            if not continue_test:
                break
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(("0.0.0.0", port))
                s.listen(1)
                open_listeners.append(s)
                stats["opened"] += 1
                if stats["opened"] - last_report >= 100:
                    last_report = stats["opened"]
                    print(
                        f"Bound listeners: {stats['opened']} "
                        f"(last port {port})"
                    )
            except OSError:
                # Port already in use or not allowed; continue
                continue

        exit_thread.join()

        for s in open_listeners:
            try:
                s.close()
            except OSError:
                pass
    else:
        # Default: open many connections to a local server and keep them
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind(("127.0.0.1", 0))
        server_addr = server_sock.getsockname()

        srv_thread = threading.Thread(
            target=server_thread_main,
            args=(server_sock,),
            daemon=True,
        )
        srv_thread.start()

        exit_thread = threading.Thread(target=prompt_exit)
        exit_thread.start()

        last_report = 0
        error_msg = None
        exhausted = False

        while continue_test:
            try:
                c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                except OSError:
                    pass
                c.connect(server_addr)
                open_client_sockets.append(c)
                stats["opened"] += 1
                if stats["opened"] - last_report >= 100:
                    last_report = stats["opened"]
                    elapsed = max(0.001, time.time() - stats["start"])
                    rate = stats["opened"] / elapsed
                    msg = (
                        f"Opened sockets: {stats['opened']}, "
                        f"rate: {rate:.1f}/s"
                    )
                    print(msg)
            except OSError as e:
                error_msg = str(e)
                exhausted = True
                note = (
                    f"{YELLOW}Resource limit reached; keeping sockets open until "
                    f"you press ENTER.{RESET}"
                )
                print(note)
                break

        exit_thread.join()

        try:
            server_sock.close()
        except OSError:
            pass

        for s in open_client_sockets:
            try:
                s.close()
            except OSError:
                pass

    elapsed = max(0.001, time.time() - stats["start"])
    rate = stats["opened"] / elapsed
    summary = (
        f"{YELLOW}Total sockets opened: {stats['opened']} "
        f"in {elapsed:.2f}s ({rate:.1f}/s){RESET}"
    )
    print(summary)
    try:
        if error_msg:
            print(f"{RED}Stopped due to error: {error_msg}{RESET}")
    except NameError:
        # error_msg not defined in bind-listeners branch
        pass

    try:
        input(f"{BOLD}Press ENTER to return to the menu…{RESET}")
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    run_socket_exhaustion()

