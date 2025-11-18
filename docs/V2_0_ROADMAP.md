# Space Invaders v2.0 Release Plan

**Status:** Planning Phase
**Target Release:** Q1 2025
**Current Version:** v1.0.0 ✅

---

## 📋 Overview

v2.0 will transform Space Invaders from a classic recreation into a feature-rich, modern arcade experience with dynamic visuals, gameplay variety, and expanded mechanics. The release focuses on:

1. **Dynamic Level Theming** - Vibrant, changing color schemes per level
2. **Power-up System** - Strategic gameplay elements
3. **Multiple Game Modes** - Endless, Time Attack, Arcade Perfect
4. **Improved Difficulty** - Configurable difficulty levels with scaling mechanics
5. **Auto-file Creation** - Robust gitignored file handling
6. **Audio Enhancement** - Full SFX implementation and music integration

---

## 🔧 Phase 0: Foundation & Cleanup (CRITICAL)

Before v2.0 development begins, establish a solid base by completing critical refactoring and infrastructure improvements.

### 0.1 Bug Fixes & Quick Wins
- [x] Fix coverage.ini syntax error (line 10: `if __name__ == "__main__":`)
- [x] Remove duplicate line in menu.py (line 55: `self.options_music_on = False`)
- [ ] Update .vscode/settings.json to use pytest instead of unittest
- [ ] Add `src/__init__.py` with `__version__ = "2.0.0"`
- [ ] Create `settings.default.json` as tracked template

**Estimated Time:** 30 minutes
**Impact:** High - Fixes technical debt before new features

### 0.2 Configuration Infrastructure
- [ ] Create `pyproject.toml` consolidating pytest, coverage, build configs
- [ ] Create `settings.default.json` template with all default settings
- [ ] Implement settings schema validation (use JSON schema or dataclass)
- [ ] Update .gitignore to properly exclude user settings but track defaults
- [ ] Add setup.py to enable `pip install -e .`

**Estimated Time:** 90 minutes
**Impact:** Medium - Improves packaging and configuration management

### 0.3 Code Quality & Organization
- [ ] Audit `src/core/` modules (collision_manager, input_handler, game_engine) - integrate or remove
- [ ] Add missing type hints throughout codebase
- [ ] Create comprehensive test fixtures in conftest.py
- [ ] Add asset validation tests (verify sprites exist in atlases)
- [ ] Document why duplicate sprite atlases exist (deluxe, atari, intellivision)

**Estimated Time:** 180 minutes
**Impact:** Medium - Reduces technical debt

### 0.4 Documentation Updates
- [ ] Update README.md (remove line 227 reference to `src/states/`, remove placeholder on line 302)
- [ ] Document release process in docs/
- [ ] Create Architecture Decision Records (ADRs) for core design choices
- [ ] Update CONFIGURATION.md with all sources of truth for settings
- [ ] Remove references to deleted files (CLEANUP_SUMMARY.md, DOCS_GUIDE.md)

**Estimated Time:** 120 minutes
**Impact:** Medium - Improves maintainability and onboarding

---

## 🎨 Phase 1: Dynamic Level Theming (Weeks 1-2)

### Feature: Dynamic Color Schemes Per Level

Every level gets a unique, vibrant color palette that affects:
- Player ship tint
- Alien types (squid, crab, octopus) - new vibrant colors
- Bunker colors
- Bullet/bomb colors
- Text and HUD elements
- Background effects (optional parallax stars)

### 1.1 Palette System Design

Create `src/ui/level_themes.py`:

```python
LEVEL_THEMES = {
    1: {
        "name": "Classic Green",
        "player": (180, 255, 180),
        "alien_squid": (100, 255, 100),
        "alien_crab": (150, 200, 255),
        "alien_octopus": (255, 255, 100),
        "ufo": (255, 180, 180),
        "bunker": (180, 200, 100),
        "bullet": (255, 255, 255),
        "bomb_alien": (255, 100, 100),
        "bomb_ufo": (255, 150, 150),
        "hud_text": (255, 255, 255),
        "background_effect": None,
    },
    2: {
        "name": "Neon Purple",
        "player": (255, 100, 255),
        # ... more vibrant colors
    },
    # ... up to 8 themes (cycles after)
}
```

### 1.2 Implementation Tasks
- [ ] Create level theme system with 8+ distinct palettes (vibrant colors)
- [ ] Integrate themes with ColorScheme manager
- [ ] Update all sprite tinting to use theme colors
- [ ] Add theme preview in menu
- [ ] Add optional background effects (stars, grid, glow)
- [ ] Test theme transitions at level boundaries

**Estimated Time:** 240 minutes
**Impact:** HIGH - Visual enhancement, core v2.0 feature

---

## 🎁 Phase 2: Power-up System (Weeks 2-3)

### Feature: Collectible in-game power-ups

Power-ups spawn randomly when aliens die, fall from the top, and provide temporary benefits.

### 2.1 Power-up Types

| Icon | Name | Effect | Duration | Spawn Rate |
|------|------|--------|----------|-----------|
| 🔫 | Rapid Fire | Fire up to 5 bullets at once | 8 seconds | 10% |
| 🛡️ | Shield | Invincibility to bombs | 5 seconds | 8% |
| 🐢 | Slow Time | Reduce alien speed by 50% | 6 seconds | 8% |
| ✖️ | Multi-Shot | Fire 3 bullets in spread | 10 seconds | 12% |
| ⭐ | 2x Score | Double points for kills | 5 seconds | 7% |

### 2.2 Implementation Tasks
- [ ] Create Power-up entity class (src/entities/powerup.py)
- [ ] Implement power-up spawning logic in game engine
- [ ] Create power-up collision detection
- [ ] Implement each power-up effect with duration system
- [ ] Add visual effects for power-up collection
- [ ] Add SFX for power-up sounds
- [ ] Display active power-ups on HUD
- [ ] Test interaction with existing mechanics (bunkers, UFOs, etc.)

**Estimated Time:** 300 minutes
**Impact:** HIGH - Core gameplay expansion

---

## 📊 Phase 3: Multiple Game Modes (Weeks 3-4)

### Feature: Game mode selection before play

Three distinct modes for different playstyles:

#### 3.1 Arcade Perfect
- Original rules, no assists
- No power-ups
- Classic scoring
- Goal: High score

#### 3.2 Endless Mode
- Waves never end, difficulty scales indefinitely
- Power-ups enabled
- Wave counter continues past 8
- Goal: Survive as long as possible

#### 3.3 Time Attack
- 60-second game duration
- Score as many points as possible
- Power-ups enabled
- Goal: Highest score in time limit

### 3.2 Implementation Tasks
- [ ] Create GameMode enum and mode selection menu
- [ ] Implement mode-specific logic in GameStateManager
- [ ] Create UI screen for mode selection at game start
- [ ] Implement Endless mode with infinite waves
- [ ] Implement Time Attack mode with countdown timer
- [ ] Adjust difficulty scaling per mode
- [ ] Add leaderboards per mode (separate high scores)
- [ ] Test all mode transitions and completions

**Estimated Time:** 240 minutes
**Impact:** HIGH - Replayability

---

## 🎚️ Phase 4: Difficulty Configuration (Weeks 4-5)

### Feature: In-game difficulty settings

### 4.1 Difficulty Levels

| Level | Alien Speed | Bomb Rate | Bunker Health | Power-up Rate |
|-------|------------|-----------|---------------|---------------|
| Easy | 0.3x base | 0.5x base | 1.5x normal | 1.5x normal |
| Normal | 1.0x base | 1.0x base | 1.0x normal | 1.0x normal |
| Hard | 1.5x base | 1.5x base | 0.75x normal | 0.75x normal |
| Insane | 2.0x base | 2.0x base | 0.5x normal | 0.5x normal |

### 4.2 Implementation Tasks
- [ ] Create difficulty setting interface in Options menu
- [ ] Implement difficulty multipliers in game engine
- [ ] Apply multipliers to alien speed calculations
- [ ] Apply multipliers to bomb spawn rate
- [ ] Apply multipliers to bunker health values
- [ ] Apply multipliers to power-up spawn rates
- [ ] Persist selected difficulty in settings.json
- [ ] Add difficulty indicator to HUD
- [ ] Test extreme cases (very easy, very hard)

**Estimated Time:** 180 minutes
**Impact:** MEDIUM - Accessibility and replayability

---

## 🔊 Phase 5: Audio Enhancement (Weeks 5)

### Feature: Full SFX implementation and music integration

### 5.1 Missing Audio Effects
- [ ] Verify all SFX files exist and load properly:
  - shoot, explosion, invaderkilled
  - fastinvader1-4 (movement cycle)
  - ufo_lowpitch, ufo_highpitch
  - extra_life, power-up_grab
- [ ] Add new SFX:
  - Power-up activation sound per type
  - Level transition/theme change sound
  - Difficulty warning sound (increasing danger)
- [ ] Implement music tracks:
  - Menu background (looping)
  - Per-level background track (optional, cycles with theme)
  - Game over/level complete jingles
- [ ] Audio mixing and volume balancing
- [ ] Create audio settings (Master, SFX, Music volume sliders)

### 5.2 Implementation Tasks
- [ ] Complete AudioManager implementation
- [ ] Add missing sound files to assets/audio/
- [ ] Implement volume control in Options menu
- [ ] Create audio theme integration with level themes
- [ ] Test audio playback across all game states
- [ ] Add audio mute functionality per channel

**Estimated Time:** 150 minutes
**Impact:** MEDIUM - Immersion

---

## 🐛 Phase 6: Auto-File Creation & Robustness (Week 5)

### Feature: Games don't crash if gitignored files are missing

### 6.1 File Management
- [ ] Ensure `highscores.json` auto-creates with default structure
- [ ] Ensure `settings.json` auto-creates from `settings.default.json`
- [ ] Add file corruption detection and recovery
- [ ] Add fallback defaults if files can't be written

### 6.2 Implementation Tasks
- [ ] Update HighScoreManager to create file if missing
- [ ] Update SettingsManager to create file if missing
- [ ] Create validation functions for JSON structure
- [ ] Implement corruption recovery (reset to defaults)
- [ ] Add logging for file creation/recovery events
- [ ] Test on fresh installation (no existing files)

**Estimated Time:** 90 minutes
**Impact:** HIGH - Reliability

---

## 📱 Phase 7: UI/UX Enhancements (Week 6)

### Feature: Better menus and user experience

### 7.1 Improvements
- [ ] Create proper Pause menu (Resume/Quit/Options)
- [ ] Settings menu in-game (not just config files)
- [ ] Tutorial screen explaining controls and scoring
- [ ] Wave preview (show next formation before it spawns)
- [ ] Difficulty indicator on HUD
- [ ] Active power-up display on HUD
- [ ] Score milestone announcements ("500 points!", "1000 points!")
- [ ] Screen shake effect on big events (UFO kill, level complete)

### 7.2 Implementation Tasks
- [ ] Design menu layouts (wireframes)
- [ ] Implement pause menu state
- [ ] Create in-game settings menu
- [ ] Build tutorial/how-to-play screen
- [ ] Implement screen effects (shake, flash)
- [ ] Add status indicators to HUD
- [ ] Test menu navigation and transitions

**Estimated Time:** 240 minutes
**Impact:** MEDIUM - User experience

---

## 🎮 Phase 8: Optional Advanced Features (Post-release)

These are nice-to-haves that can be added after v2.0 if time/interest permits:

### 8.1 Input Options
- [ ] Gamepad/joystick support (SDL2 controllers)
- [ ] Customizable key bindings
- [ ] Mouse aim option
- [ ] Touchscreen support (if needed)

### 8.2 Leaderboard Features
- [ ] Player name input (currently just scores)
- [ ] Per-mode leaderboards (Arcade, Endless, Time Attack)
- [ ] Achievements/badges system
- [ ] Optional cloud sync (online leaderboards)

### 8.3 Visual Enhancements
- [ ] Parallax scrolling background (subtle stars)
- [ ] Particle effects (better explosions)
- [ ] Screen effects per level theme
- [ ] Alt sprite styles (deluxe, retro, etc.)

### 8.4 Accessibility
- [ ] High contrast mode
- [ ] Large font option
- [ ] Color-blind friendly palettes
- [ ] Screen reader support

### 8.5 Replay & Analysis
- [ ] Record game replays
- [ ] Playback functionality
- [ ] Stats tracking (longest wave, best combo, etc.)

---

## 📊 Testing & QA (Throughout All Phases)

### Test Coverage Requirements
- [ ] Unit tests for all new features (maintain 100% coverage)
- [ ] Integration tests for mode transitions
- [ ] Power-up interaction tests (with bunkers, aliens, bombs)
- [ ] Difficulty scaling validation tests
- [ ] Theme transition tests
- [ ] File corruption recovery tests
- [ ] Audio playback tests (mocked in CI)
- [ ] Manual gameplay testing on multiple platforms

### QA Checklist
- [ ] Test on Windows 10/11
- [ ] Test on macOS (Intel + Apple Silicon)
- [ ] Test on Linux
- [ ] Test on Raspberry Pi (if supported)
- [ ] Test with various screen sizes and scales
- [ ] Test all mode combinations
- [ ] Test all difficulty levels
- [ ] Test power-up interactions
- [ ] Verify no regressions in v1.0 features
- [ ] Performance profiling (60 FPS target)

---

## 📈 Release Checklist

### Pre-Release
- [ ] All Phase 0-7 tasks completed
- [ ] 100% test coverage maintained
- [ ] All tests passing (CI green)
- [ ] Documentation updated
- [ ] RELEASE_NOTES.md written
- [ ] Version bumped to 2.0.0
- [ ] Git tags created
- [ ] Performance benchmarks completed

### Release
- [ ] Tag commit with v2.0.0
- [ ] Generate release notes
- [ ] Upload artifacts
- [ ] Create GitHub release
- [ ] Announce on project channels

### Post-Release
- [ ] Monitor bug reports
- [ ] Plan v2.1 with community feedback
- [ ] Consider Phase 8 features based on user interest

---

## 🎯 Success Metrics

- [ ] v2.0.0 released with all Phases 1-7 complete
- [ ] No regressions from v1.0.0
- [ ] 100% test coverage maintained
- [ ] All game modes fully functional
- [ ] Dynamic themes visible and polished
- [ ] Power-ups balanced and fun
- [ ] Zero crashes on fresh installs
- [ ] Performance: 60 FPS on target platforms

---

## 📝 Related Documentation

- See `docs/ROADMAP.md` for v2.1+ plans
- See `docs/GAMEPLAY_OVERVIEW.md` for current implementation details
- See `docs/CONFIGURATION.md` for settings reference
- See `docs/space_invaders_spec.md` for arcade accuracy goals

