"""
Basic tests for the generation module.
"""

import numpy as np
from src.generation.scene import Color, VIEWPOINTS, empty_voxel_scene, place_object, is_space_empty, build_voxel_scene
from src.generation.projection import orthographic_projection, get_orthographic_views


def test_empty_voxel_scene():
    """Test scene creation."""
    scene = empty_voxel_scene((5, 5, 5))
    assert scene.shape == (5, 5, 5)
    assert scene.dtype == np.int8
    assert np.all(scene == Color.BLACK)


def test_place_object():
    """Test object placement."""
    scene = empty_voxel_scene((5, 5, 5))
    shape_mask = np.ones((2, 2, 2), dtype=np.int8)
    place_object(scene, origin=(0, 0, 0), shape_mask=shape_mask, color=Color.BLUE)
    
    # Check cube is placed
    assert scene[0, 0, 0] == Color.BLUE
    assert scene[1, 1, 1] == Color.BLUE
    
    # Check outside cube is empty
    assert scene[2, 2, 2] == Color.BLACK


def test_is_space_empty():
    """Test space emptiness checking."""
    scene = empty_voxel_scene((5, 5, 5))
    
    # Initially all space is empty
    mask_2x2x2 = np.ones((2, 2, 2), dtype=np.int8)
    mask_1x1x1 = np.ones((1, 1, 1), dtype=np.int8)
    assert is_space_empty(scene, origin=(0, 0, 0), shape_mask=mask_2x2x2)
    assert is_space_empty(scene, origin=(3, 3, 3), shape_mask=mask_2x2x2)
    
    # Place a object
    place_object(scene, origin=(0, 0, 0), shape_mask=mask_2x2x2, color=Color.BLUE)
    
    # Now that space is not empty
    assert not is_space_empty(scene, origin=(0, 0, 0), shape_mask=mask_2x2x2)
    assert not is_space_empty(scene, origin=(0, 0, 0), shape_mask=mask_1x1x1)
    assert not is_space_empty(scene, origin=(1, 1, 1), shape_mask=mask_1x1x1)
    
    # But other space is still empty
    assert is_space_empty(scene, origin=(3, 3, 3), shape_mask=mask_2x2x2)
    assert is_space_empty(scene, origin=(2, 2, 2), shape_mask=mask_1x1x1)


def test_orthographic_projection():
    """Test orthographic projection."""
    scene = empty_voxel_scene((3, 3, 3))
    mask_1x1x1 = np.ones((1, 1, 1), dtype=np.int8)
    place_object(scene, origin=(0, 0, 0), shape_mask=mask_1x1x1, color=Color.BLUE)
    place_object(scene, origin=(2, 2, 2), shape_mask=mask_1x1x1, color=Color.RED)
    
    # Front view (along Y axis)
    front = orthographic_projection(scene, VIEWPOINTS["front"])
    assert front.shape == (3, 3)  # X by Z
    assert front[0, 0] == Color.BLUE
    assert front[2, 2] == Color.RED
    
    # Top view (along Z axis)
    top = orthographic_projection(scene, VIEWPOINTS["top"])
    assert top.shape == (3, 3)  # X by Y


def test_get_orthographic_views():
    """Test generation and transformation of orthographic views from a voxel scene."""
    scene = empty_voxel_scene((3, 3, 3))
    mask_1x1x1 = np.ones((1, 1, 1), dtype=np.int8)
    place_object(scene, origin=(0, 0, 0), shape_mask=mask_1x1x1, color=Color.BLUE)
    
    # Generate orthographic views (now takes voxel scene directly)
    ortho_views = get_orthographic_views(scene)
    
    assert len(ortho_views) == 6
    assert all(isinstance(v, np.ndarray) for v in ortho_views.values())
    assert "front" in ortho_views
    assert "top" in ortho_views


def test_build_and_show_scene():
    """Test the high-level show_scene function."""
    mask_1x1x1 = np.ones((1, 1, 1), dtype=np.int8)
    scene_descriptor = {
        "size": (3, 3, 3),
        "objects": [
            {"origin": (0, 0, 0), "shape_mask": mask_1x1x1, "color": Color.BLUE},
            {"origin": (2, 2, 2), "shape_mask": mask_1x1x1, "color": Color.RED},
        ]
    }

    voxel_scene = build_voxel_scene(scene_descriptor["size"], scene_descriptor["objects"])
    
    # Test without showing (to avoid matplotlib windows in tests)
    ortho_views = get_orthographic_views(voxel_scene)
    
    assert voxel_scene.shape == (3, 3, 3)
    assert voxel_scene[0, 0, 0] == Color.BLUE
    assert voxel_scene[2, 2, 2] == Color.RED
    assert len(ortho_views) == 6
    assert all(isinstance(v, np.ndarray) for v in ortho_views.values())


def test_build_and_show_scene_collision_detection():
    """Test collision detection in build_voxel_scene."""
    # Scene with overlapping objects
    mask_2x2x2 = np.ones((2, 2, 2), dtype=np.int8)
    overlapping_scene = {
        "size": (5, 5, 5),
        "objects": [
            {"origin": (0, 0, 0), "shape_mask": mask_2x2x2, "color": Color.BLUE},
            {"origin": (1, 1, 1), "shape_mask": mask_2x2x2, "color": Color.RED},  # Overlaps!
        ]
    }
    
    # Should raise ValueError with collision checking enabled
    try:
        build_voxel_scene(
            overlapping_scene["size"],
            overlapping_scene["objects"],
            check_collisions=True
        )
        # If we get here, the test failed
        assert False, "Expected ValueError for collision but none was raised"
    except ValueError as e:
        assert "Collision detected" in str(e)
    
    # Should succeed with collision checking disabled
    voxel_scene = build_voxel_scene(
        overlapping_scene["size"],
        overlapping_scene["objects"],
        check_collisions=False
    )
    
    assert voxel_scene.shape == (5, 5, 5)
    # The second object overwrites the first in the overlapping region
    assert voxel_scene[1, 1, 1] == Color.RED


if __name__ == "__main__":
    test_empty_voxel_scene()
    test_place_object()
    test_is_space_empty()
    test_orthographic_projection()
    test_get_orthographic_views()
    test_build_and_show_scene()
    test_build_and_show_scene_collision_detection()
    print("✓ All tests passed!")
