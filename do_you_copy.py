# Do You Copy?
# HTTP Probing CLI Tool

import socket
import time
import os
import requests
from urllib.parse import urlparse

def red(text: str) -> str:
    return f"\033[91m{text}\033[0m"

def yellow(text: str) -> str:
    return f"\033[93m{text}\033[0m"

def green(text: str) -> str:
    return f"\033[92m{text}\033[0m"

def bold(text: str) -> str:
    return f"\033[1m{text}\033[0m"

space = " "

def qm_art():
    art = ["  _____   ",
           " |     |  ",
           " |     |  ",
           "     __|",
           "    |  ",
           "    |  ",
           "    .  "]
    for line in art:
        print(yellow(bold((space * 6) + line)))

def basic_probe(target_url, enum):
    for _ in range(enum):
        response = requests.get(target_url)
        if response.status_code == 200:
            print(green(f"{target_url} is currently responding! Response: {response.status_code}"))
        elif response.status_code == 404:
            print(red(f"{target_url} is currently NOT responding! Response: {response.status_code}"))
        elif response.status_code == 429:
            print(red(f"You have hit or exceeded the rate limit for {target_url} Response: {response.status_code}"))
        else:
            print(yellow(f"Response: {response.status_code}"))

def check_port(host, port, timeout: float = 3.0) -> bool:
    """Check if a TCP port is open on the given host."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False

def probe_http_methods(url, port):
    """Probe a given URL and port with multiple HTTP methods and print the server's responses."""
    parsed = urlparse(url)
    host = parsed.netloc
    scheme = "https" if port == 443 else "http"

    if not host:
        print(red("Invalid URL"))
        return

    print(f"Checking port {port} on {host}...")
    if not check_port(host, port):
        print(red(f"Port {port} is closed or unreachable"))
        return

    print(green(f"Port {port} is open. Probing HTTP methods...\n"))

    methods = ["GET", "POST", "HEAD", "PUT", "DELETE", "OPTIONS", "PATCH"]
    for method in methods:
        try:
            # Construct full URL with custom port
            target_url = f"{scheme}://{host}:{port}{parsed.path or '/'}"
            response = requests.request(method, target_url, timeout=5)
            print(f"[{method}] {response.status_code} {response.reason}")
        except requests.exceptions.RequestException as e:
            print(red(f"[{method}] Error: {e}"))

def probe_urls_ports(target_url, start_port, end_port):
    """Probe a given URL and port with multiple HTTP methods and print the server's responses."""
    ports = list(range(start_port, end_port + 1))
    for port in ports:
        check_port(target_url, port)
        probe_http_methods(target_url, port)

def main_menu():
    user_query = input("Would you like to return to the main menu? (yes/no): ").lower().strip()
    if user_query == "yes":
        os.system("cls" if os.name == 'nt' else 'clear')
        print(green("Returning to the main menu"))
        time.sleep(0.05)
        os.system("cls" if os.name == 'nt' else 'clear')
        print(green("Returning to the main menu" + ("." * 1)))
        time.sleep(0.05)
        os.system("cls" if os.name == 'nt' else 'clear')
        print(green("Returning to the main menu" + ("." * 2)))
        time.sleep(0.05)
        os.system("cls" if os.name == 'nt' else 'clear')
        print(green("Returning to the main menu" + ("." * 3)))
        time.sleep(0.05)
        os.system("cls" if os.name == 'nt' else 'clear')
        main();
    elif user_query == "no":
        os.system("cls" if os.name == 'nt' else 'clear')
        print(green("Exiting"))
        time.sleep(0.05)
        os.system("cls" if os.name == 'nt' else 'clear')
        print(green("Exiting" + ("." * 1)))
        time.sleep(0.05)
        os.system("cls" if os.name == 'nt' else 'clear')
        print(green("Exiting" + ("." * 2)))
        time.sleep(0.05)
        os.system("cls" if os.name == 'nt' else 'clear')
        print(green("Exiting" + ("." * 3)))
        time.sleep(0.05)
        os.system("cls" if os.name == 'nt' else 'clear')
        os._exit(0);
    else:
        os.system("cls" if os.name == 'nt' else 'clear')
        print(red("Invalid Input. Returning to the main menu"))
        time.sleep(0.05)
        os.system("cls" if os.name == 'nt' else 'clear')
        print(red("Invalid Input. Returning to the main menu" + ("." * 1)))
        time.sleep(0.05)
        os.system("cls" if os.name == 'nt' else 'clear')
        print(red("Invalid Input. Returning to the main menu" + ("." * 2)))
        time.sleep(0.05)
        os.system("cls" if os.name == 'nt' else 'clear')
        print(red("Invalid Input. Returning to the main menu" + ("." * 3)))
        time.sleep(0.05)
        os.system("cls" if os.name == 'nt' else 'clear')
        main();

def trademark(main):
    def wrapper():
        qm_art()
        print("-" * 20)
        print(yellow(bold((space * 4) + "Do You Copy?")))
        print("-" * 20)
        print(red(space + "By RavenTheBird789"))
        print("-" * 20)
        main()
    return wrapper    

@trademark
def main():
    while True:
        print("Option 1: HTTP Probe a given link")
        print("Option 2: HTTP Probe a given link and specific port")
        print("Option 3: HTTP Probe a given link and a range of ports")
        print("Option 4: Exit")
        prompt = input("Please choose an option (1-4): ")
        if prompt == "1":
            os.system("cls" if os.name == 'nt' else 'clear')
            target_url = input("Paste the url you want to probe: ").strip()
            enum = int(input("Enter the number of times you want to probe the url: "))
            basic_probe(target_url, enum)
            main_menu()
        elif prompt == "2":
            os.system("cls" if os.name == 'nt' else 'clear')
            target_url = input("Paste the url you want to probe: ").strip()
            target_port = int(input("Enter the specific port you want to probe: "))
            check_port(target_url, target_port)
            probe_http_methods(target_url, target_port)
            main_menu()
        elif prompt == "3":
            os.system("cls" if os.name == 'nt' else 'clear')
            target_url = input("Paste the url you want to probe: ").strip()
            start_port = int(input("Start port: ") or 0)
            end_port = int(input("End Port: ") or 1024)
            probe_urls_ports(target_url, start_port, end_port)
            main_menu()
        elif prompt == "4":
            os.system("cls" if os.name == 'nt' else 'clear')
            print(green("Exiting"))
            time.sleep(0.5)
            os.system("cls" if os.name == 'nt' else 'clear')
            print(green("Exiting" + ("." * 1)))
            time.sleep(0.5)
            os.system("cls" if os.name == 'nt' else 'clear')
            print(green("Exiting" + ("." * 2)))
            time.sleep(0.5)
            os.system("cls" if os.name == 'nt' else 'clear')
            print(green("Exiting" + ("." * 3)))
            time.sleep(0.5)
            os.system("cls" if os.name == 'nt' else 'clear')
            os._exit(0);
        else:
            os.system("cls" if os.name == 'nt' else 'clear')
            print(red("Invalid Input"))
            time.sleep(3)
            os.system('cls' if os.name == "nt" else 'clear')
            main();

if __name__ == "__main__":
    main()