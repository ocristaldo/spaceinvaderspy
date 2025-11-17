import pygame
from typing import Optional


class Menu:
    """Minimal Menu helper for displaying a title and options."""

    CONTROL_LINES = [
        "←/→ : Move the cannon",
        "SPACE : Fire (default 1 bullet)",
        "SPACE (after death) : Respawn",
        "A : Toggle audio",
        "P / ESC : Pause / Resume",
        "Q : Quit game",
        "R : Restart (game over) / exit sprite viewer",
        "S + 1..4 : Sprite atlases (Arcade, Atari, Deluxe, Intellivision)",
        "S + 5 : Start-screen reference image",
        "S + 6 : Gameplay reference image",
        "S + 7 : Gameplay (color) reference image",
    ]

    def __init__(self, font: pygame.font.Font):
        self.font = font
        self.options = ["Start", "Controls", "Options", "Quit"]
        self.selected = 0
        self.showing_controls = False

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

        if self.showing_controls:
            self._draw_controls_overlay(surface)

    def _draw_controls_overlay(self, surface: pygame.Surface):
        """Render a translucent overlay describing all key bindings."""
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        surface.blit(overlay, (0, 0))

        w, h = surface.get_size()
        header = self.font.render("Controls & Shortcuts", True, (255, 255, 0))
        surface.blit(header, header.get_rect(center=(w // 2, h // 4)))

        small = pygame.font.SysFont("monospace", 18)
        for idx, line in enumerate(self.CONTROL_LINES):
            text = small.render(line, True, (230, 230, 230))
            surface.blit(text, text.get_rect(center=(w // 2, h // 2 - 40 + idx * 24)))

        hint = small.render("Press ESC or ENTER to return", True, (180, 180, 180))
        surface.blit(hint, hint.get_rect(center=(w // 2, h - 60)))

    def show_controls(self):
        self.showing_controls = True

    def hide_controls(self):
        self.showing_controls = False

    def handle_key(self, key: int) -> Optional[str]:
        """Handle key; return action 'start'|'options'|'quit' when selected."""
        if self.showing_controls:
            if key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                self.hide_controls()
            return None

        if key == pygame.K_UP:
            self.move_up()
            return None
        if key == pygame.K_DOWN:
            self.move_down()
            return None
        if key == pygame.K_RETURN or key == pygame.K_SPACE:
            return self.select()
        return None
