// Tests for Animation Engine
import { describe, it, expect, beforeEach, vi } from 'vitest';

// Mock dependencies
vi.mock('./bot.js', () => ({
    updateBotPosition: vi.fn(),
    setBotDirection: vi.fn(),
    getBotState: vi.fn(() => ({ x: 0, y: 0, direction: 'RIGHT' }))
}));

vi.mock('./console.js', () => ({
    addConsoleOutput: vi.fn()
}));

import { animationEngine } from './animation.js';

describe('Animation Engine', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        // Reset animation engine state
        animationEngine.queue = [];
        animationEngine.isAnimating = false;
    });

    describe('processQueue', () => {
        it('should process empty queue', async () => {
            await animationEngine.processQueue([]);
            expect(animationEngine.isAnimating).toBe(false);
        });

        it('should process single move command', async () => {
            const commands = [{ action: 'MOVE' }];
            await animationEngine.processQueue(commands);
            expect(animationEngine.isAnimating).toBe(false);
        });

        it('should process multiple commands sequentially', async () => {
            const commands = [
                { action: 'MOVE' },
                { action: 'TURN_LEFT' },
                { action: 'HARVEST' }
            ];
            await animationEngine.processQueue(commands);
            expect(animationEngine.isAnimating).toBe(false);
        });

        it('should handle command with error', async () => {
            const commands = [{ action: 'MOVE', error: 'Test error' }];
            await animationEngine.processQueue(commands);
            expect(animationEngine.isAnimating).toBe(false);
        });

        it('should prevent concurrent animation', async () => {
            animationEngine.isAnimating = true;
            const commands = [{ action: 'MOVE' }];
            await animationEngine.processQueue(commands);
            // Should not process if already animating
        });
    });

    describe('lerp', () => {
        it('should interpolate between values', () => {
            const result = animationEngine.lerp(0, 10, 0.5);
            expect(result).toBe(5);
        });

        it('should return start value at t=0', () => {
            const result = animationEngine.lerp(5, 15, 0);
            expect(result).toBe(5);
        });

        it('should return end value at t=1', () => {
            const result = animationEngine.lerp(5, 15, 1);
            expect(result).toBe(15);
        });

        it('should handle negative values', () => {
            const result = animationEngine.lerp(-10, 10, 0.5);
            expect(result).toBe(0);
        });
    });

    describe('calculateTargetPosition', () => {
        it('should calculate target for RIGHT direction', () => {
            const botState = { x: 5, y: 5, direction: 'RIGHT' };
            const target = animationEngine.calculateTargetPosition(botState);
            expect(target).toEqual({ x: 6, y: 5 });
        });

        it('should calculate target for LEFT direction', () => {
            const botState = { x: 5, y: 5, direction: 'LEFT' };
            const target = animationEngine.calculateTargetPosition(botState);
            expect(target).toEqual({ x: 4, y: 5 });
        });

        it('should calculate target for UP direction', () => {
            const botState = { x: 5, y: 5, direction: 'UP' };
            const target = animationEngine.calculateTargetPosition(botState);
            expect(target).toEqual({ x: 5, y: 4 });
        });

        it('should calculate target for DOWN direction', () => {
            const botState = { x: 5, y: 5, direction: 'DOWN' };
            const target = animationEngine.calculateTargetPosition(botState);
            expect(target).toEqual({ x: 5, y: 6 });
        });
    });

    describe('isAnimatingNow', () => {
        it('should return false when not animating', () => {
            expect(animationEngine.isAnimatingNow()).toBe(false);
        });

        it('should return true when animating', () => {
            animationEngine.isAnimating = true;
            expect(animationEngine.isAnimatingNow()).toBe(true);
        });
    });

    describe('stop', () => {
        it('should clear queue and stop animation', () => {
            animationEngine.queue = [{ action: 'MOVE' }, { action: 'TURN_LEFT' }];
            animationEngine.isAnimating = true;
            
            animationEngine.stop();
            
            expect(animationEngine.queue).toEqual([]);
            expect(animationEngine.isAnimating).toBe(false);
        });
    });
});
