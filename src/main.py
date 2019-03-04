# libraries
import pygame

# local files
import game

if __name__ == '__main__':
    # Setup
    pygame.init()

    # Start game loop
    game.Game().start()

    # Cleanup
    pygame.quit()

(lambda pg, g: (pg.init(), g.Game.start(), pygame.quit()))(__import__('pygame'))