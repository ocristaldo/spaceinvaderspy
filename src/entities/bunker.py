"""Bunker entity - destructible cover for the player."""
import pygame
from typing import Tuple
from .. import constants
from .. import config
from ..utils.logger import setup_logger

class Bunker(pygame.sprite.Sprite):
    """
    Destructible bunker that provides cover for the player.
    
    Bunkers can be damaged by both player bullets and alien bombs.
    They provide strategic cover but deteriorate over time when hit.
    """

    def __init__(self, x: int, y: int):
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
                image = get_game_sprite(sprite_name, config.SCALE)
                self.images.append(image)
            self.image = self.images[0]
        except Exception as e:
            # Fallback to simple rectangle
            self.image = pygame.Surface((32 * config.SCALE, 24 * config.SCALE))
            self.image.fill(constants.GREEN)
            self.logger.warning(f"Could not load bunker sprite: {e}. Using fallback.")
        self.rect = self.image.get_rect(topleft=(x, y))

    def damage(self) -> None:
        """Reduce bunker health when hit by bullets or bombs."""
        self.health -= 1
        if self.health <= 0:
            self.kill()
            self.logger.debug(f"Bunker destroyed at {self.rect.topleft}")
        else:
            # Change color to show damage
            damage_colors = [constants.GREEN, (255, 255, 0), (255, 165, 0), constants.RED]
            color = damage_colors[min(3, 3 - self.health)]
            self.image.fill(color)
            self.logger.debug(f"Bunker damaged, health: {self.health}")
