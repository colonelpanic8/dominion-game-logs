import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "/home/imalison/.local/share/dominion/automation")
from fixed_series import FixedSeries

A, B = "Sol High", "Fable High"


class Harness(FixedSeries):
    def __init__(self, path):
        super().__init__({"state_dir": path, "agents": [A, B], "games": 7, "max_total_games": 21})
        self.calls = []
        self.free = 3
        self.running = False
        self.winners = [A]
        self.report = {"eligible": True, "finished": True, "sessions": []}

    def note(self, _):
        pass

    def model_check(self, _):
        return self.report

    def request(self, path, body=None):
        self.calls.append((path, body))
        if path == "/api/lobby":
            return {"house": {"agents": [{"user": {"name": x}} for x in (A, B)], "free": self.free}}
        if path == "/api/games":
            return {"game_id": "gNEW", "seats": [{"token": "DO-NOT-PERSIST"}]}
        return {
            "view": {
                "game": {
                    "id": "gACTIVE",
                    "running": self.running,
                    "result": {"players": [{"name": x, "rank": 1 if x in self.winners else 2, "vp": 20} for x in (A, B)]},
                },
                "you": None,
                "opponents": [{"name": x} for x in (A, B)],
            }
        }

    def completed(self, winners):
        self.state["completed"] = [{"game_id": f"g{i}", "winner": x, "eligible_for_score": True} for i, x in enumerate(winners)]

    def active(self):
        self.state.update(active_game="gACTIVE", active_request={}, creation_pending=False)


with tempfile.TemporaryDirectory() as d:
    h = Harness(d)
    h.completed([A] * 4)
    assert not h.tick() and h.calls[-1][1]["agents"] == [A, B]
    assert "DO-NOT-PERSIST" not in h.path.read_text()
with tempfile.TemporaryDirectory() as d:
    h = Harness(d)
    h.completed([A] * 6)
    h.active()
    assert h.tick() and h.state["phase"] == "complete" and h.state["winner"] == A
    assert len(h.state["completed"]) == 7 and not any(p == "/api/games" for p, _ in h.calls)
with tempfile.TemporaryDirectory() as d:
    h = Harness(d)
    h.completed([A, A, A, B, B, B])
    h.active()
    h.winners = [A, B]
    assert h.tick() and h.state["winner"] is None and h.state["completed"][-1]["winner"] is None
with tempfile.TemporaryDirectory() as d:
    h = Harness(d)
    h.completed([A, A, A, A, B, B])
    h.state["completed"][0]["eligible_for_score"] = False
    assert not h.tick()
with tempfile.TemporaryDirectory() as d:
    h = Harness(d)
    h.active()
    h.report["finished"] = False
    assert not h.tick() and h.state["phase"] == "finishing_agents" and not h.state["completed"]
with tempfile.TemporaryDirectory() as d:
    h = Harness(d)
    h.state["creation_pending"] = True
    try:
        h.tick()
    except RuntimeError:
        pass
    else:
        raise AssertionError("Duplicate creation allowed")
    assert not h.calls
with tempfile.TemporaryDirectory() as d:
    h = Harness(d)
    h.completed([B])
    assert not h.tick() and h.calls[-1][1]["agents"] == [B, A]
with tempfile.TemporaryDirectory() as d:
    h = Harness(d)
    (Path(d) / "deployment-hold.json").write_text(json.dumps({"kind": "agent_failure"}))
    assert not h.tick() and h.state["phase"] == "awaiting_investigation"
    assert not any(p == "/api/games" for p, _ in h.calls)
with tempfile.TemporaryDirectory() as d:
    h = Harness(d)
    h.free = 1
    assert not h.tick() and h.state["phase"] == "waiting_for_capacity"
print("9 fixed-series completion, tie, eligibility, trace-finish, seat, hold, capacity and duplicate-start checks passed")
