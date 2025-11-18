#!/usr/bin/env python3
"""
Comprehensive test suite for Space Invaders game.
Tests game startup, state transitions, and core functionality.
"""
import sys
import traceback
import logging
import pygame

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class GameTestSuite:
    """Run comprehensive tests on the game."""

    def __init__(self):
        self.failed_tests = []
        self.passed_tests = []
        self.game = None

    def setup(self):
        """Initialize the game for testing."""
        try:
            from src.main import Game
            self.game = Game()
            logger.info("✓ Game instance created successfully")
            self.passed_tests.append("Game Initialization")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to create game: {e}")
            traceback.print_exc()
            self.failed_tests.append(("Game Initialization", str(e)))
            return False

    def test_initial_state(self):
        """Test that game starts in ATTRACT state."""
        try:
            assert self.game.state_manager.current_state.name == "ATTRACT"
            assert self.game.credit_count >= 0
            logger.info(f"✓ Initial state correct: ATTRACT, Credits: {self.game.credit_count:02d}")
            self.passed_tests.append("Initial State")
            return True
        except AssertionError as e:
            logger.error(f"✗ Initial state test failed: {e}")
            self.failed_tests.append(("Initial State", str(e)))
            return False

    def test_attract_to_menu_transition(self):
        """Test ATTRACT -> MENU state transition."""
        try:
            frame_count = 0
            while frame_count < 300:
                self.game.handle_events()
                if self.game.state_manager.current_state.name == "PLAYING":
                    # If we hit PLAYING, we passed through MENU
                    break
                if frame_count == 120:
                    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
                    pygame.event.post(event)
                if self.game.state_manager.current_state.name == "MENU" and frame_count > 120:
                    logger.info("✓ ATTRACT -> MENU transition successful")
                    self.passed_tests.append("Attract to Menu Transition")
                    return True
                self.game.draw()
                pygame.display.flip()
                frame_count += 1

            logger.error("✗ ATTRACT -> MENU transition timeout")
            self.failed_tests.append(("Attract to Menu Transition", "Timeout"))
            return False

        except Exception as e:
            logger.error(f"✗ ATTRACT -> MENU transition failed: {e}")
            traceback.print_exc()
            self.failed_tests.append(("Attract to Menu Transition", str(e)))
            return False

    def test_menu_to_game_transition(self):
        """Test MENU -> PLAYING state transition."""
        try:
            # First get to menu
            frame_count = 0
            while frame_count < 300 and self.game.state_manager.current_state.name != "MENU":
                if frame_count == 120:
                    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
                    pygame.event.post(event)
                self.game.handle_events()
                self.game.draw()
                pygame.display.flip()
                frame_count += 1

            # Now start 1P game
            frame_count = 0
            initial_credits = self.game.credit_count
            while frame_count < 200:
                if frame_count == 30:
                    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_1)
                    pygame.event.post(event)
                self.game.handle_events()
                if self.game.state_manager.current_state.name == "PLAYING":
                    # Check that credit was deducted
                    if self.game.credit_count == initial_credits - 1:
                        logger.info("✓ MENU -> PLAYING transition successful, credit deducted")
                        self.passed_tests.append("Menu to Playing Transition")
                        return True
                    else:
                        logger.error(f"✗ Credit not deducted: {initial_credits} -> {self.game.credit_count}")
                        self.failed_tests.append(("Menu to Playing Transition", "Credit not deducted"))
                        return False
                self.game.draw()
                pygame.display.flip()
                frame_count += 1

            logger.error("✗ MENU -> PLAYING transition timeout")
            self.failed_tests.append(("Menu to Playing Transition", "Timeout"))
            return False

        except Exception as e:
            logger.error(f"✗ MENU -> PLAYING transition failed: {e}")
            traceback.print_exc()
            self.failed_tests.append(("Menu to Playing Transition", str(e)))
            return False

    def test_credit_system(self):
        """Test credit insertion and display."""
        try:
            initial_credits = self.game.credit_count
            self.game.credit_count = 0

            # Insert credit
            self.game._insert_credit()
            assert self.game.credit_count == 1, f"Credit not inserted: {self.game.credit_count}"

            # Insert multiple credits
            self.game._insert_credit(5)
            assert self.game.credit_count == 6, f"Multiple credits not inserted: {self.game.credit_count}"

            # Test cap at 99
            self.game.credit_count = 98
            self.game._insert_credit(5)
            assert self.game.credit_count == 99, f"Credit cap not enforced: {self.game.credit_count}"

            logger.info(f"✓ Credit system working correctly (current: {self.game.credit_count})")
            self.passed_tests.append("Credit System")
            return True

        except Exception as e:
            logger.error(f"✗ Credit system test failed: {e}")
            self.failed_tests.append(("Credit System", str(e)))
            return False

    def test_fonts_available(self):
        """Test that all required fonts are available."""
        try:
            from src.ui.font_manager import get_font

            required_fonts = [
                "menu_title", "menu_body", "menu_small",
                "demo_title", "demo_subtitle", "demo_entry", "demo_prompt",
                "hud_main", "hud_small"
            ]

            missing = []
            for font_name in required_fonts:
                try:
                    get_font(font_name)
                except KeyError:
                    missing.append(font_name)

            if missing:
                logger.error(f"✗ Missing fonts: {', '.join(missing)}")
                self.failed_tests.append(("Fonts Available", f"Missing: {missing}"))
                return False

            logger.info(f"✓ All {len(required_fonts)} required fonts available")
            self.passed_tests.append("Fonts Available")
            return True

        except Exception as e:
            logger.error(f"✗ Font test failed: {e}")
            self.failed_tests.append(("Fonts Available", str(e)))
            return False

    def test_continue_screen_class(self):
        """Test that ContinueScreen can be instantiated."""
        try:
            from src.ui.continue_screen import ContinueScreen

            screen = ContinueScreen(
                on_continue_1p=lambda: None,
                on_continue_2p=lambda: None,
                on_timeout=lambda: None,
                credit_count=5
            )

            assert screen.countdown == 10
            assert screen.credit_count == 5
            assert screen.is_active

            logger.info("✓ ContinueScreen class working correctly")
            self.passed_tests.append("Continue Screen Class")
            return True

        except Exception as e:
            logger.error(f"✗ ContinueScreen test failed: {e}")
            traceback.print_exc()
            self.failed_tests.append(("Continue Screen Class", str(e)))
            return False

    def test_initials_entry_class(self):
        """Test that InitialsEntry can be instantiated."""
        try:
            from src.ui.initials_entry import InitialsEntry

            entry_screen = InitialsEntry(
                score=5000,
                callback=lambda x: None
            )

            assert entry_screen.score == 5000
            assert entry_screen.is_active
            assert entry_screen.initials == ["-", "-", "-"]

            logger.info("✓ InitialsEntry class working correctly")
            self.passed_tests.append("Initials Entry Class")
            return True

        except Exception as e:
            logger.error(f"✗ InitialsEntry test failed: {e}")
            traceback.print_exc()
            self.failed_tests.append(("Initials Entry Class", str(e)))
            return False

    def run_all_tests(self):
        """Run all tests."""
        logger.info("=" * 60)
        logger.info("Starting Space Invaders Game Test Suite")
        logger.info("=" * 60)

        if not self.setup():
            logger.error("Setup failed, aborting tests")
            return False

        tests = [
            self.test_initial_state,
            self.test_credit_system,
            self.test_fonts_available,
            self.test_continue_screen_class,
            self.test_initials_entry_class,
            self.test_attract_to_menu_transition,
            self.test_menu_to_game_transition,
        ]

        for test in tests:
            try:
                test()
            except Exception as e:
                logger.error(f"Test {test.__name__} crashed: {e}")
                traceback.print_exc()

        self.print_results()
        return len(self.failed_tests) == 0

    def print_results(self):
        """Print test results summary."""
        logger.info("=" * 60)
        logger.info("Test Results Summary")
        logger.info("=" * 60)
        logger.info(f"Passed: {len(self.passed_tests)}")
        for test in self.passed_tests:
            logger.info(f"  ✓ {test}")

        if self.failed_tests:
            logger.error(f"Failed: {len(self.failed_tests)}")
            for test_name, error in self.failed_tests:
                logger.error(f"  ✗ {test_name}: {error}")
        else:
            logger.info("Failed: 0")

        logger.info("=" * 60)


if __name__ == "__main__":
    suite = GameTestSuite()
    success = suite.run_all_tests()
    pygame.quit()
    sys.exit(0 if success else 1)
