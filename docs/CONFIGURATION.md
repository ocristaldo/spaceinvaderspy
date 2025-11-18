# Configuration Reference

This document aggregates all of the tweakable knobs that influence visuals,
UI, and gameplay so you always know *where* to modify a value and *what* each
setting controls.

## Quick Map

| Area | File | Description |
|------|------|-------------|
| Global rendering/gameplay constants | `src/config.py` | Screen sizes, scaling, alien spacing, speed/pacing defaults. |
| Persistent user toggles | `settings.json` | Runtime settings saved between sessions (audio, debug borders, intro demo). |
| Color palette + sprite tints | `src/ui/color_scheme.py` | Central location for HUD colors and per-sprite tint defaults. |
| Font catalog | `src/ui/font_manager.py` | Single source of truth for menu/HUD/demo font style + sizing. |
| Sprite atlas definitions | `assets/images/SpaceInvaders.arcade.json` | Coordinate + metadata for every sprite extracted by `SpriteSheet`. |
| Sprite documentation | `docs/SPRITES.md` | Human-readable explanation of sprite usage plus maintenance notes. |

## Global Constants (`src/config.py`)

These values are imported throughout the project; edit them when you need to
change layout or pacing globally.

| Setting | Default | Notes |
|---------|---------|-------|
| `SPRITE_SCALE` | `1` | Integer multiplier applied when sampling sprites from the atlas. Increase when adding higher-res art. |
| `PLAYFIELD_SCALE` | `env SPACEINVADERS_SCALE` (default `2.0`) | Global scale factor applied to the logical playfield; influences `BASE_WIDTH/HEIGHT`. Clamp between 1× and 4×. |
| `BASE_WIDTH`, `BASE_HEIGHT` | Derived | Logical canvas size; everything from menus to HUD uses this resolution before being scaled to the window. |
| `DEFAULT_WINDOW_SCALE` | `env SPACEINVADERS_WINDOW_SCALE` (default `1.0`) | Initial OS window size relative to `BASE_WIDTH/HEIGHT`. |
| `ALIEN_*` constants | see file | Control formation rows/columns, spacing, drop distance, speed curve, etc. Tweak for difficulty changes. |
| `PLAYER_MAX_BULLETS` | env `SPACEINVADERS_PLAYER_SHOTS` (default `1`) | How many bullets can be in-flight simultaneously. |
| `ATTRACT_IDLE_TIME`, `ATTRACT_SLIDE_INTERVAL` | env overrides | Idle timeout before the intro demo runs, and rotation speed between demo scenes. |

> Tips:
> * Whenever you change a scale constant, re-run `tests/unit/test_layout_visuals.py`
>   to ensure the menu/start-screen layout still fits inside the canvas.
> * Group related tuning by creating helper constants in `config.py` rather than
>   scattering raw numbers across gameplay modules.

## Runtime Settings (`settings.json`)

This JSON file is loaded by `SettingsManager` and persists player-facing
preferences between sessions.

```json
{
  "audio_enabled": false,
  "debug_sprite_borders": true,
  "intro_demo_enabled": true,
  "tint_enabled": false
}
```

| Key | Effect | Change via |
|-----|--------|-----------|
| `audio_enabled` | Toggles sound FX (shoot, invader killed, explosions, etc.). | Press `A` or Options → Sound FX. |
| `music_enabled` | Toggles the attract/menu music loop. | Press `M` or Options → Music. |
| `debug_sprite_borders` | Draws debug rectangles around sprites/menu elements. | Options overlay or edit JSON. |
| `intro_demo_enabled` | Controls whether the attract loop should auto-run after idling. | Options overlay or edit JSON. |
| `tint_enabled` | Enables the per-sprite tint system (aliens/UFO/bunkers/lives icons). | Options overlay → “Sprite tint” or edit JSON. |

Resetting/removing this file will regenerate defaults on next launch.

## Font Catalog (`src/ui/font_manager.py`)

All UI text pulls fonts from the centralized `FONT_PROFILES` dictionary. Each
entry is a `FontSpec` with the following fields:

- `name`: Font family passed to `pygame.font.match_font`. `None` falls back to
  the default pygame font (useful for glyph coverage such as arrow icons).
- `size`: Base point size before scaling.
- `bold`: Whether bold styling is forced.
- `min_size`/`max_size`: Clamps applied after scaling.
- `scale_with_playfield`: When `True`, multiplies `size` by `config.PLAYFIELD_SCALE`
  to keep menus readable across resolutions.

| Profile | Usage | Notes |
|---------|-------|-------|
| `menu_title` | Menu marquee header | Bold, auto-scales with playfield. |
| `menu_body` | Menu option list | Auto-scales for readability. |
| `menu_controls_main` / `_hint` | Controls overlay body + hint | Uses default font so arrow glyphs render reliably. |
| `menu_high_scores_main` / `_hint` | High-score overlay | Fixed size for tight layout. |
| `menu_options_main` / `_hint` | Options overlay text & hint | Matches controls sizing. |
| `menu_credits_main` / `_hint` | Credits overlay text & hint | Same metrics as high scores. |
| `hud_main`, `hud_small` | In-game HUD text | Adjust to change scoreboard aesthetics. |
| `demo_title`, `demo_subtitle`, `demo_entry`, `demo_prompt`, `wave_info` | Start-screen demos | Used inside `src/ui/start_screen_demo.py`. |
| `spriteviewer_*` | Sprite viewer UI + stage previews | Controls the overlay instructions in sprite viewer mode. |

To tweak a font, edit its `FontSpec`. Since every screen pulls from the manager,
you no longer need to patch individual modules.

## Sprite Atlas (`assets/images/SpaceInvaders.arcade.json`)

This JSON array powers `SpriteSheet` and defines coordinates for every asset in
`assets/images/SpaceInvaders.png`. Each object includes:

- `name`: Identifier referenced by `get_game_sprite` in `src/utils/sprite_sheet.py`.
- `platform`: Source platform (currently `arcade`).
- `frame`: Animation frame number (if applicable).
- `x`, `y`, `width`, `height`: Pixel bounds inside the sprite sheet.
- `description`: (new) plain-language note explaining the sprite’s purpose.

When adding art:

1. Cut the sprite into `SpaceInvaders.png` at the desired coordinates.
2. Append a new JSON object with the proper bounds and a descriptive `name`.
3. Update `src/utils/sprite_sheet.ARCADE_SPRITE_MAPPING` (and optionally
   `docs/SPRITES.md`) so code can request the sprite by logical name.
4. Run the layout/unit tests to confirm nothing else shifted.

## Color & Tint Controls (`src/ui/color_scheme.py`)

HUD colors and sprite tint defaults live in `src/ui/color_scheme.py`. Each entry can be tweaked without touching game logic:

- `default_theme` controls HUD text, divider lines, and background color.
- `sprite_tints` defines the tint color for each sprite category (`player`, `alien_squid`, `ufo`, etc).
- Call `get_game_sprite(..., tint=...)` to apply the configured color; the new tint system automatically leaves black pixels untouched so the cabinet-style background is preserved.
- Players can toggle tinting at runtime via the **Options → Sprite tint** entry (stored in `settings.json` under `tint_enabled`).

## Testing Your Changes

- `python3 -m pytest tests/unit/test_font_manager.py` verifies every font profile
  renders text (including arrow glyphs).
- `python3 -m pytest tests/unit/test_layout_visuals.py` ensures menu/start-screen
  layouts still fit within the logical canvas after scaling tweaks.
- Manual runs of the game remain the best way to validate attract-mode timing
  and sprite atlas updates.
