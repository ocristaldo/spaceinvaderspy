"""
Unit tests for game entities.
"""
import unittest
import pygame
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.entities.player import Player
from src.entities.alien import Alien
from src.entities.bullet import Bullet
from src.entities.bunker import Bunker
from src import config


class TestPlayer(unittest.TestCase):
    """Test cases for Player entity."""
    
    @classmethod
    def setUpClass(cls):
        """Set up pygame for testing."""
        pygame.init()
        pygame.display.set_mode((1, 1))  # Minimal display for testing
    
    def setUp(self):
        """Set up test fixtures."""
        self.player = Player()
    
    def test_player_initialization(self):
        """Test player is initialized correctly."""
        self.assertIsNotNone(self.player.image)
        self.assertIsNotNone(self.player.rect)
        self.assertEqual(self.player.speed, 5)
    
    def test_player_movement(self):
        """Test player movement."""
        initial_x = self.player.rect.x
        
        # Create a proper mock for pygame.key.get_pressed()
        import unittest.mock
        with unittest.mock.patch('pygame.key.get_pressed') as mock_keys:
            # Mock left key pressed
            mock_keys.return_value = {pygame.K_LEFT: True, pygame.K_RIGHT: False}
            
            # Create a mock pressed object that behaves like pygame keys
            pressed = unittest.mock.MagicMock()
            pressed.__getitem__ = lambda self, key: key == pygame.K_LEFT
            
            self.player.update(pressed)
            self.assertLess(self.player.rect.x, initial_x)


class TestAlien(unittest.TestCase):
    """Test cases for Alien entity."""
    
    @classmethod
    def setUpClass(cls):
        """Set up pygame for testing."""
        pygame.init()
        pygame.display.set_mode((1, 1))
    
    def test_alien_initialization(self):
        """Test alien is initialized correctly."""
        alien = Alien(100, 100, 30)
        self.assertIsNotNone(alien.image)
        self.assertIsNotNone(alien.rect)
        self.assertEqual(alien.value, 30)
        self.assertEqual(alien.rect.x, 100)
        self.assertEqual(alien.rect.y, 100)


class TestBullet(unittest.TestCase):
    """Test cases for Bullet entity."""
    
    @classmethod
    def setUpClass(cls):
        """Set up pygame for testing."""
        pygame.init()
        pygame.display.set_mode((1, 1))
    
    def test_bullet_initialization(self):
        """Test bullet is initialized correctly."""
        bullet = Bullet((100, 100))
        self.assertIsNotNone(bullet.image)
        self.assertIsNotNone(bullet.rect)
        self.assertEqual(bullet.speed, config.BULLET_SPEED)
    
    def test_bullet_movement(self):
        """Test bullet moves correctly."""
        bullet = Bullet((100, 100))
        initial_y = bullet.rect.y
        bullet.update()
        self.assertLess(bullet.rect.y, initial_y)


class TestBunker(unittest.TestCase):
    """Test cases for Bunker entity."""
    
    @classmethod
    def setUpClass(cls):
        """Set up pygame for testing."""
        pygame.init()
        pygame.display.set_mode((1, 1))
    
    def test_bunker_initialization(self):
        """Test bunker is initialized correctly."""
        bunker = Bunker(100, 100)
        self.assertIsNotNone(bunker.image)
        self.assertIsNotNone(bunker.rect)
        self.assertEqual(bunker.health, 4)

    def test_bunker_damage(self):
        """Test bunker takes damage correctly."""
        bunker = Bunker(100, 100)
        initial_health = bunker.health
        bunker.damage()
        self.assertEqual(bunker.health, initial_health - 1)


if __name__ == '__main__':
    unittest.main()
