"""
Functionality tests for RestrictedPython-based interpreter.
Tests that legitimate interpreter features work correctly.
"""
import pytest
from core.interpreter import ScriptInterpreter, ScriptValidationError


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
