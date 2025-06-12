import os
import pygame
from . import constants
from . import config

class Alien(pygame.sprite.Sprite):
    """Single alien sprite."""

    def __init__(self, x, y, value):
        super().__init__()
        sprite_map = {30: "alien1.png", 20: "alien2.png", 10: "alien3.png"}
        path = os.path.join(config.IMG_DIR, sprite_map.get(value, "alien1.png"))
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.value = value
