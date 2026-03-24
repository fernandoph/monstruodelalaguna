import pygame

from settings import EXIT_LOCKED_COLOR, EXIT_OPEN_COLOR, TILE_SIZE


class LevelExit(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.locked_image = self.build_surface(EXIT_LOCKED_COLOR)
        self.open_image = self.build_surface(EXIT_OPEN_COLOR)
        self.image = self.locked_image
        self.rect = self.image.get_rect(bottomleft=(pos[0], pos[1] + TILE_SIZE))
        self.is_open = False

    def build_surface(self, fill_color):
        surface = pygame.Surface((TILE_SIZE, TILE_SIZE * 2), pygame.SRCALPHA)
        pygame.draw.rect(surface, fill_color, (18, 6, 28, TILE_SIZE * 2 - 12), border_radius=8)
        pygame.draw.rect(surface, (225, 240, 245), (24, 14, 16, 20), border_radius=6)
        pygame.draw.rect(surface, (12, 22, 34), (8, TILE_SIZE * 2 - 18, TILE_SIZE - 16, 10), border_radius=5)
        return surface

    def set_open(self, is_open):
        self.is_open = is_open
        self.image = self.open_image if is_open else self.locked_image

    def update(self, x_shift):
        self.rect.x += x_shift
