from tkinter import *
from tkinter import ttk, filedialog, messagebox, simpledialog
from tktooltip import ToolTip

def build_gui():
    root = Tk()
    root.title("Ezi0 Port Scanner")
    root.geometry("600x650")
    root.resizable(False, False)

    try :
        root.iconbitmap("assets/icon.ico")
    except:
        pass

    notebook = ttk.Notebook(root)
    scanner_tab = Frame(notebook)
    nmap_tab = Frame(notebook)
    settings_tab = Frame(notebook)

    notebook.add(scanner_tab, text="Scanner")
    notebook.add(nmap_tab, text="Nmap")
    notebook.add(settings_tab, text="Settings")
    notebook.pack(expand=True, fill="both")

    button_frame = Frame(scanner_tab)
    button_frame.pack()

    return {
        "root": root,
        "tabs": {
            "scanner": scanner_tab,
            "nmap": nmap_tab,
            "settings": settings_tab
        },
        "frames": {
            "button": button_frame
        },
        "notebook": notebook
    }
