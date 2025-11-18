"""Alien entity - represents enemy invaders in the game."""
import pygame
from .. import constants
from .. import config
from ..utils.logger import setup_logger


class Alien(pygame.sprite.Sprite):
    """
    Alien invader sprite with animation and point values.
    
    Aliens move in formation and can drop bombs. Different alien types
    have different point values and sprite animations.
    """

    def __init__(self, x: int, y: int, value: int, tint=None):
        """
        Initialize an alien sprite.
        
        Args:
            x: X position on screen
            y: Y position on screen  
            value: Point value (30=squid, 20=crab, 10=octopus)
        """
        super().__init__()
        self.logger = setup_logger(__name__)
        self.value = value
        self.animation_frame = 0  # For sprite animation
        
        # Map point values to sprite names
        sprite_map = {
            30: 'alien_squid_1',    # Top row - highest points
            20: 'alien_crab_1',     # Middle row - medium points  
            10: 'alien_octopus_1'   # Bottom row - lowest points
        }
        
        try:
            # Load sprite from sprite sheet
            from ..utils.sprite_sheet import get_game_sprite
            sprite_name = sprite_map.get(value, 'alien_octopus_1')
            self.image = get_game_sprite(sprite_name, config.SPRITE_SCALE, tint=tint)
            
            # Store both animation frames for later use
            frame1_name = sprite_name
            frame2_name = sprite_name.replace('_1', '_2')
            self.frame1 = get_game_sprite(frame1_name, config.SPRITE_SCALE, tint=tint)
            self.frame2 = get_game_sprite(frame2_name, config.SPRITE_SCALE, tint=tint)
            
        except Exception as e:
            # Fallback to colored rectangles if sprite loading fails
            colors = {30: constants.GREEN, 20: constants.BLUE, 10: (255, 0, 255)}
            self.image = pygame.Surface((24, 16))
            self.image.fill(colors.get(value, constants.WHITE))
            self.frame1 = self.frame2 = self.image
            
            self.logger.warning(f"Could not load alien sprite for value {value}: {e}. Using fallback.")
        
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def animate(self) -> None:
        """Switch between animation frames for classic alien movement."""
        self.animation_frame = 1 - self.animation_frame  # Toggle between 0 and 1
        self.image = self.frame1 if self.animation_frame == 0 else self.frame2
