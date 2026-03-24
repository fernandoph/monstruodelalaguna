import pygame

from settings import TILE_SIZE, WATER_ANT_COLOR, WATER_ANT_SHELL_COLOR


class WaterAnt(pygame.sprite.Sprite):
    def __init__(self, pos, patrol_distance=72, speed=1.2):
        super().__init__()
        self.frames = self.build_frames()
        self.animation_index = 0.0
        self.animation_speed = 0.18
        self.image = self.frames[0]
        self.rect = self.image.get_rect(bottomleft=(pos[0], pos[1] + TILE_SIZE))
        self.origin_x = self.rect.x
        self.patrol_distance = patrol_distance
        self.speed = speed
        self.direction = 1

    def build_frames(self):
        return [self.build_frame(leg_offset) for leg_offset in (-3, 0, 3, 0)]

    def build_frame(self, leg_offset):
        surface = pygame.Surface((TILE_SIZE - 16, TILE_SIZE - 18), pygame.SRCALPHA)
        body_rect = pygame.Rect(8, 18, 22, 14)
        shell_rect = pygame.Rect(18, 10, 24, 22)
        head_rect = pygame.Rect(2, 14, 16, 14)

        pygame.draw.ellipse(surface, WATER_ANT_SHELL_COLOR, shell_rect)
        pygame.draw.ellipse(surface, WATER_ANT_COLOR, body_rect)
        pygame.draw.ellipse(surface, WATER_ANT_COLOR, head_rect)

        for index in range(3):
            base_y = 22 + index * 5
            pygame.draw.line(surface, WATER_ANT_COLOR, (18, base_y), (8, base_y + leg_offset), 2)
            pygame.draw.line(surface, WATER_ANT_COLOR, (30, base_y), (42, base_y - leg_offset), 2)

        pygame.draw.line(surface, WATER_ANT_COLOR, (8, 16), (2, 8), 2)
        pygame.draw.line(surface, WATER_ANT_COLOR, (12, 16), (12, 6), 2)
        pygame.draw.circle(surface, (24, 24, 24), (8, 20), 2)
        return surface.convert_alpha()

    def update(self, x_shift):
        self.origin_x += x_shift
        self.rect.x += x_shift + (self.speed * self.direction)

        if self.rect.x <= self.origin_x - self.patrol_distance:
            self.rect.x = self.origin_x - self.patrol_distance
            self.direction = 1
        elif self.rect.x >= self.origin_x + self.patrol_distance:
            self.rect.x = self.origin_x + self.patrol_distance
            self.direction = -1

        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.frames):
            self.animation_index = 0

        frame = self.frames[int(self.animation_index)]
        self.image = pygame.transform.flip(frame, self.direction < 0, False)
