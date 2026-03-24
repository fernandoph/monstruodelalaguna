import pygame

from settings import FISH_COLOR, TILE_SIZE


class Fish(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = self.build_surface()
        self.rect = self.image.get_rect(center=(pos[0] + TILE_SIZE // 2, pos[1] + TILE_SIZE // 2))

    def build_surface(self):
        surface = pygame.Surface((TILE_SIZE // 2, TILE_SIZE // 3), pygame.SRCALPHA)
        pygame.draw.ellipse(surface, FISH_COLOR, surface.get_rect())
        pygame.draw.polygon(
            surface,
            FISH_COLOR,
            [
                (surface.get_width() - 2, surface.get_height() // 2),
                (surface.get_width() + 10, 4),
                (surface.get_width() + 10, surface.get_height() - 4),
            ],
        )
        return surface

    def update(self, x_shift):
        self.rect.x += x_shift
