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
