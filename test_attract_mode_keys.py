#!/usr/bin/env python3
"""
Test script to verify attract mode game start keys (1/2) work correctly.
Also tests that coin insertion works in attract mode.
"""
import sys
import logging
import pygame

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

try:
    from src.main import Game
    from src.systems.game_state_manager import GameState

    logger.info("=" * 60)
    logger.info("Testing Attract Mode Game Start Keys")
    logger.info("=" * 60)

    game = Game()

    # Test 1: Verify initial credits are 0
    assert game.credit_count == 0, f"Initial credits should be 0, got {game.credit_count}"
    logger.info(f"✓ Initial credits: {game.credit_count:02d}")

    # Test 2: Try to start 1P game without credits - should fail
    logger.info("Testing 1P game start without credits...")
    frame_count = 0
    while frame_count < 50:
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_1)
        pygame.event.post(event)
        game.handle_events()
        game.draw()
        pygame.display.flip()
        frame_count += 1

    # Game should still be in ATTRACT
    assert game.state_manager.current_state.name == "ATTRACT", \
        f"Game should still be in ATTRACT after pressing 1 without credits, got {game.state_manager.current_state.name}"
    logger.info("✓ Game correctly blocked 1P start without credits")

    # Test 3: Insert coin
    logger.info("Inserting 1 coin...")
    game._insert_credit()
    assert game.credit_count == 1, f"Credit count should be 1 after insertion, got {game.credit_count}"
    logger.info(f"✓ Coins after insertion: {game.credit_count:02d}")

    # Test 4: Start 1P game from attract mode with credit
    logger.info("Testing 1P game start with credit in attract mode...")
    frame_count = 0
    while frame_count < 100:
        if frame_count == 30:
            event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_1)
            pygame.event.post(event)
        game.handle_events()
        if game.state_manager.current_state.name == "PLAYING":
            logger.info("✓ 1P game started from attract mode!")
            assert game.two_player_mode == False, "Should be 1P mode"
            assert game.credit_count == 0, f"Credits should be 0 after deduction, got {game.credit_count}"
            logger.info(f"✓ Correct mode (1P), credits remaining: {game.credit_count:02d}")
            break
        game.draw()
        pygame.display.flip()
        frame_count += 1
    else:
        logger.error("✗ Failed to start 1P game from attract mode")
        sys.exit(1)

    # Reset for 2P test
    logger.info("\nResetting for 2P test...")
    game.reset_game(start_playing=False)
    game.state_manager.change_state(GameState.ATTRACT)
    assert game.credit_count == 0, "Credits should be 0 after reset"

    # Test 5: Insert coins and start 2P game from attract
    logger.info("Inserting 1 coin for 2P test...")
    game._insert_credit()
    assert game.credit_count == 1
    logger.info(f"✓ Coins: {game.credit_count:02d}")

    logger.info("Testing 2P game start with credit in attract mode...")
    frame_count = 0
    while frame_count < 100:
        if frame_count == 30:
            event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_2)
            pygame.event.post(event)
        game.handle_events()
        if game.state_manager.current_state.name == "PLAYING":
            logger.info("✓ 2P game started from attract mode!")
            assert game.two_player_mode == True, "Should be 2P mode"
            assert game.credit_count == 0, f"Credits should be 0 after deduction, got {game.credit_count}"
            logger.info(f"✓ Correct mode (2P), credits remaining: {game.credit_count:02d}")
            break
        game.draw()
        pygame.display.flip()
        frame_count += 1
    else:
        logger.error("✗ Failed to start 2P game from attract mode")
        sys.exit(1)

    logger.info("\n" + "=" * 60)
    logger.info("All attract mode tests passed!")
    logger.info("=" * 60)

    pygame.quit()
    sys.exit(0)

except Exception as e:
    logger.error(f"Test failed: {e}")
    import traceback
    traceback.print_exc()
    pygame.quit()
    sys.exit(1)
