"""
Custom exceptions for the B-Bot script interpreter.
"""
import ast


class ScriptValidationError(Exception):
    """Raised when script validation fails due to security or syntax issues."""
    
    def __init__(self, message: str, node: ast.AST = None, line: int = None):
        """
        Initialize the validation error with optional node context.
        
        Args:
            message: The error message
            node: Optional AST node for line number context
            line: Optional explicit line number
        """
        self.message = message
        self.node = node
        self.line = line
        
        # Build the full error message with context
        if line is not None:
            full_message = f"Line {line}: {message}"
        elif node is not None and hasattr(node, 'lineno'):
            full_message = f"Line {node.lineno}: {message}"
        else:
            full_message = message
        
        super().__init__(full_message)


class SimulationError(Exception):
    """Raised when simulation execution fails."""
    pass
