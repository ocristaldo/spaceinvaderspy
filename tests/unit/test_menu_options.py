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


@pytest.fixture
def isolated_settings(tmp_path, monkeypatch):
    settings_path = tmp_path / "settings.json"
    monkeypatch.setenv("SPACEINVADERS_SETTINGS_PATH", str(settings_path))
    yield


def test_options_overlay_and_audio_toggle(isolated_settings):
    game = Game()
    # Exit attract/demo to menu
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}))
    game.handle_events()
    assert game.state == "MENU"
    assert game.debug_sprite_borders is False

    # Move down to Options (Start, High Scores, Controls, Options -> 3 DOWN presses)
    for _ in range(3):
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DOWN}))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}))
    game.handle_events()
    assert game.menu.showing_options is True

    prev_audio = game.audio_manager.enabled
    # Toggle audio with 'A'
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_a}))
    game.handle_events()
    assert game.audio_manager.enabled != prev_audio

    # Close options
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE}))
    game.handle_events()
    assert game.menu.showing_options is False


def test_sprite_border_toggle_option(isolated_settings):
    game = Game()
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}))
    game.handle_events()
    assert game.state == "MENU"

    for _ in range(3):
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DOWN}))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}))
    game.handle_events()

    # Move selection within options overlay down to "Sprite borders"
    for _ in range(3):
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DOWN}))
        game.handle_events()

    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}))
    game.handle_events()

    assert game.debug_sprite_borders is True
    assert game.menu.debug_draw_borders is True
    assert game.settings_manager.debug_borders_enabled() is True

    # Close options overlay
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE}))
    game.handle_events()
    assert game.menu.showing_options is False
