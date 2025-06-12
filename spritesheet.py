"""Utility for extracting sprites from a sprite sheet."""
import pygame
import constants


class SpriteSheet:
    """Load a sprite sheet image and provide access to individual sprites."""

    def __init__(self, file_name: str):
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x: int, y: int, width: int, height: int) -> pygame.Surface:
        """Return a single sprite from the loaded sheet."""
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(constants.KEY_COLOR)
        return image
