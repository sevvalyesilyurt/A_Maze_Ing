from .maze import Maze


def write_output(
    filename: str,
    maze: Maze,
    path: str,
) -> None:
    """Write the generated maze and solution to an output file.

    Args:
        filename: Name of the output file.
        maze: Maze structure to write.
        path: Shortest path encoded with N, E, S, and W directions.

    Raises:
        ValueError: If the maze entry or exit is not set.
    """
    if maze.entry is None:
        raise ValueError("Maze entry must be set")
    if maze.exit is None:
        raise ValueError("Maze exit must be set")

    hex_grid = maze.to_hex_grid()
    entry_x, entry_y = maze.entry
    exit_x, exit_y = maze.exit

    with open(
        filename,
        "w",
        encoding="utf-8",
    ) as file:
        for row in hex_grid:
            file.write(row + "\n")

        file.write("\n")
        file.write(f"{entry_x},{entry_y}\n")
        file.write(f"{exit_x},{exit_y}\n")
        file.write(path + "\n")
