import pygame
import pytest
from src.main import Game

# Use the SDL "dummy" video driver for headless test runs
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

@pytest.fixture(autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()


def _skip_attract(game):
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}))
    game.handle_events()
    assert game.state == "MENU"


def test_high_scores_overlay_via_main():
    game = Game()
    _skip_attract(game)
    # Move selection to "High Scores" (two DOWN keys from 1-Player)
    for _ in range(2):
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DOWN}))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}))
    game.handle_events()
    assert game.menu.showing_high_scores is True

    # Hide the overlay using ESC
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE}))
    game.handle_events()
    assert game.menu.showing_high_scores is False


def test_credits_overlay_via_main():
    game = Game()
    _skip_attract(game)
    # Move selection down to Credits (5 DOWN presses from 1-Player)
    for _ in range(5):
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DOWN}))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}))
    game.handle_events()
    assert game.menu.showing_credits is True

    # Hide the credits overlay
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE}))
    game.handle_events()
    assert game.menu.showing_credits is False
