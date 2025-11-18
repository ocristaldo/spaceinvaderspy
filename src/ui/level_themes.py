"""
Level-based color themes for Space Invaders v2.0.

Each level has a unique vibrant color palette affecting all sprites,
HUD elements, and visual effects. Themes cycle after level 8.
"""
from typing import Dict, Tuple, Optional

# RGB color type
Color = Tuple[int, int, int]


class LevelTheme:
    """A color theme for a single game level."""

    def __init__(
        self,
        level: int,
        name: str,
        player: Color,
        alien_squid: Color,
        alien_crab: Color,
        alien_octopus: Color,
        ufo: Color,
        bunker: Color,
        bullet: Color,
        bomb_alien: Color,
        bomb_ufo: Color,
        hud_text: Color,
        background_effect: Optional[str] = None,
    ):
        """Initialize a level theme with all color specifications."""
        self.level = level
        self.name = name
        self.player = player
        self.alien_squid = alien_squid
        self.alien_crab = alien_crab
        self.alien_octopus = alien_octopus
        self.ufo = ufo
        self.bunker = bunker
        self.bullet = bullet
        self.bomb_alien = bomb_alien
        self.bomb_ufo = bomb_ufo
        self.hud_text = hud_text
        self.background_effect = background_effect

    def get_alien_color(self, alien_type: int) -> Color:
        """Get color for an alien type (30=squid, 20=crab, 10=octopus)."""
        color_map = {
            30: self.alien_squid,
            20: self.alien_crab,
            10: self.alien_octopus,
        }
        return color_map.get(alien_type, self.alien_octopus)

    def to_dict(self) -> Dict[str, any]:
        """Convert theme to dictionary for serialization."""
        return {
            "level": self.level,
            "name": self.name,
            "player": self.player,
            "alien_squid": self.alien_squid,
            "alien_crab": self.alien_crab,
            "alien_octopus": self.alien_octopus,
            "ufo": self.ufo,
            "bunker": self.bunker,
            "bullet": self.bullet,
            "bomb_alien": self.bomb_alien,
            "bomb_ufo": self.bomb_ufo,
            "hud_text": self.hud_text,
            "background_effect": self.background_effect,
        }


# ============================================================================
# LEVEL THEMES - 8 VIBRANT PALETTES (Cycles after level 8)
# ============================================================================

LEVEL_THEMES = {
    1: LevelTheme(
        level=1,
        name="Classic Green",
        player=(180, 255, 180),  # Light green
        alien_squid=(100, 255, 100),  # Bright green
        alien_crab=(150, 200, 255),  # Cyan blue
        alien_octopus=(255, 255, 100),  # Bright yellow
        ufo=(255, 180, 180),  # Light pink
        bunker=(180, 200, 100),  # Olive green
        bullet=(200, 255, 200),  # Very light green
        bomb_alien=(255, 100, 100),  # Red
        bomb_ufo=(255, 180, 150),  # Light coral
        hud_text=(200, 255, 200),  # Light green text
    ),
    2: LevelTheme(
        level=2,
        name="Neon Purple",
        player=(255, 100, 255),  # Bright magenta
        alien_squid=(200, 100, 255),  # Purple
        alien_crab=(100, 200, 255),  # Sky blue
        alien_octopus=(255, 200, 100),  # Orange
        ufo=(255, 150, 200),  # Pink
        bunker=(200, 150, 255),  # Light purple
        bullet=(200, 150, 255),  # Light purple
        bomb_alien=(255, 100, 150),  # Hot pink
        bomb_ufo=(255, 150, 200),  # Light pink
        hud_text=(255, 150, 255),  # Magenta text
    ),
    3: LevelTheme(
        level=3,
        name="Volcanic Red",
        player=(255, 150, 100),  # Orange
        alien_squid=(255, 100, 50),  # Deep orange
        alien_crab=(255, 200, 100),  # Light orange
        alien_octopus=(255, 255, 100),  # Yellow
        ufo=(255, 150, 150),  # Light red
        bunker=(255, 100, 100),  # Red
        bullet=(255, 200, 150),  # Peach
        bomb_alien=(255, 50, 50),  # Bright red
        bomb_ufo=(255, 150, 100),  # Coral
        hud_text=(255, 150, 100),  # Orange text
    ),
    4: LevelTheme(
        level=4,
        name="Cyan Dreams",
        player=(100, 255, 255),  # Cyan
        alien_squid=(100, 200, 255),  # Light blue
        alien_crab=(50, 200, 255),  # Bright cyan
        alien_octopus=(100, 255, 200),  # Light green-cyan
        ufo=(150, 200, 255),  # Powder blue
        bunker=(100, 200, 200),  # Teal
        bullet=(100, 255, 255),  # Cyan
        bomb_alien=(255, 100, 200),  # Pink
        bomb_ufo=(200, 150, 255),  # Light purple
        hud_text=(100, 255, 255),  # Cyan text
    ),
    5: LevelTheme(
        level=5,
        name="Golden Sunset",
        player=(255, 200, 100),  # Golden orange
        alien_squid=(255, 150, 50),  # Burnt orange
        alien_crab=(255, 100, 100),  # Red-orange
        alien_octopus=(255, 255, 100),  # Bright yellow
        ufo=(255, 180, 100),  # Peach
        bunker=(200, 150, 100),  # Brown-gold
        bullet=(255, 255, 150),  # Light yellow
        bomb_alien=(255, 80, 80),  # Red
        bomb_ufo=(255, 200, 100),  # Golden
        hud_text=(255, 200, 100),  # Golden text
    ),
    6: LevelTheme(
        level=6,
        name="Deep Ocean",
        player=(100, 150, 255),  # Blue
        alien_squid=(50, 100, 200),  # Dark blue
        alien_crab=(100, 200, 255),  # Sky blue
        alien_octopus=(150, 255, 200),  # Aquamarine
        ufo=(200, 150, 255),  # Purple
        bunker=(100, 150, 200),  # Navy blue
        bullet=(150, 200, 255),  # Light blue
        bomb_alien=(255, 100, 150),  # Pink
        bomb_ufo=(200, 200, 255),  # Lavender
        hud_text=(100, 200, 255),  # Sky blue text
    ),
    7: LevelTheme(
        level=7,
        name="Neon Grid",
        player=(0, 255, 255),  # Pure cyan
        alien_squid=(0, 200, 255),  # Bright cyan
        alien_crab=(255, 0, 255),  # Pure magenta
        alien_octopus=(255, 255, 0),  # Pure yellow
        ufo=(255, 0, 200),  # Hot pink
        bunker=(0, 255, 200),  # Green-cyan
        bullet=(0, 255, 255),  # Cyan
        bomb_alien=(255, 0, 100),  # Pink
        bomb_ufo=(255, 255, 0),  # Yellow
        hud_text=(0, 255, 255),  # Cyan text
    ),
    8: LevelTheme(
        level=8,
        name="Plasma Storm",
        player=(255, 100, 200),  # Pink
        alien_squid=(200, 100, 255),  # Purple
        alien_crab=(255, 100, 255),  # Magenta
        alien_octopus=(100, 200, 255),  # Light blue
        ufo=(255, 200, 100),  # Orange
        bunker=(200, 100, 200),  # Purple
        bullet=(200, 100, 255),  # Purple
        bomb_alien=(255, 100, 100),  # Red
        bomb_ufo=(255, 100, 200),  # Pink
        hud_text=(255, 150, 255),  # Magenta text
    ),
}


def get_level_theme(level: int) -> LevelTheme:
    """
    Get the theme for a given level.

    Cycles through themes 1-8. Level 9 uses theme 1, level 10 uses theme 2, etc.

    Args:
        level: The game level (1+)

    Returns:
        The LevelTheme for this level
    """
    # Cycle through themes 1-8
    theme_num = ((level - 1) % 8) + 1
    return LEVEL_THEMES[theme_num]


def get_all_themes() -> Dict[int, LevelTheme]:
    """Get dictionary of all available themes."""
    return dict(LEVEL_THEMES)


def get_theme_names() -> Dict[int, str]:
    """Get mapping of theme numbers to theme names."""
    return {level: theme.name for level, theme in LEVEL_THEMES.items()}


def get_theme_preview_text() -> str:
    """Get a text preview of all available themes for menu display."""
    lines = ["AVAILABLE COLOR THEMES:", ""]
    for level in range(1, 9):
        theme = LEVEL_THEMES[level]
        lines.append(f"Level {level}: {theme.name}")
    lines.append("")
    lines.append("Themes cycle after level 8")
    return "\n".join(lines)
