import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed #Threads to make it scan ports faster.
from colorama import init, Fore, Style # pip install colorama :D

# Colors.
init(autoreset=True)

target = input("Enter the IP address you wish to scan: ")
start_port = int(input("Enter start port: "))
end_port = int(input("Enter end port: "))

open_ports = []

# Progress-bar.
total_ports = end_port - start_port + 1
scanned = 0
bar_length = 40 

# Timer.
start_time = time.time()


def scan_port(port): # Opens a socket -> Tries to connect to a specific port -> Prints if its open.
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET = IPv4, SOCK_STREAM = TCP.
        s.settimeout(0.5)
        result = s.connect_ex((target, port)) # Tries to connect to the port.
        s.close()

        if result == 0:
            try:
                service = socket.getservbyport(port) # Gets service name by port.
            except:
                service = "Unknown"
            return (port, service)
    except:
        return None


with ThreadPoolExecutor(max_workers=100) as executor: # Max 100 threads. Slower but avoids taking too much resources from the system
    futures = [executor.submit(scan_port, port) for port in range(start_port, end_port + 1)] # Gives the thread pool a task.

    for future in as_completed(futures): # Gives results one at a time.
        result = future.result()

        # Updates progress-bar.
        scanned += 1
        filled_length = int(bar_length * scanned // total_ports)
        bar = "█" * filled_length + "-" * (bar_length - filled_length)
        print(Fore.LIGHTBLACK_EX + f"[{bar}]", end ="\r")


        if result:
            port, service = result
            print(Fore.GREEN + f"\n[OPEN] Port {port} ({service.upper()})")
            open_ports.append((port, service))

# Stops timer
end_time = time.time()
duration = end_time - start_time

print(Style.BRIGHT + "\n\nScan complete. Open ports :")
for port, service in open_ports:
    print(Fore.GREEN + f" - {port} ({service.upper()})")

print(Style.BRIGHT + Fore.MAGENTA + f"\nScan finished in {duration:.2f} seconds")

# (っ◔◡◔)っ ♥ by Ezi0 ♥