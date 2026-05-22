export type Direction = 'UP' | 'DOWN' | 'LEFT' | 'RIGHT';
export type CellType = 'EMPTY' | 'TREE' | 'ROCK' | 'HOUSE';

export interface BotState {
  x: number;
  y: number;
  direction: Direction;
  inventory: { wood: number; stone: number };
}

export interface CellState {
  type: CellType;
  id: string;
}

export interface GameStore {
  grid: CellState[][];
  bot: BotState;
  population: number;
  isRunning: boolean;
  consoleOutput: string[];
  initializeLevel: (mapData: CellState[][]) => void;
  executeBotAction: (actionType: string) => void;
  setRunning: (running: boolean) => void;
  addConsoleOutput: (message: string) => void;
  clearConsole: () => void;
  resetGame: () => void;
}
