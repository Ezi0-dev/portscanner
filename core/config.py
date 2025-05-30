from tkinter import BooleanVar, StringVar

SETTINGS_F = "../settings.json"

scan_methods = ["Socket", "Nmap"]
formats = ["txt", "csv", "json"]
themes = ["Dark", "Light", "Cold"]

scan_results = {
    "target": "", # Header for IP that was scanned.
    "ports" : []  # List of the ports
}

nmap_flag_keys = ["stealth", "os_detect", "version", "verbose"]

# Matching flags
nmap_flags = {
    "stealth": "-sS",
    "os_detect": "-O",
    "version": "-sV",
    "verbose": "-v"
}

# BooleanVars
def init_checkbox_vars():
    return {
        "stealth": BooleanVar(),
        "os_detect": BooleanVar(),
        "version": BooleanVar(),
        "verbose": BooleanVar()
    }

def init_custom_args():
    return StringVar()