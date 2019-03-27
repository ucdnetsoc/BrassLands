# libraries
import pygame as pg
import json

from config import Config


class Hover:
    def __init__(self, name, description, icon=Config['resources']['ui']['icons']['default']):
        font = pg.font.Font("/home/david/Documents/BrassLands/src/res/font.ttf", 30)
        self.icon = pg.image.load(icon)
        self.surf = pg.image.load("/home/david/Documents/BrassLands/src/res/hover.png")
        self.rect = self.surf.get_rect()

        name = "<Item Name>" if name is None else name
        description = "<Item Description>" if description is None else description

        self.name_surf = font.render(name, True, (235, 235, 235))
        self.desc_surf = font.render(description, True, (235, 235, 235))

        self.surf.blit(self.icon, (13, 13))
        self.surf.blit(self.name_surf, (65, 15))
        self.surf.blit(self.desc_surf, (13, 55))

    def show_tooltip(self, surface, pos):
        self.rect.bottomright = pos
        surface.blit(self.surf, self.rect)


class Item(Hover):
    def __init__(self, j_string):
        self.name, self.description = None, None
        obj = json.loads(j_string)
        self.parse_json(obj)
        super().__init__(self.name, self.description)

    def parse_json(self, obj):
        try:
            self.name = obj['name']
            self.description = obj['description']
        except KeyError as e:
            print(f"Incorrect json format, unknown attribute: \"{e.args[0]}\"")


class Inventory:
    def __init__(self):
        w, h = 7, 3
        self.visible = False
        self.surface = pg.image.load(Config['resources']['ui']['inventory'])
        self.rect = self.surface.get_rect()
        self.rect.bottomright = (Config['game']['width'], Config['game']['height'])
        x, y = 20, 0
        self.inv_rects = [pg.Rect((x + i * 42, y + 290 + j * 42), (40, 40)) for j in range(h) for i in range(w)]

        self.items = [None for _ in range(21)]
        
    # noinspection PyTypeChecker
    def add(self, item):
        if isinstance(item, Item):
            for i, e in enumerate(self.items):
                if e is None:
                    self.items[i] = item
                    self.update()
                    return True
        return False

    def remove(self, item):
        self.items.remove(item)
        self.update()

    def event_handler(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_i:
                self.visible = not self.visible

    def update(self):
        self.surface = pg.image.load(Config['resources']['ui']['inventory'])
        for i, item in enumerate(self.items):
            if item is not None:
                self.surface.blit(item.icon, self.inv_rects[i])

    def draw(self, surface):
        if self.visible:
            surface.blit(self.surface, self.rect)
            mouse_pos = pg.mouse.get_pos()
            rel_pos = (mouse_pos[0] - self.rect.topleft[0], mouse_pos[1] - self.rect.topleft[1])
            for i, rect in enumerate(self.inv_rects):
                if rect.collidepoint(rel_pos):
                    if self.items[i] is not None:
                        self.items[i].show_tooltip(surface, mouse_pos)

        # x = 0
        # for rect in self.inv_rects:
        #     pg.draw.rect(self.surface, (255 - x, 255 - x / 2, 255 - x - 5), rect)
        #     x += 10


class Ground(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pg.image.load(Config['resources']['sprites']['ground'])
        self.rect = self.image.get_rect()
        self.rect.center = pos


class Wall(Ground):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = pg.image.load(Config['resources']['sprites']['wall'])


class Player(pg.sprite.Sprite):

    def __init__(self, sprite_sheet, grid):
        super().__init__()
        self.sheet = pg.image.load(sprite_sheet).convert_alpha()
        self.sheet_cells = []  # Divisions of sprite sheet
        self.image = self.get_image(1)
        self.rect = self.image.get_rect()
        self.curr_pos = (0, 0)  # Stores current position of player
        self.grid = grid  # List of coordinates player can move on screen

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

    def move(self, direction, scenery):
        d = (0, 0)
        if direction == pg.K_w:
            self.image = self.get_image(0)
            d = (0, -1)
        if direction == pg.K_s:
            self.image = self.get_image(1)
            d = (0, 1)
        if direction == pg.K_d:
            self.image = self.get_image(2)
            d = (1, 0)
        if direction == pg.K_a:
            d = (-1, 0)
            self.image = pg.transform.flip(self.get_image(2), True, False)

        x, y = self.curr_pos[0] + d[0], self.curr_pos[1] + d[1]
        if not scenery or not isinstance(scenery[y][x], Wall):  # Will only move if destination isn't a wall
            self.set_pos(x, y)

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


# Makes list of coordinates
def make_grid():
    tile_width = Config['game']['tile_width']
    x = Config['game']['width'] // tile_width
    y = Config['game']['height'] // tile_width
    w = tile_width // 2
    return [[(w + tile_width * j, w + tile_width * i) for j in range(x)] for i in range(y)]


# Draws sprites from a file into a sprite group
# Returns list with the location of all scenery objects
def make_level(sprite_grp, grid, level):
    lst = []
    sprite_grp.empty()  # Empties the grp to remove previous level's sprites
    try:
        level_file = open(level, "r")
    except FileNotFoundError:
        print("File not found")
        return []
    lines = level_file.readlines()
    for i, line in enumerate(lines):
        lst.append([])
        for j, char in enumerate(line):
            try:
                if char == Config['game']['ground_char']:
                    lst[i].append(Ground(grid[i][j]))
                elif char == Config['game']['wall_char']:
                    lst[i].append(Wall(grid[i][j]))
            except IndexError:
                print("Map is not 25x20")
                sprite_grp.add(lst)
                return lst

    sprite_grp.add(lst)
    return lst


class Game:
    def __init__(self):
        self.__running = True
        self.__size = Config['game']['width'], Config['game']['height']
        self.__display_surf = pg.display.set_mode(self.__size, pg.HWSURFACE | pg.DOUBLEBUF)

        self.player_grp = pg.sprite.Group()
        self.scenery_grp = pg.sprite.Group()  # Group for walls, ground, etc.

        self.coord_grid = make_grid()
        self.scenery_grid = make_level(self.scenery_grp, self.coord_grid, Config['resources']['levels']['level1'])
        print(Config['resources']['sprites']['player'])
        self.char = Player(Config['resources']['sprites']['player'], self.coord_grid)  # Initializes player at (0, 0)
        self.player_grp.add(self.char)

        self.inventory = Inventory()

    def start(self):
        self.__game_loop()

    def __game_loop(self):
        while self.__running:
            self.__display_surf.fill((255, 255, 255))
            for event in pg.event.get():
                self.__on_event(event)
            self.scenery_grp.draw(self.__display_surf)
            self.player_grp.update()  # Call the update() method on all the sprites in the group
            self.player_grp.draw(self.__display_surf)  # Draw the sprites in the group
            self.inventory.draw(self.__display_surf)
            pg.display.update()

    def __on_event(self, event):
        if event.type == pg.QUIT:
            self.__running = False
        self.inventory.event_handler(event)
        if event.type == pg.KEYDOWN:
            self.char.move(event.key, self.scenery_grid)
