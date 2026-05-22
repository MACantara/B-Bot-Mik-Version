"""
Domain Specific Language tests for simulator and bot command semantics.
Tests game logic, resource management, and building rules.
"""
import pytest
from core.interpreter import simulate_execution, Simulator


class TestSimulator:
    """Tests for the simulator logic and game state updates."""
    
    def _create_demo_grid(self):
        """Create a simple 20x20 demo grid for testing."""
        grid = []
        for y in range(20):
            row = []
            for x in range(20):
                row.append({"type": "EMPTY", "id": f"{x}-{y}"})
            grid.append(row)
        return grid
    
    def _create_demo_bot(self):
        """Create a demo bot state."""
        return {
            "x": 0,
            "y": 0,
            "direction": "RIGHT",
            "inventory": {"wood": 0, "stone": 0, "metal": 0, "energy": 0}
        }
    
    def _create_demo_resources(self):
        """Create demo resource counts."""
        return {"wood": 0, "stone": 0, "metal": 0, "energy": 0}
    
    def test_move_updates_position(self):
        """Test that MOVE command changes bot position correctly."""
        grid = self._create_demo_grid()
        bot = self._create_demo_bot()
        resources = self._create_demo_resources()
        
        command_queue = [
            {'action': 'MOVE'},
            {'action': 'MOVE'},
        ]
        
        detailed_queue, final_grid, final_resources, population, final_bot = simulate_execution(
            command_queue, grid, bot, resources
        )
        
        # Bot should move 2 steps to the right (starting at 0,0 facing RIGHT)
        assert final_bot['x'] == 2
        assert final_bot['y'] == 0
        assert len(detailed_queue) == 2
    
    def test_move_respects_boundaries(self):
        """Test that bot cannot move outside 20x20 grid."""
        grid = self._create_demo_grid()
        bot = self._create_demo_bot()
        bot['x'] = 19  # Start at right edge
        resources = self._create_demo_resources()
        
        command_queue = [{'action': 'MOVE'}]
        
        detailed_queue, final_grid, final_resources, population, final_bot = simulate_execution(
            command_queue, grid, bot, resources
        )
        
        # Bot should stay at x=19 (boundary check)
        assert final_bot['x'] == 19
        assert final_bot['y'] == 0
    
    def test_turn_left_updates_direction(self):
        """Test that TURN_LEFT updates direction correctly."""
        grid = self._create_demo_grid()
        bot = self._create_demo_bot()
        resources = self._create_demo_resources()
        
        command_queue = [{'action': 'TURN_LEFT'}]
        
        detailed_queue, final_grid, final_resources, population, final_bot = simulate_execution(
            command_queue, grid, bot, resources
        )
        
        # RIGHT -> LEFT (counter-clockwise)
        assert final_bot['direction'] == 'UP'
    
    def test_turn_right_updates_direction(self):
        """Test that TURN_RIGHT updates direction correctly."""
        grid = self._create_demo_grid()
        bot = self._create_demo_bot()
        resources = self._create_demo_resources()
        
        command_queue = [{'action': 'TURN_RIGHT'}]
        
        detailed_queue, final_grid, final_resources, population, final_bot = simulate_execution(
            command_queue, grid, bot, resources
        )
        
        # RIGHT -> DOWN (clockwise)
        assert final_bot['direction'] == 'DOWN'
    
    def test_direction_rotation_logic(self):
        """Test that direction changes follow correct rotation logic."""
        grid = self._create_demo_grid()
        bot = self._create_demo_bot()
        resources = self._create_demo_resources()
        
        command_queue = [
            {'action': 'TURN_LEFT'},
            {'action': 'TURN_LEFT'},
            {'action': 'TURN_LEFT'},
            {'action': 'TURN_LEFT'},
        ]
        
        detailed_queue, final_grid, final_resources, population, final_bot = simulate_execution(
            command_queue, grid, bot, resources
        )
        
        # Four left turns should return to original direction
        assert final_bot['direction'] == 'RIGHT'
    
    def test_harvest_tree_adds_wood(self):
        """Test that HARVEST adds wood to inventory and clears cell."""
        grid = self._create_demo_grid()
        grid[0][0] = {"type": "TREE", "id": "0-0"}  # Place tree at bot position
        bot = self._create_demo_bot()
        resources = self._create_demo_resources()
        
        command_queue = [{'action': 'HARVEST'}]
        
        detailed_queue, final_grid, final_resources, population, final_bot = simulate_execution(
            command_queue, grid, bot, resources
        )
        
        assert final_resources['wood'] == 1
        assert final_grid[0][0]['type'] == 'EMPTY'
        assert detailed_queue[0]['resource_gained'] == 'wood'
        assert detailed_queue[0]['amount'] == 1
    
    def test_harvest_rock_adds_stone(self):
        """Test that HARVEST adds stone to inventory and clears cell."""
        grid = self._create_demo_grid()
        grid[0][0] = {"type": "ROCK", "id": "0-0"}  # Place rock at bot position
        bot = self._create_demo_bot()
        resources = self._create_demo_resources()
        
        command_queue = [{'action': 'HARVEST'}]
        
        detailed_queue, final_grid, final_resources, population, final_bot = simulate_execution(
            command_queue, grid, bot, resources
        )
        
        assert final_resources['stone'] == 1
        assert final_grid[0][0]['type'] == 'EMPTY'
        assert detailed_queue[0]['resource_gained'] == 'stone'
    
    def test_build_places_building(self):
        """Test that BUILD places buildings with correct resource costs."""
        grid = self._create_demo_grid()
        bot = self._create_demo_bot()
        resources = {"wood": 5, "stone": 3, "metal": 0, "energy": 0}
        
        command_queue = [{'action': 'BUILD', 'type': 'residential'}]
        
        detailed_queue, final_grid, final_resources, population, final_bot = simulate_execution(
            command_queue, grid, bot, resources
        )
        
        assert final_grid[0][0]['type'] == 'RESIDENTIAL'
        assert final_resources['wood'] == 3  # 5 - 2
        assert final_resources['stone'] == 2  # 3 - 1
        assert population == 1
        assert detailed_queue[0]['type'] == 'residential'
    
    def test_build_requires_sufficient_resources(self):
        """Test that BUILD fails without sufficient resources."""
        grid = self._create_demo_grid()
        bot = self._create_demo_bot()
        resources = {"wood": 1, "stone": 0, "metal": 0, "energy": 0}  # Insufficient
        
        command_queue = [{'action': 'BUILD', 'type': 'residential'}]
        
        detailed_queue, final_grid, final_resources, population, final_bot = simulate_execution(
            command_queue, grid, bot, resources
        )
        
        assert final_grid[0][0]['type'] == 'EMPTY'  # No building placed
        assert final_resources['wood'] == 1  # Resources unchanged
        assert 'error' in detailed_queue[0]
        assert detailed_queue[0]['error'] == 'Insufficient resources'
    
    def test_build_only_on_empty_cells(self):
        """Test that BUILD only works on EMPTY cells."""
        grid = self._create_demo_grid()
        grid[0][0] = {"type": "TREE", "id": "0-0"}  # Non-empty cell
        bot = self._create_demo_bot()
        resources = {"wood": 5, "stone": 3, "metal": 0, "energy": 0}
        
        command_queue = [{'action': 'BUILD', 'type': 'residential'}]
        
        detailed_queue, final_grid, final_resources, population, final_bot = simulate_execution(
            command_queue, grid, bot, resources
        )
        
        assert final_grid[0][0]['type'] == 'TREE'  # Cell unchanged
        assert 'error' in detailed_queue[0]
        assert detailed_queue[0]['error'] == 'Cannot build on this cell'
    
    def test_inventory_tracking(self):
        """Test that resources are tracked correctly across operations."""
        grid = self._create_demo_grid()
        grid[0][0] = {"type": "TREE", "id": "0-0"}
        bot = self._create_demo_bot()
        resources = {"wood": 0, "stone": 0, "metal": 0, "energy": 0}
        
        command_queue = [
            {'action': 'HARVEST'},  # +1 wood
            {'action': 'BUILD', 'type': 'residential'},  # -2 wood, -1 stone (should fail)
        ]
        
        detailed_queue, final_grid, final_resources, population, final_bot = simulate_execution(
            command_queue, grid, bot, resources
        )
        
        assert final_resources['wood'] == 1  # Harvested 1, none spent
        assert final_resources['stone'] == 0
    
    def test_complex_scenario(self):
        """Test a complex scenario with multiple operations."""
        grid = self._create_demo_grid()
        grid[0][1] = {"type": "TREE", "id": "0-1"}
        grid[0][2] = {"type": "ROCK", "id": "0-2"}
        bot = self._create_demo_bot()
        resources = {"wood": 0, "stone": 0, "metal": 0, "energy": 0}
        
        command_queue = [
            {'action': 'MOVE'},  # Move to (1,0)
            {'action': 'TURN_LEFT'},  # Face UP
            {'action': 'MOVE'},  # Move to (1,0) - can't move up from y=0
            {'action': 'TURN_RIGHT'},  # Face RIGHT
            {'action': 'MOVE'},  # Move to (2,0)
            {'action': 'TURN_LEFT'},  # Face UP
            {'action': 'MOVE'},  # Move to (2,0) - can't move up from y=0
        ]
        
        detailed_queue, final_grid, final_resources, population, final_bot = simulate_execution(
            command_queue, grid, bot, resources
        )
        
        # Bot should end at (2,0) after moves
        assert final_bot['x'] == 2
        assert final_bot['y'] == 0
        assert final_bot['direction'] == 'UP'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
