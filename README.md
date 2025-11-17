# 👾 Space Invaders Python Clone

A work-in-progress recreation of the classic Space Invaders arcade game built with Python and Pygame. This is an educational project aimed at learning game development fundamentals.

## 🚧 Project Status: Work In Progress

This project is under active development. Features and fixes are being added regularly. Contributors welcome!

## 🎮 Current Features

### Core Gameplay
- Classic Space Invaders gameplay mechanics
- Alien formation movement with increasing speed
- Player ship controls (left/right movement, shooting)
- Destructible bunkers for defense
- UFO bonus enemy with random point values
- Scoring system with different alien point values
- Lives system (3 lives)

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
- ✅ Sprite sheet system with JSON coordinates
- ✅ Multi-platform sprite support (4 platforms)
- ✅ Interactive sprite viewer with pagination
- ✅ Comprehensive logging system
- ✅ Animated alien sprites
- ✅ Key press debouncing for sprite viewer

### In Progress 🚧
- 🚧 Documentation updates and improvements
- 🚧 Code review and best practices implementation

### Planned 📋
- 📋 Sound effects and music
- 📋 High score system with persistence
- 📋 Different levels with increasing difficulty
- 📋 Power-ups and special weapons
- 📋 Enhanced sprite animations and effects
- 📋 Menu system and game states
- 📋 Configuration file for game settings
