from ui.gui import build_gui
from ui.themes import set_theme
from ui.settings import init_settings

def main():
    ui = build_gui()
    settings = init_settings()
    set_theme(settings["default_theme"], ui["root"], ui["tabs"], ui["frames"])
    ui["root"].mainloop()

if __name__ == "__main__":
    main()