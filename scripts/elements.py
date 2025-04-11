import scripts.auto as auto

class Button:
    def __init__(
        self,
        x,
        y,
        text,
        action,
        text_color,
        text_hover_color,
        text_size,
        bg_color="null",
        bgh_color="null",
        width=200,
        height=50,
        alpha = 255,
        dir= "center",
        b = 2,
        bc = (0,0,0,100),
        bch = (0,0,0,0),
        block = False
    ):
        self.x = x
        self.y = y
        self.dir = dir
        self.text = text
        self.text_screen = (0,0)
        self.text_size = text_size
        self.alpha = alpha/255
        self.text_color = auto.GradientBox._add_alpha(text_color, alpha)
        self.text_hover_color = auto.GradientBox._add_alpha(text_hover_color, alpha)
        self.action = action
        self.box_width = width
        self.box_height = height
        self.box_color = auto.GradientBox._add_alpha(bg_color, alpha)
        self.box_color_h = auto.GradientBox._add_alpha(bgh_color, alpha)
        self.border = b
        self.border_collor = auto.GradientBox._add_alpha(bc, alpha)
        self.border_collor_h = auto.GradientBox._add_alpha(bch, alpha)
        self.selected = False
        self.block = block
        self.box = any

    def draw(self, screen, mouse_pos, animate=False, speed=0):
        hover = self.is_hovered(mouse_pos)
        selected_or_hover = hover or self.selected
        def apply_transition(current, target):
            return auto.GradientBox.transition_color(current, target, speed) if animate or speed > 0 else target
        if self.box_color != "null":
            if not hasattr(self, "box") or not hasattr(self.box, "fill_color"):
                self.box = auto.Box(self.box_width, self.box_height, self.box_color, self.border_collor, self.border)
            if self.box_color_h != "null":
                self.box.fill_color = apply_transition(self.box.fill_color, self.box_color_h if selected_or_hover else self.box_color)
                self.box.border_color = apply_transition(self.box.border_color, self.border_collor_h if selected_or_hover else self.border_collor)
            else:
                self.box.fill_color = self.box_color
                self.box.border_color = self.border_collor

            self.box.draw(screen, (self.x, self.y))

        text_center = (self.x + self.box_width // 2, self.y + self.box_height // 2)
        text_color = (self.text_hover_color if hover else self.text_color)
        text_alpha = text_color[3]/255
        if len(self.text_screen) < 5 :
            self.text_screen = (
                self.text, text_center,
                self.text_size, text_alpha, text_color,
                self.dir
            )
        else:
            grad = apply_transition(self.text_screen[4], text_color)
            self.text_screen = (
                self.text,
                text_center,
                self.text_size,
                grad[3]/255 if len(grad) == 4 else 1,
                grad,
                self.dir,
            )
        screen.draw.text(
            self.text_screen[0],
            center = self.text_screen[1],
            fontsize= self.text_screen[2],
            alpha=self.text_screen[3],
            color= self.text_screen[4],
            align= self.text_screen[5]
        )

    def is_hovered(self, mouse_pos):
        if self.block == True:
            return False
        else:
            return (
                self.x <= mouse_pos[0] <= self.x + self.box_width
                and self.y <= mouse_pos[1] <= self.y + self.box_height
            )


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
        auto.Box(self.screen_width, self.screen_height, (100, 100, 100)).draw(screen, (self.x, self.y))

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
        return (
            distance_x <= self.indicator_radius and distance_y <= self.indicator_radius
        )

    def update_value(self, pos):
        if self.x <= pos[0] <= self.x + self.screen_width:
            self.value = (pos[0] - self.x) / self.screen_width
            self.value = max(0.0, min(1.0, self.value))


class Dropdown:
    def __init__(
        self,
        x,
        y,
        screen_width,
        options,
        selected_option,
        text_size,
        text_color,
        text_hover_color,
        height=50,
    ):
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.screen_height = height
        self.text_hover_color = text_hover_color
        self.text_color = text_color
        self.text_size = text_size
        self.y_open = y - (len(options) + 1) * self.screen_height
        self.options = options
        self.selected_option = selected_option
        self.open = False

    def draw(self, screen, pos):

        if self.open:
            for i, option in enumerate(self.options):
                auto.Box(self.screen_width, self.screen_height, (70, 70, 70)).draw(screen, (self.x, self.y_open + (i + 1) * self.screen_height))
                screen.draw.text(
                    option,
                    center=(
                        self.x + self.screen_width // 2,
                        self.y_open + (i + 1.5) * self.screen_height,
                    ),
                    fontsize=self.text_size,
                    color=(
                        self.text_hover_color
                        if self.is_hovered(pos, i + 1)
                        else self.text_color
                    ),
                )

        auto.Box(self.screen_width, self.screen_height, (70, 70, 70)).draw(screen, (self.x, self.y))
        screen.draw.text(
            self.options[self.selected_option],
            center=(self.x + self.screen_width // 2, self.y + self.screen_height // 2),
            fontsize=self.text_size,
            color=self.text_hover_color if self.is_hovered(pos) else self.text_color,
        )

    def is_hovered(self, pos, i=0):
        if self.open:
            if (
                self.x <= pos[0] <= self.x + self.screen_width
                and self.y_open + i * self.screen_height
                <= pos[1]
                <= self.y_open + (i + 1) * self.screen_height
            ):
                return True
        else:
            if (
                self.x <= pos[0] <= self.x + self.screen_width
                and self.y <= pos[1] <= self.y + self.screen_height
            ):
                return True

    def select_option(self, pos):
        if self.open:
            for i in range(len(self.options)):
                if (
                    self.x <= pos[0] <= self.x + self.screen_width
                    and self.y_open + (i + 1) * self.screen_height
                    <= pos[1]
                    <= self.y_open + (i + 2) * self.screen_height
                ):
                    self.selected_option = i
                    self.open = False
                    return self.options[i]
                else:
                    self.open = not self.open
        else:
            self.open = True


class Float_texts:
    def __init__(self, text , pos, font_size, color = "white", bcolor ="black", bsize = 2, draw_time = 2):
        self.text = text
        self.font_size = font_size
        self.color = color
        self.bcolor = bcolor
        self.bsize = bsize
        self.time = 0
        self.x = pos[0]
        self.y = pos[1]
        self.alpha = 1
        self.draw_time = draw_time

    def update(self, dt):
        self.time += dt
        self.y -= dt*10
        self.alpha = 1 if self.time < 1 else 2 - self.time
        
    
    def draw(self, screen, cam):
        if self.time < self.draw_time: 
            screen.draw.text(self.text,
                midbottom =(self.x + cam.x, self.y + cam.y),
                fontsize=self.font_size,
                color=self.color,
                ocolor=self.bcolor,
                owidth=self.bsize,
                alpha= self.alpha)
