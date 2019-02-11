# libraries
import pygame

from src.config import Config


class Game:
    def __init__(self):
        self.__running = True
        self.__size = Config['game']['width'], Config['game']['height']
        self.__display_surf = pygame.display.set_mode(self.__size, pygame.HWSURFACE | pygame.DOUBLEBUF)

    def start(self):
        self.__game_loop()

    def __game_loop(self):
        while self.__running:
            for event in pygame.event.get():
                self.__on_event(event)

            # TODO Render a frame

    def __on_event(self, event):
        if event.type == pygame.QUIT:
            self.__running = False



