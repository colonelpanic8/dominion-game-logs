default: check

# Play one or more games; see `just play --help`.
play *args:
    python3 scripts/play.py {{args}}

# Rebuild the run index in README.md from runs/*/*/run.json.
index:
    python3 scripts/play.py --index-only

fmt:
    alejandra -q .
    ruff format scripts

fmt-check:
    alejandra -q --check .
    ruff format --check scripts

lint:
    ruff check scripts

check: fmt-check lint
