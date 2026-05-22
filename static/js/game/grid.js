// Grid rendering and tile management

import { getGridContainer } from './pixi-renderer.js';

const TILE_COLORS = {
    EMPTY: 0xf0f0f0,
    TREE: 0x90EE90,
    ROCK: 0x808080,
    ROAD: 0x404040,
    RESIDENTIAL: 0xFFD700,
    COMMERCIAL: 0x4169E1,
    INDUSTRIAL: 0xB22222
};

const ICON_SVGS = {
    TREE: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m4 22 4-10a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2l4 10"/><path d="M12 2v20"/><path d="M12 2a7 7 0 0 1 7 7c0 5-2 8-7 12-5-4-7-7-7-12a7 7 0 0 1 7-7z"/></svg>`,
    ROCK: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m8 3 4 8 5-5 5 15H2L8 3z"/></svg>`,
    RESIDENTIAL: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>`,
    COMMERCIAL: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="20" x="4" y="2" rx="2" ry="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01"/><path d="M16 6h.01"/><path d="M12 6h.01"/><path d="M12 10h.01"/><path d="M12 14h.01"/><path d="M16 10h.01"/><path d="M16 14h.01"/><path d="M8 10h.01"/><path d="M8 14h.01"/></svg>`,
    INDUSTRIAL: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 20a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8l-7 5V8l-7 5V4a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M17 18h1"/><path d="M12 18h1"/><path d="M7 18h1"/></svg>`
};

export function renderGrid(grid, cellSize) {
    const container = getGridContainer();
    if (!container) return;
    
    // Clear existing grid
    container.removeChildren();
    
    const gridSize = grid.length;
    
    // Draw grid cells
    for (let y = 0; y < gridSize; y++) {
        for (let x = 0; x < gridSize; x++) {
            const cellData = grid[y] && grid[y][x] ? grid[y][x] : { type: 'EMPTY', id: `${x}-${y}` };
            
            const graphics = new PIXI.Graphics();
            const color = TILE_COLORS[cellData.type] || TILE_COLORS.EMPTY;
            
            graphics.beginFill(color);
            graphics.drawRect(x * cellSize, y * cellSize, cellSize, cellSize);
            graphics.endFill();
            
            // Add grid border
            graphics.lineStyle(1, 0xcccccc);
            graphics.drawRect(x * cellSize, y * cellSize, cellSize, cellSize);
            
            container.addChild(graphics);
            
            // Add SVG icons for different tile types
            if (ICON_SVGS[cellData.type]) {
                const svgString = ICON_SVGS[cellData.type];
                const svgTexture = PIXI.Texture.from(svgString);
                const iconSprite = new PIXI.Sprite(svgTexture);
                iconSprite.x = x * cellSize + 7;
                iconSprite.y = y * cellSize + 7;
                iconSprite.width = 16;
                iconSprite.height = 16;
                iconSprite.tint = 0x333333;
                container.addChild(iconSprite);
            }
        }
    }
}

export function getTileColors() {
    return TILE_COLORS;
}
