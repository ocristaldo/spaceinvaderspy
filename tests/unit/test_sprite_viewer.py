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


def test_load_stage_preview_start_screen():
    screen = pygame.display.get_surface()
    viewer = SpriteViewer(screen)
    assert "start_screen" in viewer.stage_previews
    loaded = viewer.load_stage_preview("start_screen")
    assert loaded
    assert viewer.current_stage == "start_screen"
    assert viewer.stage_surface is not None
    viewer.clear_stage_preview()
    assert viewer.stage_surface is None
    assert viewer.stage_meta is None


def test_platform_key_detection_and_loading():
    screen = pygame.display.get_surface()
    viewer = SpriteViewer(screen)

    class FakeKeys:
        def __init__(self, pressed):
            self.pressed = set(pressed)

        def __getitem__(self, key):
            return key in self.pressed

    # S+1 (arcade) should be detectable — arcade JSON exists in assets
    keys = FakeKeys([pygame.K_s, pygame.K_1])
    platform = viewer.get_platform_from_key_combo(keys)
    assert platform == 'arcade'
    assert viewer.load_platform_sprites(platform)

    # S+2: Start screen stage preview should be detected and load
    keys = FakeKeys([pygame.K_s, pygame.K_2])
    stage = viewer.get_stage_from_key_combo(keys)
    assert stage == 'start_screen'
    assert viewer.load_stage_preview(stage)

    # S+3: Wave-ready stage preview
    keys = FakeKeys([pygame.K_s, pygame.K_3])
    stage = viewer.get_stage_from_key_combo(keys)
    assert stage == 'wave_ready'
    assert viewer.load_stage_preview(stage)

    # S+4: Late-wave stage preview
    keys = FakeKeys([pygame.K_s, pygame.K_4])
    stage = viewer.get_stage_from_key_combo(keys)
    assert stage == 'late_wave'
    assert viewer.load_stage_preview(stage)

