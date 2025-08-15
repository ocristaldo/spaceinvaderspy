"""
Game Engine - Core game loop and coordination.
"""
import logging
import pygame
from typing import Optional

from ..utils.logger import setup_logger
from .. import config, constants


class GameEngine:
    """Main game engine responsible for initialization and core game loop."""
    
    def __init__(self):
        """Initialize the game engine."""
        self.logger = setup_logger(__name__)
        self.screen: Optional[pygame.Surface] = None
        self.clock: Optional[pygame.time.Clock] = None
        self.font: Optional[pygame.font.Font] = None
        self.running = False
        
        self._initialize_pygame()
        self.logger.info("Game engine initialized")
    
    def _initialize_pygame(self) -> None:
        """Initialize pygame and create display."""
        try:
            pygame.init()
            self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
            pygame.display.set_caption("Space Invaders")
            self.clock = pygame.time.Clock()
            self.font = pygame.font.SysFont("monospace", 16)
            self.logger.info("Pygame initialized successfully")
        except pygame.error as e:
            self.logger.error(f"Failed to initialize pygame: {e}")
            raise
    
    def start(self) -> None:
        """Start the game engine."""
        self.running = True
        self.logger.info("Game engine started")
    
    def stop(self) -> None:
        """Stop the game engine."""
        self.running = False
        self.logger.info("Game engine stopped")
    
    def cleanup(self) -> None:
        """Clean up resources."""
        pygame.quit()
        self.logger.info("Game engine cleaned up")
    
    def get_screen(self) -> pygame.Surface:
        """Get the game screen surface."""
        if self.screen is None:
            raise RuntimeError("Screen not initialized")
        return self.screen
    
    def get_clock(self) -> pygame.time.Clock:
        """Get the game clock."""
        if self.clock is None:
            raise RuntimeError("Clock not initialized")
        return self.clock
    
    def get_font(self) -> pygame.font.Font:
        """Get the game font."""
        if self.font is None:
            raise RuntimeError("Font not initialized")
        return self.font
