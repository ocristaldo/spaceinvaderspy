"""Pytest configuration for Space Invaders tests."""
import os

import pygame
import pytest

# Set dummy video driver before pygame initialization
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")


@pytest.fixture(scope="session", autouse=True)
def setup_pygame_session():
    """Initialize pygame once per test session to avoid display state issues."""
    if not pygame.get_init():
        pygame.init()
    # Create a persistent display for the entire session
    if pygame.display.get_surface() is None:
        pygame.display.set_mode((1, 1))
    yield
    # Don't quit here - let individual tests handle pygame cleanup


@pytest.fixture(autouse=True)
def reset_pygame_per_test():
    """Ensure clean pygame state between tests."""
    yield
    # Clear any cached fonts between tests to prevent state corruption
    from src.ui.font_manager import _cache
    _cache.clear()
