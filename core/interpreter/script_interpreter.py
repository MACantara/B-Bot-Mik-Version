"""
RestrictedPython-based secure script interpreter for B-Bot commands.
Uses RestrictedPython to compile and execute user scripts in a safe environment.
"""
import multiprocessing
from typing import List, Dict, Any
from .exceptions import ScriptValidationError
from .safe_globals import get_safe_globals, compile_script
from .bot_command import BotCommand


def _execute_script_worker(script: str) -> List[Dict[str, Any]]:
    """
    Worker function for executing script in a separate process.
    
    Args:
        script: The script string to execute
        
    Returns:
        Command queue from bot object
    """
    from .safe_globals import get_safe_globals, compile_script
    from .bot_command import BotCommand
    from .exceptions import ScriptValidationError
    
    # Compile the script
    compiled_code, errors = compile_script(script)
    if errors:
        raise ScriptValidationError(f"Compilation error: {errors}")
    
    # Get fresh globals and bot instance
    safe_globals = get_safe_globals()
    bot = BotCommand()
    safe_globals['bot'] = bot
    
    # Execute the script
    try:
        exec(compiled_code, safe_globals, {})
    except ImportError as e:
        raise ScriptValidationError(f"Import error: {str(e)}")
    
    return bot.get_commands()


class ScriptInterpreter:
    """
    Secure interpreter for B-Bot scripting language.
    Uses RestrictedPython to compile and execute scripts in a safe environment.
    """
    
    def __init__(self, timeout: int = 5):
        """
        Initialize the interpreter.
        
        Args:
            timeout: Maximum execution time in seconds (default: 5)
        """
        self.command_queue: List[Dict[str, Any]] = []
        self.timeout = timeout
    
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
        
        # Get safe globals
        safe_globals = get_safe_globals()
        
        try:
            # Execute script in separate process with timeout
            pool = multiprocessing.Pool(processes=1)
            result = pool.apply_async(_execute_script_worker, (script,))
            
            # Wait for result with timeout
            self.command_queue = result.get(timeout=self.timeout)
            pool.close()
            pool.join()
            
        except multiprocessing.TimeoutError:
            pool.terminate()
            pool.join()
            raise ScriptValidationError(f"Script execution timeout: exceeded {self.timeout} seconds")
        except SyntaxError as e:
            raise ScriptValidationError(f"Syntax error at line {e.lineno}: {e.msg}", line=e.lineno)
        except NameError as e:
            raise ScriptValidationError(f"Name error: {str(e)}")
        except TypeError as e:
            raise ScriptValidationError(f"Type error: {str(e)}")
        except ValueError as e:
            raise ScriptValidationError(f"Value error: {str(e)}")
        except Exception as e:
            raise ScriptValidationError(f"Execution error: {str(e)}")
        
        return self.command_queue
