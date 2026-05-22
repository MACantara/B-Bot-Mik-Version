"""
Scope manager for handling variable scopes.
"""
from typing import Dict, Any, List


class ScopeManager:
    """Manages variable scopes for function calls and control structures."""
    
    def __init__(self):
        self.scopes: List[Dict[str, Any]] = [{}]  # Start with global scope
    
    def push_scope(self, scope: Dict[str, Any] = None) -> None:
        """
        Push a new scope onto the stack.
        
        Args:
            scope: Optional initial scope dictionary
        """
        if scope is None:
            scope = {}
        self.scopes.append(scope)
    
    def pop_scope(self) -> Dict[str, Any]:
        """
        Pop the current scope from the stack.
        
        Returns:
            The popped scope dictionary
        """
        return self.scopes.pop()
    
    def get_current_scope(self) -> Dict[str, Any]:
        """
        Get the current (innermost) scope.
        
        Returns:
            Current scope dictionary
        """
        return self.scopes[-1]
    
    def get(self, name: str) -> Any:
        """
        Get a variable value, searching from innermost to outermost scope.
        
        Args:
            name: Variable name
            
        Returns:
            Variable value or None if not found
        """
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None
    
    def set(self, name: str, value: Any) -> None:
        """
        Set a variable in the current scope.
        
        Args:
            name: Variable name
            value: Variable value
        """
        self.scopes[-1][name] = value
    
    def has(self, name: str) -> bool:
        """
        Check if a variable exists in any scope.
        
        Args:
            name: Variable name
            
        Returns:
            True if variable exists
        """
        for scope in reversed(self.scopes):
            if name in scope:
                return True
        return False
    
    def clear(self) -> None:
        """Clear all scopes and reset to global scope."""
        self.scopes = [{}]
