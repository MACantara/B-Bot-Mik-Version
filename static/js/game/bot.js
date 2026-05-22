// Bot sprite, movement, and animation

import { getGridContainer } from './pixi-renderer.js';

let botSprite;
let botState = { x: 0, y: 0, direction: 'RIGHT' };

const ICON_SVGS = {
    BOT: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z"/><path d="M8.5 2h7"/><path d="M12 2v6"/><path d="M19 10a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2Z"/><path d="M8 10v4"/><path d="M16 10v4"/><path d="M12 14v4"/></svg>`
};

export function createBotSprite(x, y, cellSize) {
    const container = getGridContainer();
    if (!container) return;
    
    const svgString = ICON_SVGS.BOT;
    const svgTexture = PIXI.Texture.from(svgString);
    botSprite = new PIXI.Sprite(svgTexture);
    botSprite.x = x * cellSize + 5;
    botSprite.y = y * cellSize + 5;
    botSprite.width = 20;
    botSprite.height = 20;
    botSprite.tint = 0x000000;
    container.addChild(botSprite);
    
    botState = { x, y, direction: 'RIGHT' };
}

export function updateBotPosition(targetX, targetY, cellSize) {
    if (!botSprite) return;
    
    botState.x = targetX;
    botState.y = targetY;
    
    const pixelX = targetX * cellSize + 5;
    const pixelY = targetY * cellSize + 5;
    
    // Smooth lerp animation
    const animate = () => {
        const dx = pixelX - botSprite.x;
        const dy = pixelY - botSprite.y;
        
        if (Math.abs(dx) < 0.5 && Math.abs(dy) < 0.5) {
            botSprite.x = pixelX;
            botSprite.y = pixelY;
            return;
        }
        
        botSprite.x += dx * 0.2;
        botSprite.y += dy * 0.2;
        requestAnimationFrame(animate);
    };
    
    animate();
}

export function getBotState() {
    return botState;
}

export function setBotDirection(direction) {
    botState.direction = direction;
}
