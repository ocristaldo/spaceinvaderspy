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

def test_menu_to_play_and_pause_toggle():
    game = Game()
    # Initially in MENU
    assert game.state == "MENU"

    # Simulate pressing RETURN to start (menu selected defaults to Start)
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
