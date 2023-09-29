import pygame
from gameconfig import *

# Tile sprite subclass
class Tile(pygame.sprite.Sprite):
    # constructor
    def __init__(self, pos, size):
        # call parent constructor
        super().__init__()
        # set image
        self.image = pygame.Surface((size, size))
        # fill image with grey
        self.image.fill('grey')
        # set rect
        self.rect = self.image.get_rect(topleft=pos)
        
    def update(self, x_shift):
        self.rect.x += x_shift       
