import math

import pygame

from settings import ALGAE_PLATFORM_COLOR, ALGAE_PLATFORM_DARK, TILE_SIZE


class AlgaePlatform(pygame.sprite.Sprite):
    def __init__(self, pos, travel_distance=70, speed=1.3):
        super().__init__()
        self.frames = self.build_frames()
        self.animation_index = 0.0
        self.animation_speed = 0.08
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(pos[0] - 10, pos[1] + TILE_SIZE // 4))
        self.anchor_x = float(self.rect.x)
        self.anchor_y = float(self.rect.y)
        self.travel_distance = travel_distance
        self.horizontal_sway = 24
        self.speed = speed * 0.035
        self.phase = (pos[0] % 180) / 180 * math.tau
        self.delta = pygame.math.Vector2(0, 0)

    def build_frames(self):
        return [self.build_surface(leaf_shift) for leaf_shift in (-2, 1, 3, 0)]

    def build_surface(self, leaf_shift):
        width = TILE_SIZE + 20
        height = TILE_SIZE // 2
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.ellipse(surface, ALGAE_PLATFORM_DARK, (8, 12, width - 16, height - 10))
        pygame.draw.ellipse(surface, ALGAE_PLATFORM_COLOR, (4, 8, width - 8, height - 16))

        for index in range(5):
            base_x = 10 + index * 14
            points = [
                (base_x, height - 8),
                (base_x - 3, 12 + (index % 2) * 2 + leaf_shift // 2),
                (base_x + 2, 4 + leaf_shift),
                (base_x + 6, 10 + (index % 3) - leaf_shift // 2),
                (base_x + 4, height - 8),
            ]
            pygame.draw.polygon(surface, ALGAE_PLATFORM_COLOR, points)

        pygame.draw.line(surface, (118, 184, 128), (16, 15), (width - 16, 15), 2)
        return surface.convert_alpha()

    def update(self, x_shift):
        previous_position = pygame.math.Vector2(self.rect.topleft)
        self.anchor_x += x_shift
        self.phase = (self.phase + self.speed) % math.tau
        current_topleft = (
            round(self.anchor_x + math.sin(self.phase) * self.horizontal_sway),
            round(self.anchor_y + math.sin(self.phase * 0.72) * self.travel_distance),
        )
        self.animation_index = (self.animation_index + self.animation_speed) % len(self.frames)
        self.image = self.frames[int(self.animation_index)]
        self.rect = self.image.get_rect(topleft=current_topleft)
        self.delta.update(self.rect.x - previous_position[0], self.rect.y - previous_position[1])
