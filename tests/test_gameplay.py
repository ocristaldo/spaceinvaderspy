import unittest
try:
    import pygame
except ImportError:  # pragma: no cover - skip tests if pygame missing
    pygame = None

if pygame:
    from src import main
    from src import config
    from src.entities.alien import Alien
    from src.entities.bullet import Bullet
else:
    main = config = Alien = Bullet = None

if pygame:
    pygame.display.init()
    pygame.display.set_mode((1, 1))

@unittest.skipIf(pygame is None, "pygame not available")
class CollisionTest(unittest.TestCase):
    def test_bullet_hits_alien(self):
        game = main.Game()
        game.bullet_group.empty()
        game.alien_group.empty()
        alien = Alien(50, 50, 10)
        bullet = Bullet((50, 50))
        game.alien_group.add(alien)
        game.bullet_group.add(bullet)
        
        # Position bullet and alien to overlap for collision
        bullet.rect.center = alien.rect.center
        
        game.update()
        self.assertEqual(game.score, 10)
        self.assertFalse(game.alien_group)
        self.assertFalse(game.bullet_group)


@unittest.skipIf(pygame is None, "pygame not available")
class AlienMovementTest(unittest.TestCase):
    def test_direction_flip_on_edge(self):
        game = main.Game()
        game.alien_group.empty()
        # create alien near right edge
        alien = Alien(config.SCREEN_WIDTH - 20, 50, 10)
        game.alien_group.add(alien)
        game.alien_direction = 1
        game.update()
        self.assertEqual(game.alien_direction, -1)


if __name__ == "__main__":
    unittest.main()

