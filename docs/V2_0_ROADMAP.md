# Space Invaders v2.0 Release Plan

**Status:** Planning Phase
**Target Release:** Q1 2025
**Current Version:** v1.0.0 ✅
**Spec Reference:** `docs/space_invaders_spec.md`

---

## 📋 Overview

v2.0 will complete a faithful recreation of the **original 1978 Space Invaders arcade game** according to the official game specifications. The focus is on implementing missing core features from the original game design while maintaining code quality and performance.

**NO features outside the original 1978 game specification will be added.**

### Core Features Required (From Spec)

Based on `space_invaders_spec.md`, the game must include:

1. **Attract Mode** - Title screen, score table, demo screens
2. **Coin System** - Credits for starting games
3. **2-Player Mode** - Alternating turn-based gameplay
4. **High Score with Initials** - Player initials entry (1978+ feature)
5. **Complete Game Loop** - Wave progression, lives system, scoring
6. **Shield Mechanics** - Destructible bunkers with pixel-level damage
7. **Audio** - Invader march sound (dynamic speed), laser/explosion effects, UFO siren
8. **Exact Scoring** - Squid (30), Crab (20), Octopus (10), UFO (50/100/150/300), Extra life at 1500 pts

---

## 🔧 Phase 0: Foundation & Critical Fixes

Before v2.0 feature development, complete infrastructure and code quality work.

### 0.1 Configuration & Infrastructure
- [x] Update .vscode/settings.json to use pytest instead of unittest
- [x] Add `src/__init__.py` with `__version__ = "2.0.0"`
- [x] Create `settings.default.json` as tracked template
- [x] Create `pyproject.toml` consolidating pytest, coverage, build configs
- [x] Update .gitignore to properly exclude user settings but track defaults
- [x] Add setup.py to enable `pip install -e .`

**Impact:** High - Enables clean package management

### 0.2 Documentation Updates
- [x] Update README.md (remove line 227 reference to deleted `src/states/`, remove placeholder on line 302)
- [x] Remove references to deleted files (CLEANUP_SUMMARY.md, DOCS_GUIDE.md)
- [ ] Create release process documentation
- [x] Document sprite atlases:
  - `SpaceInvaders.arcade.json` (343 lines) - **PRIMARY** sprite coordinates used by game
  - `SpaceInvaders.deluxe.json` (164 lines) - Alternative variant for future expansion (not used)
  - Removed: `atari.json`, `intellivision.json` (never existed, removed from README)

**Impact:** Medium - Improves maintainability

### 0.3 Code Organization
- [x] Audit `src/core/` modules - DECISION: Keep as legacy framework code (not used, but harmless)
  - `collision_manager.py` - Unused framework, pygame.sprite.groupcollide() used directly in main.py
  - `input_handler.py` - Unused framework, pygame.key.get_pressed() used directly in main.py
  - `game_engine.py` - Unused framework, initialization handled directly in main.py
  - **Status:** These can be removed in future refactoring but don't impact current code
- [ ] Add missing type hints throughout codebase
- [ ] Create comprehensive test fixtures in conftest.py

**Impact:** Medium - Reduces technical debt

---

## 🎮 Phase 1: Core Gameplay Completeness (Weeks 1-3)

### 1.1 High Score System with Player Initials

**Spec Requirement:** "Space Invaders was one of the first games to save and display the highest score achieved, though in 1978 it did not yet allow entering player initials" → **NOTE: The original 1978 game did NOT have initials, but most arcade versions added this feature. We will add it as an enhancement of the core mechanic.**

#### Tasks:
- [ ] Modify `HighScoreManager` to store `(score, initials, player_number)` tuples
- [ ] Create initials entry UI screen shown when game over occurs and score is high score
- [ ] Allow player to enter 3 initials using keyboard (A-Z)
- [ ] Save high score entries to `highscores.json` with format:
  ```json
  {
    "scores": [
      {"score": 5000, "initials": "AAA", "player": 1},
      {"score": 4500, "initials": "BBB", "player": 2}
    ]
  }
  ```
- [ ] Update high score display to show initials next to scores
- [ ] Handle both 1-player and 2-player high score entries

**Spec Source:** `space_invaders_spec.md` lines 11, 139

### 1.2 Coin/Credit System

**Spec Requirement:** "C Key – Insert a 'coin' (credit) into the game. Pressing C simulates dropping a coin in the slot, adding one credit."

#### Tasks:
- [ ] Verify credit system is fully functional (already exists)
- [ ] Ensure C key inserts credits (max 99)
- [ ] Display credits prominently on attract mode and game over screen
- [ ] Require credit > 0 to start game (1 or 2 player)
- [ ] Deduct credit when starting game

**Spec Source:** `space_invaders_spec.md` lines 17-23

### 1.3 Two-Player Mode Implementation

**Spec Requirement:** "2 Key – Start a 2-Player game... On the original machine, the two-player mode is an alternating play mode: Player 1 and Player 2 take turns"

#### Tasks:
- [ ] Implement alternating turn-based gameplay for P1 and P2
- [ ] Track separate scores and lives for P1 and P2
- [ ] Switch control between players when one loses a life
- [ ] Display "PLAYER 1" and "PLAYER 2" indicators during gameplay
- [ ] Show both players' scores on HUD: "SCORE<1> [P1_SCORE] HI-SCORE [HIGH] SCORE<2> [P2_SCORE]"
- [ ] Both players continue until both are out of lives
- [ ] After game over, compare scores and show which player won
- [ ] Award high score to the player with best score

**Spec Source:** `space_invaders_spec.md` lines 22-25, 89-95, 133

---

## 📊 Phase 2: Audio Enhancement (Week 4)

**Spec Requirement:** Complete audio system with dynamic sound effects and music from original

### 2.1 Invader March Sound (Dynamic Tempo)

- [ ] Verify invader march sound exists and plays during wave
- [ ] Implement dynamic tempo: march speed increases as aliens die
- [ ] Link march tempo to alien formation speed (should sync)
- [ ] Ensure four-note loop plays continuously during wave

**Spec Source:** `space_invaders_spec.md` lines 199-201, 209

### 2.2 Sound Effects

- [ ] Laser fire sound (player shoot)
- [ ] Alien hit explosion sound
- [ ] Player hit explosion sound (distinct from alien hit)
- [ ] UFO siren sound (looping while UFO on screen)
- [ ] UFO destruction sound (bonus sound)
- [ ] Extra life sound/fanfare (when crossing 1500 pts)
- [ ] Game start/over sounds

**Spec Source:** `space_invaders_spec.md` lines 198-216

### 2.3 Audio Implementation

- [ ] Verify all sounds are in `assets/sounds/`
- [ ] Create `AudioManager` if needed to handle sound scheduling
- [ ] Ensure sounds don't clip or overlap inappropriately
- [ ] Test audio sync with gameplay

---

## 🎨 Phase 3: Visual Polish (Week 5)

### 3.1 Shield/Bunker Mechanics

**Spec Requirement:** "Shields are stationary obstacles... provide cover... shields get eroded at impact point. Small chunks are destroyed with each hit."

#### Tasks:
- [ ] Implement pixel-perfect shield damage (not just visual tinting)
- [ ] Shields lose chunks where bullets/bombs hit
- [ ] Track shield destruction state across wave
- [ ] Regenerate shields fresh each wave
- [ ] Handle shield removal when aliens descend below their level

**Spec Source:** `space_invaders_spec.md` lines 51-59

### 3.2 Collision Detection & Hit Effects

- [ ] Verify bullet-alien collision works correctly
- [ ] Verify bomb-player collision works correctly
- [ ] Verify bomb-shield collision works correctly
- [ ] Verify bullet-bomb collision (both destroyed)
- [ ] Verify bullet-UFO collision works correctly
- [ ] Ensure alien landing detection works (game over condition)

**Spec Source:** `space_invaders_spec.md` lines 111-127

### 3.3 Visual Feedback

- [ ] Explosion sprite on alien hit (brief animation)
- [ ] Player explosion when hit by bomb
- [ ] UFO explosion when hit
- [ ] Score display on UFO hit
- [ ] Pause on alien destruction (16 frames per spec)

---

## 🎯 Phase 4: Game Progression & Difficulty

### 4.1 Wave/Level Progression

**Spec Requirement:** "Each wave, the base speed of the aliens may incrementally increase... the alien formation begins a little lower on the screen... aliens drop bombs more frequently"

#### Tasks:
- [ ] Implement progressive speed increase per wave
- [ ] Implement progressive starting position lowering per wave
- [ ] Implement progressive bomb fire rate increase per wave
- [ ] Ensure difficulty increases but no new enemy types added
- [ ] Confirm shields persist/reset properly per wave

**Spec Source:** `space_invaders_spec.md` lines 161-169

### 4.2 Scoring & Bonus Life System

- [ ] Verify scoring: Squid=30, Crab=20, Octopus=10, UFO=50/100/150/300
- [ ] Implement extra life at 1500 points (configurable?)
- [ ] Track extra lives properly
- [ ] Verify score display updates in real-time

**Spec Source:** `space_invaders_spec.md` lines 143-159

### 4.3 Game Over Conditions

- [ ] Player loses all lives → Game Over
- [ ] Any alien reaches bottom of screen → Immediate Game Over
- [ ] Both conditions trigger return to attract mode

**Spec Source:** `space_invaders_spec.md` lines 129-141

---

## 🧪 Phase 5: Testing & Quality Assurance

### 5.1 Unit Tests

- [ ] Test HighScoreManager with initials
- [ ] Test 2-player score tracking
- [ ] Test credit system
- [ ] Test wave progression
- [ ] Test collision detection

### 5.2 Integration Tests

- [ ] Full 1-player game flow
- [ ] Full 2-player game flow
- [ ] High score entry flow
- [ ] Credit system flow
- [ ] Sound timing sync

### 5.3 Manual Testing

- [ ] Play multiple full games
- [ ] Test all controls (arrows, space, C, 1, 2, P/ESC)
- [ ] Verify audio sync with gameplay
- [ ] Test attract mode loop
- [ ] Test high score display

---

## ❌ Features NOT Being Added (Outside 1978 Spec)

The following features are explicitly **NOT included** in v2.0 as they are not in the original 1978 Space Invaders:

- ❌ Power-ups (not in 1978 original)
- ❌ Multiple game modes beyond 1P/2P (not in 1978 original)
- ❌ Difficulty settings (game difficulty is fixed progression per spec)
- ❌ Dynamic level theming with vibrant colors (not in 1978 original - only overlay tints)
- ❌ Boss battles or special events (not in 1978 original)
- ❌ Weapons beyond single shot (not in 1978 original)
- ❌ New enemy types (not in 1978 original - 3 types only)
- ❌ In-game pause menu with settings (not in 1978 original)
- ❌ Tutorial/how-to screens (not in 1978 original)

---

## 📋 Summary

| Phase | Feature | Priority | Status |
|-------|---------|----------|--------|
| 0 | Infrastructure | CRITICAL | ✅ **80% Complete** |
| 0.1 | Configuration | CRITICAL | ✅ Done |
| 0.2 | Documentation | MEDIUM | ⏳ In Progress |
| 0.3 | Code Organization | MEDIUM | ✅ Audited |
| 1.1 | High Score + Initials | HIGH | ⏳ Pending |
| 1.2 | Coin/Credit System | HIGH | ✅ Mostly Done |
| 1.3 | 2-Player Mode | HIGH | ⏳ Pending |
| 2 | Audio Enhancement | HIGH | ⏳ Pending |
| 3 | Visual Polish | MEDIUM | ⏳ Pending |
| 4 | Wave Progression | HIGH | ⏳ In Progress |
| 5 | Testing | CRITICAL | ⏳ Pending |

---

## Notes

- All features must align with `space_invaders_spec.md`
- No scope creep beyond the 1978 original game
- Focus on accuracy and faithful recreation
- Keep code clean and maintainable
- Comprehensive testing before release
