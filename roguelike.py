from config import *

# Criação do Mapa
class Map:
    def __init__(self):
        self.MAP = []
        for row in range(ROWS):
            if row == 0 or row == ROWS - 1:
                self.MAP.append([1] * COLUMNS)
            else:
                self.MAP.append([1] + [0] * (COLUMNS - 2) + [1])

    # Randomizar grama
    def get_random_grass(self):
        grass_tile = Actor(random.choice(Set_images(string = Dir_images.Textures.dir + "grass_tile_", n_frames = 4).images), (0, 0), (0, 0))
        grass_tile.scale = SCAL
        return grass_tile

    # Desenhar Mapa
    def draw_map(self):
        self.map_tiles = []
        for y, row in enumerate(self.MAP):
            for x, tile in enumerate(row):
                if tile == 0:
                    grass_tile = self.get_random_grass()
                    grass_tile.x = x * grass_tile.height
                    grass_tile.y = y * grass_tile.width
                    self.map_tiles.append(grass_tile)
                elif tile == 1:
                    stone_tile = Actor(Set_images(string= Dir_images.Textures.dir + "stone_tile_", n_frames= 1).images[0], (0, 0), (0, 0))
                    stone_tile.scale = SCAL
                    stone_tile.x = x * stone_tile.height
                    stone_tile.y = y * stone_tile.width
                    self.map_tiles.append(stone_tile)

    def draw(self):
        for tile in self.map_tiles:
            tile.draw()


# Formatar Tempo
def time_format(seconds):
    hours = seconds // 3600
    minuts = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    return f"{hours:02.0f}:{minuts:02.0f}:{remaining_seconds:02.0f}"


# Ajustar hitbox
def right_hitbox(actor):
    actor.hitbox = Rect(
        (actor.tile.x + 1) - actor.tile.width / 2,
        (actor.tile.y + 1) - actor.tile.height / 2,
        actor.tile.width - 2,
        actor.tile.height - 2
    )


def draw_text_with_border(text, position, fontsize=30, color="white", border_color="black", border_width=2):
    x, y = position
    for dx in (-border_width, 0, border_width):
        for dy in (-border_width, 0, border_width):
            if dx != 0 or dy != 0:
                screen.draw.text(text, (x + dx, y + dy), fontsize=fontsize, color=border_color)
    screen.draw.text(text, (x, y), fontsize=fontsize, color=color)


# Classe Entidade
# class Power_up:
class Power_ups:
    def __init__(self, x, y, tipe, scale=1):
        self.current_frame = 0
        self.scale = scale
        self.tipe = tipe
        self.animation_timer = 0
        self.set_frames()
        self.n_frames = len(self.frames)
        self.tile.pos = (x, y)
        self.update_frames(1/60)
    def pick_up(self):
        if self.tipe == PW_HEALTH:
            game.player_health += random.randrange(1,10)
            print("Vida ",game.player_health)
        elif self.tipe == PW_CADENCE:
            game.shoot_cooldown *= 0.99
            print("Cadencia de tiro ",game.shoot_cooldown)
        elif self.tipe == PW_MOVIMENT_SPEED:
            game.speed_moviment *= 1.01
            print("Velocidade de movimento ",game.speed_moviment)
        
    def draw(self):
        self.tile.draw()

    def set_frames(self):
        if self.tipe == PW_HEALTH:
            self.frames = Set_images(string= Dir_images.Pw.dir + "health_", n_frames= 8).images
        elif self.tipe == PW_CADENCE:
            self.frames = Set_images(string= Dir_images.Pw.dir + "cadence_", n_frames= 11).images
        elif self.tipe == PW_MOVIMENT_SPEED:
            self.frames = Set_images(string= Dir_images.Pw.dir + "move_speed_", n_frames= 1).images
        
        self.tile = Actor(self.frames[self.current_frame])
        self.tile.scale = self.scale

    def update_frames(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= 1/ self.n_frames:
            self.current_frame = (self.current_frame + 1) % self.n_frames
            self.tile.image = self.frames[self.current_frame]
            self.tile.scale = self.scale
            self.animation_timer = 0

# class Sons do jogo:
class Songs_obj:
    def __init__(self, song, vol):
        self.song = song
        self.song_playing = False
        self.obj = getattr(sounds, self.song)
        self.obj.set_volume(vol)

    def play(self):
        self.obj.play()

    def stop(self):
        self.song_playing = False
        self.obj.stop()
    
    def pause(self):
        self.song_playing = False
        self.obj.pause()

    def update(self):
        if self.song_playing == False:
            self.play
        else:
            self.stop

class Entity:
    def __init__(self, x, y, frames, scale=1):
        self.frames = frames
        self.current_frame = 0
        self.tile = Actor(self.frames[self.current_frame])
        self.tile.scale = scale
        self.hit_cooldown = 0
        self.tile.pos = (x, y)
        self.state = ENTITY_NEW
        self.update_frames()

    def draw(self):
        self.tile.draw()

    def update_frames(self, charging=False):
        if charging:
            if self.current_frame < len(self.frames) - 1:
                self.current_frame += 1
                self.tile.image = self.frames[self.current_frame]
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
        if self.hit_cooldown == 0:
            new_x = self.tile.x + x * CELL_SIZE
            new_y = self.tile.y + y * CELL_SIZE
            if CELL_SIZE <= (new_x - self.tile.height / 2) <= (COLUMNS * CELL_SIZE - (CELL_SIZE + self.tile.height)) and CELL_SIZE <= (new_y - (self.tile.width / 2)) <= (ROWS * CELL_SIZE - (CELL_SIZE + self.tile.width)):
                if self.tile != game.player.tile:
                    animate(self.tile, pos=(new_x, new_y), duration=0.05)
                    self.animation = True
                else:
                    if game.player_skill_timer == 0:
                        animate(self.tile, pos=(new_x, new_y), duration=0.1)
                    else:
                        animate(self.tile, pos=(new_x, new_y), duration=0.01)
            else:
                # Deslisar pela parede
                if game.player_skill_timer == 0:
                    if CELL_SIZE > (new_x - self.tile.height / 2):
                        new_x = CELL_SIZE + self.tile.width
                    if (new_x - self.tile.height / 2) > (COLUMNS * CELL_SIZE - (CELL_SIZE + self.tile.height)):
                        new_x = WIDTH - (CELL_SIZE + self.tile.width)
                    if CELL_SIZE >= (new_y - (self.tile.width / 2)):
                        new_y = CELL_SIZE + self.tile.height / 2
                    if (new_y - (self.tile.width / 2)) > (ROWS * CELL_SIZE - (CELL_SIZE + self.tile.width)):
                        new_y = HEIGHT - (CELL_SIZE + self.tile.height)

                    animate(self.tile, pos=(new_x,new_y), duration=0.1)

# Classe Projétil
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
        self.tile.pos = (self.tile.x + self.direction_x * self.speed, self.tile.y + self.direction_y * self.speed)
        self.tile.angle = self.angles - 90

        if self.speed > 0:
            if self.offscreen():
                game.play_sound_volume(ARROW_SOUDS[3])
                self.hit(dt)
        else:
            if self.speed == 0:
                self.shoot_remove_cooldown += dt
        if self.shoot_remove_cooldown >= game.shoot_cadence:
            game.projectiles.remove(self)

    def draw(self):
        self.tile.draw()

    def hit(self, dt):
        self.speed = 0
        self.tile.image = Set_images(string= Dir_images.Weapons.dir + "arrow_", n_frames= 2).images[1]
        self.shoot_remove_cooldown += dt

    def offscreen(self):
        return self.tile.x < CELL_SIZE or self.tile.x > COLUMNS * CELL_SIZE - CELL_SIZE or self.tile.y < CELL_SIZE or self.tile.y > ROWS * CELL_SIZE - CELL_SIZE


# Criação do Botão
class Button:
    def __init__(self, x, y, text, action):
        self.x = x
        self.y = y
        self.text = text
        self.action = action
        self.screen_width = 200
        self.screen_height = 50

    def draw(self, mouse_pos):
        color = HOVER_COLOR if self.is_hovered(mouse_pos) else TEXT_COLOR
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

    def is_hovered(self, mouse_pos):
        return (
            self.x <= mouse_pos[0] <= self.x + self.screen_width
            and self.y <= mouse_pos[1] <= self.y + self.screen_height
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
            color=HOVER_COLOR if self.is_hovered(MOUSE_POS) else TEXT_COLOR,
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
        self.settings = CONFIG
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
        self.resolution_dropdown = Dropdown(WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, RESOLUTION_OPTIONS, self.screen_opt)
        self.difficulty_score = 10
        self.press = False
        self.charging = False
        self.charging_time = 0
        self.animation_speed = 0.05  # Tempo entre cada frame (em segundos)
        self.player = Entity(WIDTH // 2, HEIGHT // 2, Dir_images.Characters.Player.Girl1.Waiting.Down.images)
        self.enemy_animation_timer = 0  # Temporizador para a animação
        self.player_selected = ""
        self.player_animation_timer = 0
        self.player_skill_timer = 2 
        self.player_skill_cooldown = 2
        self.animation = False
        self.animation_string = ""
        self.score = 0
        self.projectiles = [Projectile]
        self.enemies = [Entity]
        self.pw = [Power_ups]
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
        self.sound_playng = False
        self.speed_moviment = .1
    
    def play_sound_volume(self, sound, vol = 1):
        getattr(sounds, sound).set_volume(game.effects_volume * vol)
        getattr(sounds, sound).play()
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
        self.volume()
        save_settings(self.settings)
        
    def back_to_menu(self):
        game.save_updated_settings()
        self.status = STATE_MENU
        self.paused = False

    def change_resolution(self, resolution):
        global SCRENN_OPT
        SCRENN_OPT = RESOLUTION_OPTIONS.index(resolution)

    def save_updated_settings(self):
        self.settings = {
            "music_volume": self.music_volume,
            "effects_volume": self.effects_volume,
            "screen_opt": SCRENN_OPT,
        }
        save_settings(self.settings)

    def start_game(self):
        self.status = STATE_PLAYING
        self.player_selected = Dir_images.Characters.Player.Girl1
        self.player_health = 100
        self.score = 0
        self.enemies = []
        self.projectiles = []
        self.pw = []
        self.player.tile.pos = (WIDTH / 2 - self.player.tile.width, HEIGHT / 2 - self.player.tile.height)
        self.enemy_speed = .1
        self.time_elapsed = 0
        self.shoot_cooldown = 1
        self.speed_moviment = .1
        self.volume()

    def volume(self):
        for sound in ARROW_SOUDS:
            getattr(sounds, sound).set_volume(self.effects_volume)
        pgzero.music.set_volume(self.music_volume)
        pgzero.music.play('music.wav')



    def shoot_projectile(self, mouse_pos):
        direction_x = mouse_pos[0] - self.player.tile.x
        direction_y = mouse_pos[1] - self.player.tile.y
        magnitude = math.sqrt(direction_x ** 2 + direction_y ** 2)
        # self.play_projectile_sound()
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
                Set_images(string= Dir_images.Weapons.dir + "arrow_", n_frames= 2).images[0]
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

                enemy.move(dx * self.enemy_speed, 2 * dy * self.enemy_speed)

    def spawn_enemy(self):
        x = random.randint(2, COLUMNS - 2) * CELL_SIZE
        y = random.randint(2, ROWS - 2) * CELL_SIZE
        self.enemies.append(Entity(x, y, Set_images(string= Dir_images.Characters.Player.Enemy.dir, n_frames= Dir_images.Characters.Player.Enemy.N_FRAMES).images))

    def spawn_pw(self):
        x = random.randint(2, COLUMNS - 2) * CELL_SIZE
        y = random.randint(2, ROWS - 2) * CELL_SIZE
        pw_randon = random.choice(POWER_UPS)
        self.pw.append(Power_ups(x, y, pw_randon, 2))

    def check_player_enemy_collision(self):
        if self.player_skill_timer > 0.2:
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
    def check_player_pw_collision(self):
        for pw in self.pw:
            if pw.tile.colliderect(self.player.tile):
                pw.pick_up()
                self.pw.remove(pw)

    def check_projectile_enemy_collision(self, dt):
        for enemy in self.enemies:
            if 0 < enemy.hit_cooldown < self.enemy_remove_interval:
                enemy.hit_cooldown += dt
            if enemy.hit_cooldown >= (self.enemy_remove_interval - 1) and enemy.hit_cooldown < self.enemy_remove_interval:
                enemy.tile.scale = 2
                if enemy.state != ENTITY_EXPLOSION:
                    enemy.state = ENTITY_EXPLOSION
                    self.play_sound_volume("explosion", 1.5)
                    enemy.frames = Set_images(string= Dir_images.Characters.Player.Enemy.dir + "bomb/bomb_", n_frames= 4).images

            if enemy.hit_cooldown > self.enemy_remove_interval:
                self.score += 1
                self.enemies.remove(enemy)
            for projectile in self.projectiles:
                if projectile.speed > 0 and enemy.hit_cooldown == 0:
                    if projectile.tile.colliderect(enemy.tile):
                        enemy.state = ENTITY_HIT
                        enemy.hit_cooldown += dt
                        self.play_sound_volume(ARROW_SOUDS[2])
                        projectile.hit(dt)
                        enemy.frames = Set_images(string= Dir_images.Characters.Player.Enemy.dir + "enemi_dead_", n_frames= 2).images

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
            center=((WIDTH // 2), (HEIGHT // 2) - 150),
            fontsize=30,
            color=TEXT_COLOR,
        )
        screen.draw.text(
            f"Tempo De jogo: {time_format(self.total_time)}",
            center=((WIDTH // 2), (HEIGHT // 2) - 100),
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

        for pw in self.pw:
            pw.draw()

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
            (0, 0, 0),
        )
        screen.draw.filled_rect(
            Rect(10, HEIGHT - 30, self.player_health * 2, 20),
            HEALTH_COLOR,
        )
        x = (self.player.tile.x - CELL_SIZE/2)
        y = (self.player.tile.y + CELL_SIZE/2) + 3

        screen.draw.filled_rect(
            Rect(x-1, y-1, 32, 8),
            (0, 0, 0),
        )
        
        img_skill_cooldown = Actor(self.player_selected.Walking.Side.images[2], (250, HEIGHT - 40),(0,0))
        img_skill_cooldown_2 = Actor(self.player_selected.Walking.Side.images[0], (img_skill_cooldown.x + img_skill_cooldown.height - 10, img_skill_cooldown.y),(0,0))

        img_arrow_cooldown = Actor(Set_images(string= Dir_images.Weapons.dir + "arrow_", n_frames= 1).images[0], (240, HEIGHT - 35),(0,0))
        img_arrow_cooldown.angle = -45
        img_arrow_cooldown.scale = 1.75

        img_skill_cooldown._surf.set_alpha(min( 255, self.player_skill_timer * 128))
        img_skill_cooldown_2._surf.set_alpha(min( 255, self.player_skill_timer * 128))

        if len(self.projectiles) > 0:
            shoot = self.projectiles[len(self.projectiles) - 1]
            shoot_fill = shoot.shoot_spawn_cooldown/self.shoot_cooldown
            img_arrow_cooldown._surf.set_alpha(min( 255, shoot_fill * 255))
            screen.draw.filled_rect(
                Rect(x, y,  min(1, shoot_fill) * 30, 6),
                HEALTH_COLOR,
            )
        else:
            img_arrow_cooldown._surf.set_alpha(255)
            Actor(Set_images(string= Dir_images.Weapons.dir + "arrow_", n_frames= 1).images[0], (0,0),(0,0))
            screen.draw.filled_rect(
                Rect(x, y,  30 , 6),
                HEALTH_COLOR,
            )
        img_arrow_cooldown.draw()
        img_skill_cooldown.draw()
        img_skill_cooldown_2.draw()



    def keybord_press(self):
        if self.charging:
            move_pixel = 0
        else:
            move_pixel = self.speed_moviment
        # if (keyboard.lshift):
        #     move_pixel *= 1.5
        dx = MOUSE_POS[0] - self.player.tile.x
        dy = MOUSE_POS[1] - self.player.tile.y
        magnitude = math.sqrt(dx**2 + dy**2)
        if magnitude > 0:
            dx /= magnitude
            dy /= magnitude

        if (keyboard.lshift):
            if self.player_skill_timer > self.player_skill_cooldown:
                self.player_skill_timer = 0
                self.play_sound_volume(random.choice(WOOSH_SOUDS), .5)
            elif 0 <= self.player_skill_timer <= .2:
                self.player.move(dx * 0.5, dy * 0.5)
        
        if self.player_skill_timer > 0.2:
            if (keyboard.LEFT or keyboard.A) and (keyboard.UP or keyboard.W):
                self.player.move(-move_pixel, -move_pixel)
            elif (keyboard.LEFT or keyboard.A) and (keyboard.DOWN or keyboard.S):
                self.player.move(-move_pixel, move_pixel)
            elif (keyboard.RIGHT or keyboard.D) and (keyboard.UP or keyboard.W):
                self.player.move(move_pixel, -move_pixel)
            elif (keyboard.RIGHT or keyboard.D) and (keyboard.DOWN or keyboard.S):
                self.player.move(move_pixel, move_pixel)
            elif (keyboard.LEFT or keyboard.A):
                self.player.move(-move_pixel, 0)
            elif (keyboard.RIGHT or keyboard.D):
                self.player.move(move_pixel, 0)
            elif (keyboard.UP or keyboard.W):
                self.player.move(0, -move_pixel)
            elif (keyboard.DOWN or keyboard.S):
                self.player.move(0, move_pixel)

        
        if self.charging:
            getattr(sounds, "walking").stop()

        move_keys = True in [keyboard.LEFT, keyboard.RIGHT, keyboard.UP, keyboard.DOWN, keyboard.A, keyboard.D, keyboard.W, keyboard.S]
        if move_keys and (self.sound_playng == False):
            self.sound_playng = True
            self.play_sound_volume("walking")
        elif not move_keys and self.sound_playng == True or self.charging:
            self.sound_playng = False
            getattr(sounds, "walking").stop()

        if self.charging:
            self.set_player_frames(Player(Dir.Player.DIR , Dir.Characteres.GIRL_1, Dir.Actions.ATTACK, dir_sprite).images, Player(Dir.Player.DIR , Dir.Characteres.GIRL_1, Dir.Actions.ATTACK, dir_sprite).animation_time)
        elif not move_keys and not self.charging:
            self.animation = True
            self.set_player_frames(Player(Dir.Player.DIR , Dir.Characteres.GIRL_1, Dir.Actions.WAITING, dir_sprite).images, Player(Dir.Player.DIR , Dir.Characteres.GIRL_1, Dir.Actions.WAITING, dir_sprite).animation_time)
        elif move_keys and not self.charging:
            self.animation = True
            self.set_player_frames(Player(Dir.Player.DIR , Dir.Characteres.GIRL_1, Dir.Actions.WALKING, dir_sprite).images, Player(Dir.Player.DIR , Dir.Characteres.GIRL_1, Dir.Actions.WALKING, dir_sprite).animation_time)


    def set_player_frames(self, frames, time):
        self.player.frames = frames
        if self.player_animation_timer >= self.animation_speed + time and self.animation:
            self.player_animation_timer = 0
            self.player.update_frames(self.charging)

    def draw_playing(self, dt):
        if self.status == STATE_PLAYING:
            self.total_time += dt  # Atualiza o tempo total decorrido
            self.elapsed_time += dt
            self.enemy_animation_timer += dt
            self.player_animation_timer += dt
            self.player_skill_timer += dt

            # Atualiza a animação dos inimigos
            if self.enemy_animation_timer >= self.animation_speed:
                self.enemy_animation_timer = 0  # Reseta o temporizador
                for enemy in self.enemies:
                    if enemy.hit_cooldown <= 1:
                        if enemy.tile.x > self.player.tile.x:
                            enemy.tile.flip_x = True
                        else:
                            enemy.tile.flip_x = False
                    enemy.update_frames()
            if self.charging:
                self.charging_time = min(self.charging_time + dt, 2)
            if self.elapsed_time >= 1 and self.difficulty_score < self.score:
                self.difficulty_score += 10
                self.increase_difficulty()
                self.spawn_pw()
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

            for pw in self.pw:
                pw.update_frames(dt)

            self.keybord_press()
            self.check_player_pw_collision()
            self.check_projectile_enemy_collision(dt)
            self.check_player_enemy_collision()

    def atack_pressed(self):
        if self.charging:
            self.charging = False
            self.shoot_projectile(MOUSE_POS)
            getattr(sounds, ARROW_SOUDS[0]).stop()
            self.play_sound_volume(ARROW_SOUDS[1])
            self.player.tile.image = self.player.frames[1]
        elif len(self.projectiles) > 0:
            if self.projectiles[len(self.projectiles) - 1].shoot_spawn_cooldown > self.shoot_cooldown:
                self.animation = True
                self.charging = True
                self.set_player_frames(Player(Dir.Player.DIR , Dir.Characteres.GIRL_1, Dir.Actions.ATTACK, dir_sprite).images, Player(Dir.Player.DIR , Dir.Characteres.GIRL_1, Dir.Actions.ATTACK, dir_sprite).animation_time)
                self.charging_time = 0
                self.play_sound_volume(ARROW_SOUDS[0])
        else:
            self.animation = True
            self.charging = True
            self.set_player_frames(Player(Dir.Player.DIR , Dir.Characteres.GIRL_1, Dir.Actions.ATTACK, dir_sprite).images, Player(Dir.Player.DIR , Dir.Characteres.GIRL_1, Dir.Actions.ATTACK, dir_sprite).animation_time)
            self.charging_time = 0
            self.play_sound_volume(ARROW_SOUDS[0])


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
            game.animation = False


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
        game.animation = True
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
    if key == keys.ESCAPE:
        if game.status == STATE_PLAYING:
            pause_game()
        elif game.status == STATE_PAUSED:
            resume_game()
def on_key_up(key):
    if game.status == STATE_PLAYING:
        game.animation = False
        if key == keys.SPACE:
            if game.charging:
                game.atack_pressed()

def resume_game():
    game.status = STATE_PLAYING
    pgzero.music.unpause()
    game.paused = False

def pause_game():
    game.status = STATE_PAUSED
    pgzero.music.pause()
    game.paused = True


def update(dt):
    global dir_sprite, horizontal
    if game.status == STATE_PLAYING:
        if not game.freeze_mode:
            horizontal = abs(MOUSE_POS[0] - game.player.tile.x) > abs(MOUSE_POS[1] - game.player.tile.y)
            if horizontal:
                dir_sprite = Dir.Directions.SIDE
                game.player.tile.flip_x = MOUSE_POS[0] < game.player.tile.x
            else:
                dir_sprite = Dir.Directions.DOWN if MOUSE_POS[1] > game.player.tile.y else Dir.Directions.UP
            game.draw_playing(dt)
    else:
        getattr(sounds, "walking").stop()
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