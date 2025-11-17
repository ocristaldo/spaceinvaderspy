# 👾 Space Invaders Python Clone (Galaga-inspired Evolution)

A work-in-progress recreation of the classic Space Invaders arcade game built with Python and Pygame, now marching toward Galaga-style wave choreography and challenge stages. We keep the original sprites/feel while extending gameplay to match the deep dive documented in `docs/detailed_gameplay.md`.

## � Project Status

**Current:** Phase 2 Complete ✅ | **Next:** Phase 3 (Game States + Menu)  
**For full details, see [PROJECT.md](PROJECT.md) or [STATUS.md](STATUS.md)**

### Quick Stats
- ✅ Core game playable
- ✅ Audio system (muted by default)
- ✅ High score persistence
- ✅ Extra lives milestones
- ✅ 10/10 tests passing

## 🎮 Current Features

### Core Gameplay (today)
- Classic Space Invaders loop: marching formations, incremental speed-ups
- Player ship controls (left/right movement, single-shot firing)
- Destructible bunkers for defense
- UFO bonus enemy with random point values
- Scoring system with per-alien values and 3-life structure

### Galaga-inspired Goals (in progress)
- Enemy entry swoops + dive-bomb behavior pulled from `docs/detailed_gameplay.md`
- Challenge / rally stages that reward accuracy streaks
- Tractor-beam capture mechanic and dual-ship power-up
- Credit/attract-mode flow with coin/1P/2P inputs
- Bonus-life thresholds and rank indicators on HUD

### Advanced Features
- **Sprite Sheet System**: Authentic arcade sprites loaded from JSON coordinate files
- **Multi-Platform Sprite Support**: 
  - Arcade (original)
  - Atari 2600
  - Deluxe edition
  - Intellivision
- **Sprite Viewer**: Interactive testing mode to view all sprites
  - Key combinations: S+1 (Arcade), S+2 (Atari), S+3 (Deluxe), S+4 (Intellivision)
  - Pagination with arrow keys (← →)
  - Detailed sprite information display
  - Platform switching without game restart
- **Animated Sprites**: Alien animation with frame switching
- **Comprehensive Logging**: Debug and info logging throughout the game
- **Design Docs**: `docs/detailed_gameplay.md` (Galaga reference) and `docs/GAMEPLAY_OVERVIEW.md` (current systems)

## 📚 Gameplay Vision
- `docs/detailed_gameplay.md` captures the Galaga mechanics we plan to graft onto this project: multi-wave progression, tractor beams, challenge stages, and attract/credit loops.
- `docs/GAMEPLAY_OVERVIEW.md` explains how the current Space Invaders implementation works, making it easier to identify where Galaga systems will slot in.
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

Quick start (macOS users)
-------------------------

This project includes a small helper script `workon.sh` that creates a virtualenv, installs dependencies, optionally runs tests, and drops you into an interactive shell with the venv active. See `QUICK_START.md` for usage and examples.

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

After installation, run the game using:

### Windows
```powershell
py -m src.main
```

### macOS/Linux/Raspberry Pi
```bash
python3 -m src.main
```

## 🧪 Running Tests

### Windows
```powershell
py -m unittest discover tests
```

### macOS/Linux/Raspberry Pi
```bash
python3 -m unittest discover tests
```

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
- **Space**: Fire bullet (one bullet at a time)
- **R**: Restart game (when game over) or exit sprite viewer
- **Q**: Quit game

### Sprite Viewer Controls
- **S+1**: View Arcade sprites
- **S+2**: View Atari 2600 sprites  
- **S+3**: View Deluxe sprites
- **S+4**: View Intellivision sprites
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
- 🚧 Map current systems to Galaga feature list (`docs/detailed_gameplay.md`)
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
