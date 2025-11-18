# How to Play Space Invaders Python

A complete guide for players new to Space Invaders. Learn all the rules, mechanics, and strategies to master this classic arcade game.

## Table of Contents

1. [Game Overview](#game-overview)
2. [Core Objective](#core-objective)
3. [Game Controls](#game-controls)
4. [Game Modes](#game-modes)
5. [Game Rules](#game-rules)
6. [Scoring System](#scoring-system)
7. [Enemy Mechanics](#enemy-mechanics)
8. [Defensive Structures](#defensive-structures)
9. [Game States and Flow](#game-states-and-flow)
10. [Tips and Strategies](#tips-and-strategies)
11. [Game Over and Continuation](#game-over-and-continuation)

---

## Game Overview

**Space Invaders** is a classic arcade shooter game where you control a player ship at the bottom of the screen and defend against an invading alien army. It's a battle of survival: defeat all the aliens before they reach your position, or run out of lives.

The game challenges you with:
- **Increasingly difficult waves** - Each level gets progressively harder
- **Time pressure** - The aliens get faster as they descend
- **Limited defense** - Destructible bunkers erode as the battle continues
- **Scoring opportunities** - Destroy enemies for points and bonuses

**Difficulty Progression**: The game features 8 waves of increasing difficulty. As you advance through levels:
- Aliens move faster
- Enemies drop bombs more frequently
- Bunker damage becomes more critical
- Strategy becomes essential for survival

---

## Core Objective

### Victory Condition
Defeat all aliens in the current wave to advance to the next level. Clear all 8 waves to complete the game.

### Defeat Conditions
- **Your ship is destroyed** by an alien bomb while you have no lives remaining
- **An alien reaches your position** (crosses below the bunker line)
- **Aliens reach the ground** - If a single alien reaches the bottom of the screen, you lose instantly

### Lives System
- **Start with 3 lives** - You get three chances to survive
- **Lose a life** when hit by an alien bomb or contacted by an alien
- **Game Over** when all lives are depleted
- **Continue option** - After game over, you can insert credits to continue playing

---

## Game Controls

### Movement and Firing

| Key | Action |
|-----|--------|
| **← (Left Arrow)** | Move your ship left |
| **→ (Right Arrow)** | Move your ship right |
| **SPACE** | Fire a bullet at enemies |

Your ship moves horizontally along the bottom of the screen and cannot move up or down.

### Game Flow

| Key | Action |
|-----|--------|
| **ENTER** | Enter menu from attract mode (title screen) |
| **1** | Start 1-Player game (requires 1 credit) |
| **2** | Start 2-Player game (requires 2 credits) |
| **C** | Insert credit (coin) |
| **R** | Restart game when game is over |
| **Q** | Quit the game |

### Advanced Controls

| Shortcut | Action |
|----------|--------|
| **S+1** | View arcade sprites (for debugging/testing) |
| **S+2** | View start screen preview |
| **S+3** | View wave ready screen |
| **S+4** | View late-game scenario |
| **← →** (in sprite viewer) | Navigate sprite pages |

---

## Game Modes

### Single-Player Mode (1P)

**How to Start**: Press **1** from the menu or attract mode (requires 1 credit)

**What It Is**: Classic Space Invaders gameplay where you control one ship against waves of aliens.

**Gameplay**:
- You play through all 8 waves consecutively
- When you lose a life, press SPACE to respawn
- If you lose all 3 lives, the continue screen appears
- Your score persists throughout all waves

**Best For**: Learning the game, improving your skills, or casual play

### Two-Player Mode (2P)

**How to Start**: Press **2** from the menu or attract mode (requires 2 credits)

**What It Is**: Alternating arcade-style gameplay where two players take turns.

**Gameplay**:
- **Player 1 starts first** at Level 1
- **Players alternate on every bomb hit** - Whoever gets hit passes control to the other player
- **Independent progression** - Each player maintains their own:
  - Level progress
  - Alien positions and formations
  - Bunker states
  - Score
- **First-time switch**: When playing a new player for the first time, they start fresh at Level 1
- **Subsequent switches**: When returning to a player, their exact game state is restored
- **Single-player continuation**: If one player loses all lives, the other can continue solo
- **Game Over**: Only when BOTH players have 0 lives

**Player Indicator**: The bottom of the screen shows "PLAYER 1" or "PLAYER 2" in yellow so you know whose turn it is.

**Best For**: Competitive play with a friend or cooperative challenge

---

## Game Rules

### Movement and Firing

1. **Your ship can only move left and right** - You cannot move up or down
2. **Maximum speed**: Your ship moves 5 pixels per frame
3. **Boundary collision**: Your ship cannot leave the playfield edges
4. **One bullet at a time** - You can only have one bullet on screen (classically accurate)
   - Fire again only after your previous bullet hits or leaves the screen
   - This adds strategic timing to the gameplay

### Collision Detection

**Your bullets destroy**:
- Enemy aliens
- Enemy UFO (bonus ship)
- Alien bombs (can intercept incoming fire)
- Bunker blocks (friendly fire erodes cover)

**Alien bombs destroy**:
- Your ship (if you're hit)
- Bunker blocks (enemy fire damages cover)

**Enemy contact destroys**:
- Your ship (instant game over if you're out of lives)

### Bunker Mechanics

- **4 bunkers** positioned across the lower third of the screen
- **Each bunker has 4 health**
- **Taking damage**: Both your bullets and alien bombs chip away at bunker health
- **Erosion strategy**: As bunkers degrade, they provide less cover for you
- **Strategic positioning**: Using bunkers as cover becomes critical in later waves
- **Bunker design**: Bunkers have a specific shape - learn their weak points for better tactics

---

## Scoring System

### Point Values

| Enemy Type | Points |
|-----------|--------|
| Alien (top row) | 30 pts |
| Alien (middle rows) | 20 pts |
| Alien (bottom rows) | 10 pts |
| UFO (Mystery ship) | 50-300 pts (random) |

### Scoring Strategy

- **High-value targets**: Top row aliens are worth 3x more than bottom row
- **UFO hunting**: Watch for the UFO crossing the top - shooting it gives bonus points (50, 100, 150, or 300 pts)
- **Risk vs. reward**: Going for top-row aliens requires exposing yourself
- **Wave bonuses**: Clearing a wave quickly (before aliens get too close) helps your survival

### High Scores

- **Top 10 tracking**: The game saves your top 10 high scores with initials
- **Persistence**: High scores are saved to disk and persist between game sessions
- **High score screen**: View your rankings from the menu

---

## Enemy Mechanics

### Alien Formation

**Layout**:
- 5 rows of aliens (55 total)
- Arranged in a defensive formation
- Rows from top to bottom are worth: 30pts, 30pts, 20pts, 10pts, 10pts

**Animation**:
- Aliens animate between two frames every ~0.5 seconds
- Animated wiggling motion creates the classic "moving forward" effect

**Movement Pattern**:
1. Aliens move horizontally together as one unit
2. When hitting the screen edge, the entire formation:
   - Drops down by 20 pixels
   - Reverses direction (left ↔ right)
3. **Advancing threat**: With each drop, aliens get closer to your position
4. **Speed increase**: Aliens move faster as fewer remain alive
5. **Critical line**: If ANY alien drops below the bunker line (bottom - 60 pixels), you lose instantly

### Speed Progression

- **Starting speed**: Slow and manageable
- **Speed increases** when aliens are destroyed
- **End game**: Final few aliens move very quickly, limiting your reaction time
- **Wave speeds**: Each level starts slightly faster than the previous

### Bombing Pattern

- **Random bombing**: Any remaining alien can drop a bomb each frame
- **Bombing probability**: ~2% chance per frame per alien
- **Multiple bombs**: Several bombs can be falling simultaneously
- **Bomb speed**: Bombs move downward at constant velocity
- **Frequency increases**: As aliens thin out, surviving aliens bomb more frequently (more per frame)

### UFO (Mystery Ship)

**Appearance**:
- Appears randomly at the top of the screen
- Crosses horizontally from one side to the other

**Behavior**:
- Moves at constant speed (2 pixels per frame)
- Moves in a straight line across the screen
- Disappears after leaving the screen
- No bombs - only you can shoot it down

**Rewards**:
- Awards random bonus: 50, 100, 150, or 300 points
- Provides opportunity for bonus points mid-wave
- UFO score pops up when you hit it

---

## Defensive Structures

### Bunker Overview

**Purpose**: Protective barriers that block alien bombs and provide cover

**Placement**: Four bunkers evenly spaced across the lower third of the screen

**Characteristics**:
- **Starting health**: 4 health points each
- **Each hit reduces health** by 1 (whether from your shots or alien bombs)
- **Visual degradation**: Bunker appearance changes as health decreases
- **Destroyed at 0 health**: Bunker disappears when health reaches zero

### Bunker Defense Strategy

1. **Early game**: Use bunkers to position yourself away from bomb fire
2. **Mid game**: Bunkers are partially eroded; use smaller gaps strategically
3. **Late game**: Bunkers are heavily damaged; positioning becomes critical
4. **Friendly fire risk**: Your own shots can damage bunkers - be careful where you aim
5. **Cover switching**: Move between bunkers to spread damage and maintain cover

### Terrain Strategy

- **Stay behind bunkers** when aliens are actively dropping bombs
- **Position at edges** for shots when safe
- **Move to fresh bunkers** as others degrade
- **Predict bomb trajectories** to avoid exposed areas

---

## Game States and Flow

### Attract Mode (Title Screen)

**What You See**:
- Animated intro with aliens dropping into formation
- Score table showing high scores and player names
- Credit count display
- "Press ENTER to enter menu" prompt

**What You Can Do**:
- Press **ENTER** to enter the menu
- Press **1** to start 1-Player game directly (if credits available)
- Press **2** to start 2-Player game directly (if credits available)
- Press **C** to insert credits
- Press **Q** to quit

**Auto-Demo**: If the menu is idle, attract mode will replay automatically

### Menu Screen

**What You See**:
- Game title
- Menu options
- Current credit count
- Controls overview

**Menu Options**:
- **1**: Start 1-Player game
- **2**: Start 2-Player game
- **ENTER or Arrow Keys**: Navigate menu
- **D** (from Options): Replay intro demo
- **I** (from Options): Toggle intro demo autoplay
- **C**: Insert credit

### Active Gameplay

**What Happens**:
1. You control your ship at the bottom
2. Aliens descend in formation, moving left-right
3. You shoot bullets to destroy aliens
4. Aliens drop bombs trying to hit you
5. Bunkers erode from both friendly and enemy fire
6. When all aliens are destroyed, advance to next level
7. If you're hit, you lose a life and respawn

**UI Elements**:
- **Score**: Top left corner, updates in real-time
- **Lives remaining**: Bottom left, shows ship icons
- **Wave/Level number**: Displayed when advancing
- **High score**: Top right corner

### Respawn After Being Hit

**What Happens**:
1. Your ship is destroyed by a bomb
2. **Wait for SPACE key** - A message appears "Press SPACE to continue"
3. **Press SPACE** to respawn at the bottom center
4. **Invulnerability**: You have a brief moment to recover (aliens continue moving)
5. **Resume play** - The game continues from where aliens left off

**2-Player Respawn**:
- You get hit → **Automatically switches to other player** if they have lives
- Other player gets hit → **Switches back to you**

### Level Advancement

**What Triggers It**:
- All 55 aliens in current level are destroyed

**What Happens**:
1. **Wave message appears**: "Level X - [Theme Name]"
2. **Brief pause**: 2-second delay before next level starts
3. **New formation**: Fresh alien army appears at starting position
4. **Faster progression**: Next level's aliens are slightly faster
5. **Bunkers reset**: New pristine bunkers for the new level
6. **Score persists**: Your accumulated score carries forward

**8 Waves Total**:
- Waves 1-8 each increase in difficulty
- Completing wave 8 completes the game

### Game Over Screen

**Triggered When**:
- You lose all 3 lives (single-player)
- Both players lose all lives (2-player)
- An alien reaches the bottom of the screen

**What You See**:
- Semi-transparent overlay
- Game over message
- Your final score
- Current high score for reference

**Continue Screen (10-second countdown)**:
- Displays "CONTINUE?" with countdown timer
- Shows your credit count
- Instructions: "Press 1 for 1-Player or 2 for 2-Player"
- Or: "Press C to insert coin"

**Your Options**:
- **Press 1**: Continue with 1-Player game (uses 1 credit)
- **Press 2**: Continue with 2-Player game (uses 2 credits if continuing 2P, 1 if switching to 1P)
- **Press C**: Insert credit (coin)
- **Wait**: 10-second countdown ends → Return to menu automatically

**After Continue**:
- Game resets to Level 1
- Aliens and bunkers reset
- Your score starts from zero
- You get 3 new lives

---

## Tips and Strategies

### Beginner Tips

1. **Learn bunker usage**: Stay behind bunkers in early waves while learning timing
2. **Manage your ammo**: Remember you can only have one bullet on screen
3. **Don't rush**: Wait for the perfect shot rather than firing continuously
4. **Practice dodging**: Learn the bomb patterns in early waves
5. **Stay mobile**: Keep moving to avoid predictable positions

### Intermediate Strategies

1. **Target the top**: Prioritize top-row aliens (30 pts vs 10 pts for bottom)
2. **Watch for patterns**: Alien bombs follow predictable paths
3. **Pre-position**: Anticipate where you need to be before bombs arrive
4. **Bunker management**: Spread bunker damage across all four rather than relying on one
5. **UFO hunting**: Watch for the UFO and time your shots for bonus points

### Advanced Tactics

1. **Edge positioning**: Fight near bunker edges to maximize return fire opportunities
2. **Timing perfection**: Master the exact timing to fire between bunker gaps
3. **Wave prediction**: Know which wave is coming to prepare your approach
4. **Minimum bunker damage**: Use specific trajectories to avoid unnecessary erosion
5. **End-game mastery**: When bunkers are gone, pure reflexes determine survival
6. **Strategic retreats**: Sometimes not shooting is better than exposing yourself

### Difficulty Progression

- **Waves 1-3**: Learn mechanics and build confidence
- **Waves 4-5**: Bunkers degrade significantly; positioning becomes critical
- **Waves 6-8**: Extreme speed and intensity; mastery required
- **Wave 8**: Final challenge - fastest aliens, most dangerous conditions

### Scoring Tips

- **Early points**: Build up score in early waves when aliens are slow
- **UFO bonus**: Each UFO is worth 50-300 pts - hunt them when safe
- **Top-row farming**: In later waves, focus top row aliens for higher scores
- **Risk assessment**: High-score runs require aggressive positioning

---

## Game Over and Continuation

### Continue Screen Mechanics

**When It Appears**:
- After you lose all lives (single-player)
- After both players lose all lives (2-player)

**Countdown Behavior**:
- Timer counts from 10 to 0 seconds
- Displays large countdown number in the center
- Updates credit count in real-time
- Instructions change based on credit availability

**No Credits Available**:
- Message: "INSERT COIN TO CONTINUE"
- Press **C** to insert credit (if available)
- Then press **1** or **2** to continue

**Credits Available**:
- Message: "Press 1 for 1-Player or 2 for 2-Player"
- Press **C** to insert additional credits

### Timeout Behavior

**If you don't press anything**:
- Countdown reaches 0 seconds
- Game automatically returns to menu
- Game over state is discarded
- You must start over from beginning

### Continuing the Game

**Press 1 for 1-Player**:
- Costs 1 credit
- Resets score to 0
- Resets level to 1
- Gives you 3 new lives
- Clears bunkers
- Enemies respawn at start

**Press 2 for 2-Player** (if in 2P mode):
- Costs 1-2 credits (depending on mode)
- Resets both players' scores to 0
- Resets both players to Level 1
- Both players get 3 new lives

### Credit System

**Acquiring Credits**:
- Press **C** to insert a credit (coin)
- Each credit represents one game opportunity

**Cost Breakdown**:
- **1-Player game**: 1 credit per game
- **2-Player game**: 2 credits total (1 per player)
- **Continue 1P**: 1 credit
- **Continue 2P**: Varies based on continuation method

**Credit Cap**:
- Maximum 99 credits can be stored
- Display shows "CREDITS: XX" with leading zero (e.g., "CREDITS: 05")

**Resetting Credits**:
- Credits don't reset between plays
- They persist as long as the game is running
- New game session starts credits fresh

---

## Accessibility Features

### Audio System

- **Sound Effects**: Explosion sounds when hitting enemies, gunfire feedback
- **Menu Music**: Background music during menus and attract mode
- **Audio Toggle**: Press **D** in options to toggle audio on/off
- **Mute Status**: Persists to settings file between sessions

### Visual Features

- **High contrast**: Bright colors on black background (arcade classic)
- **Sprite borders**: Debug mode shows sprite boundaries (S+key combinations)
- **Large text**: Scalable UI for readability
- **Dynamic scaling**: Game scales to any window size while maintaining aspect ratio

---

## Troubleshooting

### I can't see the continue screen

**Solutions**:
1. Make sure you're running the latest version of the game
2. Check that you have a valid display (the game needs a window)
3. Continue screen appears 10 seconds after game over - don't close the window

### The continue screen is not responding to my key presses

**Solutions**:
1. Make sure you pressed **1** or **2** (not other numbers)
2. Check your credit count - need credits to continue
3. Wait for the current frame to process (game updates at 60 FPS)
4. If credits are 0, press **C** to insert a credit first

### Game quit unexpectedly

**Solutions**:
1. Check the game log for error messages
2. Make sure all dependencies are installed (pygame, etc.)
3. Try restarting the game
4. Report the issue with the error message to GitHub Issues

### My high score didn't save

**Solutions**:
1. High scores only save for positions in top 10
2. Make sure you completed the initials entry screen
3. High scores are saved to `highscores.json` in the game directory
4. Check file permissions if you can't save

---

## Credits and Attribution

This is an unofficial fan recreation of the classic 1978 Space Invaders arcade game, created for educational purposes. The original game was developed by Taito Corporation.

This Python implementation adds modern quality-of-life features while maintaining the spirit and mechanics of the original arcade classic.

**Enjoy the game and good luck invader!**
