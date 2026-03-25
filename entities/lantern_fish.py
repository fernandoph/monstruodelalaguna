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

    @property
    def bulb_world_position(self):
        return (self.rect.x + 46, self.rect.y + 8)

    def build_frames(self, body_color):
        return [self.build_frame(offset, body_color) for offset in (-2, 1, 3, 0)]

    def build_frame(self, tail_offset, body_color):
        surface = pygame.Surface((TILE_SIZE, TILE_SIZE // 2 + 10), pygame.SRCALPHA)
        body_rect = pygame.Rect(10, 14, 28, 18)
        belly_rect = pygame.Rect(16, 22, 16, 8)
        jaw_points = [(12, 24), (24, 20), (32, 28), (18, 30)]
        tail_base_x = body_rect.right - 2
        tail_tip_x = surface.get_width() - 8

        pygame.draw.ellipse(surface, body_color, body_rect)
        pygame.draw.ellipse(surface, (*LANTERN_FISH_GLOW[:3], 40), belly_rect)
        pygame.draw.polygon(
            surface,
            LANTERN_FISH_FIN,
            [
                (tail_base_x, body_rect.centery),
                (tail_tip_x, 12 + tail_offset),
                (tail_tip_x, surface.get_height() - 12 - tail_offset),
            ],
        )
        pygame.draw.polygon(surface, body_color, jaw_points)
        pygame.draw.polygon(
            surface,
            LANTERN_FISH_FIN,
            [(26, 14), (34, 8 + tail_offset // 2), (36, 18)],
        )
        pygame.draw.polygon(
            surface,
            LANTERN_FISH_FIN,
            [(22, 28), (30, 34 - tail_offset // 3), (34, 28)],
        )
        pygame.draw.line(surface, LANTERN_FISH_FIN, (32, 15), (45, 6), 2)
        pygame.draw.circle(surface, LANTERN_FISH_GLOW[:3], (47, 5), 4)
        pygame.draw.circle(surface, (255, 255, 255), (20, 19), 3)
        pygame.draw.circle(surface, (22, 24, 32), (20, 19), 1)
        pygame.draw.line(surface, (228, 214, 162), (14, 27), (22, 27), 1)
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
        glow_surface = pygame.Surface((144, 96), pygame.SRCALPHA)
        glow_rgb = LANTERN_FISH_DIM_GLOW[:3] if self.dimmed else LANTERN_FISH_GLOW[:3]
        glow_color = (*glow_rgb, self.glow_alpha)
        outer_alpha = max(8, self.glow_alpha // 3)
        radius = 14 if self.dimmed else 22
        outer_radius = 28 if self.dimmed else 42
        glow_center = (56, 34)
        pygame.draw.circle(glow_surface, glow_color, glow_center, radius)
        pygame.draw.circle(glow_surface, (*glow_rgb, outer_alpha), glow_center, outer_radius)
        bulb_x, bulb_y = self.bulb_world_position
        surface.blit(glow_surface, (bulb_x - glow_center[0], bulb_y - glow_center[1]))
