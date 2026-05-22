# Scripting Guide

Complete reference for writing Python scripts to control B-Bot.

## Basic Scripting

### Getting Started

B-Bot uses real Python with RestrictedPython for secure execution. You can use most Python features including variables, loops, functions, and data structures.

### Bot Commands

#### Movement

```python
bot.move()        # Move forward one cell
bot.turn_left()   # Rotate 90° counter-clockwise
bot.turn_right()  # Rotate 90° clockwise
```

**Directions:** UP, RIGHT, DOWN, LEFT

#### Harvesting

```python
bot.harvest()  # Harvest resources from current cell
```

- Trees → Wood
- Rocks → Stone
- Empty → Nothing

#### Building

```python
bot.build("residential")  # Build a residential building
```

**Cost:** 2 wood + 1 stone
**Requirement:** Must be on an empty cell

### Simple Examples

#### Move in a Straight Line

```python
for i in range(5):
    bot.move()
```

#### Turn and Move

```python
bot.move()
bot.turn_right()
bot.move()
bot.turn_left()
bot.move()
```

#### Harvest Resources

```python
# Move to a tree and harvest
bot.move()
bot.move()
bot.harvest()
```

#### Build a House

```python
# First gather resources
bot.move()
bot.harvest()  # Get wood
bot.turn_right()
bot.move()
bot.harvest()  # Get stone

# Then build
bot.turn_left()
bot.move()
bot.build("residential")
```

### Variables

```python
# Define variables
steps = 5
direction = "right"

# Use variables
for i in range(steps):
    bot.move()
```

### Arithmetic

```python
# Basic operations
x = 5
y = 10
total = x + y  # 15

# Use in loops
for i in range(x + y):
    bot.move()
```

### Conditional Logic

```python
# Check if we have enough resources
wood = 5
stone = 3

if wood >= 2 and stone >= 1:
    bot.build("residential")
else:
    bot.move()
```

### Loops

#### For Loops

```python
# Repeat a set number of times
for i in range(10):
    bot.move()
```

#### While Loops

```python
# Continue while condition is true
x = 0
while x < 5:
    bot.move()
    x = x + 1
```

### Functions

```python
# Define a custom function
def move_three():
    bot.move()
    bot.move()
    bot.move()

# Call the function
move_three()
```

#### Functions with Parameters

```python
def move_steps(n):
    for i in range(n):
        bot.move()

# Call with parameter
move_steps(5)
```

### Lists

```python
# Create a list
positions = [1, 2, 3, 4, 5]

# Iterate over list
for pos in positions:
    bot.move()
```

### Combining Concepts

```python
# A more complex script
def gather_resources():
    bot.move()
    bot.harvest()
    bot.turn_right()
    bot.move()
    bot.harvest()

def build_house():
    bot.turn_left()
    bot.move()
    bot.build("residential")

# Main script
gather_resources()
build_house()
```

## Advanced Scripting

### Complex Data Structures

#### Dictionaries

```python
# Store resource counts
resources = {
    "wood": 5,
    "stone": 3,
    "metal": 0
}

# Access values
wood_count = resources["wood"]
```

#### Nested Lists

```python
# 2D grid representation
grid = [
    [0, 1, 0],
    [1, 0, 1],
    [0, 1, 0]
]

# Access elements
cell = grid[1][1]  # Middle cell
```

### Advanced Loops

#### Nested Loops

```python
# Clear a 3x3 area
for i in range(3):
    for j in range(3):
        bot.move()
        bot.harvest()
    bot.turn_right()
    bot.move()
    bot.turn_left()
```

#### Loop with Break

```python
# Stop when condition is met
for i in range(100):
    bot.move()
    if i == 10:
        break
```

#### Loop with Continue

```python
# Skip certain iterations
for i in range(10):
    if i % 2 == 0:
        continue
    bot.move()
```

### Advanced Functions

#### Recursive Functions

```python
def move_back(n):
    if n > 0:
        bot.move()
        move_back(n - 1)

# Note: Be careful with recursion depth
move_back(5)
```

#### Functions with Return Values

```python
def calculate_moves(distance):
    return distance * 2

moves = calculate_moves(5)
for i in range(moves):
    bot.move()
```

#### Default Parameters

```python
def move_and_turn(direction="right"):
    bot.move()
    if direction == "right":
        bot.turn_right()
    else:
        bot.turn_left()

move_and_turn()  # Uses default
move_and_turn("left")  # Overrides default
```

### Pattern Matching

#### Grid Patterns

```python
# Zigzag pattern
for i in range(5):
    for j in range(5):
        bot.move()
    bot.turn_right()
    bot.move()
    bot.turn_right()
    for j in range(5):
        bot.move()
    bot.turn_left()
    bot.move()
    bot.turn_left()
```

#### Spiral Pattern

```python
# Simple spiral
for i in range(4):
    for j in range(i + 1):
        bot.move()
    bot.turn_right()
```

### Optimization Techniques

#### Minimize Commands

```python
# Less efficient
bot.move()
bot.move()
bot.move()

# More efficient
for i in range(3):
    bot.move()
```

#### Batch Operations

```python
# Harvest multiple resources in one pass
for i in range(10):
    bot.move()
    bot.harvest()
```

#### Early Termination

```python
# Stop when goal is reached
target = 5
current = 0

while current < target:
    bot.move()
    current = current + 1
    if current == target:
        break
```

### Error Handling

While RestrictedPython doesn't support try/except, you can use conditional logic:

```python
# Check conditions before acting
wood = 5
stone = 3

if wood >= 2 and stone >= 1:
    bot.build("residential")
else:
    # Alternative action
    bot.move()
```

### State Management

```python
# Track position
x = 0
y = 0

# Update position
x = x + 1
y = y + 1

# Use position in logic
if x > 10:
    bot.turn_right()
```

### Mathematical Operations

```python
# Advanced math
import math  # Note: This is blocked in RestrictedPython

# Use basic operations instead
distance = 10
steps = distance * 2
half = steps // 2
```

### String Operations

```python
# String concatenation
message = "Hello" + " World"

# String repetition
pattern = "A" * 5  # "AAAAA"
```

### Boolean Logic

```python
# Complex conditions
has_wood = True
has_stone = False
is_empty = True

if has_wood and has_stone and is_empty:
    bot.build("residential")
elif has_wood and not has_stone:
    bot.move()
else:
    bot.turn_right()
```

## Best Practices

### 1. Plan Before Coding

- Visualize the robot's path
- Calculate resource needs
- Check grid boundaries

### 2. Use Functions for Reusability

```python
def gather_wood():
    bot.move()
    bot.harvest()

# Use multiple times
gather_wood()
gather_wood()
gather_wood()
```

### 3. Add Comments

```python
# Move to the tree
for i in range(3):
    bot.move()

# Harvest the tree
bot.harvest()
```

### 4. Test Incrementally

- Start with simple scripts
- Add complexity gradually
- Test each change

### 5. Optimize for Timeout

- Keep loops reasonable
- Avoid deep recursion
- Minimize command count

### 6. Use Descriptive Variable Names

```python
# Good
steps_to_tree = 5
wood_needed = 2

# Avoid
x = 5
y = 2
```

## Common Patterns

### Resource Gathering Loop

```python
# Gather resources from multiple cells
for i in range(5):
    bot.move()
    bot.harvest()
```

### Building Grid

```python
# Build a 2x2 grid of buildings
for i in range(2):
    for j in range(2):
        bot.build("residential")
        bot.move()
    bot.turn_right()
    bot.move()
    bot.turn_left()
```

### Return to Origin

```python
# Move forward then return
for i in range(5):
    bot.move()

bot.turn_right()
bot.turn_right()  # Face opposite direction

for i in range(5):
    bot.move()
```

### Clear Area

```python
# Clear a rectangular area
width = 5
height = 3

for h in range(height):
    for w in range(width):
        bot.move()
        bot.harvest()
    bot.turn_right()
    bot.move()
    bot.turn_right()
    for w in range(width):
        bot.move()
    bot.turn_left()
    bot.move()
    bot.turn_left()
```

## Debugging Tips

### Check Script Length

- Keep scripts under 100 commands for reliability
- Longer scripts may timeout

### Verify Syntax

- Check for missing colons after if/for/while
- Ensure proper indentation
- Match all parentheses and brackets

### Test Logic

- Start with small test cases
- Verify each function works independently
- Check boundary conditions

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `undefined_variable` | Variable not defined | Define variable before use |
| `syntax error` | Invalid Python syntax | Check colons, indentation |
| `timeout` | Script too long | Optimize or reduce iterations |
| `Import error` | Attempting to import | Imports are blocked |

## Security Notes

### Blocked Operations

The following are blocked for security:
- `import` statements
- `open()` for file I/O
- `eval()`, `exec()`, `compile()`
- Access to `__builtins__`
- Type introspection (`type()`, `isinstance()`)

### Safe Operations

These are allowed:
- Variables and arithmetic
- Loops and conditionals
- Functions
- Lists and dictionaries
- Bot commands

## Examples Repository

For more examples, check the game's built-in scripts and the [User Guide](user-guide.md) for common patterns.
