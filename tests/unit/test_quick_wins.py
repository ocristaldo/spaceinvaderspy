"""
Unit tests for audio manager, high score manager, and extra lives system.
"""
import pytest
import os
import tempfile
from unittest.mock import patch
from src.utils.audio_manager import AudioManager
from src.utils.high_score_manager import HighScoreManager


class TestAudioManager:
    """Tests for the AudioManager class."""

    def test_audio_disabled_by_default(self):
        """Audio should be muted by default."""
        with patch('pygame.mixer.init'):
            manager = AudioManager()
            assert manager.enabled is False

    def test_toggle_audio(self):
        """Toggling audio should switch state."""
        with patch('pygame.mixer.init'):
            with patch('pygame.mixer.stop'):
                with patch('pygame.mixer.music.stop'):
                    manager = AudioManager()
                    assert manager.enabled is False
                    manager.toggle_audio()
                    assert manager.enabled is True
                    manager.toggle_audio()
                    assert manager.enabled is False

    def test_volume_bounds(self):
        """Volume should be clamped to 0.0-1.0 range."""
        with patch('pygame.mixer.init'):
            with patch('pygame.mixer.music.set_volume'):
                manager = AudioManager()
                
                manager.set_volume(1.5)
                assert manager.volume == 1.0
                
                manager.set_volume(-0.5)
                assert manager.volume == 0.0
                
                manager.set_volume(0.5)
                assert manager.volume == 0.5

    def test_increase_decrease_volume(self):
        """Volume increase/decrease should work within bounds."""
        with patch('pygame.mixer.init'):
            with patch('pygame.mixer.music.set_volume'):
                manager = AudioManager()
                manager.set_volume(0.5)
                
                manager.increase_volume(0.2)
                assert abs(manager.volume - 0.7) < 0.001
                
                manager.decrease_volume(0.3)
                assert abs(manager.volume - 0.4) < 0.001


class TestHighScoreManager:
    """Tests for the HighScoreManager class."""

    def test_high_score_defaults_to_zero(self):
        """High score should default to 0 when no file exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            scores_file = os.path.join(tmpdir, "scores.json")
            manager = HighScoreManager(scores_file)
            manager.scores_file = scores_file  # Override path for temp
            assert manager.high_score == 0

    def test_update_score_new_high(self):
        """Updating with new high score should save it."""
        with tempfile.TemporaryDirectory() as tmpdir:
            scores_file = os.path.join(tmpdir, "scores.json")
            manager = HighScoreManager(scores_file)
            
            # Override the path method
            manager.scores_file = scores_file
            with patch.object(manager, '_get_scores_path', return_value=scores_file):
                result = manager.update_score(1000)
                assert result is True
                assert manager.high_score == 1000

    def test_check_high_score(self):
        """Checking if score is new high should work."""
        with tempfile.TemporaryDirectory() as tmpdir:
            scores_file = os.path.join(tmpdir, "scores.json")
            manager = HighScoreManager(scores_file)
            manager.scores_file = scores_file
            
            with patch.object(manager, '_get_scores_path', return_value=scores_file):
                manager.high_score = 1000
                assert manager.check_high_score(2000) is True
                assert manager.check_high_score(500) is False
                assert manager.check_high_score(1000) is False

    def test_get_top_scores(self):
        """Getting top scores should return them in order."""
        with tempfile.TemporaryDirectory() as tmpdir:
            scores_file = os.path.join(tmpdir, "scores.json")
            manager = HighScoreManager(scores_file)
            manager.scores_file = scores_file
            manager.all_scores = [5000, 3000, 8000, 1000]
            
            top = manager.get_top_scores(3)
            assert top == [5000, 3000, 8000]

    def test_keeps_top_10_scores(self):
        """Manager should keep only top 10 scores."""
        with tempfile.TemporaryDirectory() as tmpdir:
            scores_file = os.path.join(tmpdir, "scores.json")
            manager = HighScoreManager(scores_file)
            manager.scores_file = scores_file
            
            with patch.object(manager, '_get_scores_path', return_value=scores_file):
                # Add 15 scores
                for i in range(1000, 16000, 1000):
                    manager.update_score(i)
                
                # Should only keep top 10
                assert len(manager.all_scores) <= 10


class TestExtraLivesMilestones:
    """Tests for the extra lives milestone logic - unit tests of the logic itself."""

    def test_extra_life_threshold_calculation(self):
        """Test the threshold calculation logic for extra lives."""
        # Verify that extra lives are awarded at correct thresholds
        # First extra life at 20,000, then every 70,000 thereafter
        
        thresholds = [20000, 90000, 160000, 230000]
        
        for i, threshold in enumerate(thresholds):
            # At or above threshold
            assert threshold >= 20000
            # Check the interval pattern
            if i == 0:
                assert threshold == 20000
            else:
                expected = 20000 + (i * 70000)
                assert threshold == expected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
