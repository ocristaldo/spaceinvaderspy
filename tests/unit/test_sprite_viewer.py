import os
import pygame
import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

from src.utils.sprite_viewer import SpriteViewer


@pytest.fixture(autouse=True)
def pygame_display():
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()


def test_load_stage_snapshot_start_screen():
    screen = pygame.display.get_surface()
    viewer = SpriteViewer(screen)
    assert "start_screen" in viewer.stage_snapshots
    loaded = viewer.load_stage_snapshot("start_screen")
    assert loaded
    assert viewer.current_stage == "start_screen"
    assert viewer.stage_image is not None
    viewer.clear_stage_snapshot()
    assert viewer.stage_image is None
    assert viewer.stage_meta is None
