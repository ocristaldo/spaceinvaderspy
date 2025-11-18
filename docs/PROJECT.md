# 📋 Space Invaders Py - Project Management Hub

**Last Updated:** November 17, 2025  
**Version:** 0.2.0 (Audio, High Score, Extra Lives)  
**Status:** ✅ Quick wins complete, ready for next phase

---

## 🎯 Project Overview

A Python/Pygame recreation of classic Space Invaders guided by the original cabinet behaviors captured in `space_invaders_spec.md`. The game is **playable today** with core mechanics complete, and future improvements focus on matching/expanding the 1978 ruleset (attract mode, score table, pacing).

---

## 📊 Current Status: Phase 2 ✅ Complete

### What's Done (as of today)
- ✅ Core Space Invaders gameplay (movement, shooting, formations)
- ✅ Collision detection (bullets, bombs, bunkers)
- ✅ Scoring system (per-alien values, UFO bonuses)
- ✅ Lives system (3 lives, game over detection)
- ✅ **Audio System** (muted by default, 'A' to toggle)
- ✅ **High Score Persistence** (JSON storage)
- ✅ **Extra Lives Milestones** (20k + every 70k points)
- ✅ Sprite system with 4 platform variants (Arcade, Atari, Deluxe, Intellivision)
- ✅ Comprehensive logging and error handling
- ✅ 10/10 Unit tests passing
- ✅ CI/CD pipeline with test coverage

### What's Working Right Now
```
Play the game:  python -m src.main

Controls:
  ← → ......... Move ship left/right
  SPACE ...... Fire
  A ......... Toggle audio
  P/ESC ..... Pause
  Q ......... Quit
  R ......... Restart (after game over)
```

---

## 🗺️ Development Roadmap

### Phase 3: Foundation Systems (NEXT - 1-2 weeks)
**Goal:** Enable all UI and game state management

- [ ] **Game State Machine** - Proper states (Menu, Playing, Paused, GameOver)
- [ ] **Main Menu UI** - Attract mode, 1P/2P selection, options screen
- [ ] **Pause Overlay** - Pause/resume without losing game state
- [ ] **Level Progression** - Multi-wave gameplay with difficulty scaling

**Why First:** All other features depend on clean state management

---

### Phase 4: Cabinet Accuracy Pass (2-3 weeks)
**Goal:** Match the original Space Invaders cabinet presentation

- [ ] **Attract Mode** - Title + Insert Coin prompt, score advance table, looping demo
- [ ] **Credit/Start Flow** - Simulated coin drop + 1P/2P starts, alternating turns scaffold
- [ ] **Score Advance Table Overlay** - Authentic point-value display before gameplay
- [ ] **Explosion/Bunker Art** - Swap sprites per state (player, UFO, bunker damage)

**Why Next:** Builds on existing menu/state machine to deliver the vintage experience

---

### Phase 5: Optional Enhancements & Release (1-2 weeks)
**Goal:** Add QoL without sacrificing authenticity + prepare release

- [ ] **Performance Tuning** - Target 60 FPS, profile collision detection
- [ ] **Comprehensive Tests** - 70%+ coverage, integration tests
- [ ] **Modern Toggles** - Accessibility options (multi-shot default, slow mode)
- [ ] **Release Package** - Setup pip distribution, artifacts

---

## 📈 Progress Tracking

### Completed Milestones
| Milestone | Status | Date | Details |
|-----------|--------|------|---------|
| M1: Roadmap + CI | ✅ | Nov 2025 | Foundational docs + GitHub Actions |
| M2: Audio + High Score + Extra Lives | ✅ | Nov 17, 2025 | 3 systems, 10 tests, 100% passing |

### Next Milestones
| Milestone | Target | Details |
|-----------|--------|---------|
| M3: Game States + Menu | Nov 24, 2025 | Foundation for all UI |
| M4: Level Progression | Dec 1, 2025 | Multi-wave gameplay |
| M5: Cabinet Accuracy | Dec 8, 2025 | Attract mode, score table, explosions |
| M6: Polish + Release | Dec 15, 2025 | Performance, tests, packaging |

---

## 🎮 Feature Matrix

### Game Systems (Status)
| System | Status | Location | Tests | Notes |
|--------|--------|----------|-------|-------|
| Core Gameplay | ✅ Complete | `src/main.py` | ✅ Yes | Movement, shooting, collision |
| Audio Management | ✅ Complete | `src/utils/audio_manager.py` | ✅ 4/4 | Muted by default, 'A' toggle |
| High Scores | ✅ Complete | `src/utils/high_score_manager.py` | ✅ 5/5 | JSON persistent storage |
| Extra Lives | ✅ Complete | `src/main.py` | ✅ 1/1 | 20k + every 70k points |
| Game States | ⏳ Next | `src/systems/` | ⚠️ Needed | Menu, Playing, Paused, GameOver |
| Menu UI | ⏳ Next | `src/ui/menu.py` | ⚠️ Needed | Attract, select, options |
| Level Progression | ⏳ Planned | `src/systems/` | ⚠️ Needed | Multi-wave, difficulty scaling |
| Attract Mode Demo | ⏳ Planned | `src/core/` | ⚠️ Needed | Title/credit/score table loop |
| Challenge Stages | ⏳ Planned | `src/systems/` | ⚠️ Needed | Bonus non-attacking waves |
| Tractor Beam | ⏳ Planned | `src/entities/alien.py` | ⚠️ Needed | Capture/rescue mechanic |
| Dual Fighter | ⏳ Planned | `src/entities/player.py` | ⚠️ Needed | Double shots, wider hitbox |
| 2-Player Mode | ⏳ Planned | `src/systems/` | ⚠️ Needed | Alternating turns |

---

## 📁 Project Structure

```
spaceinvaderspy/
├── src/
│   ├── main.py                    # Main game loop + core logic
│   ├── config.py                  # Game configuration (screen size, speeds)
│   ├── constants.py               # Game constants (colors, counts)
│   ├── entities/
│   │   ├── player.py              # Player ship
│   │   ├── alien.py               # Alien enemies
│   │   ├── bullet.py              # Projectiles (player + enemy)
│   │   ├── bunker.py              # Defensive structures
│   │   └── ufo.py                 # Bonus enemy
│   ├── systems/
│   │   └── game_state_manager.py  # (PLANNED) State machine
│   ├── ui/
│   │   └── menu.py                # (PLANNED) Menu UI
│   └── utils/
│       ├── audio_manager.py       # Audio system (complete)
│       ├── high_score_manager.py  # High score persistence (complete)
│       ├── logger.py              # Logging setup
│       ├── sprite_sheet.py        # Sprite loading
│       └── sprite_viewer.py       # Interactive sprite viewer
├── tests/
│   ├── unit/
│   │   ├── test_quick_wins.py     # Audio, high score, extra lives tests
│   │   ├── test_entities.py
│   │   ├── test_bomb_collision.py
│   │   └── test_menu_pause.py
│   ├── integration/
│   │   └── test_game_flow.py
│   └── __init__.py
├── docs/
│   └── GAMEPLAY_OVERVIEW.md      # Current systems architecture
│   └── DEVELOPMENT_STATUS.md      # Detailed feature status
├── assets/
│   ├── images/
│   │   ├── SpaceInvaders.png      # Sprite sheet
│   │   ├── SpaceInvaders.arcade.json
│   │   ├── SpaceInvaders.atari.json
│   │   ├── SpaceInvaders.deluxe.json
│   │   └── SpaceInvaders.intellivision.json
│   └── sounds/                    # (AUDIO FILES NEEDED)
├── .github/
│   └── workflows/ci.yml           # GitHub Actions pipeline
├── PROJECT.md                     # (THIS FILE) - Project management hub
├── README.md                      # User-facing overview
├── ROADMAP.md                     # High-level roadmap
├── CHANGELOG.md                   # Release notes
├── QUICK_START.md                 # Getting started guide
├── requirements.txt               # Python dependencies
└── pytest.ini                     # Test configuration
```

---

## ⚡ Next Action Items (Priority Order)

### Phase 3, Week 1: State Machine Foundation
1. **Create `src/systems/game_state_manager.py`**
   - Implement state enum (MENU, PLAYING, PAUSED, GAME_OVER)
   - State transition logic
   - ~100 lines

2. **Update `src/main.py` to use state machine**
   - Replace `self.state` string with enum
   - Refactor update/draw to check state
   - ~50 lines modified

3. **Create basic `src/ui/menu.py`**
   - MenuState class with draw method
   - Simple text-based menu (can be visual later)
   - ~150 lines

4. **Write tests for state transitions**
   - Test state machine logic
   - ~50 lines

**Acceptance Criteria:**
- Game starts in MENU state
- Can select "Start" to go to PLAYING
- P key toggles PAUSED state
- All tests pass

---

## 🧪 Testing Strategy

### Current Coverage
- **Total Tests:** 10 (all passing ✅)
- **Unit Tests:** AudioManager (4), HighScoreManager (5), Extra Lives (1)
- **Coverage Target:** 60%+ by end of Phase 3

### Test Pyramid
```
               /\
              /  \   E2E Tests (Game flow: menu→play→over)
             /____\
            /      \
           /        \ Integration Tests (State transitions, scoring)
          /__________\
         /            \
        /              \ Unit Tests (Individual systems)
       /______________\
```

### Adding Tests
```bash
# Run tests
pytest tests/ -v

# Check coverage
pytest tests/ --cov=src --cov-report=term

# Run specific test
pytest tests/unit/test_quick_wins.py::TestAudioManager -v
```

---

## 🚀 How to Contribute

### Setup Development Environment
```bash
# Clone repo
git clone <repo-url>
cd spaceinvaderspy

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run game
python -m src.main

# Run tests
pytest tests/ -v
```

### Development Workflow
1. **Create feature branch:** `git checkout -b feature/state-machine`
2. **Write tests first:** `tests/unit/test_state_machine.py`
3. **Implement feature:** `src/systems/game_state_manager.py`
4. **Run tests:** `pytest tests/`
5. **Commit with message:** `feat: Add game state machine`
6. **Push and create PR**

### Code Standards
- Type hints on public methods
- Docstrings for all classes and methods
- Tests for all new logic
- No breaking changes without discussion
- Clear git commit messages

---

## 📚 Key Documentation

| Document | Purpose | Audience |
|----------|---------|----------|
| **PROJECT.md** (this) | Central hub for project status | Everyone |
| **README.md** | User-facing overview + setup | New players/contributors |
| **ROADMAP.md** | High-level product roadmap | Leadership/planning |
| **CHANGELOG.md** | Version history and release notes | Release tracking |
| **docs/GAMEPLAY_OVERVIEW.md** | Current system architecture | Developers |
| **space_invaders_spec.md** | Original cabinet spec | Everyone |
| **QUICK_START.md** | Quick setup guide | New developers |

---

## 🎓 Learning Resources

### To Understand Current Code
1. Read `docs/GAMEPLAY_OVERVIEW.md` - explains current systems
2. Look at `src/main.py` - see how everything fits
3. Check entity classes - understand game objects

### To Implement Spec Updates
1. Read `space_invaders_spec.md` - cabinet reference
2. Check related roadmap phase (Phase 4=accuracy, Phase 5=enhancements)
3. Look at existing enemy AI for patterns

### To Understand Architecture
1. Check `PROJECT.md` feature matrix - system dependencies
2. Look at test files - show expected behavior
3. Review docstrings in code

---

## 📞 Quick Reference

### Game Files to Modify for Different Features
- **Audio/SFX:** `src/utils/audio_manager.py`
- **Scoring:** `src/main.py` (update() method)
- **Player Behavior:** `src/entities/player.py`
- **Enemy Behavior:** `src/entities/alien.py`
- **Menu/UI:** `src/ui/menu.py`
- **Game States:** `src/systems/game_state_manager.py`
- **Configuration:** `src/config.py`, `src/constants.py`

### Common Commands
```bash
# Play game
python -m src.main

# Run all tests
pytest tests/ -v

# Run specific test suite
pytest tests/unit/test_quick_wins.py -v

# Check code coverage
pytest tests/ --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html

# Git workflow
git status
git add <files>
git commit -m "feat: description"
git push origin feature-branch
```

---

## 🎯 Success Metrics

### Phase 3 (State Machine & Menu)
- ✅ Game starts in menu state
- ✅ All state transitions working
- ✅ Tests passing (12/12+)
- ✅ No performance regression

### Phase 4 (Cabinet Accuracy)
- ✅ Attract mode loop
- ✅ Score advance table
- ✅ Credit/start flow
- ✅ Tests passing (20/20+)

### Phase 5 (Polish & Release)
- ✅ 60%+ code coverage
- ✅ Consistent 60 FPS performance
- ✅ Pip package available
- ✅ Release notes published

---

## 📝 Notes

### Why This Structure?
- **Single hub (PROJECT.md)** instead of scattered docs
- **Clear status** - what's done, what's next, what's planned
- **Priorities** - easy to see what to work on next
- **Dependencies** - understand feature order
- **Progress tracking** - see milestones and dates

### Keeping This Updated
- Update status when phase completes
- Move completed items from "Next Actions" to "Completed"
- Add new milestones as they're identified
- Keep git log and CHANGELOG in sync

---

**Current Phase:** 3 (Foundation Systems) - Ready to Start  
**Next Milestone:** Game State Machine (Est. Nov 24, 2025)  
**Questions?** Check docs/ folder or review git history for decisions
