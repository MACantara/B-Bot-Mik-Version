import { useState, useEffect } from 'react';
import { Dashboard } from './components/Dashboard';
import { CodeEditor } from './components/CodeEditor';
import { GridVisualizer } from './components/GridVisualizer';
import { Console } from './components/Console';
import { Login } from './components/Login';
import { Register } from './components/Register';
import { useGameStore } from './store/gameStore';
import { createLexer } from './interpreter/lexer';
import { createParser } from './interpreter/parser';
import { executeScript } from './interpreter/executor';
import { apiClient } from './lib/api';
import type { CellState } from './types/game';

const DEFAULT_CODE = `bbot.move()
bbot.move()
bbot.turn()
bbot.move()
bbot.harvest()
bbot.turn()
bbot.move()
bbot.build()`;

function App() {
  const [code, setCode] = useState(DEFAULT_CODE);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [authView, setAuthView] = useState<'login' | 'register'>('login');
  const { isRunning, initializeLevel, clearConsole, grid, bot, population } = useGameStore();

  useEffect(() => {
    // Check if user is already authenticated
    if (apiClient['accessToken']) {
      setIsAuthenticated(true);
      loadSavedState();
    } else {
      // Initialize with demo grid for non-authenticated users
      initializeDemoGrid();
    }
  }, []);

  const initializeDemoGrid = () => {
    const demoGrid: CellState[][] = [];
    for (let y = 0; y < 10; y++) {
      const row: CellState[] = [];
      for (let x = 0; x < 10; x++) {
        if ([2, 5, 8, 1, 6].includes(x) && [3, 7, 2, 8, 4].includes(y)) {
          row.push({ type: 'TREE', id: `${x}-${y}` });
        } else if ([3, 7, 4, 9, 2].includes(x) && [1, 5, 8, 3, 6].includes(y)) {
          row.push({ type: 'ROCK', id: `${x}-${y}` });
        } else {
          row.push({ type: 'EMPTY', id: `${x}-${y}` });
        }
      }
      demoGrid.push(row);
    }
    initializeLevel(demoGrid);
  };

  const loadSavedState = async () => {
    try {
      const savedState = await apiClient.getSavedState();
      initializeLevel(savedState.grid_json);
      useGameStore.getState().setBotInventory(savedState.wood_count, savedState.stone_count);
      useGameStore.getState().setPopulation(savedState.population_count);
    } catch (err) {
      // If no saved state, initialize demo grid
      initializeDemoGrid();
    }
  };

  const handleSave = async () => {
    try {
      await apiClient.saveSimulationState({
        grid_json: grid,
        wood_count: bot.inventory.wood,
        stone_count: bot.inventory.stone,
        population_count: population,
      });
      useGameStore.getState().addConsoleOutput('Game saved successfully!');
    } catch (err) {
      useGameStore.getState().addConsoleOutput(`Save failed: ${err instanceof Error ? err.message : 'Unknown error'}`);
    }
  };

  const handleLoad = async () => {
    try {
      await loadSavedState();
      useGameStore.getState().addConsoleOutput('Game loaded successfully!');
    } catch (err) {
      useGameStore.getState().addConsoleOutput(`Load failed: ${err instanceof Error ? err.message : 'Unknown error'}`);
    }
  };

  const handleLogout = () => {
    apiClient.clearTokens();
    setIsAuthenticated(false);
    initializeDemoGrid();
  };

  const handleRunCode = async () => {
    if (isRunning) return;

    clearConsole();

    try {
      const lexer = createLexer(code);
      const tokens = lexer.tokenize();

      const parser = createParser(tokens);
      const ast = parser.parse();

      await executeScript(ast);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      useGameStore.getState().addConsoleOutput(`Syntax Error: ${errorMessage}`);
    }
  };

  const handleReset = () => {
    useGameStore.getState().resetGame();
    initializeDemoGrid();
  };

  if (!isAuthenticated) {
    if (authView === 'login') {
      return (
        <Login
          onLogin={() => setIsAuthenticated(true)}
          onSwitchToRegister={() => setAuthView('register')}
        />
      );
    }
    return (
      <Register
        onRegister={() => setIsAuthenticated(true)}
        onSwitchToLogin={() => setAuthView('login')}
      />
    );
  }

  return (
    <div className="h-screen flex flex-col bg-gray-100">
      <Dashboard />
      <div className="flex-1 flex overflow-hidden">
        <div className="w-1/2 flex flex-col border-r border-gray-300">
          <CodeEditor code={code} onChange={setCode} disabled={isRunning} />
          <Console />
          <div className="p-4 bg-gray-800 border-t border-gray-700 flex gap-4">
            <button
              onClick={handleRunCode}
              disabled={isRunning}
              className="flex-1 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 text-white font-bold py-3 px-6 rounded transition-colors"
            >
              {isRunning ? 'Running...' : 'Run Code'}
            </button>
            <button
              onClick={handleReset}
              disabled={isRunning}
              className="flex-1 bg-red-600 hover:bg-red-700 disabled:bg-gray-600 text-white font-bold py-3 px-6 rounded transition-colors"
            >
              Reset
            </button>
            {isAuthenticated && (
              <>
                <button
                  onClick={handleSave}
                  disabled={isRunning}
                  className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white font-bold py-3 px-6 rounded transition-colors"
                >
                  Save
                </button>
                <button
                  onClick={handleLoad}
                  disabled={isRunning}
                  className="flex-1 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-white font-bold py-3 px-6 rounded transition-colors"
                >
                  Load
                </button>
                <button
                  onClick={handleLogout}
                  disabled={isRunning}
                  className="flex-1 bg-gray-600 hover:bg-gray-700 disabled:bg-gray-600 text-white font-bold py-3 px-6 rounded transition-colors"
                >
                  Logout
                </button>
              </>
            )}
          </div>
        </div>
        <div className="w-1/2">
          <GridVisualizer />
        </div>
      </div>
    </div>
  );
}

export default App;
