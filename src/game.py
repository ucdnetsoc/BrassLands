# libraries
import pygame

from src.config import Config


class Game:
    def __init__(self):
        self.__running = True
        self.__size = Config['game']['width'], Config['game']['height']
        self.__display_surf = pygame.display.set_mode(self.__size, pygame.HWSURFACE | pygame.DOUBLEBUF)

    def start(self):
        self.game_loop()

    def game_loop(self):
        while self.__running:
            for event in pygame.event.get():
                self.on_event(event)

            # TODO Render a frame

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.__running = False



