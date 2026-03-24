import math

import pygame

from settings import (
    OCTOPUS_ACCENT_COLOR,
    OCTOPUS_COLOR,
    OCTOPUS_THREAT_COLOR,
    OCTOPUS_WARNING_COLOR,
    TILE_SIZE,
)


class Octopus(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.frames = self.build_frames()
        self.animation_index = 0.0
        self.animation_speed = 0.15
        self.image = self.frames[0]
        self.rect = self.image.get_rect(midtop=(pos[0] + TILE_SIZE // 2, pos[1] - 6))
        self.anchor_centerx = float(self.rect.centerx)
        self.anchor_y = float(self.rect.y)
        self.float_phase = (pos[0] % 110) / 110 * math.tau
        self.threat_progress = 0.0
        self.threat_limit = 14.0
        self.capture_timer = 0
        self.warning_pulse = 0.0

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
        return self.rect.inflate(124, 52)

    @property
    def threat_ratio(self):
        return max(0.0, min(1.0, self.threat_progress / self.threat_limit))

    def update(self, x_shift):
        self.anchor_centerx += x_shift
        self.float_phase = (self.float_phase + 0.08) % math.tau
        self.warning_pulse = (self.warning_pulse + 0.16) % math.tau
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        current_midtop = (
            round(self.anchor_centerx),
            round(self.anchor_y + math.sin(self.float_phase) * 4),
        )
        self.image = self.frames[int(self.animation_index)]
        self.rect = self.image.get_rect(midtop=current_midtop)

    def update_threat(self, player):
        player_rect = player.hitbox
        if self.threat_rect.colliderect(player_rect):
            increase = 0.45 if player.direction.x != 0 else 0.9
            self.threat_progress = min(self.threat_limit, self.threat_progress + increase)
        else:
            self.threat_progress = max(0, self.threat_progress - 1.2)

        if self.threat_ratio >= 0.75 and self.threat_rect.colliderect(player_rect):
            self.capture_timer = min(10, self.capture_timer + 1)
        else:
            self.capture_timer = max(0, self.capture_timer - 2)

        return self.threat_progress >= self.threat_limit or self.capture_timer >= 10

    def draw_threat(self, surface):
        if self.threat_progress <= 0:
            return

        threat_rect = self.threat_rect
        ratio = self.threat_ratio
        pulse = math.sin(self.warning_pulse)
        aura = pygame.Surface(threat_rect.size, pygame.SRCALPHA)
        fill_alpha = 24 + int(34 * ratio)
        outline_alpha = 42 + int(70 * ratio)
        fill_color = (*OCTOPUS_THREAT_COLOR[:3], fill_alpha)
        outline_color = (*OCTOPUS_WARNING_COLOR, outline_alpha)
        pygame.draw.ellipse(aura, fill_color, aura.get_rect())
        pygame.draw.ellipse(aura, outline_color, aura.get_rect(), width=3)
        surface.blit(aura, threat_rect.topleft)

        line_surface = pygame.Surface((threat_rect.width, threat_rect.height), pygame.SRCALPHA)
        extension = 8 + int(16 * ratio) + int(pulse * 3)
        for index in range(3):
            base_x = threat_rect.width // 2 - 18 + index * 18
            points = [
                (base_x, 18),
                (base_x - 8, 28 + index * 4),
                (base_x + extension // 2, 46 + extension),
                (base_x + 12, 30),
            ]
            pygame.draw.lines(line_surface, outline_color, False, points, 3)
        surface.blit(line_surface, threat_rect.topleft)

        bar_rect = pygame.Rect(self.rect.left - 6, self.rect.top - 16, self.rect.width + 12, 8)
        pygame.draw.rect(surface, (42, 28, 58), bar_rect, border_radius=4)
        if ratio > 0:
            fill_width = max(6, int((bar_rect.width - 2) * ratio))
            pygame.draw.rect(
                surface,
                OCTOPUS_WARNING_COLOR,
                (bar_rect.x + 1, bar_rect.y + 1, fill_width, bar_rect.height - 2),
                border_radius=4,
            )
