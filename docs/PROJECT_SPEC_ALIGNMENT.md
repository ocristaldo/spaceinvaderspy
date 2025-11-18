# Space Invaders Project - Specification Alignment

**Date:** 2024-11-18
**Version:** v2.0 Planning Phase
**Scope:** Faithful recreation of 1978 Space Invaders arcade game

---

## Executive Summary

The Space Invaders Python project has been realigned to follow **ONLY** the official 1978 Space Invaders arcade game specification documented in `docs/space_invaders_spec.md`.

### Key Decision
**NO features will be added that are not explicitly defined in the original 1978 game specification.**

---

## Removed Features (Not in Original)

The following previously planned features are **NOT part of v2.0**:

### ❌ Phase 1: Dynamic Level Theming (REMOVED)
- **Reason:** Not in 1978 original. Original used simple color overlays, not per-level vibrant themes.
- **Status:** Design removed from V2_0_ROADMAP
- **Code Impact:** `src/ui/level_themes.py` can be removed or left as optional enhancement post-v2.0

### ❌ Phase 2: Power-up System (REMOVED)
- **Reason:** No power-ups in 1978 original
- **Status:** Cancelled
- **Code Impact:** No `src/entities/powerup.py` needed

### ❌ Phase 3: Game Modes beyond 1P/2P (REMOVED)
- **Reason:** Only single-player and 2-player alternating modes in 1978 original
- **Status:** Cancelled
- **Removed:** Endless mode, Time Attack mode ideas

### ❌ Phase 4: Difficulty Configuration Menu (REMOVED)
- **Reason:** Fixed difficulty progression in 1978 original (speed increases per wave, not selectable)
- **Status:** Cancelled
- **Code Impact:** Game difficulty is hard-coded per spec, no options menu needed

### ❌ Phase 5: Audio Enhancement (PARTIAL REMOVE)
- **Reason:** Keep only sounds from original 1978 game
- **Removed:** Per-level theme music, extra SFX not in original
- **Keep:** Invader march, laser, explosions, UFO siren (all original 1978 sounds)

### ❌ Phase 6: Auto-File Creation (REMOVED)
- **Reason:** Out of scope for core game
- **Status:** Kept in Phase 0 as infrastructure work only

### ❌ Phase 7: UI/UX Enhancements (PARTIALLY REMOVED)
- **Removed:** Pause menu, in-game settings, Tutorial, Wave preview, Power-up display
- **Keep:** High score display with initials (arcade standard enhancement)

---

## Core Features Required (Per Spec)

All of the following are from `docs/space_invaders_spec.md` and MUST be implemented:

### ✅ 1. Attract Mode
- Title screen with "SPACE INVADERS" text
- Score Advance Table (showing alien/UFO values)
- Animated demo sequences (eastereggs like fixing "PLAY" and "INSERT COIN")
- High score display
- "INSERT COIN" prompt
- Auto-cycle through demo screens
- **Spec Reference:** Lines 5-13

### ✅ 2. Coin/Credit System
- C key inserts one credit (max 99)
- Display credit count on screen
- Require credit > 0 to start game
- Deduct credit when starting
- **Spec Reference:** Lines 17-23, 21

### ✅ 3. Two-Player Mode
- 1 key starts 1-player game
- 2 key starts 2-player alternating game
- Alternating turn-based gameplay (P1 then P2)
- Separate score tracking for each player
- Switch control when one player loses a life
- Both players continue until out of lives
- Compare scores at game over
- **Spec Reference:** Lines 22-25, 89-95, 133

### ✅ 4. High Score with Player Initials
- Save high scores to disk
- Allow player to enter 3 initials when achieving high score
- Display high scores with initials
- Track player number with score
- **Spec Reference:** Lines 11, 139 (Note: Original 1978 didn't have initials, but arcade standard added this)

### ✅ 5. Game Mechanics
- **Aliens:** 55 aliens in 11×5 grid (Squid=30pts, Crab=20pts, Octopus=10pts)
- **Player:** Single cannon at bottom, 1 bullet on screen max, can move left/right only
- **Bunkers:** 4 shields that deteriorate with damage
- **UFO:** Mystery ship worth 50/100/150/300 points
- **Bombs:** 3 max on screen, aliens shoot randomly
- **Collisions:** Bullet-alien, bomb-player, bullet-shield, bomb-shield, bullet-bomb
- **Shields:** Regenerate each wave, removed if aliens descend below them
- **Wave Progression:** Aliens start faster and lower each wave
- **Difficulty:** Dynamic (speed increases as aliens die), progressive (waves get harder)
- **Spec Reference:** Lines 27-127

### ✅ 6. Scoring System
- Squid (top row): 30 points
- Crab (middle rows): 20 points
- Octopus (bottom rows): 10 points
- UFO: 50/100/150/300 points (semi-random)
- Extra life at 1500 points
- **Spec Reference:** Lines 143-159

### ✅ 7. Audio
- **Invader march:** 4-note loop, dynamic tempo (speeds up as aliens die)
- **Player laser:** Laser fire sound per shot
- **Alien hit:** Explosion sound
- **Player hit:** Distinct explosion sound
- **UFO:** Siren loop while on screen, distinct destruction sound
- **Extra life:** Fanfare/jingle at 1500 points
- **Game start/over:** Start and end sounds
- **Spec Reference:** Lines 198-216

### ✅ 8. Game Over Conditions
- Player loses all lives → Game Over
- Any alien reaches bottom of screen → Immediate Game Over
- Return to attract mode after game over
- **Spec Reference:** Lines 129-141

### ✅ 9. Visual Design
- Monochrome sprites on black background (or color overlay simulation)
- Animated aliens (2-frame animation per move)
- Shield damage with pixel-level erosion
- Explosion animations on hits
- Score display at top of screen: "SCORE<1> [score] HI-SCORE [score] SCORE<2> [score]"
- Lives display (icons or count)
- **Spec Reference:** Lines 179-195

---

## Implementation Status

### Already Implemented (v1.0.0)
- ✅ Basic game loop and alien formation movement
- ✅ Player cannon with bullet firing
- ✅ Alien movement and formation behavior
- ✅ UFO mystery ship
- ✅ Bomb dropping and collision detection
- ✅ Basic shield/bunker system
- ✅ Score tracking (basic)
- ✅ Lives system
- ✅ Audio (partial)
- ✅ Attract mode (basic)
- ✅ 1-player mode (working)
- ✅ Credit system (working)

### To Be Implemented (v2.0)
- ⏳ **High Score with Initials** - Player initials entry screen and storage
- ⏳ **Complete 2-Player Mode** - Full alternating turn-based system
- ⏳ **Audio Completion** - Dynamic march tempo, complete SFX set
- ⏳ **Shield Mechanics** - Proper pixel-level erosion instead of just tinting
- ⏳ **Wave Progression** - Progressive difficulty (speed, position, fire rate)
- ⏳ **Exact Scoring Values** - Verify all point values match spec
- ⏳ **Game Over Flow** - Proper return to attract mode and high score screen
- ⏳ **Animation Frames** - Ensure alien and explosion animations match spec
- ⏳ **Collision Polish** - All collision types per spec

### Infrastructure Only (Phase 0)
- Configuration files (.vscode, pyproject.toml, setup.py)
- Documentation cleanup and updates
- Code organization and type hints
- Test fixtures

---

## What Changed in V2_0_ROADMAP

### Before (Scope Creep)
```
Phase 1: Dynamic Level Theming with vibrant colors
Phase 2: Power-up System (5 types)
Phase 3: Game Modes (Endless, Time Attack, Arcade Perfect)
Phase 4: Difficulty Configuration (selectable difficulty)
Phase 5: Audio Enhancement (per-level music)
Phase 6: Auto-File Creation
Phase 7: UI/UX Enhancements (pause menu, settings)
```

### After (Spec-Compliant)
```
Phase 0: Foundation & Critical Fixes
Phase 1: Core Gameplay Completeness
  1.1 High Score with Initials
  1.2 Coin/Credit System (verify)
  1.3 Two-Player Mode
Phase 2: Audio Enhancement (original sounds only)
Phase 3: Visual Polish (proper shield damage, animations)
Phase 4: Game Progression & Difficulty (per spec)
Phase 5: Testing & Quality Assurance
```

---

## No Scope Creep Clause

The following are explicitly **NOT** being added to v2.0:

- ❌ New enemy types beyond Squid/Crab/Octopus
- ❌ New weapons beyond single shot
- ❌ Power-ups of any kind
- ❌ Special events or bosses
- ❌ Difficulty settings menu
- ❌ Game modes beyond 1P/2P
- ❌ Per-level themes or colors (only original overlay tints if anything)
- ❌ Pause menu with settings
- ❌ Tutorial or how-to screens
- ❌ Extra lives beyond the 1500-point bonus

**Any feature requests must be justified by reference to the 1978 Space Invaders arcade game.**

---

## Testing Checklist for v2.0

All tests must verify spec compliance:

- [ ] 1-player game flow (attract → start → play → game over → attract)
- [ ] 2-player alternating game flow
- [ ] High score entry with initials
- [ ] Exact scoring (30/20/10/50-300 points)
- [ ] Extra life at 1500 points
- [ ] Alien movement and formation (11×5 grid, speed progression)
- [ ] Shield damage and regeneration
- [ ] All collision types (bullet-alien, bomb-player, shield, projectiles)
- [ ] Audio sync (march tempo with speed, all SFX present)
- [ ] Game over conditions (lives = 0, alien lands)
- [ ] Wave progression (speed, position, fire rate increases)
- [ ] UFO behavior (periodic spawn, siren, semi-random scoring)
- [ ] Credits system (insert, display, deduct)
- [ ] Control mapping (arrows, space, C, 1, 2)

---

## References

**Primary Reference:** `docs/space_invaders_spec.md`

Key sections:
- Game Startup and Attract Mode (lines 5-13)
- Controls and Input Mapping (lines 15-25)
- Sprites (lines 27-80)
- Gameplay Mechanics (lines 83-127)
- Life System and Game Over (lines 129-141)
- Scoring System (lines 143-159)
- Game Progression and Difficulty (lines 161-173)
- Visual and Audio Design (lines 175-219)

---

## Next Steps

1. Review and approve this alignment document
2. Mark off Phase 0 infrastructure tasks
3. Begin Phase 1.1 (High Score with Initials)
4. Track progress using the updated V2_0_ROADMAP.md
5. No feature additions outside the spec
