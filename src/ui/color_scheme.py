"""Centralized color and tint configuration for the game HUD and sprites."""
from __future__ import annotations

default_theme = {
    "background": (0, 0, 0),
    "hud_text": (255, 255, 255),
    "score_text": (255, 255, 255),
    "credit_text": (255, 255, 0),
    "divider": (60, 60, 60),
    "wave_message": (255, 255, 255),
}

sprite_tints = {
    "player": (180, 255, 180),
    "life_icon": (120, 255, 120),
    "alien_squid": (120, 255, 120),
    "alien_crab": (120, 200, 255),
    "alien_octopus": (255, 255, 120),
    "ufo": (255, 120, 120),
    "bunker": (120, 255, 160),
    "bomb_1": (255, 255, 255),
    "bomb_2": (255, 200, 200),
    "explosion": (255, 180, 96),
    "explosion_alt": (255, 220, 160),
    "text_hi_score": (255, 255, 255),
    "text_credit": (255, 255, 0),
    "digit": (255, 255, 255),
}


def get_color(name: str) -> tuple[int, int, int]:
    """Return a configured RGB color name, falling back to white."""
    return tuple(default_theme.get(name, (255, 255, 255)))


def get_tint(name: str) -> tuple[int, int, int] | None:
    """Return a sprite tint color or None if no tint configured."""
    color = sprite_tints.get(name)
    return tuple(color) if color else None
