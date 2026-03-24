import pygame

from settings import LANTERN_FISH_BODY, LANTERN_FISH_FIN, LANTERN_FISH_GLOW, TILE_SIZE


class LanternFish(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.frames = self.build_frames()
        self.animation_index = 0.0
        self.animation_speed = 0.12
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(pos[0] + TILE_SIZE // 2, pos[1] + TILE_SIZE // 2))
        self.glow_alpha = LANTERN_FISH_GLOW[3]

    def build_frames(self):
        return [self.build_frame(offset) for offset in (-2, 1, 3, 0)]

    def build_frame(self, tail_offset):
        surface = pygame.Surface((TILE_SIZE - 12, TILE_SIZE // 2), pygame.SRCALPHA)
        body_rect = pygame.Rect(8, 10, 24, 14)
        pygame.draw.ellipse(surface, LANTERN_FISH_BODY, body_rect)
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
        self.rect.x += x_shift
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        center = self.rect.center
        self.image = self.frames[int(self.animation_index)]
        self.rect = self.image.get_rect(center=center)

    def update_glow(self, player):
        distance = pygame.math.Vector2(self.rect.center).distance_to(player.hitbox.center)
        if distance < 120:
            self.glow_alpha = 20
        elif distance < 220:
            self.glow_alpha = 85
        else:
            self.glow_alpha = LANTERN_FISH_GLOW[3]

    def draw_glow(self, surface):
        glow_surface = pygame.Surface((120, 120), pygame.SRCALPHA)
        glow_color = (*LANTERN_FISH_GLOW[:3], self.glow_alpha)
        pygame.draw.circle(glow_surface, glow_color, (60, 60), 34)
        pygame.draw.circle(glow_surface, (*LANTERN_FISH_GLOW[:3], max(8, self.glow_alpha // 3)), (60, 60), 52)
        surface.blit(glow_surface, (self.rect.centerx - 60, self.rect.centery - 60), special_flags=pygame.BLEND_RGBA_ADD)
