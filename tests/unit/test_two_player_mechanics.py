"""
Comprehensive tests for 2-player mechanics including hit-based switching and state persistence.
Tests Phase 1.3 features: hit-based switching and independent game state.
"""
import pygame
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.main import Game
from src.entities.bullet import Bomb
from src.systems.game_state_manager import GameState


class TestHitBasedSwitching:
    """Tests for hit-based player switching on every bomb hit."""

    def setup_method(self):
        """Initialize pygame and create a game instance."""
        pygame.init()
        pygame.display.set_mode((1, 1))
        self.game = Game()

    def teardown_method(self):
        """Clean up after tests."""
        pygame.quit()

    def test_player1_hit_switches_to_player2_if_alive(self):
        """When P1 is hit and P2 has lives, switch to P2."""
        self.game.start_two_player_game()
        self.game.state_manager.change_state(GameState.PLAYING)

        assert self.game.current_player == 1
        assert self.game.lives == 3
        assert self.game.p2_lives == 3

        # Hit player 1
        bomb = Bomb((self.game.player.rect.centerx, self.game.player.rect.centery))
        bomb.rect.center = self.game.player.rect.center
        self.game.bomb_group.add(bomb)
        self.game.update()

        # Should switch to player 2
        assert self.game.current_player == 2
        assert self.game.lives == 2  # P1 lost one life
        assert self.game.p2_lives == 3  # P2 unchanged

    def test_player2_hit_switches_to_player1_if_alive(self):
        """When P2 is hit and P1 has lives, switch to P1."""
        self.game.start_two_player_game()
        self.game.state_manager.change_state(GameState.PLAYING)

        # Manually switch to P2
        self.game.switch_player()
        assert self.game.current_player == 2

        # Hit player 2
        bomb = Bomb((self.game.player.rect.centerx, self.game.player.rect.centery))
        bomb.rect.center = self.game.player.rect.center
        self.game.bomb_group.add(bomb)
        self.game.update()

        # Should switch to player 1
        assert self.game.current_player == 1
        assert self.game.lives == 3  # P1 unchanged
        assert self.game.p2_lives == 2  # P2 lost one life

    def test_player1_zero_lives_with_player2_alive_continues_with_p2(self):
        """When P1 at 0 lives but P2 alive, P1 stays dead and P2 continues."""
        self.game.start_two_player_game()
        self.game.state_manager.change_state(GameState.PLAYING)

        # Set P1 to 1 life
        self.game.lives = 1
        self.game.p2_lives = 3

        # Hit player 1 (goes to 0 lives)
        bomb = Bomb((self.game.player.rect.centerx, self.game.player.rect.centery))
        bomb.rect.center = self.game.player.rect.center
        self.game.bomb_group.add(bomb)
        self.game.update()

        # Should switch to player 2
        assert self.game.current_player == 2
        assert self.game.lives == 0
        assert self.game.p2_lives == 3
        assert not self.game.game_over  # Not yet game over

    def test_both_players_zero_lives_shows_continue_screen(self):
        """When both players at 0 lives, show continue screen."""
        self.game.start_two_player_game()
        self.game.state_manager.change_state(GameState.PLAYING)

        # Set both to 1 life
        self.game.lives = 1
        self.game.p2_lives = 1

        # Hit player 1 (goes to 0 lives), P2 still at 1
        bomb = Bomb((self.game.player.rect.centerx, self.game.player.rect.centery))
        bomb.rect.center = self.game.player.rect.center
        self.game.bomb_group.add(bomb)
        self.game.update()

        # Switched to P2
        assert self.game.current_player == 2
        assert self.game.lives == 0
        assert self.game.p2_lives == 1

        # Hit player 2 (goes to 0 lives)
        bomb = Bomb((self.game.player.rect.centerx, self.game.player.rect.centery))
        bomb.rect.center = self.game.player.rect.center
        self.game.bomb_group.add(bomb)
        self.game.update()

        # Both out of lives - should show continue screen and set game_over
        assert self.game.lives == 0
        assert self.game.p2_lives == 0
        assert self.game.game_over
        assert self.game.continue_screen is not None

    def test_player_with_zero_lives_shows_continue_screen_on_hit(self):
        """When both at 0 lives and hit, continue screen is displayed."""
        self.game.start_two_player_game()
        self.game.state_manager.change_state(GameState.PLAYING)

        # Set both to 0 lives
        self.game.lives = 0
        self.game.p2_lives = 0

        # Hit current player
        bomb = Bomb((self.game.player.rect.centerx, self.game.player.rect.centery))
        bomb.rect.center = self.game.player.rect.center
        self.game.bomb_group.add(bomb)
        self.game.update()

        # Continue screen should be shown and game_over should be set
        assert self.game.game_over
        assert self.game.continue_screen is not None


class TestGameStatePersistence:
    """Tests for independent game state persistence per player."""

    def setup_method(self):
        """Initialize pygame and create a game instance."""
        pygame.init()
        pygame.display.set_mode((1, 1))
        self.game = Game()

    def teardown_method(self):
        """Clean up after tests."""
        pygame.quit()

    def test_player_states_initialized_at_game_start(self):
        """Player states are initialized when 2-player game starts."""
        self.game.start_two_player_game()

        # Both players should have initialized states
        assert 1 in self.game.player_states
        assert 2 in self.game.player_states

        # has_been_saved should be False initially
        assert self.game.player_states[1]['has_been_saved'] is False
        assert self.game.player_states[2]['has_been_saved'] is False

    def test_player2_starts_fresh_at_level1(self):
        """When first switching to P2, they start at level 1 fresh."""
        self.game.start_two_player_game()
        self.game.state_manager.change_state(GameState.PLAYING)

        # Set P1 to level 3
        self.game.level = 3
        initial_alien_count = len(self.game.alien_group)

        # Switch to P2 (first time)
        self.game.switch_player()

        # P2 should start fresh at level 1
        assert self.game.current_player == 2
        assert self.game.level == 1
        # Note: alien count depends on implementation, but should be fresh

    def test_player1_resumes_saved_state(self):
        """When returning to P1 after switch, resume saved state."""
        self.game.start_two_player_game()
        self.game.state_manager.change_state(GameState.PLAYING)

        # Advance P1 to level 2
        self.game.level = 2
        initial_alien_count = len(self.game.alien_group)

        # Switch to P2
        self.game.switch_player()
        assert self.game.current_player == 2
        assert self.game.level == 1

        # Switch back to P1
        self.game.switch_player()

        # P1 should resume at level 2
        assert self.game.current_player == 1
        assert self.game.level == 2

    def test_independent_levels_for_both_players(self):
        """P1 and P2 maintain independent level progression."""
        self.game.start_two_player_game()
        self.game.state_manager.change_state(GameState.PLAYING)

        # P1 at level 2
        self.game.level = 2
        self.game.switch_player()

        # P2 should be at level 1
        assert self.game.level == 1

        # Advance P2 to level 3
        self.game.level = 3
        self.game.switch_player()

        # P1 should still be at level 2
        assert self.game.level == 2
        self.game.switch_player()

        # P2 should still be at level 3
        assert self.game.level == 3

    def test_player_state_saved_on_switch(self):
        """Player state is saved when switching away."""
        self.game.start_two_player_game()
        self.game.state_manager.change_state(GameState.PLAYING)

        # Modify P1 state
        self.game.level = 2
        aliens_before = len(self.game.alien_group)

        # Switch to P2
        self.game.switch_player()

        # P1 state should be marked as saved
        assert self.game.player_states[1]['has_been_saved'] is True

    def test_only_first_switch_starts_fresh(self):
        """First switch to a player starts fresh, subsequent switches restore."""
        self.game.start_two_player_game()
        self.game.state_manager.change_state(GameState.PLAYING)

        # First switch to P2 - starts fresh
        self.game.switch_player()
        assert self.game.player_states[2]['has_been_saved'] is False
        self.game.level = 3

        # Switch back to P1
        self.game.switch_player()
        assert self.game.level == 1  # P1 at level 1

        # Switch to P2 - should restore level 3
        self.game.switch_player()
        assert self.game.level == 3

    def test_independent_alien_positions(self):
        """Alien positions are independent per player."""
        self.game.start_two_player_game()
        self.game.state_manager.change_state(GameState.PLAYING)

        # P1 has some aliens
        aliens_p1 = len(self.game.alien_group)

        # Switch to P2 (fresh start)
        self.game.switch_player()
        aliens_p2 = len(self.game.alien_group)

        # Both should have aliens (fresh formation)
        assert aliens_p1 > 0
        assert aliens_p2 > 0

        # Switch back
        self.game.switch_player()
        assert len(self.game.alien_group) == aliens_p1


class TestSinglePlayerModeUnaffected:
    """Tests to ensure 1P mode still works correctly."""

    def setup_method(self):
        """Initialize pygame and create a game instance."""
        pygame.init()
        pygame.display.set_mode((1, 1))
        self.game = Game()

    def teardown_method(self):
        """Clean up after tests."""
        pygame.quit()

    def test_single_player_mode_not_affected(self):
        """1-player mode should work without state persistence logic."""
        self.game.reset_game(start_playing=True)
        assert not self.game.two_player_mode
        assert self.game.current_player == 1
        assert self.game.level == 1

    def test_single_player_no_switch_on_hit(self):
        """In 1P mode, getting hit doesn't switch players."""
        self.game.reset_game(start_playing=True)
        self.game.state_manager.change_state(GameState.PLAYING)

        self.game.lives = 1

        # Hit player
        bomb = Bomb((self.game.player.rect.centerx, self.game.player.rect.centery))
        bomb.rect.center = self.game.player.rect.center
        self.game.bomb_group.add(bomb)
        self.game.update()

        # Should still be player 1
        assert self.game.current_player == 1
        assert self.game.lives == 0
        assert self.game.game_over
        assert self.game.continue_screen is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
