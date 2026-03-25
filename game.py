import pygame

from audio.manager import AudioManager
from data.level_loader import load_level_definition
from settings import (
    AUDIO_BUFFER_SIZE,
    AUDIO_SAMPLE_RATE,
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
        pygame.mixer.pre_init(frequency=AUDIO_SAMPLE_RATE, size=-16, channels=1, buffer=AUDIO_BUFFER_SIZE)
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = None
        self.level_definition = None
        self.level = None
        self.level_order = list(LEVEL_ORDER) or [level_id]
        self.current_level_index = 0
        self.difficulty = None
        self.lives = None
        self.state = None
        self.audio = None
        self.transition_frames = 0
        self.transition_title = ""
        self.transition_lines = []
        self.title_font = pygame.font.Font(None, 72)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        pygame.display.set_caption(SCREEN_CAPTION)
        self.load_level(level_id)
        self.audio = AudioManager()
        self.change_state("menu")

    def load_level(self, level_id):
        self.level_definition = load_level_definition(level_id)
        screen_size = (SCREEN_WIDTH, self.level_definition.pixel_height)
        self.screen = pygame.display.set_mode(screen_size, pygame.DOUBLEBUF)
        self.level = Level(self.level_definition, self.screen)

    def find_level_index(self, level_id):
        try:
            return self.level_order.index(level_id)
        except ValueError:
            return self.current_level_index

    def build_level_intro_lines(self):
        lines = [f"Nivel {self.current_level_index + 1} de {len(self.level_order)}"]
        if self.level_definition.intro_text:
            lines.append(self.level_definition.intro_text)
        lines.append(f"Meta: juntar {self.level_definition.fish_goal} peces")
        lines.append("Enter o Espacio para empezar")
        return lines

    def start_level_transition(self, level_id):
        self.current_level_index = self.find_level_index(level_id)
        self.load_level(level_id)
        self.transition_frames = 140
        self.transition_title = self.level_definition.name
        self.transition_lines = self.build_level_intro_lines()
        self.change_state("level_intro")

    def change_state(self, new_state):
        if new_state == self.state:
            return

        previous_state = self.state
        self.state = new_state

        if self.audio is None:
            return

        if new_state == "menu":
            self.audio.play_music("menu")
        elif new_state in {"playing", "level_intro"}:
            if previous_state == "paused":
                self.audio.resume_music()
            else:
                self.audio.play_music("lagoon")
        elif new_state == "paused":
            self.audio.play_sfx("pause")
            self.audio.pause_music()
        elif new_state == "game_over":
            self.audio.play_music(None)
            self.audio.play_sfx("game_over")
        elif new_state == "victory":
            if self.level and self.level.player.sprite:
                self.level.player.sprite.start_dance(duration=999999)
            self.audio.play_music(None)
            self.audio.play_sfx("victory")

    def start_new_game(self, difficulty):
        self.difficulty = difficulty
        self.lives = None if difficulty == "facil" else PLAYER_MAX_LIVES
        self.current_level_index = 0
        if self.audio:
            self.audio.play_sfx("menu_select")
        self.start_level_transition(self.level_order[self.current_level_index])

    def restart_level(self, play_sound=True):
        self.load_level(self.level_definition.level_id)
        if play_sound and self.audio:
            self.audio.play_sfx("restart")
        self.change_state("playing")

    def return_to_menu(self):
        self.change_state("menu")

    def handle_menu_key(self, event):
        if event.key == pygame.K_1:
            self.start_new_game("facil")
        elif event.key == pygame.K_2:
            self.start_new_game("normal")

    def handle_level_intro_key(self, event):
        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.transition_frames = 0
            self.change_state("playing")

    def handle_playing_key(self, event):
        if event.key == pygame.K_p:
            self.change_state("paused")
        elif event.key == pygame.K_r:
            self.restart_level()

    def handle_paused_key(self, event):
        if event.key in (pygame.K_p, pygame.K_ESCAPE):
            self.change_state("playing")
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
                elif self.state == "level_intro":
                    self.handle_level_intro_key(event)
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
                self.change_state("game_over")
                return
        self.restart_level(play_sound=False)

    def handle_level_complete(self):
        next_level_id = self.level_definition.next_level
        if next_level_id:
            self.start_level_transition(next_level_id)
            return

        next_index = self.current_level_index + 1
        if next_index < len(self.level_order):
            self.start_level_transition(self.level_order[next_index])
            return

        self.change_state("victory")

    def update(self):
        if self.state == "level_intro":
            if self.transition_frames > 0:
                self.transition_frames -= 1
            if self.transition_frames == 0:
                self.change_state("playing")
            return

        if self.state != "playing":
            return

        self.level.update()
        for sound_name in self.level.consume_sound_events():
            if self.audio:
                self.audio.play_sfx(sound_name)
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
                "Doble toque de Espacio para super jump",
                "P pausa el juego y R reinicia el nivel",
            ],
        )

    def draw_world(self):
        self.screen.fill(self.level.background_color if self.level else SCREEN_BACKGROUND_COLOR)
        if self.level:
            if self.state == "victory":
                player = self.level.player.sprite
                player.get_status()
                player.animate()
            self.level.draw()

    def draw(self):
        if self.state == "menu":
            self.draw_menu()
            return

        self.draw_world()
        self.draw_hud()

        if self.state == "level_intro":
            self.draw_overlay(self.transition_title, self.transition_lines)
        elif self.state == "paused":
            self.draw_overlay("Pausa", ["P o Esc para continuar", "R para reiniciar", "M para volver al menu"])
        elif self.state == "game_over":
            self.draw_overlay("Game Over", ["No quedan vidas", "Enter o R para volver al menu"])
        elif self.state == "victory":
            self.draw_overlay(
                "Juego Completado",
                [
                    f"Superaste los {len(self.level_order)} niveles de la laguna",
                    "El monstruo encontro la salida y se puso a bailar",
                    "Enter o R para volver al menu",
                ],
            )

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
