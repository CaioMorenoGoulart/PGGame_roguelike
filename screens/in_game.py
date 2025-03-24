# from style import *
# from config import WIDTH, HEIGHT, STATE_PLAYING, STATE_SETTINGS, STATE_EXIT

# class Menu_screen:
#     def __init__(self):
#         self.id = "Menu"
#         self.texts = {
#             "Texts": [
#                 {
#                     "Text": "Jogar",
#                     "Font_size": FONT_SIZE_MENU,
#                     "Color": FONT_COLOR_MENU,
#                     "Color_Hover": FONT_COLOR_HOVER,
#                     "Border": FONT_BORDER_MENU,
#                     "Border_Color": FONT_COLOR_BORDER_MENU,
#                     "Border_Color_HOVER": FONT_COLOR_BORDER_HOVER,
#                     "BG_Color": BG_TEXT_COLOR,
#                     "Pos": (WIDTH // 2 - 100, HEIGHT // 2 - 50),
#                     "Action": STATE_PLAYING,
#                 },
#                 {
#                     "Text": "Configurações",
#                     "Font_size": FONT_SIZE_MENU,
#                     "Color": FONT_COLOR_MENU,
#                     "Color_Hover": FONT_COLOR_HOVER,
#                     "Border": FONT_BORDER_MENU,
#                     "Border_Color": FONT_COLOR_BORDER_MENU,
#                     "Border_Color_HOVER": FONT_COLOR_BORDER_HOVER,
#                     "BG_Color": BG_TEXT_COLOR,
#                     "Pos": (WIDTH // 2 - 100, HEIGHT // 2 + 20),
#                     "Action": STATE_SETTINGS,
#                 },
#                 {
#                     "Text": "Sair",
#                     "Font_size": FONT_SIZE_MENU,
#                     "Color": FONT_COLOR_MENU,
#                     "Color_Hover": FONT_COLOR_HOVER,
#                     "Border": FONT_BORDER_MENU,
#                     "Border_Color": FONT_COLOR_BORDER_MENU,
#                     "Border_Color_HOVER": FONT_COLOR_BORDER_HOVER,
#                     "BG_Color": BG_TEXT_COLOR,
#                     "Pos": (WIDTH // 2 - 100, HEIGHT // 2 + 90),
#                     "Action": STATE_EXIT,
#                 },
#             ],
#         }
#         import auto
#         self.buttons = auto.listing(self.texts)

#     def draw(self, screen, pos):
#         screen.draw.text(
#             f"Exp: {(self.score % 100):.0f}%",
#             topright = (WIDTH*.1 - 2, 2),
#             fontsize=FONT_SIZE_ITENS,
#             color="white",
#             ocolor="black",
#             owidth=1
#         )
#         screen.draw.text(
#             f"Nivel {int(self.score / 100)}",
#             centerx = WIDTH/2,
#             bottom = CELL_SIZE,
#             fontsize=FONT_SIZE_TEXTS,
#             color="white",
#             ocolor="black",
#             owidth=1
#         )
#         back_exp_box = box(WIDTH*.8, 5, (0, 0, 0, 100), (0,0,0),1)
#         back_exp_box.draw(screen, (WIDTH*.1, 5))

#         exp_box = any
#         if self.score != 0:
#             exp_box = box(((back_exp_box.rect.width/100) * (self.score % 100)) - 2, 3, (0, 0, 255,150), (0,0,0))

#             if self.score % 100 == 0:
#                 exp_box = box(back_exp_box.rect.width - 2, 3, (0, 0, 255, 150), (0,0,0))

#             exp_box.draw(screen, (WIDTH*.1 + 1, 6))

            

        
#         screen.draw.text(
#             f"Tempo de jogo: {time_format(self.total_time)}",
#             right = WIDTH - 5,
#             bottom = CELL_SIZE,
#             fontsize=FONT_SIZE_TEXTS,
#             color="white",
#             ocolor="black",
#             owidth=1
#         )
#         screen.draw.text(
#             f"Vida: {self.player_health:.0f}",
#             (10, HEIGHT - 50),
#             fontsize=FONT_SIZE_TEXTS,
#             color="white",
#             ocolor="black",
#             owidth=1
#         )
#         for pw in self.text_pw_list:
#             pw.draw(screen)
#             if pw.time >= 2: 
#                 self.text_pw_list.remove(pw)

#         screen.draw.filled_rect(
#             Rect(9, HEIGHT - 31, 202 if self.player_health * 2 < 202 else self.player_health * 2 + 2, 22),
#             (0, 0, 0),
#         )
#         screen.draw.filled_rect(
#             Rect(10, HEIGHT - 30, min(100 ,self.player_health) * 2, 20),
#             HEALTH_COLOR,
#         )
#         screen.draw.filled_rect(
#             Rect(210, HEIGHT - 30, (self.player_health - 100) * 2, 20),
#             [0,0,255],
#         )

#         x = (self.player.tile.x - CELL_SIZE/2)
#         y = (self.player.tile.y + CELL_SIZE/2) + 3

#         screen.draw.filled_rect(
#             Rect(x-1, y-1, 32, 8),
#             (0, 0, 0),
#         )
        
#         img_skill_cooldown = Actor(self.player_selected.Walking.Side.images[2], (250, HEIGHT - 40),(0,0))
#         img_skill_cooldown_2 = Actor(self.player_selected.Walking.Side.images[0], (img_skill_cooldown.x + img_skill_cooldown.height - 10, img_skill_cooldown.y),(0,0))

#         img_arrow_cooldown = Actor(Set_images(string= Dir_images.Weapons.dir + "arrow_", n_frames= 1).images[0], (240, HEIGHT - 35),(0,0))
#         img_arrow_cooldown.angle = -45
#         img_arrow_cooldown.scale = 1.75

#         img_skill_cooldown._surf.set_alpha(min( 255, self.player_skill_timer * 128))
#         img_skill_cooldown_2._surf.set_alpha(min( 255, self.player_skill_timer * 128))

#         if len(self.projectiles) > 0:
#             shoot = self.projectiles[len(self.projectiles) - 1]
#             shoot_fill = shoot.shoot_spawn_cooldown/self.shoot_cooldown
#             img_arrow_cooldown._surf.set_alpha(min( 255, shoot_fill * 255))
#             screen.draw.filled_rect(
#                 Rect(x, y,  min(1, shoot_fill) * 30, 6),
#                 HEALTH_COLOR,
#             )
#         else:
#             img_arrow_cooldown._surf.set_alpha(255)
#             Actor(Set_images(string= Dir_images.Weapons.dir + "arrow_", n_frames= 1).images[0], (0,0),(0,0))
#             screen.draw.filled_rect(
#                 Rect(x, y,  30 , 6),
#                 HEALTH_COLOR,
#             )
#         if self.tab:
#             box(WIDTH/4, HEIGHT/4, (0,0,0, 128)).draw(screen, (CELL_SIZE,CELL_SIZE))
#             screen.draw.text(f"Velocidade de ataque: {self.shoot_cooldown}",
#                     (CELL_SIZE * 2 , CELL_SIZE * 2),
#                     fontsize=FONT_SIZE_ITENS,
#                     color="white",
#                     ocolor="black",
#                     owidth=2,
#                     alpha= 100)
#             screen.draw.text(f"Velocidade de movimento: {self.speed_moviment}",
#                     (CELL_SIZE * 2 , CELL_SIZE * 3),
#                     fontsize=FONT_SIZE_ITENS,
#                     color="white",
#                     ocolor="black",
#                     owidth=2,
#                     alpha= 100)

#         if game.draw_hitbox:
#             box(game.player.hitbox.width, game.player.hitbox.height, (0, 0, 0, 0), (255, 0, 0, 255), 1).draw(screen, (game.player.hitbox.x, game.player.hitbox.y))
#             for enemy in game.enemies:
#                 box(enemy.hitbox.width, enemy.hitbox.height, (0, 0, 0, 0), (0, 255, 0, 255), 1).draw(screen, (enemy.hitbox.x, enemy.hitbox.y))
#             for projectil in game.projectiles:
#                 box(projectil.hitbox.width, projectil.hitbox.height, (0, 0, 0, 0), (0, 0, 255, 255), 1).draw(screen, (projectil.hitbox.x, projectil.hitbox.y))
#             for pw in game.pw:
#                 box(pw.hitbox.width, pw.hitbox.height, (0, 0, 0, 0), (255, 255, 0, 255), 1).draw(screen, (pw.hitbox.x, pw.hitbox.y))

#         img_arrow_cooldown.draw()
#         img_skill_cooldown.draw()
#         img_skill_cooldown_2.draw()

# menu = Menu_screen()