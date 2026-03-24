import pygame

from entities.player import Player
from settings import EMPTY_TILE_MARKER, PLAYER_SPAWN_MARKER, SOLID_TILE_MARKER, TILE_SIZE
from world.tile import Tile


class Level:
    def __init__(self, level_definition, surface):
        self.definition = level_definition
        self.display_surface = surface
        self.background_color = level_definition.background_color
        self.world_shift = 0
        self.reserved_markers = {}
        self.setup_level(level_definition.layout)

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if cell == SOLID_TILE_MARKER:
                    self.tiles.add(Tile((x, y), TILE_SIZE))
                elif cell == PLAYER_SPAWN_MARKER:
                    self.player.add(Player((x, y)))
                elif cell != EMPTY_TILE_MARKER:
                    self.reserved_markers.setdefault(cell, []).append((x, y))

        if self.player.sprite is None:
            raise ValueError("Level loaded without a valid player spawn.")

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
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
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
