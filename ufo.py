import pygame
import random
import constants
import config

class UFO(pygame.sprite.Sprite):
    """Mystery saucer that awards bonus points."""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((24, 12))
        self.image.fill(constants.BLUE)
        self.rect = self.image.get_rect(topleft=(-30, 30))
        self.speed = 2
        self.value = random.choice([50, 100, 150, 300])

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > config.SCREEN_WIDTH:
            self.kill()
