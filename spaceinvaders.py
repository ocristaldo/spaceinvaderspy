#!/usr/bin/env python
"""Enhanced Space Invaders clone.

This version adds bunkers, alien bombs, a UFO, scoring and lives to more
closely mirror the original arcade game. Gameplay remains simple: aliens
move in formation, the player fires one bullet at a time and the game ends
if aliens reach the bottom or the player loses all lives.
"""
import pygame
import random
import constants
import config
from player import Player
from alien import Alien
from bullet import Bullet, Bomb
from bunker import Bunker
from ufo import UFO

SCREEN_WIDTH = config.SCREEN_WIDTH
SCREEN_HEIGHT = config.SCREEN_HEIGHT


class Game:
    """Main game controller."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 16)
        self.running = True
        self.game_over = False

        self.score = 0
        self.lives = constants.LIVES_NUMBER

        self.player = Player()
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.bullet_group = pygame.sprite.Group()
        self.bomb_group = pygame.sprite.Group()
        self.bunker_group = self.create_bunkers()
        self.ufo_group = pygame.sprite.Group()

        self.alien_group = self.create_aliens()
        self.alien_direction = 1
        self.last_ufo_time = pygame.time.get_ticks()

    def create_aliens(self):
        group = pygame.sprite.Group()
        margin_x = config.ALIEN_MARGIN_X
        margin_y = config.ALIEN_MARGIN_Y
        spacing_x = config.ALIEN_SPACING_X
        spacing_y = config.ALIEN_SPACING_Y
        rows = config.ALIEN_ROWS
        cols = config.ALIEN_COLUMNS
        values = [30, 20, 10]
        for row in range(rows):
            for col in range(cols):
                x = margin_x + col * spacing_x
                y = margin_y + row * spacing_y
                group.add(Alien(x, y, values[row]))
        return group

    def create_bunkers(self):
        group = pygame.sprite.Group()
        spacing = SCREEN_WIDTH // (constants.BLOCK_NUMBER + 1)
        y = SCREEN_HEIGHT - 60
        for i in range(constants.BLOCK_NUMBER):
            x = spacing * (i + 1)
            group.add(Bunker((x, y)))
        return group

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(self.bullet_group) == 0:
                    bullet = Bullet(self.player.rect.midtop)
                    self.bullet_group.add(bullet)
                if event.key == pygame.K_r and self.game_over:
                    self.__init__()

    def spawn_bomb(self):
        if not self.alien_group:
            return
        if random.random() < 0.02:
            alien = random.choice(self.alien_group.sprites())
            bomb = Bomb(alien.rect.midbottom)
            self.bomb_group.add(bomb)

    def spawn_ufo(self):
        now = pygame.time.get_ticks()
        if now - self.last_ufo_time > config.UFO_INTERVAL:
            self.ufo_group.add(UFO())
            self.last_ufo_time = now

    def update(self):
        pressed = pygame.key.get_pressed()
        self.player_group.update(pressed)
        self.bullet_group.update()
        self.bomb_group.update()
        self.ufo_group.update()

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
                if alien.rect.bottom >= SCREEN_HEIGHT - 40:
                    self.game_over = True

        self.spawn_bomb()
        self.spawn_ufo()

        # Collisions
        hits = pygame.sprite.groupcollide(self.bullet_group, self.alien_group, True, True)
        for bullet, aliens in hits.items():
            for alien in aliens:
                self.score += alien.value

        hits = pygame.sprite.groupcollide(self.bullet_group, self.ufo_group, True, True)
        for bullet, ufos in hits.items():
            for ufo in ufos:
                self.score += ufo.value
        # bullet vs bunker
        hits = pygame.sprite.groupcollide(self.bullet_group, self.bunker_group, True, False)
        for bunker_list in hits.values():
            for bunker in bunker_list:
                bunker.damage()
        # bomb vs bunker
        hits = pygame.sprite.groupcollide(self.bomb_group, self.bunker_group, True, False)
        for bunker_list in hits.values():
            for bunker in bunker_list:
                bunker.damage()
        # bomb vs player
        if pygame.sprite.spritecollide(self.player, self.bomb_group, True):
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
        if not self.alien_group:
            self.game_over = True
        if self.game_over:
            self.running = False

    def draw(self):
        self.screen.fill(constants.BLACK)
        self.player_group.draw(self.screen)
        self.alien_group.draw(self.screen)
        self.bunker_group.draw(self.screen)
        self.bullet_group.draw(self.screen)
        self.bomb_group.draw(self.screen)
        self.ufo_group.draw(self.screen)

        score_surf = self.font.render(f"Score: {self.score}", True, constants.WHITE)
        lives_surf = self.font.render(f"Lives: {self.lives}", True, constants.WHITE)
        self.screen.blit(score_surf, (10, 5))
        self.screen.blit(lives_surf, (SCREEN_WIDTH - lives_surf.get_width() - 10, 5))
        pygame.display.flip()

    def game_over_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    return True
            self.screen.fill(constants.BLACK)
            msg = self.font.render("GAME OVER - press R", True, constants.WHITE)
            rect = msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(msg, rect)
            pygame.display.flip()
            self.clock.tick(60)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        again = self.game_over_screen() if self.game_over else False
        pygame.quit()
        if again:
            self.__init__()
            self.run()


def main():
    Game().run()


if __name__ == "__main__":
    main()
