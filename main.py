from ui.gui import build_gui
from ui.themes import set_theme
from ui.settings import init_settings

def main():
    settings = init_settings()
    ui = build_gui(settings)

    set_theme(settings["default_theme"], ui["root"], ui["notebook"], ui["tabs"], ui["frames"], ui["widgets"])
    ui["root"].mainloop()

if __name__ == "__main__":
    main()