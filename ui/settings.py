import json
import os

from tkinter import ttk, filedialog, messagebox, simpledialog
from tktooltip import ToolTip

SETTINGS_FILE = "settings.json"

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


def retrieve_settings_entries(entry_refs):
    try:
        return {
            "timeout": float(entry_refs["timeout"].get()),
            "max_threads": int(entry_refs["threads"].get()),
            "default_ip": entry_refs["default_ip"].get(),
            "default_start_port": int(entry_refs["default_start_port"].get()),
            "default_end_port": int(entry_refs["default_end_port"].get()),
            "default_export_format": entry_refs["export_format"].get().lower(),
            "default_theme": entry_refs["theme"].get(),
            "default_scan_method": entry_refs["scan_method"].get(),
        }, None
    except ValueError:
        return None, "Invalid input"

# - Save settings - #

def update_settings(settings, entry_refs):
        new_settings, error = retrieve_settings_entries(entry_refs)

        settings.update(new_settings)
        save_settings(settings)

        messagebox.showinfo("Success", "Settings have been saved successfully")


    