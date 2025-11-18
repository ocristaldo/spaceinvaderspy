"""
Continue Screen for game over with countdown

Shows when both players are out of lives with a 10-second countdown.
Player can insert credit and press 1 or 2 to continue.
"""
import pygame
from typing import Callable, Optional
from ..utils.logger import setup_logger
from .font_manager import get_font


class ContinueScreen:
    """Screen shown when both players are out of lives with countdown."""

    def __init__(
        self,
        on_continue_1p: Callable[[], None],
        on_continue_2p: Callable[[], None],
        on_timeout: Callable[[], None],
        credit_count: int = 0,
        is_two_player_mode: bool = False
    ):
        """
        Initialize the continue screen.

        Args:
            on_continue_1p: Callback when player presses 1 to continue 1P
            on_continue_2p: Callback when player presses 2 to continue 2P
            on_timeout: Callback when countdown reaches 0
            credit_count: Current credit count
            is_two_player_mode: Whether the game was in 2-player mode
        """
        self.logger = setup_logger(__name__)
        self.on_continue_1p = on_continue_1p
        self.on_continue_2p = on_continue_2p
        self.on_timeout = on_timeout
        self.credit_count = credit_count
        self.is_two_player_mode = is_two_player_mode

        self.is_active = True
        self.countdown = 10  # 10 seconds countdown
        self.countdown_timer = 0  # Milliseconds
        self.frame_count = 0

        # Key state tracking to prevent repeated triggers
        self.last_keys_state = {
            pygame.K_1: False,
            pygame.K_2: False,
        }

    def set_credit_count(self, count: int) -> None:
        """Update credit count display."""
        self.credit_count = count

    def handle_input(self, keys: tuple) -> None:
        """
        Handle keyboard input on continue screen.

        Args:
            keys: Pygame key pressed state tuple from pygame.key.get_pressed()
        """
        if not self.is_active:
            return

        # Use pygame.key.get_pressed() to detect key presses without consuming events
        # This works because handle_events() in main.py already processed pygame.event.get()
        # We track state to only trigger on key press (not held down)

        if self.is_two_player_mode:
            # 2P mode: only allow key 2 to continue
            if keys[pygame.K_2] and not self.last_keys_state[pygame.K_2]:
                if self.credit_count >= 2:
                    self.logger.info("Continue 2-Player selected")
                    self.is_active = False
                    self.on_continue_2p()
                else:
                    self.logger.info("Insufficient credits for 2P continue (need 2)")
            self.last_keys_state[pygame.K_2] = keys[pygame.K_2]
        else:
            # 1P mode: only allow key 1 to continue
            if keys[pygame.K_1] and not self.last_keys_state[pygame.K_1]:
                if self.credit_count > 0:
                    self.logger.info("Continue 1-Player selected")
                    self.is_active = False
                    self.on_continue_1p()
                else:
                    self.logger.info("Insufficient credits for 1P continue (need 1)")
            self.last_keys_state[pygame.K_1] = keys[pygame.K_1]

    def update(self, dt_ms: int = 16) -> None:
        """
        Update countdown timer.

        Args:
            dt_ms: Delta time in milliseconds (default: ~16ms for 60 FPS)
        """
        if not self.is_active:
            return

        self.countdown_timer += dt_ms
        self.frame_count += 1

        # Update countdown every second (1000ms)
        if self.countdown_timer >= 1000:
            self.countdown_timer -= 1000
            self.countdown -= 1
            self.logger.info(f"Continue countdown: {self.countdown}")

            if self.countdown <= 0:
                self.is_active = False
                self.on_timeout()

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the continue screen.

        Args:
            surface: Pygame surface to draw on
        """
        # Semi-transparent overlay
        overlay = pygame.Surface(surface.get_size())
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))

        # Get fonts
        title_font = get_font("menu_title")
        text_font = get_font("demo_subtitle")  # Larger text for countdown
        small_font = get_font("menu_small")

        # Title
        title_text = title_font.render("CONTINUE?", True, (255, 255, 0))
        title_rect = title_text.get_rect(
            centerx=surface.get_width() // 2,
            y=surface.get_height() // 4
        )
        surface.blit(title_text, title_rect)

        # Countdown display (large)
        countdown_text = text_font.render(f"{max(0, self.countdown)}", True, (255, 100, 100))
        countdown_rect = countdown_text.get_rect(
            centerx=surface.get_width() // 2,
            y=title_rect.bottom + 60
        )
        surface.blit(countdown_text, countdown_rect)

        # Credit status
        credit_color = (100, 255, 100) if self.credit_count > 0 else (255, 100, 100)
        credit_text = text_font.render(f"CREDITS: {self.credit_count:02d}", True, credit_color)
        credit_rect = credit_text.get_rect(
            centerx=surface.get_width() // 2,
            y=countdown_rect.bottom + 40
        )
        surface.blit(credit_text, credit_rect)

        # Instructions
        instr_y = credit_rect.bottom + 60

        if self.is_two_player_mode:
            # 2P mode instructions
            needed_credits = 2 - self.credit_count
            if self.credit_count >= 2:
                instr_text = small_font.render("Press 2 to continue 2-Player game", True, (150, 200, 150))
            else:
                instr_text = small_font.render(f"Need {needed_credits} more credit(s)", True, (255, 150, 100))
            instr_rect = instr_text.get_rect(centerx=surface.get_width() // 2, y=instr_y)
            surface.blit(instr_text, instr_rect)

            instr_y += instr_rect.height + 20
            instr2_text = small_font.render("Press C to insert coin", True, (150, 150, 200))
            instr2_rect = instr2_text.get_rect(centerx=surface.get_width() // 2, y=instr_y)
            surface.blit(instr2_text, instr2_rect)
        else:
            # 1P mode instructions
            if self.credit_count > 0:
                instr_text = small_font.render("Press 1 to continue 1-Player game", True, (150, 200, 150))
            else:
                instr_text = small_font.render("INSERT COIN TO CONTINUE", True, (255, 100, 100))
            instr_rect = instr_text.get_rect(centerx=surface.get_width() // 2, y=instr_y)
            surface.blit(instr_text, instr_rect)

            instr_y += instr_rect.height + 20
            instr2_text = small_font.render("Press C to insert coin", True, (150, 150, 200))
            instr2_rect = instr2_text.get_rect(centerx=surface.get_width() // 2, y=instr_y)
            surface.blit(instr2_text, instr2_rect)
