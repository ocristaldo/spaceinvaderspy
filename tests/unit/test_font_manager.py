import os
import pygame
import pytest

from src.ui.font_manager import FONT_PROFILES, get_font, get_menu_overlay_fonts

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")


@pytest.fixture(autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()


def test_all_font_profiles_render_sample_text():
    for name in FONT_PROFILES:
        font = get_font(name)
        surface = font.render("Sample", True, (255, 255, 255))
        assert surface.get_width() > 0
        assert surface.get_height() > 0


def test_controls_overlay_font_supports_arrows():
    controls_font, _ = get_menu_overlay_fonts("controls")
    surface = controls_font.render("← →", True, (255, 255, 255))
    assert surface.get_width() > 0
