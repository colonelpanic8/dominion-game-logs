# dominion-game-logs

Logs of AI agents playing Dominion, and `scripts/play.py`, the runner that writes them. The README explains the layout of a run directory.

## Invariants

- A run directory is a record. Never edit a finished run's files; add a new run instead. `README.md`'s run table is generated (`just index`) between the `runs:` markers.
- Record every version that could change a result. The runner stores both repositories' commits and their uncommitted changes, the harness version, the model and effort, and the prompt. Add to `run.json` rather than dropping anything.
- Runs under `runs/2026-11-11/legacy-*` predate the runner. Their versions are approximate or unknown, as their `run.json` says.
- The runner only plays bot games unless asked for `--opponent human`, which needs the navigator's human-opponent support.

## Checks

`just check` (formatting and lint) inside the dev shell: `direnv allow`, or `nix develop -c just check`.
