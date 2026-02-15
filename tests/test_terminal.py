"""Tests for terminal interface and display."""

import pytest
from momo.core import GameOfLife
from momo.display import Display
from momo.terminal import TerminalInterface


class TestDisplay:
    """Tests for Display class."""

    def test_display_initialization(self):
        """Test display initialization."""
        display = Display()
        assert display is not None

    def test_clear(self):
        """Test clearing the display."""
        display = Display()
        display.clear()

    def test_hide_cursor(self):
        """Test hiding cursor."""
        display = Display()
        # Should not raise exception
        display.hide_cursor()

    def test_show_cursor(self):
        """Test showing cursor."""
        display = Display()
        # Should not raise exception
        display.show_cursor()

    def test_render_grid(self):
        """Test rendering a grid."""
        display = Display()
        grid = [
            [True, False],
            [False, True]
        ]
        display.render(grid, 2, 2)

    def test_render_with_info(self):
        """Test rendering with status info."""
        display = Display()
        grid = [
            [True, False],
            [False, True]
        ]
        display.render_with_info(grid, 2, 2, 5, True)

    def test_render_with_controls(self):
        """Test rendering with controls."""
        display = Display()
        grid = [
            [True, False],
            [False, True]
        ]
        controls = "Test:Help"
        display.render_with_controls(grid, 2, 2, 5, False, controls)


class TestTerminalInterface:
    """Tests for TerminalInterface class."""

    def test_initialization(self):
        """Test terminal interface initialization."""
        interface = TerminalInterface(10, 10, 100, 42)
        assert interface.game.get_width() == 10
        assert interface.game.get_height() == 10
        assert interface.generation == 0

    def test_speed_parameter(self):
        """Test speed parameter is stored."""
        interface = TerminalInterface(10, 10, 50, None)
        assert interface.speed == 50

    def test_seed_parameter(self):
        """Test seed parameter is stored."""
        interface = TerminalInterface(10, 10, 100, 123)
        assert interface.seed == 123

    def test_default_speed(self):
        """Test default speed value."""
        interface = TerminalInterface(10, 10)
        assert interface.speed == 100

    def test_default_seed(self):
        """Test default seed value."""
        interface = TerminalInterface(10, 10)
        assert interface.seed is None

    def test_control_states(self):
        """Test control states can be toggled."""
        interface = TerminalInterface(10, 10)
        assert interface.paused is False
        interface.paused = True
        assert interface.paused is True
        interface.paused = False
        assert interface.paused is False

    def test_step_advances_generation(self):
        """Test stepping advances generation counter."""
        interface = TerminalInterface(10, 10)
        assert interface.generation == 0
        interface.game.step()
        assert interface.generation == 1

    def test_randomize_with_seed(self):
        """Test randomize with seed."""
        interface = TerminalInterface(10, 10)
        interface.game.randomize(seed=42)
        grid1 = [row[:] for row in interface.game.grid]

        interface.game.randomize(seed=42)
        grid2 = [row[:] for row in interface.game.grid]

        assert grid1 == grid2

    def test_randomize_different_seeds(self):
        """Test different seeds produce different grids."""
        interface1 = TerminalInterface(10, 10)
        interface1.game.randomize(seed=42)

        interface2 = TerminalInterface(10, 10)
        interface2.game.randomize(seed=43)

        assert interface1.game.grid != interface2.game.grid

    def test_clear_resets_generation(self):
        """Test clearing resets generation counter."""
        interface = TerminalInterface(10, 10)
        interface.game.randomize()
        interface.generation = 100
        interface.game.clear()
        assert interface.generation == 0

    def test_grid_dimensions(self):
        """Test grid dimensions are maintained."""
        interface = TerminalInterface(5, 3, 0, None)
        assert interface.game.get_width() == 5
        assert interface.game.get_height() == 3

    def test_cell_operations(self):
        """Test cell operations."""
        interface = TerminalInterface(10, 10)
        interface.game.set_cell(5, 5, True)
        assert interface.game.get_cell(5, 5) is True
        interface.game.set_cell(5, 5, False)
        assert interface.game.get_cell(5, 5) is False

    def test_invalid_dimensions(self):
        """Test initialization with invalid dimensions."""
        with pytest.raises((ValueError, AssertionError)):
            TerminalInterface(-10, 10)
        with pytest.raises((ValueError, AssertionError)):
            TerminalInterface(10, -10)

    def test_invalid_speed(self):
        """Test initialization with invalid speed."""
        with pytest.raises((ValueError, AssertionError)):
            TerminalInterface(10, 10, -100)