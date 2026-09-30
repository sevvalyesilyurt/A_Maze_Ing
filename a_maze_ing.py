import sys

from mazegen.config import ConfigParser
from mazegen.generator import MazeGenerator
from mazegen.interaction import MazeInteraction
from mazegen.output import write_output
from mazegen.solver import MazeSolver


def main() -> None:
    """Generate, solve, save, and display a maze."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        return

    config_file = sys.argv[1]
    parser = ConfigParser()

    try:
        config = parser.parse(config_file)
        generator = MazeGenerator(
            config.width,
            config.height,
            config.seed,
        )
        maze = generator.generate(
            entry=config.entry,
            exit=config.exit,
            perfect=config.perfect,
        )

        solver = MazeSolver(maze)
        path = solver.solve()
        write_output(
            config.output_file,
            maze,
            path,
        )

        interaction = MazeInteraction(
            maze=maze,
            path=path,
            generator=generator,
            entry=config.entry,
            exit=config.exit,
            perfect=config.perfect,
            output_file=config.output_file,
        )
        interaction.run()

    except (ValueError, OSError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
