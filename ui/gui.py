import os
import threading

from tkinter import *
from tkinter import ttk, filedialog, messagebox, simpledialog
from tktooltip import ToolTip

from core.config import scan_methods, nmap_flag_keys, themes, formats, nmap_flags
from core.scanner import start_scan, run_nmap_scan_thread
from core.export import save_results_dialog
from ui.settings import update_settings
from ui.themes import THEMES, set_theme

def build_gui(settings):
    root = Tk()
    root.title("Sentry")
    root.geometry("600x650")
    root.resizable(False, False)

    theme_name = settings.get("default_theme", "Dark")
    theme = THEMES[theme_name]

    notebook = ttk.Notebook(root)

    # - Append UI elements later - #
    
    ui_elements = {
        "root": root,
        "notebook": notebook,
        "tabs": [],
        "frames": [],
        "entries": [],
        "labels": [],
        "text_widgets": [],
        "checkbuttons": [],
        "toplevel": []
    }

    checkbox_vars = {key: BooleanVar() for key in nmap_flag_keys}
    custom_args = StringVar()
    
    try :
        root.iconbitmap("assets/icon.ico")
    except:
        pass

    # - Tabs - #

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

    scan_method_label = Label(frame, text="Scan Method", font=("Segoe UI", 14, "bold"))
    scan_method_label.grid(row=0, column=0, columnspan=1, padx=73, sticky=E)
    ToolTip(scan_method_label, delay=1, msg="NOTE : Nmap must be installed and added to PATH in Windows in order to function")

    scan_method_entry_var = StringVar(master=root)
    scan_method_entry_var.set(settings["default_scan_method"])
    scan_method_entry = ttk.Combobox(frame, values=scan_methods, textvariable=scan_method_entry_var, font=("Segoe UI", 16), width=15, state="readonly")
    scan_method_entry.grid(row=1, column=0, sticky=E, padx=45, ipadx=1)
    ToolTip(scan_method_entry, delay=1, msg="NOTE : Nmap must be installed and added to PATH in Windows in order to function")

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

    button_frame = Frame(scanner_tab)
    button_frame.pack(pady=5, padx=10)

    # - Start button function - #

    def scantype():
        method = scan_method_entry_var.get()
        result_box.config(state=NORMAL)
        result_box.delete(1.0, END)
        result_box.config(state=DISABLED)
        
        if method == "Nmap":
            try:
                ip = ip_entry.get()
                flags = [nmap_flags[k] for k, var in checkbox_vars.items() if var.get()]
                custom = custom_args.get()

            except Exception as e:
                messagebox.showerror("Error", str(e))
                return
            
            progress_bar.config(mode='indeterminate')
            progress_bar.start()

            def show_nmap_result(result):
                result_box.config(state=NORMAL, font=("Lucida Console", 10))
                result_box.delete("1.0", END)
                result_box.insert(END, result)


                result_box.insert(END, f"\nScan completed. (っ◔◡◔)っ\n", "info")
                result_box.config(state=DISABLED)
                result_box.update_idletasks()
                messagebox.showinfo("Scan Completed", "Nmap scan finished.")
            
            def thread_target():
                run_nmap_scan_thread(
                    ip=ip,
                    flags=flags,
                    custom=custom,
                    on_result=lambda result: root.after(0, lambda: show_nmap_result(result)),
                    on_error=lambda err: root.after(0, lambda: show_nmap_result(f"Error: {err}")),
                    on_complete=lambda: root.after(0, progress_bar.stop)
            )
            
            thread = threading.Thread(target=thread_target)
            thread.start()

        else:
            try:
                ip = ip_entry.get()
                start_port = int(start_port_entry.get())
                end_port = int(end_port_entry.get())
            except ValueError:
                messagebox.showerror("Input error", "Ports must be numbers.")
                return
            
            def update_result_box(msg):
                result_box.config(state=NORMAL)
                result_box.insert(END, msg)
                result_box.config(state=DISABLED)
            
            def update_progress(scanned, total):
                progress_bar["maximum"] = total
                progress_bar["value"] = scanned
            
            def on_complete(msg):
                result_box.tag_config("info", font=("Segoe UI", 16), foreground="#4a0fac")
                result_box.config(state=NORMAL)
                result_box.insert(END, msg, "info")
                result_box.config(state=DISABLED)
                save_button.config(state=NORMAL)
                start_button.config(state=NORMAL)
            
            start_scan(
                ip,
                start_port,
                end_port,
                on_progress=lambda msg, tag=None: update_result_box(msg),
                on_complete=lambda msg, tag=None: on_complete(msg),
                on_error=lambda title, msg: messagebox.showerror(title, msg),
                on_update_progress=lambda scanned, total: update_progress(scanned, total)
            )

    def export():
        save_results_dialog(root, theme, settings, formats, ui_elements)
            
    start_button = ttk.Button(button_frame, state=NORMAL, text="▶ Start Scan", command=scantype)
    start_button.pack(side=RIGHT, ipady=15, ipadx=80, padx=(5, 0))

    save_button = ttk.Button(button_frame, state=DISABLED, text="✔ Save Results", command=export)
    save_button.pack(side=LEFT, ipady=15, ipadx=80, padx=(0, 5))

    ToolTip(save_button, delay=1, msg="NOTE : Works only for SOCKET scanning.")

    # - Progress bar - #

    progress_bar = ttk.Progressbar(scanner_tab, length=570)
    progress_bar.pack(pady=5, padx=10, ipady=5)

    # - Results box - #

    result_box = Text(scanner_tab, height=40, width=90, state=DISABLED, borderwidth=0, font=("Lucida Console", 15))
    result_box.pack(pady=(5,10), padx=10)
    ui_elements["text_widgets"].append(result_box)

    # - Settings Tab - #

    settings_frame = Frame(settings_tab)
    settings_frame.pack(pady=20, padx=10)

    settings_label = Label(settings_frame, text="Settings", font=("Segoe UI", 18, "bold"))
    settings_label.grid(row=0, column=0, columnspan=3, sticky='N', pady=(5, 10))

    # - Only creates settings for now - #

    def create_labeled_entry(parent, label_text, row, default_value, ui_elements):
        label = Label(parent, text=label_text, font=("Segoe UI", 16))
        label.grid(row=row, column=0, sticky=E, padx=5, pady=5)
        
        entry = Entry(parent, bd=1, relief="solid", font=("Segoe UI", 16))
        entry.grid(row=row, column=1, sticky=W, padx=5, pady=5)
        entry.insert(0, str(default_value))

        ui_elements["labels"].append(label)

        return entry

    timeout_entry = create_labeled_entry(settings_frame, "Timeout (sec):", 1, settings["timeout"], ui_elements)
    threads_entry = create_labeled_entry(settings_frame, "Max Threads:", 2, settings["max_threads"], ui_elements)
    default_ip_entry = create_labeled_entry(settings_frame, "Default IP:", 3, settings["default_ip"], ui_elements)
    default_start_port_entry = create_labeled_entry(settings_frame, "Start Port:", 4, settings["default_start_port"], ui_elements)
    default_end_port_entry = create_labeled_entry(settings_frame, "End Port:", 5, settings["default_end_port"], ui_elements)

    ToolTip(threads_entry, msg="NOTE : Only affects Socket scanning.")

    if settings["default_theme"] not in themes:
        settings["default_theme"] = themes[0]
    if settings["default_export_format"] not in formats:
        settings["default_export_format"] = formats[0]

    #  - Dropdowns (ugly) - #

    default_theme_label = Label(settings_frame, text="Theme:", font=("Segoe UI", 16))
    default_theme_label.grid(row=7, column=0, sticky=E, padx=5, pady=5)
    default_theme_var = StringVar(master=root)
    default_theme_var.set(settings["default_theme"])
    default_theme_entry = ttk.Combobox(settings_frame, textvariable=default_theme_var, values=themes, font=("Segoe UI", 16), width=19, state="readonly")
    default_theme_entry.grid(row=7, column=1, sticky=W, padx=5, pady=5, ipadx=1)

    default_export_format_label = Label(settings_frame, text="Export Format:", font=("Segoe UI", 16))
    default_export_format_label.grid(row=6, column=0, sticky=E, padx=5, pady=(60, 0))
    default_export_format_var = StringVar(master=root)
    default_export_format_var.set(settings["default_export_format"])
    default_export_format_entry = ttk.Combobox(settings_frame, textvariable=default_export_format_var, values=formats, font=("Segoe UI", 16), width=19, state="readonly")
    default_export_format_entry.grid(row=6, column=1, sticky=W, padx=5, pady=(60, 0), ipadx=1)

    # - Ugly asf i cba - #

    settings_entries = {
        "timeout": timeout_entry,
        "threads": threads_entry,
        "default_ip": default_ip_entry,
        "default_start_port": default_start_port_entry,
        "default_end_port": default_end_port_entry,
        "export_format": default_export_format_entry,
        "theme": default_theme_entry,
        "scan_method": scan_method_entry,
    }

    def upd_settings():

        # - Insanely stupid but it works - #
        
        theme = default_theme_var.get()
        export = default_export_format_var.get()
        update_settings(settings, settings_entries)

    save_settings_button = ttk.Button(settings_tab, text="Save Settings", command=upd_settings)
    save_settings_button.pack(pady=10, ipady=20, ipadx=40)

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

    ui_elements["checkbuttons"].extend([steath_check, os_check, ver_check, verbose_check])

    nmap_custom_args_label = Label(nmap_settings_frame, text="Custom Nmap Arguments:", font=("Segoe UI", 16))
    nmap_custom_args_label.pack(pady=(10, 0))
    nmap_custom_args_entry = Entry(nmap_settings_frame, textvariable=custom_args, width=40, font=("Segoe UI", 16))
    nmap_custom_args_entry.pack(anchor='w', padx=10)

    # Removed refresh button, this is way better :3
    default_theme_entry.bind("<<ComboboxSelected>>", lambda e: set_theme(default_theme_entry.get(), ui_elements, settings))

    for frames in [frame, button_frame, settings_frame, nmap_settings_frame]:
        ui_elements["frames"].append(frames)

    for tabs in [scanner_tab, nmap_tab, settings_tab]:
        ui_elements["tabs"].append(tabs)

    for entries in [ip_entry, start_port_entry, end_port_entry, default_ip_entry, default_start_port_entry, 
                    default_end_port_entry, timeout_entry, threads_entry, nmap_custom_args_entry,]:
        ui_elements["entries"].append(entries)

    for label in [ip_entry_label, start_port_label, end_port_label, default_theme_label, default_export_format_label,
                   scan_method_label, nmap_label, settings_label, nmap_custom_args_label]:
        ui_elements["labels"].append(label)

    disable_tab()

    def on_closing():
        root.destroy()
        os._exit(0)

    root.protocol("WM_DELETE_WINDOW", on_closing)

    return ui_elements
