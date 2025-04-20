import socket
import time
import threading
import os
import csv, json
from tkinter import *
from tkinter import ttk, filedialog, messagebox, simpledialog
from concurrent.futures import ThreadPoolExecutor, as_completed #Threads to make it scan ports faster.

scan_completed = False 
scan_results = {
    "target": "", # Header for IP that was scanned.
    "ports" : []  # List of the ports
}


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
    global scan_completed
    scan_completed = False
    save_button.config(state=DISABLED)
    start_button.config(state=DISABLED)

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
                open_ports.append((port, service))

                scan_results["target"] = ip
                scan_results["ports"].append({
                    "port": port, 
                    "service": service
                    }) # For exporting to output file and
                
                result_box.config(state=NORMAL)
                result_box.insert(END, f"✓ Port {port} is OPEN ({service.upper()})\n", "open")
                result_box.config(state=DISABLED)  

    # Stops timer
    end_time = time.time()
    duration = end_time - start_time

    global scan_completed
    scan_completed = True

    result_box.config(state=NORMAL)
    result_box.insert(END, f"\nScan complete in {duration:.2f} seconds. (っ◔◡◔)っ\n", "info")
    result_box.config(state=DISABLED)
    save_button.config(state=NORMAL)
    start_button.config(state=NORMAL)


def save_results_dialog():
    format_type = simpledialog.askstring("Save As", "Enter file format (txt, csv, json):")

    if format_type and format_type.lower() in ["txt", "csv", "json"]:
        save_results(format_type.lower())
    else:
        messagebox.showerror("Invalid format", "Supported formats : 'txt', 'csv', 'json'")


def save_results(format_type):
    filetypes = {
        "txt": [("Text file", "*.txt")],
        "csv": [("CSV file", "*.csv")],
        "json": [("JSON file", "*.json")]
    }

    ext = format_type.lower() # File Extension.
    output = filedialog.asksaveasfilename(initialfile="output", defaultextension=f".{ext}", filetypes=filetypes[ext]) # The output file.(path)
    if not output:
        return 
    
    try:
        with open(output, "w", newline="") as f:
            if ext == "txt":
                f.write(f"Scan results for {scan_results['target']}\n")
                for item in scan_results["ports"]:
                    f.write(f"Port {item['port']} is OPEN ({item['service'].upper()})\n")
            elif ext == "csv":
                csvw = csv.writer(f) # CSVw writes in csv format.
                csvw.writerow(["Target", "Port", "Service"])
                for item in scan_results["ports"]:
                    csvw.writerow([scan_results["target"], item["port"], item["service"]])
            elif ext == "json":
                json.dump(scan_results, f, indent=4) # Indent to make it look nice.
        messagebox.showinfo("File Saved!", f"Output saved as {ext.upper()}")
    except Exception as e:
        messagebox.showerror("File could not be saved", str(e))

                    
# - GUI - #

root = Tk()
root.title("Ezi0 Port Scanner")
root.geometry("500x500")
root.resizable(False, False)

try :
    root.iconbitmap("icon.ico")
except:
    pass

# Tabs
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

scanner_tab = Frame(notebook)
notebook.add(scanner_tab, text="Scanner")

settings_tab = Frame(notebook)
notebook.add(settings_tab, text="Settings")

# Inputs
frame = Frame(scanner_tab)
frame.pack(pady=10)

ip_entry_label = Label(frame, text="Target IP:", font=("Lucida Console", 14, "bold"))
ip_entry_label.grid(row=0, column=0, sticky=E)
ip_entry = Entry(frame, bd=1, relief="solid", font=("Segoe UI", 10, "bold"))
ip_entry.grid(row=0, column=1, padx=2, pady=2)

start_port_label = Label(frame, text="Start Port:", font=("Lucida Console", 14, "bold"))
start_port_label.grid(row=1, column=0, sticky=E)
start_port_entry = Entry(frame, bd=1, relief="solid", font=("Segoe UI", 10, "bold"))
start_port_entry.grid(row=1, column=1, padx=2, pady=2)

end_port_label = Label(frame, text="End Port:", font=("Lucida Console", 14, "bold"))
end_port_label.grid(row=2, column=0, sticky=E)
end_port_entry = Entry(frame, bd=1, relief="solid", font=("Segoe UI", 10, "bold"))
end_port_entry.grid(row=2, column=1, padx=2, pady=2)

# Button -> Links button to start_scan and save_results
button_frame = Frame(scanner_tab)
button_frame.pack(pady=5, padx=10)

start_button = Button(button_frame, width=20, height=2, state=NORMAL, text="Start Scan", borderwidth=0, bg="#1e1e1e", fg="white", font=("Lucida Console", 12, "bold"), command=start_scan)
start_button.pack(side=RIGHT, padx=10)

save_button = Button(button_frame, width=20, height=2, state=DISABLED, text="Save Results", borderwidth=0, bg="#1e1e1e", fg="white", font=("Lucida Console", 12, "bold"), command=save_results_dialog)
save_button.pack(side=RIGHT, padx=10)

# Progress bar
progress_bar = ttk.Progressbar(scanner_tab, length=480)
progress_bar.pack(pady=5, padx=10)

# Results box
result_box = Text(scanner_tab, height=30, width=60, state=DISABLED, font=("Lucida Console", 12), bg="#1e1e1e", fg="#00ff00")
result_box.pack(pady=5, padx=10)

# Text styling
result_box.tag_config("open", foreground="#00ff00")
result_box.tag_config("info", foreground="#6600ff")

# Makes sure the code doesn't run in the background when closed.
def on_closing():
    root.destroy()
    os._exit(0)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

# (っ◔◡◔)っ ♥ by Ezi0 ♥