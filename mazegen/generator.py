from random import Random

from .cell import Cell
from .maze import Maze
from .pattern import Pattern42
from .validator import MazeValidator


class MazeGenerator:
    """Generate perfect and non-perfect maze structures."""

    def __init__(
        self,
        width: int,
        height: int,
        seed: int | None = None,
    ) -> None:
        """Initialize the maze generator.

        Args:
            width: Width of the maze.
            height: Height of the maze.
            seed: Optional seed for reproducible generation.
        """
        self.width = width
        self.height = height
        self.rng = Random(seed)
        self.pattern = Pattern42(
            width,
            height,
        )

    def generate(
        self,
        entry: tuple[int, int],
        exit: tuple[int, int],
        perfect: bool = True,
    ) -> Maze:
        """Generate and return a maze.

        Args:
            entry: Entry coordinates.
            exit: Exit coordinates.
            perfect: Whether to generate a perfect maze.

        Returns:
            The generated maze.

        Raises:
            ValueError: If the generated maze is invalid.
        """
        maze = Maze(
            self.width,
            self.height,
        )
        maze.set_entry(entry)
        maze.set_exit(exit)
        self.pattern.place(
            maze,
            perfect,
        )
        self._generate_paths(
            maze,
            entry,
        )

        validator = MazeValidator(maze)
        if not validator.all_normal_cells_visited():
            raise ValueError(
                "42 pattern makes the maze "
                "disconnected"
            )

        if not perfect:
            self._add_loops(maze)
            self._open_corner_corridors(maze)
            self._open_centre_corridor(maze)
            self._reduce_dead_ends(maze)

        if not validator.is_fully_connected():
            raise ValueError(
                "Generated maze is not "
                "fully connected"
            )
        return maze

    def _open_corridor_cell(
        self,
        maze: Maze,
        x: int,
        y: int,
    ) -> None:
        """Ensure a cell has at least two open connections."""
        cell = maze.get_cell(x, y)
        if cell.blocked:
            return

        neighbors = maze.get_neighbors(cell)
        directions = list(neighbors.keys())
        self.rng.shuffle(directions)
        open_count = sum(
            1
            for direction in directions
            if maze.can_move(cell, direction)
        )

        for direction in directions:
            if open_count >= 2:
                break
            if maze.can_move(cell, direction):
                continue
            if self._try_remove_wall(
                maze,
                cell,
                direction,
            ):
                open_count += 1

    def _open_corner_corridors(
        self,
        maze: Maze,
    ) -> None:
        """Ensure the four maze corners are open corridors."""
        corners = [
            (0, 0),
            (self.width - 1, 0),
            (0, self.height - 1),
            (
                self.width - 1,
                self.height - 1,
            ),
        ]
        for x, y in corners:
            self._open_corridor_cell(
                maze,
                x,
                y,
            )

    def _open_centre_corridor(
        self,
        maze: Maze,
    ) -> None:
        """Ensure the centre cell is an open corridor."""
        centre_x = self.width // 2
        centre_y = self.height // 2
        self._open_corridor_cell(
            maze,
            centre_x,
            centre_y,
        )

    def _generate_paths(
        self,
        maze: Maze,
        entry: tuple[int, int],
    ) -> None:
        """Generate maze paths using iterative depth-first search."""
        x, y = entry
        current = maze.get_cell(
            x,
            y,
        )
        if current.blocked:
            raise ValueError(
                "Entry cannot be a blocked cell"
            )

        current.visited = True
        stack: list[Cell] = [current]

        while stack:
            current = stack[-1]
            neighbors = maze.get_neighbors(current)
            unvisited = [
                (direction, neighbor)
                for direction, neighbor in neighbors.items()
                if (
                    not neighbor.visited
                    and not neighbor.blocked
                )
            ]

            if unvisited:
                direction, next_cell = self.rng.choice(
                    unvisited
                )
                maze.remove_wall(
                    current,
                    direction,
                )
                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()

    def _count_open_directions(
        self,
        cell: Cell,
    ) -> int:
        """Return the number of open sides of a cell."""
        count = 0
        if not cell.north:
            count += 1
        if not cell.east:
            count += 1
        if not cell.south:
            count += 1
        if not cell.west:
            count += 1
        return count

    def _get_dead_ends(
        self,
        maze: Maze,
    ) -> list[Cell]:
        """Return all non-blocked dead-end cells."""
        dead_ends: list[Cell] = []
        for row in maze.cells:
            for cell in row:
                if cell.blocked:
                    continue
                if self._count_open_directions(cell) == 1:
                    dead_ends.append(cell)
        return dead_ends

    def _get_closed_walls(
        self,
        maze: Maze,
    ) -> list[tuple[Cell, str]]:
        """Return removable closed walls between normal cells."""
        candidates: list[tuple[Cell, str]] = []

        for y in range(self.height):
            for x in range(self.width):
                cell = maze.get_cell(x, y)
                if cell.blocked:
                    continue

                if x < self.width - 1:
                    east_neighbor = maze.get_cell(
                        x + 1,
                        y,
                    )
                    if (
                        cell.east
                        and not east_neighbor.blocked
                    ):
                        candidates.append(
                            (cell, "E")
                        )

                if y < self.height - 1:
                    south_neighbor = maze.get_cell(
                        x,
                        y + 1,
                    )
                    if (
                        cell.south
                        and not south_neighbor.blocked
                    ):
                        candidates.append(
                            (cell, "S")
                        )
        return candidates

    def _get_closed_directions(
        self,
        maze: Maze,
        cell: Cell,
    ) -> list[str]:
        """Return closed directions leading to normal neighbors."""
        directions: list[str] = []
        neighbors = maze.get_neighbors(cell)

        for direction, neighbor in neighbors.items():
            if neighbor.blocked:
                continue
            if not maze.can_move(
                cell,
                direction,
            ):
                directions.append(direction)
        return directions

    def _try_reduce_dead_end(
        self,
        maze: Maze,
        cell: Cell,
    ) -> bool:
        """Try to remove a wall to reduce a dead end."""
        if cell.blocked:
            return False
        if self._count_open_directions(cell) != 1:
            return False

        directions = self._get_closed_directions(
            maze,
            cell,
        )
        self.rng.shuffle(directions)

        for direction in directions:
            if self._try_remove_wall(
                maze,
                cell,
                direction,
            ):
                return True
        return False

    def _reduce_dead_ends(
        self,
        maze: Maze,
    ) -> None:
        """Reduce dead ends in a non-perfect maze."""
        max_passes = 3

        for _ in range(max_passes):
            dead_ends = self._get_dead_ends(maze)
            if not dead_ends:
                return

            self.rng.shuffle(dead_ends)
            changed = False

            for cell in dead_ends:
                if self._try_reduce_dead_end(
                    maze,
                    cell,
                ):
                    changed = True

            if not changed:
                return

    def _add_loops(
        self,
        maze: Maze,
    ) -> None:
        """Add multiple loops to a non-perfect maze."""
        candidates = self._get_closed_walls(maze)
        if not candidates:
            return

        self.rng.shuffle(candidates)
        loop_count = max(
            2,
            (
                self.width
                * self.height
            ) // 10,
        )
        loop_count = min(
            loop_count,
            len(candidates),
        )

        added_loops = 0
        for cell, direction in candidates:
            if added_loops >= loop_count:
                break
            if self._try_remove_wall(
                maze,
                cell,
                direction,
            ):
                added_loops += 1

    def _try_remove_wall(
        self,
        maze: Maze,
        cell: Cell,
        direction: str,
    ) -> bool:
        """Try to remove a wall without creating an open 3x3 area.

        Returns:
            True if the wall was removed successfully.
        """
        maze.remove_wall(
            cell,
            direction,
        )
        validator = MazeValidator(maze)

        if validator.has_open_3x3():
            maze.add_wall(
                cell,
                direction,
            )
            return False
        return True
