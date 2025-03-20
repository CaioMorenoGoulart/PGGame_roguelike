from pygame import Surface, SRCALPHA, Rect

# Caixa com transparencia
def draw_alpha_box(width, height, alpha_color, screen , pos):
    box = Surface((width, height), SRCALPHA)
    box.fill(alpha_color)
    screen.surface.blit(box, pos)

def draw_alpha_rect(rect, w, alpha, screen):
    box = [
        Rect(rect.topleft[0], rect.topleft[1], w, rect.height - w),
        Rect(rect.topleft[0] + w, rect.topleft[1], rect.width - w*2, w),
        Rect(rect.topright[0] - w, rect.topright[1], w, rect.height),
        Rect(rect.bottomleft[0], rect.bottomleft[1] - w, rect.width - w, w)]
    
    for i in box:
        draw_alpha_box(i.width, i.height, alpha, screen, i.topleft)

def listing(texts):
    from elements import Button
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
    from elements import Slider
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
