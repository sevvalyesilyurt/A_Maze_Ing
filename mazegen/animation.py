
"""Animate maze generation and shortest-path visualization."""

import sys
from time import sleep

from .maze import Maze
from .renderer import MazeRenderer


class MazeAnimator:
    """Display maze generation and solution animations in the terminal."""

    def __init__(
        self,
        renderer: MazeRenderer,
        delay: float = 0.02,
        every: int = 3,
    ) -> None:
        """Set the renderer, frame delay, and update interval."""
        if delay < 0 or every < 1:
            raise ValueError("Invalid animation settings")
        self.renderer = renderer
        self.delay = delay
        self.every = every
        self.steps = 0

    def draw(self, maze: Maze) -> None:
        """Show one frame for every selected number of updates."""
        self.steps += 1
        if self.steps % self.every != 0:
            return
        self._show(maze)

    def finish(self, maze: Maze) -> None:
        """Always display the completed maze before returning."""
        self._show(maze)

    def _show(self, maze: Maze) -> None:
        """Redraw the maze in place without changing its state."""
        sys.stdout.write("\033[H\033[2J")
        sys.stdout.write(self.renderer.render(maze))
        sys.stdout.write(
            f"\nGenerating maze... {self.steps} updates\n"
        )
        sys.stdout.flush()
        sleep(self.delay)

    def animate_solution(
        self,
        maze: Maze,
        path: str,
        delay: float = 0.06,
    ) -> None:
        """Reveal the shortest route from entry to exit step by step."""
        if delay < 0:
            raise ValueError("Animation delay cannot be negative")

        for step in range(len(path) + 1):
            sys.stdout.write("\033[H\033[2J")
            sys.stdout.write(
                self.renderer.render(maze, path[:step])
            )
            sys.stdout.write(
                f"\nShortest path: {step}/{len(path)} steps\n"
            )
            sys.stdout.flush()
            sleep(delay)
