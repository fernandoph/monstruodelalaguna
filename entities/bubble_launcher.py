import pygame

from settings import BUBBLE_ACTIVE_COLOR, BUBBLE_COLOR, BUBBLE_LAUNCHER_COLOR, TILE_SIZE


class BubbleLauncher(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = self.build_surface()
        self.rect = self.image.get_rect(bottomleft=(pos[0], pos[1] + TILE_SIZE))
        self.active_timer = 0
        self.cooldown_timer = 0
        self.hit_flash_timer = 0
        self.pulse_timer = 0
        self.effect_height = TILE_SIZE * 3

    def build_surface(self):
        surface = pygame.Surface((TILE_SIZE - 12, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(surface, BUBBLE_LAUNCHER_COLOR, (10, 10, 22, 42), border_radius=10)
        pygame.draw.ellipse(surface, (158, 214, 214), (8, 8, 26, 14))
        pygame.draw.rect(surface, (42, 70, 72), (14, 22, 14, 26), border_radius=6)
        return surface.convert_alpha()

    @property
    def bubble_rect(self):
        return pygame.Rect(self.rect.centerx - 16, self.rect.top - self.effect_height + 10, 32, self.effect_height)

    def activate(self):
        if self.cooldown_timer == 0:
            self.active_timer = 56
            self.cooldown_timer = 96
            self.hit_flash_timer = 12
            return True
        return False

    def note_enemy_hit(self):
        self.hit_flash_timer = 18

    def update(self, x_shift):
        self.rect.x += x_shift
        self.pulse_timer = (self.pulse_timer + 1) % 48
        if self.active_timer > 0:
            self.active_timer -= 1
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1
        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= 1

    def draw_effect(self, surface):
        nozzle_rect = pygame.Rect(self.rect.centerx - 14, self.rect.top - 8, 28, 16)
        glow_surface = pygame.Surface((44, 36), pygame.SRCALPHA)
        glow_alpha = 32 if self.cooldown_timer == 0 else 18
        if self.hit_flash_timer > 0:
            glow_alpha += 38
        pygame.draw.ellipse(glow_surface, (*BUBBLE_ACTIVE_COLOR, glow_alpha), (0, 2, 44, 28))
        surface.blit(glow_surface, (nozzle_rect.x - 8, nozzle_rect.y - 10))

        if self.active_timer <= 0:
            bubble_y = nozzle_rect.y - ((self.pulse_timer * 2) % 18)
            pygame.draw.circle(surface, BUBBLE_COLOR, (self.rect.centerx, bubble_y), 5, 2)
            return

        effect_surface = pygame.Surface((52, self.effect_height), pygame.SRCALPHA)
        active_alpha = 44 + min(48, self.hit_flash_timer * 4)
        pygame.draw.rect(effect_surface, (*BUBBLE_ACTIVE_COLOR, active_alpha), (10, 0, 32, self.effect_height), border_radius=14)
        pygame.draw.line(effect_surface, (*BUBBLE_ACTIVE_COLOR, 170), (26, 0), (26, self.effect_height), 2)

        for index in range(8):
            bubble_y = self.effect_height - 18 - ((self.active_timer * 5 + index * 20) % max(1, self.effect_height - 24))
            bubble_x = 10 + (index % 4) * 9
            radius = 4 + (index % 2)
            pygame.draw.circle(effect_surface, BUBBLE_COLOR, (bubble_x + 4, bubble_y), radius, 2)

        foam_y = max(12, self.effect_height - self.active_timer * 3)
        pygame.draw.ellipse(effect_surface, (*BUBBLE_ACTIVE_COLOR, 120), (8, foam_y, 36, 16))

        surface.blit(effect_surface, (self.rect.centerx - 26, self.rect.top - self.effect_height + 10))
