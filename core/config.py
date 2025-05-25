SETTINGS_F = "../settings.json"

methods = ["Socket", "Nmap"]
formats = ["txt", "csv", "json"]
themes = ["Dark", "Light", "Cold"]
save_dialog_frame = []
checkbutton_widgets = []
label_widgets = []

scan_results = {
    "target": "", # Header for IP that was scanned.
    "ports" : []  # List of the ports
}

scan_completed = False 

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

# Matching flags
nmap_flags = {
    "stealth": "-sS",
    "os_detect": "-O",
    "version": "-sV",
    "verbose": "-v"
}