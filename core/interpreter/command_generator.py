"""
Command generator for the B-Bot script interpreter.
Generates command queues from validated AST trees.
"""
import ast
from typing import List, Dict, Any
from core.interpreter.node_processors import processors
from core.interpreter.exceptions import ScriptValidationError
from core.interpreter.function_registry import FunctionRegistry
from core.interpreter.scope import ScopeManager


class CommandGenerator:
    """Generates command queues from validated AST trees."""
    
    def __init__(self):
        self.command_queue: List[Dict[str, Any]] = []
        self.function_registry = FunctionRegistry()
        self.scope_manager = ScopeManager()
        self.loop_control = None  # Track break/continue signals
        
        # Initialize processors with dependencies
        from core.interpreter.node_processors.function_def import FunctionDefProcessor
        from core.interpreter.node_processors.break_continue import BreakContinueProcessor
        self.processors = processors + [
            FunctionDefProcessor(self.function_registry),
            BreakContinueProcessor()
        ]
    
    def generate(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """
        Generate command queue from the validated AST.
        
        Args:
            tree: The validated AST node
            
        Returns:
            List of command dictionaries representing the action queue
        """
        self.command_queue = []
        
        # Use a single global scope for the entire script
        scope = {}
        
        # Process the module body recursively
        for node in tree.body:
            self._process_node(node, scope)
        
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
        raise ScriptValidationError(f"Unsupported node type: {type(node).__name__}")
