# libraries
import pygame

from src.config import Config


class Player(pygame.sprite.Sprite):

    def __init__(self, initial_pos, sprite_sheet):
        super().__init__()
        self.sheet = pygame.image.load(sprite_sheet).convert_alpha()
        self.sheet_cells = []  # Divisions of sprite sheet
        self.image = self.get_image(0)
        self.rect = self.image.get_rect()
        self.rect.center = initial_pos

    def get_pos(self):
        return self.rect.center

    def update(self):
        pass

    def move(self, direction):
        if direction == pygame.K_w:
            self.image = self.get_image(0)
            self.rect.top -= self.rect.height
        if direction == pygame.K_s:
            self.image = self.get_image(1)
            self.rect.top += self.rect.height
        if direction == pygame.K_d:
            self.image = self.get_image(2)
            self.rect.left += self.rect.width
        if direction == pygame.K_a:
            self.image = pygame.transform.flip(self.get_image(2), True, False)
            self.rect.left -= self.rect.width

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
        self.__display_surf = pygame.display.set_mode(self.__size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.sprite_group = pygame.sprite.Group()
        self.char = Player((400, 300), Config['resources']['sprites']['player'])  # Starting position of the player
        self.sprite_group.add(self.char)

    def start(self):
        self.__game_loop()

    def __game_loop(self):
        while self.__running:
            self.__display_surf.fill((255, 255, 255))
            for event in pygame.event.get():
                self.__on_event(event)
            self.sprite_group.update()  # Call the update() method on all the sprites in the group
            self.sprite_group.draw(self.__display_surf)  # Draw the sprites in the group
            pygame.display.update()

    def __on_event(self, event):
        if event.type == pygame.QUIT:
            self.__running = False
        if event.type == pygame.KEYDOWN:
            self.char.move(event.key)
