*This project has been created as part of the 42 curriculum by sevyesil, melipola.*

# A-Maze-ing

A-Maze-ing is a Python maze generator, solver, validator, terminal visualizer, and animation tool.

The project generates perfect and non-perfect mazes from a configuration file, finds the shortest path between the entry and exit, writes the maze to an output file using hexadecimal wall representation, and displays the result in the terminal. An optional animation shows both the maze generation process and the shortest solution path step by step.

The maze generation logic is also provided as a reusable Python package named `mazegen`.

## Description

The goal of A-Maze-ing is to generate valid random mazes according to a configuration file while providing maze solving, validation, terminal visualization, optional generation and solution animations, and reusable generation functionality.

The project supports two maze generation modes:

- **Perfect maze:** every accessible cell is connected without loops, producing a tree-like maze structure.
- **Non-perfect maze:** the maze contains multiple loops and alternative corridors while remaining fully connected.

The generated maze also contains a visible `42` pattern made of fully closed cells when the maze is large enough to place it safely.

The generation process checks key maze properties, including connectivity and forbidden fully open `3×3` areas. Other structural requirements, such as consistent walls, closed external borders, and the perfect/non-perfect maze behavior, are enforced by the maze representation and generation logic.

A shortest path from the entry to the exit is calculated and represented using the following directions:

- `N` — North
- `E` — East
- `S` — South
- `W` — West

## Project Structure

```text
A_Maze_Ing/
├── a_maze_ing.py
├── config.txt
├── maze.txt
├── Makefile
├── pyproject.toml
├── README.md
├── LICENSE.md
├── mazegen-0.1.0-py3-none-any.whl
└── mazegen/
    ├── __init__.py
    ├── animation.py
    ├── cell.py
    ├── config.py
    ├── generator.py
    ├── interaction.py
    ├── maze.py
    ├── output.py
    ├── pattern.py
    ├── renderer.py
    ├── solver.py
    └── validator.py
```

### Main Components

- `a_maze_ing.py` connects configuration parsing, generation, solving, output writing, and terminal interaction.
- `cell.py` defines an individual maze cell, its walls, and its state.
- `maze.py` stores the two-dimensional maze structure and provides cell, neighbor, movement, wall, and hexadecimal-grid operations.
- `config.py` reads and validates the configuration file.
- `generator.py` contains the randomized DFS generation logic and the perfect/non-perfect generation behavior.
- `pattern.py` handles placement of the blocked `42` pattern.
- `validator.py` contains checks for visited cells, connectivity, open areas, and dead-end counts.
- `solver.py` finds the shortest path between entry and exit.
- `output.py` writes the hexadecimal maze and solution information to the configured output file.
- `renderer.py` creates the terminal representation of the maze, including walls, the `42` pattern, entry/exit markers, and the solution path.
- `animation.py` contains `MazeAnimator`, which redraws maze-generation frames and progressively reveals the shortest path.
- `interaction.py` manages interactive terminal commands, including the combined animation option `[A]`.
- `__init__.py` defines the public interface of the reusable `mazegen` package.

## Configuration

The program receives exactly one configuration file as a command-line argument.

The configuration file contains one `KEY=VALUE` pair per line. Lines beginning with `#` are treated as comments and are ignored.

Example:

```text
WIDTH=20
HEIGHT=20
ENTRY=0,0
EXIT=19,19
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

### Configuration Fields

`WIDTH` defines the number of cells in each maze row.

`HEIGHT` defines the number of cells in each maze column.

`ENTRY` defines the entry coordinates in `x,y` format.

`EXIT` defines the exit coordinates in `x,y` format.

`OUTPUT_FILE` defines the file where the generated maze and shortest path are written.

`PERFECT` controls the maze generation mode. `True` generates a perfect maze, while `False` generates a non-perfect maze.

`SEED` is an additional optional field used to make random maze generation reproducible.

The entry and exit must be different coordinates and must remain inside the maze boundaries.

## Instructions

The project requires Python 3.10 or newer.

### Install

Install the project with:

```bash
make install
```

Or directly with:

```bash
python3 -m pip install .
```

### Run

Run the project with:

```bash
make run
```

Or:

```bash
python3 a_maze_ing.py config.txt
```

A different configuration file can be used with:

```bash
make run CONFIG=other_config.txt
```

### Debug

Run the project with the Python debugger:

```bash
make debug
```

### Lint and Type Checking

Run the project quality checks with:

```bash
make lint
```

The lint command runs:

```bash
flake8 .
mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
```

### Build the Reusable Package

Build the installable wheel file in the repository root with:

```bash
make build
```

Or, after installing the `build` tool, run:

```bash
python3 -m pip install build
python3 -m build --wheel --outdir .
```

The package is named `mazegen-0.1.0-py3-none-any.whl`. Rebuild it after modifying package source files (including animation code) so the distributed wheel matches the latest implementation.

### Clean

Remove Python caches and generated build metadata with:

```bash
make clean
```

The `clean` task also removes generated `build/`, `dist/`, and `*.egg-info/` directories when present. It keeps the distributable `.whl` file stored in the repository root.

## Maze Generation Algorithm

The main maze generation algorithm used in this project is randomized depth-first search (DFS) with backtracking.

The generator starts from a cell and explores randomly selected unvisited neighboring cells. When moving to a valid neighbor, the wall between the two cells is removed. If the current cell has no available unvisited neighbor, the algorithm backtracks until another possible route can be explored.

### Why We Chose DFS

Randomized DFS was chosen because it provides a relatively simple and efficient way to generate connected mazes.

For a perfect maze, the DFS generation process naturally produces a spanning-tree structure. This allows accessible cells to remain connected without introducing loops.

It also works well with a random seed, which makes it possible to generate random mazes while still reproducing a previous generation when the same seed and parameters are used.

For non-perfect mazes, the DFS-generated maze is used as the initial structure. Additional valid walls are then removed to introduce loops and alternative routes.

Further processing opens the required corner and centre corridor areas and reduces dead ends while preventing invalid `3×3` open areas.

## 42 Pattern

When enough space is available, the generator places a visible `42` pattern inside the maze.

Cells belonging to the pattern are blocked and remain fully closed on all four sides.

The placement logic protects important cells such as the entry and exit. For non-perfect mazes, reserved corner and centre cells are also protected.

If the maze is too small or no valid position exists for the pattern, the program reports that the pattern cannot be placed and continues without it.

## Maze Validation

The project includes a `MazeValidator` class to check important structural properties during generation. Its current checks cover:

- Whether all accessible cells were visited.
- Whether the accessible maze is fully connected.
- Whether an area is completely open, including forbidden fully open `3×3` regions.
- How many non-blocked cells are dead ends.

Other maze requirements, such as consistent neighboring walls, closed outer borders, and the creation of multiple routes in non-perfect mode, are handled by the maze data structures and generation process. The validator is separate from the generation logic so these checks can be reused without changing the maze.

## Maze Solver

`MazeSolver` finds the shortest valid path from the entry to the exit using breadth-first search (BFS).

BFS explores reachable cells level by level. Because every movement between neighboring maze cells has the same cost, the first route found to the exit is a shortest path.

The resulting path is encoded using `N`, `E`, `S`, and `W` characters and is written to the output file.

The terminal renderer can also display the solution directly inside the maze.

## Output Format

Each maze cell is represented by one hexadecimal digit.

The four least significant bits represent the walls in this order:

```text
Bit 0: North
Bit 1: East
Bit 2: South
Bit 3: West
```

A bit value of `1` means that the wall is closed, while `0` means that it is open.

Cells are written row by row, with one maze row per line.

After the hexadecimal maze, the output contains an empty line followed by:

1. The entry coordinates;
2. The exit coordinates;
3. The shortest valid path encoded with `N`, `E`, `S`, and `W`.

All output lines end with a newline character.

Example structure:

```text
FFFFFFFF
...
FFFFFFFF

0,0
7,7
EESS...
```

## Terminal Visualization

The maze is displayed directly in the terminal.

The visualization distinguishes:

- Maze walls;
- The entry with `E`;
- The exit with `X`;
- Blocked `42` cells;
- The shortest path with `●`.

When the entry or exit is located on the outer border, the renderer displays a visual opening in that border to make the maze entrance and exit clearer. This affects only the terminal visualization; the maze data keeps its external border walls closed.

The interactive interface provides the following commands:

```text
[P] Show / Hide shortest path
[A] Animate generation and shortest path
[R] Regenerate maze
[C] Change wall colour
[Q] Quit
```

The `[R]` command regenerates the maze without animation, recalculates its shortest path, and updates the configured output file. The `[P]` command toggles the already calculated shortest path, and `[C]` changes wall colours.

### Maze Generation and Shortest-Path Animation

The optional `[A]` command performs two animations in sequence:

1. **Maze generation animation:** A new maze is generated while intermediate steps are displayed in the terminal. The generator sends update notifications through an optional `on_step` callback, and `MazeAnimator` uses `MazeRenderer` to redraw the current maze as corridors are carved and later generation steps make changes.
2. **Shortest-path animation:** After maze generation finishes, `MazeSolver` computes the shortest route using BFS. `MazeAnimator.animate_solution()` then shows that completed route gradually, from entry (`E`) to exit (`X`), adding the `●` markers one step at a time.

Only one menu option, `[A]`, is needed for both animations. The solution animation displays the **final BFS path**; it does not animate BFS's internal search through all visited cells.

Animation is a visualization feature. It does not alter the wall representation or maze-solving algorithm. The newly generated maze and its shortest path are also saved to the configured output file. The animations redraw the terminal using ANSI control sequences, so a terminal with ANSI support is recommended.

The generation animation is controlled by `MazeAnimator`'s `delay` and `every` parameters; the solution animation accepts its own `delay` value. These settings can be adjusted in the Python code to change playback speed.

## Reusable Maze Generator

The maze generation functionality is separated from the command-line program and is available through the `mazegen` package.

The package exposes its main reusable classes through `mazegen/__init__.py`, allowing them to be imported directly from the package.

A basic example:

```python
from mazegen import MazeGenerator, MazeSolver
generator = MazeGenerator(
    width=20,
    height=20,
    seed=42,
)
maze = generator.generate(
    entry=(0, 0),
    exit=(19, 19),
    perfect=True,
)
solver = MazeSolver(maze)
path = solver.solve()
grid = maze.to_hex_grid()
```

Custom parameters such as maze dimensions and a random seed can be passed when creating the generator.

The generated `Maze` object provides access to the maze structure, including its cells, entry, exit, neighbors, walls, and hexadecimal representation.

The reusable module is packaged as a pip-installable `mazegen-*` artifact at the root of the repository.

## Team and Project Management

The project was developed collaboratively by:

- `sevyesil`
- `melipola`

### Team Roles

The project was developed collaboratively by `sevyesil` and `melipola`. Responsibilities were divided according to each team member's experience, while both members participated in integration, debugging, reviewing generated mazes, and preparing the final project.

#### sevyesil

`sevyesil` focused mainly on the core Python architecture and maze generation logic. Her responsibilities included:

- Designing the main project architecture and separation of components;
- Implementing the maze and cell data structures;
- Implementing the randomized DFS maze generation algorithm;
- Implementing perfect and non-perfect maze generation behavior;
- Implementing loop generation and dead-end reduction logic;
- Developing maze validation for connectivity, visited cells, dead ends, and open areas;
- Implementing shortest-path solving;
- Integrating the main generation components and resolving Python typing and structural issues.

#### melipola

`melipola` focused mainly on configuration, visualization, user interaction, and project documentation. Her responsibilities included:

- Implementing and checking configuration file handling;
- Contributing to the `42` pattern placement and its integration with maze generation;
- Developing the terminal maze visualization;
- Implementing entry, exit, blocked-cell, and shortest-path display;
- Implementing interactive controls for showing or hiding the path, regenerating the maze, and changing wall colours;
- Contributing to output-file generation and format verification;
- Contributing to README documentation and final project verification.

Both team members worked together during integration to verify that the perfect and non-perfect maze modes satisfied the project requirements. The interactive generation and shortest-path animations were also integrated into the existing visualization workflow. They also collaborated on debugging, trying different configurations, reviewing generated mazes, and preparing the project for evaluation.

### Planning and Evolution

The project was initially planned around the essential generation flow: reading a configuration file, representing maze cells, generating a valid maze, solving it, and producing the required output.

As development progressed, the architecture evolved into smaller components with clearer responsibilities. Validation, `42` pattern placement, output generation, rendering, animation, and terminal interaction were separated from the core generation logic.

The project was developed incrementally. Components were implemented and integrated step by step, while linting, static type checking, different configurations, and generated maze behavior were reviewed throughout development.

### What Worked Well

Separating the project into focused components made the code easier to understand, debug, maintain, and reuse.

Using deterministic seeds was useful during development because the same maze could be reproduced when investigating generation behavior.

Separating validation from generation also made it easier to check connectivity, dead ends, and invalid open areas without adding those checks directly to the generation algorithm.

### What Could Be Improved

A wider range of maze dimensions, configurations, and random seeds could be checked during development to cover more edge cases.

The development process could also be improved by defining some component boundaries and integration steps earlier, reducing the amount of refactoring needed as the project grew.

The terminal visualization and animations could be extended with playback controls or additional display options while keeping maze-generation logic independent from the interface.

### Tools Used

The project was developed and verified using tools including:

- Python 3;
- Git;
- flake8;
- mypy;
- Python virtual environments;
- A terminal and code editor.

## Resources

The following resources were used during the research and development of the project:

- **A-Maze-ing Subject** — Used as the main reference for project requirements, maze rules, configuration format, hexadecimal wall representation, visualization, and reusable-module requirements.
- **BTK Akademi — Yapay Zekâ ve Algoritmalarına Giriş** — Used to review Breadth-First Search (BFS), Depth-First Search (DFS), and general search algorithm concepts.
  https://www.btkakademi.gov.tr/portal/tr/course/17500
- **BTK Akademi — Algoritma Programlama ve Veri Yapılarına Giriş** — Consulted for fundamental algorithms, stacks, queues, graphs, and data structures.
  https://www.btkakademi.gov.tr/portal/tr/course/12565
- **Bilgisayar Kavramları — Şadi Evren Şeker, Breadth-First Search (BFS)** — Consulted to better understand the level-by-level graph traversal used by the shortest-path solver.
  https://bilgisayarkavramlari.com/2008/11/13/sig-oncelikli-arama-breadth-first-search/
- **Dokuz Eylül University — Research on Search Algorithms in Two-Dimensional Mazes** — Consulted as an academic reference for using DFS and BFS in maze problems.
- **Al Sweigart — The Recursive Book of Recursion: Maze Generator** — Consulted for concepts such as randomized movement, visited cells, corridor carving, and backtracking.
  https://inventwithpython.com/recursion/chapter11.html
- **Python Documentation** — Used for Python language features and standard-library components such as `random` and `collections.deque`.
  https://docs.python.org/3/
- **Python Packaging User Guide** — Used while preparing `pyproject.toml`, the reusable `mazegen` package, and the wheel distribution.
  https://packaging.python.org/
- **mypy Documentation** — Used for static type checking and type-annotation issues.
  https://mypy.readthedocs.io/
- **Flake8 Documentation** — Used for Python style and linting checks.
  https://flake8.pycqa.org/

### AI Usage

AI tools were used as supplementary resources during project development. They supported research and learning, explanations of DFS/BFS and maze-generation concepts, debugging, and suggestions or reviews of code snippets and implementation approaches. This assistance also included integrating the optional generation and shortest-path animations with the existing generator, renderer, and interaction components.

AI-assisted code and suggestions were reviewed, adapted to the project's structure, and tested by the team members before integration. The final implementation and its behavior were understood by the team members.

## License

This project is distributed under the terms described in `LICENSE.md`.