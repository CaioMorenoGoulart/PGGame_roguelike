# Player
DIR_PLAYER = "player/"

# Personagens
DIR_GIRL_1 = "girl_1/"
DIR_GIRL_2 = "girl_2/"
DIR_BOY = "boy/"
DIR_ENEMY = "enemy/"

# Ações
DIR_ATTACK = "attack/"
DIR_WAITING = "waiting/"
DIR_WALKING = "walking/"

# Direções do player
DIR_UP = "up/"
DIR_DOWN = "down/"
DIR_SIDE = "side/"

# Texturas
DIR_TEXTURES = "textures/"
DIR_WEAPONS = "weapons/"

test = {
    "Textures": DIR_TEXTURES,
    "Weapons": DIR_WEAPONS,
}

# class Directions:
#     UP = DIR_UP
#     DOWN = DIR_DOWN
#     SIDE = DIR_SIDE

# class Actions:
#     ATTACK = DIR_ATTACK
#     WAITING = DIR_WAITING
#     WALKING = DIR_WALKING
#     DIRECTIONS = Directions

class Actions:
    def __init__(self, action):
        self.action = action
        
    class Directions:
        UP = DIR_UP
        DOWN = DIR_DOWN
        SIDE = DIR_SIDE

# class Characters:
#     GIRL_1 = DIR_GIRL_1
#     GIRL_2 = DIR_GIRL_2
#     BOY = DIR_BOY
#     ENEMY = DIR_ENEMY
#     actions = Actions

# class Dir0:
#     PLAYER = DIR_PLAYER
#     TEXTURES = DIR_TEXTURES
#     WEAPONS = DIR_WEAPONS
#     characters = Characters

# DIR_CONCAT = ""
# class Dir1:
#     class Textures:
#         self_DIR = DIR_TEXTURES
#         DIR_CONCAT = self_DIR
#         DIR = DIR_CONCAT
#     class Weapons:
#         self_DIR = DIR_WEAPONS
#         DIR_CONCAT = self_DIR
#         DIR = DIR_CONCAT
#     class Characters:
#         class Enemy:
#             self_DIR = DIR_ENEMY
#             DIR_CONCAT = self_DIR
#             DIR = DIR_CONCAT
#         class Player:
#             self_DIR = DIR_PLAYER
#             DIR_CONCAT = self_DIR
#             DIR = DIR_CONCAT
#             class Girl1:
#                 self_DIR = DIR_GIRL_1
#                 DIR_CONCAT += self_DIR
#                 DIR = DIR_CONCAT
#                 class Attack:
#                     self_DIR = DIR_ATTACK
#                     UP = DIR_UP
#                     DOWN = DIR_DOWN
#                     SIDE = DIR_SIDE

#                 class Waiting:
#                     self_DIR = DIR_WAITING
#                     UP = DIR_UP
#                     DOWN = DIR_DOWN
#                     SIDE = DIR_SIDE

#                 class Walking:
#                     self_DIR = DIR_WALKING
#                     UP = DIR_UP
#                     DOWN = DIR_DOWN
#                     SIDE = DIR_SIDE
#             class Girl2:
#                 self_DIR = DIR_GIRL_2
#                 DIR_CONCAT += self_DIR
#                 DIR = DIR_CONCAT
#                 class Attack:
#                     self_DIR = DIR_ATTACK
#                     UP = DIR_UP
#                     DOWN = DIR_DOWN
#                     SIDE = DIR_SIDE

#                 class Waiting:
#                     self_DIR = DIR_WAITING
#                     UP = DIR_UP
#                     DOWN = DIR_DOWN
#                     SIDE = DIR_SIDE

#                 class Walking:
#                     self_DIR = DIR_WALKING
#                     UP = DIR_UP
#                     DOWN = DIR_DOWN
#                     SIDE = DIR_SIDE
#             class Boy:
#                 self_DIR = DIR_BOY
#                 DIR_CONCAT += self_DIR
#                 DIR = DIR_CONCAT
#                 class Attack:
#                     self_DIR = DIR_ATTACK
#                     UP = DIR_UP
#                     DOWN = DIR_DOWN
#                     SIDE = DIR_SIDE

#                 class Waiting:
#                     self_DIR = DIR_WAITING
#                     UP = DIR_UP
#                     DOWN = DIR_DOWN
#                     SIDE = DIR_SIDE

#                 class Walking:
#                     self_DIR = DIR_WALKING
#                     UP = DIR_UP
#                     DOWN = DIR_DOWN
#                     SIDE = DIR_SIDE

# print(Dir1.Characters.Player.Girl1.DIR)

# class Dir1:
#     class Textures:
#         DIR = DIR_TEXTURES
#     class Weapons:
#         DIR = DIR_WEAPONS
#     class Players:
#         DIR = DIR_PLAYER
#         class Characters:
#             GIRL_1 = DIR_GIRL_1
#             GIRL_2 = DIR_GIRL_2
#             BOY = DIR_BOY
#             ENEMY = DIR_ENEMY
#             class Actions:
#                 ATTACK = DIR_ATTACK
#                 WAITING = DIR_WAITING
#                 WALKING = DIR_WALKING
#                 class Directions:
#                     UP = DIR_UP
#                     DOWN = DIR_DOWN
#                     SIDE = DIR_SIDE