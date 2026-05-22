"""
Processor for assignment nodes.
"""
import ast
from typing import Dict, Any
from .base import NodeProcessor
from core.interpreter.exceptions import ScriptValidationError


class AssignmentProcessor(NodeProcessor):
    """Processes variable assignment nodes."""
    
    def can_process(self, node: ast.AST) -> bool:
        """Check if this is an assignment node."""
        return isinstance(node, ast.Assign)
    
    def process(self, node: ast.AST, scope: Dict[str, Any], generator) -> None:
        """
        Process a variable assignment.
        
        Args:
            node: The AST Assign node
            scope: Current variable scope dictionary
            generator: The command generator instance
        """
        assign_node = node
        
        if isinstance(assign_node.targets[0], ast.Name):
            var_name = assign_node.targets[0].id
            
            # Only support constant integer assignments for now
            if isinstance(assign_node.value, ast.Constant) and isinstance(assign_node.value.value, int):
                scope[var_name] = assign_node.value.value
            else:
                raise ScriptValidationError("Only constant integer assignments are supported")
