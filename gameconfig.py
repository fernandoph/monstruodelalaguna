from data.level_loader import load_level_definition
from settings import (
    DEFAULT_LEVEL_ID,
    FPS,
    SCREEN_BACKGROUND_COLOR,
    SCREEN_CAPTION,
    SCREEN_WIDTH,
    TILE_SIZE,
)


_default_level = load_level_definition(DEFAULT_LEVEL_ID)

level_map = _default_level.layout

tile_size = TILE_SIZE
screen_width = SCREEN_WIDTH
screen_height = _default_level.pixel_height

screen_size = (screen_width, screen_height)
screen_center = (screen_width // 2, screen_height // 2)
screen_caption = SCREEN_CAPTION
screen_color = SCREEN_BACKGROUND_COLOR
fps = FPS
