import threading
import socket
import time
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed #Threads to make it scan ports faster.
from ui.settings import init_settings
import core.config

settings = init_settings()

def scan_port(ip, port): # Opens a socket -> Tries to connect to a specific port -> Prints if its open.
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET = IPv4, SOCK_STREAM = TCP.
        s.settimeout(settings["timeout"])
        result = s.connect_ex((ip, port)) # Tries to connect to the port.
        s.close()

        if result == 0:
            try:
                service = socket.getservbyport(port) # Gets service name by port.
            except:
                service = "Unknown"
            return (port, service)
    except:
        return None


def start_scan(ip, start_port, end_port, on_progress=None, on_complete=None, on_error=None, on_update_progress=None):
    if start_port > end_port:
        on_error("Input error", "Start port must be less than end port")
        return
    
    global scan_completed
    scan_completed = False

    on_progress(f"Scanning {ip} from port {start_port} to {end_port}...\n")
    try: 
        thread = threading.Thread(target=run_scan, args=(ip, start_port, end_port, on_progress, on_complete, on_error, on_update_progress))
        thread.start()
        scan_completed = True

    except Exception as e:
        on_error("Scan error", str(e))


def run_scan(ip, start_port, end_port, on_progress=None, on_complete=None, on_error=None, on_update_progress=None):
    start_time = time.time()
    total_ports = end_port - start_port + 1
    scanned = 0
    open_ports = []

    # Limited amount of threads for stability for weaker systems - feel free to change to whatever you wish. 
    # Futures creates a list of tasks for the thread pool to do -> Loops through each port -> For each port tells worker to run scan_port(ip, port) -> executor.submit schedules the work.
    # Tasks are stored in the futures list

    with ThreadPoolExecutor(max_workers=settings["max_threads"]) as executor : # with cleans up after its done
        futures = [executor.submit(scan_port, ip, port) for port in range (start_port, end_port + 1)]

        for future in as_completed(futures): # Waits for the tasks to finish 1 by 1 -> When done it gives us its future
            result = future.result()         # Result gets the acutal return value from the function itself -> if open (80, http) if closed None.
            scanned += 1                     # Keeps track of ports scanned

            # If result is not None then the port is open -> Gets port and the service name -> Makes result box editable -> Prints the port info -> Locks result box again.

            if on_update_progress:
                on_update_progress(scanned, total_ports)
            
            if result:
                port, service = result
                open_ports.append((port, service))

                core.config.scan_results["target"] = ip
                core.config.scan_results["ports"].append({
                    "port": port, 
                    "service": service
                    }) # For exporting to output file 
                
                on_progress(f"✓ Port {port} is OPEN ({service.upper()})\n", "open")
                

    # Stops timer
    end_time = time.time()
    duration = end_time - start_time

    global scan_completed
    scan_completed = True

    on_complete(f"\nScan completed in {duration:.2f} seconds. (っ◔◡◔)っ\n", "info")

# - Tied to the start button - #

## def scantype(method):
##    if method == "Nmap":
##       start_nmap_scan()
##    else:
##        start_scan()
        
# - Nmap Integration - #


def run_nmap_scan_thread(ip, flags=None, custom=None, on_result=None, on_error=None, on_complete=None):
    command = ['nmap', ip]

    if flags:
        command += flags

    if custom:
        command += custom.split()
    
    try:
        result = subprocess.check_output(command, universal_newlines=True)
        if on_result:
            on_result(result)

    except Exception as e:
        if on_error:
            on_error(str(e))

    finally:
        if on_complete:
            on_complete()