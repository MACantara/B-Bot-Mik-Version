# Testing Guide

Overview of the test structure, running tests, and adding new tests.

## Test Structure

The test suite is organized into four main categories:

```
tests/
├── test_website.py                      # Website functionality tests
├── test_interpreter_functionality.py   # Interpreter capability tests
├── test_interpreter_security.py        # Interpreter security tests
└── test_dsl.py                         # Simulator and bot command tests
```

### Test Categories

#### 1. Website Functionality Tests (`test_website.py`)

Tests for Flask routes, API endpoints, authentication, and database operations:

- **Simulation Routes**
  - Get simulation state
  - Execute script (success, missing script, invalid syntax)
- **Authentication**
  - Missing token
  - Invalid token
- **Save State Routes**
  - Save state requires auth
  - Get save state requires auth
  - Save state creates new
  - Save state updates existing

#### 2. Interpreter Functionality Tests (`test_interpreter_functionality.py`)

Tests for what the interpreter can do (positive cases):

- Basic bot commands (move, turn_left, turn_right, harvest, build)
- Variables and arithmetic
- Loops (for, while)
- User-defined functions
- Lists and data structures
- Error messages with line numbers

#### 3. Interpreter Security Tests (`test_interpreter_security.py`)

Tests for what the interpreter blocks (negative cases):

- Import blocking (import os, from subprocess import *, etc.)
- File operations blocked (open, __builtins__.open)
- Code execution blocked (eval, exec, compile)
- Attribute access blocked (getattr, bot.__class__)
- Built-in access blocked (__builtins__, globals, locals)
- Type introspection blocked (type, isinstance, dir)
- Infinite loop timeout
- Memory exhaustion limits
- Recursion depth limits
- Module access via alternative paths

#### 4. DSL/Simulator Tests (`test_dsl.py`)

Tests for simulator logic and bot command semantics:

- Grid state updates on MOVE
- Direction changes on TURN_LEFT/TURN_RIGHT
- Resource collection on HARVEST
- Building placement and resource costs on BUILD
- Population tracking
- Inventory management
- Boundary checks (grid edges)
- Cell type validation
- Resource validation
- Direction mapping

## Running Tests

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test File

```bash
# Website tests
pytest tests/test_website.py -v

# Interpreter functionality tests
pytest tests/test_interpreter_functionality.py -v

# Interpreter security tests
pytest tests/test_interpreter_security.py -v

# DSL tests
pytest tests/test_dsl.py -v
```

### Run Specific Test Class

```bash
# Test website simulation routes
pytest tests/test_website.py::TestSimulationRoutes -v

# Test interpreter security
pytest tests/test_interpreter_security.py::TestSecurity -v

# Test simulator
pytest tests/test_dsl.py::TestSimulator -v
```

### Run Specific Test Method

```bash
# Test single method
pytest tests/test_interpreter_functionality.py::TestFunctionality::test_basic_bot_commands -v
```

### Run Tests with Coverage

```bash
pytest tests/ --cov=core --cov=routes -v
```

### Run Tests Matching Pattern

```bash
# Run all security tests
pytest tests/ -k security -v

# Run all functionality tests
pytest tests/ -k functionality -v
```

## Test Output

### Successful Test Run

```
tests/test_interpreter_functionality.py::TestFunctionality::test_basic_bot_commands PASSED
tests/test_interpreter_functionality.py::TestFunctionality::test_variables_and_arithmetic PASSED
...
========================= 38 passed in 12.06s =========================
```

### Failed Test Run

```
tests/test_interpreter_security.py::TestSecurity::test_import_blocking FAILED
...
========================= 1 failed, 37 passed in 12.06s =========================
```

## Writing New Tests

### Test Structure

Each test file follows this structure:

```python
"""
Description of what this test file covers.
"""
import pytest
from core.interpreter import ScriptInterpreter, ScriptValidationError


class TestClassName:
    """Description of test class."""
    
    def test_method_name(self):
        """Description of what this test does."""
        # Arrange
        interpreter = ScriptInterpreter()
        
        # Act
        result = interpreter.parse_and_validate("bot.move()")
        
        # Assert
        assert len(result) == 1
```

### Best Practices

1. **Descriptive Test Names**
   ```python
   def test_move_updates_position_correctly():
       # Good
   ```

2. **Arrange-Act-Assert Pattern**
   ```python
   def test_example():
       # Arrange - Set up test data
       interpreter = ScriptInterpreter()
       
       # Act - Execute the code being tested
       result = interpreter.parse_and_validate("bot.move()")
       
       # Assert - Verify the result
       assert len(result) == 1
   ```

3. **Use Fixtures for Common Setup**
   ```python
   @pytest.fixture
   def interpreter():
       return ScriptInterpreter()
   
   def test_example(interpreter):
       result = interpreter.parse_and_validate("bot.move()")
       assert len(result) == 1
   ```

4. **Test Edge Cases**
   ```python
   def test_empty_script():
       interpreter = ScriptInterpreter()
       result = interpreter.parse_and_validate("")
       assert len(result) == 0
   ```

5. **Test Error Conditions**
   ```python
   def test_invalid_syntax():
       interpreter = ScriptInterpreter()
       with pytest.raises(ScriptValidationError):
           interpreter.parse_and_validate("invalid syntax here")
   ```

### Adding Website Tests

```python
def test_new_endpoint(self, client):
    """Test that new endpoint works correctly."""
    response = client.get('/api/new-endpoint')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'expected_field' in data
```

### Adding Interpreter Functionality Tests

```python
def test_new_feature(self):
    """Test that new interpreter feature works."""
    interpreter = ScriptInterpreter()
    
    script = """
# Test new feature
bot.new_command()
"""
    
    commands = interpreter.parse_and_validate(script)
    assert len(commands) == 1
    assert commands[0]['action'] == 'NEW_COMMAND'
```

### Adding Interpreter Security Tests

```python
def test_new_attack_vector(self):
    """Test that new attack vector is blocked."""
    interpreter = ScriptInterpreter()
    
    script = "dangerous_operation()"
    
    with pytest.raises(ScriptValidationError):
        interpreter.parse_and_validate(script)
```

### Adding DSL/Simulator Tests

```python
def test_new_game_logic(self):
    """Test new game logic feature."""
    grid = self._create_demo_grid()
    bot = self._create_demo_bot()
    resources = self._create_demo_resources()
    
    command_queue = [{'action': 'NEW_ACTION'}]
    
    detailed_queue, final_grid, final_resources, population, final_bot = simulate_execution(
        command_queue, grid, bot, resources
    )
    
    assert final_bot['x'] == expected_value
```

## Test Fixtures

### Built-in Fixtures

Pytest provides built-in fixtures:

- `client` - Flask test client
- `app` - Flask application
- `tmpdir` - Temporary directory
- `monkeypatch` - Modify objects at runtime

### Custom Fixtures

Create fixtures in `conftest.py`:

```python
import pytest
from core.interpreter import ScriptInterpreter

@pytest.fixture
def interpreter():
    """Create a fresh interpreter for each test."""
    return ScriptInterpreter()

@pytest.fixture
def demo_grid():
    """Create a demo 20x20 grid."""
    grid = []
    for y in range(20):
        row = []
        for x in range(20):
            row.append({"type": "EMPTY", "id": f"{x}-{y}"})
        grid.append(row)
    return grid
```

## Mocking

### Mocking Database Operations

```python
from unittest.mock import Mock, patch

@patch('core.database.supabase')
def test_with_mock_db(mock_supabase, client):
    """Test with mocked database."""
    mock_response = Mock()
    mock_response.data = []
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response
    
    response = client.post('/api/simulation/save', json={...})
    
    assert response.status_code == 200
```

### Mocking External Services

```python
@patch('core.security.jwt.decode')
def test_with_mock_jwt(mock_decode, client):
    """Test with mocked JWT decode."""
    mock_decode.return_value = {'user_id': 'test_user'}
    
    response = client.get('/api/simulation/save', headers={'Authorization': 'Bearer token'})
    
    assert response.status_code == 200
```

## CI/CD Integration

### GitHub Actions Example

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: pytest tests/ -v --cov=core --cov=routes
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

## Troubleshooting Tests

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'core'`

**Solution:**
```bash
# Ensure you're in the project root
cd B-Bot
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Database Connection Errors

**Error:** Tests fail due to database connection

**Solution:**
- Mock database operations in tests
- Use test database instead of production
- Check `.env` file is configured

### Timeout Errors

**Error:** Security tests timeout

**Solution:**
- Reduce timeout in test configuration
- Optimize test scripts
- Check multiprocessing is working

### Fixture Not Found

**Error:** `fixture 'interpreter' not found`

**Solution:**
- Ensure fixture is defined in `conftest.py`
- Check fixture name matches usage
- Verify fixture is in correct scope

## Test Coverage

### Generate Coverage Report

```bash
pytest tests/ --cov=core --cov=routes --cov-report=html
```

This creates an `htmlcov/` directory with an HTML coverage report.

### Coverage Goals

Aim for:
- Core interpreter: 90%+ coverage
- Routes: 80%+ coverage
- Overall: 85%+ coverage

### View Coverage Report

Open `htmlcov/index.html` in your browser to view the coverage report.

## Performance Testing

### Benchmark Script Execution

```python
import time

def test_script_performance():
    """Test that script executes within time limit."""
    interpreter = ScriptInterpreter()
    
    script = "for i in range(100): bot.move()"
    
    start = time.time()
    interpreter.parse_and_validate(script)
    duration = time.time() - start
    
    assert duration < 5.0  # Should complete in under 5 seconds
```

## Integration Testing

### End-to-End Test

```python
def test_full_workflow(client):
    """Test complete user workflow."""
    # Register
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    assert response.status_code == 201
    
    # Login
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    token = response.json()['access_token']
    
    # Execute script
    response = client.post('/api/simulation/execute', 
        json={'script': 'bot.move()', 'grid': [...], 'bot': {...}, 'resources': {...}},
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
```

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Flask Testing Documentation](https://flask.palletsprojects.com/en/latest/testing/)
- [Python unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
