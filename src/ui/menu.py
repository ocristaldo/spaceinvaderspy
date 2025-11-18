import logging
import pygame
from typing import Optional, List, Tuple, Dict
from .. import config
from ..utils.sprite_sheet import get_title_logo
from .font_manager import get_font, get_menu_overlay_fonts

LOGGER = logging.getLogger(__name__)


class Menu:
    """Minimal Menu helper for displaying a title and options."""

    CONTROL_LINES = [
        "<-/-> : Move the cannon",
        "SPACE : Fire (default 1 bullet)",
        "SPACE (after death) : Respawn",
        "A : Toggle sound FX",
        "M : Toggle music",
        "ENTER : Start (uses 1 credit)",
        "C : Insert credit",
        "D : Replay intro demo (menu options)",
        "I : Toggle intro demo autoplay (menu options)",
        "P / ESC : Pause / Resume",
        "Q : Quit game",
        "R : Restart (game over) / exit sprite viewer",
        "S + 1 : Arcade sprite atlas",
        "S + 2 : Start-screen preview",
        "S + 3 : Wave-ready preview",
        "S + 4 : Late-wave preview",
    ]

    OVERLAY_SECTIONS = ("controls", "options", "credits", "high_scores")

    def __init__(self, title_font: Optional[pygame.font.Font] = None, body_font: Optional[pygame.font.Font] = None):
        self.title_font = title_font or get_font("menu_title")
        self.body_font = body_font or get_font("menu_body")
        self._section_fonts: Dict[str, Tuple[pygame.font.Font, pygame.font.Font]] = {}
        for section in self.OVERLAY_SECTIONS:
            try:
                self._section_fonts[section] = get_menu_overlay_fonts(section)
            except KeyError:
                LOGGER.exception("Missing font profile for overlay section '%s'", section)
                self._section_fonts[section] = (self.body_font, self.body_font)
        self.options = ["Start", "High Scores", "Controls", "Options", "Credits", "Quit"]
        self.selected = 0
        self.showing_controls = False
        self.showing_high_scores = False
        self.showing_options = False
        self.showing_credits = False
        self.options_audio_on = False
        self.options_demo_enabled = True
        self.options_tint_enabled = False
        self.options_music_on = False
        self.options_selection = 0
        self.high_scores = []
        self.credits = 0
        self._last_option_rects: List[pygame.Rect] = []
        self._last_title_rect: Optional[pygame.Rect] = None
        self.title_sprite_raw = self._load_title_sprite()
        self._title_cache: Dict[Tuple[int, int], pygame.Surface] = {}
        self.debug_draw_borders = False

    def move_up(self):
        self.selected = (self.selected - 1) % len(self.options)

    def move_down(self):
        self.selected = (self.selected + 1) % len(self.options)

    def select(self) -> str:
        return self.options[self.selected].lower()

    def draw(self, surface: pygame.Surface):
        # Draw a simple centered menu
        w, h = surface.get_size()
        try:
            title_rect = self._draw_logo(surface)
        except Exception:  # pragma: no cover - defensive safety net
            LOGGER.exception("Failed to render title logo; falling back to text layout")
            self.title_sprite_raw = None
            title_rect = self._draw_logo(surface)

        line_height = self.body_font.get_linesize() + 8
        total_height = len(self.options) * line_height
        min_top = title_rect.bottom + 24 if title_rect else int(h * 0.3)
        preferred_start = int((h - total_height) * 0.55)
        max_top = h - total_height - 20
        start_candidate = max(min_top, preferred_start)
        if max_top < start_candidate:
            start_y = max(0, max_top)
        else:
            start_y = start_candidate
        LOGGER.debug(
            "Menu layout: options=%d line_height=%d start_y=%d surface=%sx%s",
            len(self.options),
            line_height,
            start_y,
            w,
            h,
        )
        self._last_option_rects = []
        for i, opt in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (200, 200, 200)
            surf = self.body_font.render(opt, True, color)
            rect = surf.get_rect(center=(w // 2, start_y + i * line_height))
            surface.blit(surf, rect)
            self._last_option_rects.append(rect)
            if self.debug_draw_borders:
                pygame.draw.rect(surface, (255, 0, 255), rect, 1)

        if self.showing_controls:
            self._draw_controls_overlay(surface)
        if self.showing_high_scores:
            self._draw_high_scores_overlay(surface)
        if self.showing_options:
            self._draw_options_overlay(surface)
        if self.showing_credits:
            self._draw_credits_overlay(surface)

    def _draw_controls_overlay(self, surface: pygame.Surface):
        """Render a translucent overlay describing all key bindings."""
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        surface.blit(overlay, (0, 0))

        w, h = surface.get_size()
        header = self.title_font.render("Controls & Shortcuts", True, (255, 255, 0))
        surface.blit(header, header.get_rect(center=(w // 2, int(h * 0.15))))

        overlay_font, overlay_small = self._section_fonts["controls"]
        left_margin = int(w * 0.1)
        top = int(h * 0.25)
        line_spacing = overlay_font.get_linesize() + 4
        for idx, line in enumerate(self.CONTROL_LINES):
            text = overlay_font.render(line, True, (230, 230, 230))
            text_rect = text.get_rect(topleft=(left_margin, top + idx * line_spacing))
            surface.blit(text, text_rect)

        hint = overlay_small.render("Press ESC or ENTER to return", True, (180, 180, 180))
        surface.blit(hint, hint.get_rect(center=(w // 2, h - 50)))

    def show_controls(self):
        self.showing_controls = True

    def show_high_scores(self, scores=None):
        self.showing_high_scores = True
        if scores is not None:
            self.high_scores = scores

    def hide_high_scores(self):
        self.showing_high_scores = False

    def _draw_high_scores_overlay(self, surface: pygame.Surface):
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        surface.blit(overlay, (0, 0))

        w, h = surface.get_size()
        header = self.title_font.render("High Scores", True, (255, 255, 0))
        surface.blit(header, header.get_rect(center=(w // 2, h // 6)))

        font, small = self._section_fonts["high_scores"]
        for idx, score in enumerate(self.high_scores[:10]):
            line = font.render(f"{idx + 1}. {score}", True, (230, 230, 230))
            surface.blit(line, line.get_rect(center=(w // 2, h // 4 + idx * (font.get_linesize() + 4))))

        hint = small.render("Press ESC or ENTER to return", True, (180, 180, 180))
        surface.blit(hint, hint.get_rect(center=(w // 2, h - 60)))

    def show_credits(self):
        """Toggle showing credits overlay."""
        self.showing_credits = True

    def show_options(self):
        # default true; audio state can be passed when opening
        self.showing_options = True

    def update_options_state(
        self,
        audio_on: bool,
        demo_enabled: bool,
        tint_enabled: Optional[bool] = None,
        music_on: Optional[bool] = None,
    ):
        self.options_audio_on = bool(audio_on)
        self.options_demo_enabled = bool(demo_enabled)
        if tint_enabled is not None:
            self.options_tint_enabled = bool(tint_enabled)
        if music_on is not None:
            self.options_music_on = bool(music_on)

    def hide_options(self):
        self.showing_options = False

    def hide_credits(self):
        self.showing_credits = False

    def _draw_credits_overlay(self, surface: pygame.Surface):
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        surface.blit(overlay, (0, 0))

        w, h = surface.get_size()
        header = self.title_font.render("Credits", True, (255, 255, 0))
        surface.blit(header, header.get_rect(center=(w // 2, h // 6)))

        font, small = self._section_fonts["credits"]
        lines = [
            "SpaceInvadersPy",
            "Inspired by the 1978 arcade classic",
            "Developed for educational purposes",
            "Press ESC or ENTER to return",
        ]
        for idx, line in enumerate(lines):
            text = font.render(line, True, (230, 230, 230))
            surface.blit(text, text.get_rect(center=(w // 2, h // 4 + idx * (font.get_linesize() + 4))))

    def _draw_options_overlay(self, surface: pygame.Surface):
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        surface.blit(overlay, (0, 0))

        w, h = surface.get_size()
        header = self.title_font.render("Options", True, (255, 255, 0))
        surface.blit(header, header.get_rect(center=(w // 2, h // 6)))

        font, small = self._section_fonts["options"]
        items = self._option_items()
        start_y = h // 4
        line_height = font.get_linesize() + 6
        for idx, (label, _) in enumerate(items):
            color = (255, 255, 0) if idx == self.options_selection else (230, 230, 230)
            text = font.render(label, True, color)
            rect = text.get_rect(center=(w // 2, start_y + idx * line_height))
            surface.blit(text, rect)

        hint = small.render("Use ^/v + ENTER (ESC to exit)", True, (180, 180, 180))
        surface.blit(hint, hint.get_rect(center=(w // 2, h - 60)))

    def handle_key(self, key: int) -> Optional[str]:
        """Handle key; return action 'start'|'options'|'quit' when selected."""
        if self.showing_controls:
            if key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                self.hide_controls()
            return None

        if self.showing_high_scores:
            if key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                self.hide_high_scores()
            return None

        if self.showing_credits:
            if key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                self.hide_credits()
            return None

        if self.showing_options:
            return self._handle_options_key(key)

        if key == pygame.K_UP:
            self.move_up()
            return None
        if key == pygame.K_DOWN:
            self.move_down()
            return None
        if key == pygame.K_RETURN or key == pygame.K_SPACE:
            return self.select()
        return None

    def set_debug_borders(self, enabled: bool) -> None:
        self.debug_draw_borders = bool(enabled)

    # --- Logo helpers -----------------------------------------------------------
    def _load_title_sprite(self) -> Optional[pygame.Surface]:
        try:
            return get_title_logo(scale=config.SPRITE_SCALE)
        except Exception:
            return None

    def _get_scaled_logo_surface(self, canvas_size: Tuple[int, int]) -> Optional[pygame.Surface]:
        if not self.title_sprite_raw:
            return None
        if canvas_size in self._title_cache:
            return self._title_cache[canvas_size]
        raw = self.title_sprite_raw
        max_width = max(1, int(canvas_size[0] * 0.5))
        max_height = max(1, int(canvas_size[1] * 0.25))
        width, height = raw.get_size()
        scale = min(max_width / width, max_height / height)
        scale = max(scale, 0.1)
        new_size = (
            max(1, int(width * scale)),
            max(1, int(height * scale)),
        )
        scaled = pygame.transform.smoothscale(raw, new_size)
        self._title_cache[canvas_size] = scaled
        return scaled

    def _draw_logo(self, surface: pygame.Surface) -> Optional[pygame.Rect]:
        scaled = self._get_scaled_logo_surface(surface.get_size())
        if not scaled:
            text = self.title_font.render("SpaceInvadersPy", True, (255, 255, 255))
            rect = text.get_rect(center=(surface.get_width() // 2, int(surface.get_height() * 0.18)))
            surface.blit(text, rect)
            if self.debug_draw_borders:
                pygame.draw.rect(surface, (255, 0, 255), rect, 1)
            self._last_title_rect = rect
            return rect
        rect = scaled.get_rect(midtop=(surface.get_width() // 2, int(surface.get_height() * 0.08)))
        rect.top = max(10, rect.top)
        surface.blit(scaled, rect)
        if self.debug_draw_borders:
            pygame.draw.rect(surface, (255, 0, 255), rect, 1)
        self._last_title_rect = rect
        return rect

    def hide_controls(self):
        self.showing_controls = False

    def show_options_with_settings(
        self,
        audio_on: bool,
        demo_enabled: bool,
        debug_borders: Optional[bool] = None,
        tint_enabled: Optional[bool] = None,
        music_enabled: Optional[bool] = None,
    ):
        """Open options overlay and set option state to display."""
        self.update_options_state(audio_on, demo_enabled, tint_enabled, music_enabled)
        if debug_borders is not None:
            self.set_debug_borders(debug_borders)
        self.options_selection = 0
        self.showing_options = True

    # --- Options helpers ---------------------------------------------------------
    def _option_items(self) -> List[Tuple[str, str]]:
        sound_state = "ON" if self.options_audio_on else "OFF"
        demo_state = "ENABLED" if self.options_demo_enabled else "DISABLED"
        border_state = "ON" if self.debug_draw_borders else "OFF"
        tint_state = "ON" if self.options_tint_enabled else "OFF"
        music_state = "ON" if self.options_music_on else "OFF"
        return [
            (f"Sound FX: {sound_state}", "options_toggle_audio"),
            (f"Music: {music_state}", "options_toggle_music"),
            (f"Intro demo autoplay: {demo_state}", "options_toggle_autodemo"),
            (f"Sprite borders: {border_state}", "options_toggle_borders"),
            (f"Sprite tint: {tint_state}", "options_toggle_tint"),
            ("Back", "options_back"),
        ]

    def _handle_options_key(self, key: int) -> Optional[str]:
        items = self._option_items()
        if key == pygame.K_UP:
            self.options_selection = (self.options_selection - 1) % len(items)
            return None
        if key == pygame.K_DOWN:
            self.options_selection = (self.options_selection + 1) % len(items)
            return None
        if key in (pygame.K_RETURN, pygame.K_SPACE):
            action = items[self.options_selection][1]
            if action == "options_back":
                self.hide_options()
            return action
        if key == pygame.K_ESCAPE:
            self.hide_options()
            return "options_back"
        if key == pygame.K_a:
            return "options_toggle_audio"
        if key == pygame.K_d:
            return "options_play_demo"
        if key == pygame.K_i:
            return "options_toggle_autodemo"
        if key == pygame.K_b:
            return "options_toggle_borders"
        if key == pygame.K_t:
            return "options_toggle_tint"
        if key == pygame.K_m:
            return "options_toggle_music"
        return None
