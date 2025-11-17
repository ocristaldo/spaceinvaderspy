```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
- **NEW: Audio System** - Complete audio management with mute by default
  - Add: `AudioManager` class for handling SFX and background music with volume control
  - Add: Audio toggle with 'A' key (muted by default)
  - Add: Visual indicator showing audio status on HUD (green=ON, red=OFF)
- **NEW: High Score Persistence**
  - Add: `HighScoreManager` class for tracking and persisting high scores to JSON
  - Add: High score display in HUD and game over screen
  - Add: "NEW HIGH SCORE!" alert on game over screen (shown in green)
  - Add: Top 10 scores tracking and storage
- **NEW: Extra Lives Milestones**
  - Add: First extra life at 20,000 points
  - Add: Additional extra lives every 70,000 points thereafter
  - Add: Audio cue when extra life is earned
  - Add: Proper lives tracking and display updates
- Enhancement: Enhanced HUD display with score, high score, lives, and audio status
- Enhancement: Better game over screen showing final score, high score, and new high score indicator

## [Previous]
- Fix: Robust bomb-vs-player collision handling to avoid missed hits in tests
- Add: `workon.sh` helper to create/activate venv, install deps, and run tests
- Add: `QUICK_START.md` with macOS quick-start and adaptation notes
- Add: Unit test for bomb/player collision (`tests/unit/test_bomb_collision.py`)
- Add: GitHub Actions CI workflow (`.github/workflows/ci.yml`)
 - Add: Test coverage collection in CI and coverage report artifact

```
