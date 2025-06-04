from tkinter import BooleanVar, StringVar

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