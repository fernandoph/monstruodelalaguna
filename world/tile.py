import pygame

from settings import (
    TILE_BORDER_COLOR,
    TILE_COLOR,
    TILE_HIGHLIGHT_COLOR,
    TILE_PLANT_COLOR,
    TILE_TOP_MOSS_COLOR,
)


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, top_exposed=False, left_exposed=False, right_exposed=False):
        super().__init__()
        self.image = self.build_surface(
            pos,
            size,
            top_exposed=top_exposed,
            left_exposed=left_exposed,
            right_exposed=right_exposed,
        )
        self.rect = self.image.get_rect(topleft=pos)

    def build_surface(self, pos, size, top_exposed=False, left_exposed=False, right_exposed=False):
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        surface.fill(TILE_COLOR)
        pygame.draw.rect(surface, TILE_BORDER_COLOR, surface.get_rect(), 3, border_radius=6)

        seed = (pos[0] // max(1, size)) * 31 + (pos[1] // max(1, size)) * 17

        for index in range(3):
            width = 10 + ((seed + index * 7) % 16)
            height = 6 + ((seed + index * 11) % 10)
            x = 6 + ((seed + index * 13) % max(1, size - width - 12))
            y = size // 3 + ((seed + index * 19) % max(1, size - height - 10))
            rock_rect = pygame.Rect(x, y, width, height)
            pygame.draw.ellipse(surface, TILE_HIGHLIGHT_COLOR, rock_rect)
            pygame.draw.ellipse(surface, TILE_BORDER_COLOR, rock_rect, 1)

        if top_exposed:
            pygame.draw.rect(surface, TILE_TOP_MOSS_COLOR, (0, 0, size, 12), border_radius=6)
            for stalk in range(3):
                base_x = 10 + stalk * 18 + ((seed + stalk * 5) % 6)
                points = [
                    (base_x, 10),
                    (base_x - 4, 4 + stalk),
                    (base_x + 2, 0),
                    (base_x + 6, 4 + (stalk % 2)),
                    (base_x + 3, 12),
                ]
                pygame.draw.polygon(surface, TILE_PLANT_COLOR, points)

        if left_exposed:
            pygame.draw.line(surface, TILE_HIGHLIGHT_COLOR, (1, 12), (1, size - 8), 2)
        if right_exposed:
            pygame.draw.line(surface, TILE_HIGHLIGHT_COLOR, (size - 2, 12), (size - 2, size - 8), 2)

        for bubble_index in range(2):
            radius = 2 + ((seed + bubble_index * 9) % 3)
            x = 12 + ((seed + bubble_index * 15) % max(1, size - 24))
            y = 16 + ((seed + bubble_index * 10) % max(1, size - 32))
            pygame.draw.circle(surface, (174, 214, 198, 70), (x, y), radius, 1)

        return surface

    def update(self, x_shift):
        self.rect.x += x_shift
