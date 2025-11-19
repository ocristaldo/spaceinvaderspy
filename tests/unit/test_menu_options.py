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


@pytest.fixture
def isolated_settings(tmp_path, monkeypatch):
    settings_path = tmp_path / "settings.json"
    monkeypatch.setenv("SPACEINVADERS_SETTINGS_PATH", str(settings_path))
    yield


def _dismiss_attract_mode(game: Game) -> None:
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}))
    game.handle_events()
    assert game.state == "MENU"


def _open_options(game: Game) -> None:
    for _ in range(4):
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DOWN}))
        game.handle_events()
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}))
    game.handle_events()
    assert game.menu.showing_options is True


def test_options_overlay_and_audio_toggle(isolated_settings):
    game = Game()
    _dismiss_attract_mode(game)
    assert game.debug_sprite_borders is False

    _open_options(game)

    prev_audio = game.sfx_enabled
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_a}))
    game.handle_events()
    assert game.sfx_enabled != prev_audio

    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE}))
    game.handle_events()
    assert game.menu.showing_options is False


def test_music_toggle_and_credit_insert(isolated_settings):
    game = Game()
    _dismiss_attract_mode(game)
    _open_options(game)

    # Move selection from Sound FX to Music
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DOWN}))
    game.handle_events()
    prev_music = game.music_enabled
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}))
    game.handle_events()
    assert game.music_enabled != prev_music

    current_credit = game.credit_count
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_c}))
    game.handle_events()
    assert game.credit_count == current_credit + 1

    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE}))
    game.handle_events()
    assert game.menu.showing_options is False


def test_sprite_border_toggle_option(isolated_settings):
    game = Game()
    _dismiss_attract_mode(game)
    _open_options(game)

    # Move selection within options overlay down to "Sprite borders"
    for _ in range(3):
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DOWN}))
        game.handle_events()

    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}))
    game.handle_events()

    assert game.debug_sprite_borders is True
    assert game.menu.debug_draw_borders is True
    assert game.settings_manager.debug_borders_enabled() is True

    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE}))
    game.handle_events()
    assert game.menu.showing_options is False
