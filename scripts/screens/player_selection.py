from scripts.style import *
from scripts.config import WIDTH, HEIGHT, STATE_PLAYING, STATE_MENU, FPS, Actor
from scripts.image_dir import Dir_images, Set_images

class Images_animation:
    def __init__(self, x, y, frames, scale=1):
        self.frames = frames
        self.current_frame = 0
        self.tile = Actor(self.frames[self.current_frame], (x,y))
        self.scale = scale
        self.tile.scale = self.scale
        self.animation_timer = 0
        self.n_frames = len(self.frames)
    
    def update_frames(self):
        self.animation_timer += 1/FPS
        if self.animation_timer >= 1/ self.n_frames:
            self.current_frame = (self.current_frame - 1) % len(self.frames)
            self.tile.image = self.frames[self.current_frame]
            self.tile.scale = self.scale
            self.animation_timer = 0
        
        

class Menu_screen:
    def __init__(self):
        self.id = "Seleção de Personagens"
        self.texts = {
            "Texts": [
                {
                    "Text": "Iniciar jogo",
                    "Font_size": FONT_SIZE_MENU,
                    "Color": FONT_COLOR_MENU,
                    "Color_Hover": FONT_COLOR_HOVER,
                    "Border": FONT_BORDER_MENU,
                    "Border_Color": FONT_COLOR_BORDER_MENU,
                    "Border_Color_HOVER": FONT_COLOR_BORDER_HOVER,
                    "BG_Color": BG_TEXT_COLOR,
                    "Pos": (WIDTH // 2 - 100, HEIGHT // 2 + 20),
                    "Action": STATE_PLAYING,
                    "Block": True,
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
                    "Pos": (WIDTH // 2 - 100, HEIGHT // 2 + 90),
                    "Action": STATE_MENU,
                },
            ],
        }

        self.images = []
        import scripts.auto as auto

        self.characteres = [
            obj
            for name, obj in Dir_images.Characters.Player.__dict__.items()
            if isinstance(obj, type) and name != "Enemy"
        ]

        self.buttons = auto.characters_boxes(self.characteres, 200, bgc=BG_TEXT_COLOR, bc= FONT_COLOR_BORDER_MENU, b=10, y=100, space= 20, marg=200 ,width=0, bgch= (255,0,0,100), bch= (255,0,0,255))
        for i,buttons in enumerate(self.buttons):
            calc = Set_images(string= buttons.action.Waiting.Side.dir, n_frames= buttons.action.Waiting.Side.N_FRAMES).images
            actor_calc = Actor(calc[0])
            scale = min((buttons.box_width-5-(buttons.border * 2))/actor_calc.width, (buttons.box_height-5-(buttons.border * 2))/actor_calc.height)
            self.images.append(Images_animation(buttons.x + buttons.box_width/2, buttons.y + buttons.box_height/2, calc, scale)) 

        self.buttons.extend(auto.listing(self.texts))

        self.grad_boxes = auto.GradientBox(
                start_color= (150, 0, 0, 200),
                end_color= (0, 0, 0, 0),
                mid_color= (0, 0, 0, 0),
                width=WIDTH,
                height=HEIGHT,
                vertical=True
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

    def draw(self, screen, pos, var1 = any, var2 = any):
        self.grad_boxes.draw(screen)
        self.update(pos)
        for i in self.buttons:
            i.draw(screen, pos, True, .2)
        for i in self.images:
            i.tile.draw()

    def update(self, pos):
        for button in self.buttons:
            if button.selected or button.is_hovered(pos):
                if hasattr(button.action, "Waiting"):
                    for image in self.images:
                        if button.action.Waiting.Side.dir in image.tile.image:
                            image.update_frames()
menu = Menu_screen()