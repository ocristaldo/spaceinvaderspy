"""
Start screen demo scenes used for the intro and attract loop.
"""
from __future__ import annotations

import pygame

from .. import config, constants
from ..utils.sprite_sheet import get_game_sprite, get_title_logo
from .color_scheme import get_tint
from .font_manager import get_font


class ScoreTableDemo:
    """Score-table intro animation shown on startup."""

    def __init__(self, tint_enabled: bool = False, credit_count: int = 0):
        self.title_font = get_font("demo_title")
        self.subtitle_font = get_font("demo_subtitle")
        self.entry_font = get_font("demo_entry")
        self.prompt_font = get_font("demo_prompt")
        self.tint_enabled = tint_enabled
        self.credit_count = credit_count

        center_x = config.BASE_WIDTH // 2
        # Title marquee overlay – adjust width_ratio/height_ratio if you need
        # to reclaim more space for the alien animation.
        self.logo_surface, self.logo_rect = _make_logo_surface(
            config.BASE_WIDTH,
            config.BASE_HEIGHT,
            top_margin=24,
            width_ratio=0.5,
            height_ratio=0.25,
        )
        subtitle_top = (self.logo_rect.bottom + 24) if self.logo_rect else 110
        self.subtitle_top = subtitle_top
        self.subtitle_pos = (center_x - 150, subtitle_top)
        self.credit_pos = (center_x - 80, config.BASE_HEIGHT - 80)
        self.prompt_pos = (center_x, config.BASE_HEIGHT - 40)

        self.table_entries: list[dict] = []
        self._build_table_entries()

        self.entry_delay_ms = 600
        self.entry_drop_duration_ms = 400
        self.entry_drop_distance = 50
        self.hold_duration_ms = 1800
        self.blink_interval_ms = 450

        self.visible_entries = 0
        self.next_entry_time = 0
        self.hold_complete_time = None
        self.running = False
        self.completed = False
        self.entry_states = []
        self.blink_visible = True
        self.next_blink_time = 0
        self.debug_borders = False

    def start(self) -> None:
        now = pygame.time.get_ticks()
        self.visible_entries = 0
        self.entry_states = []
        self.next_entry_time = now + self.entry_delay_ms
        self.hold_complete_time = None
        self.completed = False
        self.running = True
        self.blink_visible = True
        self.next_blink_time = now + self.blink_interval_ms

    def skip(self) -> None:
        self.running = False
        self.completed = True

    def is_running(self) -> bool:
        return self.running

    def is_finished(self) -> bool:
        return self.completed

    def set_debug_borders(self, enabled: bool) -> None:
        self.debug_borders = bool(enabled)

    def set_credit_count(self, count: int) -> None:
        """Update the credit count display."""
        self.credit_count = max(0, int(count))

    def update(self) -> None:
        if not self.running:
            return

        now = pygame.time.get_ticks()
        if self.visible_entries < len(self.table_entries) and now >= self.next_entry_time:
            entry = self.table_entries[self.visible_entries]
            self.entry_states.append({"entry": entry, "start_time": now})
            self.visible_entries += 1
            self.next_entry_time = now + self.entry_delay_ms
            if self.visible_entries == len(self.table_entries):
                self.hold_complete_time = now + self.hold_duration_ms
        elif (
            self.visible_entries == len(self.table_entries)
            and self.hold_complete_time is not None
            and now >= self.hold_complete_time
        ):
            self.running = False
            self.completed = True

        if now >= self.next_blink_time:
            self.blink_visible = not self.blink_visible
            self.next_blink_time = now + self.blink_interval_ms

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(constants.BLACK)
        if self.logo_surface and self.logo_rect:
            surface.blit(self.logo_surface, self.logo_rect)
            if self.debug_borders:
                pygame.draw.rect(surface, constants.GREEN, self.logo_rect, 1)
        surface.blit(
            self.subtitle_font.render("SCORE ADVANCE TABLE", True, (255, 255, 0)),
            self.subtitle_pos,
        )

        now = pygame.time.get_ticks()
        for state in self.entry_states:
            self._draw_entry(surface, state, now)

        credit_text = self.subtitle_font.render(f"CREDIT {self.credit_count:02d}", True, constants.WHITE)
        surface.blit(credit_text, self.credit_pos)

        if self.blink_visible:
            prompt = self.prompt_font.render("Press ENTER or SPACE to continue", True, (200, 200, 200))
            prompt_rect = prompt.get_rect(center=self.prompt_pos)
            surface.blit(prompt, prompt_rect)
            if self.debug_borders:
                pygame.draw.rect(surface, constants.GREEN, prompt_rect, 1)

    def _draw_entry(self, surface: pygame.Surface, state: dict, now: int) -> None:
        entry = state["entry"]
        elapsed = max(0, now - state["start_time"])
        progress = min(1.0, elapsed / self.entry_drop_duration_ms)
        offset = int((1.0 - progress) * self.entry_drop_distance)
        sprite_y = entry["sprite_y"] - offset
        text_y = entry["text_y"] - offset
        surface.blit(entry["sprite"], (entry["sprite_x"], sprite_y))

        # Lazy render text surface if not already done
        if entry["text_surface"] is None and "text" in entry:
            try:
                entry["text_surface"] = self.entry_font.render(entry["text"], True, (200, 200, 200))
            except Exception:
                # Fallback if rendering fails
                entry["text_surface"] = pygame.Surface((100, 16))
                entry["text_surface"].fill((255, 0, 255))

        if entry["text_surface"] is not None:
            surface.blit(entry["text_surface"], (entry["text_x"], text_y))

    def set_tint_enabled(self, enabled: bool) -> None:
        enabled = bool(enabled)
        if self.tint_enabled == enabled:
            return
        self.tint_enabled = enabled
        self._build_table_entries()

    def _build_table_entries(self) -> None:
        center_x = config.BASE_WIDTH // 2
        entry_y = self.subtitle_top + 56
        sprite_x = center_x - 160
        text_x = center_x - 110
        entries = []

        for sprite_name, text in [
            ("ufo", "? = MYSTERY"),
            ("alien_squid_1", "= 30 POINTS"),
            ("alien_crab_1", "= 20 POINTS"),
            ("alien_octopus_1", "= 10 POINTS"),
        ]:
            try:
                sprite = get_game_sprite(sprite_name, config.SPRITE_SCALE, tint=self._sprite_tint(sprite_name))
            except Exception:
                sprite = pygame.Surface((16, 16))
                sprite.fill((255, 0, 255))

            # Try to render text immediately, but store the text for lazy rendering if display not ready
            text_surface = None
            try:
                text_surface = self.entry_font.render(text, True, (200, 200, 200))
            except Exception:
                # Display might not be ready yet - will render on demand
                pass

            entries.append(
                {
                    "sprite": sprite,
                    "sprite_x": sprite_x,
                    "sprite_y": entry_y,
                    "text": text,  # Store the text for lazy rendering if needed
                    "text_surface": text_surface,
                    "text_x": text_x,
                    "text_y": entry_y + sprite.get_height() // 4,
                }
            )
            entry_y += 32
        self.table_entries = entries

    def _sprite_tint(self, sprite_name: str):
        if not self.tint_enabled:
            return None
        if sprite_name.startswith("alien_squid"):
            return get_tint("alien_squid")
        if sprite_name.startswith("alien_crab"):
            return get_tint("alien_crab")
        if sprite_name.startswith("alien_octopus"):
            return get_tint("alien_octopus")
        if sprite_name == "ufo":
            return get_tint("ufo")
        return None


class WaveFormationDemo:
    """Wave-ready mock scene where aliens fall into formation."""

    def __init__(self, tint_enabled: bool = False):
        self.title_font = get_font("demo_subtitle")
        self.info_font = get_font("wave_info")
        self.prompt_font = get_font("demo_prompt")
        self.tint_enabled = tint_enabled

        self.background = pygame.Surface((config.BASE_WIDTH, config.BASE_HEIGHT))
        self._background_dirty = True  # Flag to rebuild on first draw
        self.formation_slots = self._build_formation_slots()

        self.spawn_interval_ms = 110
        self.drop_duration_ms = 450
        self.hold_duration_ms = 2200
        self.blink_interval_ms = 420

        self.active_aliens: list[dict] = []
        self.spawn_index = 0
        self.next_spawn_time = 0
        self.hold_complete_time = None
        self.running = False
        self.completed = False
        self.blink_visible = True
        self.next_blink_time = 0
        self.debug_borders = False

    def start(self) -> None:
        now = pygame.time.get_ticks()
        self.spawn_index = 0
        self.active_aliens = []
        self.next_spawn_time = now + self.spawn_interval_ms
        self.hold_complete_time = None
        self.completed = False
        self.running = True
        self.blink_visible = True
        self.next_blink_time = now + self.blink_interval_ms

    def skip(self) -> None:
        self.running = False
        self.completed = True

    def is_running(self) -> bool:
        return self.running

    def is_finished(self) -> bool:
        return self.completed

    def set_debug_borders(self, enabled: bool) -> None:
        self.debug_borders = bool(enabled)

    def update(self) -> None:
        if not self.running:
            return

        now = pygame.time.get_ticks()

        if self.spawn_index < len(self.formation_slots) and now >= self.next_spawn_time:
            slot = self.formation_slots[self.spawn_index]
            self.active_aliens.append({"slot": slot, "start_time": now})
            self.spawn_index += 1
            self.next_spawn_time = now + self.spawn_interval_ms
            if self.spawn_index == len(self.formation_slots):
                self.hold_complete_time = now + self.hold_duration_ms
        elif (
            self.spawn_index == len(self.formation_slots)
            and self.hold_complete_time is not None
            and now >= self.hold_complete_time
        ):
            self.running = False
            self.completed = True

        if now >= self.next_blink_time:
            self.blink_visible = not self.blink_visible
            self.next_blink_time = now + self.blink_interval_ms

    def draw(self, surface: pygame.Surface) -> None:
        # Build background on first draw (lazy loading to avoid display issues)
        if self._background_dirty:
            self._build_background()
            self._background_dirty = False

        surface.blit(self.background, (0, 0))
        now = pygame.time.get_ticks()
        for state in self.active_aliens:
            self._draw_alien(surface, state, now)
            if self.debug_borders:
                slot = state["slot"]
                rect = pygame.Rect(
                    slot["target_x"],
                    slot["target_y"],
                    slot["sprite"].get_width(),
                    slot["sprite"].get_height(),
                )
                pygame.draw.rect(surface, constants.GREEN, rect, 1)

        if self.blink_visible:
            prompt = self.prompt_font.render("Press ENTER or SPACE to continue", True, (200, 200, 200))
            prompt_rect = prompt.get_rect(center=(config.BASE_WIDTH // 2, config.BASE_HEIGHT - 32))
            surface.blit(prompt, prompt_rect)

    # ----- Helpers -----------------------------------------------------------------
    def _build_background(self) -> None:
        self.background.fill(constants.BLACK)
        center_x = config.BASE_WIDTH // 2
        text_top = 16
        self.background.blit(
            self.info_font.render("SCORE <1>      HI-SCORE      SCORE <2>", True, (180, 180, 180)),
            (40, text_top),
        )
        self.background.blit(
            self.info_font.render("0000              0000              0000", True, constants.WHITE),
            (40, text_top + 20),
        )
        self._draw_bunkers(self.background, config.BASE_HEIGHT - 90)
        self._draw_player(self.background, config.BASE_HEIGHT - 42)
        footer = self.info_font.render("PUSH START BUTTON", True, (200, 200, 200))
        self.background.blit(footer, footer.get_rect(center=(center_x, config.BASE_HEIGHT - 60)))

    def _build_formation_slots(self) -> list[dict]:
        slots: list[dict] = []
        row_types = [
            ("alien_squid_1", config.ALIEN_SPACING_Y),
            ("alien_crab_1", config.ALIEN_SPACING_Y),
            ("alien_crab_1", config.ALIEN_SPACING_Y),
            ("alien_octopus_1", config.ALIEN_SPACING_Y),
            ("alien_octopus_1", config.ALIEN_SPACING_Y),
        ]
        row_sprites = [
            get_game_sprite(name, config.SPRITE_SCALE, tint=self._sprite_tint_for_name(name)) for name, _ in row_types
        ]
        max_width = max(sprite.get_width() for sprite in row_sprites)
        column_gap = config.ALIEN_SPACING_X
        formation_width = config.ALIEN_COLUMNS * max_width + (config.ALIEN_COLUMNS - 1) * column_gap
        start_x = (config.BASE_WIDTH - formation_width) // 2
        y = 120
        for sprite, (_, row_spacing) in zip(row_sprites, row_types):
            width = sprite.get_width()
            offset_within_cell = (max_width - width) // 2
            for col in range(config.ALIEN_COLUMNS):
                slots.append(
                    {
                        "sprite": sprite,
                        "target_x": start_x + col * (max_width + column_gap) + offset_within_cell,
                        "target_y": y,
                        "drop_from": -sprite.get_height() - 40,
                    }
                )
            y += row_spacing
        return slots

    def _draw_alien(self, surface: pygame.Surface, state: dict, now: int) -> None:
        slot = state["slot"]
        elapsed = max(0, now - state["start_time"])
        progress = min(1.0, elapsed / self.drop_duration_ms)
        start_y = slot["drop_from"]
        target_y = slot["target_y"]
        current_y = start_y + (target_y - start_y) * progress
        surface.blit(slot["sprite"], (slot["target_x"], int(current_y)))

    def _draw_bunkers(self, surface: pygame.Surface, bottom_y: int) -> None:
        bunker = get_game_sprite("bunker_full", config.SPRITE_SCALE, tint=self._sprite_tint_for_name("bunker_full"))
        spacing = config.BASE_WIDTH // (constants.BLOCK_NUMBER + 1)
        for i in range(constants.BLOCK_NUMBER):
            x = spacing * (i + 1) - bunker.get_width() // 2
            rect = pygame.Rect(x, bottom_y - bunker.get_height(), bunker.get_width(), bunker.get_height())
            surface.blit(bunker, rect.topleft)

    def _draw_player(self, surface: pygame.Surface, bottom_y: int) -> None:
        player = get_game_sprite("player", config.SPRITE_SCALE, tint=self._sprite_tint_for_name("player"))
        x = (config.BASE_WIDTH - player.get_width()) // 2
        surface.blit(player, (x, bottom_y - player.get_height()))

    def set_tint_enabled(self, enabled: bool) -> None:
        enabled = bool(enabled)
        if self.tint_enabled == enabled:
            return
        self.tint_enabled = enabled
        self._background_dirty = True  # Mark for lazy rebuild
        self.formation_slots = self._build_formation_slots()
        self.active_aliens = []

    def _sprite_tint_for_name(self, sprite_name: str):
        if not self.tint_enabled:
            return None
        if sprite_name.startswith("alien_squid"):
            return get_tint("alien_squid")
        if sprite_name.startswith("alien_crab"):
            return get_tint("alien_crab")
        if sprite_name.startswith("alien_octopus"):
            return get_tint("alien_octopus")
        if sprite_name == "player":
            return get_tint("player")
        if sprite_name == "bunker_full":
            return get_tint("bunker")
        return None


def _make_logo_surface(
    canvas_width: int,
    canvas_height: int,
    top_margin: int = 24,
    width_ratio: float = 0.5,
    height_ratio: float = 0.25,
):
    """
    Create a scaled marquee logo surface centered near the top of the canvas.

    width_ratio / height_ratio describe the maximum portion of the playfield
    the sprite may occupy (e.g. width_ratio=0.55 means clamp to 55% of the
    available width before scaling down). Lower these values if the logo is
    covering too much of the alien animation.
    """
    try:
        raw = get_title_logo(scale=config.SPRITE_SCALE)
    except Exception:
        return None, None
    width, height = raw.get_size()
    max_width = max(1, int(canvas_width * width_ratio))
    max_height = max(1, int(canvas_height * height_ratio))
    scale = min(max_width / width, max_height / height)
    scale = max(scale, 0.1)
    new_size = (
        max(1, int(width * scale)),
        max(1, int(height * scale)),
    )
    surface = pygame.transform.smoothscale(raw, new_size)
    rect = surface.get_rect(midtop=(canvas_width // 2, top_margin))
    return surface, rect
