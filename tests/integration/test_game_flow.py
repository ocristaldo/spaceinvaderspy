"""
Integration tests for game flow and restart functionality.
"""
import os
import sys
import unittest

import pygame

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src import constants
from src.main import Game


class TestGameFlow(unittest.TestCase):
    """Test cases for complete game flow scenarios."""

    @classmethod
    def setUpClass(cls):
        """Set up pygame for testing."""
        pygame.init()
        pygame.display.set_mode((1, 1))  # Minimal display for testing

    def setUp(self):
        """Set up test fixtures."""
        self.game = Game()

    def tearDown(self):
        """Clean up after each test."""
        if hasattr(self.game, 'running'):
            self.game.running = False

    def test_game_initialization(self):
        """Test game initializes correctly."""
        self.assertFalse(self.game.game_over)
        self.assertTrue(self.game.running)
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.lives, constants.LIVES_NUMBER)
        self.assertIsNotNone(self.game.alien_group)
        self.assertGreater(len(self.game.alien_group), 0)

    def test_game_over_state(self):
        """Test game over state is handled correctly."""
        # Force game over
        self.game.lives = 0
        self.game.game_over = True

        # Verify game over state
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.lives, 0)

    def test_restart_functionality(self):
        """Test game restart works correctly."""
        # Modify game state
        self.game.score = 1000
        self.game.lives = 1
        self.game.game_over = True
        self.game.alien_group.empty()
        # Add a real bullet object for testing
        from src.entities.bullet import Bullet
        bullet = Bullet((100, 100))
        self.game.bullet_group.add(bullet)

        # Test reset
        initial_alien_count = len(self.game.alien_group)
        self.game.reset_game()

        # Verify reset worked
        self.assertFalse(self.game.game_over)
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.lives, constants.LIVES_NUMBER)
        self.assertEqual(len(self.game.bullet_group), 0)
        self.assertGreater(len(self.game.alien_group), initial_alien_count)

    def test_alien_destruction_advances_wave(self):
        """Clearing all aliens should advance to the next wave."""
        self.game.alien_group.empty()
        current_level = self.game.level
        self.game.update()
        self.assertFalse(self.game.game_over)
        self.assertEqual(self.game.level, current_level + 1)
        self.assertGreater(len(self.game.alien_group), 0)

    def test_alien_reaching_player_triggers_defeat(self):
        """Test defeat condition when an alien collides with the player."""
        alien = next(iter(self.game.alien_group))
        alien.rect.center = self.game.player.rect.center
        self.game.update()
        self.assertTrue(self.game.game_over)

    def test_player_death_defeat(self):
        """Test defeat condition when player loses all lives."""
        # Set player to 1 life
        self.game.lives = 1

        # Simulate player getting hit
        from src.entities.bullet import Bomb
        bomb = Bomb((self.game.player.rect.centerx, self.game.player.rect.centery))
        self.game.bomb_group.add(bomb)

        # Update to trigger collision
        self.game.update()

        # Should trigger game over when lives reach 0
        self.assertEqual(self.game.lives, 0)
        self.assertTrue(self.game.game_over)


class TestErrorScenarios(unittest.TestCase):
    """Test error handling and edge cases."""

    @classmethod
    def setUpClass(cls):
        """Set up pygame for testing."""
        pygame.init()
        pygame.display.set_mode((1, 1))

    def test_empty_alien_group_handling(self):
        """Test game handles empty alien group by starting next wave."""
        game = Game()
        game.alien_group.empty()
        game.spawn_bomb()
        game.update()
        self.assertFalse(game.game_over)
        self.assertEqual(game.level, 2)

    def test_multiple_resets(self):
        """Test multiple consecutive resets work correctly."""
        game = Game()

        for i in range(5):
            # Modify state
            game.score = i * 100
            game.game_over = True

            # Reset
            game.reset_game()

            # Verify clean state
            self.assertFalse(game.game_over)
            self.assertEqual(game.score, 0)
            self.assertEqual(game.lives, constants.LIVES_NUMBER)

    def test_collision_edge_cases(self):
        """Test collision detection edge cases."""
        game = Game()

        # Test with empty groups
        game.bullet_group.empty()
        game.alien_group.empty()
        game.bomb_group.empty()

        # Should not crash
        game.update()

        # Verify next wave started instead of game over
        self.assertFalse(game.game_over)
        self.assertEqual(game.level, 2)


if __name__ == '__main__':
    unittest.main()
