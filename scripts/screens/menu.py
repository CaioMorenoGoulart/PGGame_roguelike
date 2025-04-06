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

    def bg_animation(self, speed = 0, speed2 = 0, speed3 = 0):

        if speed > 0:
            if self.grad_boxes.start_color[3] < 255 and self.loopfinished1 == False:
                self.grad_boxes.start_color= (self.grad_boxes.start_color[0], self.grad_boxes.start_color[1], self.grad_boxes.start_color[2], min(255,self.grad_boxes.start_color[3] + speed))
            if self.grad_boxes.start_color[3] == 255:
                self.loopfinished1 = True
            if self.grad_boxes.start_color[3] <= 0:
                self.loopfinished1 = False
            if self.grad_boxes.start_color[3] > 0 and self.loopfinished1 == True:
                self.grad_boxes.start_color= (self.grad_boxes.start_color[0], self.grad_boxes.start_color[1], self.grad_boxes.start_color[2], max(0,self.grad_boxes.start_color[3] - speed))
        if speed2 > 0:
            if self.grad_boxes.mid_color[3] < 255 and self.loopfinished2 == False:
                self.grad_boxes.mid_color= (self.grad_boxes.mid_color[0], self.grad_boxes.mid_color[1], self.grad_boxes.mid_color[2], min(255,self.grad_boxes.mid_color[3] + speed2))
            if self.grad_boxes.mid_color[3] == 255:
                self.loopfinished2 = True
            if self.grad_boxes.mid_color[3] <= 0:
                self.loopfinished2 = False
            if self.grad_boxes.mid_color[3] > 0 and self.loopfinished2 == True:
                self.grad_boxes.mid_color= (self.grad_boxes.mid_color[0], self.grad_boxes.mid_color[1], self.grad_boxes.mid_color[2], max(0,self.grad_boxes.mid_color[3] - speed2))
        if speed3 > 0:
            if self.grad_boxes.end_color[3] < 255 and self.loopfinished3 == False:
                self.grad_boxes.end_color= (self.grad_boxes.end_color[0], self.grad_boxes.end_color[1], self.grad_boxes.end_color[2], min(255,self.grad_boxes.end_color[3] + speed3))
            if self.grad_boxes.end_color[3] == 255:
                self.loopfinished3 = True
            if self.grad_boxes.end_color[3] <= 0:
                self.loopfinished3 = False
            if self.grad_boxes.end_color[3] > 0 and self.loopfinished3 == True:
                self.grad_boxes.end_color= (self.grad_boxes.end_color[0], self.grad_boxes.end_color[1], self.grad_boxes.end_color[2], max(0,self.grad_boxes.end_color[3] - speed3))

        if speed + speed2 + speed3 > 0:
            self.grad_boxes.create_gradient()

    # def bg_animation(self, start_color = 0, mid_color = 0, end_color = 0, speed = 0):
    #     if start_color != self.start_color:
    #         if self.grad_boxes.mid_color[3] < 255 and self.loopfinished1 == False:
    #             self.grad_boxes.mid_color= (150, 0, 0, min(255,self.grad_boxes.mid_color[3] + speed))
    #         if self.grad_boxes.mid_color[3] == 255:
    #             self.loopfinished1 = True
    #         if self.grad_boxes.mid_color[3] <= 50:
    #             self.loopfinished1 = False
    #         if self.grad_boxes.mid_color[3] > 50 and self.loopfinished1 == True:
    #             self.grad_boxes.mid_color= (150, 0, 0, max(0,self.grad_boxes.mid_color[3] - speed))

    #     self.grad_boxes._interpolate(self.start_color, self.grad_boxes.start_color, i, mid_range)
    #     self.grad_boxes.create_gradient()

    def draw(self, screen, pos, var1 = any, var2 = any):
        self.grad_boxes.draw(screen)
        [i.draw(screen, pos, True, .2) for i in self.buttons]

menu = Menu_screen()