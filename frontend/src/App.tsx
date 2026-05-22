import { useState, useEffect } from 'react';
import { Dashboard } from './components/Dashboard';
import { CodeEditor } from './components/CodeEditor';
import { GridVisualizer } from './components/GridVisualizer';
import { Console } from './components/Console';
import { useGameStore } from './store/gameStore';
import { createLexer } from './interpreter/lexer';
import { createParser } from './interpreter/parser';
import { executeScript } from './interpreter/executor';
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
  const { isRunning, initializeLevel, clearConsole } = useGameStore();

  useEffect(() => {
    // Initialize with demo grid
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
  }, [initializeLevel]);

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
