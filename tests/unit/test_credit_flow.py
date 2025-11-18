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


def test_start_requires_credit(isolated_settings):
    game = Game()
    _dismiss_attract_mode(game)
    game.credit_count = 0
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}))
    game.handle_events()
    assert game.state == "MENU"
    assert game.credit_count == 0


def test_insert_credit_hotkey(isolated_settings):
    game = Game()
    _dismiss_attract_mode(game)
    current = game.credit_count
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_c}))
    game.handle_events()
    assert game.credit_count == min(99, current + 1)
