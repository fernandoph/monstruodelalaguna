import pygame

from settings import ALGAE_PLATFORM_COLOR, ALGAE_PLATFORM_DARK, TILE_SIZE


class AlgaePlatform(pygame.sprite.Sprite):
    def __init__(self, pos, travel_distance=70, speed=1.3):
        super().__init__()
        self.image = self.build_surface()
        self.rect = self.image.get_rect(topleft=(pos[0], pos[1] + TILE_SIZE // 4))
        self.anchor_y = self.rect.y
        self.travel_distance = travel_distance
        self.speed = speed
        self.direction = 1
        self.delta = pygame.math.Vector2(0, 0)

    def build_surface(self):
        width = TILE_SIZE + 20
        height = TILE_SIZE // 2
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.ellipse(surface, ALGAE_PLATFORM_DARK, (8, 12, width - 16, height - 10))
        pygame.draw.ellipse(surface, ALGAE_PLATFORM_COLOR, (4, 8, width - 8, height - 16))

        for index in range(5):
            base_x = 10 + index * 14
            points = [
                (base_x, height - 8),
                (base_x - 3, 12 + (index % 2) * 2),
                (base_x + 2, 4),
                (base_x + 6, 10 + (index % 3)),
                (base_x + 4, height - 8),
            ]
            pygame.draw.polygon(surface, ALGAE_PLATFORM_COLOR, points)

        return surface.convert_alpha()

    def update(self, x_shift):
        previous_position = self.rect.topleft
        self.rect.x += x_shift
        self.rect.y += self.direction * self.speed

        if abs(self.rect.y - self.anchor_y) >= self.travel_distance:
            self.rect.y = self.anchor_y + (self.travel_distance * self.direction)
            self.direction *= -1

        self.delta.update(self.rect.x - previous_position[0], self.rect.y - previous_position[1])
