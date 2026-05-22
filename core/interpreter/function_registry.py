"""
Function registry for storing user-defined functions.
"""
from typing import Dict, List, Any, Optional
import ast


class FunctionRegistry:
    """Registry for storing user-defined function definitions."""
    
    def __init__(self):
        self.functions: Dict[str, Dict[str, Any]] = {}
    
    def register(self, name: str, params: List[str], body: List[ast.AST]) -> None:
        """
        Register a function definition.
        
        Args:
            name: Function name
            params: List of parameter names
            body: List of AST nodes representing the function body
        """
        self.functions[name] = {
            'params': params,
            'body': body
        }
    
    def get(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a function definition by name.
        
        Args:
            name: Function name
            
        Returns:
            Function definition dict or None if not found
        """
        return self.functions.get(name)
    
    def has(self, name: str) -> bool:
        """
        Check if a function is registered.
        
        Args:
            name: Function name
            
        Returns:
            True if function exists
        """
        return name in self.functions
    
    def clear(self) -> None:
        """Clear all registered functions."""
        self.functions.clear()
