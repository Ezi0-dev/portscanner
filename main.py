import tkinter as tk
from tkinter import ttk

from ui.gui import build_gui  # This returns the GUI elements
from core.settings import init_settings
from core.themes import set_theme
from core.scanner import run_scan, run_nmap_scan



def main():
    root = tk.Tk()
    root.title("Port Scanner")
    root.geometry("800x600")

    settings = init_settings()
    set_theme(root, settings.get("theme", "dark"))

    widgets = build_gui(root)

    def on_scan_click():
        target = widgets['ip_entry'].get()
        scan_type = widgets['scan_type'].get()

        if scan_type == "Nmap":
            run_nmap_scan(target, widgets)
        else:
            run_scan(target, widgets)

    widgets['scan_button'].configure(command=on_scan_click)

    root.mainloop()

if __name__ == "__main__":
    main()