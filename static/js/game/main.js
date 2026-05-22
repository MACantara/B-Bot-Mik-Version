// Main entry point for game initialization

import { initThreeJS } from './three-renderer.js';
import { renderGrid } from './grid.js';
import { createBotSprite, getBotState, setBotDirection } from './bot.js';
import { processCommandQueue, executeCode } from './commands.js';
import { setResources, setPopulation, getResources, getPopulation } from './resources.js';
import { addConsoleOutput, clearConsole } from './console.js';
import { saveGameState, loadGameState, applyLoadedState } from './storage.js';
import { initIcons } from '../shared/icons.js';

const DEFAULT_CODE = `positions = [1, 2, 3]
for i in range(len(positions)):
    bot.move()
bot.turn_left()
bot.move()
bot.harvest()
bot.turn_right()
bot.move()
bot.harvest()
bot.build("residential")`;

// Grid configuration
const GRID_SIZE = 20;
const CELL_SIZE = 1.5;
const GRID_WIDTH = GRID_SIZE * CELL_SIZE;
const GRID_HEIGHT = GRID_SIZE * CELL_SIZE;

// Game state
let grid = [];
let bot = { x: 0, y: 0, direction: 'RIGHT', inventory: { wood: 0, stone: 0, metal: 0, energy: 0 } };
let isRunning = false;

function initializeDemoGrid() {
    grid = [];
    const treePositions = [[2, 3], [5, 7], [8, 2], [1, 8], [6, 4], [12, 15], [15, 5], [18, 12], [3, 17], [10, 10]];
    const rockPositions = [[3, 1], [7, 5], [4, 8], [9, 3], [2, 6], [14, 11], [16, 8], [11, 14], [5, 18], [13, 2]];
    const roadPositions = [[4, 4], [5, 4], [6, 4], [7, 4], [8, 4]];
    
    for (let y = 0; y < GRID_SIZE; y++) {
        const row = [];
        for (let x = 0; x < GRID_SIZE; x++) {
            const isTree = treePositions.some(pos => pos[0] === x && pos[1] === y);
            const isRock = rockPositions.some(pos => pos[0] === x && pos[1] === y);
            const isRoad = roadPositions.some(pos => pos[0] === x && pos[1] === y);
            
            if (isTree) {
                row.push({ type: 'TREE', id: `${x}-${y}` });
            } else if (isRock) {
                row.push({ type: 'ROCK', id: `${x}-${y}` });
            } else if (isRoad) {
                row.push({ type: 'ROAD', id: `${x}-${y}` });
            } else {
                row.push({ type: 'EMPTY', id: `${x}-${y}` });
            }
        }
        grid.push(row);
    }
    bot = { x: 0, y: 0, direction: 'RIGHT', inventory: { wood: 0, stone: 0, metal: 0, energy: 0 } };
    setResources({ wood: 0, stone: 0, metal: 0, energy: 0 });
    setPopulation(0);
}

async function initGame() {
    // Initialize Lucide icons
    initIcons();
    
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/login';
        return;
    }
    
    document.getElementById('codeEditor').value = DEFAULT_CODE;
    
    // Fetch initial state from backend
    try {
        const response = await fetch('/api/simulation/state');
        if (response.ok) {
            const data = await response.json();
            grid = data.grid;
            bot = data.bot;
            setResources(data.resources);
            setPopulation(data.population);
        } else {
            initializeDemoGrid();
        }
    } catch (err) {
        initializeDemoGrid();
    }
    
    // Initialize Three.js
    initThreeJS('pixiContainer', GRID_WIDTH, GRID_HEIGHT);
    renderGrid(grid, CELL_SIZE);
    createBotSprite(bot.x, bot.y, CELL_SIZE);
    setBotDirection(bot.direction);
    
    // Load saved state
    const savedState = await loadGameState(CELL_SIZE);
    if (savedState) {
        grid = savedState.grid;
        bot = savedState.bot;
        setResources(savedState.resources);
        setPopulation(savedState.population);
        renderGrid(grid, CELL_SIZE);
        createBotSprite(bot.x, bot.y, CELL_SIZE);
        setBotDirection(bot.direction);
    }
    
    // Setup event listeners
    setupEventListeners();
}

function setupEventListeners() {
    // Toggle editor popup
    document.getElementById('toggleEditorBtn').addEventListener('click', () => {
        const popup = document.getElementById('editorPopup');
        popup.classList.toggle('hidden');
        lucide.createIcons();
    });
    
    document.getElementById('runBtn').addEventListener('click', async () => {
        if (isRunning) return;
        isRunning = true;
        clearConsole();
        const code = document.getElementById('codeEditor').value;
        
        const data = await executeCode(code, grid, bot, getResources());
        
        if (data) {
            await processCommandQueue(data.commands, CELL_SIZE);
            
            grid = data.final_state.grid;
            setResources(data.final_state.resources);
            setPopulation(data.final_state.population);
            bot = data.final_state.bot;
            
            renderGrid(grid, CELL_SIZE);
            createBotSprite(bot.x, bot.y, CELL_SIZE);
            setBotDirection(bot.direction);
            addConsoleOutput('Script execution completed!');
        }
        
        isRunning = false;
    });
    
    document.getElementById('resetBtn').addEventListener('click', () => {
        clearConsole();
        initializeDemoGrid();
        renderGrid(grid, CELL_SIZE);
        createBotSprite(bot.x, bot.y, CELL_SIZE);
        setBotDirection(bot.direction);
    });
    
    document.getElementById('logoutBtn').addEventListener('click', () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
    });
    
    document.getElementById('saveBtn').addEventListener('click', async () => {
        await saveGameState(grid, getResources(), getPopulation(), bot, CELL_SIZE);
    });
    
    document.getElementById('loadBtn').addEventListener('click', async () => {
        const savedState = await loadGameState(CELL_SIZE);
        if (savedState) {
            grid = savedState.grid;
            bot = savedState.bot;
            setResources(savedState.resources);
            setPopulation(savedState.population);
            renderGrid(grid, CELL_SIZE);
            createBotSprite(bot.x, bot.y, CELL_SIZE);
            setBotDirection(bot.direction);
        }
    });
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', initGame);
