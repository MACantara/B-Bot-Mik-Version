# B-Bot User Guide

Learn how to play B-Bot, a command-based city-building simulation game where you control a robot using Python scripts.

## Getting Started

### What is B-Bot?

B-Bot is a game where you write Python scripts to control a robot on a 20x20 grid. Your goal is to harvest resources (wood and stone) and build structures to grow your city.

### First Steps

1. **Register an Account**: Create an account on the login page
2. **Enter the Game**: After logging in, you'll see the game interface with a 20x20 grid
3. **Write Your First Script**: Use the code editor to write commands for your robot
4. **Run Your Script**: Click "Run Code" to execute your commands and watch your robot in action

## Game Interface

### The Grid
- **20x20 map** with different cell types:
  - 🌲 **Trees** - Harvest for wood
  - 🪨 **Rocks** - Harvest for stone
  - ⬜ **Empty plots** - Build structures here
  - 🏠 **Buildings** - Residential and other structures

### The Robot (B-Bot)
- Starts at position (0, 0) facing RIGHT
- Has an inventory for collected resources
- Can move, turn, harvest, and build

### Resources
- **Wood** - Harvested from trees, used for building
- **Stone** - Harvested from rocks, used for building
- **Metal** - Currently not used in game
- **Energy** - Currently not used in game
- **Population** - Increases when you build residential buildings

## Basic Commands

### Movement
```python
bot.move()  # Move forward one cell in current direction
```

### Turning
```python
bot.turn_left()   # Rotate 90 degrees counter-clockwise
bot.turn_right()  # Rotate 90 degrees clockwise
```

### Harvesting
```python
bot.harvest()  # Harvest resources from current cell
```
- Harvests wood from trees
- Harvests stone from rocks
- Adds resources to your inventory

### Building
```python
bot.build("residential")  # Build a residential building
```
- Costs: 2 wood + 1 stone
- Can only build on empty cells
- Increases population by 1

## Your First Script

Try this simple script to get started:

```python
# Move to a tree and harvest
bot.move()
bot.move()
bot.turn_left()
bot.move()
bot.harvest()

# Move to an empty spot and build
bot.turn_right()
bot.move()
bot.build("residential")
```

## Game Objectives

1. **Harvest Resources**: Navigate to trees and rocks to collect wood and stone
2. **Build Structures**: Use resources to build residential buildings
3. **Grow Population**: Each residential building increases your population
4. **Optimize Your Scripts**: Write efficient scripts to automate tasks

## Tips for Beginners

### Start Simple
- Begin with short scripts (5-10 commands)
- Test each command individually
- Watch the animation to understand robot movement

### Plan Your Route
- Look at the grid before writing your script
- Note the positions of trees, rocks, and empty spaces
- Plan the shortest path to your targets

### Use Variables
```python
moves = 5
for i in range(moves):
    bot.move()
```

### Save Your Progress
- Click "Save Game" to save your current state
- Your resources, grid, and robot position are saved
- Load your save later to continue

## Common Patterns

### Harvest Multiple Resources
```python
# Harvest three trees in a row
for i in range(3):
    bot.move()
    bot.harvest()
```

### Clear an Area
```python
# Clear a 2x2 area
for i in range(2):
    bot.move()
    bot.harvest()
bot.turn_right()
for i in range(2):
    bot.move()
    bot.harvest()
```

### Build Multiple Buildings
```python
# Build three buildings in a line
for i in range(3):
    bot.build("residential")
    bot.move()
```

## Troubleshooting

### Script Won't Run
- Check for syntax errors (missing parentheses, colons, etc.)
- Make sure you're using `bot.` not `bbot.`
- Check the error message in the console

### Robot Won't Move
- Check if the robot is at the grid boundary
- Make sure you're using the correct direction
- The robot cannot move outside the 20x20 grid

### Can't Build
- Check if you have enough resources (2 wood + 1 stone)
- Make sure you're on an empty cell
- You cannot build on trees, rocks, or existing buildings

### Script Times Out
- Your script has a 5-second execution limit
- Reduce the number of iterations in loops
- Optimize your script to be more efficient

## Advanced Tips

Once you're comfortable with the basics, check out the [Scripting Guide](scripting-guide.md) for advanced Python features like:
- Custom functions
- Complex loops
- Data structures (lists, dictionaries)
- Conditional logic

## Need Help?

- Check the [Scripting Guide](scripting-guide.md) for detailed command reference
- Review the [API Documentation](api.md) for technical details
- Report issues on the project repository
