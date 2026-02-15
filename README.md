# Game of Life - Momo

A terminal-based implementation of Conway's Game of Life.

## Features

- Terminal display with in-place refresh (no scrolling)
- Controls:
  - `Space`: Pause/Resume
  - `N`: Step one generation (when paused)
  - `R`: Randomize grid
  - `C`: Clear grid
  - `Q`: Quit
- Optional command-line arguments:
  - `--width`: Grid width (default: 50)
  - `--height`: Grid height (default: 25)
  - `--speed`: Simulation speed in milliseconds (default: 100)
  - `--seed`: Random seed for reproducible randomization

## Installation

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
```

## Usage

Run the simulation:

```bash
python3 -m momo [options]
```

Example:

```bash
python3 -m momo --width 50 --height 25 --speed 100
```

## License

MIT