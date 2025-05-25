import socket
import time
import threading
import os
import csv, json
import subprocess
from tkinter import *
from tkinter import ttk, filedialog, messagebox, simpledialog
from tktooltip import ToolTip
from concurrent.futures import ThreadPoolExecutor, as_completed #Threads to make it scan ports faster.

SETTINGS_F = "settings.json"

THEMES = {
    "Dark": {
        "bg": "#121212",
        "fg": "#e0e0e0",
        "button_bg": "#1e1e1e",
        "notebook_bg": "#121212",
        "button_fg": "#e0e0e0",
        "entry_bg": "#1e1e1e",
        "entry_fg": "#e0e0e0",
        "highlight": "#4c1d7e",
        "result_bg": "#1e1e1e",
        "result_fg": "#00ff00",
        "combobox_highlight": "#FF000000",
        "button_hover_bg": "#242424",
        "progress_bar": "#4c1d7e"
    },
    "Light": {
        "bg": "white",
        "fg": "#333333",
        "button_bg": "#e6e6e6",
        "button_fg": "#333333",
        "notebook_bg": "white",
        "entry_bg": "#e6e6e6",
        "entry_fg": "#000000",
        "highlight": "#191919",
        "result_bg": "#e6e6e6",
        "result_fg": "#333333",
        "combobox_highlight": "#FF000000",
        "button_hover_bg": "#b8b8b8",
        "progress_bar": "#00ff00"
    },
    "Cold": {
        "bg": "#F4EEFF",
        "fg": "#424874",
        "button_bg": "#DCD6F7",
        "button_fg": "#424874",
        "notebook_bg": "#F4EEFF",
        "entry_bg": "#DCD6F7",
        "entry_fg": "#000000",
        "highlight": "#A6B1E1",
        "result_bg": "#DCD6F7",
        "result_fg": "#424874",
        "combobox_highlight": "#FF000000",
        "button_hover_bg": "#b0abc6",
        "progress_bar": "#A6B1E1"
    }
}

methods = ["Socket", "Nmap"]
formats = ["txt", "csv", "json"]
themes = ["Dark", "Light", "Cold"]
save_dialog_frame = []
checkbutton_widgets = []
label_widgets = []

scan_results = {
    "target": "", # Header for IP that was scanned.
    "ports" : []  # List of the ports
}

scan_completed = False 

def init_settings():
    default = {
        "timeout": 0.5,
        "max_threads": 300,
        "default_ip": "",
        "default_start_port": "",
        "default_end_port": "",
        "default_export_format": "txt",
        "default_theme": "Dark",
        "default_scan_method": "Socket"
    }
    if os.path.exists(SETTINGS_F):
        try:
            with open(SETTINGS_F, "r") as s:
                data = json.load(s)
                default.update(data)
        except:
            pass # Resets to default if error occurs.
    return default

def save_settings(settings):
    try:
        with open(SETTINGS_F, "w") as s:
            json.dump(settings, s, indent=4)
    except Exception as e:
        messagebox.showerror("Could not save settings", str(e))


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

def scantype():
    method = scan_method_entry_var.get()
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

------------------------------

def save_results_dialog():
    win = Toplevel(root)
    win.title("Save As")
    win.geometry("380x230")
    win.resizable(False, False)
    win.configure(bg=theme["bg"])

    results_window = win

    try:
        win.iconbitmap("assets/save.ico") # In case the user does not have the icon, the code runs anyway :P
    except:
        pass

    save_results_label = Label(win, bg=theme["bg"], fg=theme["fg"], text="Select export format:", font=("Segoe UI", 16, "bold"))
    save_results_label.pack(pady=10)

    format_type = StringVar()
    format_type.set(settings["default_export_format"]) # Selects the default.

    format_dropdown = ttk.Combobox(win, textvariable=format_type, values=formats, font=("Segoe UI", 14), state="readonly")
    format_dropdown.pack(pady=5)

    remember_type = BooleanVar()
    remember_check = Checkbutton(win, text="Remember", font=("Segoe UI", 14, "bold"), variable=remember_type, bg=theme["bg"], fg=theme["fg"], activebackground=theme["bg"], activeforeground=theme["fg"], selectcolor=theme["entry_bg"])
    remember_check.pack(pady=5)

    def confirm_format():
        active_format = format_type.get()
        if active_format in formats:
            if remember_type.get():
                settings["default_export_format"] = active_format
                save_settings(settings) # - Remembers and updates settings.json - #
            win.destroy()
            save_results(active_format)
        else:
            messagebox.showerror("Invalid Format", "Please enter a valid format.")
    
    save_dialog_button = ttk.Button(win, text="✔ Save", command=confirm_format)
    save_dialog_button.pack(pady=10, ipady=15, ipadx=35)

    # Ugly for now

    label_widgets.append(save_results_label)
    checkbutton_widgets.append(remember_check)
    save_dialog_frame.append(results_window)

    
def save_results(format_type):
    filetypes = {
        "txt": [("Text file", "*.txt")],
        "csv": [("CSV file", "*.csv")],
        "json": [("JSON file", "*.json")]
    }

    ext = format_type.lower() # File Extension.
    output = filedialog.asksaveasfilename(initialfile="output", defaultextension=settings["default_export_format"], filetypes=filetypes[ext]) # The output file.(path)
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

settings = init_settings()
root = Tk()
root.title("Ezi0 Port Scanner")
root.geometry("600x650")
root.resizable(False, False)

try :
    root.iconbitmap("assets/icon.ico")
except:
    pass

# - Themes - #

def set_theme(theme_name):
    theme = THEMES[theme_name]
    settings["default_theme"] = theme_name

    root.config(bg=theme["bg"])
    scanner_tab.config(bg=theme["bg"])
    settings_tab.config(bg=theme["bg"])
    button_frame.config(bg=theme["bg"])
    nmap_tab.config(bg=theme["bg"])

    style = ttk.Style()
    style.theme_use("default")

    style.configure("TCombobox", fieldbackground=theme["entry_bg"], background=theme["entry_bg"], foreground=theme["entry_fg"], selectforeground=theme["fg"], selectbackground=theme["combobox_highlight"], insertbackground=theme["highlight"], relief="flat", highlightbackground=theme["highlight"])
    style.configure("TButton", background=theme["button_bg"], focuscolor=theme["button_bg"], foreground=theme["button_fg"], borderwidth=0, font=("Segoe UI", 14, "bold"))

    style.map("TCombobox", fieldbackground=[('focus', theme["entry_bg"])], borderwidth=[('readonly', 0)], highlightbackground=[('focus', theme["highlight"])], highlightcolor=[('focus', theme["highlight"])], highlightthickness=[('focus', 1)])
    style.map("TButton", background=[("active", theme["button_hover_bg"])])

    style.configure("TNotebook", background=theme["bg"], focuscolor=theme["notebook_bg"], borderwidth=0)
    style.configure("TNotebook.Tab", background=theme["notebook_bg"], font=("Segoe UI", 11), foreground=theme["fg"], borderwidth=0)
    style.map("TNotebook.Tab", background=[("selected", theme["entry_bg"])])

    style.configure("TProgressbar", background=theme["progress_bar"], borderwidth=0, troughcolor=theme["button_bg"])

    entry_widgets = [ip_entry, start_port_entry, end_port_entry, default_ip_entry, default_start_port_entry,
                      default_end_port_entry, timeout_entry, threads_entry, nmap_custom_args_entry]

    for entry in entry_widgets:
        entry.config(
        bg=theme["entry_bg"],
        fg=theme["entry_fg"],
        insertbackground=theme["highlight"],
        relief="flat",
        highlightthickness=1,
        highlightbackground=theme["highlight"],
        )

    for checkbutton in checkbutton_widgets:
        if checkbutton.winfo_exists():
            checkbutton.config(bg=theme["bg"], fg=theme["fg"], activebackground=theme["bg"], activeforeground=theme["fg"], selectcolor=theme["entry_bg"])

    for label in label_widgets:
        if label.winfo_exists():
            label.config(bg=theme["bg"], fg=theme["fg"])

    for Toplevel in save_dialog_frame:
        if Toplevel.winfo_exists():
            Toplevel.configure(bg=theme["bg"], borderwidth=0)

    result_box.config(bg=theme["result_bg"], fg=theme["result_fg"])
    frame.config(bg=theme["bg"], borderwidth=0)
    result_box.tag_config("open", foreground=theme["result_fg"])
    settings_frame.config(bg=theme["bg"])
    nmap_settings_frame.config(bg=theme["bg"])
    save_settings(settings)

theme = THEMES[settings["default_theme"]]

# Tabs

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=5, pady=5)

scanner_tab = Frame(notebook)
notebook.add(scanner_tab, text="Scanner")

settings_tab = Frame(notebook)
notebook.add(settings_tab, text="Settings")

nmap_tab = Frame(notebook)
notebook.add(nmap_tab, text="Nmap Settings")

# - Scanner tab - #

frame = Frame(scanner_tab)
frame.pack(pady=10, padx=10)


# - Ugly and bad but works - #

def disable_tab(event=None):
    if scan_method_entry.get() == "Nmap":
        notebook.tab(2, state=NORMAL)
        start_port_entry.grid_remove()
        start_port_label.grid_remove()
        end_port_entry.grid_remove()
        end_port_label.grid_remove()

    else:
        notebook.tab(2, state=DISABLED)
        start_port_entry.grid()
        start_port_label.grid()
        end_port_entry.grid()
        end_port_label.grid()

scan_method_label = Label(frame, text="Scan Method", font=("Segoe UI", 14, "bold"))
scan_method_label.grid(row=0, column=0, columnspan=1, padx=73, sticky=E)
ToolTip(scan_method_label, delay=1, msg="NOTE : Nmap must be installed and added to PATH in Windows in order to function")

scan_method_entry_var = StringVar()
scan_method_entry_var.set(settings["default_scan_method"])
scan_method_entry = ttk.Combobox(frame, values=methods, textvariable=scan_method_entry_var, font=("Segoe UI", 16), width=15, state="readonly")
scan_method_entry.grid(row=1, column=0, sticky=E, padx=45, ipadx=1)
ToolTip(scan_method_entry, delay=1, msg="NOTE : Nmap must be installed and added to PATH in Windows in order to function")

scan_method_entry.bind("<<ComboboxSelected>>", disable_tab)

ip_entry_label = Label(frame, text="Target IP : ", font=("Segoe UI", 14, "bold"))
ip_entry_label.grid(row=0, column=1, sticky=E)
ip_entry = Entry(frame, bd=1, borderwidth=2, relief="solid", font=("Segoe UI", 12))
ip_entry.grid(row=0, column=2, padx=2, pady=3)
ip_entry.insert(0, settings["default_ip"])

start_port_label = Label(frame, text="Start Port : ", font=("Segoe UI", 14, "bold"))
start_port_label.grid(row=1, column=1, sticky=E)
start_port_entry = Entry(frame, bd=1, borderwidth=2, relief="solid", font=("Segoe UI", 12))
start_port_entry.grid(row=1, column=2, padx=2, pady=3)
start_port_entry.insert(0, str(settings["default_start_port"]))

end_port_label = Label(frame, text="End Port : ", font=("Segoe UI", 14, "bold"))
end_port_label.grid(row=2, column=1, sticky=E)
end_port_entry = Entry(frame, bd=1, borderwidth=2, font=("Segoe UI", 12))
end_port_entry.grid(row=2, column=2, padx=2, pady=3)
end_port_entry.insert(0, str(settings["default_end_port"]))

# Button -> Links button to start_scan and save_results

button_frame = Frame(scanner_tab, bg=theme["bg"])
button_frame.pack(pady=5, padx=10)

start_button = ttk.Button(button_frame, state=NORMAL, text="▶ Start Scan", command=scantype)
start_button.pack(side=RIGHT, ipady=15, ipadx=80, padx=(5, 0))

save_button = ttk.Button(button_frame, state=DISABLED, text="✔ Save Results", command=save_results_dialog)
save_button.pack(side=LEFT, ipady=15, ipadx=80, padx=(0, 5))

# - Progress bar - #

progress_bar = ttk.Progressbar(scanner_tab, length=570)
progress_bar.pack(pady=5, padx=10, ipady=5)

# - Results box - #

result_box = Text(scanner_tab, height=40, width=90, state=DISABLED, borderwidth=0, font=("Lucida Console", 15))
result_box.pack(pady=(5,10), padx=10)

# - Text styling - #

result_box.tag_config("info", font=("Segoe UI", 16), foreground="#4a0fac")

# - Settings Tab - #

settings_frame = Frame(settings_tab)
settings_frame.pack(pady=20, padx=10)

settings_label = Label(settings_frame, text="Settings", font=("Segoe UI", 18, "bold"))
settings_label.grid(row=0, column=0, columnspan=3, sticky='N', pady=(5, 10))

def create_labeled_entry(parent, label_text, row, default_value):
    label = Label(parent, text=label_text, font=("Segoe UI", 16))
    label.grid(row=row, column=0, sticky=E, padx=5, pady=5)
    entry = Entry(parent, bd=1, relief="solid", font=("Segoe UI", 16))
    entry.grid(row=row, column=1, sticky=W, padx=5, pady=5)
    entry.insert(0, str(default_value))
    label_widgets.append(label)
    return entry

timeout_entry = create_labeled_entry(settings_frame, "Timeout (sec):", 1, settings["timeout"])
threads_entry = create_labeled_entry(settings_frame, "Max Threads:", 2, settings["max_threads"])
default_ip_entry = create_labeled_entry(settings_frame, "Default IP:", 3, settings["default_ip"])
default_start_port_entry = create_labeled_entry(settings_frame, "Start Port:", 4, settings["default_start_port"])
default_end_port_entry = create_labeled_entry(settings_frame, "End Port:", 5, settings["default_end_port"])

ToolTip(threads_entry, msg="NOTE : Only affects Socket scanning.")

#  - Dropdowns (ugly) - #

default_theme_label = Label(settings_frame, text="Theme:", font=("Segoe UI", 16))
default_theme_label.grid(row=7, column=0, sticky=E, padx=5, pady=5)
default_theme_var = StringVar()
default_theme_var.set(settings["default_theme"])
default_theme_entry = ttk.Combobox(settings_frame, textvariable=default_theme_var, values=themes, font=("Segoe UI", 16), width=19, state="readonly")
default_theme_entry.grid(row=7, column=1, sticky=W, padx=5, pady=5, ipadx=1)

default_export_format_label = Label(settings_frame, text="Export Format:", font=("Segoe UI", 16))
default_export_format_label.grid(row=6, column=0, sticky=E, padx=5, pady=(60, 0))
default_export_format_var = StringVar()
default_export_format_var.set(settings["default_export_format"])
default_export_format_entry = ttk.Combobox(settings_frame, textvariable=default_export_format_var, values=formats, font=("Segoe UI", 16), width=19, state="readonly")
default_export_format_entry.grid(row=6, column=1, sticky=W, padx=5, pady=(60, 0), ipadx=1)

# - Nmap settings tab - #

nmap_settings_frame = Frame(nmap_tab)
nmap_settings_frame.pack(pady=20, padx=10)

# - Variables to store options - #

stealth_var = BooleanVar()
os_detect_var = BooleanVar()
version_var = BooleanVar()
verbose_var = BooleanVar()
custom_args = StringVar()

# BooleanVars
checkbox_vars = {
    "stealth": stealth_var,
    "os_detect": os_detect_var,
    "version": version_var,
    "verbose": verbose_var
}

# Matching flags
nmap_flags = {
    "stealth": "-sS",
    "os_detect": "-O",
    "version": "-sV",
    "verbose": "-v"
}
# - Widgets - #

nmap_label = Label(nmap_settings_frame, text="Nmap Scan Options", font=("Segoe UI", 18, "bold"))
nmap_label.pack(pady=5)

steath_check =Checkbutton(nmap_settings_frame, font=("Segoe UI", 16), text="Stealth Scan (-sS)", variable=stealth_var)
steath_check.pack(anchor='w')
os_check = Checkbutton(nmap_settings_frame, font=("Segoe UI", 16), text="OS Detection (-O)", variable=os_detect_var)
os_check.pack(anchor='w')
ver_check = Checkbutton(nmap_settings_frame, font=("Segoe UI", 16), text="Version Detection (-sV)", variable=version_var)
ver_check.pack(anchor='w')
verbose_check = Checkbutton(nmap_settings_frame, font=("Segoe UI", 16), text="Verbose Output (-v)", variable=verbose_var)
verbose_check.pack(anchor='w')

checkbutton_widgets.extend([steath_check, os_check, ver_check, verbose_check])

nmap_custom_args_label = Label(nmap_settings_frame, text="Custom Nmap Arguments:", font=("Segoe UI", 16))
nmap_custom_args_label.pack(pady=(10, 0))
nmap_custom_args_entry = Entry(nmap_settings_frame, textvariable=custom_args, width=40, font=("Segoe UI", 16))
nmap_custom_args_entry.pack(anchor='w', padx=10)




# - Save settings - #

def upd_save_settings():
    try:
        settings["timeout"] = float(timeout_entry.get())
        settings["max_threads"] = int(threads_entry.get())
        settings["default_ip"] = default_ip_entry.get()
        settings["default_start_port"] = int(default_start_port_entry.get())
        settings["default_end_port"] = int(default_end_port_entry.get())
        settings["default_export_format"] = default_export_format_entry.get().lower()
        settings["default_theme"] = default_theme_entry.get()
        settings["default_scan_method"] = scan_method_entry.get()

        save_settings(settings)
        
        ip_entry.delete(0, END)
        ip_entry.insert(0, settings["default_ip"])

        start_port_entry.delete(0, END)
        start_port_entry.insert(0, str(settings["default_start_port"]))

        end_port_entry.delete(0, END)    
        end_port_entry.insert(0, str(settings["default_end_port"]))

        messagebox.showinfo("Success", "Settings have been saved successfully")
    except ValueError:
        messagebox.showerror("Error", "Invalid input!")

save_settings_button = ttk.Button(settings_tab, text="Save Settings", command=upd_save_settings)
save_settings_button.pack(pady=10, ipady=20, ipadx=40)

# Removed refresh button, this is way better :3

default_theme_entry.bind("<<ComboboxSelected>>", lambda e: set_theme(default_theme_entry.get()))

# Hover effect

for label in [ip_entry_label, start_port_label, end_port_label, default_theme_label, default_export_format_label, scan_method_label
              ,nmap_label, nmap_custom_args_label, settings_label]:
    label_widgets.append(label)

disable_tab()
set_theme(settings["default_theme"])

# Makes sure the code doesn't run in the background when closed.
def on_closing():
    root.destroy()
    os._exit(0)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

# (っ◔◡◔)っ ♥ by Ezi0 ♥