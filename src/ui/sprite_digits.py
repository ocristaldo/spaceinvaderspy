"""Utility helpers for rendering numeric strings via sprite digits or font digits."""
from __future__ import annotations

import pygame
from typing import Dict

from .. import config
from ..utils.sprite_sheet import get_game_sprite
from .color_scheme import get_color, get_tint


class SpriteDigitWriter:
    """Renders digits using sprite sheet images (legacy)."""
    def __init__(self, scale: int | None = None, tint_enabled: bool = False):
        self.scale = scale or config.SPRITE_SCALE
        tint = get_tint('digit') if tint_enabled else None
        self.digit_spacing = 1  # Small buffer so digits don't touch each other
        self.digits: Dict[str, pygame.Surface] = {}
        for value in range(8):
            sprite_name = f'digit_{value}'
            tint_color = tint if tint is not None else None
            self.digits[str(value)] = get_game_sprite(sprite_name, self.scale, tint=tint_color)
        self.font = pygame.font.SysFont('monospace', 14)
        self.font_color = get_color('hud_text')

    def render(self, text: str) -> pygame.Surface:
        pieces = []
        max_height = 0
        for ch in text:
            surf = self.digits.get(ch)
            if not surf:
                surf = self.font.render(ch, True, self.font_color)
            pieces.append(surf)
            max_height = max(max_height, surf.get_height())
        width = sum(s.get_width() for s in pieces)
        if pieces:
            width += self.digit_spacing * (len(pieces) - 1)
        surface = pygame.Surface((max(1, width), max_height), pygame.SRCALPHA)
        x = 0
        for surf in pieces:
            surface.blit(surf, (x, max_height - surf.get_height()))
            x += surf.get_width() + self.digit_spacing
        return surface


class FontDigitWriter:
    """Renders digits using monospace font (matches sprite digit size)."""
    def __init__(self, font_size: int | None = None, color: tuple | None = None):
        """
        Initialize font digit writer.

        Args:
            font_size: Font size in pixels (default: 14 to match sprite digits)
            color: RGB color tuple (default: hud_text color)
        """
        self.font_size = font_size or 14
        self.font = pygame.font.SysFont('courier', self.font_size, bold=True)
        self.color = color or get_color('hud_text')
        self.digit_spacing = 2  # Small spacing between digits for readability

    def render(self, text: str) -> pygame.Surface:
        """Render text string as digits."""
        pieces = []
        max_height = 0

        for ch in text:
            # Render each character
            surf = self.font.render(ch, True, self.color)
            pieces.append(surf)
            max_height = max(max_height, surf.get_height())

        if not pieces:
            return pygame.Surface((0, 0), pygame.SRCALPHA)

        # Calculate total width
        width = sum(s.get_width() for s in pieces)
        width += self.digit_spacing * (len(pieces) - 1)

        # Create combined surface
        surface = pygame.Surface((max(1, width), max_height), pygame.SRCALPHA)
        x = 0
        for surf in pieces:
            surface.blit(surf, (x, max_height - surf.get_height()))
            x += surf.get_width() + self.digit_spacing

        return surface
