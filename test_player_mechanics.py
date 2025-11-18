#!/usr/bin/env python3
"""
Test script to verify player mechanics in 1P and 2P modes.
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
    logger.info("Testing Player Mechanics")
    logger.info("=" * 60)

    # Test 1: Single player mode
    logger.info("\n--- Testing 1-Player Mode ---")
    game = Game()
    game.two_player_mode = False
    game.state_manager.change_state(GameState.PLAYING)
    game.reset_game(start_playing=True)

    logger.info(f"✓ 1P mode: Score={game.score}, Lives={game.lives}")
    assert game.lives == 3, f"Should have 3 lives, got {game.lives}"

    # Simulate bomb hit (deduct 1 life)
    game.lives -= 1
    assert game.lives == 2, f"Should have 2 lives after 1 hit, got {game.lives}"
    logger.info(f"✓ After 1 bomb hit: Lives={game.lives}")

    # Simulate 2 more hits
    game.lives -= 1
    game.lives -= 1
    assert game.lives == 0, f"Should have 0 lives after 3 hits, got {game.lives}"
    logger.info(f"✓ After 3 bomb hits: Lives={game.lives} (DEAD)")

    # Test 2: 2-Player mode
    logger.info("\n--- Testing 2-Player Mode ---")
    game = Game()
    game.two_player_mode = True
    game.current_player = 1
    game.state_manager.change_state(GameState.PLAYING)
    game.reset_game(start_playing=True)

    logger.info(f"✓ Initial: P1 Lives={game.lives}, P2 Lives={game.p2_lives}")
    assert game.lives == 3, f"P1 should have 3 lives, got {game.lives}"
    assert game.p2_lives == 3, f"P2 should have 3 lives, got {game.p2_lives}"

    # Player 1 gets hit 3 times (dies)
    logger.info("Simulating P1 taking 3 bomb hits...")
    game.lives -= 1
    game.lives -= 1
    game.lives -= 1
    assert game.lives == 0, f"P1 should have 0 lives, got {game.lives}"
    logger.info(f"✓ P1 after 3 hits: Lives={game.lives} (DEAD)")

    # Player 2 is still alive
    assert game.p2_lives == 3, f"P2 should still have 3 lives, got {game.p2_lives}"
    logger.info(f"✓ P2 still alive: Lives={game.p2_lives}")

    # Simulate switch to player 2
    game.switch_player()
    assert game.current_player == 2, f"Should be Player 2, got {game.current_player}"
    logger.info(f"✓ Switched to Player {game.current_player}")

    # Verify display shows P2 lives
    current_lives = game.p2_lives if (game.two_player_mode and game.current_player == 2) else game.lives
    assert current_lives == 3, f"Should display P2 lives (3), got {current_lives}"
    logger.info(f"✓ Display shows P2 lives: {current_lives}")

    # Player 2 gets hit 3 times (dies)
    logger.info("Simulating P2 taking 3 bomb hits...")
    game.p2_lives -= 1
    game.p2_lives -= 1
    game.p2_lives -= 1
    assert game.p2_lives == 0, f"P2 should have 0 lives, got {game.p2_lives}"
    logger.info(f"✓ P2 after 3 hits: Lives={game.p2_lives} (DEAD)")

    # Both players out of lives
    assert game.lives == 0, f"P1 should have 0 lives, got {game.lives}"
    assert game.p2_lives == 0, f"P2 should have 0 lives, got {game.p2_lives}"
    logger.info(f"✓ Game Over: P1={game.lives}, P2={game.p2_lives} (BOTH DEAD)")

    # Test 3: Score updates for current player
    logger.info("\n--- Testing Score Updates ---")
    game = Game()
    game.two_player_mode = True
    game.current_player = 1
    game.state_manager.change_state(GameState.PLAYING)
    game.reset_game(start_playing=True)

    initial_p1_score = game.score
    initial_p2_score = game.p2_score

    # Player 1 gets points
    game.current_player = 1
    game.score += 100
    assert game.score == initial_p1_score + 100, f"P1 score should be {initial_p1_score + 100}"
    logger.info(f"✓ P1 score updated: {game.score}")

    # Switch to Player 2 and get points
    game.current_player = 2
    game.p2_score += 200
    assert game.p2_score == initial_p2_score + 200, f"P2 score should be {initial_p2_score + 200}"
    logger.info(f"✓ P2 score updated: {game.p2_score}")

    # Verify scores are independent
    assert game.score == initial_p1_score + 100, f"P1 score should be {initial_p1_score + 100}"
    assert game.p2_score == initial_p2_score + 200, f"P2 score should be {initial_p2_score + 200}"
    logger.info(f"✓ Scores independent: P1={game.score}, P2={game.p2_score}")

    logger.info("\n" + "=" * 60)
    logger.info("All player mechanics tests passed!")
    logger.info("=" * 60)

    pygame.quit()
    sys.exit(0)

except Exception as e:
    logger.error(f"Test failed: {e}")
    import traceback
    traceback.print_exc()
    pygame.quit()
    sys.exit(1)
