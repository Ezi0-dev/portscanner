from tkinter import *
from tkinter import ttk, filedialog, messagebox, simpledialog
from core.config import scan_methods, nmap_flag_keys
from core.scanner import scantype
from core.export import save_results_dialog
import os
from tktooltip import ToolTip

def build_gui(settings):
    root = Tk()
    root.title("Ezi0 Port Scanner")
    root.geometry("600x650")
    root.resizable(False, False)

    checkbox_vars = {key: BooleanVar() for key in nmap_flag_keys}
    custom_args = StringVar()
    

    try :
        root.iconbitmap("assets/icon.ico")
    except:
        pass

    notebook = ttk.Notebook(root)
    scanner_tab = Frame(notebook)
    nmap_tab = Frame(notebook)
    settings_tab = Frame(notebook)

    notebook.add(scanner_tab, text="Scanner")
    notebook.add(nmap_tab, text="Nmap")
    notebook.add(settings_tab, text="Settings")
    notebook.pack(expand=True, fill="both")

    frame = Frame(scanner_tab)
    frame.pack(pady=10, padx=10)

    scan_method_label = Label(frame, text="Scan Method", font=("Segoe UI", 14, "bold"))
    scan_method_label.grid(row=0, column=0, columnspan=1, padx=73, sticky=E)
    ToolTip(scan_method_label, delay=1, msg="NOTE : Nmap must be installed and added to PATH in Windows in order to function")

    scan_method_entry_var = StringVar(master=root)
    scan_method_entry_var.set(settings["default_scan_method"])
    scan_method_entry = ttk.Combobox(frame, values=scan_methods, textvariable=scan_method_entry_var, font=("Segoe UI", 16), width=15, state="readonly")
    scan_method_entry.grid(row=1, column=0, sticky=E, padx=45, ipadx=1)
    ToolTip(scan_method_entry, delay=1, msg="NOTE : Nmap must be installed and added to PATH in Windows in order to function")

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

    button_frame = Frame(scanner_tab)
    button_frame.pack(pady=5, padx=10)

    method = scan_method_entry_var.get()
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


    def on_closing():
        root.destroy()
        os._exit(0)

    root.protocol("WM_DELETE_WINDOW", on_closing)

    return {
        "root": root,
        "notebook": notebook,
        "tabs": {
            "scanner": scanner_tab,
            "nmap": nmap_tab,
            "settings": settings_tab
        },
        "frames": {
            "main": frame,
            "button": button_frame
        },
        "widgets": {
            "ip_entry": ip_entry,
            "start_port_entry": start_port_entry,
            "end_port_entry": end_port_entry,
            "scan_method_entry": scan_method_entry,
            "scan_method_var": scan_method_entry_var
        }
    }
