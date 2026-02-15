import sys

from .core import GameOfLife


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
        self.running = True
        while self.running:
            self.game.render()
            if not self.paused:
                self.step()
            if self.speed:
                import time
                time.sleep(self.speed / 1000)
