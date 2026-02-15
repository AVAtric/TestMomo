"""Tests for Game of Life core logic."""

import pytest
from momo.core import GameOfLife


class TestGameOfLife:
    """Tests for GameOfLife class."""

    def test_initialization(self):
        """Test game initialization."""
        game = GameOfLife(10, 10)
        assert game.get_width() == 10
        assert game.get_height() == 10
        assert game.generation == 0

    def test_clear(self):
        """Test clearing the grid."""
        game = GameOfLife(10, 10)
        game.set_cell(0, 0, True)
        game.clear()
        assert not game.get_cell(0, 0)
        assert all(not cell for row in game.grid for cell in row)

    def test_set_get_cell(self):
        """Test setting and getting cells."""
        game = GameOfLife(10, 10)
        game.set_cell(5, 5, True)
        assert game.get_cell(5, 5) is True
        game.set_cell(5, 5, False)
        assert game.get_cell(5, 5) is False

    def test_randomize(self):
        """Test randomizing the grid."""
        game = GameOfLife(10, 10)
        game.randomize(seed=42)
        grid1 = [row[:] for row in game.grid]
        game.randomize(seed=42)
        grid2 = [row[:] for row in game.grid]
        assert grid1 == grid2

    def test_randomize_different_seeds(self):
        """Test that different seeds produce different grids."""
        game1 = GameOfLife(10, 10)
        game1.randomize(seed=42)
        game2 = GameOfLife(10, 10)
        game2.randomize(seed=43)
        assert game1.grid != game2.grid

    def test_toroidal_wrap_neighbors(self):
        """Test neighbor counting with toroidal wrap."""
        game = GameOfLife(5, 5)
        game.set_cell(0, 0, True)
        game.set_cell(0, 4, True)
        game.set_cell(4, 0, True)

        # Cell at (0, 0) should see (0, 4) and (4, 0) as neighbors due to wrap
        neighbors = game._get_neighbors(0, 0)
        assert neighbors == 2

    def test_underpopulation(self):
        """Test underpopulation rule."""
        game = GameOfLife(5, 5)
        # Single cell dies due to underpopulation
        game.set_cell(2, 2, True)
        game.step()
        assert not game.get_cell(2, 2)

    def test_survival(self):
        """Test survival rule."""
        game = GameOfLife(5, 5)
        # Cell with 2 neighbors survives
        game.set_cell(2, 1, True)
        game.set_cell(2, 2, True)
        game.set_cell(2, 3, True)
        game.step()
        assert game.get_cell(2, 2) is True

    def test_overpopulation(self):
        """Test overpopulation rule."""
        game = GameOfLife(5, 5)
        # Cell with 4 neighbors dies due to overpopulation
        game.set_cell(2, 2, True)
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                game.set_cell((2 + dx) % 5, (2 + dy) % 5, True)
        game.step()
        assert not game.get_cell(2, 2)

    def test_reproduction(self):
        """Test reproduction rule."""
        game = GameOfLife(5, 5)
        game.clear()
        # Empty cell with 3 neighbors becomes alive
        # Set orthogonal neighbors only (no diagonals)
        game.set_cell(2, 3, True)  # Left
        game.set_cell(4, 3, True)  # Right
        game.set_cell(3, 4, True)  # Below
        game.step()
        assert game.get_cell(3, 3) is True

    def test_blinker_oscillator(self):
        """Test blinker oscillator."""
        game = GameOfLife(5, 5)
        game.clear()
        # Create a vertical blinker oscillator
        game.set_cell(1, 2, True)
        game.set_cell(2, 2, True)
        game.set_cell(3, 2, True)
        game.step()
        # Should be horizontal
        assert game.get_cell(2, 1) is True
        assert game.get_cell(2, 2) is True
        assert game.get_cell(2, 3) is True

    def test_still_life_block(self):
        """Test block still life."""
        game = GameOfLife(5, 5)
        game.clear()
        # Create a block
        game.set_cell(1, 1, True)
        game.set_cell(1, 2, True)
        game.set_cell(2, 1, True)
        game.set_cell(2, 2, True)
        game.step()
        # Should remain unchanged
        assert game.get_cell(1, 1) is True
        assert game.get_cell(1, 2) is True
        assert game.get_cell(2, 1) is True
        assert game.get_cell(2, 2) is True

    def test_multiple_generations(self):
        """Test multiple generations."""
        game = GameOfLife(10, 10)
        # Create a glider
        game.set_cell(4, 4, True)
        game.set_cell(5, 4, True)
        game.set_cell(6, 4, True)
        game.set_cell(4, 5, True)
        game.set_cell(6, 5, True)
        game.set_cell(5, 6, True)

        initial_pattern = [row[:] for row in game.grid]

        for _ in range(10):
            game.step()

        # Glider moves, so pattern should change
        assert game.grid != initial_pattern

    def test_block_still_life(self):
        """Test block still life."""
        game = GameOfLife(5, 5)
        game.clear()
        # Create a block
        game.set_cell(1, 1, True)
        game.set_cell(1, 2, True)
        game.set_cell(2, 1, True)
        game.set_cell(2, 2, True)

        # Should remain unchanged
        for _ in range(5):
            game.step()

        assert game.get_cell(1, 1) is True
        assert game.get_cell(1, 2) is True
        assert game.get_cell(2, 1) is True
        assert game.get_cell(2, 2) is True