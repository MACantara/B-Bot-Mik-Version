"""
Safe globals dictionary for RestrictedPython execution.
Provides a restricted Python environment with safe built-ins and custom bot object.
"""
import ast
from RestrictedPython import compile_restricted, safe_builtins
from RestrictedPython.Guards import guarded_iter_unpack_sequence, safer_getattr
from .bot_command import BotCommand


def _check_for_imports(script: str) -> None:
    """
    Check if script contains any import statements.
    
    Args:
        script: The Python script to check
        
    Raises:
        ValueError: If script contains import statements
    """
    try:
        tree = ast.parse(script)
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                raise ValueError(f"Import statements are not allowed: {ast.unparse(node)}")
    except SyntaxError:
        # Will be caught later during compilation
        pass


def get_safe_globals() -> dict:
    """
    Create and return a safe globals dictionary for RestrictedPython execution.
    
    Returns:
        Dictionary containing safe built-ins and custom objects
    """
    # Start with RestrictedPython's safe built-ins
    safe_globals = safe_builtins.copy()
    
    # Add additional safe built-ins for common operations
    additional_builtins = {
        'print': print,
        'len': len,
        'range': range,
        'int': int,
        'str': str,
        'bool': bool,
        'list': list,
        'dict': dict,
        'set': set,
        'tuple': tuple,
        'enumerate': enumerate,
        'zip': zip,
        'min': min,
        'max': max,
        'sum': sum,
        'abs': abs,
        'round': round,
        'sorted': sorted,
        'reversed': reversed,
        'any': any,
        'all': all,
        'map': map,
        'filter': filter,
    }
    
    safe_globals.update(additional_builtins)
    
    # Override dangerous built-ins to None (blocked)
    dangerous_builtins = [
        '__import__',
        'open',
        'eval',
        'exec',
        'compile',
        'globals',
        'locals',
        'vars',
        'getattr',
        'setattr',
        'delattr',
        'hasattr',
        'dir',
        'type',
        'isinstance',
        'issubclass',
        'super',
        'property',
        'staticmethod',
        'classmethod',
        '__build_class__',
    ]
    
    for builtin in dangerous_builtins:
        safe_globals[builtin] = None
    
    # Add RestrictedPython-specific guard functions
    safe_globals['_getiter_'] = iter
    safe_globals['_iter_unpack_sequence_'] = guarded_iter_unpack_sequence
    safe_globals['_getattr_'] = safer_getattr
    
    # Block imports completely
    def _import_guard(name, globals=None, locals=None, fromlist=None, level=0):
        raise ImportError(f"Import of '{name}' is not allowed")
    
    safe_globals['_import_'] = _import_guard
    
    # Block write operations
    safe_globals['_write_'] = lambda *args, **kwargs: None
    
    # Add custom bot object
    safe_globals['bot'] = BotCommand()
    
    # Add __name__ for module context
    safe_globals['__name__'] = '__main__'
    
    return safe_globals


def compile_script(script: str) -> tuple:
    """
    Compile a script using RestrictedPython.
    
    Args:
        script: The Python script to compile
        
    Returns:
        Tuple of (compiled_code, errors) where errors is None if successful
    """
    # Check for import statements at AST level
    try:
        _check_for_imports(script)
    except ValueError as e:
        return None, str(e)
    
    try:
        result = compile_restricted(script, '<script>', 'exec')
        # RestrictedPython returns a code object on success
        # If it has errors attribute, compilation failed
        if hasattr(result, 'errors') and result.errors:
            return None, result.errors
        # Otherwise, result is the compiled code object
        return result, None
    except SyntaxError as e:
        return None, str(e)
