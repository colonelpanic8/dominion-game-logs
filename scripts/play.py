#!/usr/bin/env python3
"""Run an AI agent through a game of Dominion and keep everything needed to read or repeat it.

Each game gets its own directory under runs/<date>/<time>-<model>-<effort>/ holding:
  run.json         versions of everything involved, the settings, and the outcome
  prompt.md        the exact prompt the agent got
  <game>.md/.jsonl the decision log written by the dominion-navigator MCP server
  transcript.jsonl the agent's full Claude Code stream-json transcript
  report.md        the agent's closing report
  *.diff           uncommitted changes in a repository it ran from, if any
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "runs"
README = ROOT / "README.md"
INDEX_START = "<!-- runs:start -->"
INDEX_END = "<!-- runs:end -->"
MAX_UNTRACKED_BYTES = 200_000

ALLOWED_TOOLS = [
    "mcp__dominion__state",
    "mcp__dominion__step",
    "mcp__dominion__wait",
    "mcp__dominion__new_game",
    "mcp__dominion__log",
    "mcp__dominion__cards",
    "Read",
    "Glob",
    "Grep",
    "Skill",
]
DISALLOWED_TOOLS = ["mcp__dominion__inspect", "mcp__dominion__resign", "Bash", "Write", "Edit"]


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout


def repo_state(repo: Path, out_dir: Path, name: str) -> dict:
    """Commit, branch and dirty state of a repository; its uncommitted changes go to <name>.diff."""
    state: dict = {
        "path": str(repo),
        "commit": git(repo, "rev-parse", "HEAD").strip(),
        "branch": git(repo, "rev-parse", "--abbrev-ref", "HEAD").strip(),
    }
    remote = subprocess.run(["git", "-C", str(repo), "remote", "get-url", "origin"], check=False, capture_output=True, text=True)
    if remote.returncode == 0:
        state["remote"] = remote.stdout.strip()
    changed = [line for line in git(repo, "status", "--porcelain").splitlines() if line]
    state["dirty"] = bool(changed)
    if changed:
        state["changed"] = changed
        diff = git(repo, "diff", "HEAD")
        for line in changed:
            if not line.startswith("??"):
                continue
            path = repo / line[3:]
            files = [path] if path.is_file() else sorted(p for p in path.rglob("*") if p.is_file())
            for file in files:
                if file.stat().st_size > MAX_UNTRACKED_BYTES:
                    continue
                untracked = subprocess.run(
                    ["git", "-C", str(repo), "diff", "--no-index", "--", "/dev/null", str(file.relative_to(repo))],
                    check=False,
                    capture_output=True,
                    text=True,
                )
                diff += untracked.stdout
        (out_dir / f"{name}.diff").write_text(diff)
        state["diff"] = f"{name}.diff"
    return state


def command_version(*command: str) -> str | None:
    try:
        return subprocess.run(command, check=True, capture_output=True, text=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def start_instruction(args: argparse.Namespace) -> str:
    if args.opponent == "human":
        return (
            "Call `find_match` to be matched with a human opponent for an unrated game, and wait until the game starts. "
            "Its result lists the kingdom and the card text."
        )
    kingdom = f" and kingdom {json.dumps(args.kingdom)}" if args.kingdom else " and a random kingdom"
    return f"Call `new_game` with {args.bots} bot(s){kingdom}. Its result lists the kingdom and the card text."


def final_result(transcript: Path) -> dict:
    """The stream-json `result` message: cost, duration, turns and the agent's closing report."""
    result: dict = {}
    for line in transcript.read_text().splitlines():
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            continue
        if message.get("type") == "result":
            result = message
    return result


def game_summary(run_dir: Path) -> list[dict]:
    """Game numbers and results from the navigator's game logs in a run directory."""
    games = []
    for log in sorted(run_dir.glob("*.jsonl")):
        if log.name == "transcript.jsonl":
            continue
        records = [json.loads(line) for line in log.read_text().splitlines() if line.strip()]
        result = next((record["result"] for record in reversed(records) if record.get("type") == "result"), None)
        decisions = sum(1 for record in records if record.get("type") == "decision")
        games.append({"game": log.stem, "decisions": decisions, "result": result})
    return games


def play(args: argparse.Namespace) -> Path:
    now = dt.datetime.now(dt.UTC)
    run_dir = RUNS / now.strftime("%Y-%m-%d") / f"{now.strftime('%H%M%S')}-{args.model}-{args.effort}"
    run_dir.mkdir(parents=True)
    run_id = f"{now.strftime('%Y-%m-%d')}/{run_dir.name}"

    prompt = Path(args.prompt).read_text().replace("{start}", start_instruction(args))
    (run_dir / "prompt.md").write_text(prompt)
    agents = repo_state(args.agents, run_dir, "dominion-agents")
    navigator = repo_state(args.navigator, run_dir, "dominion-navigator")
    meta = {
        "run": run_id,
        "harness": {"name": "claude-code", "version": command_version(args.claude, "--version")},
        "model": args.model,
        "effort": args.effort,
        "opponent": args.opponent,
        "agents": {"commit": agents["commit"], "dirty": agents["dirty"]},
        "prompt": hashlib.sha256(prompt.encode()).hexdigest()[:16],
    }
    run = {
        "run": run_id,
        "started": now.isoformat(),
        "settings": {
            "model": args.model,
            "effort": args.effort,
            "opponent": args.opponent,
            "bots": args.bots,
            "kingdom": args.kingdom,
            "max_turns": args.max_turns,
            "allowed_tools": ALLOWED_TOOLS,
        },
        "versions": {
            "harness": meta["harness"],
            "node": command_version("node", "--version"),
            "dominion-agents": agents,
            "dominion-navigator": navigator,
        },
        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
    }
    (run_dir / "run.json").write_text(json.dumps(run, indent=2) + "\n")

    server_flags = [f"--game-log-dir {run_dir}"]
    if args.opponent == "human":
        server_flags.append("--allow-human-opponents")
    mcp_config = {
        "mcpServers": {
            "dominion": {
                "command": "bash",
                "args": ["-c", f"cd {args.navigator} && exec node --import tsx scripts/mcp-server.ts {' '.join(server_flags)}"],
                "env": {"DOMINION_GAME_LOG_META": json.dumps(meta)},
            }
        }
    }
    (run_dir / "mcp-config.json").write_text(json.dumps(mcp_config, indent=2) + "\n")

    allowed = [*ALLOWED_TOOLS, *(["mcp__dominion__find_match"] if args.opponent == "human" else [])]
    command = [
        args.claude,
        "-p",
        prompt,
        "--model",
        args.model,
        "--effort",
        args.effort,
        "--mcp-config",
        str(run_dir / "mcp-config.json"),
        "--strict-mcp-config",
        "--allowedTools",
        ",".join(allowed),
        "--disallowedTools",
        ",".join(DISALLOWED_TOOLS),
        "--max-turns",
        str(args.max_turns),
        "--output-format",
        "stream-json",
        "--verbose",
    ]
    print(f"{run_id}: playing", flush=True)
    with (run_dir / "transcript.jsonl").open("w") as transcript, (run_dir / "claude.err").open("w") as stderr:
        exit_code = subprocess.run(command, check=False, cwd=args.agents, stdout=transcript, stderr=stderr, timeout=args.timeout).returncode

    result = final_result(run_dir / "transcript.jsonl")
    if result.get("result"):
        (run_dir / "report.md").write_text(result["result"].strip() + "\n")
    if not (run_dir / "claude.err").read_text().strip():
        (run_dir / "claude.err").unlink()
    run.update(
        {
            "finished": dt.datetime.now(dt.UTC).isoformat(),
            "exit_code": exit_code,
            "outcome": {
                "cost_usd": result.get("total_cost_usd"),
                "duration_s": round((result.get("duration_ms") or 0) / 1000),
                "agent_turns": result.get("num_turns"),
                "usage": {key: value for key, value in (result.get("usage") or {}).items() if isinstance(value, int)},
                "games": game_summary(run_dir),
            },
        }
    )
    (run_dir / "run.json").write_text(json.dumps(run, indent=2) + "\n")
    return run_dir


def result_cell(game: dict) -> str:
    result = game.get("result")
    if not result:
        return f"{game['game']}: unfinished"
    return f"{game['game']}: " + ", ".join(f"{p['name']} {p['points']}" for p in result["players"])


def short_commit(versions: dict, name: str) -> str:
    repo = versions.get(name) or {}
    return repo.get("commit", "?")[:7] + ("*" if repo.get("dirty") else "")


def write_index() -> None:
    rows = []
    for run_json in sorted(RUNS.glob("*/*/run.json"), reverse=True):
        run = json.loads(run_json.read_text())
        settings = run.get("settings", {})
        versions = run.get("versions", {})
        outcome = run.get("outcome", {})
        games = "; ".join(result_cell(game) for game in outcome.get("games", [])) or run.get("note", "")
        cost = outcome.get("cost_usd")
        rows.append(
            f"| [{run['run']}](runs/{run['run']}) | {settings.get('model', '?')} {settings.get('effort', '')} "
            f"| {settings.get('opponent', 'bot')} | {games} | {short_commit(versions, 'dominion-agents')} | {short_commit(versions, 'dominion-navigator')} "
            f"| {'' if cost is None else f'${cost:.2f}'} |"
        )
    table = "\n".join(
        [
            "| Run | Model | Opponent | Games (final VP) | dominion-agents | dominion-navigator | Cost |",
            "| --- | --- | --- | --- | --- | --- | --- |",
            *rows,
        ]
    )
    text = README.read_text()
    start, end = text.index(INDEX_START) + len(INDEX_START), text.index(INDEX_END)
    README.write_text(f"{text[:start]}\n{table}\n{text[end:]}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--model", default="opus")
    parser.add_argument("--effort", default="high", choices=["low", "medium", "high", "xhigh", "max"])
    parser.add_argument("--opponent", default="bot", choices=["bot", "human"])
    parser.add_argument("--bots", type=int, default=1)
    parser.add_argument("--kingdom", nargs="*", default=[], help="card and landscape names the kingdom must use")
    parser.add_argument("--count", type=int, default=1, help="games to play, one after another")
    parser.add_argument("--prompt", default=str(ROOT / "prompts" / "play.md"))
    parser.add_argument("--agents", type=Path, default=Path(os.environ.get("DOMINION_AGENTS", "~/projects/dominion-agents")).expanduser())
    parser.add_argument(
        "--navigator", type=Path, default=Path(os.environ.get("DOMINION_NAVIGATOR", "~/projects/dominion-navigator")).expanduser()
    )
    parser.add_argument("--claude", default="claude")
    parser.add_argument("--max-turns", type=int, default=400)
    parser.add_argument("--timeout", type=int, default=3600, help="seconds before a game's agent is stopped")
    parser.add_argument("--index-only", action="store_true", help="only rebuild the run index in README.md")
    args = parser.parse_args()

    if not args.index_only:
        for _ in range(args.count):
            run_dir = play(args)
            write_index()
            print(
                f"{run_dir.relative_to(ROOT)}: "
                + "; ".join(result_cell(g) for g in json.loads((run_dir / "run.json").read_text())["outcome"]["games"])
            )
    write_index()
    return 0


if __name__ == "__main__":
    sys.exit(main())
