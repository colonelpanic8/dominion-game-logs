import argparse
import fcntl
import http.cookiejar
import json
import secrets
import subprocess
import time
import tomllib
import urllib.request
from pathlib import Path

from rated_series import now


def complete_records(path):
    snapshot = path.read_bytes()
    for line in snapshot.split(b"\n")[:-1]:
        if line:
            try:
                yield json.loads(line)
            except ValueError as error:
                raise RuntimeError("Malformed complete JSONL record") from error


class FixedSeries:
    def __init__(self, config):
        self.config = config
        self.directory = Path(config["state_dir"])
        self.directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.lock = (self.directory / "lock").open("w")
        fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        self.path = self.directory / "status.json"
        self.state = (
            json.loads(self.path.read_text())
            if self.path.exists()
            else {
                "created_at": now(),
                "phase": "ready",
                "completed": [],
                "active_game": None,
            }
        )
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

    def save(self, phase, **updates):
        self.state.update(
            phase=phase,
            updated_at=now(),
            agents=self.config["agents"],
            games=self.config["games"],
            series_format="fixed_games",
            **updates,
        )
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.state, indent=2) + "\n")
        tmp.replace(self.path)

    def note(self, text):
        print(f"{now()} {text}", flush=True)

    def request(self, path, body=None):
        headers = {"Origin": self.config["server"]}
        if body is not None:
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(
            self.config["server"] + path,
            headers=headers,
            data=json.dumps(body).encode() if body is not None else None,
        )
        with self.opener.open(req, timeout=90) as response:
            return json.load(response)

    def login(self):
        password = subprocess.check_output(["pass", "show", self.config["password_entry"]], text=True).splitlines()[0]
        self.request("/api/auth/login", {"name": self.config["owner"], "password": password})

    def score(self):
        score = dict.fromkeys(self.config["agents"], 0)
        excluded = set(self.config.get("exclude_from_score", []))
        for game in self.state["completed"]:
            if game["game_id"] not in excluded and game.get("eligible_for_score", True) and game["winner"] is not None:
                score[game["winner"]] += 1
        return score

    def model_check(self, game_id):
        required = self.config.get("required_models", {})
        if not required:
            return {"eligible": True, "finished": True, "sessions": []}
        archives = Path(self.config["archives_dir"])
        sessions = []
        problems = []
        found = set()
        finished = True
        for journal in sorted(archives.glob("*/interactions.jsonl")):
            with journal.open() as stream:
                try:
                    first = json.loads(next(stream))
                except (StopIteration, ValueError):
                    continue
            data = first.get("data", {})
            if data.get("job", {}).get("gameId") != game_id:
                continue
            agent = data.get("agent", {})
            name = agent.get("name")
            if name not in required:
                problems.append(f"Unexpected agent in game traces: {name}")
                continue
            found.add(name)
            models = set()
            last_kind = None
            for event in complete_records(journal):
                last_kind = event.get("kind")
                if last_kind == "seat_finished" and "Err" in event.get("data", {}).get("result", {}):
                    problems.append(f"{name}: seat/provider error")
                if event.get("kind") == "direct_request":
                    model = event.get("data", {}).get("model")
                    if model:
                        models.add(model)
            if agent.get("program") == "claude":
                for stdout in journal.parent.glob("response-*.stdout.jsonl"):
                    for event in complete_records(stdout):
                        model = event.get("message", {}).get("model")
                        if event.get("type") == "assistant" and model and model != "<synthetic>":
                            models.add(model)
                        if event.get("type") == "result" and event.get("is_error"):
                            problems.append(f"{name}: provider error")
            expected = required[name]
            if agent.get("model") != expected or any(m != expected for m in models):
                problems.append(f"{name}: unexpected model; observed {sorted(models)}")
            done = last_kind == "seat_finished"
            if done and not models:
                problems.append(f"{name}: finished without model evidence")
            finished = finished and done
            sessions.append({"archive": journal.parent.name, "agent": name, "models": sorted(models), "finished": done})
        finished = finished and found == set(required)
        report = {"eligible": not problems, "finished": finished, "sessions": sessions, "problems": problems}
        if problems:
            hold = self.directory / "deployment-hold.json"
            if not hold.exists():
                hold.write_text(
                    json.dumps(
                        {
                            "kind": "agent_failure",
                            "reason": "Model identity/provider validation failed; let the active game finish, then hold",
                            "game_id": game_id,
                            "problems": problems,
                            "created_at": now(),
                        },
                        indent=2,
                    )
                    + "\n"
                )
        return report

    def tick(self):
        active = self.state["active_game"]
        if active:
            observed = self.request(f"/api/games/{active}/watch?logFrom=0")
            view = observed["view"]
            if view["game"]["id"] != active:
                raise RuntimeError("Active game identity changed")
            players = {player["name"] for player in view["opponents"]}
            if view.get("you") is not None:
                players.add(view["you"]["name"])
            if players != set(self.config["agents"]):
                raise RuntimeError("Active game players changed")
            folder = self.directory / "games" / active
            folder.mkdir(parents=True, exist_ok=True)
            temporary = folder / ".watch.tmp"
            temporary.write_text(json.dumps(observed) + "\n")
            temporary.replace(folder / "latest-watch.json")
            model_check = self.model_check(active)
            if view["game"]["running"]:
                self.save("playing", current_turn=view.get("turn"), score=self.score(), model_verification=model_check)
                return False
            if not model_check["finished"]:
                self.save("finishing_agents", model_verification=model_check, score=self.score())
                return False
            result = view["game"].get("result")
            if not result or {p["name"] for p in result["players"]} != set(self.config["agents"]):
                raise RuntimeError("Missing or unexpected authoritative game result")
            winners = [p["name"] for p in result["players"] if p["rank"] == 1]
            if not winners:
                raise RuntimeError("Result has no winner")
            winner = winners[0] if len(winners) == 1 else None
            if any(g["game_id"] == active for g in self.state["completed"]):
                raise RuntimeError("Active game result was already recorded")
            self.state["completed"].append(
                {
                    "game_id": active,
                    "completed_at": now(),
                    "winner": winner,
                    "result": result,
                    "request": self.state["active_request"],
                    "eligible_for_score": model_check["eligible"],
                    "model_verification": model_check,
                }
            )
            temporary = folder / "final-watch.json"
            temporary.write_text(json.dumps(observed, indent=2) + "\n")
            self.save("between_games", active_game=None, score=self.score())
            self.note(f"Finished {active}; score={self.score()}, winner={winner}")
        score = self.score()
        eligible_games = sum(game.get("eligible_for_score", True) for game in self.state["completed"])
        if eligible_games >= self.config["games"]:
            leaders = [name for name, wins in score.items() if wins == max(score.values())]
            winner = leaders[0] if len(leaders) == 1 else None
            self.save("complete", winner=winner, score=score, finished_at=now())
            self.note(f"Fixed {self.config['games']}-game series complete: {winner}; {score}")
            return True
        if len(self.state["completed"]) >= self.config["max_total_games"]:
            raise RuntimeError("Series attempt safety limit reached")
        if self.state.get("creation_pending"):
            raise RuntimeError("Previous creation is uncertain; refusing a duplicate game")
        if self.state["phase"] == "creating":
            raise RuntimeError("Previous creation is uncertain; refusing a duplicate game")
        if (self.directory / "deployment-hold.json").exists():
            hold = json.loads((self.directory / "deployment-hold.json").read_text())
            phase = "awaiting_investigation" if hold.get("kind") == "agent_failure" else "awaiting_deployment"
            self.save(phase, score=score)
            return False
        house = self.request("/api/lobby")["house"]
        available = {a["user"]["name"] for a in house["agents"]}
        if not set(self.config["agents"]).issubset(available):
            raise RuntimeError("Selected agent profile is unavailable")
        if house["free"] < 2:
            self.save("waiting_for_capacity", score=score)
            return False
        agents = self.config["agents"][:]
        if len(self.state["completed"]) % 2:
            agents.reverse()
        body = {
            "players": 2,
            "names": agents,
            "agents": agents,
            "seed": secrets.randbits(64),
            "watchable": True,
        }
        self.save("creating", pending_request=body, creation_pending=True, score=score)
        created = self.request("/api/games", body)
        game_id = created["game_id"]
        if not isinstance(game_id, str) or not game_id.startswith("g"):
            raise RuntimeError("Unexpected created game identity")
        self.save("playing", active_game=game_id, active_request=body, creation_pending=False)
        self.note(f"Started {game_id}: {agents[0]} first, {agents[1]} second")
        return False

    def run(self):
        try:
            if self.state.get("creation_pending") or self.state["phase"] == "creating":
                raise RuntimeError("Previous creation is uncertain; inspect before continuing")
            self.login()
            while not self.tick():
                time.sleep(self.config["poll_seconds"])
        except Exception as error:
            self.save("needs_attention", error=str(error))
            self.note("Coordinator stopped; active agents were left to finish")
            raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=Path)
    args = parser.parse_args()
    with args.config.open("rb") as handle:
        FixedSeries(tomllib.load(handle)).run()
