#!/bin/bash
# Debug wrapper for Space Invaders
# Runs the game in debug mode with full logging

export SPACEINVADERS_DEBUG=1

echo "═══════════════════════════════════════════════════════════"
echo "Space Invaders - DEBUG MODE"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Logging to: game.log"
echo "Debug output will be shown on console"
echo ""
echo "Steps to reproduce the issue:"
echo "1. Start a game (press 1 or 2)"
echo "2. Lose all 3 lives"
echo "3. Observe if game quits"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""

python -m src.main

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "Game ended. Check game.log for detailed logs."
echo "═══════════════════════════════════════════════════════════"
