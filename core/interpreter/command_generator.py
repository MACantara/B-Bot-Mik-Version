"""
Command generator for the B-Bot script interpreter.
Generates command queues from validated AST trees.
"""
import ast
from typing import List, Dict, Any
from core.interpreter.node_processors import processors
from core.interpreter.exceptions import ScriptValidationError


class CommandGenerator:
    """Generates command queues from validated AST trees."""
    
    def __init__(self):
        self.command_queue: List[Dict[str, Any]] = []
        self.processors = processors
    
    def generate(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """
        Generate command queue from the validated AST.
        
        Args:
            tree: The validated AST node
            
        Returns:
            List of command dictionaries representing the action queue
        """
        self.command_queue = []
        
        # Process the module body recursively
        for node in tree.body:
            self._process_node(node, {})
        
        return self.command_queue
    
    def _process_node(self, node: ast.AST, scope: Dict[str, Any]) -> None:
        """
        Recursively process AST nodes, handling control structures.
        
        Args:
            node: The AST node to process
            scope: Current variable scope dictionary
        """
        # Try each processor
        for processor in self.processors:
            if processor.can_process(node):
                processor.process(node, scope, self)
                return
        
        # Handle unsupported nodes
        if isinstance(node, ast.While):
            raise ScriptValidationError("While loops are not currently supported. Use for loops with range() instead.")
        
        elif isinstance(node, ast.If):
            raise ScriptValidationError("If statements are not currently supported.")
