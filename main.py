# libraries
import pygame

# local files
from src import game

if __name__ == '__main__':
    # Setup
    pygame.init()

    # Start game loop
    game.Game().start()

    # Cleanup
    pygame.quit()
