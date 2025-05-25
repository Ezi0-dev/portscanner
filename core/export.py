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