"""Centralized font configuration for UI screens."""
import pygame
from pygame import font as pg_font


FONT_PROFILES = {
    "menu_title": {"name": "monospace", "size": 28, "bold": True},
    "menu_body": {"name": "monospace", "size": 16, "bold": False},
    "menu_Options_controls": {"name": "monospace", "size": 16, "bold": False},
    "menu_Options_high_scores": {"name": "monospace", "size": 16, "bold": False},
    "menu_Options_credits": {"name": "monospace", "size": 16, "bold": False},
    "menu_Options_options": {"name": "monospace", "size": 16, "bold": False},
    "demo_title": {"name": "monospace", "size": 30, "bold": True},
    "demo_subtitle": {"name": "monospace", "size": 18, "bold": False},
    "demo_entry": {"name": "monospace", "size": 16, "bold": False},
    "demo_prompt": {"name": "monospace", "size": 14, "bold": False},
    "wave_info": {"name": "monospace", "size": 14, "bold": False},
}


pygame.font.init()
_cache = {}


def _build_font(spec):
    name = spec.get("name")
    size = spec.get("size", 16)
    bold = spec.get("bold", False)
    matched = pg_font.match_font(name or "", bold=bold) if name else None
    try:
        font = pg_font.Font(matched, size)
    except Exception:
        font = pg_font.Font(None, size)
        if bold:
            font.set_bold(True)
    return font


def get_font(profile: str) -> pygame.font.Font:
    """Return a pygame Font for the given profile name."""
    if profile not in FONT_PROFILES:
        raise KeyError(f"Unknown font profile: {profile}")
    if profile not in _cache:
        spec = FONT_PROFILES[profile]
        _cache[profile] = _build_font(spec)
    return _cache[profile]
