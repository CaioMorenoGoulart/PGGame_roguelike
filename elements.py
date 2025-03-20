import auto

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
        width=200,
        height=50,
        alpha = 1,
    ):
        self.x = x
        self.y = y
        self.text = text
        self.text_size = text_size
        self.text_color = text_color
        self.alpha = alpha
        self.text_hover_color = text_hover_color
        self.action = action
        self.box_width = width
        self.box_height = height
        self.box_color = bg_color

    def draw(self, screen, mouse_pos):
        if self.box_color != "null":
            auto.draw_alpha_box(self.box_width, self.box_height,  self.box_color, screen, (self.x, self.y))

        screen.draw.text(
            self.text,
            center=(self.x + self.box_width // 2, self.y + self.box_height // 2),
            fontsize=self.text_size,
            alpha=self.alpha,
            color=(
                self.text_hover_color if self.is_hovered(mouse_pos) else self.text_color
            ),
        )

    def is_hovered(self, mouse_pos):
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
        auto.draw_alpha_box(self.screen_width, self.screen_height, alpha_color= (100, 100, 100), screen= screen, pos= (self.x, self.y))
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
                auto.draw_alpha_box(self.screen_width, self.screen_height, alpha_color= (70, 70, 70), screen= screen, pos= (self.x, self.y_open + (i + 1) * self.screen_height))
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
        auto.draw_alpha_box(self.screen_width, self.screen_height, alpha_color= (50, 50, 50), screen= screen, pos= (self.x, self.y))
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
        
    
    def draw(self, screen):
        if self.time < self.draw_time: 
            screen.draw.text(self.text,
                midbottom =(self.x, self.y),
                fontsize=self.font_size,
                color=self.color,
                ocolor=self.bcolor,
                owidth=self.bsize,
                alpha= self.alpha)
