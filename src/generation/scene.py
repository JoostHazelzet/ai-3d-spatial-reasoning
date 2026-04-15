"""
Scene representation and manipulation for 3D voxel scenes.

Coordinate system (Z-up, right-handed):
  X = right (red axis)
  Y = forward/depth (green axis)  
  Z = up (blue axis)
"""

from enum import IntEnum
import numpy as np


# ARC color palette (indices 0‑9 → RGB)
ARC_COLORS = [
    "#000000",  # 0 black  (background)
    "#0074D9",  # 1 blue
    "#FF4136",  # 2 red
    "#2ECC40",  # 3 green
    "#FFDC00",  # 4 yellow
    "#AAAAAA",  # 5 gray
    "#F012BE",  # 6 fuchsia
    "#FF851B",  # 7 orange
    "#7FDBFF",  # 8 azure
    "#870C25",  # 9 maroon
]


class Color(IntEnum):
    """ARC color palette as an enum for convenient access."""
    BLACK = 0      # background
    BLUE = 1
    RED = 2
    GREEN = 3
    YELLOW = 4
    GRAY = 5
    FUCHSIA = 6
    ORANGE = 7
    AZURE = 8
    MAROON = 9


# Viewpoint configurations for orthographic projections
VIEWPOINTS = {
    "front": {"axis": 1, "reverse": False, "labels": ("X", "Z")},   # view along +Y (X horizontal, Z vertical)
    "back": {"axis": 1, "reverse": True, "labels": ("X", "Z")},    # view along -Y (X horizontal, Z vertical)
    "left": {"axis": 0, "reverse": False, "labels": ("Y", "Z")},    # view along -X (Y horizontal, Z vertical)
    "right": {"axis": 0, "reverse": True, "labels": ("Y", "Z")},   # view along +X (Y horizontal, Z vertical)
    "top": {"axis": 2, "reverse": True, "labels": ("X", "Y")},     # view along +Z (X horizontal, Y vertical)
    "bottom": {"axis": 2, "reverse": False, "labels": ("X", "Y")},  # view along -Z (X horizontal, Y vertical)
}


# Allowed object masks for scene generation
# Each mask is a 3D list representing a voxel shape (1 = filled, 0 = empty)
ALLOWED_OBJECT_MASKS = [
    ## Single rectangular cuboid objects
    [[[1]]], # np.ones((1, 1, 1))

    ## Two-voxel rectangular cuboid objects
    [[[1]], [[1]]], # np.ones((2, 1, 1))
    [[[1], [1]]], # np.ones((1, 2, 1))
    [[[1, 1]]], # np.ones((1, 1, 2))

    ## Three-voxel rectangular cuboid objects
    [[[1]], [[1]], [[1]]], # np.ones((3, 1, 1))
    [[[1], [1], [1]]], # np.ones((1, 3, 1))
    [[[1, 1, 1]]], # np.ones((1, 1, 3))

    [[[1]], [[0]], [[1]]], 
    [[[1], [0], [1]]], 
    [[[1, 0, 1]]], 

    ## Four-voxel rectangular cuboid objects
    [[[1, 1], [1, 1]]], # np.ones((1, 2, 2))
    [[[1, 1]], [[1, 1]]], # np.ones((2, 1, 2))
    [[[1], [1]], [[1], [1]]], # np.ones((2, 2, 1))

    [[[0, 1], [1, 0]]],
    [[[1, 0]], [[0, 1]]],
    [[[0, 1]], [[1, 0]]],
    [[[1, 0]], [[0, 1]]],
    [[[0], [1]], [[1], [0]]],
    [[[1], [0]], [[0], [1]]],

    [[[0, 1], [1, 1]]],
    [[[1, 0], [1, 1]]],
    [[[1, 1], [0, 1]]],
    [[[1, 1], [1, 0]]],
    [[[0, 1]], [[1, 1]]],
    [[[1, 0]], [[1, 1]]],
    [[[1, 1]], [[0, 1]]],
    [[[1, 1]], [[1, 0]]],
    [[[0], [1]], [[1], [1]]],
    [[[1], [0]], [[1], [1]]],
    [[[1], [1]], [[0], [1]]],
    [[[1], [1]], [[1], [0]]],

    ## Six-voxel rectangular cuboid objects
    [[[1, 1, 1], [1, 1, 1]]], # np.ones((1, 2, 3))
    [[[1, 1], [1, 1], [1, 1]]], # np.ones((1, 3, 2))
    [[[1, 1, 1]], [[1, 1, 1]]], # np.ones((2, 1, 3))
    [[[1], [1], [1]], [[1], [1], [1]]], # np.ones((2, 3, 1))
    [[[1, 1]], [[1, 1]], [[1, 1]]], # np.ones((3, 1, 2))
    [[[1], [1]], [[1], [1]], [[1], [1]]], # np.ones((3, 2, 1))

    [[[0, 1, 1], [1, 1, 1]]],
    [[[1, 0, 1], [1, 1, 1]]],
    [[[1, 1, 0], [1, 1, 1]]],
    [[[1, 1, 1], [0, 1, 1]]],
    [[[1, 1, 1], [1, 0, 1]]],
    [[[1, 1, 1], [1, 1, 0]]],

    [[[1, 0, 0], [1, 1, 1]]],
    [[[0, 1, 0], [1, 1, 1]]],
    [[[0, 0, 1], [1, 1, 1]]],
    [[[1, 1, 1], [1, 0, 0]]],
    [[[1, 1, 1], [0, 1, 0]]],
    [[[1, 1, 1], [0, 0, 1]]],

    [[[0, 1, 0], [1, 0, 1]]],
    [[[1, 0, 1], [0, 1, 0]]],

    [[[0, 1], [1, 1], [1, 1]]],
    [[[1, 0], [1, 1], [1, 1]]],
    [[[1, 1], [0, 1], [1, 1]]],
    [[[1, 1], [1, 0], [1, 1]]],
    [[[1, 1], [1, 1], [0, 1]]],
    [[[1, 1], [1, 1], [1, 0]]],

    [[[1, 0], [0, 1], [1, 1]]],
    [[[0, 1], [0, 1], [1, 1]]],
    [[[0, 0], [1, 1], [1, 1]]],
    [[[1, 1], [1, 1], [0, 0]]],
    [[[1, 1], [1, 0], [1, 0]]],
    [[[1, 1], [1, 0], [0, 1]]],

    [[[0, 1], [0, 1], [0, 1]]],
    [[[1, 0], [1, 0], [1, 0]]],

    [[[0, 1, 1]], [[1, 1, 1]]],
    [[[1, 0, 1]], [[1, 1, 1]]],
    [[[1, 1, 0]], [[1, 1, 1]]],
    [[[1, 1, 1]], [[0, 1, 1]]],
    [[[1, 1, 1]], [[1, 0, 1]]],
    [[[1, 1, 1]], [[1, 1, 0]]],

    [[[1, 0, 0]], [[1, 1, 1]]],
    [[[0, 1, 0]], [[1, 1, 1]]],
    [[[0, 0, 1]], [[1, 1, 1]]],
    [[[1, 1, 1]], [[1, 0, 0]]],
    [[[1, 1, 1]], [[0, 1, 0]]],
    [[[1, 1, 1]], [[0, 0, 1]]],

    [[[0, 1, 0]], [[1, 0, 1]]],
    [[[1, 0, 1]], [[0, 1, 0]]],

    [[[0], [1], [1]], [[1], [1], [1]]],
    [[[1], [0], [1]], [[1], [1], [1]]],
    [[[1], [1], [0]], [[1], [1], [1]]],
    [[[1], [1], [1]], [[0], [1], [1]]],
    [[[1], [1], [1]], [[1], [0], [1]]],
    [[[1], [1], [1]], [[1], [1], [0]]],

    [[[1], [0], [0]], [[1], [1], [1]]],
    [[[0], [1], [0]], [[1], [1], [1]]],
    [[[0], [0], [1]], [[1], [1], [1]]],
    [[[1], [1], [1]], [[0], [0], [1]]],
    [[[1], [1], [1]], [[0], [1], [0]]],
    [[[1], [1], [1]], [[1], [0], [0]]],

    [[[0], [1], [0]], [[1], [0], [1]]],
    [[[1], [0], [1]], [[0], [1], [0]]],

    [[[0, 1]], [[1, 1]], [[1, 1]]],
    [[[1, 0]], [[1, 1]], [[1, 1]]],
    [[[1, 1]], [[0, 1]], [[1, 1]]],
    [[[1, 1]], [[1, 0]], [[1, 1]]],
    [[[1, 1]], [[1, 1]], [[0, 1]]],
    [[[1, 1]], [[1, 1]], [[1, 0]]],

    [[[1, 0]], [[0, 1]], [[1, 1]]],
    [[[0, 1]], [[0, 1]], [[1, 1]]],
    [[[0, 0]], [[1, 1]], [[1, 1]]],
    [[[1, 1]], [[1, 1]], [[0, 0]]],
    [[[1, 1]], [[1, 0]], [[1, 0]]],
    [[[1, 1]], [[1, 0]], [[0, 1]]],

    [[[1, 0]], [[1, 0]], [[1, 0]]],
    [[[0, 1]], [[0, 1]], [[0, 1]]],

    [[[0], [1]], [[1], [1]], [[1], [1]]],
    [[[1], [0]], [[1], [1]], [[1], [1]]],
    [[[1], [1]], [[0], [1]], [[1], [1]]],
    [[[1], [1]], [[1], [0]], [[1], [1]]],
    [[[1], [1]], [[1], [1]], [[0], [1]]],
    [[[1], [1]], [[1], [1]], [[1], [0]]],

    [[[1], [0]], [[0], [1]], [[1], [1]]],
    [[[0], [1]], [[0], [1]], [[1], [1]]],
    [[[0], [0]], [[1], [1]], [[1], [1]]],
    [[[1], [1]], [[1], [1]], [[0], [0]]],
    [[[1], [1]], [[1], [0]], [[1], [0]]],
    [[[1], [1]], [[1], [0]], [[0], [1]]],

    [[[1], [0]], [[1], [0]], [[1], [0]]],
    [[[0], [1]], [[0], [1]], [[0], [1]]]
]


def empty_voxel_scene(grid_size: tuple[int, int, int]) -> np.ndarray:
    """
    Create an empty voxel scene.
    
    Returns a (x_size, y_size, z_size) int array.
    0 = empty/background, non-zero = ARC color index.
    
    Coordinate system (Z-up, right-handed):
      X = right (red axis)
      Y = forward/depth (green axis)
      Z = up (blue axis)
    
    Array indexing: scene[x, y, z]
    
    Args:
        grid_size: Tuple of (x_size, y_size, z_size) for the voxel grid dimensions
        
    Returns:
        A numpy array filled with zeros (background color)
    """
    scene = np.zeros(grid_size, dtype=np.int8)
    return scene


def is_space_empty(
    scene: np.ndarray,
    origin: tuple[int, int, int],
    shape_mask: np.ndarray,
) -> bool:
    """
    Check if a region of space is empty (all background color) where the mask is 1.
    
    Args:
        scene: The voxel scene array to check
        origin: (x, y, z) coordinates of the region's lower corner
        shape_mask: 3D numpy array with values 0 or 1 defining the region to check
        
    Returns:
        True if all voxels where mask == 1 are empty (Color.BLACK), False otherwise
    """
    x0, y0, z0 = origin
    sx, sy, sz = shape_mask.shape
    
    # Calculate the actual region we can check (handle boundary clipping)
    x1 = min(x0 + sx, scene.shape[0])
    y1 = min(y0 + sy, scene.shape[1])
    z1 = min(z0 + sz, scene.shape[2])
    
    # Calculate corresponding mask region (in case of clipping)
    mx1 = x1 - x0
    my1 = y1 - y0
    mz1 = z1 - z0
    
    # Check only the overlapping region
    region = scene[x0:x1, y0:y1, z0:z1]
    mask_region = shape_mask[:mx1, :my1, :mz1]
    mask_bool = mask_region == 1
    return np.all(region[mask_bool] == Color.BLACK)


def place_object(
    scene: np.ndarray,
    origin: tuple[int, int, int],
    shape_mask: np.ndarray,
    color: int,
) -> np.ndarray:
    """
    Place a custom-shaped object into the scene using a binary mask.
    
    The shape_mask is a 3D binary array (0s and 1s) that defines the object's geometry.
    Only voxels where shape_mask == 1 will be filled with the specified color.
    
    Modifies the scene array in-place.
    
    Args:
        scene: The voxel scene array to modify
        origin: (x, y, z) coordinates of the object's lower corner
        shape_mask: 3D numpy array with values 0 or 1 defining the object shape
        color: ARC color index (0-9)
        
    Returns:
        The modified scene array (same object as input)
    """
    x0, y0, z0 = origin
    sx, sy, sz = shape_mask.shape
    
    # Calculate the actual region we can write to (handle boundary clipping)
    x1 = min(x0 + sx, scene.shape[0])
    y1 = min(y0 + sy, scene.shape[1])
    z1 = min(z0 + sz, scene.shape[2])
    
    # Calculate corresponding mask region (in case of clipping)
    mx1 = x1 - x0
    my1 = y1 - y0
    mz1 = z1 - z0
    
    # Only set voxels where the mask is 1
    mask_region = shape_mask[:mx1, :my1, :mz1]
    mask_bool = mask_region == 1
    scene[x0:x1, y0:y1, z0:z1][mask_bool] = color
    return scene


def build_voxel_scene(
    size: tuple[int, int, int],
    objects: list[dict],
    check_collisions: bool = True,
) -> np.ndarray:
    """
    Build a voxel scene from a scene descriptor and visualize it.
    
    High-level convenience function that creates a scene, places objects,
    generates projections, and displays visualizations.
    
    Args:
        size: tuple of (x_size, y_size, z_size)
        objects: list of dicts, each with 'origin', 'shape_mask', 'color'
        check_collisions: Whether to check for overlapping objects before placing
        
    Returns:
        voxel_scene: 3D numpy array representing the scene
        
    Raises:
        ValueError: If check_collisions=True and a object overlaps with existing geometry
        
    Example:
        >>> mask = np.ones((2, 2, 2), dtype=np.int8)  # solid 2x2x2 cube
        >>> voxel_scene = build_voxel_scene(
        ...     size=(5, 5, 5),
        ...     objects=[
        ...         {"origin": (0, 0, 0), "shape_mask": mask, "color": Color.BLUE},
        ...         {"origin": (3, 3, 3), "shape_mask": np.ones((1,1,1)), "color": Color.RED},
        ...     ]
        ... )
    """
    # Create empty scene
    voxel_scene = empty_voxel_scene(size)

    # Place all objects with optional collision checking
    for idx, object in enumerate(objects):
        origin = object["origin"]
        shape_mask = object["shape_mask"]
        color = object["color"]
        
        # Check for collisions if requested
        if check_collisions and not is_space_empty(voxel_scene, origin, shape_mask):
            raise ValueError(
                f"Collision detected: object {idx} at origin={origin} with shape_mask.shape={shape_mask.shape} "
                f"overlaps with existing geometry. Set check_collisions=False to allow overlaps."
            )
        
        place_object(voxel_scene, origin=origin, shape_mask=shape_mask, color=color)

    return voxel_scene