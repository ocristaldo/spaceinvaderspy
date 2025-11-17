# 👾 Space Invaders Python Clone

A work-in-progress recreation of the classic Space Invaders arcade game built with Python and Pygame, guided directly by the design notes in `docs/space_invaders_spec.md`. We keep the original sprites/feel while layering quality-of-life features for modern platforms.

## 🎯 Project Status

**Current:** Phase 2 Complete ✅ | **Next:** Phase 3 (Game States + Menu)  
**For full details, see [docs/PROJECT.md](docs/PROJECT.md) or [docs/STATUS.md](docs/STATUS.md)**

### Quick Stats
- ✅ Core game playable
- ✅ Audio system (muted by default)
- ✅ High score persistence
- ✅ Extra lives milestones
- ✅ 10/10 tests passing

## 🎮 Current Features

### Core Gameplay (today)
- Classic Space Invaders loop: marching formations, incremental speed-ups
- Multi-wave progression with a visible level counter (aliens respawn faster each wave)
- Configurable logical playfield scale (`SPACEINVADERS_SCALE`, default 2×) with automatic letterboxing so you can resize or zoom to taste
- Player ship controls (left/right movement, authentic single-shot firing — raise the limit with `SPACEINVADERS_PLAYER_SHOTS` if you prefer modern pacing)
- Destructible bunkers for defense (now spaced farther from the cannon to avoid overlap)
- UFO bonus enemy with random point values and floating score popups
- Player shots can intercept alien bombs mid-air (straight out of the arcade feel)
- Animated attract/demo sequence (the classic S+2-style screen) with aliens dropping into formation before returning to the menu
- In-game menu includes a "Controls" overlay that lists every shortcut (including sprite viewer combos) and persists audio/demo settings
- Scoring system with per-alien values and 3-life structure

### Advanced Features
- **Sprite Sheet System**: Authentic arcade sprites loaded from JSON coordinate files
- **Sprite Viewer**: Interactive testing mode
  - Key combinations: S+1 (Arcade atlas), S+2 (start-screen preview), S+3 (wave-ready preview), S+4 (late-wave preview)
  - Pagination with arrow keys (← →)
  - Detailed sprite information display
  - Platform switching without game restart
- **Animated Sprites**: Alien animation with frame switching
- **Comprehensive Logging**: Debug and info logging throughout the game
- **Design Docs**: `docs/space_invaders_spec.md` (original gameplay blueprint) and `docs/GAMEPLAY_OVERVIEW.md` (current systems)

## 📚 Gameplay Vision
- `docs/space_invaders_spec.md` captures the original Space Invaders cabinet behavior (attract mode, scoring table, gameplay pacing) and is now our primary reference for future improvements.
- `docs/GAMEPLAY_OVERVIEW.md` explains how the current Space Invaders implementation works, making it easier to track deltas from the spec.
- `docs/SPRITES.md` catalogs every sprite in the JSON atlas and how the code uses it (handy when updating bunkers/FX).
- `docs/space_invaders_start_screen.png` (and other reference PNGs in `docs/`) provide the visual targets for layout, colors, and HUD placement. Use them when adjusting positions or art.
- Roadmap items below link directly back to these documents so design and implementation stay aligned.

## 📋 Requirements

- Python 3.8+
- Pygame 2.0+

## 🛠 Installation & Setup

### Windows
1. Install Python 3.8+ from [python.org](https://www.python.org/downloads/)
2. Install Pygame:
```powershell
py -m pip install pygame
```
3. Clone the repository:
```powershell
git clone https://github.com/yourusername/spaceinvaderspy.git
cd spaceinvaderspy
```
4. Install other dependencies:
```powershell
py -m pip install -r requirements.txt
```

### macOS
1. Install Python using Homebrew:
```bash
brew install python3
```
2. Install Pygame:
```bash
python3 -m pip install pygame
```
3. Clone the repository:
```bash
git clone https://github.com/yourusername/spaceinvaderspy.git
cd spaceinvaderspy
```
4. Install other dependencies:
```bash
python3 -m pip install -r requirements.txt
```

Quick start script (all platforms)
----------------------------------

Use `./spaceinvaders.sh` to handle the entire toolchain:

- `./spaceinvaders.sh` → create/activate `.venv` (if needed), install requirements once, launch the game.
- `./spaceinvaders.sh test` → ensure dependencies and run `pytest -q`.
- `./spaceinvaders.sh shell` → drop into an interactive shell with the managed virtualenv activated.
- Pass `SPACEINVADERS_WINDOW_SCALE=1.5 ./spaceinvaders.sh` to pick the initial window size (the game now renders to a logical playfield and scales/letterboxes to any window size you drag it to).

The script automatically skips creation/installation when you're already inside any virtualenv, so you can opt into a custom environment without extra prompts.

Coverage
--------

This repository collects test coverage during CI and provides a coverage report artifact. To run coverage locally:

```bash
# from project root
pytest --cov=src --cov-report=term --cov-report=xml
```

You can view the CI workflow badge here:

![CI](https://github.com/ocristaldo/spaceinvaderspy/actions/workflows/ci.yml/badge.svg)

### Linux (Ubuntu/Debian)
1. Install Python and required system packages:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
```
2. Install Pygame:
```bash
python3 -m pip install pygame
```
3. Clone the repository:
```bash
git clone https://github.com/yourusername/spaceinvaderspy.git
cd spaceinvaderspy
```
4. Install other dependencies:
```bash
python3 -m pip install -r requirements.txt
```

### Raspberry Pi
1. Update system and install dependencies:
```bash
sudo apt update
sudo apt install python3-pygame
```
2. Clone the repository:
```bash
git clone https://github.com/yourusername/spaceinvaderspy.git
cd spaceinvaderspy
```
3. Install other dependencies:
```bash
python3 -m pip install -r requirements.txt
```

## 🎮 Running the Game

After installation, the quickest way to play is:

```bash
./spaceinvaders.sh
```

This ensures the virtualenv exists, installs requirements if needed, and launches `python -m src.main`.  
Prefer manual commands? Use the per-platform invocations below:

### Windows
```powershell
py -m src.main
```

### macOS/Linux/Raspberry Pi
```bash
python3 -m src.main
```

## 🧪 Running Tests

Quick path:

```bash
./spaceinvaders.sh test
```

Manual commands:

### Windows
```powershell
py -m pytest -v
```

### macOS/Linux/Raspberry Pi
```bash
python3 -m pytest -v
```

Tip for headless environments (CI): set the SDL drivers to 'dummy' so pygame can initialize without a real display:

```bash
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python3 -m pytest -v
```

## ⚙️ Configuration Tweaks

You can tweak the arcade feel without editing code by setting environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `SPACEINVADERS_SCALE` | `2.0` | Logical playfield scale factor (2× = 448×512). Set `3.0` for the roomy 672×768 view or any value between 1–4. |
| `SPACEINVADERS_WINDOW_SCALE` | `1.0` | Initial OS window scaling multiplier (the window still resizes freely). |
| `SPACEINVADERS_PLAYER_SHOTS` | `1` | Maximum number of player bullets allowed on-screen. Raise to modernize the pacing while keeping the default authentic. |

## 📁 Project Structure
```
spaceinvaderspy/
├── src/                    # Source code
│   ├── entities/          # Game entities (Player, Alien, Bullet, etc.)
│   ├── utils/             # Utility modules (SpriteSheet, SpriteViewer, Logger)
│   ├── core/              # Core game systems
│   ├── states/            # Game states
│   ├── main.py            # Main game entry point
│   ├── config.py          # Game configuration
│   └── constants.py       # Game constants
├── assets/                # Game assets
│   └── images/           # Sprite images and JSON coordinate files
│       ├── SpaceInvaders.png           # Main sprite sheet
│       ├── SpaceInvaders.arcade.json   # Arcade sprite coordinates
│       ├── SpaceInvaders.atari.json    # Atari 2600 coordinates
│       ├── SpaceInvaders.deluxe.json   # Deluxe coordinates
│       └── SpaceInvaders.intellivision.json # Intellivision coordinates
├── tests/                 # Unit and integration tests
├── docs/                  # Documentation
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🤝 Contributing

This is a work in progress and help is welcome! Some areas that need attention:

- Bug fixes and code optimization
- Additional game features (sound effects, high score system)
- Improved graphics and animations
- Documentation improvements
- Test coverage
- Performance optimization

To contribute:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 🎯 Game Controls

### Basic Controls
- **Left Arrow/Right Arrow**: Move player ship
- **Space**: Fire bullet (default: one bullet at a time)
- **Space (after losing a life)**: Respawn and resume play when prompted
- **D (from Options)**: Replay the intro demo animation
- **I (from Options)**: Toggle intro demo autoplay (persists to disk)
- **R**: Restart game (when game over) or exit sprite viewer
- **Q**: Quit game

### Sprite Viewer Controls
- **S+1**: View Arcade sprites
- **S+2**: Render the “Start Screen” mock scene (title, score table, credit prompt)
- **S+3**: Render the “Wave Ready” mock scene (player + bunkers + alien formation)
- **S+4**: Render the “Late-Game” mock scene (aliens near bunkers, bombs mid-air)
- **← →**: Navigate between sprite pages
- **R**: Return to game from sprite viewer

## 🐛 Known Issues

- Sprite viewer navigation has been optimized with debouncing
- Some sprite coordinate files may need platform-specific adjustments
- Please report any bugs in the Issues section

## 📝 License

This is an unofficial fan project created for educational purposes only. It includes no original assets or code from the 1978 release and is not endorsed by the trademark holders.

## 🙏 Acknowledgments

- Original Space Invaders game by Taito
- Pygame community
- All contributors and testers

## ✉️ Contact

- Report issues on GitHub
- [Your contact information]

## 🔜 Roadmap

### Completed ✅
- ✅ Space Invaders core loop (player, aliens, bunkers, UFO, bombs)
- ✅ Sprite sheet system with JSON coordinates + multi-platform atlases
- ✅ Interactive sprite viewer with pagination
- ✅ Comprehensive logging system and gameplay documentation
- ✅ Animated alien sprites + scaling fixes

### In Progress 🚧
- 🚧 Map current systems to Space Invaders cabinet spec (`docs/space_invaders_spec.md`)
- 🚧 Prototype enemy swoop/dive behaviors using existing sprite assets
- 🚧 Design credit/attract flow + HUD updates (scores, stage badges)
- 🚧 Expand docs with migration steps (GAMEPLAY_OVERVIEW vs detailed gameplay)

### Planned 📋
- 📋 Challenge stages & accuracy bonus tallies
- 📋 Tractor-beam capture + dual-ship firing mode
- 📋 Enemy bullet patterns & varied formations (butterflies, boss ships)
- 📋 Sound effects, music, and attract-mode cues
- 📋 Credit system with 1P/2P alternating-play support
- 📋 Persistent high scores + bonus-life thresholds (20k/70k etc.)
