from text_list import *
from config import WIDTH, HEIGHT, STATE_RESUME_GAME, RESOLUTION_OPTIONS, SCRENN_OPT, CONFIG

class Menu_screen:
    def __init__(self):
        self.id = "Configurações Pause"
        self.texts = {
            "Texts": [
                {
                    "Text": "Voltar ao jogo",
                    "Font_size": FONT_SIZE_MENU,
                    "Color": FONT_COLOR_MENU,
                    "Color_Hover": FONT_COLOR_HOVER,
                    "Border": FONT_BORDER_MENU,
                    "Border_Color": FONT_COLOR_BORDER_MENU,
                    "Border_Color_HOVER": FONT_COLOR_BORDER_HOVER,
                    "BG_Color": BG_TEXT_COLOR,
                    "Pos": (WIDTH // 2 - 100, HEIGHT // 2 + 20),
                    "Action": STATE_RESUME_GAME,
                },
            ],
        }
        import auto
        import elements
        self.dropdown = elements.Dropdown(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, RESOLUTION_OPTIONS, SCRENN_OPT, FONT_SIZE_MENU, FONT_COLOR_MENU, FONT_COLOR_HOVER)
        self.slide = [elements.Slider(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, CONFIG["music_volume"]),
                      elements.Slider(WIDTH // 2 - 100, HEIGHT // 2 + 170, 200, CONFIG["effects_volume"])]
        self.texts["Texts"].extend(
            [
                {
                "Text": f"Volume Música: {int(self.slide[0].value * 100)}%",
                "Font_size": FONT_SIZE_MENU,
                "Color": FONT_COLOR_MENU,
                "Color_Hover": FONT_COLOR_HOVER,
                "Border": FONT_BORDER_MENU,
                "Border_Color": FONT_COLOR_BORDER_MENU,
                "Border_Color_HOVER": FONT_COLOR_BORDER_HOVER,
                "BG_Color": "null",
                "Pos": (self.slide[0].x, self.slide[0].y - 20),
                "Action": "null",
                },
                {
                "Text": f"Volume Efeitos: {int(self.slide[1].value * 100)}%",
                "Font_size": FONT_SIZE_MENU,
                "Color": FONT_COLOR_MENU,
                "Color_Hover": FONT_COLOR_HOVER,
                "Border": FONT_BORDER_MENU,
                "Border_Color": FONT_COLOR_BORDER_MENU,
                "Border_Color_HOVER": FONT_COLOR_BORDER_HOVER,
                "BG_Color": "null",
                "Pos": (self.slide[1].x, self.slide[1].y - 20),
                "Action": "null",}
                ]
        )
        self.buttons = auto.listing(self.texts)

menu = Menu_screen()