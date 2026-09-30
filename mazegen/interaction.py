from .generator import MazeGenerator
from .maze import Maze
from .output import write_output
from .renderer import MazeRenderer
from .solver import MazeSolver


class MazeInteraction:
    """Manage interactive terminal controls for the maze."""

    WALL_COLORS = [
        "default",
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
    ]

    def __init__(
        self,
        maze: Maze,
        path: str,
        generator: MazeGenerator,
        entry: tuple[int, int],
        exit: tuple[int, int],
        perfect: bool,
        output_file: str,
    ) -> None:
        """Initialize the maze interaction controller.

        Args:
            maze: Maze currently displayed.
            path: Shortest path of the maze.
            generator: Generator used to create new mazes.
            entry: Maze entry coordinates.
            exit: Maze exit coordinates.
            perfect: Whether the maze is perfect.
            output_file: File where maze data is written.
        """
        self.maze = maze
        self.path = path
        self.generator = generator
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.renderer = MazeRenderer()
        self.show_path = True
        self.color_index = 0
        self.output_file = output_file

    def _display(self) -> None:
        """Display the maze with or without the solution path."""
        if self.show_path:
            print(
                self.renderer.render(
                    self.maze,
                    self.path,
                )
            )
        else:
            print(
                self.renderer.render(self.maze)
            )

    def _toggle_path(self) -> None:
        """Toggle the visibility of the shortest path."""
        self.show_path = not self.show_path

    def _change_wall_color(self) -> None:
        """Change the wall color to the next available color."""
        self.color_index = (
            self.color_index + 1
        ) % len(self.WALL_COLORS)
        color = self.WALL_COLORS[self.color_index]
        self.renderer.set_wall_color(color)

    def _regenerate(self) -> None:
        """Generate a new maze and update its output file."""
        self.maze = self.generator.generate(
            entry=self.entry,
            exit=self.exit,
            perfect=self.perfect,
        )
        solver = MazeSolver(self.maze)
        self.path = solver.solve()

        write_output(
            self.output_file,
            self.maze,
            self.path,
        )

    def run(self) -> None:
        """Run the interactive terminal menu."""
        self._display()

        while True:
            print()
            print("[P] Show / Hide shortest path")
            print("[R] Regenerate maze")
            print("[C] Change wall colour")
            print("[Q] Quit")

            choice = input(
                "Choice: "
            ).strip().lower()

            if choice == "p":
                self._toggle_path()
                self._display()
            elif choice == "r":
                self._regenerate()
                self._display()
            elif choice == "c":
                self._change_wall_color()
                self._display()
            elif choice == "q":
                break
            else:
                print("Invalid choice")
