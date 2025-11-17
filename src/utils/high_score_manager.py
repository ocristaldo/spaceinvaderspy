"""
High Score Manager for Space Invaders.

Persists the high score to disk and provides methods to track and update it.
"""
import os
import json
import logging

logger = logging.getLogger(__name__)


class HighScoreManager:
    """Manages high score persistence and tracking."""

    def __init__(self, scores_file="highscores.json"):
        """Initialize the high score manager."""
        self.scores_file = scores_file
        self.high_score = 0
        self.all_scores = []
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
                    self.all_scores = data.get("scores", [])
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
                "scores": self.all_scores,
            }
            with open(path, "w") as f:
                json.dump(data, f, indent=2)
            logger.info(f"Saved high score: {self.high_score}")
        except IOError as e:
            logger.warning(f"Failed to save high scores: {e}")

    def check_high_score(self, score):
        """Check if a score is a new high score."""
        if score > self.high_score:
            return True
        return False

    def update_score(self, score):
        """Update with a new score, saving if it's a new high score."""
        self.all_scores.append(score)
        # Keep only top 10 scores
        self.all_scores = sorted(self.all_scores, reverse=True)[:10]

        if score > self.high_score:
            self.high_score = score
            logger.info(f"New high score! {self.high_score}")
            self._save_scores()
            return True
        return False

    def get_high_score(self):
        """Get the current high score."""
        return self.high_score

    def get_top_scores(self, count=10):
        """Get the top N scores."""
        return self.all_scores[:count]

    def reset_scores(self):
        """Reset all scores (mostly for testing)."""
        self.high_score = 0
        self.all_scores = []
        self._save_scores()
        logger.info("High scores reset")
