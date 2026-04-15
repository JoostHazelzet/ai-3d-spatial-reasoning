/**
 * Task Viewer - Read-only viewer for orthographic benchmark datasets
 */

class TaskViewer {
    constructor() {
        this.dataset = null;
        this.currentIndex = 0;
        this.currentTask = null;
        this.currentFilename = null;
        this.threeScene = null;
        
        this.initializeElements();
        this.attachEventListeners();
        // Don't initialize ThreeScene yet - wait until first task is loaded
    }

    initializeElements() {
        // Buttons
        this.loadBtn = document.getElementById('loadBtn');
        this.firstBtn = document.getElementById('firstBtn');
        this.prevBtn = document.getElementById('prevBtn');
        this.nextBtn = document.getElementById('nextBtn');
        this.lastBtn = document.getElementById('lastBtn');
        this.searchBtn = document.getElementById('searchBtn');
        this.closeModalBtn = document.getElementById('closeModalBtn');
        this.resetViewBtn = document.getElementById('resetViewBtn');
        
        // Info displays
        this.taskInfo = document.getElementById('taskInfo');
        this.taskId = document.getElementById('taskId');
        this.fileInfo = document.getElementById('fileInfo');
        
        // Search
        this.indexSearch = document.getElementById('indexSearch');
        
        // Containers
        this.modal = document.getElementById('fileBrowserModal');
        this.fileList = document.getElementById('fileList');
        this.statusMessage = document.getElementById('statusMessage');
        this.noTaskMessage = document.getElementById('noTaskMessage');
        this.taskContent = document.getElementById('taskContent');
        
        // View canvases
        this.viewCanvases = {
            top: document.getElementById('view-top'),
            left: document.getElementById('view-left'),
            front: document.getElementById('view-front'),
            back: document.getElementById('view-back'),
            right: document.getElementById('view-right'),
            bottom: document.getElementById('view-bottom')
        };
    }

    attachEventListeners() {
        this.loadBtn.addEventListener('click', () => this.showFileBrowser());
        this.closeModalBtn.addEventListener('click', () => this.hideFileBrowser());
        
        this.firstBtn.addEventListener('click', () => this.goToFirst());
        this.prevBtn.addEventListener('click', () => this.goToPrevious());
        this.nextBtn.addEventListener('click', () => this.goToNext());
        this.lastBtn.addEventListener('click', () => this.goToLast());
        
        this.searchBtn.addEventListener('click', () => this.searchByIndex());
        this.indexSearch.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.searchByIndex();
        });
        
        this.resetViewBtn.addEventListener('click', () => {
            if (this.threeScene) this.threeScene.resetView();
        });
        
        // Close modal when clicking outside
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) this.hideFileBrowser();
        });
    }

    initializeThreeScene() {
        // Initialize the 3D scene
        try {
            if (typeof THREE === 'undefined') {
                console.error('THREE.js not loaded yet');
                return;
            }
            this.threeScene = new ThreeScene('threeContainer');
            console.log('ThreeScene initialized successfully');
        } catch (error) {
            console.error('Error initializing ThreeScene:', error);
        }
    }

    async showFileBrowser() {
        this.modal.style.display = 'flex';
        this.fileList.innerHTML = '<p class="loading">Loading files...</p>';
        
        try {
            const response = await fetch('/api/list-files');
            if (!response.ok) throw new Error('Failed to fetch file list');
            
            const data = await response.json();
            this.renderFileList(data.files);
        } catch (error) {
            this.fileList.innerHTML = `<p class="error">Error: ${error.message}</p>`;
        }
    }

    hideFileBrowser() {
        this.modal.style.display = 'none';
    }

    renderFileList(files) {
        if (files.length === 0) {
            this.fileList.innerHTML = '<p>No JSON files found in datasets/raw/</p>';
            return;
        }
        
        this.fileList.innerHTML = '';
        files.forEach(file => {
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            
            const fileName = document.createElement('div');
            fileName.className = 'file-name';
            fileName.textContent = file.name;
            
            const fileSize = document.createElement('div');
            fileSize.className = 'file-size';
            fileSize.textContent = this.formatFileSize(file.size);
            
            fileItem.appendChild(fileName);
            fileItem.appendChild(fileSize);
            
            fileItem.addEventListener('click', () => this.loadFile(file.name));
            
            this.fileList.appendChild(fileItem);
        });
    }

    formatFileSize(bytes) {
        if (bytes < 1024) return `${bytes} B`;
        if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
        return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
    }

    async loadFile(filename) {
        this.hideFileBrowser();
        this.showStatus('Loading dataset...', 'info');
        
        try {
            const response = await fetch(`/api/load-file?filename=${encodeURIComponent(filename)}`);
            if (!response.ok) throw new Error('Failed to load file');
            
            const data = await response.json();
            this.dataset = data.tasks || [];
            this.currentFilename = filename;
            this.currentIndex = 0;
            
            this.fileInfo.textContent = `${filename} (${this.dataset.length} tasks)`;
            this.indexSearch.disabled = false;
            this.searchBtn.disabled = false;
            
            this.updateNavigation();
            await this.displayCurrentTask();
            
            this.showStatus(`Loaded ${this.dataset.length} tasks from ${filename}`, 'success');
        } catch (error) {
            this.showStatus(`Error: ${error.message}`, 'error');
        }
    }

    async displayCurrentTask() {
        if (!this.dataset || this.dataset.length === 0) {
            this.noTaskMessage.style.display = 'block';
            this.taskContent.style.display = 'none';
            return;
        }
        
        this.noTaskMessage.style.display = 'none';
        this.taskContent.style.display = 'block';
        
        // Initialize ThreeScene after content is visible (only once)
        if (!this.threeScene) {
            console.log('First task load - initializing ThreeScene');
            this.initializeThreeScene();
        }
        
        this.currentTask = this.dataset[this.currentIndex];
        
        // Update task info
        this.taskId.textContent = this.currentTask.id;
        this.taskInfo.innerHTML = `Task ${this.currentIndex + 1} of ${this.dataset.length} <span class="task-id-badge">${this.currentTask.id}</span>`;
        
        // Get voxel data
        const voxels = this.currentTask.voxels;
        const shape = [voxels.length, voxels[0].length, voxels[0][0].length];
        
        // Update 3D scene
        if (this.threeScene) {
            console.log('Updating 3D scene with voxels:', shape, 'Sample voxel:', voxels[0][0][0]);
            this.threeScene.updateScene(voxels, shape[0]);
        } else {
            console.warn('ThreeScene not initialized');
        }
        
        // Generate and display views
        await this.generateViews(voxels);
    }

    async generateViews(voxels) {
        try {
            const voxelsJson = JSON.stringify(voxels);
            const response = await fetch(`/api/get-views?voxels=${encodeURIComponent(voxelsJson)}`);
            
            if (!response.ok) throw new Error('Failed to generate views');
            
            const data = await response.json();
            this.renderViews(data.views);
        } catch (error) {
            this.showStatus(`Error generating views: ${error.message}`, 'error');
        }
    }

    renderViews(views) {
        // Render each view
        Object.keys(views).forEach(viewName => {
            const canvas = this.viewCanvases[viewName];
            if (!canvas) return;
            
            const grid = views[viewName];
            this.renderGrid(canvas, grid);
        });
    }

    renderGrid(canvas, grid) {
        const rows = grid.length;
        const cols = grid[0].length;
        const cellSize = 30; // pixels per cell
        
        canvas.width = cols * cellSize;
        canvas.height = rows * cellSize;
        
        const ctx = canvas.getContext('2d');
        
        // Draw cells
        for (let row = 0; row < rows; row++) {
            for (let col = 0; col < cols; col++) {
                const color = grid[row][col];
                const x = col * cellSize;
                const y = row * cellSize;
                
                // Fill cell
                ctx.fillStyle = getARCColor(color);
                ctx.fillRect(x, y, cellSize, cellSize);
                
                // Draw grid lines
                ctx.strokeStyle = '#333';
                ctx.lineWidth = 1;
                ctx.strokeRect(x, y, cellSize, cellSize);
            }
        }
    }

    goToFirst() {
        this.currentIndex = 0;
        this.updateNavigation();
        this.displayCurrentTask();
    }

    goToPrevious() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
            this.updateNavigation();
            this.displayCurrentTask();
        }
    }

    goToNext() {
        if (this.currentIndex < this.dataset.length - 1) {
            this.currentIndex++;
            this.updateNavigation();
            this.displayCurrentTask();
        }
    }

    goToLast() {
        this.currentIndex = this.dataset.length - 1;
        this.updateNavigation();
        this.displayCurrentTask();
    }

    searchByIndex() {
        const index = parseInt(this.indexSearch.value, 10);
        
        if (isNaN(index) || index < 1 || index > this.dataset.length) {
            this.showStatus(`Invalid index. Please enter a number between 1 and ${this.dataset.length}`, 'error');
            return;
        }
        
        this.currentIndex = index - 1;
        this.updateNavigation();
        this.displayCurrentTask();
        this.indexSearch.value = '';
    }

    updateNavigation() {
        if (!this.dataset || this.dataset.length === 0) {
            this.firstBtn.disabled = true;
            this.prevBtn.disabled = true;
            this.nextBtn.disabled = true;
            this.lastBtn.disabled = true;
            return;
        }
        
        this.firstBtn.disabled = this.currentIndex === 0;
        this.prevBtn.disabled = this.currentIndex === 0;
        this.nextBtn.disabled = this.currentIndex === this.dataset.length - 1;
        this.lastBtn.disabled = this.currentIndex === this.dataset.length - 1;
    }

    showStatus(message, type = 'info') {
        this.statusMessage.textContent = message;
        this.statusMessage.className = `status-message ${type}`;
        this.statusMessage.style.display = 'block';
        
        setTimeout(() => {
            this.statusMessage.style.display = 'none';
        }, 3000);
    }
}

// Initialize viewer when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Wait for THREE.js to load if not already loaded
    function initViewer() {
        console.log('Checking for THREE.js...', typeof THREE);
        console.log('Checking for OrbitControls...', typeof THREE !== 'undefined' ? typeof THREE.OrbitControls : 'THREE not loaded');
        
        if (typeof THREE !== 'undefined') {
            console.log('THREE.js loaded, initializing viewer');
            new TaskViewer();
        } else {
            console.log('Waiting for THREE.js to load...');
            setTimeout(initViewer, 100);
        }
    }
    
    // Give scripts more time to load
    setTimeout(initViewer, 500);
});
