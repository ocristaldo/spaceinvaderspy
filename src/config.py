import os
from . import constants

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(os.path.dirname(BASE_DIR), "assets")
IMG_DIR = os.path.join(ASSETS_DIR, "images")
SOUND_DIR = os.path.join(ASSETS_DIR, "sounds")
FONT_DIR = os.path.join(ASSETS_DIR, "fonts")

SCALE = 2
SCREEN_WIDTH = constants.ORIGINAL_WIDTH * SCALE
SCREEN_HEIGHT = constants.ORIGINAL_HEIGHT * SCALE

# Gameplay settings
ALIEN_ROWS = 5
ALIEN_COLUMNS = 11
ALIEN_SPACING_X = 32
ALIEN_SPACING_Y = 24
ALIEN_MARGIN_X = 24
ALIEN_MARGIN_Y = 50
BULLET_SPEED = -5
BOMB_SPEED = 3
UFO_INTERVAL = 25000  # milliseconds

# Alien speed behaviour
ALIEN_START_SPEED = 1
ALIEN_SPEED_INCREMENT = 0.05
