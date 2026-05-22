"""
Processor for function definition nodes.
"""
import ast
from typing import Dict, Any
from .base import NodeProcessor
from core.interpreter.exceptions import ScriptValidationError
from core.interpreter.function_registry import FunctionRegistry


class FunctionDefProcessor(NodeProcessor):
    """Processes function definition nodes."""
    
    def __init__(self, registry: FunctionRegistry):
        self.registry = registry
    
    def can_process(self, node: ast.AST) -> bool:
        """Check if this is a function definition node."""
        return isinstance(node, ast.FunctionDef)
    
    def process(self, node: ast.AST, scope: Dict[str, Any], generator) -> None:
        """
        Process a function definition and register it.
        
        Args:
            node: The AST FunctionDef node
            scope: Current variable scope dictionary
            generator: The command generator instance
        """
        func_node = node
        
        # Extract function name
        func_name = func_node.name
        
        # Extract parameter names
        params = []
        for arg in func_node.args.args:
            params.append(arg.arg)
        
        # Register the function
        self.registry.register(func_name, params, func_node.body)
