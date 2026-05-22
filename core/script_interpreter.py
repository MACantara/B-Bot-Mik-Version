"""
AST-based secure script interpreter for B-Bot commands.
Uses Python's ast module to parse and validate user scripts without using eval/exec.
"""
import ast
from typing import List, Dict, Any, Optional, Tuple


class ScriptValidationError(Exception):
    """Raised when script validation fails due to security or syntax issues."""
    pass


class ScriptInterpreter:
    """
    Secure interpreter for B-Bot scripting language.
    Parses Python-like scripts using AST and validates against a whitelist of allowed operations.
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
    
    def __init__(self):
        self.command_queue: List[Dict[str, Any]] = []
        self.iteration_count = 0
    
    def parse_and_validate(self, script: str) -> List[Dict[str, Any]]:
        """
        Parse and validate a script, returning a command queue.
        
        Args:
            script: The user-submitted script string
            
        Returns:
            List of command dictionaries representing the action queue
            
        Raises:
            ScriptValidationError: If script contains invalid or unsafe code
        """
        self.command_queue = []
        self.iteration_count = 0
        
        try:
            # Parse the script into an AST
            tree = ast.parse(script)
        except SyntaxError as e:
            raise ScriptValidationError(f"Syntax error: {e}")
        
        # Validate the AST structure
        self._validate_ast(tree)
        
        # Generate command queue from the validated AST
        self._generate_commands(tree)
        
        return self.command_queue
    
    def _validate_ast(self, tree: ast.AST) -> None:
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
                    if alias.name in self.FORBIDDEN_MODULES:
                        raise ScriptValidationError(f"Import of '{alias.name}' is not allowed")
            
            if isinstance(node, ast.ImportFrom):
                if node.module and node.module in self.FORBIDDEN_MODULES:
                    raise ScriptValidationError(f"Import from '{node.module}' is not allowed")
            
            # Check for forbidden function calls
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in self.FORBIDDEN_FUNCTIONS:
                        raise ScriptValidationError(f"Function '{node.func.id}' is not allowed")
            
            # Check for dangerous attribute access
            if isinstance(node, ast.Attribute):
                if node.attr in self.FORBIDDEN_FUNCTIONS:
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
                                    if limit > self.MAX_ITERATIONS:
                                        raise ScriptValidationError(
                                            f"Loop limit {limit} exceeds maximum of {self.MAX_ITERATIONS}"
                                        )
                                else:
                                    raise ScriptValidationError("Range limit must be a constant integer")
                            except (ValueError, TypeError):
                                raise ScriptValidationError("Invalid range argument")
    
    def _generate_commands(self, tree: ast.AST) -> None:
        """
        Generate command queue from the validated AST.
        
        Args:
            tree: The validated AST node
        """
        for node in ast.walk(tree):
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                self._process_function_call(node.value)
    
    def _process_function_call(self, call_node: ast.Call) -> None:
        """
        Process a function call node and add to command queue if it's a bot command.
        
        Args:
            call_node: The AST Call node representing a function call
        """
        # Check if it's a method call on 'bot' object
        if isinstance(call_node.func, ast.Attribute):
            if isinstance(call_node.func.value, ast.Name) and call_node.func.value.id == 'bot':
                command = call_node.func.attr
                
                if command not in self.ALLOWED_COMMANDS:
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
                self.command_queue.append(command_dict)
    
    def _create_command_dict(self, command: str, args: List[Any]) -> Dict[str, Any]:
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


def simulate_execution(
    command_queue: List[Dict[str, Any]],
    initial_grid: List[List[Dict[str, str]]],
    initial_bot: Dict[str, Any],
    initial_resources: Dict[str, int]
) -> Tuple[List[Dict[str, Any]], Dict[str, Any], Dict[str, int], int, Dict[str, Any]]:
    """
    Simulate the execution of a command queue and return the delta actions.
    
    Args:
        command_queue: List of command dictionaries
        initial_grid: Initial 20x20 grid state
        initial_bot: Initial bot state (x, y, direction, inventory)
        initial_resources: Initial resource counts
        
    Returns:
        Tuple of (detailed command queue, final grid, final resources, population, final bot)
    """
    grid = [row[:] for row in initial_grid]  # Deep copy
    bot = initial_bot.copy()
    bot['inventory'] = initial_bot['inventory'].copy()
    resources = initial_resources.copy()
    population = 0
    
    detailed_queue = []
    directions = ['UP', 'RIGHT', 'DOWN', 'LEFT']
    
    for cmd in command_queue:
        action = cmd['action']
        detailed_cmd = {'action': action}
        
        if action == 'MOVE':
            # Calculate new position based on direction
            new_x, new_y = bot['x'], bot['y']
            if bot['direction'] == 'UP':
                new_y = max(0, bot['y'] - 1)
            elif bot['direction'] == 'DOWN':
                new_y = min(19, bot['y'] + 1)
            elif bot['direction'] == 'LEFT':
                new_x = max(0, bot['x'] - 1)
            elif bot['direction'] == 'RIGHT':
                new_x = min(19, bot['x'] + 1)
            
            detailed_cmd['target_x'] = new_x
            detailed_cmd['target_y'] = new_y
            detailed_cmd['resources'] = resources.copy()
            bot['x'], bot['y'] = new_x, new_y
        
        elif action == 'TURN_LEFT':
            current_idx = directions.index(bot['direction'])
            bot['direction'] = directions[(current_idx - 1) % 4]
            detailed_cmd['direction'] = bot['direction']
        
        elif action == 'TURN_RIGHT':
            current_idx = directions.index(bot['direction'])
            bot['direction'] = directions[(current_idx + 1) % 4]
            detailed_cmd['direction'] = bot['direction']
        
        elif action == 'HARVEST':
            cell = grid[bot['y']][bot['x']]
            if cell['type'] == 'TREE':
                resources['wood'] += 1
                grid[bot['y']][bot['x']] = {'type': 'EMPTY', 'id': cell['id']}
                detailed_cmd['resource_gained'] = 'wood'
                detailed_cmd['amount'] = 1
            elif cell['type'] == 'ROCK':
                resources['stone'] += 1
                grid[bot['y']][bot['x']] = {'type': 'EMPTY', 'id': cell['id']}
                detailed_cmd['resource_gained'] = 'stone'
                detailed_cmd['amount'] = 1
            detailed_cmd['resources'] = resources.copy()
        
        elif action == 'BUILD':
            build_type = cmd.get('type', 'residential').upper()
            cell = grid[bot['y']][bot['x']]
            if cell['type'] == 'EMPTY':
                if resources['wood'] >= 2 and resources['stone'] >= 1:
                    resources['wood'] -= 2
                    resources['stone'] -= 1
                    grid[bot['y']][bot['x']] = {'type': build_type, 'id': cell['id']}
                    population += 1
                    detailed_cmd['type'] = build_type.lower()
                    detailed_cmd['x'] = bot['x']
                    detailed_cmd['y'] = bot['y']
                    detailed_cmd['population'] = population
                else:
                    detailed_cmd['error'] = 'Insufficient resources'
            else:
                detailed_cmd['error'] = 'Cannot build on this cell'
            detailed_cmd['resources'] = resources.copy()
        
        detailed_queue.append(detailed_cmd)
    
    return detailed_queue, grid, resources, population, bot
