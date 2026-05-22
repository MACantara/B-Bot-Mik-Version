// Command queue processing

import { updateBotPosition, setBotDirection, getBotState } from './bot.js';
import { renderGrid } from './grid.js';
import { updateResources } from './resources.js';
import { addConsoleOutput } from './console.js';

export async function processCommandQueue(commands, cellSize) {
    const directions = ['UP', 'RIGHT', 'DOWN', 'LEFT'];
    let resources = {};
    
    for (const cmd of commands) {
        if (cmd.error) {
            addConsoleOutput(`Error: ${cmd.error}`);
            continue;
        }
        
        switch (cmd.action) {
            case 'MOVE':
                const botState = getBotState();
                botState.x = cmd.target_x;
                botState.y = cmd.target_y;
                addConsoleOutput(`Moved to (${botState.x}, ${botState.y})`);
                updateBotPosition(cmd.target_x, cmd.target_y, cellSize);
                break;
            
            case 'TURN_LEFT':
                const leftIdx = directions.indexOf(getBotState().direction);
                setBotDirection(directions[(leftIdx - 1 + 4) % 4]);
                addConsoleOutput(`Turned left to face ${getBotState().direction}`);
                break;
            
            case 'TURN_RIGHT':
                const rightIdx = directions.indexOf(getBotState().direction);
                setBotDirection(directions[(rightIdx + 1) % 4]);
                addConsoleOutput(`Turned right to face ${getBotState().direction}`);
                break;
            
            case 'HARVEST':
                if (cmd.resource_gained) {
                    addConsoleOutput(`Harvested ${cmd.resource_gained}. Amount: ${cmd.amount}`);
                }
                if (cmd.resources) {
                    resources = cmd.resources;
                    updateResources(resources);
                }
                break;
            
            case 'BUILD':
                if (cmd.error) {
                    addConsoleOutput(`Build failed: ${cmd.error}`);
                } else {
                    addConsoleOutput(`Built ${cmd.type} at (${cmd.x}, ${cmd.y}). Population: ${cmd.population}`);
                }
                if (cmd.resources) {
                    resources = cmd.resources;
                    updateResources(resources);
                }
                break;
        }
        
        // Wait for animation to complete before processing next command
        await new Promise(resolve => setTimeout(resolve, 400));
    }
    
    return resources;
}

export async function executeCode(code, grid, bot, resources) {
    const token = localStorage.getItem('access_token');
    
    if (!token) {
        addConsoleOutput('Error: Not logged in. Redirecting to login...');
        setTimeout(() => window.location.href = '/login', 1000);
        return null;
    }
    
    try {
        const response = await fetch('/api/simulation/execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                script: code,
                grid: grid,
                bot: bot,
                resources: resources
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            addConsoleOutput(`Error: ${errorData.error}`);
            
            // If token is invalid, redirect to login
            if (response.status === 401) {
                addConsoleOutput('Session expired. Redirecting to login...');
                setTimeout(() => window.location.href = '/login', 1000);
            }
            return null;
        }
        
        const data = await response.json();
        
        if (!data.success) {
            addConsoleOutput(`Validation error: ${data.error}`);
            return null;
        }
        
        return data;
        
    } catch (err) {
        addConsoleOutput(`Network error: ${err.message}`);
        return null;
    }
}
