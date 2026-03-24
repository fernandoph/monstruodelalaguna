import pygame

from settings import (
    GRAPHICS_DIR,
    PLACEHOLDER_ANIMATION_COLORS,
    PLAYER_ANIMATIONS,
    PLAYER_GRAVITY,
    PLAYER_JUMP_SPEED,
    PLAYER_SPEED,
    TILE_SIZE,
)
from support import load_animation_set


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.animations = self.import_character_assets()
        self.frame_index = 0.0
        self.animation_speed = 0.15
        self.status = "idle"
        self.image = self.animations[self.status][0]
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pygame.math.Vector2(0, 0)
        self.base_speed = PLAYER_SPEED
        self.speed = self.base_speed
        self.gravity = PLAYER_GRAVITY
        self.jump_speed = PLAYER_JUMP_SPEED

    def import_character_assets(self):
        character_path = GRAPHICS_DIR / "character"
        return load_animation_set(
            character_path,
            PLAYER_ANIMATIONS,
            fallback_size=(TILE_SIZE, TILE_SIZE),
            fallback_colors=PLACEHOLDER_ANIMATION_COLORS,
        )

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            self.jump()

    def get_status(self):
        if self.direction.y < 0:
            self.status = "jump"
        elif self.direction.y > 1:
            self.status = "fall"
        elif self.direction.x != 0:
            self.status = "run"
        else:
            self.status = "idle"

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        midbottom = self.rect.midbottom
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(midbottom=midbottom)

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
