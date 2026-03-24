import pygame

from entities.fish import Fish
from entities.hazard import Hazard
from entities.level_exit import LevelExit
from entities.player import Player
from settings import (
    EMPTY_TILE_MARKER,
    EXIT_MARKERS,
    FISH_MARKER,
    HAZARD_MARKER,
    PLAYER_SPAWN_MARKER,
    SOLID_TILE_MARKER,
    TILE_SIZE,
)
from world.tile import Tile


class Level:
    def __init__(self, level_definition, surface):
        self.definition = level_definition
        self.display_surface = surface
        self.background_color = level_definition.background_color
        self.fish_goal = level_definition.fish_goal
        self.collected_fish = 0
        self.world_shift = 0
        self.failed = False
        self.completed = False
        self.failure_reason = None
        self.fail_countdown = 0
        self.completion_countdown = 0
        self.blocked_exit_feedback_timer = 0
        self.reserved_markers = {}
        self.setup_level(level_definition.layout)

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group()
        self.fishes = pygame.sprite.Group()
        self.exits = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if cell == SOLID_TILE_MARKER:
                    self.tiles.add(Tile((x, y), TILE_SIZE))
                elif cell == PLAYER_SPAWN_MARKER:
                    self.player.add(Player((x, y)))
                elif cell == FISH_MARKER:
                    self.fishes.add(Fish((x, y)))
                elif cell in EXIT_MARKERS:
                    self.exits.add(LevelExit((x, y)))
                elif cell == HAZARD_MARKER:
                    self.hazards.add(Hazard((x, y), TILE_SIZE))
                elif cell != EMPTY_TILE_MARKER:
                    self.reserved_markers.setdefault(cell, []).append((x, y))

        if self.player.sprite is None:
            raise ValueError("Level loaded without a valid player spawn.")

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.hitbox.centerx
        direction_x = player.direction.x
        screen_center_x = self.display_surface.get_width() // 2

        if player_x < screen_center_x and direction_x < 0:
            self.world_shift = player.base_speed
            player.speed = 0
        elif player_x > screen_center_x and direction_x > 0:
            self.world_shift = -player.base_speed
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = player.base_speed

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.hitbox.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.hitbox):
                if player.direction.x < 0:
                    player.hitbox.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.hitbox.right = sprite.rect.left

        player.sync_rect()

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.on_ground = False
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.hitbox):
                if player.direction.y > 0:
                    player.hitbox.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.hitbox.top = sprite.rect.bottom
                    player.direction.y = 0

        player.sync_rect()

    @property
    def fish_remaining(self):
        return max(0, self.fish_goal - self.collected_fish)

    @property
    def exit_open(self):
        return self.collected_fish >= self.fish_goal

    @property
    def message_text(self):
        if self.blocked_exit_feedback_timer > 0:
            return f"Faltan {self.fish_remaining} peces para abrir la salida"
        if self.fail_countdown > 0:
            return "Cuidado con los pozos y obstaculos"
        if self.completion_countdown > 0:
            return "Nivel completado"
        return ""

    def update_world_shift(self):
        for group in (self.tiles, self.hazards, self.fishes, self.exits):
            group.update(self.world_shift)

    def update_exits(self):
        for exit_sprite in self.exits.sprites():
            exit_sprite.set_open(self.exit_open)

    def collect_fish(self):
        player = self.player.sprite
        collected = [sprite for sprite in self.fishes.sprites() if sprite.rect.colliderect(player.hitbox)]
        for fish in collected:
            fish.kill()
        self.collected_fish += len(collected)

    def trigger_failure(self, reason):
        if self.fail_countdown > 0 or self.completion_countdown > 0:
            return
        self.failure_reason = reason
        self.fail_countdown = 30
        self.player.sprite.start_hurt()

    def check_hazards(self):
        player = self.player.sprite

        if player.hitbox.top > self.display_surface.get_height() + TILE_SIZE:
            self.trigger_failure("pit")
            return

        for hazard in self.hazards.sprites():
            if hazard.rect.colliderect(player.hitbox):
                self.trigger_failure("hazard")
                return

    def check_exit_collision(self):
        player = self.player.sprite
        for exit_sprite in self.exits.sprites():
            if not exit_sprite.rect.colliderect(player.hitbox):
                continue

            if self.exit_open:
                if self.completion_countdown == 0:
                    self.completion_countdown = 45
                    player.start_dance(duration=self.completion_countdown)
                return

            self.blocked_exit_feedback_timer = 45

    def update_level_timers(self):
        if self.blocked_exit_feedback_timer > 0:
            self.blocked_exit_feedback_timer -= 1

        if self.fail_countdown > 0:
            self.fail_countdown -= 1
            if self.fail_countdown == 0:
                self.failed = True

        if self.completion_countdown > 0:
            self.completion_countdown -= 1
            if self.completion_countdown == 0:
                self.completed = True

    def update(self):
        player = self.player.sprite
        lock_input = self.fail_countdown > 0 or self.completion_countdown > 0
        player.update(lock_input=lock_input)
        self.scroll_x()
        self.update_world_shift()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.collect_fish()
        self.update_exits()
        self.check_exit_collision()
        self.check_hazards()
        player.get_status()
        player.animate()
        self.update_level_timers()

    def draw(self):
        self.tiles.draw(self.display_surface)
        self.hazards.draw(self.display_surface)
        self.fishes.draw(self.display_surface)
        self.exits.draw(self.display_surface)
        self.player.draw(self.display_surface)

    def run(self):
        self.update()
        self.draw()
