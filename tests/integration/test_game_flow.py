"""
Integration tests for game flow and restart functionality.
"""
import unittest
import pygame
import sys
import os
import time

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.main import Game
from src import constants


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
    
    def test_alien_destruction_victory(self):
        """Test victory condition when all aliens destroyed."""
        # Remove all aliens
        self.game.alien_group.empty()
        
        # Simulate update cycle
        self.game.update()
        
        # Should trigger game over
        self.assertTrue(self.game.game_over)
    
    def test_alien_invasion_defeat(self):
        """Test defeat condition when aliens reach bottom."""
        # Move aliens to bottom of screen (below the trigger threshold)
        # The threshold in main.py is SCREEN_HEIGHT - 60
        from src import config
        for alien in self.game.alien_group:
            alien.rect.bottom = config.SCREEN_HEIGHT - 50  # Below the threshold
            # Position alien at right edge to force move_down
            alien.rect.right = config.SCREEN_WIDTH - 5
        
        # Force move_down to trigger the check
        self.game.alien_direction = 1
        
        # Simulate update cycle
        self.game.update()
        
        # Should trigger game over
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
        
        # Should trigger game over
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.lives, 0)


class TestErrorScenarios(unittest.TestCase):
    """Test error handling and edge cases."""
    
    @classmethod
    def setUpClass(cls):
        """Set up pygame for testing."""
        pygame.init()
        pygame.display.set_mode((1, 1))
    
    def test_empty_alien_group_handling(self):
        """Test game handles empty alien group correctly."""
        game = Game()
        game.alien_group.empty()
        
        # Should not crash when spawning bombs
        game.spawn_bomb()
        
        # Should not crash during update
        game.update()
        
        # Should trigger victory condition
        self.assertTrue(game.game_over)
    
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
        
        # Verify game over triggered (no aliens = victory)
        self.assertTrue(game.game_over)


if __name__ == '__main__':
    unittest.main()
