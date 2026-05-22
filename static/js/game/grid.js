// Grid rendering and tile management

import { getGridContainer } from './three-renderer.js';

const TILE_COLORS = {
    EMPTY: 0xf0f0f0,
    TREE: 0x90EE90,
    ROCK: 0x808080,
    ROAD: 0x404040,
    RESIDENTIAL: 0xFFD700,
    COMMERCIAL: 0x4169E1,
    INDUSTRIAL: 0xB22222
};

const TILE_HEIGHTS = {
    EMPTY: 0.1,
    TREE: 1.5,
    ROCK: 0.8,
    ROAD: 0.1,
    RESIDENTIAL: 2,
    COMMERCIAL: 4,
    INDUSTRIAL: 3
};

export function renderGrid(grid, cellSize) {
    const container = getGridContainer();
    if (!container) return;
    
    // Clear existing grid
    while (container.children.length > 0) {
        const child = container.children[0];
        if (child.geometry) child.geometry.dispose();
        if (child.material) {
            if (Array.isArray(child.material)) {
                child.material.forEach(m => m.dispose());
            } else {
                child.material.dispose();
            }
        }
        container.remove(child);
    }
    
    const gridSize = grid.length;
    const offset = (gridSize * cellSize) / 2;
    
    // Draw grid cells
    for (let y = 0; y < gridSize; y++) {
        for (let x = 0; x < gridSize; x++) {
            const cellData = grid[y] && grid[y][x] ? grid[y][x] : { type: 'EMPTY', id: `${x}-${y}` };
            
            const color = TILE_COLORS[cellData.type] || TILE_COLORS.EMPTY;
            const height = TILE_HEIGHTS[cellData.type] || 0.1;
            
            // Create 3D tile geometry
            let geometry;
            let material;
            
            if (cellData.type === 'TREE') {
                // Tree: cylinder trunk + cone foliage
                const trunkGeometry = new THREE.CylinderGeometry(0.1, 0.15, 0.5, 8);
                const trunkMaterial = new THREE.MeshStandardMaterial({ color: 0x8B4513 });
                const trunk = new THREE.Mesh(trunkGeometry, trunkMaterial);
                trunk.position.set(x * cellSize - offset, 0.25, y * cellSize - offset);
                trunk.castShadow = true;
                container.add(trunk);
                
                const foliageGeometry = new THREE.ConeGeometry(0.6, 1.2, 8);
                const foliageMaterial = new THREE.MeshStandardMaterial({ color: color });
                const foliage = new THREE.Mesh(foliageGeometry, foliageMaterial);
                foliage.position.set(x * cellSize - offset, 1.1, y * cellSize - offset);
                foliage.castShadow = true;
                container.add(foliage);
                
            } else if (cellData.type === 'ROCK') {
                // Rock: irregular dodecahedron
                geometry = new THREE.DodecahedronGeometry(0.4);
                material = new THREE.MeshStandardMaterial({ color: color, roughness: 0.9 });
                const rock = new THREE.Mesh(geometry, material);
                rock.position.set(x * cellSize - offset, 0.4, y * cellSize - offset);
                rock.castShadow = true;
                container.add(rock);
                
            } else {
                // Standard tiles: box geometry
                geometry = new THREE.BoxGeometry(cellSize - 0.1, height, cellSize - 0.1);
                material = new THREE.MeshStandardMaterial({ 
                    color: color,
                    roughness: 0.7
                });
                const tile = new THREE.Mesh(geometry, material);
                tile.position.set(x * cellSize - offset, height / 2, y * cellSize - offset);
                tile.castShadow = true;
                tile.receiveShadow = true;
                container.add(tile);
            }
        }
    }
}

export function getTileColors() {
    return TILE_COLORS;
}
