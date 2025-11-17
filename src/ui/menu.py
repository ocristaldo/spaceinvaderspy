import pygame
from typing import Optional


class Menu:
    """Minimal Menu helper for displaying a title and options."""

    def __init__(self, font: pygame.font.Font):
        self.font = font
        self.options = ["Start", "Options", "Quit"]
        self.selected = 0

    def move_up(self):
        self.selected = (self.selected - 1) % len(self.options)

    def move_down(self):
        self.selected = (self.selected + 1) % len(self.options)

    def select(self) -> str:
        return self.options[self.selected].lower()

    def draw(self, surface: pygame.Surface):
        # Draw a simple centered menu
        w, h = surface.get_size()
        title_surf = self.font.render("SpaceInvadersPy", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(w // 2, h // 4))
        surface.blit(title_surf, title_rect)

        for i, opt in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (200, 200, 200)
            surf = self.font.render(opt, True, color)
            rect = surf.get_rect(center=(w // 2, h // 2 + i * 30))
            surface.blit(surf, rect)

    def handle_key(self, key: int) -> Optional[str]:
        """Handle key; return action 'start'|'options'|'quit' when selected."""
        if key == pygame.K_UP:
            self.move_up()
            return None
        if key == pygame.K_DOWN:
            self.move_down()
            return None
        if key == pygame.K_RETURN or key == pygame.K_SPACE:
            return self.select()
        return None
