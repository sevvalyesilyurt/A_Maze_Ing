class Cell:
    """Represent a single cell in the maze."""

    def __init__(
        self,
        x: int,
        y: int,
    ) -> None:
        """Initialize a cell with all four walls closed.

        Args:
            x: Horizontal coordinate of the cell.
            y: Vertical coordinate of the cell.
        """
        self.x = x
        self.y = y

        self.north = True
        self.east = True
        self.south = True
        self.west = True

        self.visited = False
        self.blocked = False

    def to_hex(self) -> str:
        """Convert the cell walls to a hexadecimal digit.

        Returns:
            A hexadecimal digit representing the closed walls.
        """
        mask = 0

        if self.north:
            mask |= 1

        if self.east:
            mask |= 2

        if self.south:
            mask |= 4

        if self.west:
            mask |= 8

        return format(mask, "X")
