import pygame
import constants

class Alien(pygame.sprite.Sprite):
    """Single alien sprite."""

    def __init__(self, x, y, value):
        super().__init__()
        self.image = pygame.Surface((16, 12))
        self.image.fill(constants.GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.value = value
