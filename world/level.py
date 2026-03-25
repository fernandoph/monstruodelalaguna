import pygame

from entities.algae_platform import AlgaePlatform
from entities.bubble_launcher import BubbleLauncher
from entities.fish import Fish
from entities.hazard import Hazard
from entities.lantern_fish import LanternFish
from entities.level_exit import LevelExit
from entities.octopus import Octopus
from entities.player import Player
from entities.water_ant import WaterAnt
from settings import (
    ALGAE_PLATFORM_MARKER,
    BUBBLE_LAUNCHER_MARKER,
    BUBBLE_POP_COLOR,
    EMPTY_TILE_MARKER,
    EXIT_MARKERS,
    FISH_MARKER,
    HAZARD_MARKER,
    LAGOON_MIST,
    LAGOON_REED_DARK,
    LAGOON_REED_LIGHT,
    LAGOON_SKY_BOTTOM,
    LAGOON_SKY_TOP,
    LAGOON_SUN_GLOW,
    LAGOON_SURFACE_LINE,
    LAGOON_WATER_BOTTOM,
    LAGOON_WATER_TOP,
    LANTERN_FISH_MARKER,
    OCTOPUS_MARKER,
    PLAYER_DAMAGE_FLASH_COLOR,
    PLAYER_SPAWN_MARKER,
    SOLID_TILE_MARKER,
    TILE_SIZE,
    WATER_ANT_MARKER,
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
        self.event_text = ""
        self.event_timer = 0
        self.tutorial_text = ""
        self.tutorial_timer = 0
        self.shown_hints = set()
        self.sound_events = []
        self.bubble_particles = []
        self.damage_flash_timer = 0
        self.exit_open_announced = False
        self.camera_offset_x = 0
        self.reserved_markers = {}
        self.setup_level(level_definition.layout)
        self.build_background_cache()

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group()
        self.fishes = pygame.sprite.Group()
        self.exits = pygame.sprite.Group()
        self.algae_platforms = pygame.sprite.Group()
        self.water_ants = pygame.sprite.Group()
        self.octopuses = pygame.sprite.Group()
        self.bubble_launchers = pygame.sprite.Group()
        self.lantern_fishes = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if cell == SOLID_TILE_MARKER:
                    top_exposed = self.is_exposed(layout, row_index - 1, col_index)
                    left_exposed = self.is_exposed(layout, row_index, col_index - 1)
                    right_exposed = self.is_exposed(layout, row_index, col_index + 1)
                    self.tiles.add(
                        Tile(
                            (x, y),
                            TILE_SIZE,
                            top_exposed=top_exposed,
                            left_exposed=left_exposed,
                            right_exposed=right_exposed,
                        )
                    )
                elif cell == PLAYER_SPAWN_MARKER:
                    self.player.add(Player((x, y)))
                elif cell == FISH_MARKER:
                    self.fishes.add(Fish((x, y)))
                elif cell in EXIT_MARKERS:
                    self.exits.add(LevelExit((x, y)))
                elif cell == HAZARD_MARKER:
                    self.hazards.add(Hazard((x, y), TILE_SIZE))
                elif cell == ALGAE_PLATFORM_MARKER:
                    self.algae_platforms.add(AlgaePlatform((x, y)))
                elif cell == WATER_ANT_MARKER:
                    self.water_ants.add(WaterAnt((x, y)))
                elif cell == OCTOPUS_MARKER:
                    self.octopuses.add(Octopus((x, y)))
                elif cell == BUBBLE_LAUNCHER_MARKER:
                    self.bubble_launchers.add(BubbleLauncher((x, y)))
                elif cell == LANTERN_FISH_MARKER:
                    self.lantern_fishes.add(LanternFish((x, y)))
                elif cell != EMPTY_TILE_MARKER:
                    self.reserved_markers.setdefault(cell, []).append((x, y))

        if self.player.sprite is None:
            raise ValueError("Level loaded without a valid player spawn.")

    def is_exposed(self, layout, row_index, col_index):
        if row_index < 0 or row_index >= len(layout):
            return True
        if col_index < 0 or col_index >= len(layout[row_index]):
            return True
        return layout[row_index][col_index] != SOLID_TILE_MARKER

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
        player.current_platform = None
        player.apply_gravity()
        landed_on_platform = False

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.hitbox):
                if player.direction.y > 0:
                    player.hitbox.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                    player.reset_jump_chain()
                elif player.direction.y < 0:
                    player.hitbox.top = sprite.rect.bottom
                    player.direction.y = 0

        for platform in self.algae_platforms.sprites():
            if not platform.rect.colliderect(player.hitbox):
                continue
            if player.direction.y >= 0 and player.hitbox.bottom <= platform.rect.top + 24:
                player.hitbox.bottom = platform.rect.top
                if platform.delta.x != 0:
                    player.hitbox.x += round(platform.delta.x)
                    for tile in self.tiles.sprites():
                        if not tile.rect.colliderect(player.hitbox):
                            continue
                        if platform.delta.x > 0:
                            player.hitbox.right = tile.rect.left
                        else:
                            player.hitbox.left = tile.rect.right
                player.direction.y = 0
                player.on_ground = True
                player.current_platform = platform
                landed_on_platform = True

        if landed_on_platform:
            player.reset_jump_chain()

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
        if self.event_timer > 0:
            return self.event_text
        if self.tutorial_timer > 0:
            return self.tutorial_text
        return ""

    def show_event_message(self, text, duration=75):
        self.event_text = text
        self.event_timer = duration

    def show_tutorial_hint(self, hint_id, text, duration=150):
        if hint_id in self.shown_hints:
            return
        self.shown_hints.add(hint_id)
        self.tutorial_text = text
        self.tutorial_timer = duration

    def queue_sound_event(self, sound_name):
        self.sound_events.append(sound_name)

    def consume_sound_events(self):
        queued = list(self.sound_events)
        self.sound_events.clear()
        return queued

    def spawn_bubble_burst(self, center):
        velocities = (
            (-1.2, -3.6),
            (1.0, -4.2),
            (-2.0, -2.4),
            (2.2, -2.8),
            (-0.8, -5.0),
            (0.6, -3.1),
        )
        for index, velocity in enumerate(velocities):
            self.bubble_particles.append(
                {
                    "position": pygame.math.Vector2(center),
                    "velocity": pygame.math.Vector2(velocity),
                    "radius": 4 + (index % 2),
                    "life": 20 + index * 2,
                    "max_life": 20 + index * 2,
                }
            )

    def update_world_shift(self):
        self.camera_offset_x -= self.world_shift
        player = self.player.sprite
        for group in (self.tiles, self.hazards, self.fishes, self.exits):
            group.update(self.world_shift)
        for sprite in self.algae_platforms.sprites():
            sprite.update(self.world_shift)
        for sprite in self.water_ants.sprites():
            sprite.update(self.world_shift, player)
        for sprite in self.octopuses.sprites():
            sprite.update(self.world_shift)
        for sprite in self.bubble_launchers.sprites():
            sprite.update(self.world_shift)
        for sprite in self.lantern_fishes.sprites():
            sprite.update(self.world_shift)

    def update_exits(self):
        for exit_sprite in self.exits.sprites():
            exit_sprite.set_open(self.exit_open)
        if self.exit_open and not self.exit_open_announced:
            self.exit_open_announced = True
            self.queue_sound_event("exit_open")
            self.show_event_message("La salida ya esta abierta", duration=85)

    def collect_fish(self):
        player = self.player.sprite
        collected = [sprite for sprite in self.fishes.sprites() if sprite.rect.colliderect(player.hitbox)]
        for fish in collected:
            fish.kill()
        self.collected_fish += len(collected)
        if collected:
            self.queue_sound_event("fish_collect")

    def trigger_failure(self, reason):
        if self.fail_countdown > 0 or self.completion_countdown > 0:
            return
        self.failure_reason = reason
        self.fail_countdown = 30
        self.damage_flash_timer = 18
        self.queue_sound_event("damage")
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

        for ant in self.water_ants.sprites():
            if ant.rect.colliderect(player.hitbox):
                self.trigger_failure("water_ant")
                return

        for octopus in self.octopuses.sprites():
            if octopus.update_threat(player):
                self.trigger_failure("octopus")
                return

    def update_lantern_fishes(self):
        player = self.player.sprite
        for lantern_fish in self.lantern_fishes.sprites():
            dim_state_changed = lantern_fish.update_glow(player)
            if dim_state_changed and lantern_fish.dimmed:
                self.show_event_message("El pez linterna solo ilumina y se apaga si te acercas", duration=95)
                self.queue_sound_event("lantern_dim")

    def update_bubble_launchers(self):
        player = self.player.sprite
        for launcher in self.bubble_launchers.sprites():
            if launcher.rect.colliderect(player.hitbox):
                if launcher.activate():
                    self.show_event_message("Surtidor activado", duration=70)
                    self.queue_sound_event("bubble_activate")

    def resolve_bubble_effects(self):
        for launcher in self.bubble_launchers.sprites():
            if launcher.active_timer <= 0:
                continue

            bubble_rect = launcher.bubble_rect
            hit_enemy = False
            for ant in self.water_ants.sprites():
                if bubble_rect.colliderect(ant.rect):
                    launcher.note_enemy_hit()
                    self.spawn_bubble_burst(ant.rect.center)
                    self.show_event_message("La burbuja neutralizo una hormiga", duration=80)
                    ant.kill()
                    hit_enemy = True
            for octopus in self.octopuses.sprites():
                if bubble_rect.colliderect(octopus.rect):
                    launcher.note_enemy_hit()
                    self.spawn_bubble_burst(octopus.rect.center)
                    self.show_event_message("La columna de burbujas despejo el pulpo", duration=80)
                    octopus.kill()
                    hit_enemy = True
            if hit_enemy:
                self.queue_sound_event("bubble_hit")

    def check_exit_collision(self):
        player = self.player.sprite
        for exit_sprite in self.exits.sprites():
            if not exit_sprite.rect.colliderect(player.hitbox):
                continue

            if self.exit_open:
                if self.completion_countdown == 0:
                    self.completion_countdown = 45
                    self.queue_sound_event("level_complete")
                    player.start_dance(duration=self.completion_countdown)
                return

            self.blocked_exit_feedback_timer = 45

    def update_context_hints(self):
        player = self.player.sprite

        if any(platform.rect.inflate(120, 80).colliderect(player.hitbox) for platform in self.algae_platforms.sprites()):
            self.show_tutorial_hint("algae", "Las algas te transportan si te quedas arriba", duration=160)

        if any(launcher.rect.inflate(120, 80).colliderect(player.hitbox) for launcher in self.bubble_launchers.sprites()):
            self.show_tutorial_hint("bubble", "Toca el surtidor para lanzar burbujas contra enemigos", duration=160)

        if any(ant.rect.inflate(140, 70).colliderect(player.hitbox) and ant.is_alerted for ant in self.water_ants.sprites()):
            self.show_tutorial_hint("water_ant", "La hormiga te persigue cuando te detecta cerca", duration=160)

        if any(octopus.threat_rect.colliderect(player.hitbox) for octopus in self.octopuses.sprites()):
            self.show_tutorial_hint("octopus", "El pulpo avisa antes de atrapar: segui moviendote", duration=170)

        if any(lantern.rect.inflate(120, 90).colliderect(player.hitbox) and lantern.dimmed for lantern in self.lantern_fishes.sprites()):
            self.show_tutorial_hint("lantern", "El pez linterna no se junta: solo ilumina el camino", duration=170)

    def update_visual_effects(self):
        updated_particles = []
        for particle in self.bubble_particles:
            particle["life"] -= 1
            if particle["life"] <= 0:
                continue
            particle["position"] += particle["velocity"]
            particle["velocity"].y += 0.06
            updated_particles.append(particle)
        self.bubble_particles = updated_particles

    def update_level_timers(self):
        if self.blocked_exit_feedback_timer > 0:
            self.blocked_exit_feedback_timer -= 1

        if self.event_timer > 0:
            self.event_timer -= 1

        if self.tutorial_timer > 0:
            self.tutorial_timer -= 1

        if self.damage_flash_timer > 0:
            self.damage_flash_timer -= 1

        self.update_visual_effects()

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
        for sound_name in player.consume_sound_events():
            self.queue_sound_event(sound_name)
        self.scroll_x()
        self.update_world_shift()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.collect_fish()
        self.update_exits()
        self.update_lantern_fishes()
        self.update_bubble_launchers()
        self.resolve_bubble_effects()
        self.check_exit_collision()
        self.check_hazards()
        self.update_context_hints()
        player.get_status()
        player.animate()
        self.update_level_timers()

    def draw(self):
        self.draw_background()
        self.tiles.draw(self.display_surface)
        self.algae_platforms.draw(self.display_surface)
        self.hazards.draw(self.display_surface)
        for launcher in self.bubble_launchers.sprites():
            launcher.draw_effect(self.display_surface)
        self.fishes.draw(self.display_surface)
        self.water_ants.draw(self.display_surface)
        for octopus in self.octopuses.sprites():
            octopus.draw_threat(self.display_surface)
        self.octopuses.draw(self.display_surface)
        self.bubble_launchers.draw(self.display_surface)
        for lantern_fish in self.lantern_fishes.sprites():
            lantern_fish.draw_glow(self.display_surface)
        self.lantern_fishes.draw(self.display_surface)
        self.exits.draw(self.display_surface)
        self.draw_visual_effects()
        self.player.draw(self.display_surface)
        self.draw_damage_flash()

    def run(self):
        self.update()
        self.draw()

    def draw_visual_effects(self):
        for particle in self.bubble_particles:
            alpha = int(255 * (particle["life"] / particle["max_life"]))
            radius = max(2, particle["radius"])
            particle_surface = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
            pygame.draw.circle(
                particle_surface,
                (*BUBBLE_POP_COLOR[:3], alpha),
                (radius * 2, radius * 2),
                radius,
                2,
            )
            self.display_surface.blit(
                particle_surface,
                (particle["position"].x - radius * 2, particle["position"].y - radius * 2),
                special_flags=pygame.BLEND_RGBA_ADD,
            )

    def draw_damage_flash(self):
        if self.damage_flash_timer <= 0:
            return
        flash_alpha = int(PLAYER_DAMAGE_FLASH_COLOR[3] * (self.damage_flash_timer / 18))
        flash = pygame.Surface(self.display_surface.get_size(), pygame.SRCALPHA)
        flash.fill((*PLAYER_DAMAGE_FLASH_COLOR[:3], flash_alpha))
        self.display_surface.blit(flash, (0, 0))

    def draw_background(self):
        self.display_surface.blit(self.background_base_surface, (0, 0))
        self.blit_repeated_layer(self.lily_pad_surface, 0.12)
        self.blit_repeated_layer(self.particle_surface, 0.08)
        self.blit_repeated_layer(self.reed_far_surface, 0.25)
        self.blit_repeated_layer(self.reed_near_surface, 0.55)

    def build_background_cache(self):
        width = self.display_surface.get_width()
        height = self.display_surface.get_height()
        self.horizon_y = max(72, int(height * 0.24))

        base_surface = pygame.Surface((width, height)).convert()
        self.draw_vertical_gradient(
            base_surface,
            (0, 0, width, self.horizon_y),
            LAGOON_SKY_TOP,
            LAGOON_SKY_BOTTOM,
        )
        self.draw_vertical_gradient(
            base_surface,
            (0, self.horizon_y, width, height - self.horizon_y),
            LAGOON_WATER_TOP,
            LAGOON_WATER_BOTTOM,
        )

        glow_surface = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        pygame.draw.circle(glow_surface, LAGOON_SUN_GLOW, (width // 4, self.horizon_y // 2), 150)
        pygame.draw.circle(glow_surface, LAGOON_SUN_GLOW, (width // 3, self.horizon_y - 10), 110)
        base_surface.blit(glow_surface, (0, 0))

        surface_band = pygame.Surface((width, 32), pygame.SRCALPHA).convert_alpha()
        for index in range(6):
            y = 4 + index * 4
            pygame.draw.line(
                surface_band,
                LAGOON_SURFACE_LINE,
                (0, y),
                (width, y + (index % 2)),
                2,
            )
        base_surface.blit(surface_band, (0, self.horizon_y - 14))

        mist_surface = pygame.Surface((width, self.horizon_y + 40), pygame.SRCALPHA).convert_alpha()
        for index in range(5):
            mist_rect = pygame.Rect(index * 220 - 30, self.horizon_y - 20 + (index % 2) * 8, 240, 44)
            pygame.draw.ellipse(mist_surface, LAGOON_MIST, mist_rect)
        base_surface.blit(mist_surface, (0, 0))

        self.background_base_surface = base_surface
        self.reed_far_surface = self.build_water_plant_pattern(420, height, LAGOON_REED_LIGHT, 140)
        self.reed_near_surface = self.build_water_plant_pattern(420, height, LAGOON_REED_DARK, 190)
        self.lily_pad_surface = self.build_lily_pad_pattern(480)
        self.particle_surface = self.build_particle_pattern(520, height)

    def draw_vertical_gradient(self, target_surface, rect, top_color, bottom_color):
        x, y, width, height = rect
        if height <= 0:
            return

        for row in range(height):
            blend = row / max(1, height - 1)
            color = tuple(
                int(top_color[index] + (bottom_color[index] - top_color[index]) * blend)
                for index in range(3)
            )
            pygame.draw.line(
                target_surface,
                color,
                (x, y + row),
                (x + width, y + row),
            )

    def build_water_plant_pattern(self, pattern_width, screen_height, color, base_height):
        layer_surface = pygame.Surface((pattern_width, screen_height), pygame.SRCALPHA).convert_alpha()
        base_y = screen_height - 10

        for index in range(-2, (pattern_width // 70) + 4):
            root_x = int(index * 70)
            plant_height = base_height + (index % 4) * 18
            for blade_index in range(3):
                shift = blade_index * 10
                points = [
                    (root_x + shift, base_y),
                    (root_x - 8 + shift, base_y - plant_height * 0.45),
                    (root_x + 4 + shift, base_y - plant_height),
                    (root_x + 12 + shift, base_y - plant_height * 0.52),
                    (root_x + 8 + shift, base_y),
                ]
                pygame.draw.polygon(layer_surface, color, points)

        return layer_surface

    def build_lily_pad_pattern(self, pattern_width):
        pad_surface = pygame.Surface((pattern_width, self.horizon_y + 24), pygame.SRCALPHA).convert_alpha()

        for index in range(-1, (pattern_width // 160) + 3):
            center_x = int(index * 160)
            center_y = self.horizon_y - 6 + (index % 2) * 8
            pad_rect = pygame.Rect(center_x, center_y, 56, 18)
            pygame.draw.ellipse(pad_surface, (59, 118, 79, 180), pad_rect)
            pygame.draw.line(
                pad_surface,
                (88, 158, 101, 220),
                (pad_rect.centerx, pad_rect.centery),
                (pad_rect.right - 6, pad_rect.centery - 2),
                2,
            )

        return pad_surface

    def build_particle_pattern(self, pattern_width, height):
        particle_surface = pygame.Surface((pattern_width, height), pygame.SRCALPHA).convert_alpha()

        for index in range(18):
            x = int((index * 91) % (pattern_width + 80)) - 40
            y = self.horizon_y + 18 + (index * 43) % max(60, height - self.horizon_y - 28)
            radius = 2 + (index % 3)
            pygame.draw.circle(particle_surface, (210, 240, 228, 58), (x, y), radius)

        return particle_surface

    def blit_repeated_layer(self, layer_surface, depth_factor):
        layer_width = layer_surface.get_width()
        if layer_width <= 0:
            return

        offset = int((self.camera_offset_x * depth_factor) % layer_width)
        start_x = -offset - layer_width
        end_x = self.display_surface.get_width() + layer_width

        for x in range(start_x, end_x, layer_width):
            self.display_surface.blit(layer_surface, (x, 0))
