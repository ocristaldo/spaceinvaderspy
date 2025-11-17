# 🤝 Contributing to Space Invaders Py

Thanks for your interest in contributing! This document will help you get started quickly.

---

## 📌 Before You Start

**New to the project?**
1. Read [README.md](README.md) - Overview
2. Read [STATUS.md](STATUS.md) - Current status
3. Read [PROJECT.md](PROJECT.md) - Full details
4. Play the game: `python -m src.main`

**Know what you want to work on?**
- Jump to [Development Workflow](#-development-workflow) below

---

## 🎯 What to Work On

### Phase 3 (Next - Ready Now!)
Pick one of these to get started:

- **Game State Machine** - Replace string states with proper enum
  - Files: `src/systems/game_state_manager.py`
  - Complexity: Medium
  - Tests needed: 5+
  
- **Menu UI** - Create main menu and select screen
  - Files: `src/ui/menu.py`
  - Complexity: Medium
  - Tests needed: 3+

- **Level Progression** - Multi-wave levels with difficulty scaling
  - Files: `src/main.py`, `src/systems/`
  - Complexity: Medium
  - Tests needed: 5+

See [PROJECT.md](PROJECT.md) for full feature matrix and dependencies.

---

## 🔧 Development Workflow

### 1. Setup
```bash
# Clone repo
git clone https://github.com/yourusername/spaceinvaderspy.git
cd spaceinvaderspy

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Create Feature Branch
```bash
git checkout -b feature/state-machine
# or
git checkout -b bugfix/collision-issue
```

### 3. Write Tests First (TDD)
```bash
# Create test file
touch tests/unit/test_state_machine.py

# Write tests for expected behavior
# Example structure in tests/unit/test_quick_wins.py
```

### 4. Implement Feature
```bash
# Create implementation file
touch src/systems/game_state_manager.py

# Write code to pass tests
```

### 5. Run Tests
```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/unit/test_state_machine.py -v

# Check coverage
pytest tests/ --cov=src --cov-report=term
```

### 6. Commit
```bash
git add .
git commit -m "feat: Add game state machine

- Implement state enum (MENU, PLAYING, PAUSED, GAME_OVER)
- Add state transition logic
- Add comprehensive tests"
```

### 7. Push & Create PR
```bash
git push origin feature/state-machine
# Create PR on GitHub
```

---

## ✍️ Code Standards

### Naming
- Classes: `PascalCase` (e.g., `AudioManager`)
- Functions/methods: `snake_case` (e.g., `check_extra_lives`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `LIVES_NUMBER`)
- Private: prefix with `_` (e.g., `_update_speed`)

### Documentation
```python
class GameStateManager:
    """Manages game state transitions and current state.
    
    States: MENU, PLAYING, PAUSED, GAME_OVER
    """
    
    def __init__(self):
        """Initialize with MENU state."""
        self.state = GameState.MENU
    
    def transition(self, new_state: GameState) -> bool:
        """Transition to new state if valid.
        
        Args:
            new_state: Target game state
            
        Returns:
            True if transition successful, False otherwise
        """
        pass
```

### Type Hints
```python
# Good
def update_score(self, score: int) -> None:
    """Update game score."""
    self.score = score

# Also fine for simple code
def get_score(self):
    """Get current score."""
    return self.score
```

### Testing
```python
# Test file naming: test_<module>.py
# Test class naming: Test<Feature>
# Test method naming: test_<behavior>

class TestGameStateManager:
    """Tests for GameStateManager."""
    
    def test_initial_state_is_menu(self):
        """Initial state should be MENU."""
        manager = GameStateManager()
        assert manager.state == GameState.MENU
    
    def test_transition_to_playing(self):
        """Should transition from MENU to PLAYING."""
        manager = GameStateManager()
        success = manager.transition(GameState.PLAYING)
        assert success
        assert manager.state == GameState.PLAYING
```

---

## 📊 Review Checklist

Before submitting a PR, ensure:

- [ ] **Code works** - Feature functions as intended
- [ ] **Tests pass** - All tests passing locally
- [ ] **Tests added** - New tests for new code
- [ ] **Coverage maintained** - Don't reduce coverage
- [ ] **Documentation updated** - Docstrings, comments where needed
- [ ] **No breaking changes** - Existing code still works
- [ ] **Git history clean** - Logical, well-formatted commits
- [ ] **Follows standards** - Naming, style, conventions

---

## 🐛 Bug Reports

Found a bug? Create an issue with:

1. **Clear title** - What's broken?
2. **Reproduction steps** - How to reproduce it
3. **Expected behavior** - What should happen
4. **Actual behavior** - What actually happens
5. **Environment** - Python version, OS, etc.

Example:
```
Title: Aliens not animating correctly

Steps to reproduce:
1. Start game
2. Wait 10 seconds
3. Observe aliens

Expected: Aliens should animate every ~0.5 seconds
Actual: Aliens stop animating after 30 seconds

Environment: Python 3.11, macOS Ventura
```

---

## 💡 Feature Requests

Have an idea? Create an issue with:

1. **Clear description** - What's the feature?
2. **Why it matters** - How does it improve the game?
3. **Acceptance criteria** - How do we know it's done?

Example:
```
Title: Add difficulty levels

Description:
Add easy/normal/hard difficulty selection in menu.
Each difficulty adjusts: alien speed, bomb frequency, UFO interval

Acceptance Criteria:
- Menu has difficulty selector
- Easy: 20% slower aliens, fewer bombs
- Normal: Current game speed (baseline)
- Hard: 20% faster aliens, more bombs
```

---

## 🎓 Learning Resources

### To Understand Current Code
1. **[PROJECT.md](PROJECT.md)** - Full system overview
2. **[docs/GAMEPLAY_OVERVIEW.md](docs/GAMEPLAY_OVERVIEW.md)** - Current architecture
3. **src/main.py** - Main game loop (start here)
4. **tests/** - Test files show expected behavior

### To Implement Galaga Features
1. **[docs/detailed_gameplay.md](docs/detailed_gameplay.md)** - Complete Galaga spec
2. **Look at existing enemies** - Pattern to follow
3. **Check related tests** - Understand expected behavior

### Pygame Docs
- [Pygame Docs](https://www.pygame.org/)
- [Pygame Collision Detection](https://www.pygame.org/docs/ref/sprite.html)

---

## 💬 Communication

- **Questions?** Open an issue with label `question`
- **Need feedback?** Create a draft PR
- **Stuck?** Comment in the issue you're working on
- **Want to discuss design?** Create an issue first

---

## 🚀 Tips for Successful PRs

1. **Start small** - Easier to review, less likely to conflict
2. **Reference issues** - Link to related issues in PR description
3. **Write descriptive commits** - Future you will thank you
4. **Test thoroughly** - Run tests locally before pushing
5. **Keep history clean** - Squash or rebase before final PR
6. **Engage with feedback** - Be responsive to reviews

---

## 📋 PR Template

When creating a PR, use this template:

```markdown
## What does this PR do?
Brief description of the feature or fix.

## Related Issue
Fixes #123 or Related to #456

## How to Test?
1. Start game with `python -m src.main`
2. Do X
3. Observe Y

## Checklist
- [ ] Tests passing locally
- [ ] New tests added
- [ ] Documentation updated
- [ ] No breaking changes
```

---

## ✨ Thank You!

Thank you for contributing! Your work helps make this project better for everyone. 🎉

Questions? Open an issue or check [PROJECT.md](PROJECT.md).
