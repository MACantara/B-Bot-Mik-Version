"""
Node processors for AST node types.
"""
from .base import NodeProcessor
from .expression import ExpressionProcessor
from .for_loop import ForLoopProcessor
from .assignment import AssignmentProcessor
from .if_statement import IfStatementProcessor
from .while_loop import WhileLoopProcessor
from .function_def import FunctionDefProcessor
from .break_continue import BreakContinueProcessor

__all__ = [
    'NodeProcessor',
    'ExpressionProcessor',
    'ForLoopProcessor',
    'AssignmentProcessor',
    'IfStatementProcessor',
    'WhileLoopProcessor',
    'FunctionDefProcessor',
    'BreakContinueProcessor'
]

# Create processor instances for easy access
# Note: FunctionDefProcessor and BreakContinueProcessor are added dynamically in CommandGenerator
processors = [
    ExpressionProcessor(),
    ForLoopProcessor(),
    AssignmentProcessor(),
    IfStatementProcessor(),
    WhileLoopProcessor()
]
