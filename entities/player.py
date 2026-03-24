from pathlib import Path

import pygame

from settings import (
    GRAPHICS_DIR,
    PLAYER_ANIMATIONS,
    PLAYER_DANCE_DURATION,
    PLAYER_GRAVITY,
    PLAYER_HURT_DURATION,
    PLAYER_JUMP_SPEED,
    PLAYER_SPEED,
    PLAYER_SUPER_JUMP_SPEED,
    PLAYER_SUPER_JUMP_WINDOW_FRAMES,
)
from support import IMAGE_EXTENSIONS, import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.animations = self.import_character_assets()
        self.frame_index = 0.0
        self.animation_speed = 0.15
        self.status = "idle"
        self.previous_status = self.status
        self.animation_speeds = {
            "idle": 0.15,
            "run": 0.22,
            "jump": 0.12,
            "fall": 0.12,
            "crouch": 0.10,
            "hurt": 0.28,
            "dance": 0.24,
        }
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
        self.super_jump_timer = 0
        self.super_jump_available = False

    def import_character_assets(self):
        character_path = GRAPHICS_DIR / "character"
        idle_frames = import_folder(character_path / "idle")
        animations = {"idle": idle_frames}

        for animation_name in PLAYER_ANIMATIONS:
            if animation_name == "idle":
                continue

            animation_path = character_path / animation_name
            if self.animation_folder_has_frames(animation_path):
                animations[animation_name] = import_folder(animation_path)
            else:
                animations[animation_name] = self.build_generated_animation(
                    animation_name,
                    idle_frames,
                )

        return animations

    def build_generated_animation(self, animation_name, idle_frames):
        animation_builders = {
            "run": lambda: self.generate_transformed_frames(
                idle_frames,
                angles=(-6, -2, 0, 3, 6),
                scales=((0.95, 1.05), (1.02, 0.98), (1.06, 0.95), (1.0, 1.0), (0.97, 1.03)),
                add_colors=((4, 16, 10), (0, 0, 0), (8, 10, 0), (0, 0, 0), (4, 16, 10)),
            ),
            "jump": lambda: self.generate_transformed_frames(
                idle_frames,
                angles=(5, 0, -5, 0, 4),
                scales=((0.92, 1.14), (0.90, 1.16), (0.94, 1.10), (0.92, 1.14), (0.90, 1.16)),
                add_colors=((8, 8, 18),) * len(idle_frames),
            ),
            "fall": lambda: self.generate_transformed_frames(
                idle_frames,
                angles=(-4, 0, 4, 0, -3),
                scales=((1.08, 0.92), (1.12, 0.90), (1.05, 0.95), (1.10, 0.90), (1.08, 0.92)),
                add_colors=((18, 6, 6),) * len(idle_frames),
            ),
            "crouch": lambda: self.generate_transformed_frames(
                idle_frames,
                angles=(0, 0, 0, 0, 0),
                scales=((1.10, 0.74), (1.08, 0.76), (1.12, 0.72), (1.08, 0.76), (1.10, 0.74)),
                add_colors=((0, 0, 0),) * len(idle_frames),
            ),
            "hurt": lambda: self.generate_transformed_frames(
                idle_frames,
                angles=(12, -12, 10, -10, 0),
                scales=((1.04, 0.96),) * len(idle_frames),
                add_colors=((60, 0, 24), (40, 0, 18), (60, 0, 24), (40, 0, 18), (70, 0, 30)),
            ),
            "dance": lambda: self.generate_transformed_frames(
                idle_frames,
                angles=(-14, 14, -8, 8, 0),
                scales=((1.02, 1.02), (1.04, 0.98), (0.98, 1.04), (1.04, 0.98), (1.02, 1.02)),
                add_colors=((12, 20, 0), (24, 18, 0), (12, 20, 0), (24, 18, 0), (18, 24, 0)),
            ),
        }

        builder = animation_builders.get(animation_name)
        if builder is None:
            return idle_frames
        return builder()

    def generate_transformed_frames(self, idle_frames, angles, scales, add_colors):
        transformed_frames = []

        for index, frame in enumerate(idle_frames):
            transformed_frames.append(
                self.transform_frame(
                    frame,
                    angle=angles[index % len(angles)],
                    scale=scales[index % len(scales)],
                    add_color=add_colors[index % len(add_colors)],
                )
            )

        return transformed_frames

    def transform_frame(self, frame, angle=0, scale=(1.0, 1.0), add_color=(0, 0, 0)):
        transformed = frame.copy()

        if add_color != (0, 0, 0):
            overlay = pygame.Surface(transformed.get_size(), pygame.SRCALPHA)
            overlay.fill((*add_color, 0))
            transformed.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        width = max(1, int(transformed.get_width() * scale[0]))
        height = max(1, int(transformed.get_height() * scale[1]))
        transformed = pygame.transform.smoothscale(transformed, (width, height))

        if angle:
            transformed = pygame.transform.rotate(transformed, angle)

        return transformed

    def animation_folder_has_frames(self, path):
        directory = Path(path)
        if not directory.is_dir():
            return False

        return any(
            file_path.is_file() and file_path.suffix.lower() in IMAGE_EXTENSIONS
            for file_path in directory.iterdir()
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
        if wants_jump and not self.jump_held:
            self.handle_jump_press(lock_input=lock_input)
        self.jump_held = wants_jump

    def update_timers(self):
        if self.hurt_timer > 0:
            self.hurt_timer -= 1
        if self.dance_timer > 0:
            self.dance_timer -= 1
        if self.super_jump_timer > 0:
            self.super_jump_timer -= 1
        if self.super_jump_timer == 0:
            self.super_jump_available = False

    def handle_jump_press(self, lock_input=False):
        if lock_input or self.controls_locked or self.crouching:
            return

        if self.on_ground:
            self.jump()
            self.super_jump_timer = PLAYER_SUPER_JUMP_WINDOW_FRAMES
            self.super_jump_available = True
            return

        if self.super_jump_available and self.super_jump_timer > 0:
            self.super_jump()
            self.super_jump_available = False
            self.super_jump_timer = 0

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
        if self.status != self.previous_status:
            self.frame_index = 0
            self.previous_status = self.status

        self.frame_index += self.animation_speeds.get(self.status, self.animation_speed)

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

    def super_jump(self):
        self.direction.y = PLAYER_SUPER_JUMP_SPEED
        self.on_ground = False

    def reset_jump_chain(self):
        self.super_jump_timer = 0
        self.super_jump_available = False

    def start_hurt(self, duration=PLAYER_HURT_DURATION):
        self.hurt_timer = duration
        self.direction.x = 0
        self.reset_jump_chain()

    def start_dance(self, duration=PLAYER_DANCE_DURATION):
        self.dance_timer = duration
        self.direction.x = 0
        self.direction.y = 0
        self.set_crouching(False)
        self.reset_jump_chain()

    def update(self, lock_input=False):
        self.update_timers()
        self.process_input(lock_input=lock_input)
