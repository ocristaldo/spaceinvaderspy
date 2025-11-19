# Use the SDL "dummy" video driver for headless test runs
import os

import pygame
import pytest

from src.main import Game

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

@pytest.fixture(autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()

def test_menu_to_play_and_pause_toggle():
    game = Game()
    # Initially in ATTRACT (demo) - pressing any key should return to MENU
    assert game.state == "ATTRACT"

    # Simulate a key press (RETURN) to exit attract/demo and go to MENU
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN})
    pygame.event.post(event)
    game.handle_events()
    assert game.state == "MENU"

    # Insert a credit first
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_c})
    pygame.event.post(event)
    game.handle_events()

    # Simulate pressing RETURN to start (menu selected defaults to 1-Player)
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN})
    pygame.event.post(event)
    game.handle_events()
    assert game.state == "PLAYING"

    # Press P to pause
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_p})
    pygame.event.post(event)
    game.handle_events()
    assert game.state == "PAUSED"

    # Press ESC to resume
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE})
    pygame.event.post(event)
    game.handle_events()
    assert game.state == "PLAYING"
