"""Utility helpers for rendering numeric strings via sprite digits."""
from __future__ import annotations

import pygame
from typing import Dict

from .. import config
from ..utils.sprite_sheet import get_game_sprite
from .color_scheme import get_color, get_tint


class SpriteDigitWriter:
    def __init__(self, scale: int | None = None, tint_enabled: bool = False):
        self.scale = scale or config.SPRITE_SCALE
        tint = get_tint('digit') if tint_enabled else None
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
        surface = pygame.Surface((max(1, width), max_height), pygame.SRCALPHA)
        x = 0
        for surf in pieces:
            surface.blit(surf, (x, max_height - surf.get_height()))
            x += surf.get_width()
        return surface
