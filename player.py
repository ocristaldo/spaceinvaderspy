import pygame
import constants
import config

class Player(pygame.sprite.Sprite):
    """Ship controlled by the player."""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((22, 16))
        self.image.fill(constants.WHITE)
        self.rect = self.image.get_rect(midbottom=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 20))
        self.speed = 5

    def update(self, pressed):
        if pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        # Keep the player within the screen bounds
        self.rect.clamp_ip(pygame.Rect(0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
