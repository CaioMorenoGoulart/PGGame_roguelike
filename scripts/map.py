from scripts.config import CELL_SIZE, ROWS, COLUMNS, SCAL, Actor, random
from scripts.image_dir import Set_images, Dir_images

Map_heigth = (ROWS*2,COLUMNS*2)

# Criação do Mapa
class Map:
    def __init__(self):
        self.MAP = []
        # self.world_pos = (0,0)
        for row in range(Map_heigth[0]):
            if row == 0 or row == Map_heigth[0] - 1:
                self.MAP.append([1] * Map_heigth[1])
            else:
                self.MAP.append([1] + [random.choices([0, 1], weights=[0.99, 0.01])[0] for _ in range(Map_heigth[1] - 2)] + [1])
    # Randomizar grama

    # def update_world_pos(self, x, y):
    #     self.world_pos = [self.world_pos[0] + x, self.world_pos[1] + y]

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

    def pos_in_map(self, tile, desloc_x = 0, desloc_y = 0):
        start_x = int((tile.x - tile.width / 2 + desloc_x) // CELL_SIZE)
        start_y = int((tile.y - tile.height / 2 + desloc_y) // CELL_SIZE)
        end_x = int((tile.x + tile.width / 2 + desloc_x) // CELL_SIZE)
        end_y = int((tile.y + tile.height / 2 + desloc_y) // CELL_SIZE)
        for y in range(start_y, end_y + 1):
            for x in range(start_x, end_x + 1):
                if self.MAP[y][x] == 1:
                    return False
        return True

    def draw(self, cam):
        for tile in self.map_tiles:
            original_pos = tile.pos
            tile.pos = (tile.x - cam.x, tile.y - cam.y)
            tile.draw()            
            tile.pos = original_pos 