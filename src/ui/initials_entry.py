"""
Initials Entry Screen for High Score Entry

Allows players to enter 3-character initials after achieving a high score.
"""
import pygame
from typing import Optional, Callable
from ..utils.logger import setup_logger
from .font_manager import get_font


class InitialsEntry:
    """Screen for entering player initials for a high score."""

    # Valid characters for initials
    VALID_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"

    def __init__(self, score: int, callback: Callable[[str], None]):
        """
        Initialize the initials entry screen.

        Args:
            score: The high score value to display
            callback: Function to call when initials are confirmed, receives initials string
        """
        self.logger = setup_logger(__name__)
        self.score = score
        self.callback = callback
        self.initials = ["-", "-", "-"]  # Three character slots
        self.current_position = 0  # Which initial we're editing (0-2)
        self.is_active = True
        self.blink_timer = 0
        self.blink_interval = 30  # Frames between blinks

        # Key state tracking to prevent repeated triggers
        self.last_keys_state = {
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_UP: False,
            pygame.K_DOWN: False,
            pygame.K_BACKSPACE: False,
            "confirm": False,  # For RETURN or SPACE
        }

    def handle_input(self, keys: tuple) -> None:
        """
        Handle keyboard input for initials entry.

        Args:
            keys: Pygame key pressed state tuple from pygame.key.get_pressed()
        """
        if not self.is_active:
            return

        if not keys or len(keys) < 512:
            self.logger.warning("Invalid keys tuple received in initials entry")
            return

        # Use pygame.key.get_pressed() to detect key presses without consuming events
        # Track state to only trigger on key press (not held down)

        # Left/Right arrows to move between initial slots
        try:
            if keys[pygame.K_LEFT] and not self.last_keys_state.get(pygame.K_LEFT, False):
                if self.current_position > 0:
                    self.current_position -= 1
            self.last_keys_state[pygame.K_LEFT] = keys[pygame.K_LEFT]

            if keys[pygame.K_RIGHT] and not self.last_keys_state.get(pygame.K_RIGHT, False):
                if self.current_position < 2:
                    self.current_position += 1
            self.last_keys_state[pygame.K_RIGHT] = keys[pygame.K_RIGHT]

            # Up/Down arrows to cycle character
            if keys[pygame.K_UP] and not self.last_keys_state.get(pygame.K_UP, False):
                self._cycle_character(direction=1)
            self.last_keys_state[pygame.K_UP] = keys[pygame.K_UP]

            if keys[pygame.K_DOWN] and not self.last_keys_state.get(pygame.K_DOWN, False):
                self._cycle_character(direction=-1)
            self.last_keys_state[pygame.K_DOWN] = keys[pygame.K_DOWN]

            # Backspace to clear slot
            if keys[pygame.K_BACKSPACE] and not self.last_keys_state.get(pygame.K_BACKSPACE, False):
                self.initials[self.current_position] = "-"
            self.last_keys_state[pygame.K_BACKSPACE] = keys[pygame.K_BACKSPACE]

            # Enter/Space to confirm
            if (keys[pygame.K_RETURN] or keys[pygame.K_SPACE]) and not self.last_keys_state.get("confirm", False):
                self.confirm_initials()
            self.last_keys_state["confirm"] = keys[pygame.K_RETURN] or keys[pygame.K_SPACE]
        except (IndexError, TypeError) as e:
            self.logger.error(f"Error processing initials entry input: {e}", exc_info=True)

    def _cycle_character(self, direction: int = 1) -> None:
        """
        Cycle the current character up or down.

        Args:
            direction: 1 for next, -1 for previous
        """
        current_char = self.initials[self.current_position]
        try:
            current_idx = self.VALID_CHARS.index(current_char)
        except ValueError:
            current_idx = 0

        new_idx = (current_idx + direction) % len(self.VALID_CHARS)
        self.initials[self.current_position] = self.VALID_CHARS[new_idx]

    def confirm_initials(self) -> None:
        """Confirm the entered initials and call the callback."""
        initials_str = "".join(self.initials)
        self.logger.info(f"Initials confirmed: {initials_str}")
        self.is_active = False
        self.callback(initials_str)

    def update(self) -> None:
        """Update the screen state (for blinking cursor animation)."""
        self.blink_timer = (self.blink_timer + 1) % (self.blink_interval * 2)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the initials entry screen.

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
        text_font = get_font("menu_large")
        small_font = get_font("menu_small")

        # Title
        title_text = title_font.render("NEW HIGH SCORE!", True, (255, 255, 0))
        title_rect = title_text.get_rect(
            centerx=surface.get_width() // 2,
            y=surface.get_height() // 4
        )
        surface.blit(title_text, title_rect)

        # Score display
        score_text = text_font.render(f"{self.score}", True, (200, 200, 200))
        score_rect = score_text.get_rect(
            centerx=surface.get_width() // 2,
            y=title_rect.bottom + 40
        )
        surface.blit(score_text, score_rect)

        # "ENTER YOUR INITIALS" prompt
        prompt_text = text_font.render("ENTER YOUR INITIALS", True, (255, 255, 255))
        prompt_rect = prompt_text.get_rect(
            centerx=surface.get_width() // 2,
            y=score_rect.bottom + 60
        )
        surface.blit(prompt_text, prompt_rect)

        # Initials entry boxes
        box_y = prompt_rect.bottom + 60
        box_spacing = 50
        box_width = 40
        box_height = 50
        box_start_x = surface.get_width() // 2 - (box_spacing * 2) // 2 - box_width // 2

        for i, initial in enumerate(self.initials):
            box_x = box_start_x + (i * box_spacing)

            # Draw box
            is_active = i == self.current_position
            box_color = (255, 255, 0) if is_active else (200, 200, 200)
            pygame.draw.rect(surface, box_color, (box_x, box_y, box_width, box_height), 2)

            # Draw character
            char_text = text_font.render(initial, True, (255, 255, 255))
            char_rect = char_text.get_rect(center=(box_x + box_width // 2, box_y + box_height // 2))
            surface.blit(char_text, char_rect)

            # Draw cursor (blinking)
            if is_active and self.blink_timer < self.blink_interval:
                cursor_y = box_y + box_height + 5
                pygame.draw.line(surface, box_color, (box_x, cursor_y), (box_x + box_width, cursor_y), 2)

        # Instructions
        instr_y = box_y + box_height + 60
        instr_font = small_font
        instr_text = instr_font.render("UP/DOWN: Change Letter | LEFT/RIGHT: Move | SPACE/ENTER: Confirm", True, (150, 150, 150))
        instr_rect = instr_text.get_rect(centerx=surface.get_width() // 2, y=instr_y)
        surface.blit(instr_text, instr_rect)
