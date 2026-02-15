"""Core Game of Life logic."""

from typing import List, Tuple


class GameOfLife:
    """Conway's Game of Life implementation."""

    def __init__(self, width: int = 50, height: int = 25, seed: int | None = None):
        """
        Initialize the Game of Life.

        Args:
            width: Width of the grid
            height: Height of the grid
            seed: Random seed for reproducible randomization
        """
        self.width = width
        self.height = height
        self.generation = 0
        self.grid = [[False for _ in range(width)] for _ in range(height)]
        self._randomize(seed)

    def _randomize(self, seed: int | None = None):
        """Randomize the grid with a given seed for reproducibility."""
        import random

        if seed is not None:
            random.seed(seed)

        for row in self.grid:
            for i in range(len(row)):
                row[i] = random.choice([True, False])

    def _get_neighbors(self, x: int, y: int) -> int:
        """
        Count living neighbors for cell at (x, y).

        Uses toroidal (wrapping) boundaries.
        """
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = (x + dx) % self.width, (y + dy) % self.height
                if self.grid[ny][nx]:
                    count += 1
        return count

    def step(self) -> None:
        """Advance to the next generation."""
        new_grid = [[False for _ in range(self.width)] for _ in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                neighbors = self._get_neighbors(x, y)
                is_alive = self.grid[y][x]

                if is_alive:
                    # Underpopulation: dies if < 2 neighbors
                    if neighbors < 2:
                        new_grid[y][x] = False
                    # Survival: lives if 2 or 3 neighbors
                    elif neighbors in (2, 3):
                        new_grid[y][x] = True
                    # Overpopulation: dies if > 3 neighbors
                    else:
                        new_grid[y][x] = False
                else:
                    # Reproduction: born if exactly 3 neighbors
                    if neighbors == 3:
                        new_grid[y][x] = True

        self.grid = new_grid

    def randomize(self, seed: int | None = None) -> None:
        """
        Randomize the grid.

        Args:
            seed: Random seed for reproducibility
        """
        self._randomize(seed)

    def clear(self) -> None:
        """Clear all cells."""
        self.grid = [[False for _ in range(self.width)] for _ in range(self.height)]

    def is_paused(self) -> bool:
        """Return whether the simulation is paused."""
        return False

    def get_width(self) -> int:
        """Return grid width."""
        return self.width

    def get_height(self) -> int:
        """Return grid height."""
        return self.height

    def get_cell(self, x: int, y: int) -> bool:
        """Get state of cell at (x, y)."""
        return self.grid[y][x]

    def set_cell(self, x: int, y: int, alive: bool) -> None:
        """Set state of cell at (x, y)."""
        self.grid[y][x] = alive