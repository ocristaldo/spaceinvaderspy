"""Tests for the game state manager."""
import pytest
from src.systems.game_state_manager import GameStateManager, GameState


class TestGameStateManager:
    """Test suite for GameStateManager class."""
    
    def test_initialization(self):
        """Test that GameStateManager initializes correctly."""
        manager = GameStateManager()
        assert manager.current_state == GameState.MENU
        assert manager.previous_state is None
        
    def test_get_current_state(self):
        """Test getting the current state."""
        manager = GameStateManager()
        assert manager.current_state == GameState.MENU
        
    def test_change_state_valid(self):
        """Test changing to a valid state."""
        manager = GameStateManager()
        manager.change_state(GameState.PLAYING)
        assert manager.current_state == GameState.PLAYING
        assert manager.previous_state == GameState.MENU
        
    def test_change_state_preserves_previous(self):
        """Test that previous state is preserved on multiple changes."""
        manager = GameStateManager()
        manager.change_state(GameState.PLAYING)
        assert manager.previous_state == GameState.MENU
        
        manager.change_state(GameState.PAUSED)
        assert manager.current_state == GameState.PAUSED
        assert manager.previous_state == GameState.PLAYING
        
    def test_change_state_to_same_state(self):
        """Test that changing to the same state does nothing."""
        manager = GameStateManager()
        manager.change_state(GameState.PLAYING)
        assert manager.current_state == GameState.PLAYING
        
        # Try to change to same state
        manager.change_state(GameState.PLAYING)
        assert manager.current_state == GameState.PLAYING
        
    def test_state_data_set_and_get(self):
        """Test setting and getting state data."""
        manager = GameStateManager()
        manager.set_state_data("score", 1000)
        assert manager.get_state_data("score") == 1000
        
    def test_state_data_get_default(self):
        """Test getting state data with default value."""
        manager = GameStateManager()
        assert manager.get_state_data("nonexistent") is None
        assert manager.get_state_data("nonexistent", 42) == 42
        
    def test_state_data_clear(self):
        """Test clearing state data."""
        manager = GameStateManager()
        manager.set_state_data("score", 1000)
        manager.set_state_data("lives", 3)
        
        assert manager.get_state_data("score") == 1000
        assert manager.get_state_data("lives") == 3
        
        manager.clear_state_data()
        assert manager.get_state_data("score") is None
        assert manager.get_state_data("lives") is None
        
    def test_is_playing(self):
        """Test is_playing method."""
        manager = GameStateManager()
        assert not manager.is_playing()
        
        manager.change_state(GameState.PLAYING)
        assert manager.is_playing()
        
        manager.change_state(GameState.PAUSED)
        assert not manager.is_playing()
        
    def test_is_game_over(self):
        """Test is_game_over method."""
        manager = GameStateManager()
        assert not manager.is_game_over()
        
        manager.change_state(GameState.GAME_OVER)
        assert manager.is_game_over()
        
        manager.change_state(GameState.MENU)
        assert not manager.is_game_over()
        
    def test_should_quit(self):
        """Test should_quit method."""
        manager = GameStateManager()
        assert not manager.should_quit()
        
        manager.change_state(GameState.QUIT)
        assert manager.should_quit()
        
    def test_all_states_accessible(self):
        """Test that all defined states are accessible."""
        manager = GameStateManager()
        
        for state in GameState:
            manager.change_state(state)
            assert manager.current_state == state
            
    def test_state_transitions_flow(self):
        """Test typical game state transition flow."""
        manager = GameStateManager()
        
        # Start in menu
        assert manager.current_state == GameState.MENU
        
        # Go to playing
        manager.change_state(GameState.PLAYING)
        assert manager.current_state == GameState.PLAYING
        assert manager.is_playing()
        
        # Pause
        manager.change_state(GameState.PAUSED)
        assert manager.current_state == GameState.PAUSED
        
        # Resume
        manager.change_state(GameState.PLAYING)
        assert manager.current_state == GameState.PLAYING
        
        # Game over
        manager.change_state(GameState.GAME_OVER)
        assert manager.is_game_over()
        
        # Back to menu
        manager.change_state(GameState.MENU)
        assert manager.current_state == GameState.MENU
        
    def test_state_data_isolation(self):
        """Test that state data persists across state changes."""
        manager = GameStateManager()
        
        manager.set_state_data("player_score", 5000)
        manager.change_state(GameState.PLAYING)
        
        # Data should still be there
        assert manager.get_state_data("player_score") == 5000
        
        manager.change_state(GameState.PAUSED)
        # Data should still be there
        assert manager.get_state_data("player_score") == 5000


class TestGameStateEnum:
    """Test suite for GameState enum."""
    
    def test_game_state_enum_values(self):
        """Test that GameState enum has expected values."""
        assert GameState.MENU.value == "menu"
        assert GameState.PLAYING.value == "playing"
        assert GameState.PAUSED.value == "paused"
        assert GameState.GAME_OVER.value == "game_over"
        assert GameState.QUIT.value == "quit"
        
    def test_game_state_enum_members(self):
        """Test that GameState enum has expected members."""
        states = {state.name for state in GameState}
        expected = {"MENU", "PLAYING", "PAUSED", "GAME_OVER", "QUIT"}
        assert states == expected
        
    def test_game_state_enum_comparisons(self):
        """Test enum comparisons."""
        assert GameState.MENU != GameState.PLAYING
        assert GameState.MENU == GameState.MENU
        assert GameState.PLAYING == GameState.PLAYING
