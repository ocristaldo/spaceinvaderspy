"""Bunker entity - destructible cover for the player."""
import pygame

from .. import config, constants
from ..utils.logger import setup_logger


class Bunker(pygame.sprite.Sprite):
    """
    Destructible bunker that provides cover for the player.

    Bunkers can be damaged by both player bullets and alien bombs.
    They provide strategic cover but deteriorate over time when hit.
    """

    def __init__(self, x: int, y: int, tint=None):
        """
        Initialize a bunker.

        Args:
            x: X position on screen
            y: Y position on screen
        """
        super().__init__()
        self.logger = setup_logger(__name__)
        self.health = 4
        self.images = []

        try:
            # Load bunker sprites from sprite sheet
            from ..utils.sprite_sheet import get_game_sprite
            bunker_sprites = ['bunker_full', 'bunker_damaged_1', 'bunker_damaged_2', 'bunker_damaged_3']
            for sprite_name in bunker_sprites:
                image = get_game_sprite(sprite_name, config.SPRITE_SCALE, tint=tint)
                self.images.append(image)
            self.image = self.images[0]
            self.base_image = self.image.copy()
        except Exception as e:
            # Fallback to simple rectangle
            self.image = pygame.Surface((32 * config.SPRITE_SCALE, 24 * config.SPRITE_SCALE))
            self.image.fill(constants.GREEN)
            self.logger.warning(f"Could not load bunker sprite: {e}. Using fallback.")
            self.base_image = self.image.copy()
        self.rect = self.image.get_rect(midbottom=(x, y))

    def damage(self) -> None:
        """Reduce bunker health when hit by bullets or bombs."""
        self.health -= 1
        if self.health <= 0:
            self.kill()
            self.logger.debug(f"Bunker destroyed at {self.rect.topleft}")
        else:
            # Tint the bunker instead of wiping the sprite
            damage_ratio = self.health / 4
            tint_value = int(80 + 175 * damage_ratio)
            tinted = self.base_image.copy()
            tint_color = (tint_value, tint_value, tint_value, 255)
            tinted.fill(tint_color, special_flags=pygame.BLEND_RGBA_MULT)
            self.image = tinted
            self.logger.debug(f"Bunker damaged, health: {self.health}")
