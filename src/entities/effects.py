"""Lightweight transient visual effects."""
from __future__ import annotations

import pygame

from .. import config
from ..utils.sprite_sheet import get_game_sprite


class ExplosionEffect(pygame.sprite.Sprite):
    """Simple animated explosion using arcade sprites."""

    def __init__(self, pos, tint=None, duration_ms: int = 300):
        super().__init__()
        self.frames = [
            get_game_sprite('explosion', config.SPRITE_SCALE, tint=tint),
            get_game_sprite('explosion_alt', config.SPRITE_SCALE, tint=tint),
        ]
        self.rect = self.frames[0].get_rect(center=pos)
        self.image = self.frames[0]
        self.start_time = pygame.time.get_ticks()
        self.duration = duration_ms
        self.frame_interval = duration_ms // len(self.frames) if duration_ms else 100

    def update(self) -> None:
        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed >= self.duration:
            self.kill()
            return
        index = min(len(self.frames) - 1, elapsed // max(1, self.frame_interval))
        self.image = self.frames[index]
