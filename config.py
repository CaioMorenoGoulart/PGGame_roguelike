# Importações

import math
import random
import pgzero
from pygame import Rect
import pgzrun
from image_dir import Set_images, Dir_images, Player, Dir

import json
from pgzhelper import Actor

Rect
math
random
pgzero
pgzrun
Set_images
Dir_images
Player
Dir

# Funções para salvar e carregar configurações
def save_settings(config):
    with open("configuracoes.txt", "w") as file:
        json.dump(config, file)


def load_settings():
    try:
        with open("configuracoes.txt", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            "music_volume": 0.5,
            "effects_volume": 0.5,
            "screen_opt": 0,
        }

# Variáveis Globais

# Cores
TEXT_COLOR = (255, 255, 255)
HOVER_COLOR = (100, 100, 255)
HEALTH_COLOR = (0, 255, 0)

# Configurações iniciais

ARROW_SOUDS = ["arrow_1", "arrow_2", "arrow_3", "arrow_4"]
CONFIG = load_settings()
SCAL = 2
CELL_SIZE = Actor("textures/stone_tile_1", (0, 0), (0, 0)).height * SCAL
RESOLUTION_OPTIONS = ["800x600", "1024x768", "1280x720"]
SCRENN_OPT = CONFIG["screen_opt"]
RESOLUTION = RESOLUTION_OPTIONS[SCRENN_OPT].split("x")
WIDTH = int(RESOLUTION[0])
HEIGHT = int(RESOLUTION[1])
COLUMNS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

# Estados de jogo
STATE_PLAYING = "playing"
STATE_MENU = "menu"
STATE_PAUSED = "paused"
STATE_PAUSED_CONFIG = "config_paused"
STATE_SETTINGS = "config"
STATE_GAME_OVER = "game_over"

# Estados da entidade
ENTITY_NEW = "new"
ENTITY_HIT = "hit"
ENTITY_EXPLOSION = "explosion"

MOUSE_POS = (0, 0)