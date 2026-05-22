"""
Configuration constants for the B-Bot script interpreter.
"""

# Allowed bot commands
ALLOWED_COMMANDS = {
    'move', 'turn_left', 'turn_right', 'harvest', 'build'
}

# Allowed control structures
ALLOWED_CONTROL = {
    'For', 'If', 'While'
}

# Forbidden modules (security blacklist)
FORBIDDEN_MODULES = {
    'os', 'sys', 'subprocess', 'shutil', 'pickle', 'eval', 'exec',
    'compile', 'open', '__import__', 'globals', 'locals', 'vars'
}

# Forbidden function calls
FORBIDDEN_FUNCTIONS = {
    'eval', 'exec', 'compile', '__import__', 'open', 'getattr',
    'setattr', 'delattr', 'hasattr', 'dir', 'globals', 'locals'
}

# Maximum loop iterations to prevent infinite loops
MAX_ITERATIONS = 500

# Supported comparison operators
COMPARISON_OPERATORS = {
    'Eq',      # ==
    'NotEq',   # !=
    'Lt',      # <
    'LtE',     # <=
    'Gt',      # >
    'GtE'      # >=
}

# Supported arithmetic operators
ARITHMETIC_OPERATORS = {
    'Add',     # +
    'Sub',     # -
    'Mult',    # *
    'Div',     # / (integer division)
    'Mod'      # %
}

# Supported logical operators
LOGICAL_OPERATORS = {
    'And',     # and
    'Or',      # or
    'Not'      # not
}

# Supported data types
SUPPORTED_TYPES = {
    'int',     # Integers
    'bool',    # Booleans
    'list'     # Lists
}
