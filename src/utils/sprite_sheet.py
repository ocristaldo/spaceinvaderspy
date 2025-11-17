"""
Sprite sheet utility for extracting sprites from the main SpaceInvaders.png file.

This module handles loading and extracting individual sprites from the sprite sheet,
providing a centralized way to manage all game graphics using JSON coordinate data.
"""
import pygame
import os
import json
from typing import Dict, Optional
from .logger import setup_logger


class SpriteSheet:
    """
    Handles loading and extracting sprites from a sprite sheet using JSON coordinate data.
    
    The SpaceInvaders.png contains all game sprites in a grid layout.
    This class loads coordinate data from JSON files and extracts sprites accordingly.
    """
    
    def __init__(self, filename: str, json_filename: Optional[str] = None):
        """
        Initialize the sprite sheet loader.
        
        Args:
            filename: Path to the sprite sheet image file
            json_filename: Path to the JSON coordinate file (optional)
        """
        self.logger = setup_logger(__name__)
        self.filename = filename
        self.json_filename = json_filename
        self.sprite_sheet: Optional[pygame.Surface] = None
        self.sprite_coords: Dict = {}
        self._load_sprite_sheet()
        self._load_sprite_coordinates()
    
    def _load_sprite_sheet(self) -> None:
        """Load the sprite sheet image from file."""
        try:
            self.sprite_sheet = pygame.image.load(self.filename).convert_alpha()
            self.logger.info(f"Loaded sprite sheet: {self.filename}")
            self.logger.debug(f"Sprite sheet size: {self.sprite_sheet.get_size()}")
        except (pygame.error, FileNotFoundError, OSError) as e:
            self.logger.error(f"Failed to load sprite sheet {self.filename}: {e}")
            # Create a fallback surface
            self.sprite_sheet = pygame.Surface((256, 256), pygame.SRCALPHA)
            self.sprite_sheet.fill((255, 0, 255))  # Magenta for missing sprites
    
    def _load_sprite_coordinates(self) -> None:
        """Load sprite coordinates from JSON file."""
        if not self.json_filename:
            self.logger.debug("No JSON coordinate file specified, using fallback coordinates")
            return
        
        try:
            with open(self.json_filename, 'r') as f:
                sprite_data = json.load(f)
            
            # Convert list of sprite data to dictionary keyed by sprite name
            for sprite in sprite_data:
                name = sprite.get('name', '')
                self.sprite_coords[name] = {
                    'x': sprite.get('x', 0),
                    'y': sprite.get('y', 0),
                    'width': sprite.get('width', 16),
                    'height': sprite.get('height', 16),
                    'frame': sprite.get('frame')
                }
            
            self.logger.info(f"Loaded {len(self.sprite_coords)} sprite coordinates from {self.json_filename}")
            
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            self.logger.error(f"Failed to load sprite coordinates from {self.json_filename}: {e}")
            self.sprite_coords = {}
    
    def get_sprite_by_name(self, sprite_name: str, scale: int = 1) -> pygame.Surface:
        """
        Extract a sprite by name using JSON coordinate data.
        
        Args:
            sprite_name: Name of the sprite from the JSON file
            scale: Scale factor for the sprite (default: 1)
        
        Returns:
            pygame.Surface containing the extracted sprite
        """
        if sprite_name not in self.sprite_coords:
            self.logger.warning(f"Sprite '{sprite_name}' not found in coordinate data")
            # Return a fallback sprite
            sprite = pygame.Surface((16 * scale, 16 * scale), pygame.SRCALPHA)
            sprite.fill((255, 0, 255))  # Magenta for missing sprites
            return sprite
        
        coords = self.sprite_coords[sprite_name]
        return self.get_sprite(coords['x'], coords['y'], coords['width'], coords['height'], scale)
    
    def get_sprite(self, x: int, y: int, width: int, height: int, scale: int = 1) -> pygame.Surface:
        """
        Extract a sprite from the sprite sheet.
        
        Args:
            x: X coordinate of the sprite in the sheet
            y: Y coordinate of the sprite in the sheet
            width: Width of the sprite
            height: Height of the sprite
            scale: Scale factor for the sprite (default: 1)
        
        Returns:
            pygame.Surface containing the extracted sprite
        """
        if self.sprite_sheet is None:
            self.logger.error("Sprite sheet not loaded")
            # Return a fallback sprite
            sprite = pygame.Surface((width, height), pygame.SRCALPHA)
            sprite.fill((255, 0, 255))  # Magenta for missing sprites
            return sprite
        
        try:
            # Extract the sprite from the sheet
            sprite_rect = pygame.Rect(x, y, width, height)
            sprite = pygame.Surface((width, height), pygame.SRCALPHA)
            sprite.blit(self.sprite_sheet, (0, 0), sprite_rect)
            
            # Scale the sprite if requested
            if scale != 1:
                new_size = (width * scale, height * scale)
                sprite = pygame.transform.scale(sprite, new_size)
            
            return sprite
            
        except Exception as e:
            self.logger.error(f"Failed to extract sprite at ({x}, {y}, {width}, {height}): {e}")
            # Return a fallback sprite
            sprite = pygame.Surface((width * scale, height * scale), pygame.SRCALPHA)
            sprite.fill((255, 0, 255))  # Magenta for missing sprites
            return sprite


# Mapping from game entity names to arcade JSON sprite names
ARCADE_SPRITE_MAPPING = {
    # Player ship sprites
    'player': 'player_cannon_jumbo_arcade_frame1',
    # No explosion sprite in JSON, fallback to explosion_arcade_frame1
    'player_explosion': 'explosion_arcade_frame1',

    # Alien sprites (different types and animation frames)
    'alien_squid_1': 'invader_squid_jumbo_arcade_frame1',
    'alien_squid_2': 'invader_squid_jumbo_arcade_frame2',
    'alien_crab_1': 'invader_crab_jumbo_arcade_frame1',
    'alien_crab_2': 'invader_crab_jumbo_arcade_frame2',
    'alien_octopus_1': 'invader_octopus_jumbo_arcade_frame1',
    'alien_octopus_2': 'invader_octopus_jumbo_arcade_frame2',

    # UFO (mystery ship)
    'ufo': 'ufo_jumbo_arcade_frame1',

    # Projectiles
    'bullet': 'projectile_player_missile_arcade',
    'bomb_1': 'projectile_enemy_bomb_arcade_variant1',
    'bomb_2': 'projectile_enemy_bomb_arcade_variant2',
    'bomb_3': 'projectile_enemy_bomb_arcade_variant3',

    # Bunker pieces (for destructible bunkers)
    'bunker_full': 'barricade_arcade_full',
    'bunker_damaged_1': 'barricade_arcade_full',  # No damaged variants in JSON
    'bunker_damaged_2': 'barricade_arcade_full',
    'bunker_damaged_3': 'barricade_arcade_full',

    # Explosion sprites
    'explosion': 'explosion_arcade_frame1',

    # UI elements
    'title_logo': 'title_logo_marquee',
}


def _get_shared_sprite_sheet() -> SpriteSheet:
    """Return the shared sprite sheet instance used by helper functions."""
    if not hasattr(_get_shared_sprite_sheet, "_sheet"):
        from .. import config
        sprite_sheet_path = os.path.join(config.IMG_DIR, 'SpaceInvaders.png')
        json_path = os.path.join(config.IMG_DIR, 'SpaceInvaders.arcade.json')
        _get_shared_sprite_sheet._sheet = SpriteSheet(sprite_sheet_path, json_path)
    return _get_shared_sprite_sheet._sheet


def get_game_sprite(sprite_name: str, scale: int = 2) -> pygame.Surface:
    """
    Get a specific game sprite by name using arcade JSON coordinates.
    
    Args:
        sprite_name: Name of the sprite (key in ARCADE_SPRITE_MAPPING)
        scale: Scale factor for the sprite
    
    Returns:
        pygame.Surface containing the requested sprite
    """
    sheet = _get_shared_sprite_sheet()
    
    arcade_sprite_name = ARCADE_SPRITE_MAPPING.get(sprite_name)
    if not arcade_sprite_name:
        logger = setup_logger(__name__)
        logger.warning(f"Unknown sprite name: {sprite_name}")
        placeholder = pygame.Surface((16 * scale, 16 * scale), pygame.SRCALPHA)
        placeholder.fill((255, 0, 255))
        return placeholder
    
    return sheet.get_sprite_by_name(arcade_sprite_name, scale)


def get_title_logo(scale: int = 1) -> pygame.Surface:
    """Return the marquee logo sprite for menus/intro screens."""
    return get_game_sprite('title_logo', scale)
