# Importações
import math
import random
import pgzero
from pygame import Rect, Surface, SRCALPHA
import pgzrun
from scripts.image_dir import Set_images, Dir_images, Player, Dir
from scripts.auto import *
from scripts.elements import Button, Float_texts

import json
from scripts.pgzhelper import Actor

Button
Float_texts
Surface
Rect
math
random
pgzero
pgzrun
Set_images
Dir_images
Player
Dir

# Restirando avisos
screen: any
animate: any
keyboard: any
sounds: any
keys: any
mouse: any


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
# Configurações iniciais

ARROW_SOUDS = ["arrow_1", "arrow_2", "arrow_3", "arrow_4"]
WOOSH_SOUDS = ["woosh_01", "woosh_02", "woosh_03", "woosh_04", "woosh_05"]
CONFIG = load_settings()
SCAL = 2
CELL_SIZE = Actor("textures/stone_tile_1", (0, 0), (0, 0)).height * SCAL
RESOLUTION_OPTIONS = ["800x600", "1024x768", "1280x720"]
SCRENN_OPT = CONFIG["screen_opt"]
RESOLUTION = RESOLUTION_OPTIONS[SCRENN_OPT].split("x")
MUSIC_VOL = CONFIG["music_volume"]
EFFECT_VOL = CONFIG["effects_volume"]
WIDTH = int(RESOLUTION[0])
HEIGHT = int(RESOLUTION[1])
COLUMNS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

# Estados de jogo
STATE_PLAYER_SELECT = "player_select"
STATE_PLAYING = "playing"
STATE_RESUME_GAME = "resume_play"
STATE_MENU = "menu"
STATE_CONTROLLS = "controlls"
STATE_PAUSED = "paused"
STATE_PAUSED_CONFIG = "config_paused"
STATE_SETTINGS = "config"
STATE_GAME_OVER = "game_over"
STATE_EXIT = "exit"


# Tipos de bonus
PW_MOVIMENT_SPEED = "speed"
PW_HEALTH = "health"
PW_CADENCE = "cadence"
POWER_UPS = ["speed", "health", "cadence"]

# Estados da entidade
ENTITY_NEW = "new"
ENTITY_HIT = "hit"
ENTITY_EXPLOSION = "explosion"

MOUSE_POS = (0, 0)