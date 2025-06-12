#!/usr/bin/env python
"""Simple Space Invaders clone.

This version recreates basic gameplay using pygame. Aliens move as a group
back and forth across the screen and descend when hitting a side. The player
controls a ship at the bottom of the screen and can fire a single bullet at a
time. When all aliens are destroyed the game ends.
"""
import pygame
import random
import constants

# Scale the original arcade resolution to fit modern displays
SCALE = 3
SCREEN_WIDTH = constants.ORIGINAL_WIDTH * SCALE
SCREEN_HEIGHT = constants.ORIGINAL_HEIGHT * SCALE


class Player(pygame.sprite.Sprite):
    """Ship controlled by the player."""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((22, 16))
        self.image.fill(constants.WHITE)
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10))
        self.speed = 5

    def update(self, pressed):
        if pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))


class Alien(pygame.sprite.Sprite):
    """Single alien sprite."""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((16, 12))
        self.image.fill(constants.GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))


class Bullet(pygame.sprite.Sprite):
    """Bullet fired by the player."""

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((2, 8))
        self.image.fill(constants.WHITE)
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = -7

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


class Game:
    """Main game controller."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.running = True

        self.player = Player()
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.bullet_group = pygame.sprite.Group()
        self.alien_group = self.create_aliens()
        self.alien_direction = 1

    def create_aliens(self):
        group = pygame.sprite.Group()
        margin_x = 20
        margin_y = 40
        spacing_x = 40
        spacing_y = 30
        rows = 3
        cols = 6
        for row in range(rows):
            for col in range(cols):
                x = margin_x + col * spacing_x
                y = margin_y + row * spacing_y
                group.add(Alien(x, y))
        return group

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if len(self.bullet_group) == 0:
                    bullet = Bullet(self.player.rect.midtop)
                    self.bullet_group.add(bullet)

    def update(self):
        pressed = pygame.key.get_pressed()
        self.player_group.update(pressed)
        self.bullet_group.update()

        # Move aliens as a group
        move_x = self.alien_direction
        move_down = False
        for alien in self.alien_group.sprites():
            if (alien.rect.right + move_x >= SCREEN_WIDTH) or (alien.rect.left + move_x <= 0):
                move_down = True
                self.alien_direction *= -1
                break
        for alien in self.alien_group.sprites():
            alien.rect.x += move_x
            if move_down:
                alien.rect.y += 10

        # Check collisions
        for bullet in pygame.sprite.groupcollide(self.bullet_group, self.alien_group, True, True):
            pass

        if not self.alien_group:
            self.running = False

    def draw(self):
        self.screen.fill(constants.BLACK)
        self.player_group.draw(self.screen)
        self.alien_group.draw(self.screen)
        self.bullet_group.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()


def main():
    Game().run()


if __name__ == "__main__":
    main()
