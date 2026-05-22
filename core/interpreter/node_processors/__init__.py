"""
Node processors for AST node types.
"""
from .base import NodeProcessor
from .expression import ExpressionProcessor
from .for_loop import ForLoopProcessor
from .assignment import AssignmentProcessor

__all__ = [
    'NodeProcessor',
    'ExpressionProcessor',
    'ForLoopProcessor',
    'AssignmentProcessor'
]

# Create processor instances for easy access
processors = [
    ExpressionProcessor(),
    ForLoopProcessor(),
    AssignmentProcessor()
]
