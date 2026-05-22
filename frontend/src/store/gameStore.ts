import { create } from 'zustand';
import type { GameStore, BotState, CellState, Direction } from '../types/game';

const createEmptyGrid = (): CellState[][] => {
  const grid: CellState[][] = [];
  for (let y = 0; y < 10; y++) {
    const row: CellState[] = [];
    for (let x = 0; x < 10; x++) {
      row.push({ type: 'EMPTY', id: `${x}-${y}` });
    }
    grid.push(row);
  }
  return grid;
};

const createInitialBot = (): BotState => ({
  x: 0,
  y: 0,
  direction: 'RIGHT',
  inventory: { wood: 0, stone: 0 },
});

export const useGameStore = create<GameStore>((set, get) => ({
  grid: createEmptyGrid(),
  bot: createInitialBot(),
  population: 0,
  isRunning: false,
  consoleOutput: [],

  initializeLevel: (mapData: CellState[][]) => {
    set({
      grid: mapData,
      bot: createInitialBot(),
      population: 0,
      consoleOutput: [],
    });
  },

  executeBotAction: (actionType: string) => {
    const { grid, bot } = get();
    const newBot = { ...bot };
    const newGrid = grid.map(row => row.map(cell => ({ ...cell })));
    let message = '';

    switch (actionType) {
      case 'move':
        switch (newBot.direction) {
          case 'UP':
            newBot.y = Math.max(0, newBot.y - 1);
            break;
          case 'DOWN':
            newBot.y = Math.min(9, newBot.y + 1);
            break;
          case 'LEFT':
            newBot.x = Math.max(0, newBot.x - 1);
            break;
          case 'RIGHT':
            newBot.x = Math.min(9, newBot.x + 1);
            break;
        }
        message = `Moved to (${newBot.x}, ${newBot.y})`;
        break;

      case 'turn':
        const directions: Direction[] = ['UP', 'RIGHT', 'DOWN', 'LEFT'];
        const currentIndex = directions.indexOf(newBot.direction);
        newBot.direction = directions[(currentIndex + 1) % 4];
        message = `Turned to face ${newBot.direction}`;
        break;

      case 'harvest':
        const currentCell = newGrid[newBot.y][newBot.x];
        if (currentCell.type === 'TREE') {
          newBot.inventory.wood += 1;
          newGrid[newBot.y][newBot.x] = { type: 'EMPTY', id: currentCell.id };
          message = `Harvested tree. Wood: ${newBot.inventory.wood}`;
        } else if (currentCell.type === 'ROCK') {
          newBot.inventory.stone += 1;
          newGrid[newBot.y][newBot.x] = { type: 'EMPTY', id: currentCell.id };
          message = `Harvested rock. Stone: ${newBot.inventory.stone}`;
        } else {
          message = 'Nothing to harvest here';
        }
        break;

      case 'build':
        const buildCell = newGrid[newBot.y][newBot.x];
        if (buildCell.type === 'EMPTY') {
          if (newBot.inventory.wood >= 2 && newBot.inventory.stone >= 1) {
            newBot.inventory.wood -= 2;
            newBot.inventory.stone -= 1;
            newGrid[newBot.y][newBot.x] = { type: 'HOUSE', id: buildCell.id };
            set({ population: get().population + 1 });
            message = `Built house. Population: ${get().population + 1}`;
          } else {
            message = 'Not enough resources to build (need 2 wood, 1 stone)';
          }
        } else {
          message = 'Cannot build on this cell';
        }
        break;

      default:
        message = `Unknown action: ${actionType}`;
    }

    set({ bot: newBot, grid: newGrid });
    get().addConsoleOutput(message);
  },

  setRunning: (running: boolean) => {
    set({ isRunning: running });
  },

  addConsoleOutput: (message: string) => {
    set((state) => ({
      consoleOutput: [...state.consoleOutput, message],
    }));
  },

  clearConsole: () => {
    set({ consoleOutput: [] });
  },

  resetGame: () => {
    set({
      grid: createEmptyGrid(),
      bot: createInitialBot(),
      population: 0,
      consoleOutput: [],
      isRunning: false,
    });
  },

  setBotInventory: (wood: number, stone: number) => {
    set((state) => ({
      bot: {
        ...state.bot,
        inventory: { wood, stone },
      },
    }));
  },

  setPopulation: (count: number) => {
    set({ population: count });
  },
}));
