"""
Processor for for loop nodes.
"""
import ast
from typing import Dict, Any
from .base import NodeProcessor
from core.interpreter.config import MAX_ITERATIONS
from core.interpreter.exceptions import ScriptValidationError


class ForLoopProcessor(NodeProcessor):
    """Processes for loop nodes and unrolls them."""
    
    def can_process(self, node: ast.AST) -> bool:
        """Check if this is a for loop node."""
        return isinstance(node, ast.For)
    
    def process(self, node: ast.AST, scope: Dict[str, Any], generator) -> None:
        """
        Process a for loop and unroll it if it uses range() with constant value.
        
        Args:
            node: The AST For node
            scope: Current variable scope dictionary
            generator: The command generator instance
        """
        for_node = node
        
        # Check if it's a range() loop
        if not isinstance(for_node.iter, ast.Call) or not isinstance(for_node.iter.func, ast.Name):
            raise ScriptValidationError("For loops only support range() with constant integer values")
        
        if for_node.iter.func.id != 'range':
            raise ScriptValidationError("For loops only support range() with constant integer values")
        
        # Get the range limit
        if len(for_node.iter.args) == 0:
            raise ScriptValidationError("range() requires at least one argument")
        
        limit_arg = for_node.iter.args[0]
        if not isinstance(limit_arg, ast.Constant):
            raise ScriptValidationError("Range limit must be a constant integer")
        
        limit = limit_arg.value
        if not isinstance(limit, int) or limit < 0:
            raise ScriptValidationError("Range limit must be a positive integer")
        
        if limit > MAX_ITERATIONS:
            raise ScriptValidationError(f"Loop limit {limit} exceeds maximum of {MAX_ITERATIONS}")
        
        # Unroll the loop
        loop_var = for_node.target.id if isinstance(for_node.target, ast.Name) else None
        new_scope = scope.copy()
        
        for i in range(limit):
            if loop_var:
                new_scope[loop_var] = i
            
            # Reset loop control signal
            generator.loop_control = None
            
            # Process each statement in the loop body
            for body_node in for_node.body:
                generator._process_node(body_node, new_scope)
                
                # Check for break/continue
                if generator.loop_control == 'break':
                    break
                elif generator.loop_control == 'continue':
                    generator.loop_control = None
                    break
