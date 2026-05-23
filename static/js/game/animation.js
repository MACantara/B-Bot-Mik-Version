// Animation Engine for Smooth Command Queue Processing
// Implements lerp-based interpolation for smooth bot movement and animations

import { updateBotPosition, setBotDirection, getBotState } from './bot.js';
import { addConsoleOutput } from './console.js';
import { updateResources, getResources } from './resources.js';

/**
 * Animation Engine Class
 * Handles smooth animations for bot commands using lerp interpolation
 */
class AnimationEngine {
    constructor() {
        this.queue = [];
        this.isAnimating = false;
        this.animationDuration = 400; // milliseconds per command
    }

    /**
     * Process the command queue with smooth animations
     * @param {Array} commands - Array of command objects
     * @param {Array} grid - The game grid for harvest/build operations
     * @returns {Promise} Resolves when all animations complete
     */
    async processQueue(commands, grid) {
        if (this.isAnimating) {
            console.warn('Animation already in progress');
            return;
        }

        this.isAnimating = true;
        this.queue = [...commands];

        while (this.queue.length > 0) {
            const command = this.queue.shift();
            await this.animateCommand(command, grid);
        }

        this.isAnimating = false;
    }

    /**
     * Animate a single command
     * @param {Object} command - Command object with action and parameters
     * @param {Array} grid - The game grid for harvest/build operations
     * @returns {Promise} Resolves when animation completes
     */
    async animateCommand(command, grid) {
        if (command.error) {
            addConsoleOutput(`Error: ${command.error}`);
            return;
        }

        switch (command.action) {
            case 'MOVE':
                await this.animateMove(command);
                break;
            case 'TURN_LEFT':
                await this.animateTurn('LEFT');
                break;
            case 'TURN_RIGHT':
                await this.animateTurn('RIGHT');
                break;
            case 'HARVEST':
                await this.animateHarvest(command, grid);
                break;
            case 'BUILD':
                await this.animateBuild(command, grid);
                break;
            default:
                console.warn(`Unknown command: ${command.action}`);
        }
    }

    /**
     * Animate movement with lerp interpolation
     * @param {Object} command - MOVE command with target position
     * @returns {Promise} Resolves when movement animation completes
     */
    async animateMove(command) {
        const botState = getBotState();
        const startPos = { x: botState.x, y: botState.y };
        
        // Calculate target position based on current direction
        const targetPos = this.calculateTargetPosition(botState);
        
        const startTime = performance.now();
        
        return new Promise(resolve => {
            const animate = (currentTime) => {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / this.animationDuration, 1);
                
                // Lerp interpolation: linear interpolation between start and end
                const currentX = this.lerp(startPos.x, targetPos.x, progress);
                const currentY = this.lerp(startPos.y, targetPos.y, progress);
                
                // Update visual position only (not botState)
                updateBotPosition(currentX, currentY, 1.5);
                
                if (progress < 1) {
                    requestAnimationFrame(animate);
                } else {
                    // Animation complete - update actual bot state with integer coordinates
                    botState.x = targetPos.x;
                    botState.y = targetPos.y;
                    addConsoleOutput(`Moved to (${botState.x}, ${botState.y})`);
                    resolve();
                }
            };
            
            requestAnimationFrame(animate);
        });
    }

    /**
     * Animate turn with smooth rotation
     * @param {string} direction - 'LEFT' or 'RIGHT'
     * @returns {Promise} Resolves when turn animation completes
     */
    async animateTurn(direction) {
        const botState = getBotState();
        const directions = ['UP', 'RIGHT', 'DOWN', 'LEFT'];
        const currentIdx = directions.indexOf(botState.direction);
        
        let newIdx;
        if (direction === 'LEFT') {
            newIdx = (currentIdx - 1 + 4) % 4;
        } else {
            newIdx = (currentIdx + 1) % 4;
        }
        
        const newDirection = directions[newIdx];
        const startTime = performance.now();
        
        return new Promise(resolve => {
            const animate = (currentTime) => {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / this.animationDuration, 1);
                
                // Smooth direction change (instant for now, could add rotation animation)
                if (progress >= 1) {
                    setBotDirection(newDirection);
                    addConsoleOutput(`Turned ${direction.toLowerCase()} to face ${newDirection}`);
                    resolve();
                } else {
                    requestAnimationFrame(animate);
                }
            };
            
            requestAnimationFrame(animate);
        });
    }

    /**
     * Animate harvest action
     * @param {Object} command - HARVEST command
     * @param {Array} grid - The game grid
     * @returns {Promise} Resolves when harvest animation completes
     */
    async animateHarvest(command, grid) {
        const botState = getBotState();
        const startTime = performance.now();
        
        return new Promise(resolve => {
            const animate = (currentTime) => {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / this.animationDuration, 1);
                
                if (progress >= 1) {
                    // Perform actual harvest logic
                    const cell = grid[botState.y] && grid[botState.y][botState.x];
                    if (cell) {
                        const resourceType = cell.type;
                        
                        // Only harvest if there's a resource
                        if (resourceType === 'TREE' || resourceType === 'ROCK') {
                            // Remove resource from grid
                            grid[botState.y][botState.x] = { type: 'EMPTY', id: `${botState.x}-${botState.y}` };
                            
                            // Add to resources
                            const resources = getResources();
                            if (resourceType === 'TREE') {
                                resources.wood += 1;
                            } else if (resourceType === 'ROCK') {
                                resources.stone += 1;
                            }
                            updateResources(resources);
                            
                            addConsoleOutput(`Harvested ${resourceType.toLowerCase()}`);
                        } else {
                            addConsoleOutput('Nothing to harvest here');
                        }
                    }
                    resolve();
                } else {
                    requestAnimationFrame(animate);
                }
            };
            
            requestAnimationFrame(animate);
        });
    }

    /**
     * Animate build action
     * @param {Object} command - BUILD command
     * @param {Array} grid - The game grid
     * @returns {Promise} Resolves when build animation completes
     */
    async animateBuild(command, grid) {
        const botState = getBotState();
        const startTime = performance.now();
        
        return new Promise(resolve => {
            const animate = (currentTime) => {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / this.animationDuration, 1);
                
                if (progress >= 1) {
                    // Perform actual build logic
                    const cell = grid[botState.y] && grid[botState.y][botState.x];
                    if (cell) {
                        const buildType = command.type;
                        
                        // Only build if cell is empty
                        if (cell.type === 'EMPTY') {
                            // Add structure to grid
                            grid[botState.y][botState.x] = { type: buildType.toUpperCase(), id: `${botState.x}-${botState.y}` };
                            
                            addConsoleOutput(`Built ${buildType} at (${botState.x}, ${botState.y})`);
                        } else {
                            addConsoleOutput('Cannot build here - cell not empty');
                        }
                    }
                    resolve();
                } else {
                    requestAnimationFrame(animate);
                }
            };
            
            requestAnimationFrame(animate);
        });
    }

    /**
     * Linear interpolation (lerp) between two values
     * @param {number} start - Start value
     * @param {number} end - End value
     * @param {number} t - Progress (0 to 1)
     * @returns {number} Interpolated value
     */
    lerp(start, end, t) {
        return start + (end - start) * t;
    }

    /**
     * Calculate target position based on current direction
     * @param {Object} botState - Current bot state
     * @returns {Object} Target position {x, y} (clamped to grid bounds)
     */
    calculateTargetPosition(botState) {
        const directions = {
            'UP': { x: 0, y: -1 },
            'RIGHT': { x: 1, y: 0 },
            'DOWN': { x: 0, y: 1 },
            'LEFT': { x: -1, y: 0 }
        };
        
        const delta = directions[botState.direction];
        const targetX = botState.x + delta.x;
        const targetY = botState.y + delta.y;
        
        // Clamp to grid bounds (0-19 for 20x20 grid)
        const clampedX = Math.max(0, Math.min(19, targetX));
        const clampedY = Math.max(0, Math.min(19, targetY));
        
        return {
            x: clampedX,
            y: clampedY
        };
    }

    /**
     * Check if animation is currently in progress
     * @returns {boolean} True if animating
     */
    isAnimatingNow() {
        return this.isAnimating;
    }

    /**
     * Stop current animation
     */
    stop() {
        this.queue = [];
        this.isAnimating = false;
    }
}

// Export singleton instance
export const animationEngine = new AnimationEngine();
