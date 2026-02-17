"""Test script to verify Game of Life functionality."""

import sys
sys.path.insert(0, '/home/argus/.openclaw/workspace/TestMomo')

from momo.core import GameOfLife
from momo.display import Display

# Test basic functionality
print("Testing Game of Life...")

# Create a simple pattern
game = GameOfLife(width=20, height=10, seed=42, randomize=False)

# Create a blinker pattern
game.set_cell(5, 4, True)
game.set_cell(6, 4, True)
game.set_cell(7, 4, True)

print("Initial state:")
display = Display()
display.clear()
display.render(game.grid, game.width, game.height)

# Run a few steps
for i in range(3):
    print(f"\nGeneration {i+1}:")
    game.step()
    display.render(game.grid, game.width, game.height)
    display.clear()

print("\nTest completed successfully!")