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
    """Load and persist simple boolean/toggle options with schema validation."""

    DEFAULTS = {
        "audio_enabled": False,  # Sound effects
        "music_enabled": False,
        "intro_demo_enabled": True,
        "debug_sprite_borders": False,
        "tint_enabled": False,
    }

    # Schema: key -> (type, description)
    SCHEMA = {
        "audio_enabled": (bool, "Enable sound effects"),
        "music_enabled": (bool, "Enable background music"),
        "intro_demo_enabled": (bool, "Auto-play intro demo on menu"),
        "debug_sprite_borders": (bool, "Draw borders around sprites (debug)"),
        "tint_enabled": (bool, "Apply color tints to sprites"),
    }

    def __init__(self, path: Optional[str] = None):
        base_dir = os.path.dirname(config.BASE_DIR)
        env_path = os.environ.get("SPACEINVADERS_SETTINGS_PATH")
        self.path = path or env_path or os.path.join(base_dir, "settings.json")
        self.logger = setup_logger(__name__)
        self.settings: Dict[str, Any] = {}
        self._load()

    def _validate_setting(self, key: str, value: Any) -> bool:
        """Validate a single setting against schema. Returns True if valid."""
        if key not in self.SCHEMA:
            self.logger.warning("Unknown setting key: %s (ignoring)", key)
            return False
        expected_type, description = self.SCHEMA[key]
        if not isinstance(value, expected_type):
            self.logger.warning(
                "Setting '%s' has invalid type %s (expected %s). Ignoring.",
                key,
                type(value).__name__,
                expected_type.__name__,
            )
            return False
        return True

    def _validate_settings(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate all settings, return cleaned dict with only valid entries."""
        validated = {}
        for key, value in data.items():
            if self._validate_setting(key, value):
                validated[key] = value
        return validated

    def _load(self) -> None:
        """Load settings file, falling back to defaults on errors."""
        data = self.DEFAULTS.copy()
        try:
            if os.path.isfile(self.path):
                with open(self.path, "r", encoding="utf-8") as fh:
                    file_data = json.load(fh)
                    if isinstance(file_data, dict):
                        # Validate loaded settings
                        validated_data = self._validate_settings(file_data)
                        data.update(validated_data)
                        if len(validated_data) < len(file_data):
                            self.logger.info(
                                "Settings file had invalid entries; using defaults for them."
                            )
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

    def tint_enabled(self) -> bool:
        return bool(self.get_option("tint_enabled", False))

    def set_tint_enabled(self, enabled: bool) -> None:
        self.set_option("tint_enabled", bool(enabled))

    def music_enabled(self) -> bool:
        return bool(self.get_option("music_enabled", False))

    def set_music_enabled(self, enabled: bool) -> None:
        self.set_option("music_enabled", bool(enabled))

    def as_dict(self) -> Dict[str, Any]:
        """Return a shallow copy of the in-memory settings."""
        return dict(self.settings)
