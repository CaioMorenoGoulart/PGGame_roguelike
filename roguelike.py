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

# Ajustar hitbox
def right_hitbox(actor):
    actor.hitbox = Rect(
        (actor.tile.x + 1) - actor.tile.width / 2,
        (actor.tile.y + 1) - actor.tile.height / 2,
        actor.tile.width - 2,
        actor.tile.height - 2
    )

class Time_texts:
    def __init__(self, text, pos):
        self.text = text
        self.time = 0
        self.pos = pos
        
    def update(self, dt):
        self.time+= dt


# Classe Power_up:
class Power_ups:
    def __init__(self, x, y, tipe, scale=1):
        self.current_frame = 0
        self.scale = scale
        self.tipe = tipe
        self.animation_timer = 0
        self.text = ""
        self.set_frames()
        self.n_frames = len(self.frames)
        self.tile.pos = (x, y)
        self.update_frames(1/60)
    def pick_up(self):
        if self.tipe == PW_HEALTH:
            if game.player_health < 200:
                game.player_health += self.pw
        elif self.tipe == PW_CADENCE:
            if game.shoot_cooldown > 0.05:
                game.shoot_cooldown *= self.pw
        elif self.tipe == PW_MOVIMENT_SPEED:
            if game.speed_moviment < 0.4:
                game.speed_moviment *= self.pw
        
    def draw(self):
        self.tile.draw()
        
    def set_frames(self):
        if self.tipe == PW_HEALTH:
            self.pw = random.randrange(1,10)
            self.text = (f"+ {self.pw} de vida")
            self.frames = Set_images(string= Dir_images.Pw.dir + "health_", n_frames= 8).images
        elif self.tipe == PW_CADENCE:
            self.pw = 0.99
            self.text = (f"+ 0.1% de cadência")
            self.frames = Set_images(string= Dir_images.Pw.dir + "cadence_", n_frames= 11).images
        elif self.tipe == PW_MOVIMENT_SPEED:
            self.pw = 1.01
            self.text = (f"+ 0.1% de movimento")
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

# Classe Entidade
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

class Slider:
    def __init__(self, x, y, screen_width, initial_value=0.5):
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.screen_height = 10
        self.value = initial_value
        self.dragging = False
        self.indicator_radius = 10

    def draw(self):
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

class Game:
    def __init__(self):
        self.settings = CONFIG
        self.mapa = Map()
        self.mapa.draw_map()
        self.freeze_mode = False
        self.draw_hitbox = False
        self.status = STATE_MENU
        self.paused = False
        self.music_volume = self.settings["music_volume"]
        self.effects_volume = self.settings["effects_volume"]
        self.screen_opt = self.settings["screen_opt"]
        self.music_volume_slider = Slider(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, self.music_volume)
        self.effects_volume_slider = Slider(WIDTH // 2 - 100, HEIGHT // 2 + 170, 200, self.effects_volume)
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
        self.text_pw_list = [Time_texts]
    
    def play_sound_volume(self, sound, vol = 1):
        getattr(sounds, sound).set_volume(self.opt.slide[1].value * vol)
        getattr(sounds, sound).play()
    def draw_menu(self):
        import screens.menu
        self.opt = screens.menu.menu.buttons
        [i.draw(screen, MOUSE_POS) for i in self.opt]

    def call_settings(self):
        if self.status == STATE_MENU or self.status == STATE_GAME_OVER:
            self.status = STATE_SETTINGS
        elif self.status == STATE_PAUSED:
            self.status = STATE_PAUSED_CONFIG

    def draw_settings(self):
        if self.status == STATE_SETTINGS:
            import screens.screen_config
            self.opt = screens.screen_config.menu
        elif self.status == STATE_PAUSED_CONFIG:
            import screens.config_pause
            self.opt = screens.config_pause.menu

        self.opt.dropdown.draw(screen, MOUSE_POS)

        [i.draw(screen, MOUSE_POS) for i in self.opt.buttons]
        [i.draw(screen) for i in self.opt.slide]


        # screen.draw.text(
        #     f"Volume Música: {int(self.music_volume * 100)}%",
        #     topleft=(self.music_volume_slider.x, self.music_volume_slider.y - 20),
        #     fontsize=FONT_SIZE_MENU,
        #     color=TEXT_COLOR,
        # )
        # screen.draw.text(
        #     f"Volume Efeitos: {int(self.effects_volume * 100)}%",
        #     topleft=(self.effects_volume_slider.x, self.effects_volume_slider.y - 20),
        #     fontsize=FONT_SIZE_MENU,
        #     color=TEXT_COLOR,
        # )

    def draw_pause(self):
        import screens.pause
        self.opt = screens.pause.menu.buttons
        [i.draw(screen, MOUSE_POS) for i in self.opt]

    def resume_game(self):
        self.status = STATE_PLAYING
        self.volume()
        save_settings(self.settings)
        pgzero.music.unpause()
        self.paused = False
        
    def back_to_menu(self):
        self.status = STATE_MENU
        self.paused = False
        game.save_updated_settings()

    def change_resolution(self, resolution):
        global SCRENN_OPT
        SCRENN_OPT = RESOLUTION_OPTIONS.index(resolution)

    def save_updated_settings(self):
        self.settings = {
            "music_volume": self.opt.slide[0].value,
            "effects_volume": self.opt.slide[1].value,
            "screen_opt": SCRENN_OPT,
        }
        save_settings(self.settings)

    def start_game(self):
        self.status = STATE_PLAYING
        self.player_selected = Dir_images.Characters.Player.Girl1
        self.player_health = 100
        self.score = 0
        self.enemies = []
        self.text_pw_list = []
        self.projectiles = []
        self.pw = []
        self.player.tile.pos = (WIDTH / 2 - self.player.tile.width, HEIGHT / 2 - self.player.tile.height)
        self.enemy_speed = .1
        self.time_elapsed = 0
        self.shoot_cooldown = 1
        self.speed_moviment = .1
        self.difficulty_score = 10
        self.total_time = 0
        self.volume()
        pgzero.music.play('music.wav')

    def volume(self):
        for sound in ARROW_SOUDS:
            getattr(sounds, sound).set_volume(self.opt.slide[1].value)
        pgzero.music.set_volume(self.music_volume)



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
        self.pw.append(Power_ups(x, y, pw_randon, 1.5))

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
                self.text_pw_list.append(Time_texts(pw.text, pw.tile.pos))
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
        # screen.draw.text(
        #     f"Pontuação: {self.score}",
        #     center=((WIDTH // 2), (HEIGHT // 2) - 150),
        #     fontsize=FONT_SIZE_MENU,
        #     color=TEXT_COLOR,
        # )
        # screen.draw.text(
        #     f"Tempo De jogo: {time_format(self.total_time)}",
        #     center=((WIDTH // 2), (HEIGHT // 2) - 100),
        #     fontsize=FONT_SIZE_MENU,
        #     color=TEXT_COLOR,
        # )
        import screens.game_over
        self.opt = screens.game_over.menu.buttons
        for i in self.opt:
            if "$pontuacao$" in i.text:
                i.text = i.text.replace("$pontuacao$", f"{self.score}")
            if "$tempo$" in i.text:
                i.text = i.text.replace("$tempo$", f"{time_format(self.total_time)}")
            i.draw(screen, MOUSE_POS)

    def draw_player(self):
        self.player.draw()

        for enemy in self.enemies:
            enemy.draw()

        for projectile in self.projectiles:
            projectile.draw()

        for pw in self.pw:
            pw.draw()

    def draw_hud(self):
        screen.draw.text(
            f"Pontuação: {self.score}",
            (10, 10),
            fontsize=FONT_SIZE_TEXTS,
            color="white",
            ocolor="black",
            owidth=1
        )
        screen.draw.text(
            f"Tempo de jogo: {time_format(self.total_time)}",
            (WIDTH - 250, 10),
            fontsize=FONT_SIZE_TEXTS,
            color="white",
            ocolor="black",
            owidth=1
        )
        screen.draw.text(
            f"Vida: {self.player_health:.0f}",
            (10, HEIGHT - 50),
            fontsize=FONT_SIZE_TEXTS,
            color="white",
            ocolor="black",
            owidth=1
        )
        for pw in self.text_pw_list:
            if pw.time < 2: 
                screen.draw.text(pw.text,
                    midbottom =(pw.pos[0], (pw.pos[1] - CELL_SIZE / 2) - pw.time*10 ),
                    fontsize=FONT_SIZE_ITENS,
                    color="white",
                    ocolor="black",
                    owidth=2,
                    alpha= (1 if pw.time < 1 else 2 - pw.time))
                
            else:
                self.text_pw_list.remove(pw)

        screen.draw.filled_rect(
            Rect(9, HEIGHT - 31, 202 if self.player_health * 2 < 202 else self.player_health * 2 + 2, 22),
            (0, 0, 0),
        )
        screen.draw.filled_rect(
            Rect(10, HEIGHT - 30, min(100 ,self.player_health) * 2, 20),
            HEALTH_COLOR,
        )
        screen.draw.filled_rect(
            Rect(210, HEIGHT - 30, (self.player_health - 100) * 2, 20),
            [0,0,255],
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
        if self.tab:
            draw_alpha_box(WIDTH/4, HEIGHT/4, (0,0,0, 128), screen, (CELL_SIZE,CELL_SIZE))
            screen.draw.text(f"Velocidade de ataque: {self.shoot_cooldown}",
                    (CELL_SIZE * 2 , CELL_SIZE * 2),
                    fontsize=FONT_SIZE_ITENS,
                    color="white",
                    ocolor="black",
                    owidth=2,
                    alpha= 100)
            screen.draw.text(f"Velocidade de movimento: {self.speed_moviment}",
                    (CELL_SIZE * 2 , CELL_SIZE * 3),
                    fontsize=FONT_SIZE_ITENS,
                    color="white",
                    ocolor="black",
                    owidth=2,
                    alpha= 100)
        
        # text_test = screen.draw.text("All together now:\nCombining the above options", center=(WIDTH/2,CELL_SIZE), fontsize=30, color="#AAFF00", gcolor="#66AA00", owidth=1.5, ocolor="black", alpha=0.8)

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

        if (keyboard.tab):
            self.tab = True
        else:
            self.tab = False

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
            
            for pw in self.text_pw_list:
                pw.update(dt)
            
            # self.spawn_pw()

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

def actions(action):
    if action == STATE_EXIT:
        game.exit()
    elif action == STATE_MENU:
        game.back_to_menu()
    elif action == STATE_PLAYING:
        game.start_game()
    elif action == STATE_SETTINGS or action == STATE_PAUSED_CONFIG:
        game.call_settings()
    elif action == STATE_RESUME_GAME:
        game.resume_game()

def on_mouse_down(pos, button):
    if button == mouse.LEFT:
        if game.status == STATE_MENU:
            for button in game.opt:
                if button.is_hovered(pos):
                    actions(button.action)
        elif game.status == STATE_SETTINGS or game.status == STATE_PAUSED_CONFIG:
            for button in game.opt.buttons:
                if button.is_hovered(pos):
                    actions(button.action)
            if game.music_volume_slider.is_hovered_indicator(pos):
                game.music_volume_slider.dragging = True
            if game.effects_volume_slider.is_hovered_indicator(pos):
                game.effects_volume_slider.dragging = True
            if game.opt.dropdown.is_hovered(pos) and not game.opt.dropdown.open:
                game.opt.dropdown.open = True
            elif game.opt.dropdown.open:
                selected_option = game.opt.dropdown.select_option(pos)
                if selected_option:
                    game.change_resolution(selected_option)
        elif game.status == STATE_PLAYING:
            game.atack_pressed()
        elif game.status == STATE_PAUSED:
            for button in game.opt:
                if button.is_hovered(pos):
                    actions(button.action)
        elif game.status == STATE_GAME_OVER:
            for button in game.opt:
                if button.is_hovered(pos):
                    actions(button.action)


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
        if game.opt.slide[0].dragging:
            game.opt.slide[0].update_value(pos)
            pgzero.music.set_volume(game.opt.slide[0].value)
        if game.opt.slide[1].dragging:
            game.opt.slide[1].update_value(pos)
            sounds.shot.set_volume(game.opt.slide[0].value)


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
            draw_alpha_box(WIDTH, HEIGHT, (0,0,0, 100), screen, (0,0))
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