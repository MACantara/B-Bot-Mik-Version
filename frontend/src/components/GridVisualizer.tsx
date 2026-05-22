import React from 'react';
import { useGameStore } from '../store/gameStore';
import type { CellType, Direction } from '../types/game';

const getCellColor = (type: CellType): string => {
  switch (type) {
    case 'EMPTY':
      return 'bg-gray-200';
    case 'TREE':
      return 'bg-green-500';
    case 'ROCK':
      return 'bg-gray-500';
    case 'HOUSE':
      return 'bg-blue-500';
    default:
      return 'bg-gray-200';
  }
};

const getCellIcon = (type: CellType): string => {
  switch (type) {
    case 'TREE':
      return '🌲';
    case 'ROCK':
      return '🪨';
    case 'HOUSE':
      return '🏠';
    default:
      return '';
  }
};

const getBotArrow = (direction: Direction): string => {
  switch (direction) {
    case 'UP':
      return '↑';
    case 'DOWN':
      return '↓';
    case 'LEFT':
      return '←';
    case 'RIGHT':
      return '→';
    default:
      return '→';
  }
};

export const GridVisualizer: React.FC = () => {
  const { grid, bot } = useGameStore();

  return (
    <div className="flex flex-col h-full">
      <div className="bg-gray-800 text-white px-4 py-2 text-sm font-semibold">
        City Map (10x10)
      </div>
      <div className="flex-1 p-4 overflow-auto bg-gray-100">
        <div className="grid grid-cols-10 grid-rows-10 gap-1 w-full max-w-2xl mx-auto aspect-square">
          {grid.map((row, y) =>
            row.map((cell, x) => {
              const isBotPosition = bot.x === x && bot.y === y;
              return (
                <div
                  key={cell.id}
                  className={`
                    ${getCellColor(cell.type)}
                    flex items-center justify-center
                    text-2xl font-bold
                    border border-gray-300
                    rounded-sm
                    transition-all duration-200
                    ${isBotPosition ? 'ring-4 ring-yellow-400 ring-inset' : ''}
                  `}
                >
                  {isBotPosition ? (
                    <span className="text-3xl">{getBotArrow(bot.direction)}</span>
                  ) : (
                    getCellIcon(cell.type)
                  )}
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
};
