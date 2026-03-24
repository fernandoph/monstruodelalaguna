import math

import pygame

from settings import (
    LANTERN_FISH_BODY,
    LANTERN_FISH_DIM_BODY,
    LANTERN_FISH_DIM_GLOW,
    LANTERN_FISH_FIN,
    LANTERN_FISH_GLOW,
    TILE_SIZE,
)


class LanternFish(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.frames = self.build_frames(LANTERN_FISH_BODY)
        self.dim_frames = self.build_frames(LANTERN_FISH_DIM_BODY)
        self.animation_index = 0.0
        self.animation_speed = 0.12
        self.image = self.frames[0]
        initial_center = (pos[0] + TILE_SIZE // 2, pos[1] + TILE_SIZE // 2)
        self.rect = self.image.get_rect(center=initial_center)
        self.anchor = pygame.math.Vector2(initial_center)
        self.center = pygame.math.Vector2(initial_center)
        self.evade_offset = pygame.math.Vector2()
        self.swim_phase = (pos[0] % 128) / 128 * math.tau
        self.glow_alpha = LANTERN_FISH_GLOW[3]
        self.dimmed = False

    def build_frames(self, body_color):
        return [self.build_frame(offset, body_color) for offset in (-2, 1, 3, 0)]

    def build_frame(self, tail_offset, body_color):
        surface = pygame.Surface((TILE_SIZE - 12, TILE_SIZE // 2), pygame.SRCALPHA)
        body_rect = pygame.Rect(8, 10, 24, 14)
        pygame.draw.ellipse(surface, body_color, body_rect)
        pygame.draw.polygon(
            surface,
            LANTERN_FISH_FIN,
            [
                (body_rect.right - 2, body_rect.centery),
                (surface.get_width() - 6, 8 + tail_offset),
                (surface.get_width() - 6, surface.get_height() - 8 - tail_offset),
            ],
        )
        pygame.draw.circle(surface, (255, 255, 255), (body_rect.x + 8, body_rect.y + 5), 3)
        pygame.draw.circle(surface, (30, 30, 32), (body_rect.x + 8, body_rect.y + 5), 1)
        pygame.draw.line(surface, LANTERN_FISH_FIN, (body_rect.x + 18, body_rect.y + 4), (body_rect.x + 28, 0), 2)
        pygame.draw.circle(surface, LANTERN_FISH_GLOW[:3], (body_rect.x + 30, 1), 4)
        return surface.convert_alpha()

    def update(self, x_shift):
        self.anchor.x += x_shift
        self.swim_phase = (self.swim_phase + 0.09) % math.tau
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        swim_offset = pygame.math.Vector2(
            math.sin(self.swim_phase) * 9,
            math.sin(self.swim_phase * 1.7) * 4,
        )
        target_center = self.anchor + self.evade_offset + swim_offset
        self.center = self.center.lerp(target_center, 0.18)
        frame_set = self.dim_frames if self.dimmed else self.frames
        self.image = frame_set[int(self.animation_index)]
        self.rect = self.image.get_rect(center=(round(self.center.x), round(self.center.y)))

    def update_glow(self, player):
        previous_dimmed = self.dimmed
        distance = self.center.distance_to(player.hitbox.center)
        if distance < 120:
            self.dimmed = True
            self.glow_alpha = 20
            evade_vector = self.center - pygame.math.Vector2(player.hitbox.center)
            if evade_vector.length_squared() == 0:
                evade_vector = pygame.math.Vector2(1, 0)
            evade_vector.scale_to_length(20)
            self.evade_offset = self.evade_offset.lerp(evade_vector, 0.12)
        elif distance < 220:
            self.dimmed = True
            self.glow_alpha = 85
            evade_vector = self.center - pygame.math.Vector2(player.hitbox.center)
            if evade_vector.length_squared() == 0:
                evade_vector = pygame.math.Vector2(1, 0)
            evade_vector.scale_to_length(10)
            self.evade_offset = self.evade_offset.lerp(evade_vector, 0.08)
        else:
            self.dimmed = False
            self.glow_alpha = LANTERN_FISH_GLOW[3]
            self.evade_offset = self.evade_offset.lerp((0, 0), 0.1)

        return previous_dimmed != self.dimmed

    def draw_glow(self, surface):
        glow_surface = pygame.Surface((120, 120), pygame.SRCALPHA)
        glow_rgb = LANTERN_FISH_DIM_GLOW[:3] if self.dimmed else LANTERN_FISH_GLOW[:3]
        glow_color = (*glow_rgb, self.glow_alpha)
        outer_alpha = max(12, self.glow_alpha // 3)
        radius = 24 if self.dimmed else 34
        outer_radius = 42 if self.dimmed else 54
        pygame.draw.circle(glow_surface, glow_color, (60, 60), radius)
        pygame.draw.circle(glow_surface, (*glow_rgb, outer_alpha), (60, 60), outer_radius)
        surface.blit(glow_surface, (self.rect.centerx - 60, self.rect.centery - 60), special_flags=pygame.BLEND_RGBA_ADD)
