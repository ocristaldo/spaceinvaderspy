"""
Game State Management System.
"""
from enum import Enum
from typing import Optional, Dict, Any
from ..utils.logger import setup_logger


class GameState(Enum):
    """Enumeration of possible game states."""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    QUIT = "quit"


class GameStateManager:
    """Manages game state transitions and data."""
    
    def __init__(self):
        """Initialize the game state manager."""
        self.logger = setup_logger(__name__)
        self._current_state = GameState.MENU
        self._previous_state: Optional[GameState] = None
        self._state_data: Dict[str, Any] = {}
        
    @property
    def current_state(self) -> GameState:
        """Get the current game state."""
        return self._current_state
    
    @property
    def previous_state(self) -> Optional[GameState]:
        """Get the previous game state."""
        return self._previous_state
    
    def change_state(self, new_state: GameState) -> None:
        """Change to a new game state."""
        if new_state == self._current_state:
            self.logger.debug(f"Already in state {new_state.value}")
            return
            
        self.logger.info(f"State change: {self._current_state.value} -> {new_state.value}")
        self._previous_state = self._current_state
        self._current_state = new_state
        
    def set_state_data(self, key: str, value: Any) -> None:
        """Set data for the current state."""
        self._state_data[key] = value
        
    def get_state_data(self, key: str, default: Any = None) -> Any:
        """Get data for the current state."""
        return self._state_data.get(key, default)
        
    def clear_state_data(self) -> None:
        """Clear all state data."""
        self._state_data.clear()
        
    def is_playing(self) -> bool:
        """Check if the game is in playing state."""
        return self._current_state == GameState.PLAYING
        
    def is_game_over(self) -> bool:
        """Check if the game is in game over state."""
        return self._current_state == GameState.GAME_OVER
        
    def should_quit(self) -> bool:
        """Check if the game should quit."""
        return self._current_state == GameState.QUIT
