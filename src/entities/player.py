"""
Player entity - represents the player's spaceship.
"""
import pygame
from typing import Any
from .. import constants
from .. import config
from ..utils.logger import setup_logger


class Player(pygame.sprite.Sprite):
    """
    Player spaceship entity.
    
    The player ship can move left and right and fire bullets.
    It has collision detection and proper boundary checking.
    """

    def __init__(self):
        """Initialize the player spaceship."""
        super().__init__()
        self.logger = setup_logger(__name__)
        
        try:
            self._create_sprite()
            self._initialize_position()
            self.speed = 5
            self.logger.debug("Player initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize player: {e}")
            raise
    
    def _create_sprite(self) -> None:
        """Create the player sprite graphics using the sprite sheet."""
        try:
            from ..utils.sprite_sheet import get_game_sprite
            self.image = get_game_sprite('player', config.SCALE)
            self.logger.debug("Loaded player sprite from sprite sheet")
        except Exception as e:
            self.logger.warning(f"Failed to load player sprite from sheet: {e}. Using fallback.")
            # Fallback to drawn sprite
            self.image = pygame.Surface((22, 16), pygame.SRCALPHA)
            self.image.fill((0, 0, 0, 0))  # Transparent background
            
            # Draw a simple spaceship shape
            points = [
                (11, 0),   # Top center
                (6, 8),    # Left wing
                (8, 8),    # Left body
                (8, 16),   # Left bottom
                (14, 16),  # Right bottom
                (14, 8),   # Right body
                (16, 8),   # Right wing
            ]
            pygame.draw.polygon(self.image, constants.WHITE, points)
    
    def _initialize_position(self) -> None:
        """Set the initial position of the player."""
        self.rect = self.image.get_rect(
            midbottom=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 20)
        )

    def update(self, pressed: Any) -> None:
        """
        Update player position based on input.
        
        Args:
            pressed: Pygame key state object
        """
        try:
            if pressed[pygame.K_LEFT]:
                self.rect.x -= self.speed
            if pressed[pygame.K_RIGHT]:
                self.rect.x += self.speed
            
            # Keep player within screen bounds
            self.rect.clamp_ip(pygame.Rect(0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        except Exception as e:
            self.logger.error(f"Error updating player: {e}")
    
    def get_bullet_spawn_position(self) -> tuple:
        """Get the position where bullets should spawn."""
        return self.rect.midtop
