"""
Base class for AST node processors.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
import ast


class NodeProcessor(ABC):
    """Base class for processing AST nodes."""
    
    @abstractmethod
    def can_process(self, node: ast.AST) -> bool:
        """
        Check if this processor can handle the given node.
        
        Args:
            node: The AST node to check
            
        Returns:
            True if this processor can handle the node
        """
        pass
    
    @abstractmethod
    def process(self, node: ast.AST, scope: Dict[str, Any], generator) -> None:
        """
        Process the AST node and add commands to the generator's queue.
        
        Args:
            node: The AST node to process
            scope: Current variable scope dictionary
            generator: The command generator instance
        """
        pass
