# Space Invaders - Refactoring & Code Quality Guide

**Purpose:** Document technical debt, refactoring opportunities, and cleanup tasks for v2.0 preparation.

**Target Audience:** Developers working on v2.0 and future maintenance.

---

## 📋 Executive Summary

The Space Invaders codebase is well-structured with good test coverage (71+ tests, 100% coverage). However, there are several areas of technical debt that should be addressed before v2.0 to establish a solid foundation:

| Category | Severity | Tasks | Est. Time |
|----------|----------|-------|-----------|
| Critical Bugs | 🔴 High | 3 | 30 min |
| Configuration | 🟡 Medium | 5 | 90 min |
| Code Organization | 🟡 Medium | 3 | 180 min |
| Documentation | 🟡 Medium | 4 | 120 min |
| **Total Phase 0** | - | **15** | **≈420 min (7 hrs)** |

---

## 🔴 CRITICAL BUGS (Fixed)

### CB-1: coverage.ini Syntax Error ✅ FIXED
**File:** `coverage.ini` (line 10)
**Issue:** Missing quotes in `if __name__` exclusion
```ini
# BEFORE (broken):
if __name__ == .__main__.:

# AFTER (fixed):
if __name__ == "__main__":
```
**Impact:** Coverage reports may fail during CI
**Status:** ✅ Fixed

---

### CB-2: Duplicate Line in menu.py ✅ FIXED
**File:** `src/ui/menu.py` (line 55)
**Issue:** `self.options_music_on = False` declared twice
```python
# BEFORE:
self.options_music_on = False
self.options_music_on = False

# AFTER:
self.options_music_on = False
```
**Impact:** Confusing code, suggests incomplete refactoring
**Status:** ✅ Fixed

---

### CB-3: .gitignore Conflicts with Tracked Files ⚠️ PENDING
**File:** `.gitignore` (lines 2, 33-34)
**Issue:** Wildcard patterns conflict with tracked files:
- Line 2: `settings.json` (but needs defaults tracked)
- Line 33: `*.ini` ignores `pytest.ini` (which is tracked)
- Line 34: `*.cfg` may conflict with config patterns

**Solution:**
```bash
# BEFORE:
*.ini
*.cfg
settings.json

# AFTER:
pytest.ini  # Keep, explicitly tracked
setup.cfg   # Keep, explicitly tracked
# Remove *.ini and *.cfg wildcards, use specific patterns
settings.json  # User settings, not tracked
settings.default.json  # Default template, tracked
```

**Impact:** Cleaner version control, prevents user configs in repo
**Status:** ⏳ Pending

---

## 🟡 CONFIGURATION INFRASTRUCTURE

### CF-1: Create pyproject.toml ⏳ PENDING
**Goal:** Modern Python packaging standard, consolidate tool configs

**Current State:**
- pytest.ini (scattered config)
- coverage.ini (separate file)
- setup.cfg equivalent missing
- No central source of truth

**Target State:**
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "spaceinvaderspy"
version = "2.0.0"
description = "A faithful Python recreation of Space Invaders"
requires-python = ">=3.8"
dependencies = ["pygame>=2.0"]

[project.optional-dependencies]
dev = ["pytest>=7.0", "pytest-cov", "ruff"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src --cov-report=xml"

[tool.coverage.run]
source = ["src"]
omit = ["*/__init__.py"]

[tool.ruff]
line-length = 100
```

**Impact:** Better packaging, single config source
**Effort:** 30 minutes
**Priority:** HIGH

---

### CF-2: Create settings.default.json Template ⏳ PENDING
**Goal:** Tracked default settings, user can override

**Current State:**
- `settings.json` in .gitignore (user-specific)
- Game creates default on first run
- No version control of defaults
- Users can't see what settings are available

**Target State:**
```json
{
  "version": "2.0.0",
  "audio": {
    "sfx_enabled": true,
    "music_enabled": false,
    "master_volume": 1.0,
    "sfx_volume": 0.8,
    "music_volume": 0.6
  },
  "display": {
    "tint_enabled": false,
    "scale": 2
  },
  "gameplay": {
    "intro_demo_enabled": true,
    "difficulty": "normal",
    "game_mode": "arcade"
  }
}
```

**Files:**
- Create: `settings.default.json` (tracked)
- Keep: `settings.json` (gitignored, user-specific)
- Update: `.gitignore` to track defaults

**Impact:** Better defaults, version control of settings schema
**Effort:** 15 minutes
**Priority:** HIGH

---

### CF-3: Implement Settings Schema Validation ⏳ PENDING
**Goal:** Validate settings.json structure, handle corruption

**Current State:**
- Settings loaded with basic dict access
- No validation of structure
- Corrupted JSON crashes game

**Target State:**
```python
# src/utils/settings_manager.py
from dataclasses import dataclass

@dataclass
class AudioSettings:
    sfx_enabled: bool = True
    music_enabled: bool = False
    master_volume: float = 1.0

@dataclass
class GameSettings:
    audio: AudioSettings
    display: dict
    gameplay: dict

    @staticmethod
    def from_file(path: str) -> 'GameSettings':
        """Load and validate settings, fallback to defaults on error."""
        try:
            with open(path) as f:
                data = json.load(f)
            return GameSettings(**data)
        except (json.JSONDecodeError, KeyError, FileNotFoundError):
            logging.warning(f"Settings corrupted/missing at {path}, using defaults")
            return GameSettings()
```

**Impact:** Robust error handling, prevents crashes
**Effort:** 60 minutes
**Priority:** HIGH

---

### CF-4: Update .vscode Settings ⏳ PENDING
**File:** `.vscode/settings.json`
**Issue:** Configured for unittest, project uses pytest

**Current:**
```json
{
  "python.testing.unittestArgs": ["-p", "test_*.py"]
}
```

**Target:**
```json
{
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests"],
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true
  },
  "ruff.lineLength": 100
}
```

**Impact:** Better IDE integration for developers
**Effort:** 10 minutes
**Priority:** LOW

---

### CF-5: Create setup.py for Pip Install Support ⏳ PENDING
**Goal:** Enable `pip install -e .` for development

**Current State:**
- Game must be run from repo root
- Cannot install as package
- No distribution support

**Target:**
```python
# setup.py
from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name="spaceinvaderspy",
    version="2.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["pygame>=2.0"],
    python_requires=">=3.8",
)
```

**Then also add to pyproject.toml build-system section**

**Impact:** Professional packaging, easier distribution
**Effort:** 20 minutes
**Priority:** MEDIUM

---

## 🔧 CODE ORGANIZATION

### CO-1: Audit and Integrate src/core/ Modules ⏳ PENDING
**Goal:** Clarify purpose of unused core modules

**Current State:**
```
src/core/
├── collision_manager.py
├── game_engine.py
└── input_handler.py
```

**Issue:** These modules exist but main.py likely reimplements functionality

**Action Plan:**
1. **Review each file:**
   ```bash
   grep -r "from src.core" src/  # Check if imported
   grep -l "collision_manager\|game_engine\|input_handler" src/main.py
   ```

2. **Decision for each:**
   - **Option A: Integrate** - Use these modules properly in main.py
   - **Option B: Remove** - Delete if truly unused, simplify codebase
   - **Option C: Document** - Explain why they're placeholders for v2.0

3. **Example refactoring (if integrate):**
   ```python
   # Before: Everything in main.py
   class Game:
       def update(self):
           self.handle_collisions()  # 100 lines of code

   # After: Delegated
   from src.core.collision_manager import CollisionManager

   class Game:
       def __init__(self):
           self.collision_manager = CollisionManager()
       def update(self):
           self.collision_manager.handle(self.groups)
   ```

**Impact:** Cleaner architecture, better separation of concerns
**Effort:** 120 minutes (depends on decision)
**Priority:** HIGH

---

### CO-2: Add Missing Type Hints ⏳ PENDING
**Goal:** Complete type hint coverage for better IDE support and documentation

**Current State:**
- game_state_manager.py: ✓ Good coverage
- main.py: ⚠️ Partial (some functions untyped)
- entities/*.py: ⚠️ Minimal hints
- ui/*.py: ⚠️ Mixed coverage

**Targets:**
```python
# Before:
def update():
    for alien in self.aliens:
        alien.move()

# After:
def update(self) -> None:
    for alien: Alien in self.aliens:
        alien.move()

def create_aliens(self) -> List[Alien]:
    return [Alien(...) for _ in range(55)]
```

**Files to Update:**
- `src/main.py` - Game class methods
- `src/entities/player.py` - All methods
- `src/entities/alien.py` - All methods
- `src/entities/bullet.py` - All methods
- `src/ui/menu.py` - Methods lacking hints

**Impact:** Better IDE autocomplete, easier debugging, self-documenting code
**Effort:** 90 minutes
**Priority:** MEDIUM

---

### CO-3: Extract Magic Numbers to Named Constants ⏳ PENDING
**Goal:** Replace hardcoded values with descriptive constants

**Current Issues:**
```python
# From various files - unclear meaning
x = 80  # What is this?
if health > 4:  # Why 4?
speed = 0.4  # Why this multiplier?
```

**Solution:** Create `src/constants.py` extensions:
```python
# src/constants.py (enhance existing)

# Collision/Positioning
BUNKER_DISTANCE_FROM_PLAYER = 80  # pixels above player
ALIEN_FORMATION_SPACING_X = 20  # pixels between aliens
ALIEN_FORMATION_SPACING_Y = 16  # pixels between rows

# Game Physics
BASE_ALIEN_SPEED = 0.4  # units per frame
MAX_ALIEN_SPEED = 1.6
BOMB_SPAWN_PROBABILITY = 0.01
UFO_SPAWN_INTERVAL = 15  # seconds

# Bunker System
BUNKER_HEALTH_STAGES = 4
BUNKER_TINT_BASE = 80
BUNKER_TINT_RANGE = 175

# Scoring
POINTS_PER_ALIEN_TYPE = {
    "squid": 30,
    "crab": 20,
    "octopus": 10,
    "ufo": lambda: choice([50, 100, 150, 300]),
}

# UI
LIVES_DISPLAY_LIMIT = 5
CREDIT_DISPLAY_WIDTH = 2  # digits
SCORE_DISPLAY_WIDTH = 8
```

**Files to Update:**
- `src/main.py` - Game mechanics
- `src/entities/bunker.py` - Health/tint calculations
- `src/ui/*.py` - Layout constants
- `src/core/collision_manager.py` - Thresholds

**Impact:** Code readability, easier tuning, documentation
**Effort:** 60 minutes
**Priority:** MEDIUM

---

## 📚 DOCUMENTATION IMPROVEMENTS

### DO-1: Update README.md ⏳ PENDING
**File:** `README.md`

**Issues:**
- Line 227: References non-existent `src/states/` directory
- Line 302: Placeholder text "[Your contact information]"
- v1.1 planning outdated (README says v1.1 next, but v2.0 planned)

**Tasks:**
1. Remove line 227 reference or update to correct path
2. Remove/replace placeholder on line 302
3. Update "Next" version from v1.1 to v2.0
4. Add v2.0 preview section with new features

**Impact:** Accurate documentation, first impression
**Effort:** 20 minutes
**Priority:** LOW

---

### DO-2: Document Release Process ⏳ PENDING
**Create:** `docs/RELEASE_PROCESS.md`

**Content:**
```markdown
# Release Process

## Before Release
1. Update version in src/__init__.py
2. Update version in docs/V2_0_ROADMAP.md
3. Update RELEASE_NOTES.md
4. Run full test suite: pytest
5. Run coverage check: pytest --cov
6. Manual QA on Windows/macOS/Linux
7. Performance benchmarking

## Tagging
1. Create git tag: git tag -a v2.0.0 -m "Release v2.0.0"
2. Push tag: git push origin v2.0.0

## CI/CD
1. GitHub Actions automatically:
   - Runs tests
   - Builds artifacts
   - Creates GitHub release
   - Uploads to artifact storage

## Post-Release
1. Announce on GitHub discussions
2. Monitor for immediate bug reports
3. Plan v2.1 based on feedback
```

**Impact:** Clear process, consistent releases
**Effort:** 30 minutes
**Priority:** MEDIUM

---

### DO-3: Create Architecture Decision Records (ADRs) ⏳ PENDING
**Create:** `docs/adr/`

**ADRs Needed:**
1. **ADR-001: Why separate core modules?** - Explain intended vs current design
2. **ADR-002: Color scheme vs level themes** - Architecture for v2.0 themes
3. **ADR-003: Settings persistence strategy** - defaults vs user overrides
4. **ADR-004: Game state machine design** - Why not use library?

**Format:**
```markdown
# ADR-001: Core Module Architecture

## Status
Proposed/Accepted/Deprecated

## Context
[What decisions we're making and why]

## Decision
[What we decided to do]

## Consequences
[Impacts and tradeoffs]

## Related
[Links to other ADRs/docs]
```

**Impact:** Future-proof design documentation, easier onboarding
**Effort:** 90 minutes
**Priority:** LOW

---

### DO-4: Update CONFIGURATION.md ⏳ PENDING
**File:** `docs/CONFIGURATION.md`

**Issues:**
- References deleted documentation
- Incomplete test section (line 120 cuts off)
- Should consolidate all config sources

**Tasks:**
1. Fix incomplete line 120
2. Remove references to CLEANUP_SUMMARY.md, DOCS_GUIDE.md
3. Add section: "Configuration Sources of Truth"
   - config.py (constants)
   - settings.default.json (user preferences template)
   - settings.json (user overrides, gitignored)
   - Environment variables (overrides)
   - Command-line args (highest priority)

**Impact:** Clear configuration documentation
**Effort:** 30 minutes
**Priority:** MEDIUM

---

## 🧪 TEST STRUCTURE ENHANCEMENTS

### TS-1: Expand conftest.py Fixtures ⏳ PENDING
**File:** `tests/conftest.py`

**Current Limitations:**
- Only basic pygame init and font cache
- No fixtures for common test scenarios
- Tests recreate objects repeatedly

**New Fixtures Needed:**
```python
@pytest.fixture
def mock_surface():
    """224x256 logical surface for testing."""
    return pygame.Surface((224, 256))

@pytest.fixture
def game_state():
    """Pre-configured GameStateManager."""
    manager = GameStateManager()
    return manager

@pytest.fixture
def test_player(mock_surface):
    """Player object for testing."""
    return Player(mock_surface, 100, 200)

@pytest.fixture
def test_aliens(mock_surface):
    """Full alien formation for testing."""
    return create_alien_formation(mock_surface)

@pytest.fixture
def test_bunkers(mock_surface):
    """4 bunkers in standard positions."""
    return create_bunkers(mock_surface)
```

**Impact:** Cleaner tests, less duplication, faster test development
**Effort:** 45 minutes
**Priority:** MEDIUM

---

### TS-2: Add Asset Validation Tests ⏳ PENDING
**Create:** `tests/test_assets.py`

**Tests Needed:**
```python
def test_all_sprites_exist_in_atlases():
    """Verify all referenced sprites exist in JSON atlases."""

def test_sprite_coordinates_within_bounds():
    """Verify sprite coordinates don't exceed image dimensions."""

def test_audio_files_exist():
    """Verify all sound files referenced exist."""

def test_font_files_loadable():
    """Verify font files can be loaded successfully."""
```

**Impact:** Prevent asset loading failures, catch regressions
**Effort:** 45 minutes
**Priority:** MEDIUM

---

## 📊 SUMMARY TABLE

| Task | Priority | Effort | Impact | Status |
|------|----------|--------|--------|--------|
| Fix coverage.ini | 🔴 CRITICAL | 5 min | Fixes CI | ✅ Done |
| Remove duplicate menu.py | 🔴 CRITICAL | 2 min | Code quality | ✅ Done |
| .gitignore patterns | 🔴 CRITICAL | 10 min | Version control | ⏳ TODO |
| pyproject.toml | 🟡 HIGH | 30 min | Packaging | ⏳ TODO |
| settings.default.json | 🟡 HIGH | 15 min | Configuration | ⏳ TODO |
| Settings validation | 🟡 HIGH | 60 min | Robustness | ⏳ TODO |
| Audit src/core/ | 🟡 HIGH | 120 min | Architecture | ⏳ TODO |
| Type hints | 🟡 MEDIUM | 90 min | Quality | ⏳ TODO |
| Magic numbers | 🟡 MEDIUM | 60 min | Readability | ⏳ TODO |
| .vscode settings | 🟡 MEDIUM | 10 min | DX | ⏳ TODO |
| setup.py | 🟡 MEDIUM | 20 min | Distribution | ⏳ TODO |
| Release process doc | 🟡 MEDIUM | 30 min | Process | ⏳ TODO |
| Test fixtures | 🟡 MEDIUM | 45 min | Testing | ⏳ TODO |
| Asset validation | 🟡 MEDIUM | 45 min | Testing | ⏳ TODO |
| README updates | 🟠 LOW | 20 min | Documentation | ⏳ TODO |
| ADRs | 🟠 LOW | 90 min | Documentation | ⏳ TODO |
| CONFIGURATION.md | 🟠 LOW | 30 min | Documentation | ⏳ TODO |

---

## 🚀 Recommended Execution Order

### Week 1: Critical Fixes & Configuration
1. ✅ Fix coverage.ini syntax (DONE)
2. ✅ Remove duplicate menu.py line (DONE)
3. Fix .gitignore patterns
4. Create pyproject.toml
5. Create settings.default.json
6. Implement settings validation

### Week 2: Code Quality
1. Audit src/core/ modules
2. Add missing type hints
3. Extract magic numbers to constants
4. Update .vscode settings
5. Create setup.py

### Week 3: Testing & Documentation
1. Expand conftest.py fixtures
2. Add asset validation tests
3. Update README.md
4. Document release process
5. Create ADRs (optional, low priority)

### After Phase 0 Complete
→ Begin v2.0 implementation (Phases 1-8)

---

## 📝 Related Documentation

- See `docs/V2_0_ROADMAP.md` for v2.0 feature planning
- See `docs/PROJECT.md` for project overview
- See `CONTRIBUTING.md` for development workflow

