from style import *
from config import WIDTH, HEIGHT, STATE_MENU, RESOLUTION_OPTIONS, SCRENN_OPT, MUSIC_VOL, EFFECT_VOL

class Menu_screen:
    def __init__(self):
        self.id = "Configurações"
        self.texts = {
            "Texts": [
                {
                "Text": "Voltar",
                "Font_size": FONT_SIZE_MENU,
                "Color": FONT_COLOR_MENU,
                "Color_Hover": FONT_COLOR_HOVER,
                "Border": FONT_BORDER_MENU,
                "Border_Color": FONT_COLOR_BORDER_MENU,
                "Border_Color_HOVER": FONT_COLOR_BORDER_HOVER,
                "BG_Color": BG_TEXT_COLOR,
                "Pos": (WIDTH // 2 - 100, HEIGHT // 2 + 20),
                "Action": STATE_MENU,
                },
                {
                "Text": "Volume Música:",
                "Font_size": FONT_SIZE_MENU,
                "Color": FONT_COLOR_MENU,
                "Color_Hover": FONT_COLOR_HOVER,
                "Border": FONT_BORDER_MENU,
                "Border_Color": FONT_COLOR_BORDER_MENU,
                "Border_Color_HOVER": FONT_COLOR_BORDER_HOVER,
                "BG_Color": "null",
                "Pos": (WIDTH // 2 - 100, HEIGHT // 2 + 80),
                "Action": "null",
                },
                {
                "Text": "Volume Efeitos:",
                "Font_size": FONT_SIZE_MENU,
                "Color": FONT_COLOR_MENU,
                "Color_Hover": FONT_COLOR_HOVER,
                "Border": FONT_BORDER_MENU,
                "Border_Color": FONT_COLOR_BORDER_MENU,
                "Border_Color_HOVER": FONT_COLOR_BORDER_HOVER,
                "BG_Color": "null",
                "Pos": (WIDTH // 2 - 100, HEIGHT // 2 + 130),
                "Action": "null",
                }
            ],
        }
        import auto
        import elements
        self.dropdown = elements.Dropdown(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, RESOLUTION_OPTIONS, SCRENN_OPT, FONT_SIZE_MENU, FONT_COLOR_MENU, FONT_COLOR_HOVER)
        self.buttons = auto.listing(self.texts)

menu = Menu_screen()