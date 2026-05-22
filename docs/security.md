# Security Documentation

Overview of the security model, RestrictedPython sandbox, and authentication mechanisms.

## Security Model Overview

B-Bot uses a multi-layered security approach to ensure safe execution of user-provided Python scripts:

1. **AST-Level Import Blocking** - Blocks imports at compile time
2. **RestrictedPython Compilation** - Rewrites dangerous operations
3. **Safe Globals Environment** - Provides only safe built-in functions
4. **Timeout Protection** - Prevents infinite loops via multiprocessing
5. **JWT Authentication** - Protects API endpoints

## RestrictedPython Sandbox

### What is RestrictedPython?

RestrictedPython is a library that compiles Python code to run in a restricted environment. It transforms the AST (Abstract Syntax Tree) to limit access to dangerous operations.

### Security Layers

#### Layer 1: AST Import Blocking

Before compilation, the script is parsed to detect import statements:

```python
import ast

def _check_for_imports(script: str) -> None:
    tree = ast.parse(script)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise ValueError(f"Import statements are not allowed")
```

**Blocked imports:**
- `import os`
- `import sys`
- `from subprocess import *`
- `import json`
- Any other import statement

#### Layer 2: RestrictedPython Compilation

Scripts are compiled using `compile_restricted()` which:
- Rewrites attribute access to use guarded functions
- Replaces `__import__` with a safe guard
- Adds guard functions for iteration and unpacking

```python
from RestrictedPython import compile_restricted

result = compile_restricted(script, '<script>', 'exec')
```

#### Layer 3: Safe Globals

The execution environment includes only safe built-ins:

**Allowed built-ins:**
- `abs`, `all`, `any`, `bin`, `bool`, `chr`, `complex`, `dict`, `divmod`
- `enumerate`, `filter`, `float`, `format`, `hex`, `int`, `isinstance`, `issubclass`
- `iter`, `len`, `list`, `map`, `max`, `min`, `next`, `oct`, `ord`, `pow`, `range`
- `repr`, `round`, `set`, `slice`, `sorted`, `str`, `sum`, `tuple`, `zip`

**Blocked built-ins:**
- `__import__`, `open`, `eval`, `exec`, `compile`
- `globals`, `locals`, `vars`, `dir`, `type`
- `__builtins__`, `__dict__`, `__class__`

**Guard functions:**
- `_getiter_` - Controls iteration
- `_iter_unpack_sequence_` - Controls sequence unpacking
- `_getattr_` - Controls attribute access
- `_write_` - Blocks write operations
- `_import_` - Blocks imports

#### Layer 4: Timeout Protection

Scripts execute in a separate process with a 5-second timeout:

```python
from multiprocessing import Pool

with Pool() as pool:
    result = pool.apply_async(_execute_script_worker, (script,))
    commands = result.get(timeout=5)  # 5-second timeout
```

**Protection against:**
- Infinite loops
- Excessive memory allocation
- Deep recursion
- Long-running computations

#### Layer 5: Multiprocessing Isolation

Each script execution runs in a separate process:
- Isolated memory space
- Cannot affect the main process
- Terminated cleanly on timeout

## Blocked Operations

### File Operations

```python
# BLOCKED
open('file.txt', 'r')
__builtins__.open('test.txt')
```

**Reason:** Prevents reading/writing files on the server.

### Code Execution

```python
# BLOCKED
eval('1+1')
exec('x=1')
compile('x=1', '<string>', 'exec')
```

**Reason:** Prevents arbitrary code execution.

### Imports

```python
# BLOCKED
import os
import sys
from subprocess import *
import json
__import__('os')
importlib.import_module('os')
```

**Reason:** Prevents accessing system modules and external libraries.

### Attribute Access

```python
# BLOCKED
getattr(bot, '__dict__')
bot.__class__
setattr(bot, 'x', 1)
bot.__dict__
```

**Reason:** Prevents accessing internal object state.

### Built-in Access

```python
# BLOCKED
__builtins__
globals()
locals()
vars()
```

**Reason:** Prevents accessing the global namespace.

### Type Introspection

```python
# BLOCKED
type(bot)
isinstance(bot, object)
issubclass(int, object)
dir(bot)
```

**Reason:** Prevents examining object internals.

## Allowed Operations

### Bot Commands

```python
# ALLOWED
bot.move()
bot.turn_left()
bot.turn_right()
bot.harvest()
bot.build("residential")
```

### Variables and Arithmetic

```python
# ALLOWED
x = 5
y = 10
z = x + y
result = z * 2
```

### Control Flow

```python
# ALLOWED
for i in range(10):
    bot.move()

while x < 5:
    bot.move()
    x = x + 1

if x > 0:
    bot.turn_left()
```

### Functions

```python
# ALLOWED
def move_three():
    bot.move()
    bot.move()
    bot.move()

move_three()
```

### Data Structures

```python
# ALLOWED
my_list = [1, 2, 3]
my_dict = {"key": "value"}
my_tuple = (1, 2, 3)
```

## Authentication Security

### JWT Token Structure

**Access Token:**
- Algorithm: HS256
- Expiration: 30 minutes
- Contains: user_id, username

**Refresh Token:**
- Algorithm: HS256
- Expiration: 7 days
- Contains: user_id

### Token Validation

```python
def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
```

### Protected Endpoints

All simulation endpoints require authentication:

```python
@simulation_bp.route('/execute', methods=['POST'])
@token_required
def execute_script():
    # Protected endpoint
    pass
```

### Password Security

- Passwords are hashed using bcrypt before storage
- Never store plain-text passwords
- Verify using bcrypt.compare()

## Known Security Considerations

### Resource Exhaustion

**Risk:** Users could create scripts that consume excessive memory or CPU.

**Mitigation:**
- 5-second timeout on script execution
- Multiprocessing isolation
- Process termination on timeout

### Denial of Service

**Risk:** Many simultaneous script executions could overload the server.

**Mitigation:**
- Consider rate limiting (not currently implemented)
- Consider request queuing
- Monitor server resources

### Side-Channel Attacks

**Risk:** Timing attacks could reveal information about the system.

**Mitigation:**
- Scripts run in isolated processes
- No access to system information
- Limited error messages

### Social Engineering

**Risk:** Users might be tricked into running malicious scripts.

**Mitigation:**
- Clear documentation about what scripts can do
- User education about security
- No auto-execution of external scripts

## Security Best Practices

### For Developers

1. **Keep RestrictedPython Updated**
   - Regularly check for security updates
   - Review changelog for security fixes

2. **Monitor Timeout Failures**
   - Log timeout events
   - Investigate repeated timeouts

3. **Review Safe Globals**
   - Periodically audit allowed built-ins
   - Remove unnecessary functions

4. **Test Security**
   - Run security tests regularly
   - Add tests for new attack vectors

### For Users

1. **Understand Script Behavior**
   - Read scripts before running
   - Understand what each command does

2. **Use Trusted Sources**
   - Only run scripts from trusted sources
   - Review shared scripts carefully

3. **Report Issues**
   - Report suspicious behavior
   - Report security vulnerabilities

## Security Testing

The project includes comprehensive security tests in `tests/test_interpreter_security.py`:

- Import blocking tests
- File operation blocking tests
- Code execution blocking tests
- Attribute access blocking tests
- Built-in access blocking tests
- Type introspection blocking tests
- Timeout protection tests
- Memory exhaustion tests
- Recursion depth tests

Run security tests:

```bash
pytest tests/test_interpreter_security.py -v
```

## Future Security Enhancements

### Potential Improvements

1. **Rate Limiting**
   - Limit requests per user
   - Prevent abuse

2. **Resource Quotas**
   - Per-user memory limits
   - Per-user execution time limits

3. **Script Signing**
   - Verify script authenticity
   - Prevent tampering

4. **Audit Logging**
   - Log all script executions
   - Track resource usage

5. **Sandbox Hardening**
   - Additional RestrictedPython guards
   - More restrictive safe globals

## Security Contact

To report security vulnerabilities:
- Do not open public issues
- Contact the project maintainers privately
- Provide detailed information about the vulnerability

## References

- [RestrictedPython Documentation](https://restrictedpython.readthedocs.io/)
- [OWASP Python Security](https://owasp.org/www-project-python-security/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
