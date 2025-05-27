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

    with ThreadPoolExecutor(max_workers=settings["max_threads"]) as executor : # with cleans up after its done
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
                
                result_box.config(state=NORMAL, font=("Lucida Console", 15))
                result_box.insert(END, f"✓ Port {port} is OPEN ({service.upper()})\n", "open")
                result_box.config(state=DISABLED)  

    # Stops timer
    end_time = time.time()
    duration = end_time - start_time

    global scan_completed
    scan_completed = True

    result_box.config(state=NORMAL)
    result_box.insert(END, f"\nScan completed in {duration:.2f} seconds. (っ◔◡◔)っ\n", "info")
    result_box.config(state=DISABLED)
    save_button.config(state=NORMAL)
    start_button.config(state=NORMAL)

# - Tied to the start button - #

def scantype(method):
    if method == "Nmap":
        start_nmap_scan()
    else:
        start_scan()
        
# - Nmap Integration - #

def run_nmap_scan():
    progress_bar.start()
    global result_box
    target = ip_entry.get()
    command = ['nmap', target]

    for key, var in checkbox_vars.items():
        if var.get():
            command.append(nmap_flags[key])

    if custom_args.get():
        command += custom_args.get().split()
    
    try:
        result = subprocess.check_output(command, universal_newlines=True)
        result_box.config(state=NORMAL, font=("Lucida Console", 10))
        result_box.delete("1.0", END)
        result_box.insert(END, result)
        result_box.config(state=DISABLED)
        progress_bar.stop()

        global scan_completed
        scan_completed = True
        messagebox.showinfo("Scan Completed", "Nmap scan completed!")

    except Exception as e:
        result_box.insert(END, f"Nmap error {e}")


def start_nmap_scan():
    progress_bar.start()
    progress_bar.config(mode='indeterminate')
    thread = threading.Thread(target=run_nmap_scan_thread)
    thread.start()


def show_nmap_result(result):
    global result_box
    result_box.config(state=NORMAL, font=("Lucida Console", 10))
    result_box.delete("1.0", END)
    result_box.insert(END, result)


    result_box.insert(END, f"\nScan completed. (っ◔◡◔)っ\n", "info")
    result_box.config(state=DISABLED)
    result_box.update_idletasks()
    messagebox.showinfo("Scan Completed", "Nmap scan finished.")


def run_nmap_scan_thread():
    progress_bar.start()
    global result_box
    target = ip_entry.get()
    command = ['nmap', target]

    for key, var in checkbox_vars.items():
        if var.get():
            command.append(nmap_flags[key])

    if custom_args.get():
        command += custom_args.get().split()
    
    try:
        result = subprocess.check_output(command, universal_newlines=True)
        
        progress_bar.config(mode='determinate')
        root.after(0, lambda: show_nmap_result(result))

        global scan_completed
        scan_completed = True

    except Exception as e:
        root.after(0, lambda: show_nmap_result(f"Error: {e}"))

    finally:
        root.after(0, progress_bar.stop)