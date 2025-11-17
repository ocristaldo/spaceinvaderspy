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
from .systems.game_state_manager import GameStateManager, GameState

logging.basicConfig(
    level=logging.INFO,
    filename="game.log",
    filemode="w",
    format="%(asctime)s [%(levelname)s] %(message)s",
)

SCREEN_WIDTH = config.SCREEN_WIDTH
SCREEN_HEIGHT = config.SCREEN_HEIGHT


class Game:
    """Main game controller."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 16)
        self.running = True
        self.game_over = False

        # State management
        self.state_manager = GameStateManager()

        # Audio and scoring systems
        self.audio_manager = AudioManager()
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
        
        # Sprite viewer for testing
        self.sprite_viewer = SpriteViewer(self.screen)
        self.viewing_sprites = False
        self.menu = Menu(self.font)
        self.alien_speed = config.ALIEN_START_SPEED
        self.initial_alien_count = len(self.alien_group)
        self.last_ufo_time = pygame.time.get_ticks()
        logging.info("Game started. Player lives=%d. Audio muted by default (press 'A' to toggle)", self.lives)

    def reset_game(self):
        """Reset the game to initial state."""
        self.game_over = False
        self.score = 0
        self.lives = constants.LIVES_NUMBER
        self.lives_awarded = 0
        
        # Clear all sprite groups
        self.bullet_group.empty()
        self.bomb_group.empty()
        self.ufo_group.empty()
        
        # Reset player
        self.player = Player()
        self.player_group = pygame.sprite.GroupSingle(self.player)
        
        # Recreate aliens and bunkers
        self.alien_group = self.create_aliens()
        self.bunker_group = self.create_bunkers()
        
        # Reset alien movement
        self.alien_direction = 1
        self.alien_speed = config.ALIEN_START_SPEED
        self.initial_alien_count = len(self.alien_group)
        self.last_ufo_time = pygame.time.get_ticks()
        
        logging.info("Game reset complete")

    def create_aliens(self):
        group = pygame.sprite.Group()
        margin_x = config.ALIEN_MARGIN_X
        margin_y = config.ALIEN_MARGIN_Y
        spacing_x = config.ALIEN_SPACING_X
        spacing_y = config.ALIEN_SPACING_Y
        rows = config.ALIEN_ROWS
        cols = config.ALIEN_COLUMNS
        values = [30, 20, 20, 10, 10]  # Top row worth most points
        for row in range(rows):
            for col in range(cols):
                x = margin_x + col * spacing_x
                y = margin_y + row * spacing_y
                group.add(Alien(x, y, values[row]))
        return group

    def create_bunkers(self):
        group = pygame.sprite.Group()
        spacing = SCREEN_WIDTH // (constants.BLOCK_NUMBER + 1)
        y = SCREEN_HEIGHT - 60
        for i in range(constants.BLOCK_NUMBER):
            x = spacing * (i + 1)
            group.add(Bunker(x, y))
        return group

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
        
        # Check for sprite viewer key combinations (works both in game and sprite viewer)
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
            # Handle window close button
            if event.type == pygame.QUIT:
                self.running = False
                logging.info("Game quit via window close")

            # Handle keyboard key press events
            elif event.type == pygame.KEYDOWN:
                # R key: Exit sprite viewer or restart when game over
                if event.key == pygame.K_r:
                    if self.viewing_sprites:
                        self.viewing_sprites = False
                        logging.info("Exited sprite viewer mode")
                        continue
                    if self.game_over:
                        self.reset_game()
                        logging.info("Game restarted")
                        continue

                # Menu navigation when in MENU state
                if self.state_manager.current_state == GameState.MENU:
                    action = self.menu.handle_key(event.key)
                    if action == "start":
                        self.state_manager.change_state(GameState.PLAYING)
                        logging.info("Game started from menu")
                    elif action == "quit":
                        self.running = False
                        logging.info("Game quit from menu")
                    elif action == "options":
                        # Options not implemented yet
                        logging.info("Options selected (not implemented)")
                    continue

                # Spacebar: Fire bullet (only if no bullet currently active and playing)
                if event.key == pygame.K_SPACE and len(self.bullet_group) == 0 and self.state_manager.current_state == GameState.PLAYING and not self.viewing_sprites:
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
                    self.audio_manager.toggle_audio()
                    logging.info(f"Audio toggled: {'ON' if self.audio_manager.enabled else 'OFF'}")

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
        if not self.alien_group:
            return
        
        # 2% chance per frame to spawn a bomb (at 60 FPS = ~1.2 bombs per second)
        if random.random() < 0.02:
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
            self.ufo_group.add(UFO(-50, 50))  # Start UFO off-screen left
            self.last_ufo_time = now
            logging.info("UFO spawned")

    def update_alien_speed(self):
        """Increase alien speed as their numbers decrease."""
        remaining = len(self.alien_group)
        if remaining:
            self.alien_speed = (
                config.ALIEN_START_SPEED
                + (self.initial_alien_count - remaining) * config.ALIEN_SPEED_INCREMENT
            )

    def update(self):
        pressed = pygame.key.get_pressed()
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

            # Check if any alien hits the edge
            for alien in self.alien_group.sprites():
                if (alien.rect.right + move_x >= SCREEN_WIDTH - 10 or 
                    alien.rect.left + move_x <= 10):
                    move_down = True
                    self.alien_direction *= -1
                    break

            # Move aliens
            for alien in self.alien_group.sprites():
                if move_down:
                    alien.rect.y += 20  # Drop down when hitting edge
                    if alien.rect.bottom >= SCREEN_HEIGHT - 60:
                        self.game_over = True
                        self.state_manager.change_state(GameState.GAME_OVER)
                        logging.info("Game over: aliens reached bottom")
                else:
                    alien.rect.x += move_x

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

        # bullet vs bunker
        hits = pygame.sprite.groupcollide(self.bullet_group, self.bunker_group, True, False)
        for bunker_list in hits.values():
            for bunker in bunker_list:
                bunker.damage()
                logging.debug("Bunker damaged at %s", bunker.rect.topleft)

        # bomb vs bunker
        hits = pygame.sprite.groupcollide(self.bomb_group, self.bunker_group, True, False)
        for bunker_list in hits.values():
            for bunker in bunker_list:
                bunker.damage()
                logging.debug("Bunker hit by bomb at %s", bunker.rect.topleft)

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

        if not self.alien_group:
            self.game_over = True
            self.state_manager.change_state(GameState.GAME_OVER)
            logging.info("Game over: all aliens destroyed")

        # Check for extra lives milestones
        self._check_extra_lives()

        # Update bullets and bombs after handling collisions to keep frame semantics
        self.bullet_group.update()
        self.bomb_group.update()

        if self.game_over:
            logging.info("Game over detected")
            # Don't stop running immediately, let game_over_screen handle it

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
        if self.viewing_sprites:
            self.sprite_viewer.draw_sprite_grid()
        else:
            # Normal game drawing
            self.screen.fill(constants.BLACK)
            # If in MENU state, draw the menu and return
            if self.state_manager.current_state == GameState.MENU:
                self.menu.draw(self.screen)
                pygame.display.flip()
                return
            self.player_group.draw(self.screen)
            self.alien_group.draw(self.screen)
            self.bunker_group.draw(self.screen)
            self.bullet_group.draw(self.screen)
            self.bomb_group.draw(self.screen)
            self.ufo_group.draw(self.screen)

            # Draw HUD: Score, High Score, Lives, and Audio Status
            small_font = pygame.font.SysFont("monospace", 12)
            score_surf = self.font.render(f"Score: {self.score}", True, constants.WHITE)
            high_score_surf = self.font.render(f"Hi: {self.high_score_manager.get_high_score()}", True, constants.WHITE)
            lives_surf = self.font.render(f"Lives: {self.lives}", True, constants.WHITE)
            
            # Audio status indicator
            audio_status = "Audio: ON" if self.audio_manager.enabled else "Audio: OFF"
            audio_color = constants.GREEN if self.audio_manager.enabled else constants.RED
            audio_surf = small_font.render(audio_status, True, audio_color)
            
            self.screen.blit(score_surf, (10, 5))
            self.screen.blit(high_score_surf, (SCREEN_WIDTH // 2 - 50, 5))
            self.screen.blit(lives_surf, (SCREEN_WIDTH - lives_surf.get_width() - 10, 5))
            self.screen.blit(audio_surf, (10, SCREEN_HEIGHT - 25))
        
        pygame.display.flip()

    def game_over_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    return True
            self.screen.fill(constants.BLACK)
            msg = self.font.render("GAME OVER - press R", True, constants.WHITE)
            rect = msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(msg, rect)
            pygame.display.flip()
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
            
            # Only update game logic if not in game over state and not viewing sprites
            if not self.game_over and not self.viewing_sprites:
                self.update()
            
            # Always draw the current game state
            self.draw()
            
            # Handle game over state - show game over screen and wait for restart
            if self.game_over:
                # Update high score on first game over frame
                if not hasattr(self, '_game_over_processed'):
                    self.high_score_manager.update_score(self.score)
                    self._game_over_processed = True
                
                # Draw game over message on current screen
                self._draw_game_over_message()
                pygame.display.flip()
                
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
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)  # 50% transparency
        overlay.fill(constants.BLACK)
        self.screen.blit(overlay, (0, 0))
        
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
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(final_score_text, final_score_rect)
        self.screen.blit(high_score_text, high_score_rect)
        self.screen.blit(restart_text, restart_rect)


def main():
    Game().run()


if __name__ == "__main__":
    main()
