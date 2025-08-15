"""
Sprite viewer utility for testing and displaying sprites from different platforms.

This module provides functionality to display all sprites from a specific platform
(arcade, atari, deluxe, intellivision) in a grid layout for testing purposes.
"""
import pygame
import json
import os
from typing import Dict, List, Optional, Tuple
from .sprite_sheet import SpriteSheet
from .logger import setup_logger
from .. import config


class SpriteViewer:
    """
    Handles displaying sprites from different platforms for testing purposes.
    """
    
    def __init__(self, screen: pygame.Surface):
        """
        Initialize the sprite viewer.
        
        Args:
            screen: The pygame screen surface to draw on
        """
        self.screen = screen
        self.logger = setup_logger(__name__)
        self.font = pygame.font.Font(None, 20)
        self.small_font = pygame.font.Font(None, 14)
        self.tiny_font = pygame.font.Font(None, 12)
        
        # Platform configurations
        self.platforms = {
            'arcade': {
                'name': 'Arcade',
                'json_file': 'SpaceInvaders.arcade.json',
                'title_color': (255, 255, 0),  # Yellow
            },
            'atari': {
                'name': 'Atari 2600',
                'json_file': 'SpaceInvaders.atari.json',
                'title_color': (255, 100, 100),  # Light red
            },
            'deluxe': {
                'name': 'Atari 2600 Deluxe',
                'json_file': 'SpaceInvaders.deluxe.json',
                'title_color': (100, 255, 100),  # Light green
            },
            'intellivision': {
                'name': 'Intellivision',
                'json_file': 'SpaceInvaders.intellivision.json',
                'title_color': (100, 100, 255),  # Light blue
            }
        }
        
        self.current_platform = None
        self.sprites_data = []
        self.sprite_sheet = None
        self.current_page = 0
        self.sprites_per_page = 12  # 3 rows x 4 columns for better spacing
        
        # Key debouncing variables
        self.last_key_time = 0
        self.key_debounce_delay = 200  # milliseconds between key presses
    
    def load_platform_sprites(self, platform: str) -> bool:
        """
        Load sprites for a specific platform.
        
        Args:
            platform: Platform name ('arcade', 'atari', 'deluxe', 'intellivision')
            
        Returns:
            True if successful, False otherwise
        """
        if platform not in self.platforms:
            self.logger.error(f"Unknown platform: {platform}")
            return False
        
        platform_config = self.platforms[platform]
        json_path = os.path.join(config.IMG_DIR, platform_config['json_file'])
        sprite_sheet_path = os.path.join(config.IMG_DIR, 'SpaceInvaders.png')
        
        try:
            # Load sprite sheet with JSON coordinates
            self.sprite_sheet = SpriteSheet(sprite_sheet_path, json_path)
            
            # Load JSON data for display
            with open(json_path, 'r') as f:
                self.sprites_data = json.load(f)
            
            self.current_platform = platform
            self.current_page = 0  # Reset to first page when switching platforms
            self.logger.info(f"Loaded {len(self.sprites_data)} sprites for {platform_config['name']}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load {platform} sprites: {e}")
            return False
    
    def draw_sprite_grid(self) -> None:
        """Draw all sprites in a paginated grid layout with detailed information."""
        if not self.current_platform or not self.sprites_data:
            return
        
        # Clear screen
        self.screen.fill((20, 20, 40))  # Dark blue background
        
        platform_config = self.platforms[self.current_platform]
        total_sprites = len(self.sprites_data)
        total_pages = (total_sprites + self.sprites_per_page - 1) // self.sprites_per_page
        
        # Draw title with page info
        title_text = f"{platform_config['name']} Sprites ({total_sprites} total) - Page {self.current_page + 1}/{total_pages}"
        title_surface = self.font.render(title_text, True, platform_config['title_color'])
        title_rect = title_surface.get_rect(centerx=config.SCREEN_WIDTH // 2, y=8)
        self.screen.blit(title_surface, title_rect)
        
        # Instructions
        instruction_text = "S+1/2/3/4: Switch platforms | ←→: Navigate pages | R: Return to game"
        instruction_surface = self.tiny_font.render(instruction_text, True, (200, 200, 200))
        instruction_rect = instruction_surface.get_rect(centerx=config.SCREEN_WIDTH // 2, y=28)
        self.screen.blit(instruction_surface, instruction_rect)
        
        # Grid layout parameters
        start_y = 50
        cols = 4  # Number of columns (reduced for more space)
        rows = 3  # Number of rows
        col_width = config.SCREEN_WIDTH // cols
        row_height = (config.SCREEN_HEIGHT - start_y - 20) // rows
        scale = 2  # Scale factor for sprites
        
        # Calculate sprites for current page
        start_idx = self.current_page * self.sprites_per_page
        end_idx = min(start_idx + self.sprites_per_page, total_sprites)
        page_sprites = self.sprites_data[start_idx:end_idx]
        
        # Draw sprites in grid
        for i, sprite_data in enumerate(page_sprites):
            col = i % cols
            row = i // cols
            
            x = col * col_width + col_width // 2
            y = start_y + row * row_height + row_height // 2
            
            try:
                # Get sprite
                sprite_name = sprite_data['name']
                sprite_surface = self.sprite_sheet.get_sprite_by_name(sprite_name, scale)
                
                # Center sprite in cell
                sprite_rect = sprite_surface.get_rect(center=(x, y - 30))
                self.screen.blit(sprite_surface, sprite_rect)
                
                # Draw sprite number
                sprite_num = start_idx + i + 1
                num_text = f"#{sprite_num}"
                num_surface = self.small_font.render(num_text, True, (255, 255, 100))
                num_rect = num_surface.get_rect(center=(x, y - 60))
                self.screen.blit(num_surface, num_rect)
                
                # Draw sprite name (truncated if too long)
                display_name = sprite_name
                if len(display_name) > 18:
                    display_name = display_name[:15] + "..."
                
                name_surface = self.tiny_font.render(display_name, True, (255, 255, 255))
                name_rect = name_surface.get_rect(center=(x, y + 15))
                self.screen.blit(name_surface, name_rect)
                
                # Draw coordinates
                coords_text = f"({sprite_data['x']}, {sprite_data['y']})"
                coords_surface = self.tiny_font.render(coords_text, True, (150, 200, 255))
                coords_rect = coords_surface.get_rect(center=(x, y + 28))
                self.screen.blit(coords_surface, coords_rect)
                
                # Draw dimensions
                dims_text = f"{sprite_data['width']}×{sprite_data['height']}"
                dims_surface = self.tiny_font.render(dims_text, True, (150, 255, 150))
                dims_rect = dims_surface.get_rect(center=(x, y + 41))
                self.screen.blit(dims_surface, dims_rect)
                
            except Exception as e:
                self.logger.warning(f"Failed to draw sprite {sprite_data.get('name', 'unknown')}: {e}")
                
                # Draw error placeholder
                error_rect = pygame.Rect(x - 30, y - 40, 60, 60)
                pygame.draw.rect(self.screen, (255, 0, 255), error_rect)
                
                error_text = "ERROR"
                error_surface = self.tiny_font.render(error_text, True, (255, 255, 255))
                error_text_rect = error_surface.get_rect(center=(x, y + 15))
                self.screen.blit(error_surface, error_text_rect)
    
    def get_platform_from_key_combo(self, keys_pressed) -> Optional[str]:
        """
        Determine which platform to show based on key combination.
        
        Args:
            keys_pressed: pygame key state from pygame.key.get_pressed()
            
        Returns:
            Platform name or None if no valid combination
        """
        if keys_pressed[pygame.K_s]:
            if keys_pressed[pygame.K_1]:
                return 'arcade'
            elif keys_pressed[pygame.K_2]:
                return 'atari'
            elif keys_pressed[pygame.K_3]:
                return 'deluxe'
            elif keys_pressed[pygame.K_4]:
                return 'intellivision'
        
        return None
    
    def handle_navigation(self, keys_pressed) -> None:
        """
        Handle navigation keys for page switching and platform switching.
        
        Args:
            keys_pressed: pygame key state from pygame.key.get_pressed()
        """
        if not self.sprites_data:
            return
        
        current_time = pygame.time.get_ticks()
        
        # Check if enough time has passed since last key press (debouncing)
        if current_time - self.last_key_time < self.key_debounce_delay:
            return
        
        total_pages = (len(self.sprites_data) + self.sprites_per_page - 1) // self.sprites_per_page
        
        # Handle arrow key navigation for pages
        if keys_pressed[pygame.K_RIGHT] and self.current_page < total_pages - 1:
            self.current_page += 1
            self.last_key_time = current_time
        elif keys_pressed[pygame.K_LEFT] and self.current_page > 0:
            self.current_page -= 1
            self.last_key_time = current_time
