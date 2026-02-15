"""Main pytest configuration and tests."""

import pytest


def test_import_momo():
    """Test that momo module can be imported."""
    import momo
    assert momo.__version__ == "0.1.0"


def test_import_submodules():
    """Test that all submodules can be imported."""
    from momo import core, display, terminal


def test_gameoflife_import():
    """Test GameOfLife class can be imported."""
    from momo.core import GameOfLife
    game = GameOfLife(5, 5)
    assert game is not None


def test_display_import():
    """Test Display class can be imported."""
    from momo.display import Display
    display = Display()
    assert display is not None