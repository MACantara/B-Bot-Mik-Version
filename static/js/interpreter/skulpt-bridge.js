// Skulpt.js Bridge for Client-Side Python Execution
// This module configures Skulpt and provides the bot object FFI bridge

// Command queue array - stores bot commands generated from Python execution
let commandQueue = [];

/**
 * Execute a Python script using Skulpt
 * @param {string} script - The Python script string to execute
 * @returns {Promise<Array>} Promise resolving to the command queue array
 * @throws {Error} If script execution fails
 */
export function executeScript(script) {
    return new Promise((resolve, reject) => {
        // Ensure Skulpt is loaded
        if (typeof Sk === 'undefined') {
            reject(new Error('Skulpt is not loaded'));
            return;
        }
        
        // Configure Skulpt following official documentation pattern
        function builtinRead(x) {
            if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined) {
                throw "File not found: '" + x + "'";
            }
            return Sk.builtinFiles["files"][x];
        }
        
        function outf(text) {
            console.log('Skulpt output:', text);
        }
        
        Sk.configure({ output: outf, read: builtinRead });
        
        // Create bot object for this execution
        const bot = {
            move: new Sk.builtin.func(() => {
                commandQueue.push({ action: 'MOVE' });
                return Sk.builtin.none.none$;
            }),
            turn_left: new Sk.builtin.func(() => {
                commandQueue.push({ action: 'TURN_LEFT' });
                return Sk.builtin.none.none$;
            }),
            turn_right: new Sk.builtin.func(() => {
                commandQueue.push({ action: 'TURN_RIGHT' });
                return Sk.builtin.none.none$;
            }),
            harvest: new Sk.builtin.func(() => {
                commandQueue.push({ action: 'HARVEST' });
                return Sk.builtin.none.none$;
            }),
            build: new Sk.builtin.func((buildType) => {
                const type = Sk.ffi.remapToJs(buildType);
                commandQueue.push({ action: 'BUILD', type: type });
                return Sk.builtin.none.none$;
            })
        };
        
        // Reset command queue for new execution
        commandQueue = [];

        // Inject bot object into Skulpt's global scope
        Sk.builtins.bot = bot;

        // Execute the script using Skulpt's asyncToPromise
        Sk.misceval.asyncToPromise(() => {
            return Sk.importMainWithBody('<stdin>', false, script, true);
        })
        .then(() => {
            // Clean up bot from builtins after execution
            delete Sk.builtins.bot;
            
            // Script executed successfully, return command queue
            resolve(commandQueue);
        })
        .catch(err => {
            // Clean up bot from builtins on error
            delete Sk.builtins.bot;
            
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
