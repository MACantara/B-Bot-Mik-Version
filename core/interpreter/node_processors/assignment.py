"""
Processor for assignment nodes.
"""
import ast
from typing import Dict, Any
from .base import NodeProcessor
from core.interpreter.exceptions import ScriptValidationError
from core.interpreter.evaluator import ExpressionEvaluator


class AssignmentProcessor(NodeProcessor):
    """Processes variable assignment nodes."""
    
    def __init__(self):
        self.evaluator = ExpressionEvaluator()
    
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
            
            # Use expression evaluator to evaluate the right-hand side
            try:
                value = self.evaluator.evaluate(assign_node.value, scope)
                
                # Type validation - support int, bool, and list
                from core.interpreter.data_types import BotList
                if not isinstance(value, (int, bool, BotList)):
                    raise ScriptValidationError(
                        f"Unsupported type for assignment: {type(value).__name__}",
                        node=assign_node
                    )
                
                scope[var_name] = value
            except ScriptValidationError:
                raise
            except Exception as e:
                raise ScriptValidationError(f"Failed to evaluate assignment: {e}", node=assign_node)
