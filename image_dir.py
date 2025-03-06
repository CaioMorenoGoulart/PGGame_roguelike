class Dir():
    # Player
    class Player():
        DIR = "player/"

    # Personagens
    class Characteres():
        BOY = "boy/"
        GIRL_1 = "girl_1/"
        GIRL_2 = "girl_2/"
        ENEMY = "enemy/"

    # Ações
    class Actions():
        ATTACK = "attack/"
        WAITING = "waiting/"
        WALKING = "walking/"

    # Direções do player
    class Directions():
        UP = "up/"
        DOWN = "down/"
        SIDE = "side/"

    # Texturas
    class Textures():
        DIR = "textures/"
    class Weapons():
        DIR = "weapons/"

IMAGES = []
NUMB = []

def string_list(n_frames):
    global NUMB
    if NUMB != n_frames:
        NUMB = [str(num) for num in range(1, n_frames + 1)]
    return NUMB

def loading_images(string, n_frames):
    global IMAGES
    if IMAGES != [string + image for image in string_list(n_frames)]:
        IMAGES = [string + image for image in string_list(n_frames)]
    return [string + image for image in string_list(n_frames)]

class Directions():
    def __init__(self, dir_player, dir_characters ,dir_action, dir_direction, n_frames):
        self.dir_player = dir_player
        self.character = dir_characters
        self.dir_action = dir_action
        self.dir_direction = dir_direction
        self.dir = self.dir_player + self.character + self.dir_action + self.dir_direction
        self.N_FRAMES = n_frames
        self.frame_time = 1 / self.N_FRAMES
        self.images = loading_images(self.dir, self.N_FRAMES)

class Dir_images:
    class Textures:
        dir = Dir.Textures.DIR
        N_FRAMES = 1
    class Weapons:
        dir = Dir.Weapons.DIR
        N_FRAMES = 1
    class Characters:
        dir = ""
        N_FRAMES = 0
        frame_time = 0
        class Player:
            dir = Dir.Player.DIR
            N_FRAMES = 0
            frame_time = 0
            class Enemy:
                dir = Dir.Player.DIR + Dir.Characteres.ENEMY
                N_FRAMES = 2
            class Girl1:
                dir = Dir.Player.DIR + Dir.Characteres.GIRL_1
                N_FRAMES = 0
                frame_time = 0
                class Attack:
                    dir = Dir.Player.DIR + Dir.Characteres.GIRL_1 + Dir.Actions.ATTACK
                    Up = Directions(Dir.Player.DIR, Dir.Characteres.GIRL_1, Dir.Actions.ATTACK, Dir.Directions.UP, 4)
                    Down = Directions(Dir.Player.DIR, Dir.Characteres.GIRL_1, Dir.Actions.ATTACK, Dir.Directions.DOWN, 4)
                    Side = Directions(Dir.Player.DIR, Dir.Characteres.GIRL_1, Dir.Actions.ATTACK, Dir.Directions.SIDE, 5)
                    N_FRAMES = 0
                    frame_time = 0
                class Waiting:
                    dir = Dir.Player.DIR + Dir.Characteres.GIRL_1 + Dir.Actions.WAITING
                    Up = Directions(Dir.Player.DIR, Dir.Characteres.GIRL_1, Dir.Actions.WAITING, Dir.Directions.UP, 4)
                    Down = Directions(Dir.Player.DIR, Dir.Characteres.GIRL_1, Dir.Actions.WAITING, Dir.Directions.DOWN, 2)
                    Side = Directions(Dir.Player.DIR, Dir.Characteres.GIRL_1, Dir.Actions.WAITING, Dir.Directions.SIDE, 4)
                    N_FRAMES = 0
                    frame_time = 0
                class Walking:
                    dir = Dir.Player.DIR + Dir.Characteres.GIRL_1 + Dir.Actions.WALKING
                    Up = Directions(Dir.Player.DIR, Dir.Characteres.GIRL_1, Dir.Actions.WALKING, Dir.Directions.UP, 6)
                    Down = Directions(Dir.Player.DIR, Dir.Characteres.GIRL_1, Dir.Actions.WALKING, Dir.Directions.DOWN, 6)
                    Side = Directions(Dir.Player.DIR, Dir.Characteres.GIRL_1, Dir.Actions.WALKING, Dir.Directions.SIDE, 6)
                    N_FRAMES = 0
                    frame_time = 0
            class Girl2:
                dir = Dir.Player.DIR + Dir.Characteres.GIRL_2
                N_FRAMES = 0
                frame_time = 0
                class Attack:
                    dir = Dir.Player.DIR + Dir.Characteres.GIRL_2 + Dir.Actions.ATTACK
                    Up = Directions(Dir.Player.DIR, Dir.Characteres.GIRL_2, Dir.Actions.ATTACK, Dir.Directions.UP, 4)
                    Down = Directions(Dir.Player.DIR, Dir.Characteres.GIRL_2, Dir.Actions.ATTACK, Dir.Directions.DOWN, 4)
                    Side = Directions(Dir.Player.DIR, Dir.Characteres.GIRL_2, Dir.Actions.ATTACK, Dir.Directions.SIDE, 5)
                    N_FRAMES = 0
                    frame_time = 0
                class Waiting:
                    dir = Dir.Player.DIR + Dir.Characteres.GIRL_2 + Dir.Actions.WAITING
                    Up = Directions(Dir.Player.DIR, Dir.Characteres.GIRL_2, Dir.Actions.WAITING, Dir.Directions.UP, 2)
                    Down = Directions(Dir.Player.DIR, Dir.Characteres.GIRL_2, Dir.Actions.WAITING, Dir.Directions.DOWN, 2)
                    Side = Directions(Dir.Player.DIR, Dir.Characteres.GIRL_2, Dir.Actions.WAITING, Dir.Directions.SIDE, 2)
                    N_FRAMES = 0
                    frame_time = 0
                class Walking:
                    dir = Dir.Player.DIR + Dir.Characteres.GIRL_2 + Dir.Actions.WALKING
                    Up = Directions(Dir.Player.DIR, Dir.Characteres.GIRL_2, Dir.Actions.WALKING, Dir.Directions.UP, 6)
                    Down = Directions(Dir.Player.DIR, Dir.Characteres.GIRL_2, Dir.Actions.WALKING, Dir.Directions.DOWN, 6)
                    Side = Directions(Dir.Player.DIR, Dir.Characteres.GIRL_2, Dir.Actions.WALKING, Dir.Directions.SIDE, 6)
                    N_FRAMES = 0
            class Boy:
                dir = Dir.Player.DIR + Dir.Characteres.BOY
                N_FRAMES = 0
                frame_time = 0
                class Attack:
                    dir = Dir.Player.DIR + Dir.Characteres.BOY + Dir.Actions.ATTACK
                    Up = Directions(Dir.Player.DIR, Dir.Characteres.BOY, Dir.Actions.ATTACK, Dir.Directions.UP, 4)
                    Down = Directions(Dir.Player.DIR, Dir.Characteres.BOY, Dir.Actions.ATTACK, Dir.Directions.DOWN, 4)
                    Side = Directions(Dir.Player.DIR, Dir.Characteres.BOY, Dir.Actions.ATTACK, Dir.Directions.SIDE, 5)
                    N_FRAMES = 0
                class Waiting:
                    dir = Dir.Player.DIR + Dir.Characteres.BOY + Dir.Actions.WAITING
                    Up = Directions(Dir.Player.DIR, Dir.Characteres.BOY, Dir.Actions.WAITING, Dir.Directions.UP, 2)
                    Down = Directions(Dir.Player.DIR, Dir.Characteres.BOY, Dir.Actions.WAITING, Dir.Directions.DOWN, 2)
                    Side = Directions(Dir.Player.DIR, Dir.Characteres.BOY, Dir.Actions.WAITING, Dir.Directions.SIDE, 2)
                    N_FRAMES = 0
                class Walking:
                    dir = Dir.Player.DIR + Dir.Characteres.BOY + Dir.Actions.WALKING
                    Up = Directions(Dir.Player.DIR, Dir.Characteres.BOY, Dir.Actions.WALKING, Dir.Directions.UP, 6)
                    Down = Directions(Dir.Player.DIR, Dir.Characteres.BOY, Dir.Actions.WALKING, Dir.Directions.DOWN, 6)
                    Side = Directions(Dir.Player.DIR, Dir.Characteres.BOY, Dir.Actions.WALKING, Dir.Directions.SIDE, 6)
                    N_FRAMES = 0

# Classe Projétil
class Set_images:
    def __init__(self, img_obj = "", string = "", n_frames = 0):
        if img_obj != "":
            self.img_obj = img_obj
            self.dir = self.img_obj.dir + string
            self.frames = self.img_obj.N_FRAMES + n_frames
        else:
            self.dir = string
            self.frames = n_frames

        self.images = loading_images(self.dir, self.frames)
        self.frame_time = 1 / self.frames if self.frames > 0 else 1

class Player:
    def __init__(self ,main ,type  = "", action  = "", direction  = "", frames = 0, string = ""):
        self.dir = string
        self.main = main
        self.type = type
        self.action = action
        self.direction = direction
        self.images_dir = Dir
        if frames < 1:
            self.dir_string()
        else:
            self.frames = frames
        self.images = loading_images(self.dir, self.frames)

    def dir_string(self):
        if self.main == self.images_dir.Player.DIR:    
            if self.action == self.images_dir.Actions.WALKING:
                self.frames = 6
            elif self.action == self.images_dir.Actions.ATTACK:
                if self.direction == self.images_dir.Directions.SIDE:
                    self.frames = 5
                else:
                    self.frames = 4
            elif self.action == self.images_dir.Actions.WAITING:
                if self.direction == self.images_dir.Directions.DOWN or self.type != self.images_dir.Characteres.GIRL_1:
                    self.frames = 2
                else:
                    self.frames = 4
            self.dir = self.main + self.type + self.action + self.direction + self.dir
        elif self.main == self.images_dir.Textures.DIR:
            self.frames = 4
            self.dir = self.main + self.dir

        elif self.main == self.images_dir.Weapons.DIR:
            self.frames = 2
            self.dir = self.main + self.dir
        self.animation_time = 1 / self.frames