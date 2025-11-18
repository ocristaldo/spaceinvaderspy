"""Centralized font management for UI elements and overlays."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict, Tuple

import pygame
from pygame import font as pg_font

from .. import config

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class FontSpec:
    """Immutable description of a reusable font profile."""

    name: str | None = "monospace"
    size: int = 16
    bold: bool = False
    min_size: int | None = None
    max_size: int | None = None
    scale_with_playfield: bool = False


FONT_PROFILES: Dict[str, FontSpec] = {
    # Menu chrome
    "menu_title": FontSpec(size=14, bold=True, min_size=18, scale_with_playfield=True),
    "menu_body": FontSpec(size=12, min_size=14, scale_with_playfield=True),
    # Menu overlays (section-specific)
    "menu_controls_main": FontSpec(name=None, size=12, min_size=12, scale_with_playfield=True),
    "menu_controls_hint": FontSpec(name=None, size=11, min_size=11),
    "menu_high_scores_main": FontSpec(size=18),
    "menu_high_scores_hint": FontSpec(size=18),
    "menu_options_main": FontSpec(size=16),
    "menu_options_hint": FontSpec(size=16),
    "menu_credits_main": FontSpec(size=16),
    "menu_credits_hint": FontSpec(size=16),
    # In-game HUD
    "hud_main": FontSpec(size=16),
    "hud_small": FontSpec(size=12),
    # Intro demos
    "demo_title": FontSpec(size=30, bold=True),
    "demo_subtitle": FontSpec(size=18),
    "demo_entry": FontSpec(size=16),
    "demo_prompt": FontSpec(size=14),
    "wave_info": FontSpec(size=14),
    # Sprite viewer overlays
    "spriteviewer_title": FontSpec(size=20, bold=True),
    "spriteviewer_small": FontSpec(size=14),
    "spriteviewer_tiny": FontSpec(size=12),
    "spriteviewer_stage_title": FontSpec(size=36, bold=True),
    "spriteviewer_stage_subtitle": FontSpec(size=20),
    "spriteviewer_stage_score": FontSpec(size=18),
    "spriteviewer_stage_info": FontSpec(size=20),
}

MENU_OVERLAY_FONT_SECTIONS: Dict[str, Tuple[str, str]] = {
    "controls": ("menu_controls_main", "menu_controls_hint"),
    "high_scores": ("menu_high_scores_main", "menu_high_scores_hint"),
    "options": ("menu_options_main", "menu_options_hint"),
    "credits": ("menu_credits_main", "menu_credits_hint"),
}

pygame.font.init()
_cache: Dict[str, pygame.font.Font] = {}


def _resolve_size(spec: FontSpec) -> int:
    size = spec.size
    if spec.scale_with_playfield:
        size = int(size * config.PLAYFIELD_SCALE)
    if spec.min_size is not None:
        size = max(spec.min_size, size)
    if spec.max_size is not None:
        size = min(spec.max_size, size)
    return max(1, size)


def _build_font(spec: FontSpec) -> pygame.font.Font:
    size = _resolve_size(spec)
    matched = pg_font.match_font(spec.name or "", bold=spec.bold) if spec.name else None
    try:
        font = pg_font.Font(matched, size)
    except Exception as exc:  # pragma: no cover - defensive fallback
        logger.warning("Falling back to default font. spec=%s error=%s", spec, exc)
        font = pg_font.Font(None, size)
        if spec.bold:
            font.set_bold(True)
    return font


def get_font(profile: str) -> pygame.font.Font:
    """Return a pygame Font for the given profile name."""
    if profile not in FONT_PROFILES:
        logger.error("Unknown font profile requested: %s", profile)
        raise KeyError(f"Unknown font profile: {profile}")
    if profile not in _cache:
        spec = FONT_PROFILES[profile]
        _cache[profile] = _build_font(spec)
        logger.debug(
            "Loaded font profile '%s' (size=%d bold=%s)",
            profile,
            _cache[profile].get_height(),
            spec.bold,
        )
    return _cache[profile]


def get_menu_overlay_fonts(section: str) -> Tuple[pygame.font.Font, pygame.font.Font]:
    """Return the headline + hint fonts for a specific menu overlay section."""
    section_key = section.lower()
    if section_key not in MENU_OVERLAY_FONT_SECTIONS:
        logger.error("Unknown menu overlay section requested: %s", section)
        raise KeyError(f"Unknown overlay section: {section}")
    main_profile, hint_profile = MENU_OVERLAY_FONT_SECTIONS[section_key]
    return get_font(main_profile), get_font(hint_profile)
