from .maze import Maze


class Pattern42:
    """Place and manage the closed-cell 42 pattern in a maze."""

    PATTERN = [
        "#   #  ###",
        "#   #    #",
        "#####  ###",
        "    #  #  ",
        "    #  ###",
    ]

    def __init__(
        self,
        width: int,
        height: int,
    ) -> None:
        """Initialize the 42 pattern manager.

        Args:
            width: Width of the maze.
            height: Height of the maze.
        """
        self.width = width
        self.height = height

    def place(
        self,
        maze: Maze,
        perfect: bool,
    ) -> bool:
        """Place the 42 pattern in a valid maze position.

        Args:
            maze: Maze where the pattern will be placed.
            perfect: Whether the maze is perfect.

        Returns:
            True if the pattern was placed successfully.
        """
        position = self._find_position(
            maze,
            perfect,
        )
        if position is None:
            print(
                "Error: Maze is too small "
                "or has no valid position "
                "for the 42 pattern"
            )
            return False

        start_x, start_y = position
        positions = self._get_positions(
            start_x,
            start_y,
        )

        for x, y in positions:
            cell = maze.get_cell(x, y)
            cell.blocked = True
            self._close_cell(
                maze,
                x,
                y,
            )

        return True

    def _close_cell(
        self,
        maze: Maze,
        x: int,
        y: int,
    ) -> None:
        """Close all four walls of a blocked pattern cell."""
        cell = maze.get_cell(x, y)
        for direction in ("N", "E", "S", "W"):
            maze.add_wall(
                cell,
                direction,
            )

    def _get_positions(
        self,
        start_x: int,
        start_y: int,
    ) -> list[tuple[int, int]]:
        """Return blocked-cell positions for a pattern placement."""
        positions: list[tuple[int, int]] = []

        for pattern_y, row in enumerate(self.PATTERN):
            for pattern_x, value in enumerate(row):
                if value != "#":
                    continue
                positions.append(
                    (
                        start_x + pattern_x,
                        start_y + pattern_y,
                    )
                )

        return positions

    def _get_reserved_positions(
        self,
        maze: Maze,
        perfect: bool,
    ) -> set[tuple[int, int]]:
        """Return positions that cannot contain pattern cells."""
        reserved: set[tuple[int, int]] = set()

        if maze.entry is not None:
            reserved.add(maze.entry)
        if maze.exit is not None:
            reserved.add(maze.exit)

        if not perfect:
            reserved.add((0, 0))
            reserved.add((self.width - 1, 0))
            reserved.add((0, self.height - 1))
            reserved.add(
                (
                    self.width - 1,
                    self.height - 1,
                )
            )
            center = (
                self.width // 2,
                self.height // 2,
            )
            reserved.add(center)

        return reserved

    def _is_layout_connected(
        self,
        blocked_positions: set[tuple[int, int]],
    ) -> bool:
        """Check connectivity when the pattern cells are blocked."""
        start: tuple[int, int] | None = None

        for y in range(self.height):
            for x in range(self.width):
                position = (x, y)
                if position not in blocked_positions:
                    start = position
                    break
            if start is not None:
                break

        if start is None:
            return False

        stack: list[tuple[int, int]] = [start]
        visited: set[tuple[int, int]] = {start}
        directions = (
            (0, -1),
            (1, 0),
            (0, 1),
            (-1, 0),
        )

        while stack:
            x, y = stack.pop()

            for dx, dy in directions:
                next_x = x + dx
                next_y = y + dy

                if not (
                    0 <= next_x < self.width
                    and 0 <= next_y < self.height
                ):
                    continue

                next_position = (
                    next_x,
                    next_y,
                )
                if next_position in blocked_positions:
                    continue
                if next_position in visited:
                    continue

                visited.add(next_position)
                stack.append(next_position)

        normal_cell_count = (
            self.width * self.height
            - len(blocked_positions)
        )
        return len(visited) == normal_cell_count

    def _find_position(
        self,
        maze: Maze,
        perfect: bool,
    ) -> tuple[int, int] | None:
        """Find the valid pattern position closest to maze centre."""
        pattern_height = len(self.PATTERN)
        pattern_width = len(self.PATTERN[0])

        if (
            self.width < pattern_width
            or self.height < pattern_height
        ):
            return None

        reserved = self._get_reserved_positions(
            maze,
            perfect,
        )
        candidates: list[tuple[int, int, int]] = []
        maze_center_x = self.width // 2
        maze_center_y = self.height // 2

        for start_y in range(
            self.height - pattern_height + 1
        ):
            for start_x in range(
                self.width - pattern_width + 1
            ):
                positions = self._get_positions(
                    start_x,
                    start_y,
                )
                if any(
                    position in reserved
                    for position in positions
                ):
                    continue

                blocked_positions = set(positions)
                if not self._is_layout_connected(
                    blocked_positions
                ):
                    continue

                pattern_center_x = (
                    start_x + pattern_width // 2
                )
                pattern_center_y = (
                    start_y + pattern_height // 2
                )
                distance = (
                    abs(pattern_center_x - maze_center_x)
                    + abs(pattern_center_y - maze_center_y)
                )
                candidates.append(
                    (
                        distance,
                        start_x,
                        start_y,
                    )
                )

        if not candidates:
            return None

        candidates.sort()
        _, start_x, start_y = candidates[0]
        return (start_x, start_y)
