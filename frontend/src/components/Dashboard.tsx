import React from 'react';
import { useGameStore } from '../store/gameStore';

export const Dashboard: React.FC = () => {
  const { bot, population } = useGameStore();

  return (
    <div className="bg-gray-800 text-white px-6 py-3 flex items-center justify-between">
      <div className="flex items-center space-x-8">
        <div className="flex items-center space-x-2">
          <span className="text-2xl">🪵</span>
          <div>
            <div className="text-xs text-gray-400">Wood</div>
            <div className="text-lg font-bold">{bot.inventory.wood}</div>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <span className="text-2xl">🪨</span>
          <div>
            <div className="text-xs text-gray-400">Stone</div>
            <div className="text-lg font-bold">{bot.inventory.stone}</div>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <span className="text-2xl">👥</span>
          <div>
            <div className="text-xs text-gray-400">Population</div>
            <div className="text-lg font-bold">{population}</div>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <span className="text-2xl">⚡</span>
          <div>
            <div className="text-xs text-gray-400">Energy</div>
            <div className="text-lg font-bold">100%</div>
          </div>
        </div>
      </div>
      <div className="text-sm text-gray-400">
        B-Bot City Builder
      </div>
    </div>
  );
};
