import pygame
import sys
import os

# Ensure src is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.main import Game
from src.entities.bullet import Bomb
from src import constants


def test_bomb_collision_decrements_lives_and_triggers_game_over():
    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()

    # Set to one life to verify game_over when hit
    game.lives = 1

    # Create a bomb at player's center to force collision
    bomb = Bomb((game.player.rect.centerx, game.player.rect.centery))
    # Ensure rect overlap — set center explicitly to avoid anchor differences
    bomb.rect.center = game.player.rect.center
    game.bomb_group.add(bomb)
    # Debug: show rects before update
    print('TEST DEBUG player rect:', game.player.rect)
    for b in game.bomb_group:
        print('TEST DEBUG bomb rect before update:', b.rect)

    # Call update which should process collisions
    game.update()

    # Debug: show rects after update
    print('TEST DEBUG player rect after update:', game.player.rect)
    for b in game.bomb_group:
        print('TEST DEBUG bomb rect after update:', b.rect)

    assert game.lives == 0
    assert game.game_over
