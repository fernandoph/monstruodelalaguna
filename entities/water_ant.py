import math

import pygame

from settings import TILE_SIZE, WATER_ANT_ALERT_COLOR, WATER_ANT_COLOR, WATER_ANT_SHELL_COLOR


class WaterAnt(pygame.sprite.Sprite):
    def __init__(self, pos, patrol_distance=72, speed=1.2):
        super().__init__()
        self.frames = self.build_frames()
        self.alert_frames = self.build_frames(alert=True)
        self.animation_index = 0.0
        self.animation_speed = 0.18
        self.image = self.frames[0]
        self.rect = self.image.get_rect(bottomleft=(pos[0], pos[1] + TILE_SIZE))
        self.origin_x = float(self.rect.x)
        self.world_x = float(self.rect.x)
        self.ground_y = float(self.rect.bottom)
        self.patrol_distance = patrol_distance
        self.chase_distance = patrol_distance + 80
        self.speed = speed
        self.direction = 1
        self.alertness = 0
        self.pause_timer = 0
        self.bob_phase = (pos[0] % 90) / 90 * math.tau

    def build_frames(self, alert=False):
        return [self.build_frame(leg_offset, alert=alert) for leg_offset in (-3, 0, 3, 0)]

    def build_frame(self, leg_offset, alert=False):
        surface = pygame.Surface((TILE_SIZE - 16, TILE_SIZE - 18), pygame.SRCALPHA)
        body_rect = pygame.Rect(8, 18, 22, 14)
        shell_rect = pygame.Rect(18, 10, 24, 22)
        head_rect = pygame.Rect(2, 14, 16, 14)
        eye_color = WATER_ANT_ALERT_COLOR if alert else (24, 24, 24)

        pygame.draw.ellipse(surface, WATER_ANT_SHELL_COLOR, shell_rect)
        pygame.draw.ellipse(surface, WATER_ANT_COLOR, body_rect)
        pygame.draw.ellipse(surface, WATER_ANT_COLOR, head_rect)

        for index in range(3):
            base_y = 22 + index * 5
            pygame.draw.line(surface, WATER_ANT_COLOR, (18, base_y), (8, base_y + leg_offset), 2)
            pygame.draw.line(surface, WATER_ANT_COLOR, (30, base_y), (42, base_y - leg_offset), 2)

        pygame.draw.line(surface, WATER_ANT_COLOR, (8, 16), (2, 8), 2)
        pygame.draw.line(surface, WATER_ANT_COLOR, (12, 16), (12, 6), 2)
        pygame.draw.circle(surface, eye_color, (8, 20), 2)
        if alert:
            pygame.draw.line(surface, WATER_ANT_ALERT_COLOR, (18, 8), (24, 6), 2)
            pygame.draw.line(surface, WATER_ANT_ALERT_COLOR, (26, 6), (32, 8), 2)
        return surface.convert_alpha()

    @property
    def is_alerted(self):
        return self.alertness >= 6

    def update(self, x_shift, player=None):
        self.origin_x += x_shift
        self.world_x += x_shift
        self.bob_phase = (self.bob_phase + 0.14) % math.tau

        chase_mode = False
        move_speed = self.speed

        if player is not None:
            player_dx = player.hitbox.centerx - self.rect.centerx
            player_dy = abs(player.hitbox.centery - self.rect.centery)
            if abs(player_dx) <= self.chase_distance and player_dy <= TILE_SIZE:
                self.alertness = min(16, self.alertness + 1)
                self.direction = 1 if player_dx >= 0 else -1
                chase_mode = self.alertness >= 6
            else:
                self.alertness = max(0, self.alertness - 1)

        if self.pause_timer > 0:
            self.pause_timer -= 1
        else:
            if self.alertness > 0 and not chase_mode:
                move_speed *= 0.55
            elif chase_mode:
                move_speed *= 1.65
            self.world_x += move_speed * self.direction

        roam_limit = self.patrol_distance + (48 if chase_mode else 0)
        left_limit = self.origin_x - roam_limit
        right_limit = self.origin_x + roam_limit

        if self.world_x <= left_limit:
            self.world_x = left_limit
            self.direction = 1
            if not chase_mode:
                self.pause_timer = 8
        elif self.world_x >= right_limit:
            self.world_x = right_limit
            self.direction = -1
            if not chase_mode:
                self.pause_timer = 8

        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.frames):
            self.animation_index = 0

        frame_set = self.alert_frames if self.is_alerted else self.frames
        frame = frame_set[int(self.animation_index)]
        self.image = pygame.transform.flip(frame, self.direction < 0, False)
        current_bottomleft = (round(self.world_x), round(self.ground_y + math.sin(self.bob_phase) * 2))
        self.rect = self.image.get_rect(bottomleft=current_bottomleft)
