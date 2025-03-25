from pygame import Surface, SRCALPHA, Rect

# Caixa com transparencia

class box:
    def __init__(self, width, height, fill_color, border_color = "", border  = 0, border_top = 0, border_rigth  = 0, border_botton  = 0, border_left  = 0, pos =(0, 0)):
        self.rect = Rect( pos[0], pos[1], width, height)
        self.fill_color = fill_color
        self.border_color = border_color
        self.border = border
        self.border_top = border_top
        self.border_rigth = border_rigth
        self.border_botton = border_botton
        self.border_left = border_left

    def draw_alpha_box(self, width, height, pos, screen, color):
        box = Surface((width, height), SRCALPHA)
        box.fill(color)
        screen.surface.blit(box, pos)

    def draw_alpha_rect(self, screen):
        box = [
            Rect(self.rect.topleft[0], self.rect.topleft[1], self.border, self.rect.height - self.border),
            Rect(self.rect.topleft[0] + self.border, self.rect.topleft[1], self.rect.width - self.border*2, self.border),
            Rect(self.rect.topright[0] - self.border, self.rect.topright[1], self.border, self.rect.height),
            Rect(self.rect.bottomleft[0], self.rect.bottomleft[1] - self.border, self.rect.width - self.border, self.border)]
        for i in box:
            self.draw_alpha_box(i.width, i.height, i.topleft, screen, self.border_color)

    def draw(self, screen, pos = (0,0)):
        self.rect = Rect( pos[0], pos[1], self.rect.width, self.rect.height)
        self.draw_alpha_box(self.rect.width, self.rect.height, self.rect.topleft, screen,  self.fill_color)
        if self.border > 0:
            self.draw_alpha_rect(screen)

def listing(texts):
    from scripts.elements import Button
    list = []
    for text in texts["Texts"]:  
        list.append(Button(
            text["Pos"][0],
            text["Pos"][1],
            text["Text"],
            text["Action"],
            text["Color"],
            text["Color_Hover"],
            text["Font_size"],
            text["BG_Color"],
        ))
    return list

def slide_config(WIDTH, HEIGHT, MUSIC_VOL, EFFECT_VOL):
    from scripts.elements import Slider
    return [Slider(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, MUSIC_VOL),
            Slider(WIDTH // 2 - 100, HEIGHT // 2 + 170, 200, EFFECT_VOL)]

# Formatar Tempo
def time_format(seconds):
    hours = seconds // 3600
    minuts = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    return f"{hours:02.0f}:{minuts:02.0f}:{remaining_seconds:02.0f}"

class Time_texts:
    def __init__(self, text, pos):
        self.text = text
        self.time = 0
        self.pos = pos
        
    def update(self, dt):
        self.time+= dt

# Ajustar hitbox

def right_hitbox(actor):
    actor.hitbox = Rect(
        (actor.tile.x + 1) - actor.tile.width / 2,
        (actor.tile.y + 1) - actor.tile.height / 2,
        actor.tile.width - 2,
        actor.tile.height - 2
    )

# Classe Sons do jogo:
class Songs_obj:
    def __init__(self, song, sounds, vol):
        self.song = song
        self.song_playing = False
        self.obj = getattr(sounds, self.song)
        self.obj.set_volume(vol)

    def play(self):
        self.obj.play()

    def stop(self):
        self.song_playing = False
        self.obj.stop()
    
    def pause(self):
        self.song_playing = False
        self.obj.pause()

    def update(self):
        if self.song_playing == False:
            self.play
        else:
            self.stop
