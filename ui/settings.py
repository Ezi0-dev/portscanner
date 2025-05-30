import json
import os

from tkinter import ttk, filedialog, messagebox, simpledialog
from tktooltip import ToolTip

SETTINGS_FILE = "../settings.json"

DEFAULT_SETTINGS = {
    "timeout": 0.5,
    "max_threads": 300,
    "default_ip": "127.0.0.1",
    "default_start_port": "",
    "default_end_port": "",
    "default_export_format": "txt",
    "default_theme": "Dark",
    "default_scan_method": "Socket"
}

def init_settings():
    try:
        with open("settings.json", "r") as f:
            loaded = json.load(f)
    except FileNotFoundError:
        loaded = {}

    changed = False
    for key, value in DEFAULT_SETTINGS.items():
        if key not in loaded:
            loaded[key] = value
            changed = True

    if changed:
        with open("settings.json", "w") as f:
            json.dump(loaded, f, indent=4)

    return loaded

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

# - Save settings - #

def upd_save_settings(settings):
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