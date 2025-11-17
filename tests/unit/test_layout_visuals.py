import os
import pygame
import pytest

from src import config
from src.ui.menu import Menu
from src.ui.start_screen_demo import ScoreTableDemo, WaveFormationDemo
from src.utils.sprite_sheet import get_title_logo

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")


@pytest.fixture(autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()


def test_title_logo_asset_present():
    logo = get_title_logo()
    assert isinstance(logo, pygame.Surface)
    assert logo.get_width() > 0
    assert logo.get_height() > 0


def test_menu_options_fit_canvas():
    menu = Menu(pygame.font.SysFont("monospace", 18), pygame.font.SysFont("monospace", 14))
    surface = pygame.Surface((config.BASE_WIDTH, config.BASE_HEIGHT))
    menu.draw(surface)
    assert menu._last_option_rects, "Expected option rects recorded after draw"
    for rect in menu._last_option_rects:
        assert rect.top >= 0
        assert rect.bottom <= config.BASE_HEIGHT
    assert menu._last_title_rect is not None
    assert menu._last_option_rects[0].top > menu._last_title_rect.bottom


def test_title_logo_ratio_preserved():
    menu = Menu(pygame.font.SysFont("monospace", 18), pygame.font.SysFont("monospace", 14))
    surface = pygame.Surface((config.BASE_WIDTH, config.BASE_HEIGHT))
    menu.draw(surface)
    raw = get_title_logo()
    assert menu._last_title_rect is not None
    expected_ratio = raw.get_width() / raw.get_height()
    actual_ratio = menu._last_title_rect.width / menu._last_title_rect.height
    assert abs(actual_ratio - expected_ratio) < 0.05


def test_intro_demo_logo_spacing():
    demo = ScoreTableDemo()
    assert demo.logo_rect is not None
    assert demo.logo_rect.top >= 0
    assert demo.logo_rect.bottom < int(config.BASE_HEIGHT * 0.8)
    first_entry = demo.table_entries[0]
    assert first_entry["sprite_y"] > demo.logo_rect.bottom


def test_wave_demo_has_no_logo():
    wave = WaveFormationDemo()
    assert not hasattr(wave, "logo_rect")
