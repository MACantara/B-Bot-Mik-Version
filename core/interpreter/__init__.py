"""
B-Bot Script Interpreter Module

A secure AST-based interpreter for B-Bot scripting language.
This module provides validation, command generation, and simulation capabilities.
"""

from .script_interpreter import ScriptInterpreter
from .simulator import simulate_execution, Simulator
from .exceptions import ScriptValidationError, SimulationError
from .config import (
    ALLOWED_COMMANDS,
    ALLOWED_CONTROL,
    FORBIDDEN_MODULES,
    FORBIDDEN_FUNCTIONS,
    MAX_ITERATIONS
)

__all__ = [
    'ScriptInterpreter',
    'simulate_execution',
    'Simulator',
    'ScriptValidationError',
    'SimulationError',
    'ALLOWED_COMMANDS',
    'ALLOWED_CONTROL',
    'FORBIDDEN_MODULES',
    'FORBIDDEN_FUNCTIONS',
    'MAX_ITERATIONS'
]
