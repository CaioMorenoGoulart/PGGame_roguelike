from scripts.style import *
from scripts.config import WIDTH, HEIGHT, STATE_PLAYER_SELECT, STATE_SETTINGS, STATE_CONTROLLS, STATE_EXIT

class Menu_screen:
    def __init__(self):
        self.id = "Menu"
        self.texts = {
            "Texts": [
                {
                    "Text": "Novo Jogo",
                    "Font_size": FONT_SIZE_MENU,
                    "Color": FONT_COLOR_MENU,
                    "Color_Hover": FONT_COLOR_HOVER,
                    "Border": FONT_BORDER_MENU,
                    "Border_Color": FONT_COLOR_BORDER_MENU,
                    "Border_Color_HOVER": FONT_COLOR_BORDER_HOVER,
                    "BG_Color": BG_TEXT_COLOR,
                    "Pos": (WIDTH // 2 - 100, HEIGHT // 2 - 50),
                    "Action": STATE_PLAYER_SELECT,
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
                    "Text": "Controles",
                    "Font_size": FONT_SIZE_MENU,
                    "Color": FONT_COLOR_MENU,
                    "Color_Hover": FONT_COLOR_HOVER,
                    "Border": FONT_BORDER_MENU,
                    "Border_Color": FONT_COLOR_BORDER_MENU,
                    "Border_Color_HOVER": FONT_COLOR_BORDER_HOVER,
                    "BG_Color": BG_TEXT_COLOR,
                    "Pos": (WIDTH // 2 - 100, HEIGHT // 2 + 90),
                    "Action": STATE_CONTROLLS,
                },
                {
                    "Text": "Sair",
                    "Font_size": FONT_SIZE_MENU,
                    "Color": FONT_COLOR_MENU,
                    "Color_Hover": FONT_COLOR_HOVER,
                    "Border": FONT_BORDER_MENU,
                    "Border_Color": FONT_COLOR_BORDER_MENU,
                    "Border_Color_HOVER": FONT_COLOR_BORDER_HOVER,
                    "BG_Color": BG_TEXT_COLOR,
                    "Pos": (WIDTH // 2 - 100, HEIGHT // 2 + 160),
                    "Action": STATE_EXIT,
                },
            ],
        }
        self.start_color = (0, 0, 0, 0),
        self.mid_color = (0, 0, 0, 0),
        self.end_color = (150, 0, 0, 200),
        import scripts.auto as auto
        self.buttons = auto.listing(self.texts)
        self.grad_boxes = auto.GradientBox(
                start_color= (0, 0, 150, 0),
                end_color= (0, 0, 150, 0),
                mid_color= (150, 0, 0, 200),
                width=WIDTH,
                height=HEIGHT,
                vertical=False
            )
        self.loopfinished1 = False
        self.loopfinished2 = False
        self.loopfinished3 = False

    def bg_animation(self, speed=0, speed2=0, speed3=0):
        import scripts.auto as auto
        auto.bg_animation(self, speed, speed2, speed3)

    def draw(self, screen, pos, var1 = any, var2 = any):
        self.grad_boxes.draw(screen)
        [i.draw(screen, pos, True, .1) for i in self.buttons]

menu = Menu_screen()