import math
import random
from pygame import Rect
import pgzrun
from pgzhelper import *
# import json
# Cores
TEXT_COLOR = (255, 255, 255)
HOVER_COLOR = (100, 100, 255)
HEALTH_COLOR = (0, 255, 0) 
    
# Carregar Diretorios
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
DIR_SIDE = "side/"
DIR_DOWN = "down/"

    # Texturas
DIR_TEXTURES = "textures/"
DIR_WEAPONS = "weapons/"

    # Leitor Sprites
numb = 0
def string_list(number):
    global numb
    if numb != number:
        numb = [str(num) for num in range(1, number + 1)]
    return numb

IMAGES = [""]
def loading_images(dir_string, frames):
    global IMAGES
    if IMAGES != [dir_string + image for image in string_list(frames)]:
        IMAGES = [dir_string + image for image in string_list(frames)]
    return [dir_string + image for image in string_list(frames)]

# def set_actors_tiles(IMAGES):
#     return [Actor(image for image in IMAGES)]
    
# Funções para salvar e carregar configurações
# def save_settings(config):
#     with open("configuracoes.txt", "w") as file:
#         json.dump(config, file)

# def load_settings():
#     try:
#         with open("configuracoes.txt", "r") as file:
#             return json.load(file)
#     except FileNotFoundError:
#         return {
#             "music_volume": 0.5,
#             "effects_volume": 0.5,
#             "screen_opt": 0,
#         }

# Configurações iniciais
# config = load_settings()
config = {
            "music_volume": 0.5,
            "effects_volume": 0.5,
            "screen_opt": 0,
         }
# SCAL = 2
# CELL_SIZE = Actor(loading_images(DIR_TEXTURES + "stone_tile_", 1)[0], (0, 0),(0, 0)).height * SCAL
CELL_SIZE = Actor(loading_images(DIR_TEXTURES + "stone_tile_", 1)[0], (0, 0),(0, 0)).height
resolution_options = ["800x600", "1024x768", "1280x720"]
SCRENN_OPT = config["screen_opt"]
resolution = resolution_options[SCRENN_OPT].split("x")
WIDTH = int(resolution[0])
HEIGHT = int(resolution[1])
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

#Variavel Global
MOUSE_POS = (0, 0)

# Criação do Mapa
class Map:
    def __init__(self):
        self.MAP = []
        for row in range(ROWS):
            if row == 0 or row == ROWS-1:
                self.MAP.append([1] * COLUMNS)
            else:
                self.MAP.append([1] + [0] * (COLUMNS-2) + [1])
    
    # Randomizar grama
    def get_random_grass(self):
        GRASS_TILE = Actor(random.choice(loading_images(DIR_TEXTURES + "grass_tile_", 4)), (0, 0),(0, 0))
        # GRASS_TILE.scale = SCAL
        return GRASS_TILE
    # Desenhar Mapa
    def draw_map(self):
        self.map_tiles = []
        for y, row in enumerate(self.MAP):
            for x, tile in enumerate(row):
                if tile == 0:
                    GRASS_TILE = self.get_random_grass()
                    GRASS_TILE.x = x * GRASS_TILE.height
                    GRASS_TILE.y = y * GRASS_TILE.width
                    self.map_tiles.append(GRASS_TILE)
                elif tile == 1:
                    STONE_TILE = Actor(loading_images(DIR_TEXTURES + "stone_tile_", 1)[0], (0, 0),(0, 0))
                    # STONE_TILE.scale = SCAL
                    STONE_TILE.x = x * STONE_TILE.height
                    STONE_TILE.y = y * STONE_TILE.width
                    self.map_tiles.append(STONE_TILE)

    def draw(self):
        for tile in self.map_tiles:
            tile.draw()

# Formatar Tempo
def time_format(seconds):
    hours = seconds // 3600  
    minuts = (seconds % 3600) // 60  
    remaining_seconds = seconds % 60
    return f"{hours:02.0f}:{minuts:02.0f}:{remaining_seconds:02.0f}"

#  Arrumar hitbox
def right_hitbox(actor):
    actor.hitbox = Rect(
    (actor.tile.x + 1) - actor.tile.width / 2,
    (actor.tile.y + 1) - actor.tile.height / 2,
    actor.tile.width - 2,
    actor.tile.height -2
)
def draw_text_with_border(text, position, fontsize=30, color="white", border_color="black", border_width=2):
    x, y = position
    for dx in (-border_width, 0, border_width):
        for dy in (-border_width, 0, border_width):
            if dx != 0 or dy != 0: 
                screen.draw.text(text, (x + dx, y + dy), fontsize=fontsize, color=border_color)
    screen.draw.text(text, (x, y), fontsize=fontsize, color=color)
# Classe Entidade
class Entity:
    def __init__(self, x, y, frames, scale = 1):
        self.frames = frames
        self.current_frame = 0
        self.tile = Actor(self.frames[self.current_frame])
        self.tile_scale = scale
        self.tile.scale = self.tile_scale
        self.hit_cooldown = 0
        self.tile.pos = (x, y)
        self.state = ENTITY_NEW
        self.update_frames()
    def draw(self):
        self.tile.draw()

    def update_frames(self, charging = False,):
        if charging:
            if self.current_frame < len(self.frames) - 1:
                self.current_frame += 1
                # self.tile.image = self.frames[self.current_frame]
                self.tile.next_image()
            else:
                self.tile.image = self.frames[len(self.frames) - 1]
        else:
            if not self.tile.flip_x:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
            elif self.tile.flip_x:
                self.current_frame = (self.current_frame - 1) % len(self.frames)
            self.tile.image = self.frames[self.current_frame]
        right_hitbox(self)

    def move(self, x, y):
        if  self.hit_cooldown == 0:
            new_x = self.tile.x + x * CELL_SIZE
            new_y = self.tile.y + y * CELL_SIZE
            # Inimigo olhando para o player
            if self.tile != game.player.tile:
                if new_x > game.player.tile.x:
                    self.tile.flip_x = True
                else:
                    self.tile.flip_x = False

            if CELL_SIZE < (new_x - self.tile.height/2) < (COLUMNS*CELL_SIZE - (CELL_SIZE + self.tile.height)) and CELL_SIZE <= (new_y - (self.tile.width/2)) < (ROWS*CELL_SIZE - (CELL_SIZE + self.tile.width)):
                if self.tile != game.player.tile:
                    animate(self.tile, pos=(new_x, new_y), duration=0.05)
                else:
                    animate(self.tile, pos=(new_x, new_y), duration=0.01)

# Classe Projetil
class Projectile:
    def __init__(self, x, y, direction_x, direction_y, tile):
        self.tile = Actor(tile, (x, y))
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.angles = math.degrees(math.atan2(-direction_y, direction_x))  # Converte para graus
        self.shoot_remove_cooldown = 0
        self.shoot_spawn_cooldown = 0
        self.initial_speed = 10
        self.speed = min(max(game.charging_time * self.initial_speed, 4), 20)
        right_hitbox(self)
        
    def update(self, dt):
        self.shoot_spawn_cooldown += dt
        self.tile.pos=(self.tile.x + self.direction_x * self.speed, self.tile.y + self.direction_y * self.speed)
        self.tile.angle = self.angles-90
        
        if self.speed > 0:
            if self.offscreen():
                self.hit(dt)
        else:
            if  self.speed == 0:
                self.shoot_remove_cooldown += dt
        if  self.shoot_remove_cooldown >= game.shoot_cadence:
            game.projectiles.remove(self)

    def draw(self):
        self.tile.draw()

    def hit(self, dt):
        self.speed = 0
        self.tile.image = loading_images(DIR_WEAPONS + "arrow_", 2)[1]
        self.shoot_remove_cooldown += dt
    def offscreen(self):  
        return self.tile.x < CELL_SIZE or self.tile.x > COLUMNS*CELL_SIZE - CELL_SIZE or self.tile.y < CELL_SIZE or self.tile.y > ROWS*CELL_SIZE - CELL_SIZE


# Criação Botão
class Button:
    def __init__(self, x, y, text, action):
        self.x = x
        self.y = y
        self.text = text
        self.action = action
        self.screen_width = 200
        self.screen_height = 50

    def draw(self, MOUSE_POS):
        color = HOVER_COLOR if self.is_hovered(MOUSE_POS) else TEXT_COLOR
        screen.draw.filled_rect(
            Rect(self.x, self.y, self.screen_width, self.screen_height),
            (50, 50, 50),
        )
        screen.draw.text(
            self.text,
            center=(self.x + self.screen_width // 2, self.y + self.screen_height // 2),
            fontsize=30,
            color=color,
        )

    def is_hovered(self, MOUSE_POS):
        return (
            self.x <= MOUSE_POS[0] <= self.x + self.screen_width
            and self.y <= MOUSE_POS[1] <= self.y + self.screen_height
        )
    
# Classe Slider
class Slider:
    def __init__(self, x, y, screen_width, initial_value=0.5):
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.screen_height = 10
        self.value = initial_value
        self.dragging = False
        self.indicator_radius = 10

    def draw(self, screen):
        screen.draw.filled_rect(
            Rect(self.x, self.y, self.screen_width, self.screen_height),
            (100, 100, 100),
        )
        indicator_position = self.x + int(self.value * self.screen_width)
        screen.draw.filled_circle(
            (indicator_position, self.y + self.screen_height // 2),
            self.indicator_radius,
            (200, 200, 200),
        )

    def is_hovered_indicator(self, pos):
        indicator_position = self.x + int(self.value * self.screen_width)
        distance_x = abs(pos[0] - indicator_position)
        distance_y = abs(pos[1] - (self.y + self.screen_height // 2))
        return distance_x <= self.indicator_radius and distance_y <= self.indicator_radius

    def update_value(self, pos):
        if self.x <= pos[0] <= self.x + self.screen_width:
            self.value = (pos[0] - self.x) / self.screen_width
            self.value = max(0.0, min(1.0, self.value))

# Classe Dropdown
class Dropdown:
    def __init__(self, x, y, screen_width, options, selected_option):
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.screen_height = 40
        self.options = options
        self.selected_option = selected_option
        self.open = False

    def draw(self, screen):
        screen.draw.filled_rect(
            Rect(self.x, self.y, self.screen_width, self.screen_height),
            (50, 50, 50),
        )
        screen.draw.text(
            self.options[self.selected_option],
            center=(self.x + self.screen_width // 2, self.y + self.screen_height // 2),
            fontsize=30,
            color = HOVER_COLOR if self.is_hovered(MOUSE_POS) else TEXT_COLOR,
        )

        if self.open:
            for i, option in enumerate(self.options):
                screen.draw.filled_rect(
                    Rect(self.x, self.y + (i + 1) * self.screen_height, self.screen_width, self.screen_height),
                    (70, 70, 70),
                )
                screen.draw.text(
                    option,
                    center=(self.x + self.screen_width // 2, self.y + (i + 1.5) * self.screen_height),
                    fontsize=30,
                    color=TEXT_COLOR,
                )

    def is_hovered(self, pos):
        if self.open:
            return (
                self.x <= pos[0] <= self.x + self.screen_width
                and self.y <= pos[1] <= self.y + (len(self.options) + 1) * self.screen_height
            )
        else:
            return (
                self.x <= pos[0] <= self.x + self.screen_width
                and self.y <= pos[1] <= self.y + self.screen_height
            )

    def select_option(self, pos):
        if self.open:
            for i in range(len(self.options)):
                if (
                    self.x <= pos[0] <= self.x + self.screen_width
                    and self.y + (i + 1) * self.screen_height <= pos[1] <= self.y + (i + 2) * self.screen_height
                ):
                    self.selected_option = i
                    self.open = False
                    return self.options[i]
        else:
            self.open = not self.open
        return None

# Classe Telas
class Screens:
    def menu(self):
        return [
            Button(WIDTH // 2 - 100, HEIGHT // 2 - 50, "Jogar", game.start_game),
            Button(WIDTH // 2 - 100, HEIGHT // 2 + 20, "Configurações", game.call_settings),
            Button(WIDTH // 2 - 100, HEIGHT // 2 + 90, "Sair", game.exit),
        ]

    def settings(self):
        if not game.paused:
            return [
                Button(WIDTH // 2 - 100, HEIGHT // 2 + 20, "Voltar", game.back_to_menu),
            ]
        else:
            return [
                Button(WIDTH // 2 - 100, HEIGHT // 2 + 20, "Voltar ao jogo", game.resume_game),
            ]

    def pause(self):
        return [
            Button(WIDTH // 2 - 100, HEIGHT // 2 - 50, "Continuar", game.resume_game),
            Button(WIDTH // 2 - 100, HEIGHT // 2 + 20, "Configurações", game.call_settings),
            Button(WIDTH // 2 - 100, HEIGHT // 2 + 90, "Voltar para o menu", game.back_to_menu),
        ]

    def game_over(self):
        return [
            Button(WIDTH // 2 - 100, HEIGHT // 2 - 50, "Jogar novamente", game.start_game),
            Button(WIDTH // 2 - 100, HEIGHT // 2 + 20, "Configurações", game.call_settings),
            Button(WIDTH // 2 - 100, HEIGHT // 2 + 90, "Voltar para o Menu", game.back_to_menu),
        ]
    
# Criação do jogo
class Game:
    def __init__(self):
        self.settings = config
        self.mapa = Map()
        self.mapa.draw_map()
        self.screens = Screens()
        self.freeze_mode = False
        self.draw_hitbox = False
        self.status = STATE_MENU
        self.paused = False
        self.music_volume = self.settings["music_volume"]
        self.effects_volume = self.settings["effects_volume"]
        self.screen_opt = self.settings["screen_opt"]
        self.music_volume_slider = Slider(WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, self.music_volume)
        self.effects_volume_slider = Slider(WIDTH // 2 - 100, HEIGHT // 2 + 200, 200, self.effects_volume)
        self.resolution_dropdown = Dropdown(WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, resolution_options, self.screen_opt)
        self.difficulty_score = 10
        self.press = False
        self.charging = False
        self.charging_time = 0
        self.animation_speed = 0.05  # Tempo entre cada frame (em segundos)
        self.player = Entity(WIDTH // 2, HEIGHT // 2, loading_images(DIR_PLAYER + DIR_GIRL_1 + DIR_WAITING + DIR_DOWN, 2))
        self.enemy_animation_timer = 0  # Temporizador para a animação
        self.player_selected = ""
        self.player_animation_timer = 0
        self.player_animation_timer = 0  # Temporizador para a animação
        self.animation = False
        self.animation_string = ""
        self.score = 0
        self.projectiles = [Projectile]
        self.enemies = [Entity]
        self.player_health = 100
        self.last_enemy_move_time = 0
        self.enemy_move_interval = 0.03
        self.last_enemy_spawn_time = 0
        self.enemy_spawn_interval = 2
        self.enemy_remove_interval = 2
        self.enemy_speed = .1
        self.elapsed_time = 0
        self.total_time = 0  # Tempo total decorrido no jogo
        self.last_damage_time = 0  # Tempo desde o último dano
        self.damage_cooldown = .001  # Cooldown entre danos
        self.shoot_cadence = 1
        self.shoot_cooldown = 1

    def draw_menu(self):
        for button in self.screens.menu():
            button.draw(MOUSE_POS)

    def call_settings(self):
        if self.status == STATE_MENU or self.status == STATE_GAME_OVER:
            self.status = STATE_SETTINGS
        elif self.status == STATE_PAUSED:
            self.status = STATE_PAUSED_CONFIG

    def draw_settings(self):
        for button in self.screens.settings():
            button.draw(MOUSE_POS)

        self.music_volume_slider.draw(screen)
        self.effects_volume_slider.draw(screen)
        self.resolution_dropdown.draw(screen)

        screen.draw.text(
            f"Volume Música: {int(self.music_volume * 100)}%",
            topleft=(WIDTH // 2 - 100, HEIGHT // 2 + 170),
            fontsize=30,
            color=TEXT_COLOR,
        )
        screen.draw.text(
            f"Volume Efeitos: {int(self.effects_volume * 100)}%",
            topleft=(WIDTH // 2 - 100, HEIGHT // 2 + 220),
            fontsize=30,
            color=TEXT_COLOR,
        )

    def draw_pause(self):
        for button in self.screens.pause():
            button.draw(MOUSE_POS)

    def resume_game(self):
        self.status = STATE_PLAYING
        pgzero.music.unpause()
        self.paused = False

    def back_to_menu(self):
        game.save_updated_settings()
        self.status = STATE_MENU
        self.paused = False

    def change_resolution(self, resolution):
        global SCRENN_OPT
        SCRENN_OPT = resolution_options.index(resolution)

    def save_updated_settings(self):
        self.settings = {
            "music_volume": self.music_volume,
            "effects_volume": self.effects_volume,
            "screen_opt": SCRENN_OPT,
        }
        # save_settings(self.settings)

    def start_game(self):
        self.status = STATE_PLAYING
        self.player_selected = DIR_PLAYER + DIR_GIRL_1
        self.player_health = 100
        self.score = 0
        self.enemies = []
        self.projectiles = []
        self.player.tile.pos = (WIDTH/2 - self.player.tile.width, HEIGHT/2 - self.player.tile.height)
        self.enemy_speed = .1
        self.time_elapsed = 0
        pgzero.music.set_volume(self.music_volume)
        pgzero.music.play('music.wav')

    def play_projectile_sound(self):
        sounds.shot.set_volume(self.effects_volume)
        sounds.shot.play()

    def shoot_projectile(self, mouse_pos):
        direction_x = mouse_pos[0] - self.player.tile.x
        direction_y = mouse_pos[1] - self.player.tile.y
        magnitude = math.sqrt(direction_x ** 2 + direction_y ** 2)
        self.play_projectile_sound()
        if magnitude == 0:
            return
        direction_x /= magnitude
        direction_y /= magnitude

        self.projectiles.append(
            Projectile(
                self.player.tile.x,
                self.player.tile.y,
                direction_x,
                direction_y,
                loading_images(DIR_WEAPONS + "arrow_", 2)[0]
            )
        )

    def move_enemies(self):
        for enemy in self.enemies:
            if enemy.hit_cooldown == 0:
                dx = self.player.tile.x - enemy.tile.x
                dy = self.player.tile.y - enemy.tile.y
                magnitude = math.sqrt(dx ** 2 + dy ** 2)
                if magnitude == 0:
                    continue
                dx /= magnitude
                dy /= magnitude

                dx += random.uniform(-1.5, 1.5)
                dy += random.uniform(-1.5, 1.5)

                magnitude = math.sqrt(dx ** 2 + dy ** 2)
                if magnitude == 0:
                    continue
                dx /= magnitude
                dy /= magnitude

                enemy.move(dx * self.enemy_speed, 2*dy * self.enemy_speed)

    def spawn_enemy(self):
        x = random.randint(2, COLUMNS - 2) * CELL_SIZE
        y = random.randint(2, ROWS - 2) * CELL_SIZE
        self.enemies.append(Entity(x,y, loading_images(DIR_PLAYER + DIR_ENEMY, 2)))
    def check_player_enemy_collision(self):
        for enemy in self.enemies:
            if enemy.tile.colliderect(self.player.tile):
                if self.total_time - self.last_damage_time >= self.damage_cooldown:
                    self.last_damage_time = self.total_time
                    if enemy.state == ENTITY_NEW:
                        self.player_health -= 0.2
                    elif enemy.state == ENTITY_HIT:
                        self.player_health -= 0
                    elif enemy.state == ENTITY_EXPLOSION:
                        self.player_health -= 2
                    if self.player_health <= 0:
                        self.status = STATE_GAME_OVER
                        pgzero.music.stop()
                    break

    def check_projectile_enemy_collision(self, dt):
        for enemy in self.enemies:
            if 0 < enemy.hit_cooldown < self.enemy_remove_interval:
                    enemy.hit_cooldown += dt
            if enemy.hit_cooldown >= (self.enemy_remove_interval - 1) and enemy.hit_cooldown < self.enemy_remove_interval:
                    enemy.state = ENTITY_EXPLOSION
                    enemy.frames = loading_images(DIR_PLAYER + DIR_ENEMY + "bomb/bomb_", 4)
                    enemy.tile.scale = 2
            if enemy.hit_cooldown > self.enemy_remove_interval:
                    self.score += 1
                    self.enemies.remove(enemy)
            for projectile in self.projectiles:
                if projectile.speed > 0 and enemy.hit_cooldown == 0:
                    if projectile.tile.colliderect(enemy.tile):
                        enemy.state = ENTITY_HIT
                        enemy.hit_cooldown += dt
                        projectile.hit(dt)
                        enemy.frames = loading_images(DIR_PLAYER + DIR_ENEMY + "enemi_dead_", 2)

    def increase_difficulty(self):
        self.enemy_speed += 0.01
        self.enemy_spawn_interval = max(0.5, self.enemy_spawn_interval - 0.1)
    
    def draw_game_over(self):
        screen.draw.text(
            "Game Over",
            center=((WIDTH // 2), (HEIGHT // 2) - 200),
            fontsize=50,
            color=TEXT_COLOR,
        )
        screen.draw.text(
            f"Pontuação: {self.score}",
            center=((WIDTH // 2), (HEIGHT // 2) -150),
            fontsize=30,
            color=TEXT_COLOR,
        )
        screen.draw.text(
            f"Tempo De jogo: {time_format(self.total_time)}",
            center=((WIDTH // 2), (HEIGHT // 2) -100),
            fontsize=30,
            color=TEXT_COLOR,
        )
        for button in self.screens.game_over():
            button.draw(MOUSE_POS)

    def draw_player(self):
        self.player.draw()

        for enemy in self.enemies:
            enemy.draw()

        for projectile in self.projectiles:
            projectile.draw()

    def draw_hud(self):
        draw_text_with_border(
        f"Pontuação: {self.score}",
        position=(10, 10),
        fontsize=30,
        color="white",
        border_color="black",
        border_width=1
        )
        draw_text_with_border(
        f"Tempo de jogo: {time_format(self.total_time)}",
        position=(WIDTH - 250, 10),
        fontsize=30,
        color="white",
        border_color="black",
        border_width=1
        )
        draw_text_with_border(
        f"Vida: {self.player_health:.0f}",
        position=(10, HEIGHT - 50),
        fontsize=30,
        color="white",
        border_color="black",
        border_width=1
        )
        screen.draw.filled_rect(
            Rect(9, HEIGHT - 31, 202, 22),
            (0,0,0),
        )
        screen.draw.filled_rect(
            Rect(10, HEIGHT - 30, self.player_health * 2, 20),
            HEALTH_COLOR,
        )

    def keybord_press(self):
        if self.charging:
            move_pixel = .05
        else:
            move_pixel = .1

        if (keyboard.LEFT or keyboard.A) and (keyboard.UP or keyboard.W):
            self.player.move(-move_pixel, -move_pixel)
            self.animation = True
        elif (keyboard.LEFT or keyboard.A) and (keyboard.DOWN or keyboard.S):
            self.player.move(-move_pixel, move_pixel)
            self.animation = True
        elif (keyboard.RIGHT or keyboard.D) and (keyboard.UP or keyboard.W):
            self.player.move(move_pixel, -move_pixel)
            self.animation = True
        elif (keyboard.RIGHT or keyboard.D) and (keyboard.DOWN or keyboard.S):
            self.player.move(move_pixel, move_pixel)
            self.animation = True
        elif (keyboard.LEFT or keyboard.A):
            self.player.move(-move_pixel, 0)
            self.animation = True
        elif (keyboard.RIGHT or keyboard.D):
            self.player.move(move_pixel, 0)
            self.animation = True
        elif (keyboard.UP or keyboard.W):
            self.player.move(0, -move_pixel)
            self.animation = True
        elif (keyboard.DOWN or keyboard.S):
            self.player.move(0, move_pixel)
            self.animation = True
        elif keyboard.ESCAPE:
            self.status = STATE_PAUSED
            pgzero.music.pause()
            self.paused = True

    def set_player_frames(self, frames, time):
        self.player.frames = frames
        if self.player_animation_timer >= self.animation_speed+time and self.animation:
            self.player_animation_timer = 0
            self.player.update_frames(self.charging)
            self.animation = False

    def draw_playing(self, dt):
        if self.status == STATE_PLAYING:
            self.total_time += dt  # Atualiza o tempo total decorrido
            self.elapsed_time += dt
            self.enemy_animation_timer += dt
            self.player_animation_timer += dt
            
            # Atualiza a animação dos inimigos
            if self.enemy_animation_timer >= self.animation_speed:
                self.enemy_animation_timer = 0  # Reseta o temporizador
                for enemy in self.enemies:
                    enemy.update_frames()
            if self.charging:
                self.charging_time = min(self.charging_time + dt, 2)
            if self.elapsed_time >= 1 and self.difficulty_score < self.score:
                self.difficulty_score +=10
                self.increase_difficulty()
                self.elapsed_time = 0
            
            for projectile in self.projectiles:
                projectile.update(dt)

            self.last_enemy_move_time += dt
            if self.last_enemy_move_time >= self.enemy_move_interval:
                self.move_enemies()
                self.last_enemy_move_time = 0

            self.last_enemy_spawn_time += dt
            if self.last_enemy_spawn_time >= self.enemy_spawn_interval:
                self.spawn_enemy()
                self.last_enemy_spawn_time = 0

            self.keybord_press()
            self.check_projectile_enemy_collision(dt)
            self.check_player_enemy_collision()

    def atack_pressed(self):
        if self.charging:
            self.charging = False
            self.animation = True
            self.shoot_projectile(MOUSE_POS)
        elif len(self.projectiles) > 0:
            if self.projectiles[len(self.projectiles)-1].shoot_spawn_cooldown > self.shoot_cooldown:
                self.charging = True
                self.animation = True
                self.set_player_frames(loading_images(self.player_selected + DIR_ATTACK + DIR_SIDE, 4), self.animation_speed)
                self.charging_time = 0
        else:
            self.charging = True
            self.animation = True
            self.set_player_frames(loading_images(self.player_selected + DIR_ATTACK + DIR_SIDE, 4), self.animation_speed)
            self.charging_time = 0 

    def exit(self):
        exit()

def on_mouse_down(pos, button):
    if button == mouse.LEFT:
        if game.status == STATE_MENU:
            for button in game.screens.menu():
                if button.is_hovered(pos):
                    button.action()
        elif game.status == STATE_SETTINGS or game.status == STATE_PAUSED_CONFIG:
            for button in game.screens.settings():
                if button.is_hovered(pos):
                    button.action()
            if game.music_volume_slider.is_hovered_indicator(pos):
                game.music_volume_slider.dragging = True
            if game.effects_volume_slider.is_hovered_indicator(pos):
                game.effects_volume_slider.dragging = True
            if game.resolution_dropdown.is_hovered(pos):
                selected_option = game.resolution_dropdown.select_option(pos)
                if selected_option:
                    game.change_resolution(selected_option)
            elif not game.resolution_dropdown.is_hovered(pos) and game.resolution_dropdown.open:
                game.resolution_dropdown.open = False
        elif game.status == STATE_PLAYING:
            game.atack_pressed()
        elif game.status == STATE_PAUSED:
            for button in game.screens.pause():
                if button.is_hovered(pos):
                    button.action()
        elif game.status == STATE_GAME_OVER:
            for button in game.screens.game_over():
                if button.is_hovered(pos):
                    button.action()

def on_mouse_up(pos, button):
    if button == mouse.LEFT:
        if game.status == STATE_SETTINGS or game.status == STATE_PAUSED_CONFIG:
            game.music_volume_slider.dragging = False
            game.effects_volume_slider.dragging = False
        if game.status == STATE_PLAYING:
            if game.charging:
                game.atack_pressed()


def on_mouse_move(pos):
    global MOUSE_POS
    MOUSE_POS = pos
    if game.status == STATE_SETTINGS or game.status == STATE_PAUSED_CONFIG:
        if game.music_volume_slider.dragging:
            game.music_volume_slider.update_value(pos)
            game.music_volume = game.music_volume_slider.value
            pgzero.music.set_volume(game.music_volume)
        if game.effects_volume_slider.dragging:
            game.effects_volume_slider.update_value(pos)
            game.effects_volume = game.effects_volume_slider.value
            sounds.shot.set_volume(game.effects_volume)

def on_key_down(key):
    if game.status == STATE_PLAYING:
        if key == keys.F1:
            game.freeze_mode = not game.freeze_mode
            if game.freeze_mode:
                print("Modo de congelamento ativado.")
            else:
                print("Modo de congelamento desativado.")
        if key == keys.F2:
            game.draw_hitbox = not game.draw_hitbox
        if key == keys.SPACE:            
            game.atack_pressed()
    
def on_key_up(key):
    if game.status == STATE_PLAYING:
        if key == keys.SPACE:
            if game.charging:
                game.atack_pressed()

def update(dt):
    if game.status == STATE_PLAYING:
        if not game.freeze_mode:
            game.draw_playing(dt)         
            horizontal = abs(MOUSE_POS[0] - game.player.tile.x) > abs(MOUSE_POS[1] - game.player.tile.y)
            if horizontal:
                dir_sprite = DIR_SIDE
                flip_x = MOUSE_POS[0] < game.player.tile.x
            else:
                dir_sprite = DIR_DOWN if MOUSE_POS[1] > game.player.tile.y else DIR_UP
            if game.charging:
                game.animation = True
                game.set_player_frames(loading_images(game.player_selected + DIR_ATTACK + dir_sprite, 5 if horizontal else 4), game.animation_speed)
            else:
                game.set_player_frames(loading_images(game.player_selected + DIR_WALKING + dir_sprite, 6), game.animation_speed)
            if horizontal:
                game.player.tile.flip_x = flip_x

def draw():
    if game.status == STATE_MENU:
        screen.clear()
        game.draw_menu()
    elif game.status == STATE_SETTINGS or game.status == STATE_PAUSED_CONFIG:
        screen.clear()
        game.draw_settings()
    elif game.status == STATE_PAUSED:
        game.draw_pause()
    elif game.status == STATE_GAME_OVER:
        screen.clear()
        game.draw_game_over()          
    if game.status == STATE_PLAYING:
        screen.clear()
        game.mapa.draw()
        game.draw_player()
        game.draw_hud()
        if game.draw_hitbox:
            screen.draw.rect(Rect(game.player.hitbox), (255, 0, 0))
            for enemy in game.enemies:
                screen.draw.rect(Rect(enemy.hitbox), (0, 255, 0))
            for projectil in game.projectiles:
                screen.draw.rect(Rect(projectil.tile.x, projectil.tile.y, projectil.tile.width, projectil.tile.height), (0, 0, 255))

# Inicialização rápida do jogo
game = Game()
pgzrun.go()