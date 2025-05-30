from tkinter import ttk, filedialog, messagebox, simpledialog

THEMES = {
    "Dark": {
        "bg": "#121212",
        "fg": "#e0e0e0",
        "button_bg": "#1e1e1e",
        "notebook_bg": "#121212",
        "button_fg": "#e0e0e0",
        "entry_bg": "#1e1e1e",
        "entry_fg": "#e0e0e0",
        "highlight": "#4c1d7e",
        "result_bg": "#1e1e1e",
        "result_fg": "#00ff00",
        "combobox_highlight": "#FF000000",
        "button_hover_bg": "#242424",
        "progress_bar": "#4c1d7e"
    },
    "Light": {
        "bg": "white",
        "fg": "#333333",
        "button_bg": "#e6e6e6",
        "button_fg": "#333333",
        "notebook_bg": "white",
        "entry_bg": "#e6e6e6",
        "entry_fg": "#000000",
        "highlight": "#191919",
        "result_bg": "#e6e6e6",
        "result_fg": "#333333",
        "combobox_highlight": "#FF000000",
        "button_hover_bg": "#b8b8b8",
        "progress_bar": "#00ff00"
    },
    "Cold": {
        "bg": "#F4EEFF",
        "fg": "#424874",
        "button_bg": "#DCD6F7",
        "button_fg": "#424874",
        "notebook_bg": "#F4EEFF",
        "entry_bg": "#DCD6F7",
        "entry_fg": "#000000",
        "highlight": "#A6B1E1",
        "result_bg": "#DCD6F7",
        "result_fg": "#424874",
        "combobox_highlight": "#FF000000",
        "button_hover_bg": "#b0abc6",
        "progress_bar": "#A6B1E1"
    }
}

# - Themes - #

from ui.settings import save_settings

def set_theme(theme_name, ui_elements, settings):
    theme = THEMES[theme_name]
    ui_elements["root"].config(bg=theme["bg"])
    
    for tab in ui_elements["tabs"]:
        tab.config(bg=theme["bg"])
    
    for frames in ui_elements["frames"]:
        frames.config(bg=theme["bg"])

    for entry in ui_elements["entries"]:
        entry.config(
        bg=theme["entry_bg"],
        fg=theme["entry_fg"],
        insertbackground=theme["highlight"],
        relief="flat",
        highlightthickness=1,
        highlightbackground=theme["highlight"],
        )

    for checkbutton in ui_elements["checkbuttons"]:
        if checkbutton.winfo_exists():
            checkbutton.config(bg=theme["bg"], fg=theme["fg"], activebackground=theme["bg"], activeforeground=theme["fg"], selectcolor=theme["entry_bg"])

    for label in ui_elements["labels"]:
        if label.winfo_exists():
            label.config(bg=theme["bg"], fg=theme["fg"])

    for Toplevel in ui_elements["export"]["toplevel"]:
        if Toplevel.winfo_exists():
            Toplevel.configure(bg=theme["bg"], borderwidth=0)

    for result_box in ui_elements["text_widgets"]:
        result_box.config(bg=theme["result_bg"], fg=theme["result_fg"])
        result_box.tag_config("open", foreground=theme["result_fg"])

    # Styles
    style = ttk.Style()
    style.theme_use("default")

    style.configure("TCombobox", fieldbackground=theme["entry_bg"], background=theme["entry_bg"], foreground=theme["entry_fg"], selectforeground=theme["fg"], selectbackground=theme["combobox_highlight"], insertbackground=theme["highlight"], relief="flat", highlightbackground=theme["highlight"])
    style.configure("TButton", background=theme["button_bg"], focuscolor=theme["button_bg"], foreground=theme["button_fg"], borderwidth=0, font=("Segoe UI", 14, "bold"))

    style.map("TCombobox", fieldbackground=[('focus', theme["entry_bg"])], borderwidth=[('readonly', 0)], highlightbackground=[('focus', theme["highlight"])], highlightcolor=[('focus', theme["highlight"])], highlightthickness=[('focus', 1)])
    style.map("TButton", background=[("active", theme["button_hover_bg"])])

    style.configure("TNotebook", background=theme["bg"], focuscolor=theme["notebook_bg"], borderwidth=0)
    style.configure("TNotebook.Tab", background=theme["notebook_bg"], font=("Segoe UI", 11), foreground=theme["fg"], borderwidth=0)
    style.map("TNotebook.Tab", background=[("selected", theme["entry_bg"])])

    style.configure("TProgressbar", background=theme["progress_bar"], borderwidth=0, troughcolor=theme["button_bg"])

    save_settings(settings)


def set_themexz(theme_name):
    theme = THEMES[theme_name]
    settings["default_theme"] = theme_name

    root.config(bg=theme["bg"])
    scanner_tab.config(bg=theme["bg"])
    settings_tab.config(bg=theme["bg"])
    button_frame.config(bg=theme["bg"])
    nmap_tab.config(bg=theme["bg"])

    style = ttk.Style()
    style.theme_use("default")

    style.configure("TCombobox", fieldbackground=theme["entry_bg"], background=theme["entry_bg"], foreground=theme["entry_fg"], selectforeground=theme["fg"], selectbackground=theme["combobox_highlight"], insertbackground=theme["highlight"], relief="flat", highlightbackground=theme["highlight"])
    style.configure("TButton", background=theme["button_bg"], focuscolor=theme["button_bg"], foreground=theme["button_fg"], borderwidth=0, font=("Segoe UI", 14, "bold"))

    style.map("TCombobox", fieldbackground=[('focus', theme["entry_bg"])], borderwidth=[('readonly', 0)], highlightbackground=[('focus', theme["highlight"])], highlightcolor=[('focus', theme["highlight"])], highlightthickness=[('focus', 1)])
    style.map("TButton", background=[("active", theme["button_hover_bg"])])

    style.configure("TNotebook", background=theme["bg"], focuscolor=theme["notebook_bg"], borderwidth=0)
    style.configure("TNotebook.Tab", background=theme["notebook_bg"], font=("Segoe UI", 11), foreground=theme["fg"], borderwidth=0)
    style.map("TNotebook.Tab", background=[("selected", theme["entry_bg"])])

    style.configure("TProgressbar", background=theme["progress_bar"], borderwidth=0, troughcolor=theme["button_bg"])

    entry_widgets = [ip_entry, start_port_entry, end_port_entry, default_ip_entry, default_start_port_entry,
                      default_end_port_entry, timeout_entry, threads_entry, nmap_custom_args_entry]

    for entry in entry_widgets:
        entry.config(
        bg=theme["entry_bg"],
        fg=theme["entry_fg"],
        insertbackground=theme["highlight"],
        relief="flat",
        highlightthickness=1,
        highlightbackground=theme["highlight"],
        )

    for checkbutton in checkbutton_widgets:
        if checkbutton.winfo_exists():
            checkbutton.config(bg=theme["bg"], fg=theme["fg"], activebackground=theme["bg"], activeforeground=theme["fg"], selectcolor=theme["entry_bg"])

    for label in label_widgets:
        if label.winfo_exists():
            label.config(bg=theme["bg"], fg=theme["fg"])

    for Toplevel in save_dialog_frame:
        if Toplevel.winfo_exists():
            Toplevel.configure(bg=theme["bg"], borderwidth=0)

    result_box.config(bg=theme["result_bg"], fg=theme["result_fg"])
    result_box.tag_config("open", foreground=theme["result_fg"])
    frame.config(bg=theme["bg"], borderwidth=0)
    settings_frame.config(bg=theme["bg"])
    nmap_settings_frame.config(bg=theme["bg"])
    save_settings(settings)