import os
from typing import Tuple
from . import constants

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(os.path.dirname(BASE_DIR), "assets")
IMG_DIR = os.path.join(ASSETS_DIR, "images")
SOUND_DIR = os.path.join(ASSETS_DIR, "sounds")
FONT_DIR = os.path.join(ASSETS_DIR, "fonts")

# Rendering/scaling configuration
SPRITE_SCALE = 1  # Pixel scale for sprites pulled from the sheet
PLAYFIELD_SCALE = float(os.environ.get("SPACEINVADERS_SCALE", "2.0"))
PLAYFIELD_SCALE = max(1.0, min(4.0, PLAYFIELD_SCALE))
BASE_WIDTH = int(constants.ORIGINAL_WIDTH * PLAYFIELD_SCALE)
BASE_HEIGHT = int(constants.ORIGINAL_HEIGHT * PLAYFIELD_SCALE)
MIN_WINDOW_SCALE = 0.5
MAX_WINDOW_SCALE = 5.0
DEFAULT_WINDOW_SCALE = float(os.environ.get("SPACEINVADERS_WINDOW_SCALE", "1.0"))
DEFAULT_WINDOW_SCALE = max(MIN_WINDOW_SCALE, min(MAX_WINDOW_SCALE, DEFAULT_WINDOW_SCALE))

# Backwards-compat constants used by legacy tests/utilities
SCALE = SPRITE_SCALE
SCREEN_WIDTH = BASE_WIDTH
SCREEN_HEIGHT = BASE_HEIGHT


def get_window_size(scale: float) -> Tuple[int, int]:
    """Return a window size (w, h) for a given scale."""
    width = max(1, int(BASE_WIDTH * scale))
    height = max(1, int(BASE_HEIGHT * scale))
    return width, height

# Gameplay settings
ALIEN_ROWS = 5
ALIEN_COLUMNS = 11
ALIEN_SPACING_X = 12  # Preferred gap between aliens
ALIEN_MIN_SPACING_X = 6  # Minimum gap when fitting formation on screen
ALIEN_SPACING_Y = 40
ALIEN_MARGIN_X = 48
ALIEN_MARGIN_Y = 60
ALIEN_EDGE_PADDING = 8
ALIEN_DROP_DISTANCE = 6
BULLET_SPEED = -5
BOMB_SPEED = 3
UFO_INTERVAL = 25000  # milliseconds
PLAYER_MAX_BULLETS = int(os.environ.get("SPACEINVADERS_PLAYER_SHOTS", "1"))
BUNKER_PLAYER_GAP = 50

# Alien pacing behaviour
ALIEN_START_SPEED = 0.55
ALIEN_SPEED_INCREMENT = 0.035
ALIEN_BOMB_CHANCE = 0.01  # Base probability per frame to drop a bomb
