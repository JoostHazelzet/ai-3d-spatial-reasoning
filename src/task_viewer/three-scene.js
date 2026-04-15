// Three.js scene management for 3D voxel visualization
class ThreeScene {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        
        if (!this.container) {
            console.error('ThreeScene: Container not found:', containerId);
            return;
        }
        
        console.log('ThreeScene: Container found', {
            width: this.container.clientWidth,
            height: this.container.clientHeight,
            visible: this.container.offsetParent !== null
        });
        
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.labelRenderer = null;
        this.controls = null;
        this.voxelMeshes = [];
        this.labels = [];
        this.currentSize = 5;
        
        this.init();
    }
    
    init() {
        console.log('ThreeScene.init() starting...');
        
        // Create scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x1a1a1a);
        console.log('Scene created');
        
        // Create camera
        const aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera = new THREE.PerspectiveCamera(50, aspect, 0.1, 1000);
        this.camera.position.set(15, 15, 15);
        this.camera.lookAt(0, 0, 0);
        console.log('Camera created');
        
        // Create renderer
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.container.appendChild(this.renderer.domElement);
        console.log('Renderer created and added to container');
        
        // Create CSS2D renderer for labels
        this.labelRenderer = new THREE.CSS2DRenderer();
        this.labelRenderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.labelRenderer.domElement.style.position = 'absolute';
        this.labelRenderer.domElement.style.top = '0';
        this.labelRenderer.domElement.style.pointerEvents = 'none';
        this.container.appendChild(this.labelRenderer.domElement);
        console.log('Label renderer created');
        
        // Add orbit controls
        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        console.log('OrbitControls created');
        
        // Add lights
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        this.scene.add(ambientLight);
        
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(10, 10, 10);
        this.scene.add(directionalLight);
        
        const directionalLight2 = new THREE.DirectionalLight(0xffffff, 0.4);
        directionalLight2.position.set(-10, -10, -10);
        this.scene.add(directionalLight2);
        console.log('Lights added');
        
        // Add grid helper
        this.updateGridHelper(5);
        
        // Add face labels
        this.createLabels(5);
        console.log('Grid and labels created');
        
        // Handle window resize
        window.addEventListener('resize', () => this.onWindowResize());
        
        // Start animation loop
        this.animate();
        console.log('ThreeScene.init() complete - animation started');
    }
    
    updateGridHelper(size) {
        // Remove old grid
        const oldGrid = this.scene.getObjectByName('gridHelper');
        if (oldGrid) this.scene.remove(oldGrid);
        
        // Create 3D grid showing all voxel cell boundaries
        const gridLines = [];
        const darkGray = 0x3c3c3c;
        
        // Voxels are centered at integer positions 0 to size-1
        // Grid lines are at -0.5, 0.5, 1.5, ..., size-0.5
        for (let i = 0; i <= size; i++) {
            const pos = i - 0.5;
            
            // Lines parallel to X axis (varying Y and Z)
            for (let j = 0; j <= size; j++) {
                const pos2 = j - 0.5;
                gridLines.push(new THREE.Vector3(-0.5, pos, pos2));
                gridLines.push(new THREE.Vector3(size - 0.5, pos, pos2));
            }
            
            // Lines parallel to Y axis (varying X and Z)
            for (let j = 0; j <= size; j++) {
                const pos2 = j - 0.5;
                gridLines.push(new THREE.Vector3(pos, -0.5, pos2));
                gridLines.push(new THREE.Vector3(pos, size - 0.5, pos2));
            }
            
            // Lines parallel to Z axis (varying X and Y)
            for (let j = 0; j <= size; j++) {
                const pos2 = j - 0.5;
                gridLines.push(new THREE.Vector3(pos, pos2, -0.5));
                gridLines.push(new THREE.Vector3(pos, pos2, size - 0.5));
            }
        }
        
        const gridGeometry = new THREE.BufferGeometry().setFromPoints(gridLines);
        const gridMaterial = new THREE.LineBasicMaterial({ color: darkGray });
        const grid = new THREE.LineSegments(gridGeometry, gridMaterial);
        grid.name = 'gridHelper';
        this.scene.add(grid);
    }
    
    createLabels(size) {
        // Remove old labels
        this.labels.forEach(label => this.scene.remove(label));
        this.labels = [];
        
        const center = (size - 1) / 2;
        const offset = size * 0.6;
        
        // Create label helper function
        const createLabel = (text, position) => {
            const div = document.createElement('div');
            div.className = 'face-label';
            div.textContent = text;
            
            const label = new THREE.CSS2DObject(div);
            label.position.copy(position);
            this.scene.add(label);
            this.labels.push(label);
        };
        
        // Bottom label (negative Y)
        createLabel('Bottom', new THREE.Vector3(center, -offset, center));
        
        // Front label (positive Z)
        createLabel('Front', new THREE.Vector3(center, center, size + offset - 1));
        
        // Right label (positive X)
        createLabel('Right', new THREE.Vector3(size + offset - 1, center, center));
        
        // Back label (negative Z)
        createLabel('Back', new THREE.Vector3(center, center, -offset));
        
        // Top label (positive Y)
        createLabel('Top', new THREE.Vector3(center, size + offset - 1, center));
        
        // Left label (negative X)
        createLabel('Left', new THREE.Vector3(-offset, center, center));
    }
    
    updateScene(voxelData, size) {
        this.currentSize = size;
        
        console.log('ThreeScene.updateScene called with size:', size);
        console.log('VoxelData sample:', voxelData[0]?.[0]?.[0]);
        
        // Remove old voxels
        this.voxelMeshes.forEach(mesh => this.scene.remove(mesh));
        this.voxelMeshes = [];
        
        // Update grid and labels
        this.updateGridHelper(size);
        this.createLabels(size);
        
        // Create voxel geometry (no gaps - full size)
        const geometry = new THREE.BoxGeometry(1.0, 1.0, 1.0);
        
        // Create edges geometry for white lines
        const edges = new THREE.EdgesGeometry(geometry);
        const edgeMaterial = new THREE.LineBasicMaterial({ color: 0xffffff, linewidth: 1 });
        
        let voxelCount = 0;
        
        // Add voxels (rotate so Z points up: x->x, y->z, z->y)
        for (let x = 0; x < size; x++) {
            for (let y = 0; y < size; y++) {
                for (let z = 0; z < size; z++) {
                    const colorNum = voxelData[x][y][z];
                    if (!isTransparent(colorNum)) {
                        voxelCount++;
                        const color = getThreeColor(colorNum);
                        const material = new THREE.MeshStandardMaterial({ 
                            color: color,
                            metalness: 0.3,
                            roughness: 0.7
                        });
                        
                        const mesh = new THREE.Mesh(geometry, material);
                        // Rotate coordinate system to match matplotlib (Z up, right-handed)
                        // Matplotlib: voxels[x][y][z] → world(x, y, z) with Z up
                        // Three.js: need to map to (x, z, size-1-y) to flip Y direction
                        mesh.position.set(x, z, size - 1 - y);
                        
                        // Add white edges
                        const edgeMesh = new THREE.LineSegments(edges, edgeMaterial);
                        mesh.add(edgeMesh);
                        
                        this.scene.add(mesh);
                        this.voxelMeshes.push(mesh);
                    }
                }
            }
        }
        
        console.log('Created', voxelCount, 'voxel meshes');
        
        // Adjust camera to fit scene (Z points up, matches matplotlib)
        const distance = size * 2.0;
        const center = (size - 1) / 2; // Center of the voxel space
        this.camera.position.set(distance, distance, distance);
        this.camera.lookAt(center, center, center);
        this.controls.target.set(center, center, center);
        this.controls.update();
    }
    
    onWindowResize() {
        const aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera.aspect = aspect;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.labelRenderer.setSize(this.container.clientWidth, this.container.clientHeight);
    }
    
    resetView() {
        const size = this.currentSize;
        const distance = size * 2.0;
        const center = (size - 1) / 2;
        this.camera.position.set(distance, distance, distance);
        this.camera.lookAt(center, center, center);
        this.controls.target.set(center, center, center);
        this.controls.update();
    }
    
    updateLabelBrightness() {
        if (!this.labels || this.labels.length === 0) return;
        
        // Calculate distances from camera to each label
        const distances = this.labels.map(label => {
            return this.camera.position.distanceTo(label.position);
        });
        
        // Find min and max distances for normalization
        const minDist = Math.min(...distances);
        const maxDist = Math.max(...distances);
        const range = maxDist - minDist;
        
        // Update each label's brightness
        this.labels.forEach((label, i) => {
            const dist = distances[i];
            // Normalize distance to 0-1 range, then invert (closer = brighter)
            const normalized = range > 0 ? 1 - (dist - minDist) / range : 1;
            // Map to brightness range (0.3 to 1.0 for visibility)
            const brightness = 0.3 + normalized * 0.7;
            
            // Apply brightness through opacity and color lightness
            const div = label.element;
            div.style.opacity = brightness;
        });
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        this.controls.update();
        this.updateLabelBrightness();
        this.renderer.render(this.scene, this.camera);
        this.labelRenderer.render(this.scene, this.camera);
    }
}
