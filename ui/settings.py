import json
import os

from tkinter import ttk, filedialog, messagebox, simpledialog
from tktooltip import ToolTip

from core.config import DEFAULT_SETTINGS, SETTINGS_FILE, themes


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

    if "default_theme" not in loaded or loaded["default_theme"] not in themes:
        loaded["default_theme"] = DEFAULT_SETTINGS["default_theme"]
        changed = True

    if changed:
        with open("settings.json", "w") as f:
            json.dump(loaded, f, indent=4)

    return loaded

def save_settings(settings):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
    except Exception as e:
        messagebox.showerror("Could not save settings", str(e))


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
    try:
        new_settings, error = retrieve_settings_entries(entry_refs)

        if error:
            messagebox.showerror("Error", error)
            return

        settings.update(new_settings)
        save_settings(settings)

        messagebox.showinfo("Success", "Settings have been saved successfully")
    except ValueError:
        messagebox.showerror("Error", "Invalid input!")


    