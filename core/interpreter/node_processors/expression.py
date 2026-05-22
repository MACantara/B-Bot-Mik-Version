"""
Processor for expression nodes and function calls.
"""
import ast
from typing import Dict, Any
from .base import NodeProcessor
from core.interpreter.config import ALLOWED_COMMANDS
from core.interpreter.exceptions import ScriptValidationError


class ExpressionProcessor(NodeProcessor):
    """Processes expression nodes and function calls."""
    
    def can_process(self, node: ast.AST) -> bool:
        """Check if this is an expression node with a function call."""
        return isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
    
    def process(self, node: ast.AST, scope: Dict[str, Any], generator) -> None:
        """
        Process an expression node and add bot commands to the queue.
        
        Args:
            node: The AST Expr node
            scope: Current variable scope dictionary
            generator: The command generator instance
        """
        call_node = node.value
        
        # Check if it's a method call on 'bot' object
        if isinstance(call_node.func, ast.Attribute):
            if isinstance(call_node.func.value, ast.Name) and call_node.func.value.id == 'bot':
                command = call_node.func.attr
                
                if command not in ALLOWED_COMMANDS:
                    raise ScriptValidationError(f"Unknown command: bot.{command}()")
                
                # Parse arguments
                args = []
                for arg in call_node.args:
                    if isinstance(arg, ast.Constant):
                        args.append(arg.value)
                    elif isinstance(arg, ast.Str):  # Python 3.7 compatibility
                        args.append(arg.s)
                    else:
                        raise ScriptValidationError(f"Invalid argument type for bot.{command}()")
                
                # Add to command queue
                command_dict = self._create_command_dict(command, args)
                generator.command_queue.append(command_dict)
    
    def _create_command_dict(self, command: str, args: list) -> Dict[str, Any]:
        """
        Create a command dictionary for the command queue.
        
        Args:
            command: The command name
            args: List of command arguments
            
        Returns:
            Dictionary representing the command
        """
        cmd = {'action': command.upper()}
        
        if command == 'build' and args:
            cmd['type'] = args[0]
        
        return cmd
