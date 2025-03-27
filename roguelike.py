from scripts.style import *
from scripts.config import *

import os, sys
dirpath = os.getcwd()
sys.path.append(dirpath)
if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)
###

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
        right_hitbox(self)
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
        elif self.tipe == "exp":
            game.score += self.pw
            game.play_sound_volume(sound="gem",vol=.5)
        
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
        elif self.tipe == "exp":
            self.pw = random.randrange(1,10)
            self.text = (f"+ {self.pw}% de experiência")
            self.frames = Set_images(string= Dir_images.Pw.dir + "exp_", n_frames= 8).images
        
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
        self.project_hit_cooldown = 0
        self.entity_hit_cooldown = 0
        self.tile.pos = (x, y)
        self.state = ENTITY_NEW
        self.update_frames()
        right_hitbox(self)

    def draw(self):
        right_hitbox(self)
        self.tile.draw()

    def update_frames(self, charging=False):
        right_hitbox(self)
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

    def move(self, x, y):
        if self.project_hit_cooldown == 0:
            new_x = self.tile.x + x * CELL_SIZE
            new_y = self.tile.y + y * CELL_SIZE
            pos=(new_x, new_y)
            if game.mapa.pos_in_map(self.tile, x * CELL_SIZE, y * CELL_SIZE):
                if self.tile != game.player.tile:
                    animate(self.tile, pos=pos, duration=0.05)
                    self.animation = True
                else:
                    if game.player_skill_timer == 0:
                        animate(self.tile, pos=pos, duration=0.1)
                    else:
                        animate(self.tile, pos=pos, duration=0.01)

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
        self.hitbox.inflate_ip(-5, -5)

    def update(self, dt):
        self.shoot_spawn_cooldown += dt
        self.tile.pos = (self.tile.x + self.direction_x * self.speed, self.tile.y + self.direction_y * self.speed)
        self.tile.angle = self.angles - 90

        if self.speed > 0:
            if not game.mapa.pos_in_map(self.tile):
                game.play_sound_volume(ARROW_SOUDS[3])
                self.hit(dt)
        else:
            if self.speed == 0:
                self.shoot_remove_cooldown += dt
        if self.shoot_remove_cooldown >= game.shoot_cadence:
            game.projectiles.remove(self)
        right_hitbox(self)
        self.hitbox.inflate_ip(-2, -2)

    def draw(self):
        self.tile.draw()

    def hit(self, dt):
        self.speed = 0
        self.tile.image = Set_images(string= Dir_images.Weapons.dir + "arrow_", n_frames= 2).images[1]
        self.shoot_remove_cooldown += dt

class Game:
    def __init__(self):
        self.settings = CONFIG
        self.freeze_mode = False
        self.draw_hitbox = False
        self.status = STATE_MENU
        self.paused = False
        self.difficulty_score = 100
        self.press = False
        self.charging = False
        self.charging_time = 0
        self.animation_speed = 0.05  # Tempo entre cada frame (em segundos)
        self.enemy_animation_timer = 0  # Temporizador para a animação
        self.player_animation_timer = 0
        self.player_selected = any
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
        self.damage_cooldown = .001  # Cooldown entre danos
        self.shoot_cadence = 1
        self.shoot_cooldown = 1
        self.sound_playng = False
        self.speed_moviment = .1
        self.text_pw_list = [Float_texts]
    
    def play_sound_volume(self, sound = "", music = "", vol = 1.0):
        if sound:
            getattr(sounds, sound).set_volume(EFFECT_VOL * vol)
            getattr(sounds, sound).play()
        if music:
            pgzero.music.set_volume(MUSIC_VOL * vol)
            pgzero.music.play(music)

    def draw_menu(self):
        import scripts.screens.menu
        self.opt = scripts.screens.menu.menu

    def call_settings(self):
        if self.status == STATE_MENU or self.status == STATE_GAME_OVER:
            self.status = STATE_SETTINGS
        elif self.status == STATE_PAUSED:
            self.status = STATE_PAUSED_CONFIG

    def draw_settings(self):
        if self.status == STATE_SETTINGS:
            import scripts.screens.screen_config
            self.opt = scripts.screens.screen_config.menu
        elif self.status == STATE_PAUSED_CONFIG:
            import scripts.screens.config_pause
            self.opt = scripts.screens.config_pause.menu

    def draw_pause(self):
        import scripts.screens.pause
        self.opt = scripts.screens.pause.menu
    
    def draw_player_select(self):
        import scripts.screens.player_selection
        self.opt = scripts.screens.player_selection.menu

    def draw_controlls(self):
        import scripts.screens.controlls
        self.opt = scripts.screens.controlls.menu

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
            "music_volume": MUSIC_VOL,
            "effects_volume": EFFECT_VOL,
            "screen_opt": SCRENN_OPT,
        }
        save_settings(self.settings)

    def start_game(self):
        from scripts.map import Map
        self.mapa = Map()
        self.mapa.draw_map()
        self.status = STATE_PLAYING
        self.player_health = 100
        self.score = 0
        self.text_pw_list = []
        self.projectiles = []
        self.pw = []
        self.exp = []
        self.player = Entity(WIDTH // 2, HEIGHT // 2, self.player_selected.Waiting.Down.images)
        self.player.tile.pos = (WIDTH / 2 - self.player.tile.width, HEIGHT / 2 - self.player.tile.height)
        self.time_elapsed = 0
        self.shoot_cooldown = 1
        self.speed_moviment = .1
        self.total_time = 0
        self.volume()
        self.enemy()
        pgzero.music.play('music.wav')

    def enemy(self):
        self.difficulty_score = 100
        self.enemies = []
        self.enemy_speed = .1
        self.enemy_spawn_interval = 2

    def volume(self):
        for sound in ARROW_SOUDS:
            getattr(sounds, sound).set_volume(EFFECT_VOL)
        pgzero.music.set_volume(MUSIC_VOL)



    def shoot_projectile(self, mouse_pos):
        direction_x = mouse_pos[0] - self.player.tile.x
        direction_y = mouse_pos[1] - self.player.tile.y
        magnitude = math.sqrt(direction_x ** 2 + direction_y ** 2)
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
            if enemy.project_hit_cooldown == 0:
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
                if enemy.hitbox.colliderect(self.player.hitbox):
                    if self.total_time - enemy.entity_hit_cooldown >= self.damage_cooldown:
                        enemy.entity_hit_cooldown = self.total_time
                        if enemy.state == ENTITY_NEW:
                            self.player_health -= 0.2
                        elif enemy.state == ENTITY_HIT:
                            self.player_health -= 0
                        elif enemy.state == ENTITY_EXPLOSION:
                            self.player_health -= 2
                        if self.player_health <= 0:
                            self.status = STATE_GAME_OVER
                            pgzero.music.stop()
    def check_player_pw_collision(self):
        for pw in self.pw:
            if pw.hitbox.colliderect(self.player.hitbox):
                pw.pick_up()
                self.text_pw_list.append(Float_texts(pw.text, (pw.tile.pos[0], pw.tile.pos[1] - CELL_SIZE/2), FONT_SIZE_ITENS))
                self.pw.remove(pw)

    def check_projectile_enemy_collision(self, dt):
        for enemy in self.enemies:
            if 0 < enemy.project_hit_cooldown < self.enemy_remove_interval:
                enemy.project_hit_cooldown += dt
            if enemy.project_hit_cooldown >= (self.enemy_remove_interval - 1) and enemy.project_hit_cooldown < self.enemy_remove_interval:
                enemy.tile.scale = 2
                if enemy.state != ENTITY_EXPLOSION:
                    enemy.state = ENTITY_EXPLOSION
                    self.play_sound_volume("explosion", vol=1.5)
                    enemy.frames = Set_images(string= Dir_images.Characters.Player.Enemy.dir + "bomb/bomb_", n_frames= 4).images

            if enemy.project_hit_cooldown > self.enemy_remove_interval:
                self.pw.append(Power_ups(enemy.tile.x, enemy.tile.y, "exp", .5))
                self.enemies.remove(enemy)
            for projectile in self.projectiles:
                if projectile.speed > 0 and enemy.project_hit_cooldown == 0:
                    if projectile.hitbox.colliderect(enemy.hitbox):
                        enemy.state = ENTITY_HIT
                        enemy.project_hit_cooldown += dt
                        self.play_sound_volume(ARROW_SOUDS[2])
                        projectile.hit(dt)
                        enemy.frames = Set_images(string= Dir_images.Characters.Player.Enemy.dir + "enemi_dead_", n_frames= 2).images

    def increase_difficulty(self):
        self.enemy_speed += 0.01
        self.enemy_spawn_interval = max(0.5, self.enemy_spawn_interval - 0.1)

    def draw_game_over(self):
        import scripts.screens.game_over
        self.opt = scripts.screens.game_over.menu

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
            f"Exp: {(self.score % 100):.0f}%",
            topright = (WIDTH*.1 - 2, 2),
            fontsize=FONT_SIZE_ITENS,
            color="white",
            ocolor="black",
            owidth=1
        )
        screen.draw.text(
            f"Nivel {int(self.score / 100)}",
            centerx = WIDTH/2,
            bottom = CELL_SIZE,
            fontsize=FONT_SIZE_TEXTS,
            color="white",
            ocolor="black",
            owidth=1
        )
        back_exp_box = box(WIDTH*.8, 5, (0, 0, 0, 100), (0,0,0),1)
        back_exp_box.draw(screen, (WIDTH*.1, 5))

        exp_box = any
        if self.score != 0:
            exp_box = box(((back_exp_box.rect.width/100) * (self.score % 100)) - 2, 3, (0, 0, 255,150), (0,0,0))

            if self.score % 100 == 0:
                exp_box = box(back_exp_box.rect.width - 2, 3, (0, 0, 255, 150), (0,0,0))

            exp_box.draw(screen, (WIDTH*.1 + 1, 6))

            

        
        screen.draw.text(
            f"Tempo de jogo: {time_format(self.total_time)}",
            right = WIDTH - 5,
            bottom = CELL_SIZE,
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
            pw.draw(screen)
            if pw.time >= 2: 
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
            box(WIDTH/4, HEIGHT/4, (0,0,0, 128)).draw(screen, (CELL_SIZE,CELL_SIZE))
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

        if game.draw_hitbox:
            box(game.player.hitbox.width, game.player.hitbox.height, (0, 0, 0, 0), (255, 0, 0, 255), 1).draw(screen, (game.player.hitbox.x, game.player.hitbox.y))
            for enemy in game.enemies:
                box(enemy.hitbox.width, enemy.hitbox.height, (0, 0, 0, 0), (0, 255, 0, 255), 1).draw(screen, (enemy.hitbox.x, enemy.hitbox.y))
            for projectil in game.projectiles:
                box(projectil.hitbox.width, projectil.hitbox.height, (0, 0, 0, 0), (0, 0, 255, 255), 1).draw(screen, (projectil.hitbox.x, projectil.hitbox.y))
            for pw in game.pw:
                box(pw.hitbox.width, pw.hitbox.height, (0, 0, 0, 0), (255, 255, 0, 255), 1).draw(screen, (pw.hitbox.x, pw.hitbox.y))

        img_arrow_cooldown.draw()
        img_skill_cooldown.draw()
        img_skill_cooldown_2.draw()

    def keybord_press(self):
        if self.charging:
            move_pixel = 0
        else:
            move_pixel = self.speed_moviment
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
                self.play_sound_volume(random.choice(WOOSH_SOUDS), vol=.5)
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
            self.set_player_frames(Player(self.player_selected._dir , self.player_selected.dir_, Dir.Actions.ATTACK, dir_sprite).images, Player(self.player_selected._dir , self.player_selected.dir_, Dir.Actions.ATTACK, dir_sprite).animation_time)
        elif not move_keys and not self.charging:
            self.animation = True
            self.set_player_frames(Player(self.player_selected._dir , self.player_selected.dir_, Dir.Actions.WAITING, dir_sprite).images, Player(self.player_selected._dir , self.player_selected.dir_, Dir.Actions.WAITING, dir_sprite).animation_time)
        elif move_keys and not self.charging:
            self.animation = True
            self.set_player_frames(Player(self.player_selected._dir , self.player_selected.dir_, Dir.Actions.WALKING, dir_sprite).images, Player(self.player_selected._dir , self.player_selected.dir_, Dir.Actions.WALKING, dir_sprite).animation_time)


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
                    if enemy.project_hit_cooldown <= 1:
                        if enemy.tile.x > self.player.tile.x:
                            enemy.tile.flip_x = True
                        else:
                            enemy.tile.flip_x = False
                    enemy.update_frames()
            if self.charging:
                self.charging_time = min(self.charging_time + dt, 2)
            if self.elapsed_time >= 1 and self.difficulty_score <= self.score:
                self.difficulty_score += 100
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
                self.set_player_frames(Player(self.player_selected._dir , self.player_selected.dir_, Dir.Actions.ATTACK, dir_sprite).images, Player(self.player_selected._dir , self.player_selected.dir_, Dir.Actions.ATTACK, dir_sprite).animation_time)
                self.charging_time = 0
                self.play_sound_volume(ARROW_SOUDS[0])
        else:
            self.animation = True
            self.charging = True
            self.set_player_frames(Player(self.player_selected._dir , self.player_selected.dir_, Dir.Actions.ATTACK, dir_sprite).images, Player(self.player_selected._dir , self.player_selected.dir_, Dir.Actions.ATTACK, dir_sprite).animation_time)
            self.charging_time = 0
            self.play_sound_volume(ARROW_SOUDS[0])


    def exit(self):
        exit()

def actions(action):
    if action == STATE_EXIT:
        game.exit()
    elif action == STATE_MENU:
        game.back_to_menu()
    elif action == STATE_PLAYER_SELECT:
        game.status = STATE_PLAYER_SELECT
    elif action == STATE_CONTROLLS:
        game.status = STATE_CONTROLLS
    elif action == STATE_PLAYING:
        game.start_game()
    elif action == STATE_SETTINGS or action == STATE_PAUSED_CONFIG:
        game.call_settings()
    elif action == STATE_RESUME_GAME:
        game.resume_game()
    elif any(
    obj == action
    for obj in Dir_images.Characters.Player.__dict__.values()
    if isinstance(obj, type)  # Garante que é uma classe
    ):        
        game.player_selected = action

def on_mouse_down(pos, button):
    if button == mouse.LEFT:
        if game.status == STATE_PLAYING:
            game.atack_pressed()
        else:
            if game.status == STATE_SETTINGS or game.status == STATE_PAUSED_CONFIG:
                if game.opt.config_slide[0].is_hovered_indicator(pos):
                    game.opt.config_slide[0].dragging = True
                if game.opt.config_slide[1].is_hovered_indicator(pos):
                    game.opt.config_slide[1].dragging = True
                if game.opt.dropdown.is_hovered(pos) and not game.opt.dropdown.open:
                    game.opt.dropdown.open = True
                elif game.opt.dropdown.open:
                    selected_option = game.opt.dropdown.select_option(pos)
                    if selected_option:
                        game.change_resolution(selected_option)
            for button in game.opt.buttons:
                if any(button.selected for button in game.opt.buttons):
                    button.block = False
                if button.is_hovered(pos):
                    for buttons in game.opt.buttons:
                        buttons.selected = False                          
                    button.selected = not button.selected 
                    actions(button.action)



def on_mouse_up(pos, button):
    if button == mouse.LEFT:
        if game.status == STATE_SETTINGS or game.status == STATE_PAUSED_CONFIG:
            game.opt.config_slide[0].dragging = False
            game.opt.config_slide[1].dragging = False
        if game.status == STATE_PLAYING:
            if game.charging:
                game.atack_pressed()
            game.animation = False


def on_mouse_move(pos):
    global MOUSE_POS, MUSIC_VOL, EFFECT_VOL
    MOUSE_POS = pos
    if game.status == STATE_SETTINGS or game.status == STATE_PAUSED_CONFIG:
        if game.opt.config_slide[0].dragging:
            game.opt.config_slide[0].update_value(pos)
            MUSIC_VOL = game.opt.config_slide[0].value
            pgzero.music.set_volume(MUSIC_VOL)
        if game.opt.config_slide[1].dragging:
            game.opt.config_slide[1].update_value(pos)
            EFFECT_VOL = game.opt.config_slide[1].value
            sounds.shot.set_volume(EFFECT_VOL)


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
            box(WIDTH, HEIGHT, (0,0,0, 100)).draw(screen, (0,0))
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
    var1, var2 = 0, 0

    if game.status != STATE_PAUSED:
        screen.clear()
    if game.status == STATE_MENU:
        game.draw_menu()
    elif game.status == STATE_PLAYER_SELECT:
        game.draw_player_select()
    elif game.status == STATE_CONTROLLS:
        game.draw_controlls()
    elif game.status == STATE_SETTINGS or game.status == STATE_PAUSED_CONFIG:
        game.draw_settings()
        var1 = MUSIC_VOL * 100
        var2 = EFFECT_VOL * 100
    elif game.status == STATE_PAUSED:
        game.draw_pause()
    elif game.status == STATE_GAME_OVER:
        game.draw_game_over()
        var1, var2 = game.score, time_format(game.total_time)
    
    game.opt.draw(screen, MOUSE_POS, var1, var2)

    if game.status == STATE_PLAYING:
        game.mapa.draw()
        game.draw_player()
        game.draw_hud()
# Inicialização rápida do jogo
game = Game()
pgzrun.go()