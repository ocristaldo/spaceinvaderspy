#!/usr/bin/env python
"""Enhanced Space Invaders clone.

This version adds bunkers, alien bombs, a UFO, scoring and lives to more
closely mirror the original arcade game. Gameplay remains simple: aliens
move in formation, the player fires one bullet at a time and the game ends
if aliens reach the bottom or the player loses all lives.

This implementation is an unofficial, fan-made recreation created for
educational purposes only. It includes no original assets or code from the
1978 release and is not endorsed by the trademark holders.
"""
import logging
import sys
from typing import List, Optional, Tuple
import pygame
import random
from . import constants
from . import config
from .entities.player import Player
from .entities.alien import Alien
from .entities.bullet import Bullet, Bomb
from .entities.bunker import Bunker
from .entities.ufo import UFO
from .entities.effects import ExplosionEffect
from .utils.sprite_viewer import SpriteViewer
from .utils.audio_manager import AudioManager
from .utils.high_score_manager import HighScoreManager
from .utils.sprite_sheet import get_game_sprite, clear_tint_cache
from .ui.menu import Menu
from .ui.font_manager import get_font
from .ui.start_screen_demo import ScoreTableDemo, WaveFormationDemo
from .ui.color_scheme import get_color, get_tint
from .ui.sprite_digits import FontDigitWriter
from .ui.level_themes import get_level_theme, LevelTheme
from .ui.initials_entry import InitialsEntry
from .ui.continue_screen import ContinueScreen
from .systems.game_state_manager import GameStateManager, GameState
from .utils.settings_manager import SettingsManager

logging.basicConfig(
    level=logging.INFO,
    filename="game.log",
    filemode="w",
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def _install_global_exception_logger() -> None:
    """Install a global exception handler for logging unhandled exceptions."""
    def handle_exception(exc_type, exc_value, exc_traceback) -> None:
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logging.critical("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = handle_exception


_install_global_exception_logger()


class Game:
    """Main game controller."""

    def __init__(self):
        pygame.init()
        initial_size = config.get_window_size(config.DEFAULT_WINDOW_SCALE)
        self.screen = pygame.display.set_mode(initial_size, pygame.RESIZABLE)
        pygame.display.set_caption("Space Invaders")
        self.logical_width = config.BASE_WIDTH
        self.logical_height = config.BASE_HEIGHT
        self.playfield_surface = pygame.Surface((self.logical_width, self.logical_height))
        self.window_width, self.window_height = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.font = get_font("hud_main")
        self.small_font = get_font("hud_small")
        self.running = True
        self.game_over = False
        self.waiting_for_respawn = False
        self.level = 1
        self.current_theme: LevelTheme = get_level_theme(self.level)
        self.wave_message_text = ""
        self.wave_message_timer = 0
        self.floating_texts = []
        self.settings_manager = SettingsManager()
        self.tint_enabled = self.settings_manager.tint_enabled()
        self.sfx_enabled = self.settings_manager.audio_enabled()
        self.music_enabled = self.settings_manager.music_enabled()
        self.level_start_delay_ms = 1500
        self.level_start_ready_time = 0
        self.game_over_intro_delay_ms = 5000
        self._game_over_return_time = None
        self._game_over_processed = False
        self.credit_count = 0
        self.max_life_icons = 5
        self.bottom_panel_height = 36
        self.fast_invader_step = 0
        self._last_music_should_play = None
        self._build_ui_assets()

        # State management
        self.state_manager = GameStateManager()

        # Audio and scoring systems
        self.audio_manager = AudioManager()
        self.audio_manager.set_sfx_enabled(self.sfx_enabled)
        self.audio_manager.set_music_enabled(self.music_enabled)
        self.high_score_manager = HighScoreManager()

        # Single/2-player mode tracking
        self.two_player_mode = False
        self.current_player = 1  # Which player is currently playing (1 or 2)

        # Player 1 scores and lives
        self.score = 0
        self.lives = constants.LIVES_NUMBER
        self.extra_lives_threshold = 20000  # Extra life at 20k, then every 70k
        self.extra_lives_interval = 70000
        self.lives_awarded = 0  # Track how many extra lives have been awarded

        # Player 2 scores and lives (2-player mode only)
        self.p2_score = 0
        self.p2_lives = constants.LIVES_NUMBER
        self.p2_lives_awarded = 0

        # Player-specific game state (for persisting game state when switching players)
        # Each player maintains independent state: first switch starts fresh, subsequent switches restore
        self.player_states = {
            1: {
                'level': 1,
                'alien_direction': 1,
                'alien_speed': config.ALIEN_START_SPEED,
                'initial_alien_count': 0,
                'aliens': None,
                'bunkers': None,
                'has_been_saved': False,  # Track if this player has ever been played
            },
            2: {
                'level': 1,
                'alien_direction': 1,
                'alien_speed': config.ALIEN_START_SPEED,
                'initial_alien_count': 0,
                'aliens': None,
                'bunkers': None,
                'has_been_saved': False,  # Track if this player has ever been played
            }
        }

        self.player = Player(tint=self._sprite_tint("player"))
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self._position_player()
        self.bullet_group = pygame.sprite.Group()
        self.bomb_group = pygame.sprite.Group()
        self.effects_group = pygame.sprite.Group()
        self.bunker_group = self.create_bunkers()
        self.ufo_group = pygame.sprite.Group()

        self.alien_group = self.create_aliens()
        self.alien_direction = 1
        self._reset_alien_progression()
        
        # Sprite viewer for testing
        self.sprite_viewer = SpriteViewer(self.screen)
        self.viewing_sprites = False
        self.menu = Menu()
        self.menu.update_options_state(
            self.sfx_enabled,
            self.settings_manager.intro_demo_enabled(),
            self.tint_enabled,
            self.music_enabled,
        )
        self.score_demo = ScoreTableDemo(tint_enabled=self.tint_enabled, credit_count=self.credit_count)
        self.start_screen_demo = self.score_demo  # Backwards-compatibility for older tests/utilities
        self.wave_demo = WaveFormationDemo(tint_enabled=self.tint_enabled)
        self.demo_cycle = [self.score_demo, self.wave_demo]
        self.demo_cycle_enabled = False
        self.demo_cycle_index = 0
        self.active_demo = None
        self.initials_entry_screen: Optional[InitialsEntry] = None
        self.continue_screen: Optional[ContinueScreen] = None
        self.alien_speed = config.ALIEN_START_SPEED
        self.initial_alien_count = len(self.alien_group)
        self.last_ufo_time = pygame.time.get_ticks()
        # Attract mode/demo settings
        self.attract_last_activity_time = pygame.time.get_ticks()
        self.attract_idle_time = config.ATTRACT_IDLE_TIME
        self.debug_sprite_borders = self.settings_manager.debug_borders_enabled()
        self.menu.set_debug_borders(self.debug_sprite_borders)
        self.score_demo.set_debug_borders(self.debug_sprite_borders)
        if hasattr(self.wave_demo, "set_debug_borders"):
            self.wave_demo.set_debug_borders(self.debug_sprite_borders)

        if self.settings_manager.intro_demo_enabled():
            self.start_intro_demo()
        else:
            self.state_manager.change_state(GameState.MENU)
        audio_status = "ON" if self.sfx_enabled else "muted (press 'A' to toggle)"
        logging.info("Game started. Player lives=%d. Audio %s", self.lives, audio_status)

    @property
    def state(self):
        """Backwards-compatible string state for existing tests/utilities."""
        return self.state_manager.current_state.name

    def reset_game(self, start_playing: bool = True):
        """Reset the game to initial state."""
        self.game_over = False
        self.waiting_for_respawn = False
        self.score = 0
        self.lives = constants.LIVES_NUMBER
        self.lives_awarded = 0
        self.level = 1
        self.wave_message_text = "Ready!"
        self.wave_message_timer = pygame.time.get_ticks() + 2000
        self.level_start_ready_time = pygame.time.get_ticks() + self.level_start_delay_ms
        self.state_manager.change_state(GameState.PLAYING if start_playing else GameState.MENU)
        self._game_over_processed = False
        self._game_over_return_time = None
        
        # Clear all sprite groups
        self.bullet_group.empty()
        self.bomb_group.empty()
        self.ufo_group.empty()
        self.effects_group.empty()
        self.audio_manager.stop_ufo_loop()
        
        # Reset player
        self._respawn_player()
        
        # Recreate aliens and bunkers
        self.alien_group = self.create_aliens()
        self.bunker_group = self.create_bunkers()
        
        # Reset alien movement
        self.alien_direction = 1
        self._reset_alien_progression()
        self.last_ufo_time = pygame.time.get_ticks()
        self.fast_invader_step = 0
        
        logging.info("Game reset complete")

    def start_two_player_game(self) -> None:
        """Initialize a 2-player alternating game."""
        self.two_player_mode = True
        self.current_player = 1
        self.score = 0
        self.lives = constants.LIVES_NUMBER
        self.p2_score = 0
        self.p2_lives = constants.LIVES_NUMBER
        self.lives_awarded = 0
        self.p2_lives_awarded = 0

        # Reset player states - each will start fresh on first switch
        for player_num in [1, 2]:
            self.player_states[player_num] = {
                'level': 1,
                'alien_direction': 1,
                'alien_speed': config.ALIEN_START_SPEED,
                'initial_alien_count': 0,
                'aliens': None,
                'bunkers': None,
                'has_been_saved': False,
            }

        self.reset_game(start_playing=True)
        logging.info("2-Player game started. Player 1 begins")

    def switch_player(self) -> None:
        """Switch to the other player in 2-player mode, preserving their game state."""
        if not self.two_player_mode:
            return

        old_player = self.current_player

        # Save current player's state before switching
        self._save_player_state(old_player)

        # Switch player
        if old_player == 1:
            self.current_player = 2
            logging.info("Switched to Player 2 (Score: %d, Lives: %d)", self.p2_score, self.p2_lives)
        else:
            self.current_player = 1
            logging.info("Switched to Player 1 (Score: %d, Lives: %d)", self.score, self.lives)

        # Restore the new player's state
        self._restore_player_state(self.current_player)

        # Clear active projectiles and effects
        self.bullet_group.empty()
        self.bomb_group.empty()
        self.effects_group.empty()
        self.audio_manager.stop_ufo_loop()
        self._respawn_player()

    def _save_player_state(self, player_num: int) -> None:
        """Save the current player's game state (level, aliens, bunkers, etc.)."""
        if not self.two_player_mode:
            return

        self.player_states[player_num] = {
            'level': self.level,
            'alien_direction': self.alien_direction,
            'alien_speed': self.alien_speed,
            'initial_alien_count': self.initial_alien_count,
            'aliens': self.alien_group.copy(),
            'bunkers': self.bunker_group.copy(),
            'has_been_saved': True,
        }
        logging.debug("Saved state for Player %d (Level %d, %d aliens)",
                      player_num, self.level, len(self.alien_group))

    def _restore_player_state(self, player_num: int) -> None:
        """Restore a player's previously saved game state, or create fresh for first-time switch."""
        if not self.two_player_mode:
            return

        state = self.player_states[player_num]

        # Check if this player has ever been played before
        if not state['has_been_saved']:
            # First time this player is playing - start fresh at level 1
            self.level = 1
            self.alien_direction = 1
            self.alien_speed = config.ALIEN_START_SPEED
            self.current_theme = get_level_theme(self.level)
            self.alien_group = self.create_aliens()
            self.bunker_group = self.create_bunkers()
            logging.info("Player %d starting fresh (first time)", player_num)
        else:
            # Player has been saved before - restore their exact state
            self.level = state['level']
            self.alien_direction = state['alien_direction']
            self.alien_speed = state['alien_speed']
            self.initial_alien_count = state['initial_alien_count']
            self.current_theme = get_level_theme(self.level)

            # Restore sprite groups from saved state
            if state['aliens'] is not None and len(state['aliens']) > 0:
                self.alien_group = state['aliens'].copy()
            else:
                self.alien_group = self.create_aliens()

            if state['bunkers'] is not None and len(state['bunkers']) > 0:
                self.bunker_group = state['bunkers'].copy()
            else:
                self.bunker_group = self.create_bunkers()

            logging.debug("Restored saved state for Player %d (Level %d, %d aliens)",
                          player_num, self.level, len(self.alien_group))

    def get_current_score(self) -> int:
        """Get the current player's score."""
        return self.score if self.current_player == 1 else self.p2_score

    def get_current_lives(self) -> int:
        """Get the current player's lives."""
        return self.lives if self.current_player == 1 else self.p2_lives

    def set_current_score(self, value: int) -> None:
        """Set the current player's score."""
        if self.current_player == 1:
            self.score = value
        else:
            self.p2_score = value

    def set_current_lives(self, value: int) -> None:
        """Set the current player's lives."""
        if self.current_player == 1:
            self.lives = value
        else:
            self.p2_lives = value

    def create_aliens(self) -> pygame.sprite.Group:
        """Create alien formation and return sprite group."""
        group = pygame.sprite.Group()
        margin_y = config.ALIEN_MARGIN_Y
        spacing_y = config.ALIEN_SPACING_Y
        rows = config.ALIEN_ROWS
        cols = config.ALIEN_COLUMNS
        base_values = [30, 20, 20, 10, 10]  # Top row worth most points
        values = base_values[:rows]

        # Get sprite dimensions for centering
        sprite_widths = {
            30: get_game_sprite('alien_squid_1', config.SPRITE_SCALE).get_width(),
            20: get_game_sprite('alien_crab_1', config.SPRITE_SCALE).get_width(),
            10: get_game_sprite('alien_octopus_1', config.SPRITE_SCALE).get_width(),
        }
        sprite_heights = {
            30: get_game_sprite('alien_squid_1', config.SPRITE_SCALE).get_height(),
            20: get_game_sprite('alien_crab_1', config.SPRITE_SCALE).get_height(),
            10: get_game_sprite('alien_octopus_1', config.SPRITE_SCALE).get_height(),
        }
        max_row_height = max(sprite_heights.values())

        max_sprite_width = max(sprite_widths.values())
        column_gap = config.ALIEN_SPACING_X
        formation_width = cols * max_sprite_width + (cols - 1) * column_gap
        start_x = max(
            config.ALIEN_MARGIN_X,
            (self.logical_width - formation_width) / 2,
        )
        for row_idx, value in enumerate(values):
            alien_width = sprite_widths[value]
            offset_within_cell = (max_sprite_width - alien_width) / 2
            x_offset = start_x
            for col_idx in range(cols):
                cell_x = x_offset + col_idx * (max_sprite_width + column_gap)
                x = cell_x + offset_within_cell
                row_base_y = margin_y + row_idx * spacing_y
                y = row_base_y + (max_row_height - sprite_heights[value])
                group.add(Alien(x, y, value, tint=self._alien_tint(value)))
        return group

    def create_bunkers(self) -> pygame.sprite.Group:
        """Create bunkers and return sprite group."""
        group = pygame.sprite.Group()
        spacing = self.logical_width // (constants.BLOCK_NUMBER + 1)
        player_top = self.player.rect.top
        bunker_bottom = max(0, player_top - config.BUNKER_PLAYER_GAP)
        tint = self._sprite_tint("bunker")
        for i in range(constants.BLOCK_NUMBER):
            center_x = spacing * (i + 1)
            group.add(Bunker(center_x, bunker_bottom, tint=tint))
        return group

    def _sprite_tint(self, key: str) -> Optional[Tuple[int, int, int]]:
        """Get tint color for sprite from current theme or None if tinting disabled."""
        if not self.tint_enabled:
            return None

        # Get color from current level theme
        theme_colors = {
            "player": self.current_theme.player,
            "life_icon": self.current_theme.player,
            "alien_squid": self.current_theme.alien_squid,
            "alien_crab": self.current_theme.alien_crab,
            "alien_octopus": self.current_theme.alien_octopus,
            "ufo": self.current_theme.ufo,
            "bunker": self.current_theme.bunker,
            "bullet": self.current_theme.bullet,
            "bomb_alien": self.current_theme.bomb_alien,
            "bomb_ufo": self.current_theme.bomb_ufo,
            "hud_text": self.current_theme.hud_text,
        }

        # Return theme color if available, otherwise use default
        if key in theme_colors:
            return theme_colors[key]
        return get_tint(key)

    def _alien_tint(self, value: int) -> Optional[Tuple[int, int, int]]:
        """Get tint color for alien type from current theme."""
        if not self.tint_enabled:
            return None
        return self.current_theme.get_alien_color(value)

    def _player_floor(self) -> int:
        """Calculate the y-coordinate where player should rest."""
        return self.logical_height - self.bottom_panel_height - 4

    def _position_player(self) -> None:
        """Position player at bottom center of playfield."""
        if hasattr(self, "player") and self.player:
            self.player.rect.midbottom = (self.logical_width // 2, self._player_floor())

    def _build_ui_assets(self) -> None:
        """Build UI asset surfaces (life icons, digits, etc)."""
        life_icon = get_game_sprite("player", config.SPRITE_SCALE, tint=self._sprite_tint("life_icon"))
        if life_icon.get_width() > 0:
            scale_factor = 0.8
            size = (
                max(1, int(life_icon.get_width() * scale_factor)),
                max(1, int(life_icon.get_height() * scale_factor)),
            )
            self.life_icon_surface = pygame.transform.smoothscale(life_icon, size)
        else:
            self.life_icon_surface = life_icon
        self.hi_label_surface = get_game_sprite(
            "text_hi_score", config.SPRITE_SCALE, tint=self._sprite_tint("text_hi_score")
        )
        self.credit_label_surface = get_game_sprite(
            "text_credit", config.SPRITE_SCALE, tint=self._sprite_tint("text_credit")
        )
        self.digit_writer = FontDigitWriter(font_size=16)
        icon_height = self.life_icon_surface.get_height() if self.life_icon_surface else 16
        self.bottom_panel_height = max(36, icon_height + 12)
        if hasattr(self, "player"):
            self._position_player()

    def _refresh_playfield_sprites(self):
        self.player = Player(tint=self._sprite_tint("player"))
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self._position_player()
        self.bunker_group = self.create_bunkers()
        self.alien_group = self.create_aliens()
        self.bullet_group.empty()
        self.bomb_group.empty()
        self.effects_group.empty()

    def _apply_tint_preference(self, enabled: bool):
        if enabled == self.tint_enabled:
            return
        self.tint_enabled = enabled
        clear_tint_cache()
        self._build_ui_assets()
        self._refresh_playfield_sprites()
        self.score_demo.set_tint_enabled(self.tint_enabled)
        if hasattr(self.wave_demo, "set_tint_enabled"):
            self.wave_demo.set_tint_enabled(self.tint_enabled)
        self.menu.update_options_state(
            self.sfx_enabled,
            self.settings_manager.intro_demo_enabled(),
            self.tint_enabled,
            self.music_enabled,
        )

    def _toggle_tint_setting(self):
        new_state = not self.tint_enabled
        self.settings_manager.set_tint_enabled(new_state)
        self._apply_tint_preference(new_state)
        logging.info("Sprite tint %s", "enabled" if new_state else "disabled")


    def start_intro_demo(self, triggered_from_options: bool = False, cycle: bool = False):
        """Kick off the start-screen animation."""
        if self.state_manager.current_state == GameState.ATTRACT and self.active_demo and self.active_demo.is_running():
            if not cycle or self.demo_cycle_enabled:
                return
        if self.viewing_sprites:
            self.viewing_sprites = False
            self.sprite_viewer.reset_view()
        self.menu.hide_controls()
        self.menu.hide_high_scores()
        self.menu.hide_credits()
        self.menu.hide_options()
        self.demo_cycle_enabled = cycle
        if self.demo_cycle_enabled:
            self.demo_cycle_index = 0
            self.active_demo = self.demo_cycle[self.demo_cycle_index]
        else:
            self.active_demo = self.score_demo
        if hasattr(self.active_demo, "set_debug_borders"):
            self.active_demo.set_debug_borders(self.debug_sprite_borders)
        self.active_demo.start()
        self.state_manager.change_state(GameState.ATTRACT)
        logging.info(
            "Intro demo started%s (%s)",
            " from options" if triggered_from_options else "",
            "cycling" if cycle else "intro",
        )

    def _finish_intro_demo(self, forced: bool = False):
        """Return to the menu once the intro demo is complete."""
        if self.state_manager.current_state != GameState.ATTRACT:
            return
        if forced and self.active_demo and self.active_demo.is_running():
            self.active_demo.skip()
        elif not forced and (not self.active_demo or not self.active_demo.is_finished()):
            return
        self.state_manager.change_state(GameState.MENU)
        self.demo_cycle_enabled = False
        self.active_demo = None
        self.attract_last_activity_time = pygame.time.get_ticks()
        logging.info("Intro demo finished; returning to menu")

    def _toggle_sfx_setting(self):
        """Toggle sound effects and persist the setting."""
        new_state = not self.sfx_enabled
        self.sfx_enabled = new_state
        self.audio_manager.set_sfx_enabled(new_state)
        self.settings_manager.set_audio_enabled(new_state)
        self.menu.update_options_state(
            self.sfx_enabled,
            self.settings_manager.intro_demo_enabled(),
            self.tint_enabled,
            self.music_enabled,
        )
        logging.info("Sound FX toggled: %s", "ON" if self.sfx_enabled else "OFF")

    def _toggle_music_setting(self):
        """Toggle background music and persist the setting."""
        new_state = not self.music_enabled
        self.music_enabled = new_state
        self.audio_manager.set_music_enabled(new_state)
        self.settings_manager.set_music_enabled(new_state)
        self.menu.update_options_state(
            self.sfx_enabled,
            self.settings_manager.intro_demo_enabled(),
            self.tint_enabled,
            self.music_enabled,
        )
        self._update_music_state()
        logging.info("Menu music toggled: %s", "ON" if self.music_enabled else "OFF")

    def _update_music_state(self):
        playing_state = self.state_manager.current_state == GameState.PLAYING
        if not playing_state:
            self.audio_manager.stop_ufo_loop()
        should_play = self.music_enabled and not playing_state and not self.viewing_sprites
        if should_play == self._last_music_should_play:
            return
        self._last_music_should_play = should_play
        if should_play:
            self.audio_manager.play_menu_music()
        else:
            self.audio_manager.stop_music()

    def _set_debug_borders(self, enabled: bool) -> None:
        enabled = bool(enabled)
        if self.debug_sprite_borders == enabled:
            return
        self.debug_sprite_borders = enabled
        self.settings_manager.set_debug_borders_enabled(enabled)
        self.menu.set_debug_borders(enabled)
        self.score_demo.set_debug_borders(enabled)
        if hasattr(self.wave_demo, "set_debug_borders"):
            self.wave_demo.set_debug_borders(enabled)
        if hasattr(self.active_demo, "set_debug_borders"):
            self.active_demo.set_debug_borders(enabled)
        logging.info("Sprite border debug %s", "enabled" if enabled else "disabled")

    def handle_events(self):
        """
        Process all pygame events including keyboard input and window events.
        
        This method handles:
        - Window close events (X button)
        - Keyboard input for shooting, quitting, and restarting
        - Sprite viewer key combinations (S+1, S+2, S+3, S+4)
        - Game state transitions based on user input
        """
        # Get currently pressed keys for combination detection
        keys_pressed = pygame.key.get_pressed()

        if self.state_manager.current_state != GameState.ATTRACT:
            # Check for sprite viewer key combinations (works both in game and sprite viewer)
            stage_snapshot = self.sprite_viewer.get_stage_from_key_combo(keys_pressed)
            if stage_snapshot:
                if self.sprite_viewer.load_stage_preview(stage_snapshot):
                    self.viewing_sprites = True
                    logging.info("Loaded stage preview: %s", stage_snapshot)
            else:
                platform = self.sprite_viewer.get_platform_from_key_combo(keys_pressed)
                if platform:
                    if self.sprite_viewer.load_platform_sprites(platform):
                        self.viewing_sprites = True
                        logging.info(f"Switched to sprite viewer mode for {platform}")

            # Handle sprite viewer navigation if currently viewing sprites
            if self.viewing_sprites:
                self.sprite_viewer.handle_navigation(keys_pressed)

        # Process all pending pygame events
        for event in pygame.event.get():
            # Reset attract timer on any processed event
            self.attract_last_activity_time = pygame.time.get_ticks()
            # Handle window close button
            if event.type == pygame.QUIT:
                self.running = False
                logging.info("Game quit via window close")

            elif event.type == pygame.VIDEORESIZE:
                self._handle_resize(event.w, event.h)
                continue

            elif event.type == pygame.WINDOWRESIZED:
                self._handle_resize(event.x, event.y)
                continue

            # Handle keyboard key press events
            elif event.type == pygame.KEYDOWN:
                # R key: Exit sprite viewer or restart when game over
                if event.key == pygame.K_r:
                    if self.viewing_sprites:
                        self.viewing_sprites = False
                        self.sprite_viewer.reset_view()
                        logging.info("Exited sprite viewer mode")
                        continue
                    if self.game_over:
                        self._return_to_intro_screen(trigger="key_event")
                        continue

                # Universal hotkeys that work everywhere
                # Credit insertion (works at any time)
                if event.key == pygame.K_c:
                    self._insert_credit()
                    continue

                if self.state_manager.current_state == GameState.ATTRACT:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self._finish_intro_demo(forced=True)
                        continue
                    # 1/2 keys to start game directly from attract mode
                    if event.key == pygame.K_1:
                        if self.credit_count <= 0:
                            logging.info("Insert credit to start")
                            continue
                        self.credit_count -= 1
                        self.two_player_mode = False
                        self.reset_game()
                        logging.info("1-Player game started from attract (credit remaining=%02d)", self.credit_count)
                        continue
                    if event.key == pygame.K_2:
                        if self.credit_count < 2:
                            logging.info("Need 2 credits to start 2-player game")
                            continue
                        self.credit_count -= 2
                        self.start_two_player_game()
                        logging.info("2-Player game started from attract (credit remaining=%02d)", self.credit_count)
                        continue
                    continue

                # Menu navigation when in MENU state
                if self.state_manager.current_state == GameState.MENU:
                    # 1 key: Start 1-player game
                    if event.key == pygame.K_1:
                        if self.credit_count <= 0:
                            logging.info("Insert credit to start")
                            continue
                        self.credit_count -= 1
                        self.two_player_mode = False
                        self.reset_game()
                        logging.info("1-Player game started (credit remaining=%02d)", self.credit_count)
                        continue
                    # 2 key: Start 2-player game
                    elif event.key == pygame.K_2:
                        if self.credit_count < 2:
                            logging.info("Need 2 credits to start 2-player game")
                            continue
                        self.credit_count -= 2
                        self.start_two_player_game()
                        logging.info("2-Player game started (credit remaining=%02d)", self.credit_count)
                        continue

                    if self.menu.showing_options:
                        if event.key == pygame.K_d:
                            self.start_intro_demo(triggered_from_options=True, cycle=True)
                            continue
                        if event.key == pygame.K_i:
                            new_state = not self.settings_manager.intro_demo_enabled()
                            self.settings_manager.set_intro_demo_enabled(new_state)
                            self.menu.update_options_state(
                                self.sfx_enabled,
                                new_state,
                                self.tint_enabled,
                                self.music_enabled,
                            )
                            logging.info("Intro demo autoplay %s", "enabled" if new_state else "disabled")
                            continue
                    if not self.menu.showing_options and event.key == pygame.K_d:
                        self.start_intro_demo(triggered_from_options=True, cycle=True)
                        continue
                    action = self.menu.handle_key(event.key)
                    if action == "1-player":
                        if self.credit_count <= 0:
                            logging.info("Insert credit to start")
                            continue
                        self.credit_count -= 1
                        self.two_player_mode = False
                        self.reset_game()
                        logging.info("1-Player game started from menu (credit remaining=%02d)", self.credit_count)
                    elif action == "2-player":
                        if self.credit_count <= 0:
                            logging.info("Insert credit to start")
                            continue
                        self.credit_count -= 1
                        self.start_two_player_game()
                        logging.info("2-Player game started from menu (credit remaining=%02d)", self.credit_count)
                    elif action == "controls":
                        self.menu.show_controls()
                        logging.info("Controls overlay opened from menu")
                    elif action == "high scores":
                        self.menu.show_high_scores(self.high_score_manager.get_top_scores())
                        logging.info("High Scores overlay opened from menu")
                    elif action == "credits":
                        self.menu.show_credits()
                        logging.info("Credits overlay opened from menu")
                    elif action == "quit":
                        self.running = False
                        logging.info("Game quit from menu")
                    elif action == "options":
                        # Open options overlay and pass current settings state
                        self.menu.show_options_with_settings(
                            self.sfx_enabled,
                            self.settings_manager.intro_demo_enabled(),
                            self.debug_sprite_borders,
                            self.tint_enabled,
                            self.music_enabled,
                        )
                        logging.info("Options overlay opened from menu")
                    elif action == "options_toggle_audio":
                        self._toggle_sfx_setting()
                        continue
                    elif action == "options_play_demo":
                        self.menu.hide_options()
                        self.start_intro_demo(triggered_from_options=True, cycle=True)
                        continue
                    elif action == "options_toggle_autodemo":
                        new_state = not self.settings_manager.intro_demo_enabled()
                        self.settings_manager.set_intro_demo_enabled(new_state)
                        self.menu.update_options_state(
                            self.sfx_enabled,
                            new_state,
                            self.tint_enabled,
                            self.music_enabled,
                        )
                        logging.info("Intro demo autoplay %s", "enabled" if new_state else "disabled")
                        continue
                    elif action == "options_toggle_borders":
                        self._set_debug_borders(not self.debug_sprite_borders)
                        continue
                    elif action == "options_toggle_music":
                        self._toggle_music_setting()
                        continue
                    elif action == "options_toggle_tint":
                        self._toggle_tint_setting()
                        continue
                    elif action == "options_back":
                        continue
                    continue

                if self.waiting_for_respawn:
                    if event.key == pygame.K_SPACE:
                        logging.info("Resuming play after life lost")
                        self.waiting_for_respawn = False
                    continue

                # Spacebar: Fire bullet (only if no bullet currently active and playing)
                if (
                    event.key == pygame.K_SPACE
                    and len(self.bullet_group) < config.PLAYER_MAX_BULLETS
                    and self.state_manager.current_state == GameState.PLAYING
                    and not self.viewing_sprites
                    and not self.waiting_for_respawn
                ):
                    bullet = Bullet(self.player.get_bullet_spawn_position())
                    self.bullet_group.add(bullet)
                    self.audio_manager.play_sound("shoot")
                    logging.info("Bullet fired from player position")

                # P or ESC: Toggle pause when playing
                if event.key in (pygame.K_p, pygame.K_ESCAPE):
                    if self.state_manager.current_state == GameState.PLAYING:
                        self.state_manager.change_state(GameState.PAUSED)
                        logging.info("Game paused")
                    elif self.state_manager.current_state == GameState.PAUSED:
                        self.state_manager.change_state(GameState.PLAYING)
                        logging.info("Game resumed")

                # Q key: Quit game at any time
                if event.key == pygame.K_q:
                    self.running = False
                    logging.info("Game quit by user (Q key)")

                # Audio hotkeys
                if event.key == pygame.K_a:
                    if self.menu.showing_options or self.state_manager.current_state == GameState.PLAYING:
                        self._toggle_sfx_setting()
                        continue
                if event.key == pygame.K_m:
                    if self.menu.showing_options or self.state_manager.current_state != GameState.PLAYING:
                        self._toggle_music_setting()
                        continue

    def spawn_bomb(self):
        """
        Randomly spawn bombs from alien ships.
        
        This method:
        - Checks if any aliens exist (no bombs if no aliens)
        - Uses random probability (2% chance per frame) to spawn bombs
        - Selects a random alien to drop the bomb
        - Creates bomb at alien's bottom center position
        """
        # Don't spawn bombs if no aliens remain
        if (
            self.state_manager.current_state != GameState.PLAYING
            or not self.alien_group
        ):
            return
        
        # Probability-based bomb spawn (starts gentle, ramps up as aliens fall)
        bomb_chance = config.ALIEN_BOMB_CHANCE + (
            max(0, self.initial_alien_count - len(self.alien_group)) * 0.0005
        )
        if random.random() < bomb_chance:
            # Select random alien from remaining aliens
            alien = random.choice(self.alien_group.sprites())
            # Create bomb at alien's bottom center
            bomb = Bomb(alien.rect.midbottom, sprite_name='bomb_1', tint=self._sprite_tint("bomb_1"))
            self.bomb_group.add(bomb)
            logging.debug("Alien bomb spawned at %s from alien at %s", 
                         bomb.rect.topleft, alien.rect.topleft)

    def spawn_ufo(self):
        now = pygame.time.get_ticks()
        if now - self.last_ufo_time > config.UFO_INTERVAL:
            self.ufo_group.add(UFO(-60, 40))  # Start UFO slightly higher
            self.last_ufo_time = now
            logging.info("UFO spawned")
            self.audio_manager.start_ufo_loop()
    
    def _maybe_drop_ufo_bombs(self):
        """Allow active UFOs to drop their own bomb type while flying across."""
        if self.state_manager.current_state != GameState.PLAYING:
            return
        if not self.ufo_group:
            self.audio_manager.stop_ufo_loop()
            return
        for ufo in self.ufo_group.sprites():
            if random.random() < config.UFO_BOMB_CHANCE:
                bomb = Bomb(ufo.rect.midbottom, sprite_name='bomb_2', tint=self._sprite_tint("bomb_2"))
                self.bomb_group.add(bomb)
                logging.debug("UFO bomb spawned at %s", bomb.rect.topleft)
        if not self.ufo_group:
            self.audio_manager.stop_ufo_loop()

    def update_alien_speed(self):
        """Increase alien speed as their numbers decrease."""
        remaining = len(self.alien_group)
        if remaining and self.initial_alien_count:
            progress = 1.0 - (remaining / self.initial_alien_count)
            max_speed = config.ALIEN_MAX_SPEED
            base = config.ALIEN_START_SPEED
            self.alien_speed = base + progress * (max_speed - base)

    def _play_fast_invader_sound(self):
        if not self.alien_group:
            return
        self.audio_manager.play_fast_invader(self.fast_invader_step)
        self.fast_invader_step = (self.fast_invader_step + 1) % 4

    def update(self):
        pressed = pygame.key.get_pressed()
        if self.waiting_for_respawn:
            return
        self.player_group.update(pressed)
        # Update non-projectile entities first
        self.ufo_group.update()
        self._maybe_drop_ufo_bombs()

        # Animate aliens every 30 frames (0.5 seconds at 60 FPS)
        if pygame.time.get_ticks() % 500 < 16:  # Roughly every 0.5 seconds
            for alien in self.alien_group:
                alien.animate()
            self._play_fast_invader_sound()

        # Move aliens as a group (classic Space Invaders movement)
        if self.alien_group:
            move_x = self.alien_direction * self.alien_speed
            move_down = False

            aliens = self.alien_group.sprites()
            formation_left = min(alien.rect.left for alien in aliens)
            formation_right = max(alien.rect.right for alien in aliens)

            if (
                formation_right + move_x >= self.logical_width - config.ALIEN_EDGE_PADDING
                or formation_left + move_x <= config.ALIEN_EDGE_PADDING
            ):
                move_down = True
                self.alien_direction *= -1

            # Move aliens
            for alien in self.alien_group.sprites():
                if move_down:
                    alien.rect.y += config.ALIEN_DROP_DISTANCE  # Drop down when hitting edge
                else:
                    alien.rect.x += move_x
            self._handle_alien_collisions()

        # Spawn events
        self.spawn_bomb()
        self.spawn_ufo()

        # Collisions
        hits = pygame.sprite.groupcollide(self.bullet_group, self.alien_group, True, True)
        for bullet, aliens in hits.items():
            for alien in aliens:
                # Add score to current player
                if self.two_player_mode and self.current_player == 2:
                    self.p2_score += alien.value
                else:
                    self.score += alien.value
                self._spawn_explosion(alien.rect.center)
                self.audio_manager.play_sound("invaderkilled")
                logging.info("Alien destroyed at %s", alien.rect.topleft)
        if hits:
            self.update_alien_speed()

        hits = pygame.sprite.groupcollide(self.bullet_group, self.ufo_group, True, True)
        for bullet, ufos in hits.items():
            for ufo in ufos:
                # Add score to current player
                if self.two_player_mode and self.current_player == 2:
                    self.p2_score += ufo.value
                else:
                    self.score += ufo.value
                self._spawn_explosion(ufo.rect.center)
                self.audio_manager.play_sound("explosion")
                logging.info("UFO destroyed for %d points", ufo.value)
                self._add_floating_text(str(ufo.value), ufo.rect.center, color=constants.GREEN)

        # bullet vs bunker
        hits = pygame.sprite.groupcollide(self.bullet_group, self.bunker_group, True, False)
        for bunker_list in hits.values():
            for bunker in bunker_list:
                bunker.damage()
                logging.debug("Bunker damaged at %s", bunker.rect.topleft)

    # (No duplicate initialization here)
        intercepts = pygame.sprite.groupcollide(self.bullet_group, self.bomb_group, True, True)
        if intercepts:
            logging.debug("Player bullet intercepted an alien bomb")

        # bomb vs player - use sprite collision helper for robustness
        try:
            hit_bombs = pygame.sprite.spritecollide(self.player, self.bomb_group, dokill=True)
        except Exception:
            hit_bombs = []
        if hit_bombs:
            # Deduct lives from current player
            if self.two_player_mode and self.current_player == 2:
                self.p2_lives -= len(hit_bombs)
                current_lives = self.p2_lives
            else:
                self.lives -= len(hit_bombs)
                current_lives = self.lives

            logging.warning("Player %d hit! Lives left=%d", self.current_player, current_lives)
            self._spawn_explosion(self.player.rect.center)
            self.audio_manager.play_sound("explosion")

            if self.two_player_mode:
                # In 2-player mode, switch to other player on every hit
                if self.current_player == 1:
                    if self.p2_lives > 0:
                        # P2 still has lives, switch to them
                        logging.info("Player 1 hit! Switching to Player 2 (P2 lives: %d)", self.p2_lives)
                        self.switch_player()
                    else:
                        # P2 is out of lives, P1 must continue
                        if current_lives <= 0:
                            # P1 also out of lives
                            logging.info("Both players out of lives - showing continue screen")
                            self._show_continue_screen()
                        else:
                            # P1 continues after being hit
                            self._handle_life_loss()
                else:  # current_player == 2
                    if self.lives > 0:
                        # P1 still has lives, switch to them
                        logging.info("Player 2 hit! Switching to Player 1 (P1 lives: %d)", self.lives)
                        self.switch_player()
                    else:
                        # P1 is out of lives, P2 must continue
                        if current_lives <= 0:
                            # P2 also out of lives
                            logging.info("Both players out of lives - showing continue screen")
                            self._show_continue_screen()
                        else:
                            # P2 continues after being hit
                            self._handle_life_loss()
            else:
                # Single-player mode
                if current_lives <= 0:
                    self._show_continue_screen()
                else:
                    self._handle_life_loss()

        # bomb vs bunker
        hits = pygame.sprite.groupcollide(self.bomb_group, self.bunker_group, True, False)
        for bunker_list in hits.values():
            for bunker in bunker_list:
                bunker.damage()
                logging.debug("Bunker hit by bomb at %s", bunker.rect.topleft)

        self._handle_alien_collisions()

        if not self.alien_group:
            self._start_next_wave()

        # Check for extra lives milestones
        self._check_extra_lives()

        # Update bullets and bombs after handling collisions to keep frame semantics
        self.bullet_group.update()
        self.bomb_group.update()
        self.effects_group.update()

        if self.game_over:
            logging.info("Game over detected")
            # Don't stop running immediately, let game_over_screen handle it

    def _reset_alien_progression(self, speed_bonus: float = 0.0):
        """Reset alien speed progression to the slow starting pace."""
        self.initial_alien_count = len(self.alien_group)
        self.alien_speed = config.ALIEN_START_SPEED + speed_bonus

    def _respawn_player(self):
        """Respawn the player ship at the starting position."""
        self.player = Player(tint=self._sprite_tint("player"))
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self._position_player()

    def _handle_life_loss(self):
        """Pause gameplay after losing a life and wait for player input to resume."""
        self.waiting_for_respawn = True
        self.bullet_group.empty()
        self.bomb_group.empty()
        self._respawn_player()
        self._reset_alien_progression()
        logging.info("Life lost. Press SPACE to continue.")

    def _handle_alien_collisions(self):
        """Handle alien interactions with bunkers, player, and the ground."""
        if not self.alien_group or self.game_over:
            return

        for alien in list(self.alien_group):
            if alien.rect.colliderect(self.player.rect):
                self._trigger_alien_victory("Game over: an alien reached the player")
                return

            if alien.rect.bottom >= self.logical_height - 4:
                self._trigger_alien_victory("Game over: aliens reached the ground")
                return

            if self.bunker_group:
                destroyed = pygame.sprite.spritecollide(alien, self.bunker_group, dokill=True)
                for bunker in destroyed:
                    logging.debug("Bunker destroyed by alien at %s", bunker.rect.topleft)

    def _trigger_alien_victory(self, reason: str):
        """Set the game over state due to alien advancement."""
        self._enter_game_over_state(reason)

    def _enter_game_over_state(self, reason: str) -> None:
        """Centralize transition into the GAME_OVER state."""
        if self.game_over:
            return
        self.game_over = True
        self.state_manager.change_state(GameState.GAME_OVER)
        self._game_over_return_time = pygame.time.get_ticks() + self.game_over_intro_delay_ms
        logging.info(reason)

    def _show_continue_screen(self) -> None:
        """Show the continue screen with countdown."""
        # Mark game as over when showing continue screen
        self.game_over = True

        # Store the current game mode for continue callbacks
        was_two_player = self.two_player_mode

        # Save snapshot of credits at start of continue screen
        # If player lets timer expire, we'll restore this value
        # (discarding any coins inserted during countdown)
        credits_at_continue_start = self.credit_count

        def on_continue_1p():
            """Callback when player continues with 1-player."""
            # 1P continue: requires 1 credit
            if self.credit_count > 0 and not was_two_player:
                self.credit_count -= 1
                self.game_over = False  # Reset for new game
                self.two_player_mode = False
                # Continue from current level, don't reset
                self.reset_game(start_playing=True)
                logging.info("Game continued (1P) from level %d with credits remaining=%02d",
                           self.level, self.credit_count)

        def on_continue_2p():
            """Callback when player continues with 2-player."""
            # 2P continue: requires 2 credits
            if self.credit_count >= 2 and was_two_player:
                self.credit_count -= 2
                self.game_over = False  # Reset for new game
                # Continue from current level, don't reset
                self.start_two_player_game()
                logging.info("Game continued (2P) from level %d with credits remaining=%02d",
                           self.level, self.credit_count)

        def on_timeout():
            """Callback when countdown reaches 0."""
            logging.info("Continue countdown expired, returning to menu. Restoring credits from %02d to %02d",
                        self.credit_count, credits_at_continue_start)
            # Restore credits to value at start of continue screen
            # This discards any coins inserted during countdown that weren't used
            self.credit_count = credits_at_continue_start
            self._return_to_intro_screen(trigger="continue_timeout")
            self.continue_screen = None

        self.continue_screen = ContinueScreen(
            on_continue_1p=on_continue_1p,
            on_continue_2p=on_continue_2p,
            on_timeout=on_timeout,
            credit_count=self.credit_count,
            is_two_player_mode=was_two_player  # Pass mode info to screen
        )

    def _start_next_wave(self) -> None:
        """Advance to the next wave when all aliens are cleared."""
        self.level += 1
        self.current_theme = get_level_theme(self.level)
        bonus_speed = min(0.05 * (self.level - 1), 0.6)
        self.wave_message_text = f"Level {self.level} - {self.current_theme.name}"
        self.wave_message_timer = pygame.time.get_ticks() + 2000
        self.level_start_ready_time = pygame.time.get_ticks() + self.level_start_delay_ms
        self.alien_group = self.create_aliens()
        self.bullet_group.empty()
        self.bomb_group.empty()
        self.ufo_group.empty()
        self._reset_alien_progression(speed_bonus=bonus_speed)
        logging.info("Advanced to level %d (%s)", self.level, self.current_theme.name)

    def _handle_resize(self, width: int, height: int):
        """Handle window resize events and keep the sprite viewer surface in sync."""
        width = max(1, width)
        height = max(1, height)
        if (width, height) == (self.window_width, self.window_height):
            return
        self.window_width, self.window_height = width, height
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        # Update sprite viewer target surface so it draws to the new window
        if self.sprite_viewer:
            self.sprite_viewer.screen = self.screen
        logging.info("Window resized to %dx%d", width, height)

    def _check_extra_lives(self):
        """Check if player has earned extra lives based on score milestones."""
        # First extra life at 20,000 points
        if self.score >= self.extra_lives_threshold and self.lives_awarded == 0:
            self.lives += 1
            self.lives_awarded += 1
            self.audio_manager.play_sound("extra_life")
            logging.info(f"Extra life awarded! Score: {self.score}, Lives: {self.lives}")

        # Additional extra lives every 70,000 points after the first
        if self.score >= self.extra_lives_threshold + (self.lives_awarded * self.extra_lives_interval):
            self.lives += 1
            self.lives_awarded += 1
            self.audio_manager.play_sound("extra_life")
            logging.info(f"Extra life awarded! Score: {self.score}, Lives: {self.lives}")

    def draw(self):
        # If viewing sprites, draw sprite viewer instead of game
        # Attract/demo state renders whichever animated scene is active
        self._update_music_state()
        if self.state_manager.current_state == GameState.ATTRACT:
            if not self.active_demo:
                self.active_demo = self.score_demo
                self.active_demo.start()
            self.active_demo.update()
            self.active_demo.draw(self.playfield_surface)
            self._present_playfield()
            if self.active_demo.is_finished():
                if self.demo_cycle_enabled:
                    self.demo_cycle_index = (self.demo_cycle_index + 1) % len(self.demo_cycle)
                    self.active_demo = self.demo_cycle[self.demo_cycle_index]
                    self.active_demo.start()
                else:
                    self.active_demo.start()
            return

        if self.viewing_sprites:
            self.sprite_viewer.draw_sprite_grid()
            pygame.display.flip()
            return

        # Normal game drawing
        surface = self.playfield_surface
        surface.fill(get_color("background"))

        # If in MENU state, draw the menu and credits
        if self.state_manager.current_state == GameState.MENU:
            self.menu.draw(surface)
            self._draw_menu_credits(surface)
            self._present_playfield()
            return

        self.player_group.draw(surface)
        self.alien_group.draw(surface)
        self.bunker_group.draw(surface)
        self.bullet_group.draw(surface)
        self.bomb_group.draw(surface)
        self.effects_group.draw(surface)
        self.ufo_group.draw(surface)

        self._draw_floating_texts(surface)
        self._draw_scoreboard(surface)

        if self.wave_message_timer > pygame.time.get_ticks():
            self._draw_wave_message()

        if self.waiting_for_respawn:
            self._draw_life_lost_message()

        if self.game_over:
            # Draw initials entry or continue screen (initials has priority)
            if self.initials_entry_screen and self.initials_entry_screen.is_active:
                self.initials_entry_screen.draw(surface)
            elif self.continue_screen and self.continue_screen.is_active:
                self.continue_screen.draw(surface)
            else:
                self._draw_game_over_message()

        if self.debug_sprite_borders:
            self._draw_debug_sprite_borders(surface)

        self._present_playfield()

    def _present_playfield(self):
        """Scale the logical playfield surface to the current window size."""
        window_width, window_height = self.screen.get_size()
        scale_x = window_width / self.logical_width
        scale_y = window_height / self.logical_height
        scale = min(scale_x, scale_y)
        scaled_width = max(1, int(self.logical_width * scale))
        scaled_height = max(1, int(self.logical_height * scale))
        scaled_surface = pygame.transform.scale(self.playfield_surface, (scaled_width, scaled_height))
        x_offset = (window_width - scaled_width) // 2
        y_offset = (window_height - scaled_height) // 2
        self.screen.fill(constants.BLACK)
        self.screen.blit(scaled_surface, (x_offset, y_offset))
        pygame.display.flip()

    def game_over_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    return True
            self.playfield_surface.fill(constants.BLACK)
            msg = self.font.render("GAME OVER - press R", True, constants.WHITE)
            rect = msg.get_rect(center=(self.logical_width // 2, self.logical_height // 2))
            self.playfield_surface.blit(msg, rect)
            self._present_playfield()
            self.clock.tick(60)

    def run(self):
        """
        Main game loop - handles the core game execution cycle.
        
        This method runs continuously until the game is quit, managing:
        - Event handling (input processing)
        - Game state updates (physics, collisions, AI)
        - Rendering (drawing all game objects)
        - Game over state transitions
        """
        while self.running:
            # Process all input events (keyboard, mouse, window events)
            self.handle_events()
            
            # Only update game logic during active play
            if (
                self.state_manager.current_state == GameState.PLAYING
                and not self.game_over
                and not self.viewing_sprites
            ):
                if pygame.time.get_ticks() >= self.level_start_ready_time:
                    self.update()
            
            # Always draw the current game state
            self.draw()

            # Trigger the demo again if the menu sits idle
            if (
                self.state_manager.current_state == GameState.MENU
                and self.settings_manager.intro_demo_enabled()
                and not any(
                    (
                        self.menu.showing_controls,
                        self.menu.showing_high_scores,
                        self.menu.showing_options,
                        self.menu.showing_credits,
                    )
                )
                and pygame.time.get_ticks() - self.attract_last_activity_time >= self.attract_idle_time
            ):
                self.start_intro_demo(cycle=True)
            
            # Handle game over state - show game over screen and wait for restart
            if self.game_over:
                if not self._game_over_processed:
                    # In 2-player mode, compare scores and save the winner's score
                    if self.two_player_mode:
                        winner_score = max(self.score, self.p2_score)
                        winner_player = 1 if self.score >= self.p2_score else 2
                        logging.info(f"2-Player game over. Winner: Player {winner_player} with {winner_score} points")
                    else:
                        winner_score = self.score
                        winner_player = 1

                    # Check if this is a high score
                    try:
                        is_high_score = self.high_score_manager.check_high_score(winner_score)
                        if is_high_score or self.high_score_manager.is_high_score_position(winner_score):
                            # Show initials entry screen
                            def on_initials_confirmed(initials: str):
                                """Callback when initials are confirmed."""
                                try:
                                    self.high_score_manager.update_score(winner_score, initials, player=winner_player)
                                    self.initials_entry_screen = None
                                    logging.info(f"High score saved: {winner_score} by {initials} (Player {winner_player})")
                                except Exception as e:
                                    logging.error(f"Error saving high score: {e}", exc_info=True)
                                    self.initials_entry_screen = None

                            self.initials_entry_screen = InitialsEntry(winner_score, on_initials_confirmed)
                        else:
                            # Just save the score without initials entry
                            try:
                                self.high_score_manager.update_score(winner_score, initials="---", player=winner_player)
                            except Exception as e:
                                logging.error(f"Error saving score: {e}", exc_info=True)
                    except Exception as e:
                        logging.error(f"Error checking high score: {e}", exc_info=True)

                    self._game_over_processed = True
                    logging.info("High score table updated after game over")

                # Handle initials entry input (has priority over continue screen)
                if self.initials_entry_screen and self.initials_entry_screen.is_active:
                    try:
                        keys = pygame.key.get_pressed()
                        self.initials_entry_screen.handle_input(keys)
                        self.initials_entry_screen.update()
                    except Exception as e:
                        logging.error(f"Error in initials entry: {e}", exc_info=True)
                        self.initials_entry_screen = None
                # Handle continue screen input
                elif self.continue_screen and self.continue_screen.is_active:
                    keys = pygame.key.get_pressed()
                    self.continue_screen.handle_input(keys)
                    self.continue_screen.update(dt_ms=16)
                    # Note: C key for credit insertion during continue is handled in handle_events()
                else:
                    # Normal game over controls
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_q]:
                        logging.info("Quit requested from game over overlay")
                        self.running = False
                    elif keys[pygame.K_r]:
                        self._return_to_intro_screen(trigger="key")
                    elif (
                        self._game_over_return_time is not None
                        and pygame.time.get_ticks() >= self._game_over_return_time
                    ):
                        self._return_to_intro_screen(trigger="timer")
            
            # Maintain consistent frame rate (60 FPS)
            self.clock.tick(60)
        
        # Clean up pygame resources when exiting
        pygame.quit()
    
    def _draw_game_over_message(self):
        """
        Draw the game over message overlay on the current screen.
        
        This method draws a semi-transparent overlay with game over text,
        final score, high score, and restart instructions without blocking the game loop.
        """
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.logical_width, self.logical_height))
        overlay.set_alpha(128)  # 50% transparency
        overlay.fill(constants.BLACK)
        self.playfield_surface.blit(overlay, (0, 0))
        
        # Draw game over text
        game_over_text = self.font.render("GAME OVER", True, constants.WHITE)
        final_score_text = self.font.render(f"Final Score: {self.score}", True, constants.WHITE)
        
        # Check if new high score
        is_high_score = self.high_score_manager.check_high_score(self.score)
        if is_high_score:
            high_score_color = constants.GREEN
            high_score_msg = f"NEW HIGH SCORE! {self.high_score_manager.get_high_score()}"
        else:
            high_score_color = constants.WHITE
            high_score_msg = f"Hi-Score: {self.high_score_manager.get_high_score()}"
        
        high_score_text = self.font.render(high_score_msg, True, high_score_color)
        restart_text = self.font.render("Press R to restart or Q to quit", True, constants.WHITE)
        
        # Center the text on screen
        center_x = self.logical_width // 2
        center_y = self.logical_height // 2
        game_over_rect = game_over_text.get_rect(center=(center_x, center_y - 50))
        final_score_rect = final_score_text.get_rect(center=(center_x, center_y - 20))
        high_score_rect = high_score_text.get_rect(center=(center_x, center_y + 10))
        restart_rect = restart_text.get_rect(center=(center_x, center_y + 50))
        
        self.playfield_surface.blit(game_over_text, game_over_rect)
        self.playfield_surface.blit(final_score_text, final_score_rect)
        self.playfield_surface.blit(high_score_text, high_score_rect)
        self.playfield_surface.blit(restart_text, restart_rect)

    def _draw_menu_credits(self, surface: pygame.Surface) -> None:
        """Draw credit count at the bottom of the menu screen."""
        width, height = surface.get_size()

        # Get font and color
        credit_font = get_font("menu_small")
        credit_color = (100, 255, 100) if self.credit_count > 0 else (255, 100, 100)

        # Render credit text
        credit_text = credit_font.render(f"CREDITS: {self.credit_count:02d}", True, credit_color)
        credit_rect = credit_text.get_rect(centerx=width // 2, y=height - 40)

        surface.blit(credit_text, credit_rect)

    def _return_to_intro_screen(self, trigger: str = "auto") -> None:
        """Reset play state and jump back to the intro/attract mode."""
        if not self.game_over:
            return
        logging.info("Returning to intro screen after game over (%s)", trigger)
        self.reset_game(start_playing=False)
        self.menu.update_options_state(
            self.sfx_enabled,
            self.settings_manager.intro_demo_enabled(),
            self.tint_enabled,
            self.music_enabled,
        )
        self.menu.hide_controls()
        self.menu.hide_high_scores()
        self.menu.hide_options()
        self.menu.hide_credits()
        self.demo_cycle_enabled = False
        self.active_demo = None
        self._game_over_processed = False
        self._game_over_return_time = None
        self.attract_last_activity_time = pygame.time.get_ticks()
        if self.settings_manager.intro_demo_enabled():
            self.start_intro_demo()
        else:
            self.state_manager.change_state(GameState.MENU)

    def _insert_credit(self, amount: int = 1) -> None:
        self.credit_count = min(99, self.credit_count + max(1, amount))
        self.attract_last_activity_time = pygame.time.get_ticks()
        # Update credit display in attract mode screens
        if self.score_demo:
            self.score_demo.set_credit_count(self.credit_count)
        # Update credit display in continue screen
        if self.continue_screen:
            self.continue_screen.set_credit_count(self.credit_count)
        logging.info("Credit inserted. Total=%02d", self.credit_count)

    def _spawn_explosion(self, position):
        tint = self._sprite_tint("explosion")
        self.effects_group.add(ExplosionEffect(position, tint=tint))

    def _draw_scoreboard(self, surface: pygame.Surface):
        width, _ = surface.get_size()
        margin = 6
        hud_color = get_color("hud_text")

        if self.two_player_mode:
            # 2-player HUD: "SCORE<1> [P1] HI-SCORE [HIGH] SCORE<2> [P2]"
            score1_label = self.small_font.render("SCORE<1>", True, hud_color)
            hi_label = self.hi_label_surface or self.small_font.render("HI-SCORE", True, hud_color)
            score2_label = self.small_font.render("SCORE<2>", True, hud_color)

            label_height = max(score1_label.get_height(), hi_label.get_height(), score2_label.get_height())

            # Left: Player 1 score
            score1_label_y = margin + (label_height - score1_label.get_height()) // 2
            surface.blit(score1_label, (10, score1_label_y))

            # Center: Hi-score
            hi_label_y = margin + (label_height - hi_label.get_height()) // 2
            hi_rect = hi_label.get_rect(midtop=(width // 2, hi_label_y))
            surface.blit(hi_label, hi_rect)

            # Right: Player 2 score
            score2_label_y = margin + (label_height - score2_label.get_height()) // 2
            score2_rect = score2_label.get_rect(topright=(width - 10, score2_label_y))
            surface.blit(score2_label, score2_rect)

            values_y = margin + label_height + 4
            score1_digits = self.digit_writer.render(f"{self.score:05d}")
            surface.blit(score1_digits, (10, values_y))

            hi_digits = self.digit_writer.render(f"{self.high_score_manager.get_high_score():05d}")
            hi_digits_rect = hi_digits.get_rect(midtop=(width // 2, values_y))
            surface.blit(hi_digits, hi_digits_rect)

            score2_digits = self.digit_writer.render(f"{self.p2_score:05d}")
            score2_digits_rect = score2_digits.get_rect(topright=(width - 10, values_y))
            surface.blit(score2_digits, score2_digits_rect)
        else:
            # 1-player HUD: "SCORE [P1] HI-SCORE [HIGH] LEVEL [LEVEL]"
            score_label = self.small_font.render("SCORE", True, hud_color)
            hi_label = self.hi_label_surface or self.small_font.render("HI-SCORE", True, hud_color)
            level_label = self.small_font.render("LEVEL", True, hud_color)

            label_height = max(score_label.get_height(), hi_label.get_height(), level_label.get_height())

            score_label_y = margin + (label_height - score_label.get_height()) // 2
            surface.blit(score_label, (10, score_label_y))

            hi_label_y = margin + (label_height - hi_label.get_height()) // 2
            hi_rect = hi_label.get_rect(midtop=(width // 2, hi_label_y))
            surface.blit(hi_label, hi_rect)

            level_label_y = margin + (label_height - level_label.get_height()) // 2
            level_label_rect = level_label.get_rect(topright=(width - 10, level_label_y))
            surface.blit(level_label, level_label_rect)

            values_y = margin + label_height + 4
            score_digits = self.digit_writer.render(f"{self.score:05d}")
            surface.blit(score_digits, (10, values_y))

            hi_digits = self.digit_writer.render(f"{self.high_score_manager.get_high_score():05d}")
            hi_digits_rect = hi_digits.get_rect(midtop=(width // 2, values_y))
            surface.blit(hi_digits, hi_digits_rect)

            level_digits = self.digit_writer.render(f"{self.level:02d}")
            level_digits_rect = level_digits.get_rect(topright=(width - 10, values_y))
            surface.blit(level_digits, level_digits_rect)

        self._draw_bottom_panel(surface)

    def _draw_bottom_panel(self, surface: pygame.Surface):
        width, height = surface.get_size()
        overlay_height = self.bottom_panel_height
        overlay_top = height - overlay_height
        pygame.draw.line(surface, get_color("divider"), (0, overlay_top), (width, overlay_top), 1)
        icon = self.life_icon_surface
        icons_right = 10
        # Get current player's lives (P2 lives if in 2P mode and current_player == 2)
        current_lives = self.p2_lives if (self.two_player_mode and self.current_player == 2) else self.lives
        if icon:
            for idx in range(min(current_lives, self.max_life_icons)):
                x = 10 + idx * (icon.get_width() + 4)
                surface.blit(icon, (x, overlay_top + 6))
                icons_right = x + icon.get_width()
        else:
            icons_right = 10

        # Draw current player indicator in 2-player mode
        if self.two_player_mode:
            player_text = self.small_font.render(f"PLAYER {self.current_player}", True, (255, 255, 0))
            surface.blit(player_text, (icons_right + 12, overlay_top + 6))
            status_text = self.small_font.render(
                f"SFX {'ON' if self.sfx_enabled else 'OFF'}  MUSIC {'ON' if self.music_enabled else 'OFF'}",
                True,
                get_color("hud_text"),
            )
            surface.blit(status_text, (icons_right + 12, overlay_top + 18))
        else:
            status_text = self.small_font.render(
                f"SFX {'ON' if self.sfx_enabled else 'OFF'}  MUSIC {'ON' if self.music_enabled else 'OFF'}",
                True,
                get_color("hud_text"),
            )
            surface.blit(status_text, (icons_right + 12, overlay_top + 8))

        credit_text = self.credit_label_surface
        digits = self.digit_writer.render(f"{self.credit_count:02d}")
        label_height = credit_text.get_height() if credit_text else digits.get_height()
        gap = 6 if credit_text else 0
        total_width = (credit_text.get_width() if credit_text else 0) + gap + digits.get_width()
        # Position credits on the right side of the screen
        start_x = width - total_width - 10
        start_y = overlay_top + 6
        if credit_text:
            surface.blit(credit_text, (start_x, start_y))
            start_x += credit_text.get_width() + gap
        surface.blit(digits, (start_x, start_y + label_height - digits.get_height()))

    def _draw_life_lost_message(self):
        """Overlay prompting the player to continue after losing a life."""
        overlay = pygame.Surface((self.logical_width, self.logical_height))
        overlay.set_alpha(160)
        overlay.fill((0, 0, 0))
        self.playfield_surface.blit(overlay, (0, 0))

        message = self.font.render("Ship destroyed!", True, constants.WHITE)
        instruction = self.font.render("Press SPACE to continue", True, constants.WHITE)
        remaining = self.font.render(f"Lives left: {self.lives}", True, constants.WHITE)

        center_x = self.logical_width // 2
        center_y = self.logical_height // 2
        self.playfield_surface.blit(message, message.get_rect(center=(center_x, center_y - 20)))
        self.playfield_surface.blit(instruction, instruction.get_rect(center=(center_x, center_y + 10)))
        self.playfield_surface.blit(remaining, remaining.get_rect(center=(center_x, center_y + 40)))

    def _add_floating_text(self, text, position, duration=900, color=constants.WHITE):
        """Add a temporary floating text label."""
        self.floating_texts.append({
            "text": text,
            "pos": position,
            "expires": pygame.time.get_ticks() + duration,
            "color": color,
        })

    def _draw_wave_message(self):
        """Show temporary wave text (e.g., 'Level 2')."""
        message = self.font.render(self.wave_message_text, True, constants.WHITE)
        rect = message.get_rect(center=(self.logical_width // 2, self.logical_height // 2))
        overlay = pygame.Surface((self.logical_width, self.logical_height))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 0))
        self.playfield_surface.blit(overlay, (0, 0))
        self.playfield_surface.blit(message, rect)

    def _draw_floating_texts(self, surface):
        """Render temporary floating score/signal text (e.g., UFO bonuses)."""
        now = pygame.time.get_ticks()
        self.floating_texts = [ft for ft in self.floating_texts if ft["expires"] > now]
        for ft in self.floating_texts:
            text_surf = self.small_font.render(ft["text"], True, ft["color"])
            rect = text_surf.get_rect(center=ft["pos"])
            surface.blit(text_surf, rect)

    def _draw_debug_sprite_borders(self, surface: pygame.Surface) -> None:
        color = constants.GREEN
        for sprite in self.player_group.sprites():
            pygame.draw.rect(surface, color, sprite.rect, 1)
        for sprite in self.alien_group.sprites():
            pygame.draw.rect(surface, color, sprite.rect, 1)
        for sprite in self.bunker_group.sprites():
            pygame.draw.rect(surface, color, sprite.rect, 1)
        for sprite in self.bullet_group.sprites():
            pygame.draw.rect(surface, color, sprite.rect, 1)
        for sprite in self.bomb_group.sprites():
            pygame.draw.rect(surface, color, sprite.rect, 1)
        for sprite in self.ufo_group.sprites():
            pygame.draw.rect(surface, color, sprite.rect, 1)


def main():
    Game().run()


if __name__ == "__main__":
    main()
