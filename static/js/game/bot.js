// Bot sprite, movement, and animation

import { getGridContainer } from './three-renderer.js';

let botGroup;
let botState = { x: 0, y: 0, direction: 'RIGHT' };

export function createBotSprite(x, y, cellSize) {
    const container = getGridContainer();
    if (!container) return;
    
    // Remove existing bot group if it exists
    if (botGroup) {
        container.remove(botGroup);
        // Dispose of geometries and materials
        botGroup.traverse((child) => {
            if (child.geometry) child.geometry.dispose();
            if (child.material) {
                if (Array.isArray(child.material)) {
                    child.material.forEach(m => m.dispose());
                } else {
                    child.material.dispose();
                }
            }
        });
    }
    
    // Create bot group
    botGroup = new THREE.Group();
    
    const gridSize = 20; // Assuming 20x20 grid
    const offset = (gridSize * cellSize) / 2;
    
    // Bot body (cube)
    const bodyGeometry = new THREE.BoxGeometry(0.6, 0.5, 0.4);
    const bodyMaterial = new THREE.MeshStandardMaterial({ color: 0x333333 });
    const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
    body.position.y = 0.5;
    body.castShadow = true;
    botGroup.add(body);
    
    // Bot head (cube)
    const headGeometry = new THREE.BoxGeometry(0.4, 0.4, 0.4);
    const headMaterial = new THREE.MeshStandardMaterial({ color: 0x555555 });
    const head = new THREE.Mesh(headGeometry, headMaterial);
    head.position.y = 0.95;
    head.castShadow = true;
    botGroup.add(head);
    
    // Bot eyes (small spheres)
    const eyeGeometry = new THREE.SphereGeometry(0.05, 8, 8);
    const eyeMaterial = new THREE.MeshStandardMaterial({ color: 0x00ff00, emissive: 0x00ff00, emissiveIntensity: 0.5 });
    
    const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
    leftEye.position.set(-0.1, 1.0, 0.2);
    botGroup.add(leftEye);
    
    const rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
    rightEye.position.set(0.1, 1.0, 0.2);
    botGroup.add(rightEye);
    
    // Bot arms (cylinders)
    const armGeometry = new THREE.CylinderGeometry(0.08, 0.08, 0.4, 8);
    const armMaterial = new THREE.MeshStandardMaterial({ color: 0x444444 });
    
    const leftArm = new THREE.Mesh(armGeometry, armMaterial);
    leftArm.position.set(-0.4, 0.5, 0);
    leftArm.rotation.z = Math.PI / 4;
    leftArm.castShadow = true;
    botGroup.add(leftArm);
    
    const rightArm = new THREE.Mesh(armGeometry, armMaterial);
    rightArm.position.set(0.4, 0.5, 0);
    rightArm.rotation.z = -Math.PI / 4;
    rightArm.castShadow = true;
    botGroup.add(rightArm);
    
    // Position bot on grid
    botGroup.position.set(x * cellSize - offset, 0, y * cellSize - offset);
    
    container.add(botGroup);
    
    botState = { x, y, direction: 'RIGHT' };
}

export function updateBotPosition(targetX, targetY, cellSize) {
    if (!botGroup) return;
    
    const gridSize = 20;
    const offset = (gridSize * cellSize) / 2;
    
    // Direct position update (no animation - let AnimationEngine handle that)
    botGroup.position.set(
        targetX * cellSize - offset,
        0,
        targetY * cellSize - offset
    );
}

export function getBotState() {
    return botState;
}

export function setBotDirection(direction) {
    botState.direction = direction;
    
    if (!botGroup) return;
    
    // Rotate bot to face direction
    const rotations = {
        'UP': Math.PI,
        'RIGHT': -Math.PI / 2,
        'DOWN': 0,
        'LEFT': Math.PI / 2
    };
    
    botGroup.rotation.y = rotations[direction] || 0;
}

