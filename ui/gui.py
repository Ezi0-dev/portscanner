def build_gui():

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