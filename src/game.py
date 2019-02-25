# libraries
import pygame as pg

from src.config import Config


class Player(pg.sprite.Sprite):

    def __init__(self, sprite_sheet):
        super().__init__()
        self.sheet = pg.image.load(sprite_sheet).convert_alpha()
        self.sheet_cells = []  # Divisions of sprite sheet
        self.image = self.get_image(0)
        self.rect = self.image.get_rect()
        self.curr_pos = (0, 0)  # Stores current position of player
        self.grid = self.make_grid()  # List of coordinates player can move on screen

    @staticmethod
    def make_grid():
        tile_width = Config['game']['tile_width']
        x = Config['game']['width'] // tile_width
        y = Config['game']['height'] // tile_width
        grid = []
        w = tile_width // 2
        h = tile_width // 2
        for i in range(y):
            grid.append([])
            for j in range(x):
                grid[i].append((w, h))
                w += tile_width
            h += tile_width
            w = tile_width // 2
        return grid

    def set_pos(self, x, y):
        tile_width = Config['game']['tile_width']
        max_w = Config['game']['width'] // tile_width
        max_h = Config['game']['height'] // tile_width
        if x >= max_w or y >= max_h or x < 0 or y < 0:  # Does nothing if pos outside bounds
            return
        self.curr_pos = (x, y)
        self.rect.center = self.grid[y][x]

    def get_pos(self):
        return self.curr_pos

    def update(self):
        pass

    def move(self, direction):
        if direction == pg.K_w:
            self.image = self.get_image(0)
            self.set_pos(self.curr_pos[0], self.curr_pos[1] - 1)
        if direction == pg.K_s:
            self.image = self.get_image(1)
            self.set_pos(self.curr_pos[0], self.curr_pos[1] + 1)
        if direction == pg.K_d:
            self.image = self.get_image(2)
            self.set_pos(self.curr_pos[0] + 1, self.curr_pos[1])
        if direction == pg.K_a:
            self.image = pg.transform.flip(self.get_image(2), True, False)
            self.set_pos(self.curr_pos[0] - 1, self.curr_pos[1])

    def get_image(self, cell_index):  # Divides the sprite sheet and stores the divisions in self.cells
        if not self.sheet_cells:
            cols = 3
            rows = 1
            total_cells = cols * rows
            rect = self.sheet.get_rect()
            w = int(rect.width / cols)
            h = int(rect.height / rows)
            self.sheet_cells = list([(index % cols * w, int(index / cols) * h, w, h) for index in range(total_cells)])

        return self.sheet.subsurface(self.sheet_cells[cell_index])


class Game:
    def __init__(self):
        self.__running = True
        self.__size = Config['game']['width'], Config['game']['height']
        self.__display_surf = pg.display.set_mode(self.__size, pg.HWSURFACE | pg.DOUBLEBUF)
        self.sprite_group = pg.sprite.Group()
        self.char = Player(Config['resources']['sprites']['player'])  # Initializes player at (0, 0)
        self.sprite_group.add(self.char)

    def start(self):
        self.__game_loop()

    def __game_loop(self):
        while self.__running:
            self.__display_surf.fill((255, 255, 255))
            for event in pg.event.get():
                self.__on_event(event)

            self.sprite_group.update()  # Call the update() method on all the sprites in the group
            self.sprite_group.draw(self.__display_surf)  # Draw the sprites in the group
            pg.display.update()

    def __on_event(self, event):
        if event.type == pg.QUIT:
            self.__running = False
        if event.type == pg.KEYDOWN:
            self.char.move(event.key)
