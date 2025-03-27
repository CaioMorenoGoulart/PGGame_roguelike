from scripts.style import *
from scripts.config import WIDTH, HEIGHT, STATE_MENU

class Menu_screen:
    def __init__(self):
        self.id = "Controles"
        self.texts = {
            "Texts": [
                {
                    "Text": "Controles",
                    "Font_size": FONT_SIZE_MENU,
                    "Color": FONT_COLOR_MENU,
                    "Color_Hover": FONT_COLOR_MENU,
                    "Border": 0,
                    "Border_Color": "",
                    "Border_Color_HOVER": (0,0,0,0),
                    "BG_Color": (0,0,0,0),
                    "Pos": (WIDTH // 2 - 100, HEIGHT // 2 - 50),
                    "height": FONT_SIZE_MENU,
                    "Action": "",
                },
                {
                    "Text": "Cima: W"
                    "\nEsquerda: A"
                    "\nBaixo: S"
                    "\nDireita: D"
                    "\nEsquiva: LSHIFT"
                    "\nAtirar: SPACE ou mouse 1",
                    "Font_size": FONT_SIZE_MENU,
                    "Color": FONT_COLOR_MENU,
                    "Color_Hover": FONT_COLOR_MENU,
                    "Border": 1,
                    "Border_Color": "",
                    "Border_Color_HOVER": (255,255,255,50),
                    "BG_Color": (255,255,255,100),
                    "Pos": (WIDTH // 2 - 150, HEIGHT // 2 - 10),
                    "height": FONT_SIZE_MENU*6,
                    "width": 300,
                    "dir": "left",
                    "Action": "",
                },
                {
                    "Text": "Voltar para o menu",
                    "Font_size": FONT_SIZE_MENU,
                    "Color": FONT_COLOR_MENU,
                    "Color_Hover": FONT_COLOR_HOVER,
                    "Border": FONT_BORDER_MENU,
                    "Border_Color": FONT_COLOR_BORDER_MENU,
                    "Border_Color_HOVER": FONT_COLOR_BORDER_HOVER,
                    "BG_Color": BG_TEXT_COLOR,
                    "Pos": (WIDTH // 2 - 100, HEIGHT // 2 + 200),
                    "Action": STATE_MENU,
                },
            ],
        }
        import scripts.auto as auto
        self.buttons = auto.listing(self.texts)

    def draw(self, screen, pos, var1 = any, var2 = any):
        [i.draw(screen, pos) for i in self.buttons]

menu = Menu_screen()