#!/usr/bin/env python3
"""
HTTP server for the task viewer - read-only view of benchmark datasets.
Run this script to start a local web server and view tasks in your browser.
"""
import http.server
import socketserver
import webbrowser
import os
import json
import urllib.parse
import sys
from pathlib import Path

PORT = 8003

# Define paths
TASK_VIEWER_DIR = Path(__file__).parent
DATA_RAW_DIR = TASK_VIEWER_DIR.parent.parent / "datasets" / "raw"

# Add parent directories to Python path for imports
sys.path.insert(0, str(TASK_VIEWER_DIR.parent))

# Import projection functions
from generation.projection import get_orthographic_views
import numpy as np

# Change to the task_viewer directory
os.chdir(TASK_VIEWER_DIR)


class TaskViewerHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler with API endpoints for loading tasks."""
    
    def do_GET(self):
        """Handle GET requests - serve files or API endpoints."""
        parsed_path = urllib.parse.urlparse(self.path)
        
        if parsed_path.path == '/api/list-files':
            self.handle_list_files()
        elif parsed_path.path.startswith('/api/load-file'):
            self.handle_load_file(parsed_path)
        elif parsed_path.path.startswith('/api/get-views'):
            self.handle_get_views(parsed_path)
        else:
            # Default behavior for static files
            super().do_GET()
    
    def handle_list_files(self):
        """List all JSON files in datasets/raw directory."""
        try:
            files = []
            for filepath in DATA_RAW_DIR.glob("*.json"):
                files.append({
                    "name": filepath.name,
                    "size": filepath.stat().st_size,
                    "modified": filepath.stat().st_mtime
                })
            
            # Sort by name
            files.sort(key=lambda f: f["name"])
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"files": files}).encode())
            
        except Exception as e:
            self.send_error(500, f"Failed to list files: {str(e)}")
    
    def handle_load_file(self, parsed_path):
        """Load a JSON file from datasets/raw."""
        try:
            # Parse query parameters
            params = urllib.parse.parse_qs(parsed_path.query)
            filename = params.get('filename', [None])[0]
            
            if not filename:
                self.send_error(400, "Missing filename parameter")
                return
            
            # Security check - ensure filename is safe
            if '..' in filename or '/' in filename:
                self.send_error(400, "Invalid filename")
                return
            
            filepath = DATA_RAW_DIR / filename
            
            if not filepath.exists():
                self.send_error(404, f"File not found: {filename}")
                return
            
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
            
        except Exception as e:
            self.send_error(500, f"Failed to load file: {str(e)}")
    
    def handle_get_views(self, parsed_path):
        """Generate orthographic views from voxel data."""
        try:
            # Parse query parameters
            params = urllib.parse.parse_qs(parsed_path.query)
            voxels_json = params.get('voxels', [None])[0]
            
            if not voxels_json:
                self.send_error(400, "Missing voxels parameter")
                return
            
            # Parse voxels
            voxels = json.loads(voxels_json)
            voxel_array = np.array(voxels, dtype=np.int8)
            
            # Generate views
            views = get_orthographic_views(voxel_array)
            
            # Convert numpy arrays to lists for JSON serialization
            views_json = {name: view.tolist() for name, view in views.items()}
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"views": views_json}).encode())
            
        except Exception as e:
            self.send_error(500, f"Failed to generate views: {str(e)}")


def main():
    """Start the HTTP server and open browser."""
    Handler = TaskViewerHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Task Viewer running at http://localhost:{PORT}")
        print("Opening browser...")
        print("Press Ctrl+C to stop the server")
        
        # Open browser
        webbrowser.open(f'http://localhost:{PORT}/index.html')
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")


if __name__ == "__main__":
    main()
