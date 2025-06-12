# spaceinvaderspy

A small Python recreation of the classic **Space Invaders** arcade game.

## Requirements

* Python 3.8+
* [Pygame](https://www.pygame.org/)

Install the dependencies with:

```bash
pip install -r requirements.txt
```

## Running

Execute the main script to start the game:

```bash
python spaceinvaders.py
```

Use the arrow keys to move the ship and press **Space** to fire. Aliens move as a group and descend each time they hit the screen edges. Destroy all aliens to win.

This project is a work in progress and aims to mirror the behaviour of the 1978 original as closely as possible.

## Testing

Automated unit tests use `unittest` together with a small Pygame stub so they
can run without a display. The tests cover projectiles, bunkers and basic player
movement. Run the suite from the project directory with:

```bash
python -m unittest discover tests
```

## Platform notes

The game runs anywhere Python and Pygame are available. Below are example steps
for common platforms.

### Linux

Most distributions include Python. Install the requirements using pip:

```bash
pip install -r requirements.txt
```

Launch the game with:

```bash
python spaceinvaders.py
```

### Windows

Install Python from [python.org](https://www.python.org/). Open *Command
Prompt* in the project folder and run:

```cmd
pip install -r requirements.txt
python spaceinvaders.py
```

### macOS

If using [Homebrew](https://brew.sh/), install Python and the dependencies via
pip:

```bash
brew install python
pip install -r requirements.txt
python spaceinvaders.py
```

### Raspberry Pi

Raspberry Pi OS also comes with Python. Install Pygame using pip:

```bash
pip install -r requirements.txt
```

You may lower the resolution in `config.py` for smoother gameplay on the Pi.
Run the game normally:

```bash
python spaceinvaders.py
```
