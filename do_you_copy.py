# Do You Copy?
# HTTP Probing CLI Tool

import os
import socket
import time
from urllib.parse import urlparse, urlunparse
import requests

def red(text: str) -> str:
    return f"\033[91m{text}\033[0m"

def yellow(text: str) -> str:
    return f"\033[93m{text}\033[0m"

def green(text: str) -> str:
    return f"\033[92m{text}\033[0m"

def bold(text: str) -> str:
    return f"\033[1m{text}\033[0m"

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input("\nPress Enter to continue...")

def qm_art():
    art = [
        "  _____   ",
        " |     |  ",
        " |     |  ",
        "     __|  ",
        "    |     ",
        "    |     ",
        "    .     "
    ]

    for line in art:
        print(yellow(bold((" " * 6) + line)))

def show_trademark():
    qm_art()
    print("-" * 20)
    print(
        yellow(
            bold(
                (" " * 4) + "Do You Copy?"
            )
        )
    )
    print("-" * 20)
    print(red(" By RavenTheBird789"))
    print("-" * 20)

def exit_animation():
    for dots in range(4):
        clear_screen()

        if dots == 0:
            print(green("Exiting"))
        else:
            print(green("Exiting" + "." * dots))

        time.sleep(0.15)

    clear_screen()

def parse_target_host(hostname: str):
    """Parse and validate a target hostname. Returns:parsed hostname object, or None if invalid.""" 

    if not hostname.startswith(("http://", "https://")):
        hostname = "https://" + hostname

    parsed = urlparse(hostname)

    if not parsed.hostname:
        return None

    return parsed


def build_target_host(parsed, port: int):
    """Rebuild the target hostname using a specified port."""

    scheme = parsed.scheme

    # Avoid explicitly adding the default port.
    if (scheme == "http" and port == 80) or (
        scheme == "https" and port == 443
    ):
        netloc = parsed.hostname
    else:
        netloc = f"{parsed.hostname}:{port}"

    return urlunparse(
        (
            scheme,
            netloc,
            parsed.path or "/",
            parsed.params,
            parsed.query,
            ""
        )
    )

def check_port(host: str, port: int, timeout: float = 3.0) -> bool:
    """Check whether a TCP port is accepting connections."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True

    except (socket.timeout, ConnectionRefusedError, OSError):
        return False

def basic_probe(target_host: str, count: int):
    """Send repeated GET requests to a hostname and display the server's response."""

    parsed = parse_target_host(target_host)

    if parsed is None:
        print(red("Invalid hostname."))
        return

    target_host = parsed.geturl()

    print(f"\nProbing: {target_host}")
    print(f"Number of requests: {count}\n")

    for i in range(1, count + 1):

        try:
            start_time = time.perf_counter()

            response = requests.get(
                target_host,
                timeout=5,
                allow_redirects=True
            )

            elapsed = (time.perf_counter() - start_time) * 1000

            status = response.status_code

            if 200 <= status < 300:
                status_message = green(
                    f"{status} {response.reason}"
                )

            elif 300 <= status < 400:
                status_message = yellow(
                    f"{status} {response.reason}"
                )

            elif 400 <= status < 500:
                status_message = yellow(
                    f"{status} {response.reason}"
                )

            elif 500 <= status < 600:
                status_message = red(
                    f"{status} {response.reason}"
                )

            else:
                status_message = yellow(
                    f"{status} {response.reason}"
                )

            print(
                f"{i}. {status_message} "
                f"({elapsed:.2f} ms)"
            )

        except requests.exceptions.Timeout:
            print(red(f"{i}. Request timed out."))

        except requests.exceptions.ConnectionError:
            print(red(f"{i}. Could not connect to the server."))

        except requests.exceptions.RequestException as error:
            print(red(f"{i}. Request error: {error}"))

def probe_http_methods(target_host: str, port: int):
    """
    Check a TCP port and then probe safe HTTP methods.
    """

    parsed = parse_target_host(target_host)

    if parsed is None:
        print(red("Invalid hostname."))
        return

    host = parsed.hostname

    print(f"\nChecking {host}:{port}...")

    if not check_port(host, port):
        print(red(f"Port {port} is closed or unreachable."))
        return

    print(green(f"Port {port} is open."))

    target_host = build_target_host(parsed, port)

    print(f"HTTP target: {target_host}\n")

    # These methods are useful for basic HTTP diagnostics.
    methods = ["GET", "HEAD", "OPTIONS"]

    for method in methods:

        try:
            start_time = time.perf_counter()

            response = requests.request(
                method,
                target_host,
                timeout=5,
                allow_redirects=False
            )

            elapsed = (time.perf_counter() - start_time) * 1000

            print(
                f"[{method:<7}] "
                f"{response.status_code} "
                f"{response.reason} "
                f"({elapsed:.2f} ms)"
            )

        except requests.exceptions.Timeout:
            print(red(f"[{method:<7}] Request timed out."))

        except requests.exceptions.ConnectionError:
            print(red(f"[{method:<7}] Connection failed."))

        except requests.exceptions.RequestException as error:
            print(red(f"[{method:<7}] Error: {error}"))

def probe_hosts_ports(target_host: str, start_port: int, end_port: int):
    """Probe every TCP port in the specified range."""

    parsed = parse_target_host(target_host)

    if parsed is None:
        print(red("Invalid hostname."))
        return

    host = parsed.hostname

    print(f"\nScanning {host}")
    print(f"Port range: {start_port}-{end_port}\n")

    open_ports = []

    for port in range(start_port, end_port + 1):

        if check_port(host, port, timeout=1.0):
            open_ports.append(port)
            print(green(f"[OPEN]   {port}"))

        else:
            print(red(f"[CLOSED] {port}"))

    print("\n" + "-" * 40)

    if open_ports:
        print(green("Open ports found:"))

        for port in open_ports:
            print(green(f"  • {port}"))

    else:
        print(yellow("No open ports found in the specified range."))

    print("-" * 40)

def main_menu():
    while True:
        user_query = input(
            "\nWould you like to return to the main menu? (yes/no): "
        ).lower().strip()
        if user_query == "yes":
            clear_screen()
            show_trademark()
            return
        elif user_query == "no":
            exit_animation()
            raise SystemExit
        else:
            print(red("Invalid input. Please enter yes or no."))

def trademark(main_function):
    def wrapper():
        show_trademark()
        main_function()
    return wrapper

@trademark
def main():
    while True:
        print("Option 1: HTTP Probe a hostname")
        print("Option 2: HTTP Probe a hostname and specific port")
        print("Option 3: TCP Probe a hostname and port range")
        print("Option 4: Exit")

        prompt = input(
            "\nPlease choose an option (1-4): "
        ).strip()

        if prompt == "1":

            clear_screen()

            target_host = input(
                "Enter the hostname you want to probe: "
            ).strip()

            try:
                count = int(
                    input(
                        "Enter the number of times to probe the hostname: "
                    )
                )

                if count <= 0:
                    raise ValueError

            except ValueError:
                print(red("Please enter a positive whole number."))
                pause()
                clear_screen()
                show_trademark()
                continue

            clear_screen()

            basic_probe(target_host, count)

            pause()
            clear_screen()
            show_trademark()

        elif prompt == "2":

            clear_screen()

            target_host = input(
                "Paste the hostname you want to probe: "
            ).strip()

            try:
                target_port = int(
                    input("Enter the specific port to probe: ")
                )

                if not 1 <= target_port <= 65535:
                    raise ValueError

            except ValueError:
                print(red("Port must be between 1 and 65535."))
                pause()
                clear_screen()
                show_trademark()
                continue

            clear_screen()

            probe_http_methods(
                target_host,
                target_port
            )

            pause()
            clear_screen()
            show_trademark()

        elif prompt == "3":

            clear_screen()

            target_host = input(
                "Paste the hostname you want to probe: "
            ).strip()

            try:
                start_port_input = input(
                    "Start port [0]: "
                ).strip()

                end_port_input = input(
                    "End port [1024]: "
                ).strip()

                start_port = (
                    int(start_port_input)
                    if start_port_input
                    else 0
                )

                end_port = (
                    int(end_port_input)
                    if end_port_input
                    else 1024
                )

                if not (
                    0 <= start_port <= 65535
                    and 0 <= end_port <= 65535
                    and start_port <= end_port
                ):
                    raise ValueError

            except ValueError:
                print(
                    red(
                        "Invalid port range. "
                        "Use values from 0-65535."
                    )
                )

                pause()
                clear_screen()
                show_trademark()
                continue

            clear_screen()

            probe_hosts_ports(
                target_host,
                start_port,
                end_port
            )

            pause()
            clear_screen()
            show_trademark()

        elif prompt == "4":
            exit_animation()
            raise SystemExit
        else:
            clear_screen()
            print(
                red(
                    "Invalid Input. "
                    "Please choose an option from 1-4."
                )
            )
            time.sleep(1)
            clear_screen()
            show_trademark()

if __name__ == "__main__":
    main()
