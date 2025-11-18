"""
Audio Manager for Space Invaders.

Handles all sound effects and music, with support for toggling audio on/off
and volume control. Audio is muted by default.
"""
import os
import logging
import pygame

logger = logging.getLogger(__name__)


class AudioManager:
    """Manages all game audio - SFX and background music."""

    def __init__(self):
        """Initialize the audio manager with muted audio by default."""
        self.available = False
        self.sfx_enabled = False
        self.music_enabled = False
        self.volume = 0.7
        self.music_volume = 0.5
        self.sounds = {}
        self.music_track = "spaceinvaders1.mpeg"
        self._ufo_channel = None
        if self._initialize_mixer():
            self.available = True
            self._load_sounds()
            logger.info("AudioManager initialized (muted by default)")
        else:
            logger.warning("Audio subsystem unavailable; running muted.")

    def _initialize_mixer(self) -> bool:
        """Attempt to initialize pygame.mixer if not already active."""
        if pygame.mixer.get_init():
            return True
        try:
            pygame.mixer.init()
            return True
        except pygame.error as exc:
            logger.warning("Unable to initialize audio: %s", exc)
            return False

    def _get_sound_path(self, filename):
        """Construct the full path to a sound file."""
        base_dir = os.path.dirname(__file__)
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(base_dir)), "assets")
        sound_dir = os.path.join(assets_dir, "sounds")
        return os.path.join(sound_dir, filename)

    def _load_sounds(self):
        """Load all sound effects. Missing files are logged but don't crash the game."""
        sound_files = {
            "shoot": "shoot.wav",
            "explosion": "explosion.wav",
            "invaderkilled": "invaderkilled.wav",
            "fastinvader1": "fastinvader1.wav",
            "fastinvader2": "fastinvader2.wav",
            "fastinvader3": "fastinvader3.wav",
            "fastinvader4": "fastinvader4.wav",
            "ufo_lowpitch": "ufo_lowpitch.wav",
            "ufo_highpitch": "ufo_highpitch.wav",
        }

        for key, filename in sound_files.items():
            path = self._get_sound_path(filename)
            try:
                if os.path.exists(path):
                    self.sounds[key] = pygame.mixer.Sound(path)
                    logger.debug(f"Loaded sound: {key}")
                else:
                    logger.warning(f"Sound file not found: {path}")
            except pygame.error as e:
                logger.warning(f"Failed to load sound {key}: {e}")

    def play_sound(self, key):
        """Play a sound effect if audio is enabled and the sound exists."""
        if not self.available or not self.sfx_enabled or key not in self.sounds:
            return
        
        try:
            sound = self.sounds[key]
            sound.set_volume(self.volume)
            sound.play()
            logger.debug(f"Playing sound: {key}")
        except pygame.error as e:
            logger.warning(f"Failed to play sound {key}: {e}")

    def toggle_audio(self):
        """Backward-compatible toggle for sound effects."""
        self.set_sfx_enabled(not self.sfx_enabled)

    def set_volume(self, volume):
        """Set master volume (0.0 to 1.0)."""
        if not self.available:
            return
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)
        logger.info(f"Volume set to {self.volume * 100:.0f}%")

    def increase_volume(self, step=0.1):
        """Increase volume by step amount."""
        self.set_volume(self.volume + step)

    def decrease_volume(self, step=0.1):
        """Decrease volume by step amount."""
        self.set_volume(self.volume - step)

    def stop_all(self):
        """Stop all sounds and music."""
        if self.available:
            pygame.mixer.stop()
            pygame.mixer.music.stop()
            self._ufo_channel = None
            logger.info("All audio stopped")

    def cleanup(self):
        """Clean up audio resources."""
        if self.available:
            pygame.mixer.stop()
            pygame.mixer.music.stop()
            logger.info("Audio cleanup complete")

    # --- Extended controls ----------------------------------------------------

    def set_sfx_enabled(self, enabled: bool) -> None:
        """Enable/disable all sound effects."""
        if enabled and not self.available:
            if not self._initialize_mixer():
                logger.info("Unable to enable SFX; mixer unavailable.")
                return
            self.available = True
            if not self.sounds:
                self._load_sounds()
        self.sfx_enabled = bool(enabled)
        if not self.sfx_enabled and self.available:
            pygame.mixer.stop()
            self._ufo_channel = None
        logger.info("Sound FX %s", "enabled" if self.sfx_enabled else "disabled")

    def set_music_enabled(self, enabled: bool) -> None:
        """Enable/disable menu/attract background music."""
        if enabled and not self.available:
            if not self._initialize_mixer():
                logger.info("Unable to enable music; mixer unavailable.")
                return
            self.available = True
        self.music_enabled = bool(enabled)
        if not self.music_enabled:
            self.stop_music()
        logger.info("Menu music %s", "enabled" if self.music_enabled else "disabled")

    def play_menu_music(self) -> None:
        """Start looping the menu/attract music if available."""
        if not (self.available and self.music_enabled):
            return
        path = self._get_sound_path(self.music_track)
        try:
            if os.path.exists(path):
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load(path)
                    pygame.mixer.music.set_volume(self.music_volume)
                    pygame.mixer.music.play(-1)
            else:
                logger.warning("Music file not found: %s", path)
        except pygame.error as exc:
            logger.warning("Failed to start music: %s", exc)

    def stop_music(self) -> None:
        if self.available:
            pygame.mixer.music.stop()

    def is_music_playing(self) -> bool:
        return self.available and pygame.mixer.music.get_busy()

    def play_fast_invader(self, step: int) -> None:
        key = f"fastinvader{step + 1}"
        self.play_sound(key)

    def start_ufo_loop(self) -> None:
        if not self.available or not self.sfx_enabled:
            return
        sound = self.sounds.get("ufo_lowpitch")
        if not sound:
            return
        if self._ufo_channel and self._ufo_channel.get_busy():
            return
        self._ufo_channel = sound.play(-1)

    def stop_ufo_loop(self) -> None:
        if self._ufo_channel:
            self._ufo_channel.stop()
            self._ufo_channel = None
