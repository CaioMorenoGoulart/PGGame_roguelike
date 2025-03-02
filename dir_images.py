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
    class Characters:
        class Enemy:
            DIR = DIR_ENEMY
        class Player:
            DIR = DIR_PLAYER
            class Girl1:
                DIR = DIR_PLAYER + DIR_GIRL_1
                class Attack:
                    DIR = DIR_PLAYER + DIR_GIRL_1 + DIR_ATTACK
                    UP = DIR + DIR_UP
                    DOWN = DIR + DIR_DOWN
                    SIDE = DIR + DIR_SIDE

                class Waiting:
                    DIR = DIR_PLAYER + DIR_GIRL_1 + DIR_WAITING
                    UP = DIR + DIR_UP
                    DOWN = DIR + DIR_DOWN
                    SIDE = DIR + DIR_SIDE

                class Walking:
                    DIR = DIR_PLAYER + DIR_GIRL_1 + DIR_WALKING
                    UP = DIR + DIR_UP
                    DOWN = DIR + DIR_DOWN
                    SIDE = DIR + DIR_SIDE
            class Girl2:
                DIR = DIR_PLAYER + DIR_GIRL_2
                class Attack:
                    DIR = DIR_PLAYER + DIR_GIRL_2 + DIR_ATTACK
                    UP = DIR + DIR_UP
                    DOWN = DIR + DIR_DOWN
                    SIDE = DIR + DIR_SIDE

                class Waiting:
                    DIR = DIR_PLAYER + DIR_GIRL_2 + DIR_WAITING
                    UP = DIR + DIR_UP
                    DOWN = DIR + DIR_DOWN
                    SIDE = DIR + DIR_SIDE

                class Walking:
                    DIR = DIR_PLAYER + DIR_GIRL_2 + DIR_WALKING
                    UP = DIR + DIR_UP
                    DOWN = DIR + DIR_DOWN
                    SIDE = DIR + DIR_SIDE
            class Boy:
                DIR = DIR_PLAYER + DIR_BOY

                class Attack:
                    DIR = DIR_PLAYER + DIR_BOY + DIR_ATTACK
                    UP = DIR + DIR_UP
                    DOWN = DIR + DIR_DOWN
                    SIDE = DIR + DIR_SIDE

                class Waiting:
                    DIR = DIR_PLAYER + DIR_BOY + DIR_WAITING
                    UP = DIR + DIR_UP
                    DOWN = DIR + DIR_DOWN
                    SIDE = DIR + DIR_SIDE

                class Walking:
                    DIR = DIR_PLAYER + DIR_BOY + DIR_WALKING
                    UP = DIR + DIR_UP
                    DOWN = DIR + DIR_DOWN
                    SIDE = DIR + DIR_SIDE

print(Dir.Characters.Player.Boy.Attack.SIDE)

# Classe Projétil
class Player:
    def __init__(self ,main ,type  = "", action  = "", direction  = "", frames = 0, string = ""):
        self.dir = string
        self.main = main
        self.type = type
        self.action = action
        self.direction = direction
        if frames < 1:
            self.dir_string()
            print(self.dir, self.frames)
        else:
            self.frames = frames
        self.images = self.loading_images()

    def dir_string(self):
        if self.main == DIR_PLAYER:    
            if self.action == DIR_WALKING:
                self.frames = 6
            elif self.action == DIR_ATTACK:
                if self.direction == DIR_SIDE:
                    self.frames = 5
                else:
                    self.frames = 4
            elif self.action == DIR_WAITING:
                if self.direction == DIR_DOWN or self.type != DIR_GIRL_1:
                    self.frames = 2
                else:
                    self.frames = 4
            self.dir = self.main + self.type + self.action + self.direction + self.dir
        elif self.main == DIR_TEXTURES:
            self.frames = 4
            self.dir = self.main + self.dir

        elif self.main == DIR_WEAPONS:
            self.frames = 2
            self.dir = self.main + self.dir
        self.animation_time = 1 / self.frames
    def string_list(self):
        global NUMB
        if NUMB != self.frames:
            NUMB = [str(num) for num in range(1, self.frames + 1)]
        return NUMB

    def loading_images(self):
        global IMAGES
        if IMAGES != [self.dir + image for image in self.string_list()]:
            IMAGES = [self.dir + image for image in self.string_list()]
        return [self.dir + image for image in self.string_list()]