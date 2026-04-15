"""
Orthographic projection logic for 3D voxel scenes.
"""

import numpy as np
from .scene import Color, VIEWPOINTS

def orthographic_projection(scene: np.ndarray, viewpoint: dict) -> np.ndarray:
    """
    Project a 3D scene onto a 2D plane using orthographic projection.
    
    Projects by collapsing along the specified axis using a painter's algorithm
    (front-to-back rendering).
    
    Z-up coordinate system:
      axis=0  →  view from X axis (Y horizontal, Z vertical)
      axis=1  →  view from Y axis (X horizontal, Z vertical)  
      axis=2  →  view from Z axis (X horizontal, Y vertical)
    
    Args:
        scene: 3D voxel array with shape (x_size, y_size, z_size)
        viewpoint: Dict with keys:
            - 'axis': int (0, 1, or 2) - which axis to project along
            - 'reverse': bool - if True, view from negative direction
            
    Returns:
        2D numpy array where each cell holds the first non-background
        color seen along the projection ray. Background color where no object exists.
    """
    # Move the projection axis to the front, then iterate slices front→back
    vol = np.moveaxis(scene, viewpoint["axis"], 0)  # shape: (depth, h, w)
    if viewpoint["reverse"]:
        vol = vol[::-1]  # Reverse to view from opposite direction
    
    grid = np.zeros(vol.shape[1:], dtype=np.int8)
    for depth_slice in vol:
        mask = (grid == Color.BLACK) & (depth_slice != Color.BLACK)
        grid[mask] = depth_slice[mask]
    return grid


def get_orthographic_views(
    voxel_scene: np.ndarray,
) -> dict[str, np.ndarray]:
    """
    Generate orthographic views from a voxel scene.
    
    Generates all six orthographic projections and transforms them into
    display-ready grids with proper orientation for a Z-up coordinate system.
    
    Args:
        voxel_scene: 3D numpy array representing the voxel scene
        
    Returns:
        Dict[str, np.ndarray] mapping viewpoint names to 2D display grids
    """

    # Generate all six orthographic projections
    views = {
        "front": orthographic_projection(voxel_scene, VIEWPOINTS["front"]),
        "top": orthographic_projection(voxel_scene, VIEWPOINTS["top"]),
        "right": orthographic_projection(voxel_scene, VIEWPOINTS["right"]),
        "back": orthographic_projection(voxel_scene, VIEWPOINTS["back"]),
        "bottom": orthographic_projection(voxel_scene, VIEWPOINTS["bottom"]),
        "left": orthographic_projection(voxel_scene, VIEWPOINTS["left"])
    }

    # Transform raw projections into display-ready grids
    ortho_views = {}
    for name, grid in views.items():
        display_grid = np.flipud(grid.T)  # flip so Z=0 is at bottom for vertical views
        
        # Mirror left and back views (flip horizontally)
        if name in ["left", "back"]:
            display_grid = np.fliplr(display_grid)
        
        # Mirror +Z view (flip vertically)
        if name == "bottom":
            display_grid = np.flipud(display_grid)
        
        ortho_views[name] = display_grid

    return ortho_views
