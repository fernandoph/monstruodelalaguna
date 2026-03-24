import pygame

from settings import (
    FISH_BELLY_COLOR,
    FISH_COLOR,
    FISH_EYE_COLOR,
    FISH_FIN_COLOR,
    FISH_STRIPE_COLOR,
    TILE_SIZE,
)


class Fish(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.frames = self.build_frames()
        self.animation_index = 0.0
        self.animation_speed = 0.18
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(pos[0] + TILE_SIZE // 2, pos[1] + TILE_SIZE // 2))

    def build_frames(self):
        tail_swings = (-4, 2, 5, -1)
        return [self.build_frame(tail_swing) for tail_swing in tail_swings]

    def build_frame(self, tail_swing):
        width = TILE_SIZE - 12
        height = TILE_SIZE // 2 + 4
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        body_rect = pygame.Rect(10, 10, width - 26, height - 14)
        belly_rect = pygame.Rect(body_rect.x + 3, body_rect.y + body_rect.height // 2 - 1, body_rect.width - 6, body_rect.height // 2 + 2)

        tail_base_x = body_rect.right - 2
        tail_center_y = body_rect.centery
        tail_tip_x = width - 4
        tail_top_y = tail_center_y - 9 + tail_swing
        tail_bottom_y = tail_center_y + 9 - tail_swing

        pygame.draw.polygon(
            surface,
            FISH_FIN_COLOR,
            [
                (tail_base_x, tail_center_y - 4),
                (tail_tip_x, tail_top_y),
                (tail_tip_x, tail_bottom_y),
                (tail_base_x, tail_center_y + 4),
            ],
        )

        dorsal_fin = [
            (body_rect.x + 9, body_rect.y + 2),
            (body_rect.x + 16, body_rect.y - 8 + tail_swing // 2),
            (body_rect.x + 24, body_rect.y + 3),
        ]
        side_fin = [
            (body_rect.x + body_rect.width // 2 - 2, body_rect.y + body_rect.height // 2 + 2),
            (body_rect.x + body_rect.width // 2 + 6, body_rect.bottom + 4),
            (body_rect.x + body_rect.width // 2 + 12, body_rect.y + body_rect.height // 2 + 5),
        ]
        pygame.draw.polygon(surface, FISH_FIN_COLOR, dorsal_fin)
        pygame.draw.polygon(surface, FISH_FIN_COLOR, side_fin)

        pygame.draw.ellipse(surface, FISH_COLOR, body_rect)
        pygame.draw.ellipse(surface, FISH_BELLY_COLOR, belly_rect)

        highlight_rect = body_rect.inflate(-10, -10)
        highlight_rect.y -= 1
        pygame.draw.ellipse(surface, (255, 241, 215, 90), highlight_rect)

        stripe_one = pygame.Rect(body_rect.x + 8, body_rect.y + 2, 5, body_rect.height - 4)
        stripe_two = pygame.Rect(body_rect.x + 16, body_rect.y + 4, 5, body_rect.height - 8)
        pygame.draw.ellipse(surface, FISH_STRIPE_COLOR, stripe_one)
        pygame.draw.ellipse(surface, FISH_STRIPE_COLOR, stripe_two)

        eye_center = (body_rect.x + 10, body_rect.y + 8)
        pygame.draw.circle(surface, (255, 255, 255), eye_center, 4)
        pygame.draw.circle(surface, FISH_EYE_COLOR, eye_center, 2)
        pygame.draw.arc(
            surface,
            FISH_EYE_COLOR,
            pygame.Rect(body_rect.x + 2, body_rect.y + 10, 8, 6),
            3.5,
            5.2,
            1,
        )

        return surface.convert_alpha()

    def update(self, x_shift):
        center = (self.rect.centerx + x_shift, self.rect.centery)
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
        self.rect = self.image.get_rect(center=center)
