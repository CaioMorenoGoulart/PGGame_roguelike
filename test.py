import pgzrun
from pygame import SRCALPHA,Surface, Rect, mouse as mice
from config import WIDTH, HEIGHT

screen: any

# Variáveis para armazenar a posição do mouse
class mouses:
    def __init__(self):
        self.pos = (0,0)
        self.x = 0
        self.y = 0
        self.width = 50
        self.height = 50
    def update(self, pos):
        self.pos = pos
        self.x, self.y = pos


mouse = mouses()

def on_mouse_move(pos):
    mouse.update(pos)

texto = "Olá, Mundo!"
fonte = "boogaloo-regular"
tamanho_fonte = 26

mice.set_visible(False)

from map import Map
mapa = Map()
mapa.draw_map()

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


def draw():
    screen.clear()
    mapa.draw()

    # Definindo Texto
    texto = f"{mapa.pos_in_map(mouse)}"

    # Definindo tamanho da Caixa
    caixa = Rect(mouse.x - mouse.width/2, mouse.y - mouse.height/2, mouse.width, mouse.height)
    caixa.bottomleft
    # Desenhando Caixa
    draw_alpha_box(mouse.width, mouse.height, (255, 255, 255, 200), screen ,caixa.topleft)

    # Desenhando Contorno
    # screen.draw.rect(caixa, "#000000")

    draw_alpha_rect
    (caixa, 10, (0, 0, 0, 200), screen)

    # Desenhando Texto
    texto = f"{mapa.pos_in_map(mouse)}"
    screen.draw.text(texto[0], center=caixa.center, color="#000000", fontname=fonte, fontsize=tamanho_fonte, alpha=0.8)


pgzrun.go()