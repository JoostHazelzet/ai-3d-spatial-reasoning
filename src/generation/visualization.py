"""
Visualization functions for 3D voxel scenes and orthographic projections.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from .scene import ARC_COLORS, Color, VIEWPOINTS, place_object, is_space_empty
from .projection import orthographic_projection, get_orthographic_views


# Matplotlib colormap for ARC palette
arc_cmap = mcolors.ListedColormap(ARC_COLORS)
arc_norm = mcolors.BoundaryNorm(boundaries=range(11), ncolors=10)


def show_isometric_view(voxel_scene: np.ndarray) -> None:
    """
    Render the voxel scene as an isometric-style 3D view with Z-up orientation.
    
    Uses matplotlib's 3D voxel renderer with the ARC color palette.
    Coordinate gizmo: X=red, Y=green, Z=blue (RGB=XYZ convention)
    
    Args:
        voxel_scene: 3D voxel array with shape (x_size, y_size, z_size)
    """
    x_size, y_size, z_size = voxel_scene.shape
    filled = voxel_scene != Color.BLACK
    
    # Build a facecolor array matching the ARC palette
    face_colors = np.empty(voxel_scene.shape, dtype=object)
    for idx in range(voxel_scene.shape[0]):
        for idy in range(voxel_scene.shape[1]):
            for idz in range(voxel_scene.shape[2]):
                face_colors[idx, idy, idz] = ARC_COLORS[voxel_scene[idx, idy, idz]]

    fig = plt.figure(figsize=(6, 6), facecolor='black')
    ax = fig.add_subplot(111, projection="3d", facecolor='black')
    
    # Render voxels (matplotlib 3D uses Z-up by default)
    ax.voxels(
        filled,
        facecolors=face_colors,
        edgecolor="white",
        linewidth=0.3,
        alpha=0.95,
    )
    
    # Set black background for 3D panes
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('white')
    ax.yaxis.pane.set_edgecolor('white')
    ax.zaxis.pane.set_edgecolor('white')
    ax.xaxis.pane.set_alpha(0.1)
    ax.yaxis.pane.set_alpha(0.1)
    ax.zaxis.pane.set_alpha(0.1)
    ax.grid(color='white', alpha=0.2)
    
    # Set axis labels with color coding
    ax.set_xlabel("X", color="red", fontweight="bold")
    ax.set_ylabel("Y", color="green", fontweight="bold")
    ax.set_zlabel("Z", color="blue", fontweight="bold")
    ax.set_title(f"Isometric view", fontsize=11, color='white')
    ax.view_init(elev=30, azim=-30, roll=0)
    
    # Set aspect ratio and limits based on actual dimensions
    ax.set_box_aspect([x_size, y_size, z_size])
    ax.set_xlim(0, x_size)
    ax.set_ylim(0, y_size)
    ax.set_zlim(0, z_size)
    
    # Set integer ticks based on actual dimensions
    ax.set_xticks(range(x_size + 1))
    ax.set_yticks(range(y_size + 1))
    ax.set_zticks(range(z_size + 1))
    
    # Color tick labels to match axis colors (RGB)
    ax.tick_params(axis='x', colors='red')
    ax.tick_params(axis='y', colors='green')
    ax.tick_params(axis='z', colors='blue')
    
    plt.show()


def show_orthographic_views(ortho_views: dict[str, np.ndarray]) -> None:
    """
    Render orthographic views in a grid layout.
    
    Displays orthographic projections with proper axis labeling using the RGB=XYZ color convention.
    Layout is automatically determined from the number of views.
    
    Args:
        ortho_views: Dict mapping viewpoint names to display-ready 2D arrays
    """
    # Axis color mapping (RGB = XYZ)
    axis_colors = {"X": "red", "Y": "green", "Z": "blue"}
    
    # Determine layout based on number of views
    num_views = len(ortho_views)
    if num_views <= 3:
        # 1x3 layout for 3 or fewer views
        fig, axes = plt.subplots(1, num_views, figsize=(4 * num_views, 4))
        axes = [axes] if num_views == 1 else axes
    else:
        # 2x3 layout for 4-6 views
        fig, axes = plt.subplots(2, 3, figsize=(12, 8))
        axes = axes.flatten()
    
    for ax, (name, grid) in zip(axes, ortho_views.items()):
        # Get dimensions from the actual grid shape (height, width)
        height, width = grid.shape
        
        ax.imshow(
            grid,
            cmap=arc_cmap,
            norm=arc_norm,
            interpolation="nearest",
            origin="upper",
            extent=[0, width, 0, height],
        )
        ax.set_title(f"Orthographic {name} view", fontsize=11)
        xlabel, ylabel = VIEWPOINTS[name]["labels"]
        
        # Set axis labels with colors matching RGB=XYZ convention
        ax.set_xlabel(xlabel, color=axis_colors[xlabel], fontweight="bold")
        ax.set_ylabel(ylabel, color=axis_colors[ylabel], fontweight="bold")
        
        # Set ticks based on actual dimensions
        ax.set_xticks(range(width + 1))
        ax.set_yticks(range(height + 1))
        
        # Mirror horizontal axis labels for +X and -Y views
        if name in ["left", "back"]:
            ax.set_xticklabels(range(width, -1, -1), fontsize=10)
        else:
            ax.set_xticklabels(range(width + 1), fontsize=10)
        
        # Mirror vertical axis labels for +Z view
        if name == "bottom":
            ax.set_yticklabels(range(height, -1, -1), fontsize=10)
        else:
            # All other views: show 0 at bottom, height at top for vertical axis
            ax.set_yticklabels(range(height + 1), fontsize=10)
        
        # Color tick labels to match axis colors (RGB)
        ax.tick_params(axis='x', colors=axis_colors[xlabel])
        ax.tick_params(axis='y', colors=axis_colors[ylabel])
        
        ax.grid(True, color="white", linewidth=0.3)
    
    plt.tight_layout()
    plt.show()
