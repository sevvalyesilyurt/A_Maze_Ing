from collections import deque

from .maze import Maze


class MazeSolver:
    """Find the shortest path between maze entry and exit."""

    def __init__(self, maze: Maze) -> None:
        """Initialize the solver.

        Args:
            maze: Maze structure to solve.
        """
        self.maze = maze

    def solve(self) -> str:
        """Find the shortest path from entry to exit using BFS.

        Returns:
            Shortest path encoded with N, E, S, and W directions.

        Raises:
            ValueError: If entry or exit is not set, or no path exists.
        """
        if self.maze.entry is None:
            raise ValueError("Maze entry is not set")
        if self.maze.exit is None:
            raise ValueError("Maze exit is not set")

        start = self.maze.entry
        target = self.maze.exit
        queue = deque([start])
        previous: dict[
            tuple[int, int],
            tuple[tuple[int, int], str] | None,
        ] = {start: None}
        directions = {
            "N": (0, -1),
            "E": (1, 0),
            "S": (0, 1),
            "W": (-1, 0),
        }

        while queue:
            current = queue.popleft()
            if current == target:
                return self._build_path(
                    previous,
                    target,
                )

            x, y = current
            cell = self.maze.get_cell(x, y)

            for direction, (dx, dy) in directions.items():
                if not self.maze.can_move(
                    cell,
                    direction,
                ):
                    continue

                next_position = (
                    x + dx,
                    y + dy,
                )
                next_cell = self.maze.get_cell(
                    next_position[0],
                    next_position[1],
                )

                if next_cell.blocked:
                    continue
                if next_position not in previous:
                    previous[next_position] = (
                        current,
                        direction,
                    )
                    queue.append(next_position)

        raise ValueError(
            "No path from entry to exit"
        )

    def _build_path(
        self,
        previous: dict[
            tuple[int, int],
            tuple[tuple[int, int], str] | None,
        ],
        target: tuple[int, int],
    ) -> str:
        """Build the path by following parent positions backwards.

        Args:
            previous: Mapping containing each position's parent and direction.
            target: Exit position where path reconstruction begins.

        Returns:
            Path encoded with N, E, S, and W directions.
        """
        path: list[str] = []
        current = target

        while True:
            step = previous[current]
            if step is None:
                break

            parent, direction = step
            path.append(direction)
            current = parent

        path.reverse()
        return "".join(path)
