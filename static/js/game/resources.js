// Resource tracking and display updates

let resources = { wood: 0, stone: 0, metal: 0, energy: 0 };
let population = 0;

export function updateResources(newResources) {
    resources = { ...resources, ...newResources };
    updateResourceDisplay();
}

export function updatePopulation(newPopulation) {
    population = newPopulation;
    updateResourceDisplay();
}

export function getResources() {
    return resources;
}

export function getPopulation() {
    return population;
}

export function setResources(newResources) {
    resources = newResources;
    updateResourceDisplay();
}

export function setPopulation(newPopulation) {
    population = newPopulation;
    updateResourceDisplay();
}

function updateResourceDisplay() {
    const woodCount = document.getElementById('woodCount');
    const stoneCount = document.getElementById('stoneCount');
    const metalCount = document.getElementById('metalCount');
    const energyCount = document.getElementById('energyCount');
    const populationCount = document.getElementById('populationCount');
    
    if (woodCount) woodCount.textContent = resources.wood;
    if (stoneCount) stoneCount.textContent = resources.stone;
    if (metalCount) metalCount.textContent = resources.metal;
    if (energyCount) energyCount.textContent = resources.energy;
    if (populationCount) populationCount.textContent = population;
}
