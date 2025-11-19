"""Bullet and bomb entities - projectiles in the game."""
from typing import Tuple

import pygame

from .. import config, constants
from ..utils.logger import setup_logger


class Bullet(pygame.sprite.Sprite):
    """
    Player bullet projectile.

    Bullets are fired by the player and travel upward to destroy aliens.
    Only one bullet can be active at a time in classic Space Invaders.
    """

    def __init__(self, pos: Tuple[int, int]):
        """
        Initialize a player bullet.

        Args:
            pos: Starting position (x, y) for the bullet
        """
        super().__init__()
        self.logger = setup_logger(__name__)
        try:
            # Load bullet sprite from sprite sheet
            from ..utils.sprite_sheet import get_game_sprite
            self.image = get_game_sprite('bullet', config.SPRITE_SCALE)
        except Exception:
            # Fallback to simple rectangle
            self.image = pygame.Surface((2, 8))
            self.image.fill(constants.WHITE)

        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = config.BULLET_SPEED

    def update(self) -> None:
        """Update bullet position and remove if off-screen."""
        self.rect.y += config.BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()


class Bomb(pygame.sprite.Sprite):
    """
    Alien bomb projectile.

    Bombs are dropped by aliens and travel downward toward the player.
    Multiple bombs can be active simultaneously.
    """

    def __init__(self, pos: Tuple[int, int], sprite_name: str = 'bomb_1', tint=None):
        """
        Initialize an alien bomb.

        Args:
            pos: Starting position (x, y) for the bomb
            sprite_name: Sprite identifier (aliens use `bomb_1`, UFOs use `bomb_2`)
        """
        super().__init__()
        self.logger = setup_logger(__name__)
        try:
            # Load bomb sprite from sprite sheet
            from ..utils.sprite_sheet import get_game_sprite
            self.image = get_game_sprite(sprite_name, config.SPRITE_SCALE, tint=tint)
        except Exception:
            # Fallback to simple rectangle
            self.image = pygame.Surface((2, 8))
            self.image.fill(constants.RED)
        # Use center-based placement so callers can pass a logical position
        # (e.g., player's center or alien midbottom) and get a predictable rect.
        self.rect = self.image.get_rect(center=pos)
        self.speed = config.BOMB_SPEED

    def update(self) -> None:
        """Update bomb position and remove if off-screen."""
        self.rect.y += config.BOMB_SPEED
        if self.rect.top > config.BASE_HEIGHT:
            self.kill()
