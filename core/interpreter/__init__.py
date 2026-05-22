"""
B-Bot Script Interpreter Module

A RestrictedPython-based secure interpreter for B-Bot scripting language.
This module provides validation, command generation, and simulation capabilities.
"""

from .script_interpreter import ScriptInterpreter
from .simulator import simulate_execution, Simulator
from .exceptions import ScriptValidationError, SimulationError
from .bot_command import BotCommand
from .safe_globals import get_safe_globals, compile_script

__all__ = [
    'ScriptInterpreter',
    'simulate_execution',
    'Simulator',
    'ScriptValidationError',
    'SimulationError',
    'BotCommand',
    'get_safe_globals',
    'compile_script'
]
