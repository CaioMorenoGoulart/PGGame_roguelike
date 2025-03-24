import pgzrun
import math
from pygame import SRCALPHA,Surface, Rect, mouse as mice
from pygame.draw import lines, rect
from config import WIDTH, HEIGHT
from auto import box

screen: any

# Variáveis para armazenar a posição do mouse
class mouses:
    def __init__(self):
        self.pos = (0,0)
        self.center = (0,0)
        self.x = 0
        self.y = 0
        self.width = 50
        self.height = 50
    def update(self, pos):
        self.pos = pos
        self.x, self.y = pos
        self.center = (self.x - self.width/2, self.y - self.height/2)


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



# def dist(ponto1, ponto2):
#     x1, y1 = ponto1
#     x2, y2 = ponto2
#     return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# def bezier_curve(p0, p1, p2, alpha=(0, 0, 0, 0), steps=0, w = 1):
#     if steps == 0:
#         steps = int(dist(p0, p1) + dist(p1, p2))
#         print(steps)
#     points = [box]
#     for t in range(steps):
#         t /= steps
#         x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
#         y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
#         points.append(box(w, w, alpha, pos=(x, y)))
    
#     for i in points:
#         i.draw(screen)

caixa_2 = box(mouse.width, mouse.height, (255, 255, 255, 200), (0, 0, 0, 150), 10)
texto = f"{mapa.pos_in_map(mouse)}"

def draw():
    screen.clear()
    mapa.draw()

    # Desenhando Caixa
    caixa_2.draw(screen, mouse.center)

    # Desenhando Texto
    texto = f"{mapa.pos_in_map(mouse)}"
    screen.draw.text(texto[0], center=caixa_2.rect.center, color="#000000", fontname=fonte, fontsize=tamanho_fonte, alpha=0.8)


    # Definir pontos de controle

    # p0 = (100, 400)  
    # p1 = (200, 100)  
    # p2 = (300, 400)  

    # draw_alpha_box(1,1,(255,0,0),screen, caixa.midtop)
    # draw_alpha_box(1,1,(255,0,0),screen, caixa.midright)
    # draw_alpha_box(1,1,(255,0,0),screen, caixa.midleft)
    # draw_alpha_box(1,1,(255,0,0),screen, caixa.midbottom)

    # bezier_curve(caixa.midleft,caixa.midtop,caixa.midright, alpha=(0, 0, 0), w= 1)
    # bezier_curve(caixa.midleft,caixa.midbottom,caixa.midright, alpha=(0, 0, 0), w= 1)
    # bezier_curve(p0,p1,p2, alpha=(0, 0, 0, 255), w= 1)

    # text_test = screen.draw.text("All together now:\nCombining the above options", center=(WIDTH/2,CELL_SIZE), fontsize=30, color="#AAFF00", gcolor="#66AA00", owidth=1.5, ocolor="black", alpha=0.8)

pgzrun.go()