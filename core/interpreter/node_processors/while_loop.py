"""
Processor for while loop nodes.
"""
import ast
from typing import Dict, Any
from .base import NodeProcessor
from core.interpreter.exceptions import ScriptValidationError
from core.interpreter.evaluator import ExpressionEvaluator
from core.interpreter.config import MAX_ITERATIONS


class WhileLoopProcessor(NodeProcessor):
    """Processes while loop nodes and unrolls them."""
    
    def __init__(self):
        self.evaluator = ExpressionEvaluator()
    
    def can_process(self, node: ast.AST) -> bool:
        """Check if this is a while loop node."""
        return isinstance(node, ast.While)
    
    def process(self, node: ast.AST, scope: Dict[str, Any], generator) -> None:
        """
        Process a while loop and unroll it based on runtime condition.
        
        Args:
            node: The AST While node
            scope: Current variable scope dictionary
            generator: The command generator instance
        """
        while_node = node
        iteration_count = 0
        
        # Evaluate condition and unroll loop while True
        while True:
            # Check iteration limit
            if iteration_count >= MAX_ITERATIONS:
                raise ScriptValidationError(f"While loop exceeded maximum of {MAX_ITERATIONS} iterations")
            
            # Evaluate the condition
            condition = self.evaluator.evaluate(while_node.test, scope)
            
            # Exit if condition is False
            if not condition:
                break
            
            # Reset loop control signal
            generator.loop_control = None
            
            # Process the loop body
            for body_node in while_node.body:
                generator._process_node(body_node, scope)
                
                # Check for break/continue
                if generator.loop_control == 'break':
                    break
                elif generator.loop_control == 'continue':
                    generator.loop_control = None
                    break
            
            # If break was encountered, exit the loop
            if generator.loop_control == 'break':
                break
            
            iteration_count += 1
