# 👾 Space Invaders Python Clone

A work-in-progress recreation of the classic Space Invaders arcade game built with Python and Pygame. This is an educational project aimed at learning game development fundamentals.

## 🚧 Project Status: Work In Progress

This project is under active development. Features and fixes are being added regularly. Contributors welcome!

## 🎮 Current Features

- Classic Space Invaders gameplay
- Alien formation movement
- Player ship controls
- Bunkers for defense
- UFO bonus enemy
- Scoring system
- Lives system

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
├── src/              # Source code
├── assets/           # Game assets (images, sounds)
│   └── images/       # Sprite images
├── tests/            # Unit tests
└── requirements.txt  # Python dependencies
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

- Left Arrow/Right Arrow: Move player ship
- Space: Fire bullet
- R: Restart game (when game over)
- Q: Quit game

## 🐛 Known Issues

- [Your known issues here]
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

- Add sound effects
- Implement high score system
- Add different levels with increasing difficulty
- Add power-ups and special weapons
- Create custom sprite animations
