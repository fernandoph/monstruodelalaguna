import pygame

from data.level_loader import load_level_definition
from settings import (
    DEFAULT_LEVEL_ID,
    FPS,
    HUD_ACCENT_COLOR,
    HUD_PANEL_COLOR,
    HUD_TEXT_COLOR,
    LEVEL_ORDER,
    MENU_BACKGROUND_COLOR,
    OVERLAY_COLOR,
    PLAYER_MAX_LIVES,
    SCREEN_BACKGROUND_COLOR,
    SCREEN_CAPTION,
    SCREEN_WIDTH,
)
from world.level import Level


class Game:
    def __init__(self, level_id=DEFAULT_LEVEL_ID):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = None
        self.level_definition = None
        self.level = None
        self.level_order = list(LEVEL_ORDER) or [level_id]
        self.current_level_index = 0
        self.difficulty = None
        self.lives = None
        self.state = "menu"
        self.title_font = pygame.font.Font(None, 72)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        pygame.display.set_caption(SCREEN_CAPTION)
        self.load_level(level_id)

    def load_level(self, level_id):
        self.level_definition = load_level_definition(level_id)
        screen_size = (SCREEN_WIDTH, self.level_definition.pixel_height)
        self.screen = pygame.display.set_mode(screen_size)
        self.level = Level(self.level_definition, self.screen)

    def start_new_game(self, difficulty):
        self.difficulty = difficulty
        self.lives = None if difficulty == "facil" else PLAYER_MAX_LIVES
        self.current_level_index = 0
        self.load_level(self.level_order[self.current_level_index])
        self.state = "playing"

    def restart_level(self):
        self.load_level(self.level_definition.level_id)
        self.state = "playing"

    def return_to_menu(self):
        self.state = "menu"

    def handle_menu_key(self, event):
        if event.key == pygame.K_1:
            self.start_new_game("facil")
        elif event.key == pygame.K_2:
            self.start_new_game("normal")

    def handle_playing_key(self, event):
        if event.key == pygame.K_p:
            self.state = "paused"
        elif event.key == pygame.K_r:
            self.restart_level()

    def handle_paused_key(self, event):
        if event.key in (pygame.K_p, pygame.K_ESCAPE):
            self.state = "playing"
        elif event.key == pygame.K_r:
            self.restart_level()
        elif event.key == pygame.K_m:
            self.return_to_menu()

    def handle_terminal_state_key(self, event):
        if event.key in (pygame.K_RETURN, pygame.K_r):
            self.return_to_menu()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if self.state == "menu":
                    self.handle_menu_key(event)
                elif self.state == "playing":
                    self.handle_playing_key(event)
                elif self.state == "paused":
                    self.handle_paused_key(event)
                elif self.state in {"victory", "game_over"}:
                    self.handle_terminal_state_key(event)
        return True

    def handle_level_failure(self):
        if self.difficulty == "normal":
            self.lives -= 1
            if self.lives <= 0:
                self.state = "game_over"
                return
        self.restart_level()

    def handle_level_complete(self):
        next_level_id = self.level_definition.next_level
        if next_level_id:
            self.load_level(next_level_id)
            self.state = "playing"
            return

        next_index = self.current_level_index + 1
        if next_index < len(self.level_order):
            self.current_level_index = next_index
            self.load_level(self.level_order[self.current_level_index])
            self.state = "playing"
            return

        self.state = "victory"

    def update(self):
        if self.state != "playing":
            return

        self.level.update()
        if self.level.failed:
            self.handle_level_failure()
        elif self.level.completed:
            self.handle_level_complete()

    def draw_text(self, text, font, color, position):
        surface = font.render(text, True, color)
        self.screen.blit(surface, position)

    def draw_hud(self):
        panel = pygame.Surface((self.screen.get_width() - 24, 86), pygame.SRCALPHA)
        panel.fill(HUD_PANEL_COLOR)
        self.screen.blit(panel, (12, 12))

        fish_text = f"Peces: {self.level.collected_fish}/{self.level.fish_goal}"
        level_text = f"Nivel: {self.level_definition.name}"
        if self.difficulty == "facil":
            lives_text = "Modo: Facil"
        else:
            lives_text = f"Vidas: {self.lives}"

        self.draw_text(level_text, self.font, HUD_TEXT_COLOR, (28, 24))
        self.draw_text(fish_text, self.font, HUD_ACCENT_COLOR, (28, 52))
        self.draw_text(lives_text, self.font, HUD_TEXT_COLOR, (360, 52))

        if self.level.message_text:
            self.draw_text(self.level.message_text, self.small_font, HUD_TEXT_COLOR, (760, 54))

    def draw_overlay(self, title, lines):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill(OVERLAY_COLOR)
        self.screen.blit(overlay, (0, 0))

        box_width = min(760, self.screen.get_width() - 80)
        box_height = 180 + (len(lines) * 26)
        box = pygame.Rect(0, 0, box_width, box_height)
        box.center = self.screen.get_rect().center

        panel = pygame.Surface(box.size, pygame.SRCALPHA)
        panel.fill((10, 24, 42, 230))
        self.screen.blit(panel, box.topleft)

        title_surface = self.title_font.render(title, True, HUD_TEXT_COLOR)
        title_rect = title_surface.get_rect(midtop=(box.centerx, box.top + 24))
        self.screen.blit(title_surface, title_rect)

        current_y = title_rect.bottom + 20
        for line in lines:
            line_surface = self.font.render(line, True, HUD_TEXT_COLOR)
            line_rect = line_surface.get_rect(center=(box.centerx, current_y))
            self.screen.blit(line_surface, line_rect)
            current_y += 34

    def draw_menu(self):
        self.screen.fill(MENU_BACKGROUND_COLOR)
        self.draw_overlay(
            "El Monstruo de la Laguna",
            [
                "1: Iniciar en Facil",
                "2: Iniciar en Normal",
                "Flechas para moverse, Espacio para saltar",
                "P pausa el juego y R reinicia el nivel",
            ],
        )

    def draw_world(self):
        self.screen.fill(self.level.background_color if self.level else SCREEN_BACKGROUND_COLOR)
        if self.level:
            self.level.draw()

    def draw(self):
        if self.state == "menu":
            self.draw_menu()
            return

        self.draw_world()
        self.draw_hud()

        if self.state == "paused":
            self.draw_overlay("Pausa", ["P o Esc para continuar", "R para reiniciar", "M para volver al menu"])
        elif self.state == "game_over":
            self.draw_overlay("Game Over", ["No quedan vidas", "Enter o R para volver al menu"])
        elif self.state == "victory":
            self.draw_overlay("Victoria", ["Juntaste los peces y llegaste a la salida", "Enter o R para volver al menu"])

    def run(self, max_frames=None):
        frame_count = 0
        running = True

        while running:
            running = self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(FPS)

            frame_count += 1
            if max_frames is not None and frame_count >= max_frames:
                running = False

        pygame.quit()
        return 0
