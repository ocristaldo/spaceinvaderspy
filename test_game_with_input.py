#!/usr/bin/env python3
"""
Test script to verify game transitions work properly.
This test simulates user input by manually posting events to pygame.
"""
import sys
import traceback
import logging
import pygame

# Setup logging to see debug output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

try:
    logger.info("Importing Game class...")
    from src.main import Game
    logger.info("Game class imported successfully")

    logger.info("Creating Game instance...")
    game = Game()
    logger.info("Game instance created successfully")

    logger.info("Running game loop with state transitions...")

    running = True
    frame_count = 0
    max_frames = 600  # ~10 seconds at 60 FPS
    intro_skipped = False
    menu_tested = False
    game_started = False

    while running and frame_count < max_frames:
        try:
            # Simulate ENTER key after 120 frames to skip intro
            if frame_count == 120 and not intro_skipped:
                logger.info("=== Frame 120: Posting ENTER event to skip intro ===")
                event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
                pygame.event.post(event)
                intro_skipped = True

            # After state transitions to MENU, test menu selection
            if frame_count == 180 and not menu_tested and game.state_manager.current_state.name == "MENU":
                logger.info("=== Frame 180: In MENU state, posting '1' key for 1P game ===")
                event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_1)
                pygame.event.post(event)
                menu_tested = True

            game.handle_events()

            # Update only when playing
            if (game.state_manager.current_state.name == "PLAYING" and
                not game.game_over and not game.viewing_sprites):
                if pygame.time.get_ticks() >= game.level_start_ready_time:
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
                elapsed = frame_count / 60
                logger.info(f"Frame {frame_count} ({elapsed:.1f}s) - State: {game.state_manager.current_state.name}, GameOver: {game.game_over}, Credits: {game.credit_count:02d}")

        except Exception as e:
            logger.error(f"Error during frame {frame_count}: {e}")
            traceback.print_exc()
            break

    logger.info(f"Game loop completed. Total frames: {frame_count}")
    logger.info(f"Final state: {game.state_manager.current_state.name}")
    pygame.quit()
    sys.exit(0)

except Exception as e:
    logger.error(f"Failed to start game: {e}")
    traceback.print_exc()
    sys.exit(1)
