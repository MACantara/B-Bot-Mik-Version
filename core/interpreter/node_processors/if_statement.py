"""
Processor for if/else statement nodes.
"""
import ast
from typing import Dict, Any
from .base import NodeProcessor
from core.interpreter.exceptions import ScriptValidationError
from core.interpreter.evaluator import ExpressionEvaluator


class IfStatementProcessor(NodeProcessor):
    """Processes if/else statement nodes."""
    
    def __init__(self):
        self.evaluator = ExpressionEvaluator()
    
    def can_process(self, node: ast.AST) -> bool:
        """Check if this is an if statement node."""
        return isinstance(node, ast.If)
    
    def process(self, node: ast.AST, scope: Dict[str, Any], generator) -> None:
        """
        Process an if/else statement.
        
        Args:
            node: The AST If node
            scope: Current variable scope dictionary
            generator: The command generator instance
        """
        if_node = node
        
        # Evaluate the condition
        condition = self.evaluator.evaluate(if_node.test, scope)
        
        # Process the appropriate branch
        if condition:
            # Condition is True, process the if body
            for body_node in if_node.body:
                generator._process_node(body_node, scope)
        else:
            # Condition is False, process the else body if it exists
            if if_node.orelse:
                for orelse_node in if_node.orelse:
                    generator._process_node(orelse_node, scope)
