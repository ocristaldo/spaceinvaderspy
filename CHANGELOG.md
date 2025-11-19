# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-11-19

### Added
- **2-Player Mode**: Complete alternating gameplay with independent game state persistence
- **Hit-Based Player Switching**: Players switch on every bomb hit, not just on death
- **Player Indicator**: Visual display of current player in 2P mode on the HUD
- **Debug Mode Script**: New `debug.sh` script for easy debug mode execution with full logging
- **Debug Logging**: Enhanced DEBUG mode environment variable support for troubleshooting

### Fixed
- **Critical Font Profile Bug**: Fixed invalid menu_large font profile in InitialsEntry - replaced with menu_body
- **High Score Display**: Corrected high score display formatting to show properly formatted text instead of object representations
- **High Score Input Handling**: Improved error handling and validation in InitialsEntry input processing
- **Continue Screen**: Fixed high score display text and credit count persistence on continue timeout
- **Continue Screen Mode Locking**: Corrected logic to lock players to same game mode on continue screen
- **Menu Navigation Tests**: Updated test cases to account for new menu structure (1-Player, 2-Player, High Scores, Controls, Options, Credits, Quit)
- **CI Test Failures**: Fixed 8 failing test cases that were incompatible with the new 2-player menu structure

### Changed
- Menu structure now splits "Start" into "1-Player" and "2-Player" options
- Improved InitialsEntry event handling to prevent pygame event consumption conflicts

### Technical
- All 85 unit and integration tests now passing (was 77/85)
- Comprehensive 2-player mode test coverage
- Enhanced documentation for debug mode usage

---

## [1.0.0] - Previous Release

See git history for details on version 1.0.0 and earlier releases.
