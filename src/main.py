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
import pygame
import random
from . import constants
from . import config
from .entities.player import Player
from .entities.alien import Alien
from .entities.bullet import Bullet, Bomb
from .entities.bunker import Bunker
from .entities.ufo import UFO
from .utils.sprite_viewer import SpriteViewer
from .utils.audio_manager import AudioManager
from .utils.high_score_manager import HighScoreManager
from .ui.menu import Menu
from .ui.start_screen_demo import ScoreTableDemo, WaveFormationDemo
from .systems.game_state_manager import GameStateManager, GameState
from .utils.settings_manager import SettingsManager

logging.basicConfig(
    level=logging.INFO,
    filename="game.log",
    filemode="w",
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def _install_global_exception_logger():
    def handle_exception(exc_type, exc_value, exc_traceback):
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
        self.font = pygame.font.SysFont("monospace", 16)
        self.small_font = pygame.font.SysFont("monospace", 12)
        menu_font_size = max(18, int(14 * config.PLAYFIELD_SCALE))
        menu_body_size = max(14, int(12 * config.PLAYFIELD_SCALE))
        self.menu_font = pygame.font.SysFont("monospace", menu_font_size)
        self.menu_body_font = pygame.font.SysFont("monospace", menu_body_size)
        self.running = True
        self.game_over = False
        self.waiting_for_respawn = False
        self.level = 1
        self.wave_message_text = ""
        self.wave_message_timer = 0
        self.floating_texts = []
        self.settings_manager = SettingsManager()
        self.level_start_delay_ms = 1500
        self.level_start_ready_time = 0

        # State management
        self.state_manager = GameStateManager()

        # Audio and scoring systems
        self.audio_manager = AudioManager()
        if self.settings_manager.audio_enabled() and not self.audio_manager.enabled:
            self.audio_manager.toggle_audio()
        self.high_score_manager = HighScoreManager()

        self.score = 0
        self.lives = constants.LIVES_NUMBER
        self.extra_lives_threshold = 20000  # Extra life at 20k, then every 70k
        self.extra_lives_interval = 70000
        self.lives_awarded = 0  # Track how many extra lives have been awarded

        self.player = Player()
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.bullet_group = pygame.sprite.Group()
        self.bomb_group = pygame.sprite.Group()
        self.bunker_group = self.create_bunkers()
        self.ufo_group = pygame.sprite.Group()

        self.alien_group = self.create_aliens()
        self.alien_direction = 1
        self._reset_alien_progression()
        
        # Sprite viewer for testing
        self.sprite_viewer = SpriteViewer(self.screen)
        self.viewing_sprites = False
        self.menu = Menu(self.menu_font, self.menu_body_font)
        self.menu.update_options_state(self.audio_manager.enabled, self.settings_manager.intro_demo_enabled())
        self.score_demo = ScoreTableDemo()
        self.start_screen_demo = self.score_demo  # Backwards-compatibility for older tests/utilities
        self.wave_demo = WaveFormationDemo()
        self.demo_cycle = [self.score_demo, self.wave_demo]
        self.demo_cycle_enabled = False
        self.demo_cycle_index = 0
        self.active_demo = None
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
        audio_status = "ON" if self.audio_manager.enabled else "muted (press 'A' to toggle)"
        logging.info("Game started. Player lives=%d. Audio %s", self.lives, audio_status)

    @property
    def state(self):
        """Backwards-compatible string state for existing tests/utilities."""
        return self.state_manager.current_state.name

    def reset_game(self):
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
        self.state_manager.change_state(GameState.PLAYING)
        
        # Clear all sprite groups
        self.bullet_group.empty()
        self.bomb_group.empty()
        self.ufo_group.empty()
        
        # Reset player
        self._respawn_player()
        
        # Recreate aliens and bunkers
        self.alien_group = self.create_aliens()
        self.bunker_group = self.create_bunkers()
        
        # Reset alien movement
        self.alien_direction = 1
        self._reset_alien_progression()
        self.last_ufo_time = pygame.time.get_ticks()
        
        logging.info("Game reset complete")

    def create_aliens(self):
        group = pygame.sprite.Group()
        margin_y = config.ALIEN_MARGIN_Y
        spacing_y = config.ALIEN_SPACING_Y
        rows = config.ALIEN_ROWS
        cols = config.ALIEN_COLUMNS
        base_values = [30, 20, 20, 10, 10]  # Top row worth most points
        values = base_values[:rows]

        # Get sprite dimensions for centering
        from .utils.sprite_sheet import get_game_sprite
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
                group.add(Alien(x, y, value))
        return group

    def create_bunkers(self):
        group = pygame.sprite.Group()
        spacing = self.logical_width // (constants.BLOCK_NUMBER + 1)
        player_top = self.player.rect.top
        bunker_bottom = max(0, player_top - config.BUNKER_PLAYER_GAP)
        for i in range(constants.BLOCK_NUMBER):
            center_x = spacing * (i + 1)
            group.add(Bunker(center_x, bunker_bottom))
        return group

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

    def _toggle_audio_setting(self):
        """Toggle audio and persist the setting."""
        self.audio_manager.toggle_audio()
        self.settings_manager.set_audio_enabled(self.audio_manager.enabled)
        self.menu.update_options_state(self.audio_manager.enabled, self.settings_manager.intro_demo_enabled())
        logging.info("Audio toggled: %s", "ON" if self.audio_manager.enabled else "OFF")

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
                        self.reset_game()
                        logging.info("Game restarted")
                        continue

                if self.state_manager.current_state == GameState.ATTRACT:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self._finish_intro_demo(forced=True)
                    continue

                # Menu navigation when in MENU state
                if self.state_manager.current_state == GameState.MENU:
                    if self.menu.showing_options:
                        if event.key == pygame.K_d:
                            self.start_intro_demo(triggered_from_options=True, cycle=True)
                            continue
                        if event.key == pygame.K_i:
                            new_state = not self.settings_manager.intro_demo_enabled()
                            self.settings_manager.set_intro_demo_enabled(new_state)
                            self.menu.update_options_state(self.audio_manager.enabled, new_state)
                            logging.info("Intro demo autoplay %s", "enabled" if new_state else "disabled")
                            continue
                    if event.key == pygame.K_a:
                        self._toggle_audio_setting()
                        continue
                    if not self.menu.showing_options and event.key == pygame.K_d:
                        self.start_intro_demo(triggered_from_options=True, cycle=True)
                        continue
                    action = self.menu.handle_key(event.key)
                    if action == "start":
                        self.reset_game()
                        logging.info("Game started from menu")
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
                            self.audio_manager.enabled,
                            self.settings_manager.intro_demo_enabled(),
                            self.debug_sprite_borders,
                        )
                        logging.info("Options overlay opened from menu")
                    elif action == "options_toggle_audio":
                        self._toggle_audio_setting()
                        continue
                    elif action == "options_play_demo":
                        self.menu.hide_options()
                        self.start_intro_demo(triggered_from_options=True, cycle=True)
                        continue
                    elif action == "options_toggle_autodemo":
                        new_state = not self.settings_manager.intro_demo_enabled()
                        self.settings_manager.set_intro_demo_enabled(new_state)
                        self.menu.update_options_state(self.audio_manager.enabled, new_state)
                        logging.info("Intro demo autoplay %s", "enabled" if new_state else "disabled")
                        continue
                    elif action == "options_toggle_borders":
                        self._set_debug_borders(not self.debug_sprite_borders)
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

                # A key: Toggle audio on/off
                if event.key == pygame.K_a:
                    # If options overlay open or during play, allow toggling audio
                    if self.menu.showing_options or self.state_manager.current_state == GameState.PLAYING:
                        self._toggle_audio_setting()

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
            bomb = Bomb(alien.rect.midbottom)
            self.bomb_group.add(bomb)
            logging.debug("Alien bomb spawned at %s from alien at %s", 
                         bomb.rect.topleft, alien.rect.topleft)

    def spawn_ufo(self):
        now = pygame.time.get_ticks()
        if now - self.last_ufo_time > config.UFO_INTERVAL:
            self.ufo_group.add(UFO(-60, 40))  # Start UFO slightly higher
            self.last_ufo_time = now
            logging.info("UFO spawned")

    def update_alien_speed(self):
        """Increase alien speed as their numbers decrease."""
        remaining = len(self.alien_group)
        if remaining and self.initial_alien_count:
            progress = 1.0 - (remaining / self.initial_alien_count)
            max_speed = config.ALIEN_MAX_SPEED
            base = config.ALIEN_START_SPEED
            self.alien_speed = base + progress * (max_speed - base)

    def update(self):
        pressed = pygame.key.get_pressed()
        if self.waiting_for_respawn:
            return
        self.player_group.update(pressed)
        # Update non-projectile entities first
        self.ufo_group.update()

        # Animate aliens every 30 frames (0.5 seconds at 60 FPS)
        if pygame.time.get_ticks() % 500 < 16:  # Roughly every 0.5 seconds
            for alien in self.alien_group:
                alien.animate()

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
                self.score += alien.value
                logging.info("Alien destroyed at %s", alien.rect.topleft)
        if hits:
            self.update_alien_speed()

        hits = pygame.sprite.groupcollide(self.bullet_group, self.ufo_group, True, True)
        for bullet, ufos in hits.items():
            for ufo in ufos:
                self.score += ufo.value
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
            self.lives -= len(hit_bombs)
            logging.warning("Player hit! Lives left=%d", self.lives)
            if self.lives <= 0:
                self.game_over = True
                self.state_manager.change_state(GameState.GAME_OVER)
                logging.info("Game over: player destroyed")
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

        if self.game_over:
            logging.info("Game over detected")
            # Don't stop running immediately, let game_over_screen handle it

    def _reset_alien_progression(self, speed_bonus: float = 0.0):
        """Reset alien speed progression to the slow starting pace."""
        self.initial_alien_count = len(self.alien_group)
        self.alien_speed = config.ALIEN_START_SPEED + speed_bonus

    def _respawn_player(self):
        """Respawn the player ship at the starting position."""
        self.player = Player()
        self.player_group = pygame.sprite.GroupSingle(self.player)

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
        self.game_over = True
        self.state_manager.change_state(GameState.GAME_OVER)
        logging.info(reason)

    def _start_next_wave(self):
        """Advance to the next wave when all aliens are cleared."""
        self.level += 1
        bonus_speed = min(0.05 * (self.level - 1), 0.6)
        self.wave_message_text = f"Level {self.level}"
        self.wave_message_timer = pygame.time.get_ticks() + 2000
        self.level_start_ready_time = pygame.time.get_ticks() + self.level_start_delay_ms
        self.alien_group = self.create_aliens()
        self.bullet_group.empty()
        self.bomb_group.empty()
        self.ufo_group.empty()
        self._reset_alien_progression(speed_bonus=bonus_speed)
        logging.info("Advanced to level %d", self.level)

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
        surface.fill(constants.BLACK)

        # If in MENU state, draw the menu and return
        if self.state_manager.current_state == GameState.MENU:
            self.menu.draw(surface)
            self._present_playfield()
            return

        self.player_group.draw(surface)
        self.alien_group.draw(surface)
        self.bunker_group.draw(surface)
        self.bullet_group.draw(surface)
        self.bomb_group.draw(surface)
        self.ufo_group.draw(surface)

        # Draw HUD: Score, High Score, Lives, and Audio Status
        surface_width, surface_height = surface.get_size()
        score_surf = self.font.render(f"Score: {self.score}", True, constants.WHITE)
        high_score = self.high_score_manager.get_high_score()
        high_score_surf = self.font.render(f"Hi: {high_score}", True, constants.WHITE)
        lives_surf = self.font.render(f"Lives: {self.lives}", True, constants.WHITE)
        level_surf = self.font.render(f"Level: {self.level}", True, constants.WHITE)
        
        # Audio status indicator
        audio_status = "Audio: ON" if self.audio_manager.enabled else "Audio: OFF"
        audio_color = constants.GREEN if self.audio_manager.enabled else constants.RED
        audio_surf = self.small_font.render(audio_status, True, audio_color)
        
        surface.blit(score_surf, (10, 5))
        high_score_rect = high_score_surf.get_rect(midtop=(surface_width // 2, 5))
        surface.blit(high_score_surf, high_score_rect)
        surface.blit(lives_surf, (surface_width - lives_surf.get_width() - 10, 5))
        surface.blit(level_surf, (surface_width - level_surf.get_width() - 10, 30))
        surface.blit(audio_surf, (10, surface_height - audio_surf.get_height() - 10))

        self._draw_floating_texts(surface)

        if self.wave_message_timer > pygame.time.get_ticks():
            self._draw_wave_message()

        if self.waiting_for_respawn:
            self._draw_life_lost_message()

        if self.game_over:
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
                # Update high score on first game over frame
                if not hasattr(self, '_game_over_processed'):
                    self.high_score_manager.update_score(self.score)
                    self._game_over_processed = True
                
                # Check for restart input without blocking the main loop
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    self._game_over_processed = False
                    self.reset_game()
                    logging.info("Game restarted after game over")
            
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
