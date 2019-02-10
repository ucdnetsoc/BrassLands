# libraries
import pygame

# local files
from src import game

if __name__ == '__main__':
    # Setup
    game = game.Game()
    pygame.init()

    # Start game loop
    game.game_loop()

    # Cleanup
    pygame.quit()
