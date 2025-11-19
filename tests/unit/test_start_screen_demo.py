import os

import pygame
import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

from src.ui.start_screen_demo import ScoreTableDemo


@pytest.fixture(autouse=True)
def init_pygame():
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()


def test_build_table_entries_generates_four_entries():
    demo = ScoreTableDemo(tint_enabled=False)
    demo._build_table_entries()
    assert len(demo.table_entries) == 4
    for entry in demo.table_entries:
        assert "sprite" in entry and entry["sprite"].get_width() > 0
        assert "text_surface" in entry and entry["text_surface"].get_width() > 0
