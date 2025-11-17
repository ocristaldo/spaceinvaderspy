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
        
        current_level = game.level
        game.update()
        self.assertEqual(game.score, 10)
        self.assertGreater(len(game.alien_group), 0)
        self.assertFalse(game.bullet_group)

    def test_player_bullet_intercepts_bomb(self):
        game = main.Game()
        from src.entities.bullet import Bullet, Bomb
        game.bullet_group.empty()
        game.bomb_group.empty()
        bullet = Bullet((200, 200))
        bomb = Bomb((200, 200))
        bullet.rect.center = (220, 260)
        bomb.rect.center = bullet.rect.center
        game.bullet_group.add(bullet)
        game.bomb_group.add(bomb)
        game.update()
        self.assertFalse(game.bullet_group)
        self.assertFalse(game.bomb_group)


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


@unittest.skipIf(pygame is None, "pygame not available")
class AlienCollisionTest(unittest.TestCase):
    def test_alien_colliding_with_player_triggers_game_over(self):
        game = main.Game()
        alien = next(iter(game.alien_group))
        alien.rect.center = game.player.rect.center
        game.update()
        self.assertTrue(game.game_over)

    def test_alien_colliding_with_bunker_removes_it(self):
        game = main.Game()
        initial_bunkers = len(game.bunker_group)
        bunker = next(iter(game.bunker_group))
        alien = next(iter(game.alien_group))
        alien.rect.center = bunker.rect.center
        game.update()
        self.assertLess(len(game.bunker_group), initial_bunkers)


if __name__ == "__main__":
    unittest.main()
