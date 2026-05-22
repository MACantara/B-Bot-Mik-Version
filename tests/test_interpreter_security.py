"""
Security tests for RestrictedPython-based interpreter.
Tests various attack vectors to ensure the sandbox is secure.
"""
import pytest
from core.interpreter import ScriptInterpreter, ScriptValidationError


class TestSecurity:
    """Security tests for the script interpreter."""
    
    def test_import_blocking(self):
        """Test that imports are blocked."""
        interpreter = ScriptInterpreter()
        
        # Test various import attempts
        scripts = [
            "import os",
            "import sys",
            "from subprocess import *",
            "import json",
            "from math import sqrt",
        ]
        
        for script in scripts:
            with pytest.raises(ScriptValidationError):
                interpreter.parse_and_validate(script)
    
    def test_file_operations_blocked(self):
        """Test that file operations are blocked."""
        interpreter = ScriptInterpreter()
        
        scripts = [
            "open('file.txt')",
            "__builtins__.open('test.txt')",
        ]
        
        for script in scripts:
            with pytest.raises(ScriptValidationError):
                interpreter.parse_and_validate(script)
    
    def test_code_execution_blocked(self):
        """Test that eval/exec/compile are blocked."""
        interpreter = ScriptInterpreter()
        
        scripts = [
            "eval('1+1')",
            "exec('x=1')",
            "compile('x=1', '<string>', 'exec')",
        ]
        
        for script in scripts:
            with pytest.raises(ScriptValidationError):
                interpreter.parse_and_validate(script)
    
    def test_attribute_access_blocked(self):
        """Test that dangerous attribute access is blocked."""
        interpreter = ScriptInterpreter()
        
        scripts = [
            "getattr(bot, '__dict__')",
            "bot.__class__",
            "setattr(bot, 'x', 1)",
        ]
        
        for script in scripts:
            with pytest.raises(ScriptValidationError):
                interpreter.parse_and_validate(script)
    
    def test_built_in_access_blocked(self):
        """Test that access to dangerous built-ins is blocked."""
        interpreter = ScriptInterpreter()
        
        scripts = [
            "__builtins__",
            "globals()",
            "locals()",
            "vars()",
        ]
        
        for script in scripts:
            with pytest.raises(ScriptValidationError):
                interpreter.parse_and_validate(script)
    
    def test_type_introspection_blocked(self):
        """Test that type introspection functions are blocked."""
        interpreter = ScriptInterpreter()
        
        scripts = [
            "type(bot)",
            "isinstance(bot, object)",
            "issubclass(int, object)",
            "dir(bot)",
        ]
        
        for script in scripts:
            with pytest.raises(ScriptValidationError):
                interpreter.parse_and_validate(script)
    
    def test_infinite_loop_timeout(self):
        """Test that infinite loops are caught by timeout."""
        interpreter = ScriptInterpreter(timeout=2)
        
        script = """
while True:
    bot.move()
"""
        
        with pytest.raises(ScriptValidationError, match="timeout"):
            interpreter.parse_and_validate(script)
    
    def test_memory_exhaustion_limited(self):
        """Test that large memory allocations are limited by timeout."""
        interpreter = ScriptInterpreter(timeout=2)
        
        # Try to create a very large list that should timeout
        script = """
x = [0] * 100000000
for i in range(10000000):
    bot.move()
"""
        
        # This should timeout due to excessive operations
        with pytest.raises(ScriptValidationError, match="timeout"):
            interpreter.parse_and_validate(script)
    
    def test_recursion_depth_limited(self):
        """Test that deep recursion is limited."""
        interpreter = ScriptInterpreter()
        
        script = """
def recurse(n):
    if n > 0:
        recurse(n - 1)
    bot.move()

recurse(10000)
"""
        
        # This should either timeout or fail due to recursion limits
        with pytest.raises((ScriptValidationError, Exception)):
            interpreter.parse_and_validate(script)
    
    def test_module_access_alternative_paths(self):
        """Test that accessing modules via alternative paths is blocked."""
        interpreter = ScriptInterpreter()
        
        scripts = [
            "import importlib; importlib.import_module('os')",
            "__import__('os')",
        ]
        
        for script in scripts:
            with pytest.raises(ScriptValidationError):
                interpreter.parse_and_validate(script)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
