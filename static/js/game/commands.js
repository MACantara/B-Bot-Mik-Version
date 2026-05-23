// Command queue processing

import { updateBotPosition, setBotDirection, getBotState } from './bot.js';
import { renderGrid } from './grid.js';
import { updateResources } from './resources.js';
import { addConsoleOutput } from './console.js';
import { executeScript } from '../interpreter/skulpt-bridge.js';
import { animationEngine } from './animation.js';

export async function processCommandQueue(commands, cellSize, grid) {
    // Validate commands is an array
    if (!Array.isArray(commands)) {
        console.error('Invalid commands:', commands);
        return;
    }
    
    // Use animation engine for smooth command processing
    await animationEngine.processQueue(commands);
    
    // Update grid after all animations complete
    renderGrid(grid, cellSize);
}

export async function executeCode(code, grid, bot, resources) {
    try {
        // Execute script client-side using Skulpt
        const commands = await executeScript(code);
        
        // Return command queue for animation processing
        return {
            success: true,
            commands: commands
        };
        
    } catch (err) {
        addConsoleOutput(`Execution error: ${err.message}`);
        return {
            success: false,
            error: err.message
        };
    }
}
