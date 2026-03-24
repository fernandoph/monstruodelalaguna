from pathlib import Path

import pygame

from settings import PLACEHOLDER_SURFACE_SIZE, PROJECT_ROOT


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"}


def resolve_project_path(path):
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return PROJECT_ROOT / candidate


def create_placeholder_surface(
    size=PLACEHOLDER_SURFACE_SIZE,
    fill_color=(255, 0, 255),
    border_color=(32, 32, 32),
):
    width, height = size
    surface = pygame.Surface((max(1, width), max(1, height)), pygame.SRCALPHA)
    surface.fill(fill_color)
    pygame.draw.rect(surface, border_color, surface.get_rect(), 4)
    return surface


def load_image(path, fallback_size=PLACEHOLDER_SURFACE_SIZE, fallback_color=(255, 0, 255)):
    image_path = resolve_project_path(path)
    if not image_path.is_file():
        return create_placeholder_surface(fallback_size, fill_color=fallback_color)

    try:
        surface = pygame.image.load(str(image_path))
    except pygame.error:
        return create_placeholder_surface(fallback_size, fill_color=fallback_color)

    if pygame.display.get_surface() is not None:
        return surface.convert_alpha()
    return surface


def import_folder(path, fallback_size=PLACEHOLDER_SURFACE_SIZE, fallback_color=(255, 0, 255)):
    directory = resolve_project_path(path)
    surface_list = []

    if directory.is_dir():
        for image_path in sorted(directory.iterdir()):
            if image_path.suffix.lower() not in IMAGE_EXTENSIONS or not image_path.is_file():
                continue
            surface_list.append(
                load_image(
                    image_path,
                    fallback_size=fallback_size,
                    fallback_color=fallback_color,
                )
            )

    if not surface_list:
        surface_list.append(create_placeholder_surface(fallback_size, fill_color=fallback_color))

    return surface_list


def load_animation_set(
    base_path,
    animation_names,
    fallback_size=PLACEHOLDER_SURFACE_SIZE,
    fallback_colors=None,
):
    animations = {}
    fallback_colors = fallback_colors or {}

    for animation_name in animation_names:
        animations[animation_name] = import_folder(
            resolve_project_path(base_path) / animation_name,
            fallback_size=fallback_size,
            fallback_color=fallback_colors.get(animation_name, (255, 0, 255)),
        )

    return animations
