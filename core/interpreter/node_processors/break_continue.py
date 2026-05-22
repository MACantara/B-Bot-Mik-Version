"""
Processor for break and continue statements.
"""
import ast
from typing import Dict, Any
from .base import NodeProcessor
from core.interpreter.exceptions import ScriptValidationError


class BreakContinueProcessor(NodeProcessor):
    """Processes break and continue statements."""
    
    def can_process(self, node: ast.AST) -> bool:
        """Check if this is a break or continue node."""
        return isinstance(node, (ast.Break, ast.Continue))
    
    def process(self, node: ast.AST, scope: Dict[str, Any], generator) -> None:
        """
        Process a break or continue statement.
        
        Args:
            node: The AST Break or Continue node
            scope: Current variable scope dictionary
            generator: The command generator instance
        """
        if isinstance(node, ast.Break):
            generator.loop_control = 'break'
        elif isinstance(node, ast.Continue):
            generator.loop_control = 'continue'
