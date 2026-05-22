// Three.js renderer initialization

let scene;
let camera;
let renderer;
let controls;
let gridContainer;

export function initThreeJS(containerId, width, height) {
    const container = document.getElementById(containerId);
    if (!container) return null;
    
    // Use window dimensions for full screen
    const actualWidth = window.innerWidth;
    const actualHeight = window.innerHeight;
    
    // Create scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf0f0f0);
    
    // Create camera (perspective)
    camera = new THREE.PerspectiveCamera(
        60, // FOV
        actualWidth / actualHeight, // aspect ratio
        0.1, // near
        1000 // far
    );
    
    // Set initial camera position
    camera.position.set(15, 20, 15);
    camera.lookAt(0, 0, 0);
    
    // Create renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(actualWidth, actualHeight);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    container.appendChild(renderer.domElement);
    
    // Add orbit controls
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.minDistance = 5;
    controls.maxDistance = 50;
    controls.maxPolarAngle = Math.PI / 2.2; // Prevent going below ground
    
    // Add lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(10, 20, 10);
    directionalLight.castShadow = true;
    directionalLight.shadow.mapSize.width = 2048;
    directionalLight.shadow.mapSize.height = 2048;
    directionalLight.shadow.camera.near = 0.5;
    directionalLight.shadow.camera.far = 50;
    directionalLight.shadow.camera.left = -25;
    directionalLight.shadow.camera.right = 25;
    directionalLight.shadow.camera.top = 25;
    directionalLight.shadow.camera.bottom = -25;
    scene.add(directionalLight);
    
    // Create grid container
    gridContainer = new THREE.Group();
    scene.add(gridContainer);
    
    // Add ground plane
    const groundGeometry = new THREE.PlaneGeometry(100, 100);
    const groundMaterial = new THREE.MeshStandardMaterial({ 
        color: 0xe0e0e0,
        roughness: 0.8
    });
    const ground = new THREE.Mesh(groundGeometry, groundMaterial);
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -0.1;
    ground.receiveShadow = true;
    scene.add(ground);
    
    // Start animation loop
    animate();
    
    // Handle window resize
    window.addEventListener('resize', onWindowResize);
    
    return { scene, camera, renderer, controls, gridContainer };
}

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}

function onWindowResize() {
    const container = renderer.domElement.parentElement;
    if (container) {
        const width = container.clientWidth;
        const height = container.clientHeight;
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height);
    }
}

export function getGridContainer() {
    return gridContainer;
}

export function getScene() {
    return scene;
}

export function getCamera() {
    return camera;
}

export function getRenderer() {
    return renderer;
}

export function getControls() {
    return controls;
}
