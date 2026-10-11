from .cell import Cell
from .maze import Maze


class MazeValidator:
    """Validate structural properties of a maze."""

    def __init__(
        self,
        maze: Maze,
    ) -> None:
        """Initialize the maze validator.

        Args:
            maze: Maze structure to validate.
        """
        self.maze = maze

    def all_normal_cells_visited(
        self,
    ) -> bool:
        """Check whether every non-blocked cell was visited."""
        for row in self.maze.cells:
            for cell in row:
                if (
                    not cell.blocked
                    and not cell.visited
                ):
                    return False
        return True

    def is_fully_connected(
        self,
    ) -> bool:
        """Check whether all non-blocked cells are connected."""
        start: Cell | None = None

        for row in self.maze.cells:
            for cell in row:
                if not cell.blocked:
                    start = cell
                    break
            if start is not None:
                break

        if start is None:
            return False

        stack: list[Cell] = [start]
        visited: set[tuple[int, int]] = {
            (start.x, start.y)
        }

        while stack:
            current = stack.pop()
            neighbors = self.maze.get_neighbors(current)

            for direction, neighbor in neighbors.items():
                if neighbor.blocked:
                    continue
                if not self.maze.can_move(
                    current,
                    direction,
                ):
                    continue

                position = (
                    neighbor.x,
                    neighbor.y,
                )
                if position in visited:
                    continue

                visited.add(position)
                stack.append(neighbor)

        normal_cell_count = sum(
            1
            for row in self.maze.cells
            for cell in row
            if not cell.blocked
        )
        return len(visited) == normal_cell_count

    def is_open_block(
        self,
        start_x: int,
        start_y: int,
        width: int,
        height: int,
    ) -> bool:
        """Check whether a rectangular area is completely open."""
        for y in range(
            start_y,
            start_y + height,
        ):
            for x in range(
                start_x,
                start_x + width,
            ):
                cell = self.maze.get_cell(
                    x,
                    y,
                )
                if cell.blocked:
                    return False

                if x < start_x + width - 1:
                    if cell.east:
                        return False
                if y < start_y + height - 1:
                    if cell.south:
                        return False

        return True

    def has_open_3x3(
        self,
    ) -> bool:
        """Check whether the maze contains a fully open 3x3 area."""
        if (
            self.maze.width < 3
            or self.maze.height < 3
        ):
            return False

        for y in range(self.maze.height - 2):
            for x in range(self.maze.width - 2):
                if self.is_open_block(
                    x,
                    y,
                    3,
                    3,
                ):
                    return True
        return False

    def count_dead_ends(self) -> int:
        """Return the number of dead-end cells in the maze."""
        dead_end_count = 0

        for row in self.maze.cells:
            for cell in row:
                if cell.blocked:
                    continue

                neighbors = self.maze.get_neighbors(cell)
                open_count = sum(
                    1
                    for direction in neighbors
                    if self.maze.can_move(
                        cell,
                        direction,
                    )
                )

                if open_count == 1:
                    dead_end_count += 1

        return dead_end_count
