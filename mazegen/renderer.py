from .maze import Maze


class MazeRenderer:
    """Render a maze in the terminal using Unicode characters."""

    WALL_COLORS = {
        "default": "",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
    }

    CONTENT_COLORS = {
        "default": {
            "path": "\033[96m",
            "entry": "\033[92m",
            "exit": "\033[91m",
            "pattern": "\033[95m",
        },
        "red": {
            "path": "\033[93m",
            "entry": "\033[96m",
            "exit": "\033[95m",
            "pattern": "\033[92m",
        },
        "green": {
            "path": "\033[95m",
            "entry": "\033[96m",
            "exit": "\033[93m",
            "pattern": "\033[91m",
        },
        "yellow": {
            "path": "\033[95m",
            "entry": "\033[92m",
            "exit": "\033[91m",
            "pattern": "\033[96m",
        },
        "blue": {
            "path": "\033[93m",
            "entry": "\033[92m",
            "exit": "\033[91m",
            "pattern": "\033[95m",
        },
        "magenta": {
            "path": "\033[96m",
            "entry": "\033[92m",
            "exit": "\033[93m",
            "pattern": "\033[91m",
        },
        "cyan": {
            "path": "\033[93m",
            "entry": "\033[92m",
            "exit": "\033[91m",
            "pattern": "\033[95m",
        },
    }

    RESET = "\033[0m"

    JUNCTIONS = {
        (False, False, False, False): " ",
        (True, False, False, False): "╵",
        (False, True, False, False): "╴",
        (False, False, True, False): "╷",
        (False, False, False, True): "╶",
        (True, True, False, False): "┗",
        (True, False, False, True): "┛",
        (False, True, True, False): "┏",
        (False, False, True, True): "┓",
        (True, False, True, False): "┃",
        (False, True, False, True): "━",
        (True, True, True, False): "┣",
        (True, False, True, True): "┫",
        (True, True, False, True): "┻",
        (False, True, True, True): "┳",
        (True, True, True, True): "╋",
    }

    def __init__(self) -> None:
        """Initialize the renderer with the default wall color."""
        self.wall_color = "default"

    def set_wall_color(
        self,
        color: str,
    ) -> None:
        """Set the terminal color used for maze rendering.

        Args:
            color: Name of the maze color.

        Raises:
            ValueError: If the requested color is not supported.
        """
        if color not in self.WALL_COLORS:
            raise ValueError(
                f"Invalid wall color: {color}"
            )
        self.wall_color = color

    def _color(
        self,
        value: str,
    ) -> str:
        """Apply the selected terminal color to a wall."""
        color = self.WALL_COLORS[self.wall_color]
        if color == "":
            return value
        return color + value + self.RESET

    def _color_content(
        self,
        value: str,
        content_type: str,
    ) -> str:
        """Apply a matching color to maze content."""
        color = self.CONTENT_COLORS[
            self.wall_color
        ][content_type]

        if color == "":
            return value

        return color + value + self.RESET

    def _get_door_side(
        self,
        maze: Maze,
        position: tuple[int, int] | None,
    ) -> str | None:
        """Return the outer border used as a visual maze door."""
        if position is None:
            return None

        x, y = position

        if x == 0:
            return "west"
        if x == maze.width - 1:
            return "east"
        if y == 0:
            return "north"
        if y == maze.height - 1:
            return "south"

        return None

    def _is_horizontal_door(
        self,
        maze: Maze,
        x: int,
        y: int,
    ) -> bool:
        """Check whether a horizontal border contains a visual door."""
        for position in (maze.entry, maze.exit):
            side = self._get_door_side(
                maze,
                position,
            )

            if position is None:
                continue

            door_x, _ = position

            if side == "north" and y == 0 and x == door_x:
                return True

            if (
                side == "south"
                and y == maze.height
                and x == door_x
            ):
                return True

        return False

    def _is_vertical_door(
        self,
        maze: Maze,
        x: int,
        y: int,
    ) -> bool:
        """Check whether a vertical border contains a visual door."""
        for position in (maze.entry, maze.exit):
            side = self._get_door_side(
                maze,
                position,
            )

            if position is None:
                continue

            _, door_y = position

            if side == "west" and x == 0 and y == door_y:
                return True

            if (
                side == "east"
                and x == maze.width
                and y == door_y
            ):
                return True

        return False

    def _get_path_positions(
        self,
        maze: Maze,
        path: str | None,
    ) -> set[tuple[int, int]]:
        """Return all maze positions belonging to the solution path."""
        if path is None:
            return set()
        if maze.entry is None:
            return set()

        x, y = maze.entry
        positions: set[tuple[int, int]] = set()
        directions = {
            "N": (0, -1),
            "E": (1, 0),
            "S": (0, 1),
            "W": (-1, 0),
        }

        for direction in path:
            if direction not in directions:
                continue

            dx, dy = directions[direction]
            x += dx
            y += dy
            positions.add((x, y))

        return positions

    def _get_cell_content(
        self,
        maze: Maze,
        x: int,
        y: int,
        path_positions: set[tuple[int, int]],
    ) -> str:
        """Return the visual content displayed inside a maze cell."""
        position = (x, y)
        cell = maze.get_cell(x, y)

        if position == maze.entry:
            return self._color_content(
                " E ",
                "entry",
            )
        if position == maze.exit:
            return self._color_content(
                " X ",
                "exit",
            )
        if cell.blocked:
            return self._color_content(
                "###",
                "pattern",
            )
        if position in path_positions:
            return self._color_content(
                " ● ",
                "path",
            )
        return "   "

    def _has_horizontal_wall(
        self,
        maze: Maze,
        x: int,
        y: int,
    ) -> bool:
        """Check whether a horizontal wall exists at a position."""
        if x < 0 or x >= maze.width:
            return False

        if self._is_horizontal_door(
            maze,
            x,
            y,
        ):
            return False

        if y == 0:
            return maze.get_cell(
                x,
                0,
            ).north
        if y == maze.height:
            return maze.get_cell(
                x,
                maze.height - 1,
            ).south
        return maze.get_cell(
            x,
            y,
        ).north

    def _has_vertical_wall(
        self,
        maze: Maze,
        x: int,
        y: int,
    ) -> bool:
        """Check whether a vertical wall exists at a position."""
        if y < 0 or y >= maze.height:
            return False

        if self._is_vertical_door(
            maze,
            x,
            y,
        ):
            return False

        if x == 0:
            return maze.get_cell(
                0,
                y,
            ).west
        if x == maze.width:
            return maze.get_cell(
                maze.width - 1,
                y,
            ).east
        return maze.get_cell(
            x,
            y,
        ).west

    def _get_junction(
        self,
        maze: Maze,
        x: int,
        y: int,
    ) -> str:
        """Return the Unicode junction character for a position."""
        north = self._has_vertical_wall(
            maze,
            x,
            y - 1,
        )
        east = self._has_horizontal_wall(
            maze,
            x,
            y,
        )
        south = self._has_vertical_wall(
            maze,
            x,
            y,
        )
        west = self._has_horizontal_wall(
            maze,
            x - 1,
            y,
        )

        junction = self.JUNCTIONS[
            (
                north,
                east,
                south,
                west,
            )
        ]
        return self._color(junction)

    def _get_horizontal_line(
        self,
        maze: Maze,
        y: int,
    ) -> str:
        """Build one horizontal wall line of the rendered maze."""
        line = ""

        for x in range(maze.width + 1):
            line += self._get_junction(
                maze,
                x,
                y,
            )
            if x == maze.width:
                continue

            if self._has_horizontal_wall(
                maze,
                x,
                y,
            ):
                line += self._color("━━━")
            else:
                line += "   "

        return line

    def render(
        self,
        maze: Maze,
        path: str | None = None,
    ) -> str:
        """Render the maze as terminal text.

        Args:
            maze: Maze structure to render.
            path: Optional solution path to display.

        Returns:
            The complete rendered maze as a string.
        """
        lines: list[str] = []
        path_positions = self._get_path_positions(
            maze,
            path,
        )

        lines.append(
            self._get_horizontal_line(
                maze,
                0,
            )
        )

        for y, row in enumerate(maze.cells):
            line = ""

            for cell in row:
                if self._has_vertical_wall(
                    maze,
                    cell.x,
                    cell.y,
                ):
                    line += self._color("┃")
                else:
                    line += " "

                line += self._get_cell_content(
                    maze,
                    cell.x,
                    cell.y,
                    path_positions,
                )

            if self._has_vertical_wall(
                maze,
                maze.width,
                y,
            ):
                line += self._color("┃")
            else:
                line += " "

            lines.append(line)
            lines.append(
                self._get_horizontal_line(
                    maze,
                    y + 1,
                )
            )

        return "\n".join(lines)
