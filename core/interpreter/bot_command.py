"""
BotCommand class for capturing bot actions into a command queue.
This class is used as the 'bot' object in RestrictedPython scripts.
"""
from typing import List, Dict, Any


class BotCommand:
    """
    Captures bot commands into a command queue for execution.
    
    This class is instantiated and passed to user scripts as the 'bot' object.
    Each method call appends a command to the internal queue.
    """
    
    def __init__(self):
        """Initialize with an empty command queue."""
        self._command_queue: List[Dict[str, Any]] = []
    
    def move(self) -> None:
        """Add a MOVE command to the queue."""
        self._command_queue.append({'action': 'MOVE'})
    
    def turn_left(self) -> None:
        """Add a TURN_LEFT command to the queue."""
        self._command_queue.append({'action': 'TURN_LEFT'})
    
    def turn_right(self) -> None:
        """Add a TURN_RIGHT command to the queue."""
        self._command_queue.append({'action': 'TURN_RIGHT'})
    
    def harvest(self) -> None:
        """Add a HARVEST command to the queue."""
        self._command_queue.append({'action': 'HARVEST'})
    
    def build(self, build_type: str = 'residential') -> None:
        """
        Add a BUILD command to the queue.
        
        Args:
            build_type: Type of building to construct (default: residential)
        """
        self._command_queue.append({'action': 'BUILD', 'type': build_type})
    
    def get_commands(self) -> List[Dict[str, Any]]:
        """
        Return the current command queue.
        
        Returns:
            List of command dictionaries
        """
        return self._command_queue.copy()
    
    def clear_commands(self) -> None:
        """Clear the command queue."""
        self._command_queue = []
    
    def __repr__(self) -> str:
        """String representation showing command count."""
        return f"BotCommand(commands={len(self._command_queue)})"
