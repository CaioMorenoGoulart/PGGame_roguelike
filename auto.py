from pygame import Surface, SRCALPHA

# Caixa com transparencia
def draw_alpha_box(width, height, alpha_color, screen , pos):
    box = Surface((width, height), SRCALPHA)
    box.fill(alpha_color)
    screen.surface.blit(box, pos)

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