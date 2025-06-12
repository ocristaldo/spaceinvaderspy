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

# Scale the original arcade resolution for modern displays
SCALE = 3
SCREEN_WIDTH = constants.ORIGINAL_WIDTH * SCALE
SCREEN_HEIGHT = constants.ORIGINAL_HEIGHT * SCALE


class Player(pygame.sprite.Sprite):
    """Ship controlled by the player."""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((22, 16))
        self.image.fill(constants.WHITE)
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        self.speed = 5

    def update(self, pressed):
        if pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))


class Alien(pygame.sprite.Sprite):
    """Single alien sprite."""

    def __init__(self, x, y, value):
        super().__init__()
        self.image = pygame.Surface((16, 12))
        self.image.fill(constants.GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.value = value


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


class Bomb(pygame.sprite.Sprite):
    """Projectile dropped by an alien."""

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((2, 8))
        self.image.fill(constants.RED)
        self.rect = self.image.get_rect(midtop=pos)
        self.speed = 4

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


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
        if self.rect.left > SCREEN_WIDTH:
            self.kill()


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
        margin_x = 20
        margin_y = 40
        spacing_x = 40
        spacing_y = 30
        rows = 3
        cols = 6
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
        if now - self.last_ufo_time > 25000:
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
