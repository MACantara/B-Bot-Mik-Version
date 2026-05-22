import React from 'react';
import { useGameStore } from '../store/gameStore';

export const Console: React.FC = () => {
  const { consoleOutput } = useGameStore();

  return (
    <div className="flex flex-col h-48 bg-gray-900 text-green-400 font-mono text-sm">
      <div className="bg-gray-800 text-white px-4 py-2 text-sm font-semibold flex justify-between items-center">
        <span>Console Output</span>
        <span className="text-xs text-gray-400">Runtime Feedback</span>
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-1">
        {consoleOutput.length === 0 ? (
          <div className="text-gray-500 italic">No output yet...</div>
        ) : (
          consoleOutput.map((message, index) => (
            <div key={index} className="hover:bg-gray-800 px-2 py-1 rounded">
              <span className="text-gray-500 mr-2">[{index + 1}]</span>
              {message}
            </div>
          ))
        )}
      </div>
    </div>
  );
};
