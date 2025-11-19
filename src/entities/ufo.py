"""UFO entity - bonus mystery ship that appears periodically."""
import random

import pygame

from .. import config, constants
from ..utils.logger import setup_logger


class UFO(pygame.sprite.Sprite):
    """
    UFO (mystery ship) that appears occasionally for bonus points.
    
    The UFO flies across the top of the screen at regular intervals
    and awards random bonus points when destroyed.
    """

    def __init__(self, x: int, y: int):
        """
        Initialize a UFO.
        
        Args:
            x: Starting X position
            y: Starting Y position
        """
        super().__init__()
        self.logger = setup_logger(__name__)
        try:
            # Load UFO sprite from sprite sheet
            from ..utils.sprite_sheet import get_game_sprite
            self.image = get_game_sprite('ufo', config.SPRITE_SCALE)
        except Exception:
            # Fallback to drawn UFO
            self.image = pygame.Surface((32, 16))
            self.image.fill((0, 0, 0, 0))  # Transparent background
            # Draw UFO as an ellipse
            pygame.draw.ellipse(self.image, constants.RED, (0, 0, 32, 16))
            pygame.draw.ellipse(self.image, constants.WHITE, (8, 4, 16, 8))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 2
        self.value = random.choice([50, 100, 150, 300])

    def update(self) -> None:
        """Update UFO position and remove when off-screen."""
        self.rect.x += self.speed
        # Remove UFO when it goes off screen
        if self.rect.right < 0 or self.rect.left > config.BASE_WIDTH:
            self.kill()
