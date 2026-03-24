import pygame

from settings import OCTOPUS_ACCENT_COLOR, OCTOPUS_COLOR, TILE_SIZE


class Octopus(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.frames = self.build_frames()
        self.animation_index = 0.0
        self.animation_speed = 0.15
        self.image = self.frames[0]
        self.rect = self.image.get_rect(midtop=(pos[0] + TILE_SIZE // 2, pos[1] - 6))
        self.threat_progress = 0

    def build_frames(self):
        return [self.build_frame(tentacle_offset) for tentacle_offset in (-4, 0, 4, 0)]

    def build_frame(self, tentacle_offset):
        surface = pygame.Surface((TILE_SIZE, TILE_SIZE + 18), pygame.SRCALPHA)
        head_rect = pygame.Rect(12, 8, 40, 34)
        pygame.draw.ellipse(surface, OCTOPUS_COLOR, head_rect)
        pygame.draw.ellipse(surface, OCTOPUS_ACCENT_COLOR, (18, 14, 28, 10))

        for index in range(4):
            x = 16 + index * 10
            points = [
                (x, 36),
                (x - 4, 50 + (index % 2) * 3),
                (x + tentacle_offset // 2, 58 + tentacle_offset),
                (x + 4, 46),
            ]
            pygame.draw.lines(surface, OCTOPUS_COLOR, False, points, 4)

        pygame.draw.circle(surface, (255, 255, 255), (24, 24), 4)
        pygame.draw.circle(surface, (255, 255, 255), (40, 24), 4)
        pygame.draw.circle(surface, (20, 20, 22), (24, 24), 2)
        pygame.draw.circle(surface, (20, 20, 22), (40, 24), 2)
        return surface.convert_alpha()

    @property
    def threat_rect(self):
        return self.rect.inflate(56, 18)

    def update(self, x_shift):
        self.rect.x += x_shift
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        current_midtop = self.rect.midtop
        self.image = self.frames[int(self.animation_index)]
        self.rect = self.image.get_rect(midtop=current_midtop)

    def update_threat(self, player):
        player_rect = player.hitbox
        if self.threat_rect.colliderect(player_rect):
            self.threat_progress += 0.5 if player.direction.x != 0 else 1
        else:
            self.threat_progress = max(0, self.threat_progress - 1)

        return self.threat_progress >= 12
