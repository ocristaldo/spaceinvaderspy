import pygame
from . import constants

class Bunker(pygame.sprite.Sprite):
    """Defensive bunker with simple health."""

    def __init__(self, pos):
        super().__init__()
        self.health = 4
        self.images = []
        for i in range(4):
            img = pygame.Surface((32, 24))
            shade = 255 - i * 60
            img.fill((shade, shade, shade))
            self.images.append(img)
        self.image = self.images[self.health - 1]
        self.rect = self.image.get_rect(midbottom=pos)

    def damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
        else:
            self.image = self.images[self.health - 1]
