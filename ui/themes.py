
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

from ui.settings import save_settings, init_settings

def set_theme(theme_name, root, tabs, frames):
    settings = init_settings()
    theme = THEMES.get(theme_name, THEMES["Dark"])

    settings["default_theme"] = theme_name
    root.configure(bg=theme["bg"])

    for tab in tabs.values():
        tab.configure(bg=theme["bg"])
    for frame in frames.values():
        frame.configure(bg=theme["bg"])

    save_settings(settings)