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
| `name` | Identifier requested via `get_game_sprite(\"name\", scale)` |
| `platform` | Only `\"arcade\"` is active today, but other atlases share the format |
| `frame` | Animation frame index (1-based) for toggled sprites |
| `x`, `y`, `width`, `height` | Pixel bounds inside `SpaceInvaders.png` |
| `description` | Plain-language usage note (new) |

When you add, rename, or relocate sprites be sure to:

1. Update the JSON entry (coordinates + description).
2. Adjust `ARCADE_SPRITE_MAPPING` in `src/utils/sprite_sheet.py` if the logical
   names change.
3. Document the change in the relevant section below so artists/designers know
   what moved.

## Core Entities

| System | `get_game_sprite` name | JSON entry | Purpose / Notes |
|--------|-----------------------|-----------|------------------|
| Player cannon | `player` | `player_cannon_jumbo_arcade_frame1` | Player ship sprite (`src/entities/player.py`). Any replacement must stay 16×16 or adjust collision boxes. |
| Player explosion | `player_explosion` | `explosion_arcade_frame1` | Placeholder for player-death FX (currently unused; we overlay text instead). |
| UFO | `ufo` | `ufo_jumbo_arcade_frame1` | Used by `src/entities/ufo.py`. Travels across the top of the playfield. |

## Aliens (per row)

| Alien type | `get_game_sprite` names | JSON entries | Usage |
|------------|-------------------------|--------------|-------|
| Squid (row 1) | `alien_squid_1`, `alien_squid_2` | `invader_squid_jumbo_arcade_frame1/2` | Highest-value aliens. Animated by toggling frames in `Alien.animate()`. |
| Crab (rows 2–3) | `alien_crab_1`, `alien_crab_2` | `invader_crab_jumbo_arcade_frame1/2` | Mid-value aliens. Wider sprites (22 px). |
| Octopus (rows 4–5) | `alien_octopus_1`, `alien_octopus_2` | `invader_octopus_jumbo_arcade_frame1/2` | Lowest-value aliens; 25 px wide. |

## Projectiles

| Owner | `get_game_sprite` name | JSON entry | Notes |
|-------|------------------------|------------|-------|
| Player bullet | `bullet` | `projectile_player_missile_arcade` | Single-shot bullet drawn in `src/entities/bullet.py`. |
| Alien bombs | `bomb_1`, `bomb_2`, `bomb_3` | `projectile_enemy_bomb_arcade_variant(1|2|3)` | Randomized bombs dropped in `Bomb.__init__`. |

## Defensive Structures

| Component | `get_game_sprite` name | JSON entry | Notes |
|-----------|------------------------|------------|-------|
| Bunker (intact) | `bunker_full` | `barricade_arcade_full` | Currently reused for every damage stage; `src/entities/bunker.py` recolors instead of swapping sprites. |
| Bunker damage placeholder | `bunker_damaged_1`, `_2`, `_3` | (mapped to same JSON entry as `bunker_full`) | Mappings exist but point to the intact sprite; consider adding unique art for each damage stage. |

## Effects / HUD

| Feature | Sprite names | JSON entries | Usage |
|---------|--------------|--------------|-------|
| Explosion FX | `explosion` | `explosion_arcade_frame1` | Generic explosion (currently unused). |
| Digits 0–7 | `digit_*` | `digit_*_arcade` | Not yet wired up; console uses fonts instead. |
| HI-SCORE text | (none yet) | `text_hi_score_arcade` | Available for future HUD polish. |
| CREDIT text | (none yet) | `text_credit_arcade` | Available for attract/credit screen. |

## Missing / To-Do Sprites

- **Bunker damage stages**: Provide unique art for `bunker_damaged_1/2/3` and update `Bunker.damage()` to swap sprites instead of just tinting.
- **Explosion variants**: The JSON includes `explosion_arcade_frame2`; map it in `get_game_sprite` to animate cannon/alien destruction.
- **Scoreboard text**: Map `text_hi_score_arcade` and digit sprites to render authentic HUD/credit screens.
- **Destroyed UFO indicator**: Consider adding a brief explosion or score popup sprite when the UFO dies.

Update this document whenever we add or remap sprites so QA/design always know which assets are in play.
