"""
Collision detection and handling system.
"""
from typing import Any, Dict, List

import pygame

from ..utils.logger import setup_logger


class CollisionManager:
    """Manages all collision detection and responses in the game."""

    def __init__(self):
        """Initialize the collision manager."""
        self.logger = setup_logger(__name__)
        self.collision_handlers: Dict[str, callable] = {}

    def register_collision_handler(self, collision_type: str, handler: callable) -> None:
        """Register a handler for a specific collision type."""
        self.collision_handlers[collision_type] = handler

    def check_group_collisions(self, group1: pygame.sprite.Group, group2: pygame.sprite.Group,
                             kill_first: bool = False, kill_second: bool = False) -> Dict[Any, List[Any]]:
        """Check collisions between two sprite groups."""
        return pygame.sprite.groupcollide(group1, group2, kill_first, kill_second)

    def check_sprite_group_collision(self, sprite: pygame.sprite.Sprite, group: pygame.sprite.Group,
                                   kill_sprites: bool = False) -> List[pygame.sprite.Sprite]:
        """Check collision between a sprite and a group."""
        return pygame.sprite.spritecollide(sprite, group, kill_sprites)

    def handle_collision(self, collision_type: str, *args, **kwargs) -> None:
        """Handle a specific collision type."""
        if collision_type in self.collision_handlers:
            self.collision_handlers[collision_type](*args, **kwargs)
        else:
            self.logger.warning(f"No handler registered for collision type: {collision_type}")
