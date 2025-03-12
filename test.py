import pgzrun
from pygame import Rect

WIDTH = 800
HEIGHT = 600
screen: any

# Variáveis para armazenar a posição do mouse
mouse_x = 0
mouse_y = 0
mouse_pos = (0,0)

def on_mouse_move(pos):
    global mouse_x, mouse_y, mouse_pos
    mouse_pos = pos
    mouse_x, mouse_y = pos

texto = "Olá, Mundo!"
fonte = "boogaloo-regular"
tamanho_fonte = 30

import screens.menu

def draw():
    screen.clear()
    screen.draw.text(f"Mouse X: {mouse_x}, Mouse Y: {mouse_y}", midbottom = (mouse_x, mouse_y), fontsize=30, color="white")
    caixa = Rect(WIDTH/2, HEIGHT/2,WIDTH/2, HEIGHT/2, )

    # screen_.draw.text(texto, (100, 10),fontsize= tamanho_fonte, fontname=fonte)
    screen.draw.textbox("hello world", caixa, color="#000000", background="#FFFFFF" ,alpha=0.8)

    [i.draw(screen, mouse_pos) for i in screens.menu.menu.buttons]

    # print("Largura do texto:", pygame.font.SysFont(fonte, tamanho_fonte).size(texto))

pgzrun.go()