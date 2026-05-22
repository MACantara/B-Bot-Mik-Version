// Save/load functionality

import { addConsoleOutput } from './console.js';
import { setResources, setPopulation } from './resources.js';
import { getBotState, setBotDirection } from './bot.js';
import { renderGrid } from './grid.js';

export async function saveGameState(grid, resources, population, bot, cellSize) {
    const token = localStorage.getItem('access_token');
    
    try {
        const response = await fetch('/api/simulation/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                grid_json: grid,
                wood_count: resources.wood,
                stone_count: resources.stone,
                metal_count: resources.metal,
                energy_count: resources.energy,
                population_count: population,
                bot_x: bot.x,
                bot_y: bot.y,
                bot_direction: bot.direction
            })
        });
        
        if (response.ok) {
            addConsoleOutput('Game saved successfully!');
        } else {
            addConsoleOutput('Save failed');
        }
    } catch (err) {
        addConsoleOutput('Save failed: Network error');
    }
}

export async function loadGameState(cellSize) {
    const token = localStorage.getItem('access_token');
    
    try {
        const response = await fetch('/api/simulation/save', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            
            return {
                grid: data.grid_json,
                resources: {
                    wood: data.wood_count,
                    stone: data.stone_count,
                    metal: data.metal_count || 0,
                    energy: data.energy_count || 0
                },
                population: data.population_count,
                bot: {
                    x: data.bot_x || 0,
                    y: data.bot_y || 0,
                    direction: data.bot_direction || 'RIGHT'
                }
            };
        } else {
            addConsoleOutput('No saved state found');
            return null;
        }
    } catch (err) {
        addConsoleOutput('Load failed: Network error');
        return null;
    }
}

export function applyLoadedState(state, cellSize) {
    if (!state) return;
    
    setResources(state.resources);
    setPopulation(state.population);
    setBotDirection(state.bot.direction);
    
    renderGrid(state.grid, cellSize);
    addConsoleOutput('Game loaded successfully!');
}
