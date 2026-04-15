# Generation Module

3D voxel scene generation and orthographic projection for the AGI benchmark.

## Modules

### `scene.py`
Core data structures and scene manipulation:
- `Color` — IntEnum for ARC color palette (0-9)
- `ARC_COLORS` — Hex color codes for the ARC palette
- `VIEWPOINTS` — Configuration for 6 orthographic viewpoints
- `make_voxel_scene(grid_size)` — Create an empty 3D voxel array
- `is_space_empty(scene, origin, size)` — Check if a region is empty (no collisions)
- `place_object(scene, origin, size, color)` — Add a object to the scene

### `projection.py`
Orthographic projection logic:
- `orthographic_projection(scene, viewpoint)` — Project 3D scene to 2D
- `get_orthographic_views(voxel_scene)` — Generate all 6 orthographic views as display-ready grids

### `visualization.py`
Matplotlib visualization functions:
- `show_isometric_view(scene)` — Render 3D isometric view
- `show_orthographic_views(ortho_views)` — Show all 6 projections in a grid
- `build_and_show_scene(scene, show_isometric, show_orthographics, check_collisions)` — High-level function to build and visualize a scene from a descriptor dict (with optional collision detection)

## Coordinate System

**Z-up, right-handed:**
- X = right (red axis)
- Y = forward/depth (green axis)
- Z = up (blue axis)

Array indexing: `scene[x, y, z]`

## Usage Example

### High-level API (recommended for quick visualizations)

```python
from generation.scene import Color
from generation.visualization import build_and_show_scene

# Define a scene with a descriptor dict
scene = {
    "size": (5, 5, 5),
    "objects": [
        {"origin": (0, 0, 0), "size": (2, 2, 2), "color": Color.BLUE},
        {"origin": (3, 3, 3), "size": (1, 1, 1), "color": Color.RED},
    ]
}

# Build and visualize in one call (collision detection enabled by default)
voxel_scene, ortho_views = build_and_show_scene(scene)

# To allow overlapping objects, disable collision checking
voxel_scene, ortho_views = build_and_show_scene(scene, check_collisions=False)
```

### Low-level API (for programmatic scene generation)

```python
from generation.scene import Color, VIEWPOINTS, make_voxel_scene, place_object, is_space_empty
from generation.projection import orthographic_projection
from generation.visualization import show_isometric_view,, get_orthographic_views
from generation.visualization import show_isometric_view
# Create a 5×5×5 scene
scene = make_voxel_scene((5, 5, 5))

# Check if space is available before placing
origin = (0, 0, 0)
size = (2, 2, 2)
if is_space_empty(scene, origin, size):
    place_object(scene, origin=origin, size=size, color=Color.BLUE)

# Add more objects
place_cuboid(scene, origin=(3, 3, 3), size=(1, 1, 1), color=Color.RED)

# Visualize in 3D
show_isometric_view(scene)

# Generate orthographic projections
views = {
    "front": orthographic_projection(scene, VIEWPOINTS["front"]),
    "top": orthographic_projection(scene, VIEWPOINTS["top"]),
    # ... etc
}

# Show all projections
ortho_views = get_orthographic_views(views)
show_orthographic_views(ortho_views)
```

## Demo Notebook

See [analysis/3d-orthographics/engines.ipynb](../../analysis/3d-orthographics/engines.ipynb) for a full demonstration.
