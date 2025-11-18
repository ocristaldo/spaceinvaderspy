# Debug Guide - Space Invaders Python

## Running in Debug Mode

There are two ways to run the game in debug mode:

### Option 1: Using the debug script (easiest)
```bash
./debug.sh
```

This will:
- Enable full DEBUG level logging
- Show all debug messages in the console
- Save detailed logs to `game.log`
- Display instructions for reproducing the issue

### Option 2: Using environment variable
```bash
SPACEINVADERS_DEBUG=1 python -m src.main
```

## Understanding the Logs

### Log Levels
- **DEBUG**: Detailed information for debugging (only shown in console in debug mode)
- **INFO**: General information about game flow
- **WARNING**: Something unexpected but not fatal
- **ERROR**: An error occurred but game continues
- **CRITICAL**: A critical error that may cause a crash

### Console Output
In **normal mode**:
- Console shows: WARNING, ERROR, CRITICAL
- File (game.log) shows: Everything

In **debug mode** (SPACEINVADERS_DEBUG=1):
- Console shows: DEBUG, INFO, WARNING, ERROR, CRITICAL
- File (game.log) shows: Everything

## How to Reproduce and Debug the Issue

### Steps to Test
1. Run in debug mode: `./debug.sh`
2. Start a 1-Player game (press `1`)
3. Lose all 3 lives (let aliens hit you or move down)
4. Observe what happens:
   - Does the continue screen appear?
   - Does the initials entry screen appear?
   - Does the game quit completely?
5. Check the console output and game.log

### What to Look For

**If the game quits:**
- Look for ERROR or CRITICAL messages in the console
- Check game.log for the full error traceback
- Share these error messages

**If the continue screen appears but something is wrong:**
- Look for WARNING messages about input handling
- Check if initials entry screen is being created

**If the initials screen appears but has issues:**
- Look for error messages about key input
- Check for invalid keys tuple messages

## Log File Location

The log file is saved to:
```
./game.log
```

You can view it while the game is running in another terminal:
```bash
tail -f game.log
```

Or after the game closes:
```bash
cat game.log
```

## Searching Logs

Find errors:
```bash
grep -i "error\|critical" game.log
```

Find initials entry related logs:
```bash
grep -i "initials" game.log
```

Find continue screen related logs:
```bash
grep -i "continue" game.log
```

Find game over related logs:
```bash
grep -i "game.over\|game_over" game.log
```

## Common Issues and Solutions

### Issue: "Invalid keys tuple received"
- This means the keys parameter is not valid
- Check that pygame.key.get_pressed() is being called correctly
- Look for index out of range errors

### Issue: "Error in initials entry"
- The initials entry screen is crashing
- Check the full error message in the log
- Look for character input or state tracking issues

### Issue: "Error saving high score"
- The high score manager is failing
- Check if the highscores.json file exists and is readable
- Look for file permission errors

### Issue: "Unhandled exception"
- An exception occurred that wasn't caught
- The full traceback will be in the log
- Look for the exact error and line number

## Performance Debugging

In debug mode, all log messages are written immediately. This can affect performance. If you notice lag or stuttering:

1. Run without debug mode: `python -m src.main`
2. Or redirect output to a file: `SPACEINVADERS_DEBUG=1 python -m src.main > output.txt 2>&1`

## Getting Help

When reporting an issue, please provide:
1. The full game.log file
2. Your OS (Windows/Mac/Linux)
3. Python version (python --version)
4. Steps to reproduce the issue
5. What you expected to happen vs what actually happened

Example:
```
$ SPACEINVADERS_DEBUG=1 python -m src.main > /tmp/game_output.txt 2>&1
[play game, reproduce issue, quit]
$ cat /tmp/game_output.txt | grep -i error
[paste error messages here]
```
