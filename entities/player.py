import pygame

from settings import (
    GRAPHICS_DIR,
    PLACEHOLDER_ANIMATION_COLORS,
    PLAYER_ANIMATIONS,
    PLAYER_DANCE_DURATION,
    PLAYER_GRAVITY,
    PLAYER_HURT_DURATION,
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
        self.hitbox = self.rect.inflate(-18, -6)
        self.standing_height = self.hitbox.height
        self.crouching_height = max(32, self.hitbox.height - 22)

        self.direction = pygame.math.Vector2(0, 0)
        self.base_speed = PLAYER_SPEED
        self.speed = self.base_speed
        self.gravity = PLAYER_GRAVITY
        self.jump_speed = PLAYER_JUMP_SPEED

        self.on_ground = False
        self.crouching = False
        self.jump_held = False
        self.facing_right = True
        self.hurt_timer = 0
        self.dance_timer = 0

    def import_character_assets(self):
        character_path = GRAPHICS_DIR / "character"
        return load_animation_set(
            character_path,
            PLAYER_ANIMATIONS,
            fallback_size=(TILE_SIZE, TILE_SIZE),
            fallback_colors=PLACEHOLDER_ANIMATION_COLORS,
        )

    @property
    def controls_locked(self):
        return self.hurt_timer > 0 or self.dance_timer > 0

    def sync_rect(self):
        self.rect = self.image.get_rect(midbottom=self.hitbox.midbottom)

    def update_hitbox_height(self, new_height):
        if self.hitbox.height == new_height:
            return
        bottom = self.hitbox.bottom
        self.hitbox.height = new_height
        self.hitbox.bottom = bottom

    def set_crouching(self, active):
        should_crouch = active and self.on_ground and not self.controls_locked
        self.crouching = should_crouch
        target_height = self.crouching_height if should_crouch else self.standing_height
        self.update_hitbox_height(target_height)

    def process_input(self, lock_input=False):
        keys = pygame.key.get_pressed()

        if lock_input or self.controls_locked:
            self.direction.x = 0
        else:
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.facing_right = True
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.facing_right = False
            else:
                self.direction.x = 0

        self.set_crouching(keys[pygame.K_DOWN])

        wants_jump = keys[pygame.K_SPACE]
        if (
            wants_jump
            and not self.jump_held
            and self.on_ground
            and not self.crouching
            and not lock_input
            and not self.controls_locked
        ):
            self.jump()
        self.jump_held = wants_jump

    def update_timers(self):
        if self.hurt_timer > 0:
            self.hurt_timer -= 1
        if self.dance_timer > 0:
            self.dance_timer -= 1

    def get_status(self):
        if self.dance_timer > 0:
            self.status = "dance"
        elif self.hurt_timer > 0:
            self.status = "hurt"
        elif self.crouching and self.on_ground:
            self.status = "crouch"
        elif self.direction.y < 0:
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

        self.image = animation[int(self.frame_index)]
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
        self.sync_rect()

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.hitbox.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        self.on_ground = False

    def start_hurt(self, duration=PLAYER_HURT_DURATION):
        self.hurt_timer = duration
        self.direction.x = 0

    def start_dance(self, duration=PLAYER_DANCE_DURATION):
        self.dance_timer = duration
        self.direction.x = 0
        self.direction.y = 0
        self.set_crouching(False)

    def update(self, lock_input=False):
        self.update_timers()
        self.process_input(lock_input=lock_input)
