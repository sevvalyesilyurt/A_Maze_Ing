
PYTHON ?= python3
CONFIG ?= config.txt

.PHONY: install run debug build clean lint

install:
	$(PYTHON) -m pip install .

run:
	$(PYTHON) a_maze_ing.py $(CONFIG)

debug:
	$(PYTHON) -m pdb a_maze_ing.py $(CONFIG)

build:
	$(PYTHON) -m build --wheel --outdir .

clean:
	$(PYTHON) -c "from pathlib import Path; import shutil; roots = [Path('mazegen'), Path('tests')]; folders = [Path('__pycache__'), Path('.mypy_cache'), Path('build'), Path('dist'), *Path('.').glob('*.egg-info')]; folders += [p for root in roots for p in root.rglob('__pycache__')]; [shutil.rmtree(p, ignore_errors=True) for p in folders if p.is_dir()]"
	$(PYTHON) -c "from pathlib import Path; roots = [Path('mazegen'), Path('tests')]; files = list(Path('.').glob('*.pyc')) + [p for root in roots for p in root.rglob('*.pyc')]; [p.unlink() for p in files if p.is_file()]"

lint:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
