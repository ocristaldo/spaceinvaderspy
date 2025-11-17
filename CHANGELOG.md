# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
- Fix: Robust bomb-vs-player collision handling to avoid missed hits in tests
- Add: `workon.sh` helper to create/activate venv, install deps, and run tests
- Add: `QUICK_START.md` with macOS quick-start and adaptation notes
- Add: Unit test for bomb/player collision (`tests/unit/test_bomb_collision.py`)
- Add: GitHub Actions CI workflow (`.github/workflows/ci.yml`)
 - Add: Test coverage collection in CI and coverage report artifact
