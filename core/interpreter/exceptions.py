"""
Custom exceptions for the B-Bot script interpreter.
"""


class ScriptValidationError(Exception):
    """Raised when script validation fails due to security or syntax issues."""
    pass


class SimulationError(Exception):
    """Raised when simulation execution fails."""
    pass
