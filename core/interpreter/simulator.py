"""
Simulator for executing command queues.
Simulates the execution of commands and returns the final game state.
"""
from typing import List, Dict, Any, Tuple


class Simulator:
    """Simulates command execution and returns final game state."""
    
    def simulate(
        self,
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
        # Ensure bot has all required keys
        bot['x'] = bot.get('x', 0)
        bot['y'] = bot.get('y', 0)
        bot['direction'] = bot.get('direction', 'RIGHT')
        bot['inventory'] = initial_bot.get('inventory', {'wood': 0, 'stone': 0, 'metal': 0, 'energy': 0}).copy()
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


# Convenience function for backward compatibility
def simulate_execution(
    command_queue: List[Dict[str, Any]],
    initial_grid: List[List[Dict[str, str]]],
    initial_bot: Dict[str, Any],
    initial_resources: Dict[str, int]
) -> Tuple[List[Dict[str, Any]], Dict[str, Any], Dict[str, int], int, Dict[str, Any]]:
    """
    Convenience function for backward compatibility.
    Simulate the execution of a command queue and return the delta actions.
    """
    simulator = Simulator()
    return simulator.simulate(command_queue, initial_grid, initial_bot, initial_resources)
