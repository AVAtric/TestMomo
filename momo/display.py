"""Terminal display for Game of Life."""

from typing import Optional, List


class Display:
    """Terminal display for the Game of Life."""

    ALIVE_CHAR = "█"
    DEAD_CHAR = "░"
    CLEAR_SEQ = "\033[2J\033[H"

    def __init__(self):
        """Initialize the display."""
        self._cursor_visible = True

    def hide_cursor(self) -> None:
        """Hide the cursor."""
        print("\033[?25l", end="", flush=True)
        self._cursor_visible = False

    def show_cursor(self) -> None:
        """Show the cursor."""
        if not self._cursor_visible:
            print("\033[?25h", end="", flush=True)
            self._cursor_visible = True

    def clear(self) -> None:
        """Clear the terminal screen."""
        print(self.CLEAR_SEQ, end="", flush=True)

    def render(self, grid: List[List[bool]], width: int, height: int) -> None:
        """
        Render the grid to the terminal.

        Args:
            grid: 2D grid of boolean values
            width: Grid width
            height: Grid height
        """
        # Clear screen
        self.clear()

        # Render each row
        for y in range(height):
            line = ""
            for x in range(width):
                if grid[y][x]:
                    line += self.ALIVE_CHAR
                else:
                    line += self.DEAD_CHAR
            print(line)

    def render_with_info(self, grid: List[List[bool]], width: int, height: int,
                         generation: int, paused: bool) -> None:
        """
        Render the grid with status information.

        Args:
            grid: 2D grid of boolean values
            width: Grid width
            height: Grid height
            generation: Current generation number
            paused: Whether simulation is paused
        """
        self.clear()

        # Render grid
        for y in range(height):
            line = ""
            for x in range(width):
                if grid[y][x]:
                    line += self.ALIVE_CHAR
                else:
                    line += self.DEAD_CHAR
            print(line)

        # Render status line
        status = "PAUSED" if paused else "RUNNING"
        info = f"Gen: {generation} | {status} | Space:Pause N:Step R:Random C:Clear Q:Quit"
        print("\n" + info)

    def render_with_controls(self, grid: List[List[bool]], width: int, height: int,
                             generation: int, paused: bool, controls: Optional[str] = None) -> None:
        """
        Render the grid with controls help.

        Args:
            grid: 2D grid of boolean values
            width: Grid width
            height: Grid height
            generation: Current generation number
            paused: Whether simulation is paused
            controls: Additional control hints
        """
        self.clear()

        # Render grid
        for y in range(height):
            line = ""
            for x in range(width):
                if grid[y][x]:
                    line += self.ALIVE_CHAR
                else:
                    line += self.DEAD_CHAR
            print(line)

        # Render status line
        status = "PAUSED" if paused else "RUNNING"
        base_info = f"Gen: {generation} | {status}"
        print("\n" + base_info)

        # Render controls if provided
        if controls:
            print(controls)