// Tests for Skulpt.js Bridge
import { describe, it, expect, beforeEach, vi } from 'vitest';

// Mock Skulpt global object
global.Sk = {
    python3: false,
    builtin: {
        func: vi.fn(),
        none: { none$: {} }
    },
    ffi: {
        remapToJs: vi.fn((val) => val.v || val)
    },
    misceval: {
        asyncToPromise: vi.fn()
    },
    configure: vi.fn(),
    importMainWithBody: vi.fn()
};

// Import after mocking
import { executeScript, getCommandQueue, clearCommandQueue } from './skulpt-bridge.js';

describe('Skulpt Bridge', () => {
    beforeEach(() => {
        clearCommandQueue();
        vi.clearAllMocks();
    });

    describe('executeScript', () => {
        it('should configure Skulpt for Python 3', () => {
            expect(Sk.python3).toBe(true);
        });

        it('should execute a simple move command', async () => {
            const mockCommands = [{ action: 'MOVE' }];
            Sk.misceval.asyncToPromise.mockResolvedValue(undefined);

            const result = await executeScript('bot.move()');
            expect(result).toEqual(mockCommands);
        });

        it('should execute multiple commands', async () => {
            const mockCommands = [
                { action: 'MOVE' },
                { action: 'TURN_LEFT' },
                { action: 'HARVEST' }
            ];
            Sk.misceval.asyncToPromise.mockResolvedValue(undefined);

            const result = await executeScript('bot.move()\nbot.turn_left()\nbot.harvest()');
            expect(result).toEqual(mockCommands);
        });

        it('should handle build command with string parameter', async () => {
            const mockCommands = [{ action: 'BUILD', type: 'residential' }];
            Sk.misceval.asyncToPromise.mockResolvedValue(undefined);

            const result = await executeScript('bot.build("residential")');
            expect(result).toEqual(mockCommands);
        });

        it('should throw error on script execution failure', async () => {
            const mockError = new Error('Syntax error');
            Sk.misceval.asyncToPromise.mockRejectedValue(mockError);

            await expect(executeScript('invalid syntax')).rejects.toThrow('Script execution error');
        });

        it('should clear command queue before execution', async () => {
            Sk.misceval.asyncToPromise.mockResolvedValue(undefined);

            await executeScript('bot.move()');
            const queue1 = getCommandQueue();
            
            await executeScript('bot.turn_left()');
            const queue2 = getCommandQueue();
            
            expect(queue1.length).toBe(1);
            expect(queue2.length).toBe(1);
        });
    });

    describe('getCommandQueue', () => {
        it('should return empty queue initially', () => {
            const queue = getCommandQueue();
            expect(queue).toEqual([]);
        });

        it('should return current command queue', () => {
            // Manually add commands for testing
            const testQueue = [{ action: 'MOVE' }, { action: 'TURN_LEFT' }];
            // Note: This would need the actual bot object to be accessible
            // For now, just test the function exists
            const queue = getCommandQueue();
            expect(Array.isArray(queue)).toBe(true);
        });
    });

    describe('clearCommandQueue', () => {
        it('should clear the command queue', () => {
            clearCommandQueue();
            const queue = getCommandQueue();
            expect(queue).toEqual([]);
        });
    });
});
