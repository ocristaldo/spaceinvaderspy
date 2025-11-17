import os
import pygame
import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

from src import config
from src.main import Game
from src.entities.alien import Alien


@pytest.fixture(autouse=True)
def pygame_display():
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()


def test_alien_formation_starts_within_screen_bounds():
    game = Game()
    xs = [alien.rect.left for alien in game.alien_group]
    rights = [alien.rect.right for alien in game.alien_group]
    assert min(xs) >= 0
    assert max(rights) <= game.logical_width


def test_alien_drop_distance_matches_config():
    game = Game()
    game.alien_group.empty()
    alien = Alien(0, 50, 10)
    alien.rect.right = game.logical_width - config.ALIEN_EDGE_PADDING + 1
    game.alien_group.add(alien)
    starting_y = alien.rect.y
    game.alien_direction = 1
    game.alien_speed = 5

    game.update()

    assert alien.rect.y == starting_y + config.ALIEN_DROP_DISTANCE
