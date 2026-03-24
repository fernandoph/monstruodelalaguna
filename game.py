import pygame

from data.level_loader import load_level_definition
from settings import DEFAULT_LEVEL_ID, FPS, SCREEN_CAPTION, SCREEN_WIDTH
from world.level import Level


class Game:
    def __init__(self, level_id=DEFAULT_LEVEL_ID):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = None
        self.level_definition = None
        self.level = None
        pygame.display.set_caption(SCREEN_CAPTION)
        self.load_level(level_id)

    def load_level(self, level_id):
        self.level_definition = load_level_definition(level_id)
        screen_size = (SCREEN_WIDTH, self.level_definition.pixel_height)
        self.screen = pygame.display.set_mode(screen_size)
        self.level = Level(self.level_definition, self.screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def run(self, max_frames=None):
        frame_count = 0
        running = True

        while running:
            running = self.handle_events()

            self.screen.fill(self.level.background_color)
            self.level.run()

            pygame.display.update()
            self.clock.tick(FPS)

            frame_count += 1
            if max_frames is not None and frame_count >= max_frames:
                running = False

        pygame.quit()
        return 0
