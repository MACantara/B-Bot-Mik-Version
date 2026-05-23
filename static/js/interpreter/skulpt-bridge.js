// Skulpt.js Bridge for Client-Side Python Execution
// This module configures Skulpt and provides the bot object FFI bridge

// Configure Skulpt for Python 3 behavior
Sk.python3 = true;

// Command queue array - stores bot commands generated from Python execution
let commandQueue = [];

/**
 * Bot object FFI (Foreign Function Interface) Bridge
 * Maps Python bot method calls to JavaScript command queue operations
 */
const bot = {
    /**
     * MOVE command - Appends a MOVE action to the command queue
     * @returns {Sk.builtin.none} Python None object
     */
    move: new Sk.builtin.func(() => {
        commandQueue.push({ action: 'MOVE' });
        return Sk.builtin.none.none$;
    }),

    /**
     * TURN_LEFT command - Appends a TURN_LEFT action to the command queue
     * @returns {Sk.builtin.none} Python None object
     */
    turn_left: new Sk.builtin.func(() => {
        commandQueue.push({ action: 'TURN_LEFT' });
        return Sk.builtin.none.none$;
    }),

    /**
     * TURN_RIGHT command - Appends a TURN_RIGHT action to the command queue
     * @returns {Sk.builtin.none} Python None object
     */
    turn_right: new Sk.builtin.func(() => {
        commandQueue.push({ action: 'TURN_RIGHT' });
        return Sk.builtin.none.none$;
    }),

    /**
     * HARVEST command - Appends a HARVEST action to the command queue
     * @returns {Sk.builtin.none} Python None object
     */
    harvest: new Sk.builtin.func(() => {
        commandQueue.push({ action: 'HARVEST' });
        return Sk.builtin.none.none$;
    }),

    /**
     * BUILD command - Appends a BUILD action with building type to the command queue
     * @param {Sk.builtin.str} buildType - Python string for building type
     * @returns {Sk.builtin.none} Python None object
     */
    build: new Sk.builtin.func((buildType) => {
        // Unpack Python string primitive to JavaScript string using Sk.ffi.remapToJs()
        const type = Sk.ffi.remapToJs(buildType);
        commandQueue.push({ action: 'BUILD', type: type });
        return Sk.builtin.none.none$;
    })
};

/**
 * Execute a Python script using Skulpt
 * @param {string} script - The Python script string to execute
 * @returns {Promise<Array>} Promise resolving to the command queue array
 * @throws {Error} If script execution fails
 */
export function executeScript(script) {
    return new Promise((resolve, reject) => {
        // Reset command queue for new execution
        commandQueue = [];

        // Configure Skulpt output functions to capture print statements
        Sk.configure({
            output: (text) => {
                // Capture print output - can be sent to console
                console.log('Skulpt output:', text);
            },
            read: (x) => {
                // Handle file reads (blocked for security)
                throw new Error('File I/O is not allowed');
            }
        });

        // Execute the script using Skulpt's asyncToPromise
        Sk.misceval.asyncToPromise(() => {
            return Sk.importMainWithBody('<stdin>', false, script, true);
        })
        .then(() => {
            // Script executed successfully, return command queue
            resolve(commandQueue);
        })
        .catch(err => {
            // Script execution failed
            reject(new Error(`Script execution error: ${err.toString()}`));
        });
    });
}

/**
 * Get the current command queue (for testing/debugging)
 * @returns {Array} Current command queue
 */
export function getCommandQueue() {
    return commandQueue;
}

/**
 * Clear the command queue
 */
export function clearCommandQueue() {
    commandQueue = [];
}
