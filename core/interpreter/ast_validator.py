"""
AST security validator for the B-Bot script interpreter.
Validates AST trees for security violations and unsafe operations.
"""
import ast
from core.interpreter.config import (
    FORBIDDEN_MODULES,
    FORBIDDEN_FUNCTIONS,
    MAX_ITERATIONS
)
from core.interpreter.exceptions import ScriptValidationError


class ASTValidator:
    """Validates AST trees for security violations."""
    
    def validate(self, tree: ast.AST) -> None:
        """
        Recursively validate the AST for security violations.
        
        Args:
            tree: The AST node to validate
            
        Raises:
            ScriptValidationError: If unsafe code is detected
        """
        for node in ast.walk(tree):
            # Check for forbidden imports
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in FORBIDDEN_MODULES:
                        raise ScriptValidationError(f"Import of '{alias.name}' is not allowed")
            
            if isinstance(node, ast.ImportFrom):
                if node.module and node.module in FORBIDDEN_MODULES:
                    raise ScriptValidationError(f"Import from '{node.module}' is not allowed")
            
            # Check for forbidden function calls
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in FORBIDDEN_FUNCTIONS:
                        raise ScriptValidationError(f"Function '{node.func.id}' is not allowed")
            
            # Check for dangerous attribute access
            if isinstance(node, ast.Attribute):
                if node.attr in FORBIDDEN_FUNCTIONS:
                    raise ScriptValidationError(f"Attribute access '{node.attr}' is not allowed")
            
            # Validate loop bounds
            if isinstance(node, ast.For):
                # Check if it's a range() loop
                if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name):
                    if node.iter.func.id == 'range':
                        # Validate range arguments
                        if len(node.iter.args) > 0:
                            try:
                                # Attempt to evaluate the range limit (must be a constant)
                                if isinstance(node.iter.args[0], ast.Constant):
                                    limit = node.iter.args[0].value
                                    if not isinstance(limit, int) or limit < 0:
                                        raise ScriptValidationError("Range limit must be a positive integer")
                                    if limit > MAX_ITERATIONS:
                                        raise ScriptValidationError(
                                            f"Loop limit {limit} exceeds maximum of {MAX_ITERATIONS}"
                                        )
                                else:
                                    raise ScriptValidationError("Range limit must be a constant integer")
                            except (ValueError, TypeError):
                                raise ScriptValidationError("Invalid range argument")
