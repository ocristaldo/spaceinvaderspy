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


def _skip_attract(game: Game):
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}))
    game.handle_events()


def _open_options(game: Game):
    # Move selection down to Options (Start, High Scores, Controls, Options)
    for _ in range(3):
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DOWN}))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}))
    game.handle_events()
    assert game.menu.showing_options


def test_intro_demo_toggle_persists(tmp_path, monkeypatch):
    settings_path = tmp_path / "settings.json"
    monkeypatch.setenv("SPACEINVADERS_SETTINGS_PATH", str(settings_path))

    game = Game()
    _skip_attract(game)
    assert game.state == "MENU"

    _open_options(game)

    # Toggle intro demo autoplay with 'I'
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_i}))
    game.handle_events()

    assert game.settings_manager.intro_demo_enabled() is False

    # Close options
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE}))
    game.handle_events()
    assert not game.menu.showing_options

    # New game should boot directly to the menu (demo disabled)
    game2 = Game()
    assert game2.state == "MENU"
    assert not game2.start_screen_demo.is_running()


def test_debug_border_toggle_persists(tmp_path, monkeypatch):
    settings_path = tmp_path / "settings.json"
    monkeypatch.setenv("SPACEINVADERS_SETTINGS_PATH", str(settings_path))

    game = Game()
    _skip_attract(game)
    assert game.state == "MENU"

    _open_options(game)

    # Move to sprite borders option (index 3)
    for _ in range(3):
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DOWN}))
        game.handle_events()

    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}))
    game.handle_events()
    assert game.debug_sprite_borders is True

    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE}))
    game.handle_events()

    game2 = Game()
    _skip_attract(game2)
    assert game2.debug_sprite_borders is True
    assert game2.menu.debug_draw_borders is True
