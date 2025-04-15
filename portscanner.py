import socket
import time
import threading
import os
from tkinter import *
from tkinter import ttk, messagebox
from concurrent.futures import ThreadPoolExecutor, as_completed #Threads to make it scan ports faster.



def scan_port(ip, port): # Opens a socket -> Tries to connect to a specific port -> Prints if its open.
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET = IPv4, SOCK_STREAM = TCP.
        s.settimeout(0.5)
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


def start_scan():
    ip = ip_entry.get()
    try:
        start_port = int(start_port_entry.get())
        end_port = int(end_port_entry.get())
    except ValueError:
        messagebox.showerror("Input error", "Ports have to be numbers.")
        return
    
    if start_port > end_port:
        messagebox.showerror("Input error", "Start port must be less than end port")
        return
    
    # Empty the result-box.
    result_box.config(state=NORMAL)
    result_box.delete(1.0, END)
    result_box.insert(END, f"Scanning {ip} from port {start_port} to {end_port}...\n")
    result_box.config(state=DISABLED)

    # Start scanning with threads.
    thread = threading.Thread(target=run_scan, args=(ip, start_port, end_port))
    thread.start()

def run_scan(ip, start_port, end_port):
    start_time = time.time()
    total_ports = end_port - start_port + 1
    scanned = 0

    open_ports = []

    progress_bar["maximum"] = total_ports
    progress_bar["value"] = 0

    # Limited amount of threads for stability for weaker systems - feel free to change to whatever you wish. 
    # Futures creates a list of tasks for the thread pool to do -> Loops through each port -> For each port tells worker to run scan_port(ip, port) -> executor.submit schedules the work.
    # Tasks are stored in the futures list

    with ThreadPoolExecutor(max_workers=300) as executor : # with cleans up after its done
        futures = [executor.submit(scan_port, ip, port) for port in range (start_port, end_port + 1)]

        for future in as_completed(futures): # Waits for the tasks to finish 1 by 1 -> When done it gives us its future
            result = future.result()         # Result gets the acutal return value from the function itself -> if open (80, http) if closed None.
            scanned += 1                     # Keeps track of ports scanned
            progress_bar ["value"] = scanned # Updates progress-bar

            # If result is not None then the port is open -> Gets port and the service name -> Makes result box editable -> Prints the port info -> Locks result box again.

            if result:
                port, service = result
                result_box.config(state=NORMAL)
                result_box.insert(END, f"✓ Port {port} is OPEN ({service.upper()})\n", "open")
                result_box.config(state=DISABLED)

    # Stops timer
    end_time = time.time()
    duration = end_time - start_time

    result_box.config(state=NORMAL)
    result_box.config(END, f"\nScan complete in {duration:.2f} seconds.\n", "info")
    result_box.config(state=DISABLED)
    
# - GUI - #

root = Tk()
root.title("Ezi0 Port Scanner")
root.geometry("500x500")
root.resizable(False, False)

try :
    root.iconbitmap("icon.ico")
except:
    pass

# Inputs
frame = Frame(root)
frame.pack(pady=10)

Label(frame, text="Target IP :").grid(row=0, column=0, sticky=E)
ip_entry = Entry(frame)
ip_entry.grid(row=0, column=1, padx=5)

Label(frame, text="Start Port :").grid(row=1, column=0, sticky=E)
start_port_entry = Entry(frame)
start_port_entry.grid(row=1, column=1, padx=5)

Label(frame, text="End Port :").grid(row=2, column=0, sticky=E)
end_port_entry = Entry(frame)
end_port_entry.grid(row=2, column=1, padx=5)

# Button -> Links button to start_scan function
start_button = Button(root, width=20, height=2, text="Start Scan", borderwidth=0, bg="#1e1e1e", fg="white", font=("Lucida Console", 10), command=start_scan)
start_button.pack(pady=10)

# Progress bar
progress_bar = ttk.Progressbar(root, length=400)
progress_bar.pack(pady=5)

# Results box
result_box = Text(root, height=30, width=60, state=DISABLED, font=("Lucida Console", 10), bg="#1e1e1e", fg="#00ff00")
result_box.pack(pady=10, padx=10)

# Text styling
result_box.tag_config("open", foreground="#00ff00")
result_box.tag_config("info", foreground="#55aaff")

# Makes sure the code doesn't run in the background when closed.
def on_closing():
    root.destroy()
    os._exit(0)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

# (っ◔◡◔)っ ♥ by Ezi0 ♥