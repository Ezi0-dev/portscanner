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