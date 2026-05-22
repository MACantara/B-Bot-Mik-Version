// PixiJS Application initialization

let app;
let gridContainer;

export function initPixiJS(containerId, width, height) {
    const container = document.getElementById(containerId);
    if (!container) return null;
    
    app = new PIXI.Application({
        width: width,
        height: height,
        backgroundColor: 0xffffff,
        antialias: true
    });
    
    container.appendChild(app.view);
    
    // Create main grid container (camera)
    gridContainer = new PIXI.Container();
    app.stage.addChild(gridContainer);
    
    return { app, gridContainer };
}

export function getGridContainer() {
    return gridContainer;
}

export function getApp() {
    return app;
}
