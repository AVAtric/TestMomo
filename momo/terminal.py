"""Interface for running the Game of Life in a terminal.

Parameters
----------
width: int
    Width of the display area (in cells).
height: int
    Height of the display area (in cells).
speed: int | None
    Milliseconds per generation. ``None`` disables automatic stepping.
seed: int | None
    Seed for deterministic randomization.
"""

import argparse
import select
import sys
import termios
import time
import tty

from .core import GameOfLife
from .display import Display


class TerminalInterface:
    """Interface for running the Game of Life in a terminal.

    Parameters
    ----------
    width: int
        Width of the display area (in cells).
    height: int
        Height of the display area (in cells).
    speed: int | None
        Milliseconds per generation. ``None`` disables automatic stepping.
    seed: int | None
        Seed for deterministic randomization.
    """

    def __init__(self, width: int, height: int, speed: int | None = None, seed: int | None = None):
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive")
        if speed is not None and speed < 0:
            raise ValueError("speed must be non-negative")
        self.width = width
        self.height = height
        self.speed = speed if speed is not None else 100
        self.seed = seed
        self.game = GameOfLife(width, height, seed)
        self.generation = 0
        self.paused = False
        self.running = False
        # Wrap step and clear to track generation
        original_step = self.game.step
        original_clear = self.game.clear
        def wrapped_step():
            original_step()
            self.generation += 1
        def wrapped_clear():
            original_clear()
            self.generation = 0
        self.game.step = wrapped_step
        self.game.clear = wrapped_clear

    def toggle_pause(self) -> None:
        self.paused = not self.paused

    def step(self) -> None:
        self.game.step()

    def randomize(self) -> None:
        self.game.randomize()

    def clear(self) -> None:
        self.game.clear()

    def quit(self) -> None:
        self.running = False

    def run(self):
        """Run the main simulation loop with keyboard controls."""
        self.running = True
        display = Display()
        display.hide_cursor()
        try:
            while self.running:
                display.render(self.game.grid, self.width, self.height)
                if not self.paused:
                    self.step()
                if self.speed:
                    time.sleep(self.speed / 1000)
        finally:
            display.show_cursor()


def main():
    """Entry point for running the Game of Life from command line.

    Parses command-line arguments and starts the terminal interface.
    """
    parser = argparse.ArgumentParser(
        description="Conway's Game of Life - Terminal Edition"
    )
    parser.add_argument(
        "--width",
        type=int,
        default=50,
        help="Grid width (default: 50)"
    )
    parser.add_argument(
        "--height",
        type=int,
        default=25,
        help="Grid height (default: 25)"
    )
    parser.add_argument(
        "--speed",
        type=int,
        default=100,
        help="Delay between generations in milliseconds (default: 100)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for deterministic output"
    )
    args = parser.parse_args()

    interface = TerminalInterface(
        width=args.width,
        height=args.height,
        speed=args.speed,
        seed=args.seed
    )

    print(f"Game of Life initialized: {args.width}x{args.height}")
    print("Controls: Space=Pause, N=Step, R=Random, C=Clear, Q=Quit")

    # Set up terminal for raw input if possible
    old_settings = None
    try:
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
    except (termios.error, OSError):
        pass

    try:
        interface.run()

        # Handle keyboard input while running
        while interface.running:
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                char = sys.stdin.read(1)
                if char == ' ':
                    interface.toggle_pause()
                elif char == 'n':
                    interface.step()
                elif char == 'r':
                    interface.randomize()
                elif char == 'c':
                    interface.clear()
                elif char == 'q':
                    interface.quit()
    finally:
        if old_settings:
            try:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            except (termios.error, OSError):
                pass
