from .cell import Cell


class Maze:
    """Represent the maze structure and manage its cells and walls."""

    def __init__(
        self,
        width: int,
        height: int,
    ) -> None:
        """Initialize a maze with fully closed cells.

        Args:
            width: Number of cells in the horizontal direction.
            height: Number of cells in the vertical direction.
        """
        self.width = width
        self.height = height
        self.cells = [
            [Cell(x, y) for x in range(width)]
            for y in range(height)
        ]
        self.entry: tuple[int, int] | None = None
        self.exit: tuple[int, int] | None = None

    def is_inside(
        self,
        x: int,
        y: int,
    ) -> bool:
        """Check whether coordinates are inside the maze.

        Args:
            x: Horizontal coordinate.
            y: Vertical coordinate.

        Returns:
            True if the coordinates are inside the maze.
        """
        return (
            0 <= x < self.width
            and 0 <= y < self.height
        )

    def get_cell(
        self,
        x: int,
        y: int,
    ) -> Cell:
        """Return the cell at the given coordinates.

        Args:
            x: Horizontal coordinate.
            y: Vertical coordinate.

        Returns:
            The cell at the given coordinates.

        Raises:
            ValueError: If the coordinates are outside the maze.
        """
        if not self.is_inside(x, y):
            raise ValueError(
                f"Cell ({x}, {y}) is outside maze"
            )
        return self.cells[y][x]

    def get_boundary_directions(
        self,
        x: int,
        y: int,
    ) -> list[str]:
        """Return maze boundaries touched by a cell.

        Args:
            x: Horizontal coordinate.
            y: Vertical coordinate.

        Returns:
            Cardinal directions that touch the maze boundary.
        """
        directions: list[str] = []
        if y == 0:
            directions.append("N")
        if x == self.width - 1:
            directions.append("E")
        if y == self.height - 1:
            directions.append("S")
        if x == 0:
            directions.append("W")
        return directions

    def get_neighbors(
        self,
        cell: Cell,
    ) -> dict[str, Cell]:
        """Return valid neighboring cells by direction.

        Args:
            cell: Cell whose neighbors will be found.

        Returns:
            Mapping of directions to neighboring cells.
        """
        neighbors: dict[str, Cell] = {}
        directions = {
            "N": (0, -1),
            "E": (1, 0),
            "S": (0, 1),
            "W": (-1, 0),
        }

        for direction, (dx, dy) in directions.items():
            nx = cell.x + dx
            ny = cell.y + dy
            if self.is_inside(nx, ny):
                neighbors[direction] = self.get_cell(
                    nx,
                    ny,
                )
        return neighbors

    def remove_wall(
        self,
        cell: Cell,
        direction: str,
    ) -> None:
        """Remove a wall between a cell and its neighbor.

        Args:
            cell: Cell whose wall will be removed.
            direction: Direction of the wall.

        Raises:
            ValueError: If the direction has no neighbor or is invalid.
        """
        neighbors = self.get_neighbors(cell)
        if direction not in neighbors:
            raise ValueError(
                "Cell has no neighbor in "
                f"direction: {direction}"
            )

        neighbor = neighbors[direction]
        if direction == "N":
            cell.north = False
            neighbor.south = False
        elif direction == "E":
            cell.east = False
            neighbor.west = False
        elif direction == "S":
            cell.south = False
            neighbor.north = False
        elif direction == "W":
            cell.west = False
            neighbor.east = False
        else:
            raise ValueError(
                f"Invalid direction: {direction}"
            )

    def add_wall(
        self,
        cell: Cell,
        direction: str,
    ) -> None:
        """Add a wall to a cell and its neighbor.

        Args:
            cell: Cell whose wall will be added.
            direction: Direction of the wall.

        Raises:
            ValueError: If the direction is invalid.
        """
        neighbors = self.get_neighbors(cell)

        if direction == "N":
            cell.north = True
            if "N" in neighbors:
                neighbors["N"].south = True
        elif direction == "E":
            cell.east = True
            if "E" in neighbors:
                neighbors["E"].west = True
        elif direction == "S":
            cell.south = True
            if "S" in neighbors:
                neighbors["S"].north = True
        elif direction == "W":
            cell.west = True
            if "W" in neighbors:
                neighbors["W"].east = True
        else:
            raise ValueError(
                f"Invalid direction: {direction}"
            )

    def can_move(
        self,
        cell: Cell,
        direction: str,
    ) -> bool:
        """Check whether movement is possible in a direction.

        Args:
            cell: Cell from which movement starts.
            direction: Direction to check.

        Returns:
            True if there is no wall in the given direction.

        Raises:
            ValueError: If the direction is invalid.
        """
        if direction == "N":
            return not cell.north
        if direction == "E":
            return not cell.east
        if direction == "S":
            return not cell.south
        if direction == "W":
            return not cell.west
        raise ValueError(
            f"Invalid direction: {direction}"
        )

    def to_hex_grid(self) -> list[str]:
        """Convert the maze cells to hexadecimal rows.

        Returns:
            Maze rows encoded as hexadecimal strings.
        """
        return [
            "".join(cell.to_hex() for cell in row)
            for row in self.cells
        ]

    def set_entry(
        self,
        position: tuple[int, int],
    ) -> None:
        """Set the maze entry position.

        Args:
            position: Entry coordinates as an (x, y) tuple.

        Raises:
            ValueError: If the entry is invalid or equals the exit.
        """
        x, y = position
        if not self.is_inside(x, y):
            raise ValueError(
                "Entry is outside maze bounds"
            )
        if self.exit == position:
            raise ValueError(
                "Entry and exit must be different"
            )
        self.entry = position

    def set_exit(
        self,
        position: tuple[int, int],
    ) -> None:
        """Set the maze exit position.

        Args:
            position: Exit coordinates as an (x, y) tuple.

        Raises:
            ValueError: If the exit is invalid or equals the entry.
        """
        x, y = position
        if not self.is_inside(x, y):
            raise ValueError(
                "Exit is outside maze bounds"
            )
        if self.entry == position:
            raise ValueError(
                "Entry and exit must be different"
            )
        self.exit = position
