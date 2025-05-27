import json
import os

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