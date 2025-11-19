"""
Input handling system for the game.
"""
from typing import Any, Callable, Dict

import pygame

from ..utils.logger import setup_logger


class InputHandler:
    """Handles all input events and key states."""

    def __init__(self):
        """Initialize the input handler."""
        self.logger = setup_logger(__name__)
        self.key_bindings: Dict[int, Callable] = {}
        self.event_handlers: Dict[int, Callable] = {}

    def bind_key(self, key: int, callback: Callable) -> None:
        """Bind a key to a callback function."""
        self.key_bindings[key] = callback

    def bind_event(self, event_type: int, callback: Callable) -> None:
        """Bind an event type to a callback function."""
        self.event_handlers[event_type] = callback

    def handle_events(self) -> None:
        """Process all pygame events."""
        for event in pygame.event.get():
            if event.type in self.event_handlers:
                self.event_handlers[event.type](event)
            elif event.type == pygame.KEYDOWN and event.key in self.key_bindings:
                self.key_bindings[event.key](event)

    def get_pressed_keys(self) -> Any:
        """Get currently pressed keys."""
        return pygame.key.get_pressed()
