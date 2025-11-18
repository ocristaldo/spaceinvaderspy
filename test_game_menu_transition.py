#!/usr/bin/env python3
"""
Test script to diagnose menu transition issues.
"""
import sys
import traceback
import logging
import pygame

# Setup logging to see debug output
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

try:
    logger.info("Importing Game class...")
    from src.main import Game
    logger.info("Game class imported successfully")

    logger.info("Creating Game instance...")
    game = Game()
    logger.info("Game instance created successfully")

    logger.info("Running game loop with intro skip...")

    running = True
    frame_count = 0
    max_frames = 600  # ~10 seconds at 60 FPS
    intro_skipped = False

    while running and frame_count < max_frames:
        try:
            # Skip the intro after 2 seconds (120 frames)
            if frame_count == 120 and not intro_skipped:
                logger.info("Simulating ENTER key to skip intro...")
                event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
                pygame.event.post(event)
                intro_skipped = True

            game.update()
            game.draw()
            pygame.display.flip()

            # Check for quit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logger.warning("Quit event received")
                    running = False
                    break

            frame_count += 1
            if frame_count % 60 == 0:
                elapsed = (pygame.time.get_ticks()) / 1000
                logger.info(f"Frame {frame_count}, State: {game.state_manager.current_state}")

            # Log state transitions
            if frame_count < 150 or intro_skipped:
                if frame_count % 15 == 0:
                    logger.debug(f"  GameOver={game.game_over}, Menu visible={game.menu is not None}")

        except Exception as e:
            logger.error(f"Error during game loop iteration {frame_count}: {e}")
            traceback.print_exc()
            break

    logger.info(f"Game loop completed. Total frames: {frame_count}")
    pygame.quit()
    sys.exit(0)

except Exception as e:
    logger.error(f"Failed to start game: {e}")
    traceback.print_exc()
    sys.exit(1)
