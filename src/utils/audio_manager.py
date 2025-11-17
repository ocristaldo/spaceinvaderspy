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
        self.enabled = False  # Muted by default
        self.volume = 0.7  # 70% volume
        self.sounds = {}
        self.music = None
        self.available = False
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
            "capture": "capture.wav",
            "ufo": "ufo.wav",
            "extra_life": "extra_life.wav",
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

    def load_music(self, filename):
        """Load background music. Logs warnings if file is missing or fails."""
        path = self._get_sound_path(filename)
        try:
            if os.path.exists(path):
                pygame.mixer.music.load(path)
                self.music = filename
                logger.debug(f"Loaded music: {filename}")
                if self.enabled:
                    pygame.mixer.music.play(-1)  # -1 = loop indefinitely
            else:
                logger.warning(f"Music file not found: {path}")
        except pygame.error as e:
            logger.warning(f"Failed to load music {filename}: {e}")

    def play_sound(self, key):
        """Play a sound effect if audio is enabled and the sound exists."""
        if not self.available or not self.enabled or key not in self.sounds:
            return
        
        try:
            sound = self.sounds[key]
            sound.set_volume(self.volume)
            sound.play()
            logger.debug(f"Playing sound: {key}")
        except pygame.error as e:
            logger.warning(f"Failed to play sound {key}: {e}")

    def toggle_audio(self):
        """Toggle audio on/off."""
        if not self.available:
            if not self._initialize_mixer():
                logger.info("Audio toggle ignored; mixer still unavailable.")
                return
            self.available = True
            if not self.sounds:
                self._load_sounds()
        self.enabled = not self.enabled
        status = "enabled" if self.enabled else "disabled"
        logger.info(f"Audio toggled: {status}")

        if self.enabled:
            # Resume music if it was loaded
            if self.music and not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)
        else:
            # Stop all sounds and music
            pygame.mixer.stop()
            pygame.mixer.music.stop()

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
            logger.info("All audio stopped")

    def cleanup(self):
        """Clean up audio resources."""
        if self.available:
            pygame.mixer.stop()
            pygame.mixer.music.stop()
            logger.info("Audio cleanup complete")
