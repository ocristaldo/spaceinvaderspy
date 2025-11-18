#!/usr/bin/env python3
"""
Test script to diagnose game startup issues.
"""
import sys
import traceback
import logging

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

    logger.info("Running game for 5 seconds...")
    import pygame
    start_time = pygame.time.get_ticks()

    # Run the game loop for a short time
    running = True
    frame_count = 0
    max_frames = 300  # ~5 seconds at 60 FPS

    while running and frame_count < max_frames:
        try:
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
                elapsed = (pygame.time.get_ticks() - start_time) / 1000
                logger.info(f"Frame {frame_count}, Elapsed: {elapsed:.1f}s, State: {game.state_manager.current_state}")

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
