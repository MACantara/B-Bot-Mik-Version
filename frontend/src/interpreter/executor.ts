import type { ASTNode } from './parser';
import { useGameStore } from '../store/gameStore';

const MAX_EXECUTION_STEPS = 500;
const EXECUTION_DELAY_MS = 300;

export async function executeScript(
  nodes: ASTNode[],
  onStepComplete?: (step: number, total: number) => void,
  onError?: (error: string) => void
): Promise<void> {
  const store = useGameStore.getState();
  store.setRunning(true);
  store.clearConsole();

  if (nodes.length > MAX_EXECUTION_STEPS) {
    const error = `Script exceeds maximum execution limit of ${MAX_EXECUTION_STEPS} steps`;
    store.addConsoleOutput(error);
    if (onError) onError(error);
    store.setRunning(false);
    return;
  }

  try {
    for (let i = 0; i < nodes.length; i++) {
      const node = nodes[i];

      if (node.object !== 'bbot') {
        throw new Error(`Unknown object '${node.object}' at line ${node.line}`);
      }

      const validMethods = ['move', 'turn', 'harvest', 'build'];
      if (!validMethods.includes(node.method)) {
        throw new Error(`Unknown method '${node.method}' at line ${node.line}`);
      }

      store.executeBotAction(node.method);

      if (onStepComplete) {
        onStepComplete(i + 1, nodes.length);
      }

      await new Promise(resolve => setTimeout(resolve, EXECUTION_DELAY_MS));
    }

    store.addConsoleOutput('Script execution completed successfully');
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
    store.addConsoleOutput(`Error: ${errorMessage}`);
    if (onError) onError(errorMessage);
  } finally {
    store.setRunning(false);
  }
}
