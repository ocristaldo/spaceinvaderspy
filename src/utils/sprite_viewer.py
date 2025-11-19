"""
Sprite viewer utility for testing and displaying sprites from different platforms.

This module provides functionality to display all sprites from a specific platform
(arcade, atari, deluxe, intellivision) in a grid layout for testing purposes.
"""
import json
import os
from typing import Dict, Optional

import pygame

from .. import config, constants
from ..ui.font_manager import get_font
from .logger import setup_logger
from .sprite_sheet import SpriteSheet, get_game_sprite


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
        self.font = get_font("spriteviewer_title")
        self.small_font = get_font("spriteviewer_small")
        self.tiny_font = get_font("spriteviewer_tiny")

        # Platform configurations
        # Only Arcade platform is supported (S+1). Other platforms removed by user request.
        self.platforms = {
            'arcade': {
                'name': 'Arcade',
                'json_file': 'SpaceInvaders.arcade.json',
                'title_color': (255, 255, 0),  # Yellow
                'hotkey': pygame.K_1,
            }
        }

        self.current_platform = None
        self.sprites_data = []
        self.sprite_sheet = None
        self.current_page = 0
        self.sprites_per_page = 12  # 3 rows x 4 columns for better spacing
        self.stage_surface: Optional[pygame.Surface] = None
        self.stage_meta: Optional[Dict] = None
        self.current_stage: Optional[str] = None
        self.stage_cache: Dict[str, pygame.Surface] = {}
        self.sprite_cache: Dict[str, pygame.Surface] = {}
        self.stage_previews = {
            'start_screen': {
                'name': 'Start Screen',
                'description': 'Title, score advance table, and credit prompt.',
                'hotkey': pygame.K_2,
            },
            'wave_ready': {
                'name': 'Wave Ready',
                'description': 'Player, bunkers, and full alien formation at the start of a level.',
                'hotkey': pygame.K_3,
            },
            'late_wave': {
                'name': 'Late Wave',
                'description': 'Aliens near the bunkers with bombs raining down.',
                'hotkey': pygame.K_4,
            },
        }
        self.stage_renderers = {
            'start_screen': self._render_start_screen_scene,
            'wave_ready': self._render_wave_ready_scene,
            'late_wave': self._render_late_wave_scene,
        }

        # Key debouncing variables
        self.last_key_time = 0
        self.key_debounce_delay = 200  # milliseconds between key presses
        # Prune platform configs where the required JSON file is absent (avoid crash on missing assets)
        for key in list(self.platforms.keys()):
            json_file = os.path.join(config.IMG_DIR, self.platforms[key]['json_file'])
            if not os.path.isfile(json_file):
                self.logger.warning("Platform '%s' unavailable (missing JSON: %s)", key, json_file)
                del self.platforms[key]

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

        self.clear_stage_preview()
        platform_config = self.platforms[platform]
        json_path = os.path.join(config.IMG_DIR, platform_config['json_file'])
        sprite_sheet_path = os.path.join(config.IMG_DIR, 'SpaceInvaders.png')

        # Validate JSON file exists
        if not os.path.isfile(json_path):
            self.logger.error("Sprite JSON file for platform '%s' not found (%s).", platform, json_path)
            return False

        try:
            # Load sprite sheet with JSON coordinates
            self.sprite_sheet = SpriteSheet(sprite_sheet_path, json_path)

            # Load JSON data for display
            with open(json_path, 'r') as f:
                self.sprites_data = json.load(f)

            self.current_platform = platform
            self.current_page = 0  # Reset to first page when switching platforms
            self.logger.info("Loaded %d sprites for %s", len(self.sprites_data), platform_config['name'])
            return True
        except Exception as e:
            self.logger.error("Failed to load %s sprites: %s", platform, e)
            return False

    def draw_sprite_grid(self) -> None:
        """Draw all sprites in a paginated grid layout with detailed information."""
        if self.stage_surface:
            self.draw_stage_preview()
            return

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
        surface_width, surface_height = self.screen.get_size()

        title_rect = title_surface.get_rect(centerx=surface_width // 2, y=8)
        self.screen.blit(title_surface, title_rect)

        # Instructions
        instruction_text = "S+1: Arcade | S+2/3/4: Stage previews | ←→: Navigate pages | R: Return to game"
        instruction_surface = self.tiny_font.render(instruction_text, True, (200, 200, 200))
        instruction_rect = instruction_surface.get_rect(centerx=surface_width // 2, y=28)
        self.screen.blit(instruction_surface, instruction_rect)

        # Grid layout parameters
        start_y = 50
        cols = 4  # Number of columns (reduced for more space)
        rows = 3  # Number of rows
        col_width = surface_width // cols
        row_height = (surface_height - start_y - 20) // rows
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
        if not keys_pressed[pygame.K_s]:
            return None

        # Check configured platform hotkeys (only among available platforms)
        for key, cfg in self.platforms.items():
            hotkey = cfg.get('hotkey')
            if hotkey is not None and keys_pressed[hotkey]:
                return key

        return None

    def get_stage_from_key_combo(self, keys_pressed) -> Optional[str]:
        """Return the stage preview key if S plus one of the stage hotkeys is pressed."""
        if not keys_pressed[pygame.K_s]:
            return None
        for key, data in self.stage_previews.items():
            if keys_pressed[data['hotkey']]:
                return key
        return None

    def handle_navigation(self, keys_pressed) -> None:
        """
        Handle navigation keys for page switching and platform switching.
        
        Args:
            keys_pressed: pygame key state from pygame.key.get_pressed()
        """
        if self.stage_surface:
            return

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

    def load_stage_preview(self, stage_key: str) -> bool:
        """Render a mock stage using the real sprites so we can compare against references."""
        renderer = self.stage_renderers.get(stage_key)
        meta = self.stage_previews.get(stage_key)
        if not renderer or not meta:
            self.logger.error("Unknown stage preview: %s", stage_key)
            return False
        try:
            surface = self.stage_cache.get(stage_key)
            if surface is None:
                surface = renderer()
                self.stage_cache[stage_key] = surface
            self.stage_surface = surface.copy()
            self.stage_meta = meta
            self.current_stage = stage_key
            self.current_platform = None
            self.sprites_data = []
            self.sprite_sheet = None
            self.current_page = 0
            return True
        except Exception as exc:
            self.logger.error("Failed to build stage preview %s: %s", stage_key, exc)
            return False

    def clear_stage_preview(self):
        """Clear any loaded stage preview."""
        self.stage_surface = None
        self.stage_meta = None
        self.current_stage = None

    def draw_stage_preview(self):
        """Render the current stage preview on screen."""
        if not self.stage_surface or not self.stage_meta:
            return
        surface_width, surface_height = self.screen.get_size()
        image_rect = self.stage_surface.get_rect()
        scale = min(
            surface_width / image_rect.width,
            surface_height / image_rect.height
        )
        scaled_size = (
            max(1, int(image_rect.width * scale)),
            max(1, int(image_rect.height * scale)),
        )
        scaled = pygame.transform.smoothscale(self.stage_surface, scaled_size)
        x = (surface_width - scaled_size[0]) // 2
        y = (surface_height - scaled_size[1]) // 2
        self.screen.fill((5, 5, 5))
        self.screen.blit(scaled, (x, y))

        caption = self.font.render(self.stage_meta['name'], True, (255, 255, 0))
        self.screen.blit(caption, caption.get_rect(center=(surface_width // 2, 10 + caption.get_height() // 2)))

        description_lines = [
            self.stage_meta['description'],
            "Press R to return or choose another S+<number> command."
        ]
        for idx, text in enumerate(description_lines):
            line = self.small_font.render(text, True, (220, 220, 220))
            self.screen.blit(line, line.get_rect(center=(surface_width // 2, surface_height - 70 + idx * 18)))

    def reset_view(self):
        """Reset viewer state (used when exiting from the game)."""
        self.current_platform = None
        self.sprites_data = []
        self.sprite_sheet = None
        self.current_page = 0
        self.clear_stage_preview()

    # --- Stage preview rendering helpers -------------------------------------------------

    def _fetch_sprite(self, sprite_name: str) -> pygame.Surface:
        if sprite_name not in self.sprite_cache:
            self.sprite_cache[sprite_name] = get_game_sprite(sprite_name, config.SPRITE_SCALE)
        return self.sprite_cache[sprite_name]

    def _render_start_screen_scene(self) -> pygame.Surface:
        surface = pygame.Surface((config.BASE_WIDTH, config.BASE_HEIGHT), pygame.SRCALPHA)
        surface.fill((0, 0, 0))
        title_font = get_font("spriteviewer_stage_title")
        subtitle_font = get_font("spriteviewer_stage_subtitle")
        score_font = get_font("spriteviewer_stage_score")

        surface.blit(title_font.render("SPACE INVADERS", True, (255, 255, 255)),
                     (config.BASE_WIDTH // 2 - 150, 40))
        surface.blit(subtitle_font.render("SCORE ADVANCE TABLE", True, (255, 255, 0)),
                     (config.BASE_WIDTH // 2 - 150, 90))
        entries = [
            ('ufo', "? = MYSTERY"),
            ('alien_squid_1', "= 30 POINTS"),
            ('alien_crab_1', "= 20 POINTS"),
            ('alien_octopus_1', "= 10 POINTS"),
        ]
        y = 130
        for sprite_name, text in entries:
            sprite = self._fetch_sprite(sprite_name)
            surface.blit(sprite, (config.BASE_WIDTH // 2 - 160, y))
            surface.blit(score_font.render(text, True, (200, 200, 200)),
                         (config.BASE_WIDTH // 2 - 110, y + sprite.get_height() // 4))
            y += 32
        surface.blit(subtitle_font.render("CREDIT 00", True, (255, 255, 255)),
                     (config.BASE_WIDTH // 2 - 80, config.BASE_HEIGHT - 80))
        return surface

    def _render_wave_ready_scene(self) -> pygame.Surface:
        surface = pygame.Surface((config.BASE_WIDTH, config.BASE_HEIGHT), pygame.SRCALPHA)
        surface.fill((0, 0, 0))
        info_font = get_font("spriteviewer_stage_info")
        surface.blit(info_font.render("LEVEL 01", True, (255, 255, 0)), (20, 20))
        self._draw_ufo_lane(surface)
        self._draw_alien_rows(surface, top_y=80)
        bunker_bottom = config.BASE_HEIGHT - 80
        self._draw_bunkers(surface, bunker_bottom)
        self._draw_player(surface, config.BASE_HEIGHT - 40)
        pygame.draw.line(surface, (80, 80, 80), (0, config.BASE_HEIGHT - 35), (config.BASE_WIDTH, config.BASE_HEIGHT - 35))
        return surface

    def _render_late_wave_scene(self) -> pygame.Surface:
        surface = pygame.Surface((config.BASE_WIDTH, config.BASE_HEIGHT), pygame.SRCALPHA)
        surface.fill((0, 0, 0))
        info_font = get_font("spriteviewer_stage_info")
        surface.blit(info_font.render("LEVEL 04", True, (255, 120, 120)), (20, 20))
        self._draw_ufo_lane(surface)
        self._draw_alien_rows(surface, top_y=140, columns=7, spacing=12)
        bunker_bottom = config.BASE_HEIGHT - 70
        self._draw_bunkers(surface, bunker_bottom, cutouts=True)
        self._draw_player(surface, config.BASE_HEIGHT - 40)
        self._draw_bombs(surface)
        self._draw_player_bullet(surface)
        pygame.draw.line(surface, (80, 80, 80), (0, config.BASE_HEIGHT - 35), (config.BASE_WIDTH, config.BASE_HEIGHT - 35))
        return surface

    def _draw_ufo_lane(self, surface: pygame.Surface):
        ufo = self._fetch_sprite('ufo')
        surface.blit(ufo, (10, 50))
        surface.blit(self.tiny_font.render("= ? MYSTERY", True, (200, 200, 200)), (10 + ufo.get_width() + 8, 60))

    def _draw_alien_rows(self, surface: pygame.Surface, top_y: int, columns: int = 8, spacing: int = 8):
        row_types = ['alien_squid_1', 'alien_crab_1', 'alien_crab_1', 'alien_octopus_1', 'alien_octopus_1']
        y = top_y
        for sprite_name in row_types:
            sprite = self._fetch_sprite(sprite_name)
            total_width = columns * sprite.get_width() + (columns - 1) * spacing
            start_x = (config.BASE_WIDTH - total_width) // 2
            for col in range(columns):
                surface.blit(sprite, (start_x + col * (sprite.get_width() + spacing), y))
            y += sprite.get_height() + 10

    def _draw_bunkers(self, surface: pygame.Surface, bottom_y: int, cutouts: bool = False):
        bunker_sprite = self._fetch_sprite('bunker_full')
        spacing = config.BASE_WIDTH // (constants.BLOCK_NUMBER + 1)
        for i in range(constants.BLOCK_NUMBER):
            x = spacing * (i + 1) - bunker_sprite.get_width() // 2
            rect = pygame.Rect(x, bottom_y - bunker_sprite.get_height(), bunker_sprite.get_width(), bunker_sprite.get_height())
            surface.blit(bunker_sprite, rect.topleft)
            if cutouts:
                pygame.draw.rect(surface, (0, 0, 0), rect.inflate(-10, -12))

    def _draw_player(self, surface: pygame.Surface, bottom_y: int):
        player = self._fetch_sprite('player')
        x = (config.BASE_WIDTH - player.get_width()) // 2
        surface.blit(player, (x, bottom_y - player.get_height()))

    def _draw_bombs(self, surface: pygame.Surface):
        bomb = self._fetch_sprite('bomb_1')
        positions = [
            (config.BASE_WIDTH // 2 - 80, config.BASE_HEIGHT - 140),
            (config.BASE_WIDTH // 2 + 60, config.BASE_HEIGHT - 160),
            (config.BASE_WIDTH // 2 + 10, config.BASE_HEIGHT - 180),
        ]
        for pos in positions:
            surface.blit(bomb, pos)

    def _draw_player_bullet(self, surface: pygame.Surface):
        bullet = self._fetch_sprite('bullet')
        x = (config.BASE_WIDTH - bullet.get_width()) // 2
        y = config.BASE_HEIGHT - 120
        surface.blit(bullet, (x, y))
