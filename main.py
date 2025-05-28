from ui.gui import build_gui
from ui.themes import set_theme
from ui.settings import init_settings

def main():
    settings = init_settings()
    ui_elements = build_gui(settings)

    set_theme(settings["default_theme"], ui_elements, settings)
    ui_elements["root"].mainloop()

if __name__ == "__main__":
    main()