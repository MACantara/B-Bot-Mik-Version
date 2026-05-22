"""
Data type definitions and utilities for the B-Bot script interpreter.
"""
from typing import List, Any


class BotList:
    """Simple list implementation for B-Bot scripts."""
    
    def __init__(self, items: List[Any] = None):
        """
        Initialize a BotList.
        
        Args:
            items: Initial list of items
        """
        self.items = items if items is not None else []
    
    def append(self, item: Any) -> None:
        """
        Append an item to the list.
        
        Args:
            item: Item to append
        """
        self.items.append(item)
    
    def __len__(self) -> int:
        """Return the length of the list."""
        return len(self.items)
    
    def __getitem__(self, index: int) -> Any:
        """
        Get an item by index.
        
        Args:
            index: Index to retrieve
            
        Returns:
            Item at index
        """
        return self.items[index]
    
    def __setitem__(self, index: int, value: Any) -> None:
        """
        Set an item by index.
        
        Args:
            index: Index to set
            value: Value to set
        """
        self.items[index] = value
    
    def __repr__(self) -> str:
        """Return string representation."""
        return str(self.items)
