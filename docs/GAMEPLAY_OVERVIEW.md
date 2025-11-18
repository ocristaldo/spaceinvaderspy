# Space Invaders Python – Gameplay & Systems Guide

This document walks through every major component of the Space Invaders Python clone—from how the graphics pipeline works to the flow of a full play session. Use it as a reference when tuning mechanics, aligning sprites, or documenting behavior for teammates.

## 1. Game Structure at a Glance
- **Engine:** Single `Game` class in `src/main.py` drives the loop (input → update → draw).
- **Entities:** Player ship, alien invaders, UFO, bullets, bombs, and bunkers are defined in `src/entities`.
- **Assets:** All visuals live on one sprite sheet (`assets/images/SpaceInvaders.png`) plus JSON atlases per platform (Arcade/Atari/Deluxe/Intellivision).
- **Utilities:** `SpriteSheet` extracts sprites from the sheet; `SpriteViewer` is an in-engine debugging tool; `logger.py` centralizes structured logging.
- **Configuration:** `src/config.py` and `src/constants.py` expose screen size, colors, spacing, and timing constants.

## 2. Visual System & Graphics Flow
1. **Sprite Sheet Loading**
   - `SpriteSheet` (`src/utils/sprite_sheet.py`) loads `SpaceInvaders.png` and a matching JSON coordinate file (Arcade by default).
   - Each JSON entry lists `x`, `y`, `width`, `height`, and optional frame ids; these rectangles carve sprites from the texture atlas.
2. **Sprite Lookup**
   - Logical game names (`player`, `alien_crab_1`, `bunker_full`, etc.) map to JSON entries via `ARCADE_SPRITE_MAPPING`.
   - `get_game_sprite()` caches the sheet and returns a `pygame.Surface`, scaling by `config.SCALE` (currently ×2).
3. **Fallbacks**
   - If assets fail to load, entities draw simple colored primitives to keep the game playable while logging warnings.
4. **Testing Tools**
   - Press `S+1…4` in-game to open the Sprite Viewer (`src/utils/sprite_viewer.py`) for Arcade, Atari, Deluxe, or Intellivision atlases. Use `←/→` to page through sprites with their coordinates/dimensions; `R` returns to gameplay.

## 3. Core Gameplay Loop
1. **Initialization**
   - `Game.__init__()` sets up Pygame, spawns the player, creates the alien grid (5×11), lays down four bunkers, and resets scoring/lives.
2. **Input Handling**
   - Continuous polling via `pygame.key.get_pressed()` for movement and sprite viewer combos.
   - Discrete `KEYDOWN` events trigger shooting (Space), restarting after game over (R), and quitting (Q).
3. **Update Phase**
   - Player updates read the key state for left/right movement with boundary clamping.
   - Aliens march horizontally; hitting a wall flips direction and drops the formation down by 20px. Speed ramps via `update_alien_speed()` as aliens are destroyed.
   - Bomb spawning: 2% chance per frame for any remaining alien to drop a bomb.
   - UFO spawns every `config.UFO_INTERVAL` milliseconds and traverses the top of the screen.
   - Collision checks resolve (a) bullet vs alien/UFO/bunkers, (b) bomb vs player/bunkers. Hits award points, reduce lives, or damage bunkers.
   - Projectiles self-manage lifetime (off-screen cleanup).
4. **Draw Phase**
   - Renders either the Sprite Viewer or the live game state (background, entities, HUD with score & lives).
5. **Game Over Handling**
   - Conditions: aliens reach bunker line, player loses all lives, or player clears every alien.
   - A semi-transparent overlay displays “GAME OVER” with restart instructions. Holding `R` resets all actors via `reset_game()`.

## 4. Player Mechanics
- **Movement:** Horizontal only, speed 5 pixels per frame, constrained to the playfield (`rect.clamp_ip`).
- **Fire Control:** One bullet on screen at a time (classic rule). Bullets spawn from `Player.get_bullet_spawn_position()` (ship mid-top).
- **Lives:** Starts with `constants.LIVES_NUMBER` (3). Bomb hits decrement lives; no invulnerability window yet.
- **Scoring:** Destroying aliens adds their `value` (30/20/10). UFO awards a random 50–300 points. HUD updates immediately.

## 5. Enemy Mechanics
### Alien Formation
- **Layout:** Created via `create_aliens()` with configurable margins and spacing.
- **Animation:** Each alien stores two frames; `alien.animate()` toggles every ~0.5 seconds for the classic wiggle.
- **Movement Rules:** The formation shares one horizontal velocity (`alien_speed`). Hitting a screen edge causes an entire-row drop and direction flip. Crossing the bunker line wins the wave for the aliens.
- **Bombing:** Random alien chosen for each spawn; bombs travel downward at `config.BOMB_SPEED`.

### UFO (Mystery Ship)
- Appears at the top every `config.UFO_INTERVAL` ms.
- Moves horizontally at a constant speed (2 px/frame) and despawns once off-screen.
- Shots award a random bonus (50/100/150/300).

## 6. Defensive Structures – Bunkers
- Four bunkers spaced evenly across the lower-third of the playfield.
- Each bunker starts with 4 health. `Bunker.damage()` decrements health, updates the sprite (or color fallback), and removes the bunker when health reaches zero.
- Both friendly bullets and enemy bombs chip away at bunkers, so careless shooting erodes cover.

## 7. Stage Flow: From Start to End
1. **Opening State**
   - Player ship idles near the bottom; aliens occupy the upper half in five rows. Score and lives UI show zero/lives remaining.
2. **Early Stage**
   - Aliens move slowly side-to-side. Player focuses on thinning top rows for high-value targets while staying behind bunkers.
   - Bomb frequency is low, giving the player time to adjust.
3. **Mid Stage**
   - As aliens fall, `alien_speed` increases, narrowing dodge windows. Bombs spawn more often because they are attempted every frame regardless of count.
   - Bunkers accumulate damage from bombs and stray bullets, forcing the player into exposed positions.
4. **Late Stage**
   - Only a few aliens remain, now moving very quickly with sharp horizontal shifts after each edge hit.
   - Surviving aliens likely sit lower on the screen, threatening a ground invasion.
5. **End States**
   - **Player Victory:** All aliens destroyed → game over overlay celebrates the clear; press `R` to restart.
   - **Alien Victory:** Either (a) any alien reaches the lower safety line (bottom − 60 px) after a drop, or (b) bombs deplete all player lives. Overlay shows “GAME OVER” with restart instructions.
   - UFO kills are optional but boost score mid-stage.

## 8. Additional Systems & Utilities
- **Logging:** `src/utils/logger.py` configures module-level loggers used across entities and utilities to capture asset loading failures, hits, spawns, and errors. The main game also writes to `game.log`.
- **Configuration Tuning:** Tweak difficulty by editing `src/config.py` (margins, spacing, speeds) or `src/constants.py` (lives count, colors). The game reads these on start/reset.
- **Testing Sprites & Layouts:** Use the Sprite Viewer to verify JSON coordinates after editing. It is the fastest way to confirm alignment issues mentioned in development notes.

## 9. Suggested Extension Points
- Implement proper stage progression (multiple waves, increasing speed multipliers).
- Add audio cues (shots, explosions) for better feedback.
- Introduce power-ups (multi-shot, shields) and new enemy behaviors.
- Track high scores and persist them between runs.

With this guide you should be able to trace every visual, mechanical, and gameplay element from source to screen, making future tweaks or documentation updates straightforward.
