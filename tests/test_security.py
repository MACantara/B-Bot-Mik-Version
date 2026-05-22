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


class TestFunctionality:
    """Tests that legitimate functionality still works."""
    
    def test_basic_bot_commands(self):
        """Test that basic bot commands work."""
        interpreter = ScriptInterpreter()
        
        script = """
bot.move()
bot.turn_left()
bot.turn_right()
bot.harvest()
bot.build("residential")
"""
        
        commands = interpreter.parse_and_validate(script)
        assert len(commands) == 5
        assert commands[0]['action'] == 'MOVE'
        assert commands[1]['action'] == 'TURN_LEFT'
        assert commands[2]['action'] == 'TURN_RIGHT'
        assert commands[3]['action'] == 'HARVEST'
        assert commands[4]['action'] == 'BUILD'
    
    def test_variables_and_arithmetic(self):
        """Test that variables and arithmetic work."""
        interpreter = ScriptInterpreter()
        
        script = """
x = 5
y = 10
z = x + y
for i in range(z):
    bot.move()
"""
        
        commands = interpreter.parse_and_validate(script)
        assert len(commands) == 15  # 5 + 10 = 15 iterations
    
    def test_loops(self):
        """Test that for and while loops work."""
        interpreter = ScriptInterpreter()
        
        # For loop
        script = """
for i in range(3):
    bot.move()
"""
        commands = interpreter.parse_and_validate(script)
        assert len(commands) == 3
        
        # While loop
        script = """
x = 0
while x < 3:
    bot.move()
    x = x + 1
"""
        commands = interpreter.parse_and_validate(script)
        assert len(commands) == 3
    
    def test_functions(self):
        """Test that user-defined functions work."""
        interpreter = ScriptInterpreter()
        
        script = """
def move_three():
    bot.move()
    bot.move()
    bot.move()

move_three()
"""
        
        commands = interpreter.parse_and_validate(script)
        assert len(commands) == 3
    
    def test_lists(self):
        """Test that list operations work."""
        interpreter = ScriptInterpreter()
        
        script = """
positions = [1, 2, 3]
for i in range(len(positions)):
    bot.move()
"""
        
        commands = interpreter.parse_and_validate(script)
        assert len(commands) == 3
    
    def test_error_messages_show_line_numbers(self):
        """Test that error messages include line numbers."""
        interpreter = ScriptInterpreter()
        
        script = """
x = 5
y = undefined_variable
bot.move()
"""
        
        with pytest.raises(ScriptValidationError) as exc_info:
            interpreter.parse_and_validate(script)
        
        error_msg = str(exc_info.value)
        # Should mention line number or variable name
        assert 'undefined_variable' in error_msg or 'line' in error_msg.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
