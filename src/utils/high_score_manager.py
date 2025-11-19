"""
High Score Manager for Space Invaders.

Persists high scores with player initials to disk and provides methods to track and update them.
"""
import json
import logging
import os
from typing import List

logger = logging.getLogger(__name__)


class HighScoreEntry:
    """Represents a single high score entry with initials and player number."""

    def __init__(self, score: int, initials: str = "---", player: int = 1):
        """Initialize a high score entry."""
        self.score = score
        self.initials = initials[:3].upper()  # Limit to 3 characters, uppercase
        self.player = player

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "score": self.score,
            "initials": self.initials,
            "player": self.player
        }

    @staticmethod
    def from_dict(data: dict) -> 'HighScoreEntry':
        """Create from dictionary."""
        return HighScoreEntry(
            score=data.get("score", 0),
            initials=data.get("initials", "---"),
            player=data.get("player", 1)
        )

    def __repr__(self) -> str:
        return f"HighScoreEntry(score={self.score}, initials={self.initials}, player={self.player})"


class HighScoreManager:
    """Manages high score persistence and tracking with player initials."""

    def __init__(self, scores_file="highscores.json"):
        """Initialize the high score manager."""
        self.scores_file = scores_file
        self.high_score = 0
        self.all_scores: List[HighScoreEntry] = []
        self._load_scores()
        logger.info(f"HighScoreManager initialized. Current high score: {self.high_score}")

    def _get_scores_path(self):
        """Get the full path to the high scores file."""
        base_dir = os.path.dirname(__file__)
        root_dir = os.path.dirname(os.path.dirname(base_dir))
        return os.path.join(root_dir, self.scores_file)

    def _load_scores(self):
        """Load scores from disk if the file exists."""
        path = self._get_scores_path()
        try:
            if os.path.exists(path):
                with open(path, "r") as f:
                    data = json.load(f)
                    self.high_score = data.get("high_score", 0)
                    # Load scores as HighScoreEntry objects
                    scores_data = data.get("scores", [])
                    self.all_scores = []
                    for score_data in scores_data:
                        # Handle both old format (just score) and new format (dict with initials)
                        if isinstance(score_data, dict):
                            self.all_scores.append(HighScoreEntry.from_dict(score_data))
                        else:
                            # Old format: just a number
                            self.all_scores.append(HighScoreEntry(score=score_data))
                    logger.info(f"Loaded high score: {self.high_score}")
            else:
                logger.info("No existing high scores file found, starting fresh")
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Failed to load high scores: {e}. Starting fresh.")
            self.high_score = 0
            self.all_scores = []

    def _save_scores(self):
        """Save scores to disk."""
        path = self._get_scores_path()
        try:
            data = {
                "high_score": self.high_score,
                "scores": [entry.to_dict() for entry in self.all_scores],
            }
            with open(path, "w") as f:
                json.dump(data, f, indent=2)
            logger.info(f"Saved high score: {self.high_score}")
        except IOError as e:
            logger.warning(f"Failed to save high scores: {e}")

    def check_high_score(self, score: int) -> bool:
        """Check if a score is a new high score."""
        return score > self.high_score

    def update_score(self, score: int, initials: str = "---", player: int = 1) -> bool:
        """
        Update with a new score entry with initials.

        Args:
            score: The score value
            initials: Player initials (3 characters max)
            player: Player number (1 or 2)

        Returns:
            True if this is a new high score, False otherwise
        """
        entry = HighScoreEntry(score=score, initials=initials, player=player)
        self.all_scores.append(entry)

        # Keep only top 10 scores, sorted by score descending
        self.all_scores = sorted(self.all_scores, key=lambda e: e.score, reverse=True)[:10]

        if score > self.high_score:
            self.high_score = score
            logger.info(f"New high score! {self.high_score} by {initials}")
            self._save_scores()
            return True
        else:
            # Save even non-high scores (for score tracking)
            self._save_scores()
        return False

    def is_high_score_position(self, score: int) -> bool:
        """Check if a score would make the top 10."""
        if len(self.all_scores) < 10:
            return True
        return score > self.all_scores[-1].score

    def get_high_score(self) -> int:
        """Get the current high score value."""
        return self.high_score

    def get_high_score_initials(self) -> str:
        """Get the initials of the current high score holder."""
        if self.all_scores:
            return self.all_scores[0].initials
        return "---"

    def get_top_scores(self, count: int = 10) -> List[HighScoreEntry]:
        """Get the top N score entries."""
        return self.all_scores[:count]

    def reset_scores(self):
        """Reset all scores (mostly for testing)."""
        self.high_score = 0
        self.all_scores = []
        self._save_scores()
        logger.info("High scores reset")
