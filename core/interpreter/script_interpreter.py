"""
AST-based secure script interpreter for B-Bot commands.
Uses Python's ast module to parse and validate user scripts without using eval/exec.
"""
import ast
from typing import List, Dict, Any
from .config import (
    ALLOWED_COMMANDS,
    ALLOWED_CONTROL,
    FORBIDDEN_MODULES,
    FORBIDDEN_FUNCTIONS,
    MAX_ITERATIONS
)
from .exceptions import ScriptValidationError
from .ast_validator import ASTValidator
from .command_generator import CommandGenerator


class ScriptInterpreter:
    """
    Secure interpreter for B-Bot scripting language.
    Parses Python-like scripts using AST and validates against a whitelist of allowed operations.
    """
    
    def __init__(self):
        self.command_queue: List[Dict[str, Any]] = []
        self.iteration_count = 0
        self.validator = ASTValidator()
        self.generator = CommandGenerator()
    
    def parse_and_validate(self, script: str) -> List[Dict[str, Any]]:
        """
        Parse and validate a script, returning a command queue.
        
        Args:
            script: The user-submitted script string
            
        Returns:
            List of command dictionaries representing the action queue
            
        Raises:
            ScriptValidationError: If script contains invalid or unsafe code
        """
        self.command_queue = []
        self.iteration_count = 0
        
        try:
            # Parse the script into an AST
            tree = ast.parse(script)
        except SyntaxError as e:
            raise ScriptValidationError(f"Syntax error: {e}")
        
        # Validate the AST structure
        self.validator.validate(tree)
        
        # Generate command queue from the validated AST
        self.command_queue = self.generator.generate(tree)
        
        return self.command_queue
