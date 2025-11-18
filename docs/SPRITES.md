# Sprite Reference

This file lists every sprite defined in `assets/images/SpaceInvaders.arcade.json`
and explains how the code uses it today (or intends to use it) so that art
changes stay coordinated with gameplay code. See `docs/CONFIGURATION.md` for a
full overview of other tweakable systems (fonts, settings, etc.).

## Editing the Atlas JSON

Each entry in `SpaceInvaders.arcade.json` now includes a `description` field so
you can search for a sprite in your editor and immediately see how it is used.
Fields per entry:

| Field | Meaning |
|-------|---------|
| `name` | Identifier requested via `get_game_sprite("name", scale)` |
| `platform` | Only `"arcade"` is active today, but other atlases share the format |
| `frame` | Animation frame index (1-based) for toggled sprites |
| `x`, `y`, `width`, `height` | Pixel bounds inside `SpaceInvaders.png` |
| `description` | Plain-language usage note |
| `validated` | `"Y"` once the coordinates have been verified in-game; `"N"` otherwise |

When you add, rename, or relocate sprites be sure to:

1. Update the JSON entry (coordinates + description).
2. Adjust `ARCADE_SPRITE_MAPPING` in `src/utils/sprite_sheet.py` if the logical
   names change.
3. Document the change in the relevant section below so artists/designers know
   what moved.

> Need palette swaps between levels? Call `get_game_sprite("alien_squid_1", tint=(0, 255, 0))`
> to recolor only the non-black pixels while preserving the dark background.

## Core Entities

| System | `get_game_sprite` name(s) | JSON entry | In Use | Validated | Purpose / Notes |
|--------|---------------------------|------------|--------|-----------|------------------|
| Player cannon | `player` | `player` | Yes | Yes | Player ship sprite (`src/entities/player.py`). Any replacement must stay 16×16 or adjust collision boxes. |
| Explosion FX | `explosion`, `explosion_alt` | `explosion`, `explosion_alt` | Yes | Yes | Animated blast effect when aliens, UFOs, or the player explode. |
| UFO | `ufo` | `ufo` | Yes | Yes | Used by `src/entities/ufo.py`. Now drops `bomb_2` projectiles while crossing the screen. |
| Broken cannon placeholder | `cannon_broken` | `cannon_broken` | No | No | Reserve art for dramatic “destroyed cannon” scenes or attract screens. |

## Aliens (per row)

| Alien type | `get_game_sprite` names | JSON entries | In Use | Validated | Usage |
|------------|-------------------------|--------------|--------|-----------|-------|
| Squid (row 1) | `alien_squid_1`, `alien_squid_2` | `alien_squid_1/2` | Yes | Yes | Highest-value aliens. Animated by toggling frames in `Alien.animate()`. |
| Crab (rows 2–3) | `alien_crab_1`, `alien_crab_2` | `alien_crab_1/2` | Yes | Yes | Mid-value aliens. Wider sprites (22 px). |
| Octopus (rows 4–5) | `alien_octopus_1`, `alien_octopus_2` | `alien_octopus_1/2` | Yes | Yes | Lowest-value aliens; 25 px wide. |

## Projectiles

| Owner | `get_game_sprite` name(s) | JSON entry | In Use | Validated | Notes |
|-------|---------------------------|------------|--------|-----------|-------|
| Player bullet | `bullet` | `bullet` | Yes | Yes | Single-shot bullet drawn in `src/entities/bullet.py`. |
| Alien bombs | `bomb_1` | `bomb_1` | Yes | Yes | Only `bomb_1` is used by aliens; `Bomb` now receives the sprite name explicitly. |
| UFO bombs | `bomb_2` | `bomb_2` | Yes | Yes | Newly used when UFOs pass overhead and drop ordnance. |
| Legacy bomb art | `bomb_3` | `bomb_3` | No | Yes | Spare variant kept for experimentation; hook it up if a third projectile style is needed. |

## Defensive Structures

| Component | `get_game_sprite` name(s) | JSON entry | In Use | Validated | Notes |
|-----------|---------------------------|------------|--------|-----------|-------|
| Bunker (intact) | `bunker_full` | `bunker_full` | Yes | Yes | Currently reused for every damage stage; `src/entities/bunker.py` recolors instead of swapping sprites. |
| Bunker damage placeholder | `bunker_damaged_1`, `_2`, `_3` | maps to `bunker_full` | Yes (shares art) | Yes | Logical entries exist but pull the intact art; add unique sprites when available. |
| Future bunker art | `bunker_full_v2`, `bunker_broken_{1-4}` | Same name in JSON | No | No | Placeholder entries with `validated = N`. Update once fresh bunker art is cut. |

## Effects / HUD

| Feature | Sprite names | JSON entries | In Use | Validated | Usage |
|---------|--------------|--------------|--------|-----------|-------|
| Score digits 0–7 | `digit_*` | `digit_*` | Yes | Yes | Used for HUD score output and credit counters (falls back to fonts for digits 8/9). |
| HI-SCORE text | `text_hi_score` | `text_hi_score` | Yes | Yes | Displayed at the top of the playfield for cabinet-authentic HUD layout. |
| CREDIT text | `text_credit` | `text_credit` | Yes | Yes | Rendered along the new bottom panel above the divider line. |

## Missing / To-Do Sprites

- **Bunker damage stages**: Provide unique art for `bunker_damaged_1/2/3` and update `Bunker.damage()` to swap sprites instead of just tinting.
- **Destroyed UFO indicator**: Consider adding additional FX sprites (smoke, score popup) once new art exists.

Update this document whenever we add or remap sprites so QA/design always know which assets are in play.
