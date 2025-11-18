#!/usr/bin/env python3
"""
Test script to verify 2-player mode functionality.
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
    logger.info("Testing 2-Player Mode Functionality")
    logger.info("=" * 60)

    game = Game()

    # Test 1: Verify initial credits are 0
    assert game.credit_count == 0, f"Initial credits should be 0, got {game.credit_count}"
    logger.info(f"✓ Initial credits: {game.credit_count:02d}")

    # Test 2: Try to start 2P game with 1 credit - should fail
    logger.info("Testing 2P game start with only 1 credit...")
    game._insert_credit()
    assert game.credit_count == 1
    frame_count = 0
    while frame_count < 50:
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_2)
        pygame.event.post(event)
        game.handle_events()
        game.draw()
        pygame.display.flip()
        frame_count += 1

    # Game should still be in ATTRACT
    assert game.state_manager.current_state.name == "ATTRACT", \
        f"Game should block 2P with only 1 credit, got {game.state_manager.current_state.name}"
    logger.info("✓ Game correctly blocked 2P start with 1 credit")

    # Test 3: Insert another coin and start 2P game
    logger.info("Inserting 2nd coin...")
    game._insert_credit()
    assert game.credit_count == 2, f"Credit count should be 2, got {game.credit_count}"
    logger.info(f"✓ Coins: {game.credit_count:02d}")

    logger.info("Testing 2P game start with 2 credits...")
    frame_count = 0
    while frame_count < 100:
        if frame_count == 30:
            event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_2)
            pygame.event.post(event)
        game.handle_events()
        if game.state_manager.current_state.name == "PLAYING":
            logger.info("✓ 2P game started!")
            assert game.two_player_mode == True, "Should be 2P mode"
            assert game.credit_count == 0, f"Credits should be 0 after deduction, got {game.credit_count}"
            logger.info(f"✓ 2P mode enabled, credits remaining: {game.credit_count:02d}")
            logger.info(f"✓ Current player: {game.current_player}")
            logger.info(f"✓ P1 lives: {game.lives}, P2 lives: {game.p2_lives}")
            break
        game.draw()
        pygame.display.flip()
        frame_count += 1
    else:
        logger.error("✗ Failed to start 2P game with 2 credits")
        sys.exit(1)

    # Test 4: Verify both players have lives
    assert game.lives == 3, f"P1 should have 3 lives, got {game.lives}"
    assert game.p2_lives == 3, f"P2 should have 3 lives, got {game.p2_lives}"
    logger.info("✓ Both players have 3 lives")

    # Test 5: Verify player switching code exists
    assert hasattr(game, 'switch_player'), "switch_player method should exist"
    logger.info("✓ switch_player method exists")

    logger.info("\n" + "=" * 60)
    logger.info("All 2-player mode tests passed!")
    logger.info("=" * 60)

    pygame.quit()
    sys.exit(0)

except Exception as e:
    logger.error(f"Test failed: {e}")
    import traceback
    traceback.print_exc()
    pygame.quit()
    sys.exit(1)
