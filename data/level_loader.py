import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from settings import (
    ALLOWED_LEVEL_MARKERS,
    LEVELS_DIR,
    PLAYER_SPAWN_MARKER,
    SCREEN_BACKGROUND_COLOR,
    TILE_SIZE,
)


@dataclass(frozen=True)
class LevelDefinition:
    level_id: str
    name: str
    layout: list[str]
    fish_goal: int
    next_level: Optional[str]
    intro_text: str
    background_color: tuple[int, int, int]
    metadata_path: Path
    layout_path: Path
    markers: dict[str, list[tuple[int, int]]]

    @property
    def width_in_tiles(self):
        return len(self.layout[0])

    @property
    def height_in_tiles(self):
        return len(self.layout)

    @property
    def pixel_height(self):
        return self.height_in_tiles * TILE_SIZE


def load_level_definition(level_id):
    metadata_path = LEVELS_DIR / f"{level_id}.json"
    if not metadata_path.is_file():
        raise FileNotFoundError(f"Level metadata not found: {metadata_path}")

    with metadata_path.open("r", encoding="utf-8") as level_file:
        metadata = json.load(level_file)

    layout_name = metadata.get("layout", f"{level_id}.txt")
    layout_path = metadata_path.parent / layout_name
    layout = load_level_layout(layout_path)

    allowed_markers = set(metadata.get("allowed_markers", sorted(ALLOWED_LEVEL_MARKERS)))
    invalid_markers = sorted({cell for row in layout for cell in row if cell not in allowed_markers})
    if invalid_markers:
        raise ValueError(
            f"Level '{level_id}' contains unsupported markers: {', '.join(invalid_markers)}"
        )

    markers = collect_level_markers(layout)
    spawn_positions = markers.get(PLAYER_SPAWN_MARKER, [])
    if len(spawn_positions) != 1:
        raise ValueError(
            f"Level '{level_id}' must contain exactly one '{PLAYER_SPAWN_MARKER}' marker."
        )

    return LevelDefinition(
        level_id=metadata.get("id", level_id),
        name=metadata.get("name", level_id.replace("_", " ").title()),
        layout=layout,
        fish_goal=int(metadata.get("fish_goal", 0)),
        next_level=metadata.get("next_level"),
        intro_text=str(metadata.get("intro_text", "")).strip(),
        background_color=parse_color(
            metadata.get("background_color", SCREEN_BACKGROUND_COLOR)
        ),
        metadata_path=metadata_path,
        layout_path=layout_path,
        markers=markers,
    )


def load_level_layout(layout_path):
    if not layout_path.is_file():
        raise FileNotFoundError(f"Level layout not found: {layout_path}")

    rows = layout_path.read_text(encoding="utf-8").splitlines()
    if not rows:
        raise ValueError(f"Level layout is empty: {layout_path}")

    width = max(len(row) for row in rows)
    if width == 0:
        raise ValueError(f"Level layout does not contain any playable rows: {layout_path}")

    return [row.ljust(width) for row in rows]


def collect_level_markers(layout):
    markers = {}

    for row_index, row in enumerate(layout):
        for col_index, cell in enumerate(row):
            if cell == " ":
                continue
            markers.setdefault(cell, []).append((col_index, row_index))

    return markers


def parse_color(color_value):
    if (
        isinstance(color_value, (list, tuple))
        and len(color_value) == 3
        and all(isinstance(channel, int) for channel in color_value)
    ):
        return tuple(color_value)
    raise ValueError(f"Invalid RGB color value: {color_value}")
