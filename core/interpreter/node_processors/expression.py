"""
Processor for expression nodes and function calls.
"""
import ast
from typing import Dict, Any, List
from .base import NodeProcessor
from core.interpreter.config import ALLOWED_COMMANDS
from core.interpreter.exceptions import ScriptValidationError
from core.interpreter.evaluator import ExpressionEvaluator
from core.interpreter.data_types import BotList


class ExpressionProcessor(NodeProcessor):
    """Processes expression nodes and function calls."""
    
    def __init__(self):
        self.evaluator = ExpressionEvaluator()
    
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
                    raise ScriptValidationError(f"Unknown command: bot.{command}()", node=node)
                
                # Parse arguments
                args = []
                for arg in call_node.args:
                    if isinstance(arg, ast.Constant):
                        args.append(arg.value)
                    elif isinstance(arg, ast.Str):  # Python 3.7 compatibility
                        args.append(arg.s)
                    else:
                        raise ScriptValidationError(f"Invalid argument type for bot.{command}()", node=node)
                
                # Add to command queue
                command_dict = self._create_command_dict(command, args)
                generator.command_queue.append(command_dict)
            
            else:
                # Handle method calls on other objects (e.g., list.append)
                self._handle_method_call(call_node, scope, node)
        
        # Check if it's a custom function call
        elif isinstance(call_node.func, ast.Name):
            func_name = call_node.func.id
            
            if generator.function_registry.has(func_name):
                self._call_user_function(func_name, call_node.args, scope, generator, node)
    
    def _handle_method_call(self, call_node: ast.Call, scope: Dict[str, Any], expr_node: ast.AST) -> None:
        """
        Handle method calls on objects (e.g., list.append).
        
        Args:
            call_node: The AST Call node
            scope: Current variable scope dictionary
            expr_node: The parent Expr node for error context
        """
        if not isinstance(call_node.func, ast.Attribute):
            return
        
        obj_name = call_node.func.value.id if isinstance(call_node.func.value, ast.Name) else None
        method_name = call_node.func.attr
        
        if obj_name is None or obj_name not in scope:
            raise ScriptValidationError(f"Object '{obj_name}' is not defined", node=expr_node)
        
        obj = scope[obj_name]
        
        # Handle list methods
        if isinstance(obj, BotList):
            if method_name == 'append':
                if len(call_node.args) != 1:
                    raise ScriptValidationError("append() requires exactly 1 argument", node=expr_node)
                value = self.evaluator.evaluate(call_node.args[0], scope)
                obj.append(value)
            else:
                raise ScriptValidationError(f"List method '{method_name}' is not supported", node=expr_node)
        else:
            raise ScriptValidationError(f"Method '{method_name}' is not supported for this type", node=expr_node)
    
    def _call_user_function(self, func_name: str, args: List[ast.AST], scope: Dict[str, Any], generator, expr_node: ast.AST) -> None:
        """
        Call a user-defined function.
        
        Args:
            func_name: Name of the function to call
            args: AST nodes representing function arguments
            scope: Current variable scope dictionary
            generator: The command generator instance
            expr_node: The parent Expr node for error context
        """
        func_def = generator.function_registry.get(func_name)
        params = func_def['params']
        body = func_def['body']
        
        # Evaluate arguments
        arg_values = []
        for arg in args:
            arg_values.append(self.evaluator.evaluate(arg, scope))
        
        # Check argument count
        if len(arg_values) != len(params):
            raise ScriptValidationError(
                f"Function '{func_name}' expects {len(params)} arguments, got {len(arg_values)}",
                node=expr_node
            )
        
        # Create new scope for function
        func_scope = scope.copy()
        for param, value in zip(params, arg_values):
            func_scope[param] = value
        
        # Process function body
        for body_node in body:
            generator._process_node(body_node, func_scope)
    
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
