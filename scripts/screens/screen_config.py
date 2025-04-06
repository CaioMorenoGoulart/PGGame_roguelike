from scripts.style import *
from scripts.config import WIDTH, HEIGHT, STATE_MENU, RESOLUTION_OPTIONS, SCRENN_OPT, MUSIC_VOL, EFFECT_VOL

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
        import scripts.elements as elements
        import scripts.auto as auto
        self.dropdown = elements.Dropdown(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, RESOLUTION_OPTIONS, SCRENN_OPT, FONT_SIZE_MENU, FONT_COLOR_MENU, FONT_COLOR_HOVER)
        self.buttons = auto.listing(self.texts)
        self.config_slide = auto.slide_config(WIDTH, HEIGHT, MUSIC_VOL, EFFECT_VOL)

        self.grad_boxes = auto.GradientBox(
                start_color= (0, 0, 150, 0),
                end_color= (0, 0, 150, 0),
                mid_color= (150, 0, 0, 200),
                width=WIDTH,
                height=HEIGHT,
                vertical= True
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

    def draw(self, screen, pos, music, efect):
        self.grad_boxes.draw(screen)
        self.dropdown.draw(screen, pos)
        for i in self.buttons:
            if "Volume Música:" in i.text:
                i.text = "Volume Música: " f"{music:0.0f}%"
            if "Volume Efeitos:" in i.text:
                i.text = "Volume Efeitos: " f"{efect:0.0f}%"
            i.draw(screen, pos)
        [i.draw(screen) for i in self.config_slide]

menu = Menu_screen()