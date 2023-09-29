# Version: 0.1
# author: Fernando P. Hauscarriaga
# date: 2023-09-29

# imports
import pygame, sys
from tiles import Tile
from level import Level

# Game config
from gameconfig import *

# Main function
def main():
    # pygame init
    pygame.init()

    # screen
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption(screen_caption)
    clock = pygame.time.Clock()

    # tile group
    level = Level(level_map, screen)

    # game loop
    running = True
    while running:
        # event loop
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                running = False

        # fill screen
        screen.fill('black')
        level.run()
                
        # screen update
        pygame.display.update()

        # tick
        clock.tick(fps)

    # pygame quit
    pygame.quit()
    sys.exit()
    
# call main
if __name__ == "__main__":
    main()
