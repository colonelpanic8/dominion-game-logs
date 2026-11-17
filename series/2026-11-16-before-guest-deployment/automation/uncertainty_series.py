import argparse
import json
import math
import subprocess
import tomllib
from pathlib import Path

from rated_series import Series, now


class TargetReached(Exception):
    pass


class DeploymentHold(Exception):
    pass


class RatingPending(Exception):
    pass


class UncertaintySeries(Series):
    def save(self, phase, **updates):
        super().save(
            phase,
            **updates,
            target_phi=self.config["target_phi"],
            initial_games=self.config["initial_games"],
            goal="official Standard 2P deviation at or below target_phi",
        )

    def rating(self):
        accounts = self.http(self.config["server"] + "/api/online/accounts")
        observer = next(
            (a for a in accounts if a["account"] == self.config["observer_account"]),
            None,
        )
        if self.config["observer_account"] == self.config["account_name"]:
            raise RuntimeError("The rating observer must be a separate account")
        if observer is not None and (observer["connected"] or observer["running"]):
            raise RuntimeError(
                "Rating observer account is unavailable; no login attempted"
            )
        process = subprocess.run(
            self.config["rating_command"],
            check=False,
            capture_output=True,
            text=True,
            timeout=45,
        )
        if process.returncode:
            raise RuntimeError("Read-only rating probe failed; no new game started")
        rating = json.loads(process.stdout)
        if (
            rating.get("account") != self.config["account_name"]
            or rating.get("rating_type") != 0
        ):
            raise RuntimeError("Rating target or Standard 2P rating type changed")
        if not isinstance(rating.get("games"), int):
            raise TypeError("Official profile did not provide a game count")
        for key in ("level", "mu", "phi"):
            if not isinstance(rating.get(key), (float, int)) or not math.isfinite(
                rating[key]
            ):
                raise RuntimeError("Official profile supplied invalid rating data")
        if rating["phi"] <= 0:
            raise RuntimeError("Official profile supplied invalid uncertainty")
        rating["verified_at"] = now()
        if rating["games"] != len(self.state["completed"]):
            if rating["games"] > len(self.state["completed"]):
                raise RuntimeError(
                    "Official game count exceeds tracked results; inspection required"
                )
            attempts = self.state.get("pending_rating_attempts", 0) + 1
            self.save(
                "checking_rating",
                awaiting_game=False,
                pending_rating=rating,
                pending_rating_attempts=attempts,
            )
            if attempts >= self.config.get("rating_max_attempts", 12):
                raise RuntimeError(
                    "Official rating remained stale; stopped before a new search"
                )
            raise RatingPending()
        history = self.state.setdefault("rating_history", [])
        if (
            not history
            or history[-1]["games"] != rating["games"]
            or history[-1]["phi"] != rating["phi"]
        ):
            history.append(rating)
        self.save(
            "checking_rating",
            awaiting_game=False,
            latest_rating=rating,
            pending_rating_attempts=0,
        )
        self.note(
            f"Verified official rating after {rating['games']} games: "
            f"level={rating['level']:.4f}, mu={rating['mu']:.6f}, phi={rating['phi']:.6f}; "
            f"stop at phi <= {self.config['target_phi']}"
        )
        if rating["phi"] <= self.config["target_phi"]:
            raise TargetReached()
        return rating

    def request(self, suffix, body=None):
        if suffix == "start":
            if (self.directory / "deployment-hold.json").exists():
                raise DeploymentHold()
            # Check the official profile before every new search, never during play.
            self.rating()
            # Restore the durable pending marker immediately before sending the POST.
            self.save("starting_search", awaiting_game=True)
        return super().request(suffix, body)

    def tick(self):
        try:
            if (
                len(self.state["completed"]) >= self.config["games"]
                and not self.state["active_game"]
            ):
                self.rating()
                raise RuntimeError(
                    "Continuation safety limit reached above target uncertainty"
                )
            done = super().tick()
            if done:
                self.rating()
                raise RuntimeError(
                    "Continuation safety limit reached above target uncertainty"
                )
            return False
        except TargetReached:
            self.save(
                "complete", awaiting_game=False, active_game=None, finished_at=now()
            )
            self.note("Target uncertainty reached; no more searches will start")
            return True
        except DeploymentHold:
            self.save("awaiting_deployment", awaiting_game=False)
            return False
        except RatingPending:
            return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=Path)
    args = parser.parse_args()
    with args.config.open("rb") as handle:
        UncertaintySeries(tomllib.load(handle)).run()
