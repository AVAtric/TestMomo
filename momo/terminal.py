"""Terminal interface for Game of Life."""

import sys
import time
from typing import Optional

from .core import GameOfLife
from .display import Display


class TerminalInterface:
    """Terminal interface for running the Game of Life."""

    def __init__(self, width: int = 50, height: int = 25, speed: int = 100,
                 seed: Optional[int] = None):
        """
        Initialize the terminal interface.

        Args:
            width: Grid width
            height: Grid height
            speed: Simulation speed in milliseconds
            seed: Random seed for reproducible randomization
        """
        self.game = GameOfLife(width, height, seed)
        self.display = Display()
        self.speed = speed
        self.running = True
        self.paused = False
        self.generation = 0
        self.seed = seed

    def handle_input(self) -> None:
        """Handle keyboard input."""
        if sys.stdin in sys.__dict__.get('_stdio_original', {}):
            # Use select-based input for non-blocking reading
            import select

            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                key = sys.stdin.read(1)

                if key == ' ':
                    self.paused = not self.paused
                elif key == 'N':
                    if self.paused:
                        self.game.step()
                        self.generation += 1
                elif key == 'R':
                    self.game.randomize(self.seed)
                    self.generation = 0
                elif key == 'C':
                    self.game.clear()
                    self.generation = 0
                elif key == 'q' or key == 'Q':
                    self.running = False
        else:
            # Use getpass alternative for non-blocking input
            import termios

            try:
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    new_settings = termios.tcgetattr(fd)
                    new_settings[3] &= ~termios.ICANON & ~termios.ECHO
                    termios.tcsetattr(fd, termios.TCSANOW, new_settings)

                    if select.select([sys.stdin], [], [], 0)[0]:
                        key = sys.stdin.read(1)

                        if key == ' ':
                            self.paused = not self.paused
                        elif key == 'N':
                            if self.paused:
                                self.game.step()
                                self.generation += 1
                        elif key == 'R':
                            self.game.randomize(self.seed)
                            self.generation = 0
                        elif key == 'C':
                            self.game.clear()
                            self.generation = 0
                        elif key == 'q' or key == 'Q':
                            self.running = False
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            except Exception:
                pass

    def run(self) -> None:
        """Run the simulation."""
        self.display.hide_cursor()

        try:
            self.display.render_with_controls(
                self.game.grid,
                self.game.get_width(),
                self.game.get_height(),
                self.generation,
                self.paused,
                "Space:Pause N:Step R:Random C:Clear Q:Quit"
            )

            while self.running:
                if not self.paused:
                    self.game.step()
                    self.generation += 1

                self.display.render_with_controls(
                    self.game.grid,
                    self.game.get_width(),
                    self.game.get_height(),
                    self.generation,
                    self.paused
                )

                # Handle input
                self.handle_input()

                # Sleep to control speed
                if self.speed > 0 and not self.paused:
                    time.sleep(self.speed / 1000.0)

        finally:
            self.display.show_cursor()
            self.display.clear()


def parse_args():
    """Parse command line arguments."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Conway's Game of Life terminal simulation"
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
        help="Simulation speed in milliseconds (default: 100)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducible randomization"
    )

    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()

    # Validate arguments
    if args.width <= 0 or args.height <= 0:
        print("Error: Width and height must be positive integers")
        sys.exit(1)

    if args.speed < 0:
        print("Error: Speed must be non-negative")
        sys.exit(1)

    interface = TerminalInterface(args.width, args.height, args.speed, args.seed)
    interface.run()


if __name__ == "__main__":
    main()