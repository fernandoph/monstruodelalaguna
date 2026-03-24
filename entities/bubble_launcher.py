import pygame

from settings import BUBBLE_COLOR, BUBBLE_LAUNCHER_COLOR, TILE_SIZE


class BubbleLauncher(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = self.build_surface()
        self.rect = self.image.get_rect(bottomleft=(pos[0], pos[1] + TILE_SIZE))
        self.active_timer = 0
        self.cooldown_timer = 0
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
            self.active_timer = 50
            self.cooldown_timer = 90

    def update(self, x_shift):
        self.rect.x += x_shift
        if self.active_timer > 0:
            self.active_timer -= 1
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1

    def draw_effect(self, surface):
        if self.active_timer <= 0:
            return

        effect_surface = pygame.Surface((40, self.effect_height), pygame.SRCALPHA)
        pygame.draw.rect(effect_surface, (190, 236, 255, 42), (6, 0, 28, self.effect_height), border_radius=12)

        for index in range(6):
            bubble_y = self.effect_height - 18 - ((self.active_timer * 4 + index * 22) % max(1, self.effect_height - 24))
            bubble_x = 10 + (index % 3) * 8
            radius = 4 + (index % 2)
            pygame.draw.circle(effect_surface, BUBBLE_COLOR, (bubble_x + 4, bubble_y), radius, 2)

        surface.blit(effect_surface, (self.rect.centerx - 20, self.rect.top - self.effect_height + 10))
