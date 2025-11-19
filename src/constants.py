"""
Global constants
"""

# Colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
RED      = (255, 0, 0)
GREEN    = (0, 255, 0)
KEY_COLOR= (0, 119, 255)

# Object Color
BACKGROUND_COLOR = 0, 0, 0                                      # Background color
BACKGROUND_TEXT_COLOR = 50, 50, 50                              # Text color
GAME_BACKGROUND_COLOR = 100, 100, 200                                      # Background color

# Game Screen
ORIGINAL_WIDTH = 224
ORIGINAL_HEIGHT = 256

# Layout Constants
ALIEN_NUMBER = 11
BLOCK_NUMBER = 4
LIVES_NUMBER = 3
PLAYERS_NUMBER = 2
SCORE_NAME = 'SCORE'
HSCORE_NAME = 'HI-SCORE'

# Game Mechanics
BASE_ALIEN_SPEED = 0.4                  # Units per frame
MAX_ALIEN_SPEED = 1.6                   # Maximum alien speed
BOMB_SPAWN_PROBABILITY = 0.01           # Base probability per frame
UFO_SPAWN_INTERVAL = 15                 # Seconds between UFO appearances

# Collision/Positioning
BUNKER_PLAYER_GAP = 80                  # Pixels between bunker and player
ALIEN_MARGIN_X = 12                     # Margin from left edge
ALIEN_MARGIN_Y = 12                     # Margin from top edge
ALIEN_SPACING_X = 20                    # Pixels between aliens horizontally
ALIEN_SPACING_Y = 16                    # Pixels between alien rows

# Bunker System
BUNKER_HEALTH_STAGES = 4                # Number of health states
BUNKER_TINT_BASE = 80                   # Base tint value
BUNKER_TINT_RANGE = 175                 # Tint range for damage states

# Scoring
POINTS_SQUID = 30                       # Points for squid alien
POINTS_CRAB = 20                        # Points for crab alien
POINTS_OCTOPUS = 10                     # Points for octopus alien
UFO_POINTS_MIN = 50                     # Minimum UFO bonus
UFO_POINTS_MAX = 300                    # Maximum UFO bonus

# UI/Display
BOTTOM_PANEL_HEIGHT = 36                # Height of bottom HUD panel
LIVES_DISPLAY_LIMIT = 5                 # Max life icons shown
CREDIT_DISPLAY_WIDTH = 2                # Digits for credit display
SCORE_DISPLAY_WIDTH = 8                 # Digits for score display

# Timing
LEVEL_START_DELAY_MS = 1500             # Delay before level starts
GAME_OVER_DELAY_MS = 5000               # Delay before returning to menu
WAVE_MESSAGE_DURATION_MS = 2000         # Duration of wave message display
