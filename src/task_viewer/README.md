# Task Viewer

A read-only web-based viewer for navigating and visualizing tasks from the orthographic benchmark datasets.

## Features

- **Load datasets** from `datasets/raw/` directory
- **Navigate** through tasks with first/previous/next/last buttons
- **Search** by index (last 3 digits of task_id)
- **View 6 orthographic projections** in a structured 3-row layout:
  ```
  |        | top    |        |        |
  | left   | front  | back   | right  |
  |        | bottom |        |        |
  ```
- **Display voxel data** with shape information and raw JSON

## Usage

### Start the server

From the project root:

```bash
cd src/task_viewer
python serve.py
```

The viewer will open automatically at http://localhost:8003

### Navigate datasets

1. Click **"📁 Load Dataset"** to see available JSON files
2. Select a dataset file (e.g., `orthographic_dataset_3_tasks.json`)
3. Use navigation buttons to browse tasks:
   - ⏮ **First** - Jump to the first task
   - ← **Previous** - Go to previous task
   - **Next** → - Go to next task
   - ⏭ **Last** - Jump to the last task
4. Use the **index search** to jump to a specific task by its number (1-based)

### Understanding the display

- **Task ID**: Shows the full task identifier (e.g., `task_001`)
- **Orthographic Views**: Six 2D projections of the 3D scene
  - Each view shows the scene from a different angle
  - Colors follow the ARC palette (0-9)
  - Black (0) represents empty space
- **Voxel Scene**: Shows the 3D array shape and raw JSON data

## Technical Details

### Architecture

- **Python HTTP server** with custom API endpoints:
  - `/api/list-files` - List all JSON files in `datasets/raw/`
  - `/api/load-file?filename=...` - Load a specific dataset
  - `/api/get-views?voxels=...` - Generate orthographic projections using `projection.py`
  
- **Frontend** (HTML/CSS/JavaScript):
  - Vanilla JavaScript (no frameworks)
  - Canvas-based grid rendering
  - ARC color palette from `arc-colors.js`

### Dependencies

The server requires:
- Python 3.11+
- numpy
- The project's `generation` module (`projection.py`, `scene.py`)

All dependencies are managed via `pyproject.toml` and should be available in the virtualenv managed by `uv` and `direnv`.

## File Structure

```
src/task_viewer/
  ├── serve.py           # Python HTTP server with API
  ├── index.html         # Main viewer interface
  ├── viewer.js          # Viewer logic and interactions
  ├── arc-colors.js      # ARC color palette definitions
  ├── styles.css         # Styling
  └── README.md          # This file
```

## Differences from Voxel Editor

The task viewer is derived from the voxel editor but is:
- **Read-only** - no editing capabilities
- **Dataset-focused** - loads from `datasets/raw/` only
- **Task-oriented** - displays task metadata and IDs
- **View-focused** - emphasizes the 6 orthographic projections

---

**Port**: 8003 (to avoid conflicts with voxel_editor on 8000 and mc_editor on 8001)
