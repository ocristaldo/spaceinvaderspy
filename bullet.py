import pygame
import constants
import config

class Bullet(pygame.sprite.Sprite):
    """Bullet fired by the player."""

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((2, 8))
        self.image.fill(constants.WHITE)
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = config.BULLET_SPEED

    def update(self):
        self.rect.y += self.speed
        # Remove the bullet when it leaves the top of the screen
        if self.rect.bottom < 0:
            self.kill()


class Bomb(pygame.sprite.Sprite):
    """Projectile dropped by an alien."""

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((2, 8))
        self.image.fill(constants.RED)
        self.rect = self.image.get_rect(midtop=pos)
        self.speed = config.BOMB_SPEED

    def update(self):
        self.rect.y += self.speed
        # Remove the bomb when it falls below the screen
        if self.rect.top > config.SCREEN_HEIGHT:
            self.kill()
