from style import *
from config import WIDTH, HEIGHT, STATE_PLAYING, STATE_SETTINGS, STATE_MENU

class Menu_screen:
    def __init__(self):
        self.id = "GAME OVER"
        self.texts = {
            "Texts": [
                {
                    "Text": "Game Over",
                    "Font_size": FONT_SIZE_TITTLE,
                    "Color": FONT_COLOR_TITTLE,
                    "Color_Hover": FONT_COLOR_TITTLE,
                    "Border": 0,
                    "Border_Color": "",
                    "Border_Color_HOVER": FONT_COLOR_BORDER_TITTLE,
                    "BG_Color": "null",
                    "Pos": (WIDTH // 2 - 100, HEIGHT // 2 - 200),
                    "Action": "",
                },
                {
                    "Text": "Pontuação $pontuacao$",
                    "Font_size": FONT_SIZE_MENU,
                    "Color": FONT_COLOR_TITTLE,
                    "Color_Hover": FONT_COLOR_TITTLE,
                    "Border": 0,
                    "Border_Color": "",
                    "Border_Color_HOVER": FONT_COLOR_BORDER_TITTLE,
                    "BG_Color": "null",
                    "Pos": (WIDTH // 2 - 100, HEIGHT // 2 - 150),
                    "Action": "",
                },
                {
                    "Text": "Tempo De jogo $tempo$",
                    "Font_size": FONT_SIZE_MENU,
                    "Color": FONT_COLOR_TITTLE,
                    "Color_Hover": FONT_COLOR_TITTLE,
                    "Border": 0,
                    "Border_Color": "",
                    "Border_Color_HOVER": FONT_COLOR_BORDER_TITTLE,
                    "BG_Color": "null",
                    "Pos": (WIDTH // 2 - 100, HEIGHT // 2 - 100),
                    "Action": "",
                },
                {
                    "Text": "Jogar novamente",
                    "Font_size": FONT_SIZE_MENU,
                    "Color": FONT_COLOR_MENU,
                    "Color_Hover": FONT_COLOR_HOVER,
                    "Border": FONT_BORDER_MENU,
                    "Border_Color": FONT_COLOR_BORDER_MENU,
                    "Border_Color_HOVER": FONT_COLOR_BORDER_HOVER,
                    "BG_Color": BG_TEXT_COLOR,
                    "Pos": (WIDTH // 2 - 100, HEIGHT // 2 - 50),
                    "Action": STATE_PLAYING,
                },
                {
                    "Text": "Configurações",
                    "Font_size": FONT_SIZE_MENU,
                    "Color": FONT_COLOR_MENU,
                    "Color_Hover": FONT_COLOR_HOVER,
                    "Border": FONT_BORDER_MENU,
                    "Border_Color": FONT_COLOR_BORDER_MENU,
                    "Border_Color_HOVER": FONT_COLOR_BORDER_HOVER,
                    "BG_Color": BG_TEXT_COLOR,
                    "Pos": (WIDTH // 2 - 100, HEIGHT // 2 + 20),
                    "Action": STATE_SETTINGS,
                },
                {
                    "Text": "Voltar para o Menu",
                    "Font_size": FONT_SIZE_MENU,
                    "Color": FONT_COLOR_MENU,
                    "Color_Hover": FONT_COLOR_HOVER,
                    "Border": FONT_BORDER_MENU,
                    "Border_Color": FONT_COLOR_BORDER_MENU,
                    "Border_Color_HOVER": FONT_COLOR_BORDER_HOVER,
                    "BG_Color": BG_TEXT_COLOR,
                    "Pos": (WIDTH // 2 - 100, HEIGHT // 2 + 90),
                    "Action": STATE_MENU,
                },
            ],
        }
        import auto
        self.buttons = auto.listing(self.texts)

    def draw(self, screen, pos, score, time):
        for i in self.buttons:
            if "$pontuacao$" in i.text:
                i.text = i.text.replace("$pontuacao$", f"{score}")
            if "$tempo$" in i.text:
                i.text = i.text.replace("$tempo$", f"{time}")
            i.draw(screen, pos)
        [i.draw(screen, pos) for i in self.buttons]

menu = Menu_screen()