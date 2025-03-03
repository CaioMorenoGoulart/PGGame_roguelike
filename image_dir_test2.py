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

class Dir:
    class Textures:
        DIR = DIR_TEXTURES
    class Weapons:
        DIR = DIR_WEAPONS
    class Players:
        DIR = DIR_PLAYER
        class Characters:
            GIRL_1 = DIR_GIRL_1
            GIRL_2 = DIR_GIRL_2
            BOY = DIR_BOY
            ENEMY = DIR_ENEMY
            class Actions:
                ATTACK = DIR_ATTACK
                WAITING = DIR_WAITING
                WALKING = DIR_WALKING
                class Directions:
                    UP = DIR_UP
                    DOWN = DIR_DOWN
                    SIDE = DIR_SIDE

class Players(Dir):
    def __init__(self):
        self.DIR = DIR_PLAYER

class Characters(Players):
    def __init__(self):
        super().__init__()
        self.DIR 

class Actions(Characters):
    def __init__(self):
        super().__init__()
        self.variavel += 10  

class Directions(Actions):
    def __init__(self):
        super().__init__()
        self.variavel += 10  

# Criando um objeto da última geração (Neto)
obj = Neto()

# Mostrando o valor acumulado
print(obj.variavel)  # Saída: 50


print(Dir.Players.Characters.Actions.Directions.UP)