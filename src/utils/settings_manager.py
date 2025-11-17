"""
Persistent settings manager for SpaceInvadersPy.

Handles loading and saving lightweight configuration such as audio state
and whether the intro demo should run automatically.
"""
import json
import os
from typing import Any, Dict, Optional

from .. import config
from .logger import setup_logger


class SettingsManager:
    """Load and persist simple boolean/toggle options."""

    DEFAULTS = {
        "audio_enabled": False,
        "intro_demo_enabled": True,
        "debug_sprite_borders": False,
    }

    def __init__(self, path: Optional[str] = None):
        base_dir = os.path.dirname(config.BASE_DIR)
        env_path = os.environ.get("SPACEINVADERS_SETTINGS_PATH")
        self.path = path or env_path or os.path.join(base_dir, "settings.json")
        self.logger = setup_logger(__name__)
        self.settings: Dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        """Load settings file, falling back to defaults on errors."""
        data = self.DEFAULTS.copy()
        try:
            if os.path.isfile(self.path):
                with open(self.path, "r", encoding="utf-8") as fh:
                    file_data = json.load(fh)
                    if isinstance(file_data, dict):
                        data.update(file_data)
                    else:
                        self.logger.warning("Settings file malformed, using defaults.")
            else:
                self.logger.debug("Settings file not found; using defaults.")
        except (OSError, json.JSONDecodeError) as exc:
            self.logger.warning("Failed to load settings (%s). Using defaults.", exc)
        self.settings = data

    def _save(self) -> None:
        """Persist settings to disk."""
        try:
            with open(self.path, "w", encoding="utf-8") as fh:
                json.dump(self.settings, fh, indent=2, sort_keys=True)
        except OSError as exc:
            self.logger.warning("Unable to save settings: %s", exc)

    def get_option(self, key: str, default: Optional[Any] = None) -> Any:
        """Return a stored option value."""
        if key in self.settings:
            return self.settings[key]
        return self.DEFAULTS.get(key, default)

    def set_option(self, key: str, value: Any) -> None:
        """Set and persist an option value."""
        if self.settings.get(key) == value:
            return
        self.settings[key] = value
        self._save()

    # Convenience helpers for common options ---------------------------------

    def audio_enabled(self) -> bool:
        return bool(self.get_option("audio_enabled", False))

    def set_audio_enabled(self, enabled: bool) -> None:
        self.set_option("audio_enabled", bool(enabled))

    def intro_demo_enabled(self) -> bool:
        return bool(self.get_option("intro_demo_enabled", True))

    def set_intro_demo_enabled(self, enabled: bool) -> None:
        self.set_option("intro_demo_enabled", bool(enabled))

    def debug_borders_enabled(self) -> bool:
        return bool(self.get_option("debug_sprite_borders", False))

    def set_debug_borders_enabled(self, enabled: bool) -> None:
        self.set_option("debug_sprite_borders", bool(enabled))

    def as_dict(self) -> Dict[str, Any]:
        """Return a shallow copy of the in-memory settings."""
        return dict(self.settings)
