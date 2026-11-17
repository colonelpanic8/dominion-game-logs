# Sol High: 15 rated Dominion.games matches

SolDominion, gpt-6.1-sol with high reasoning effort. Exactly 15 completed matches: 12 wins, 3 losses. Verified final level 48.52, mu 0.68, phi 0.438, rank 1811.

Patient timer, two players, rating difference −5 to +5. The Complete subscription was purchased after the first match; full ownership and min/max card pool 10 were verified before the second match. No banned or disliked cards.

| Game | Official ID / archive | Result | Agent sessions |
| --- | --- | --- | --- |
| 1 | [186028514](../../runs/2026-11-16/sol-high-186028514) | Win | 1 |
| 2 | [186029319](../../runs/2026-11-16/sol-high-186029319) | Win | 1 |
| 3 | [186030563](../../runs/2026-11-16/sol-high-186030563) | Win | 1 |
| 4 | [186031039](../../runs/2026-11-16/sol-high-186031039) | Win | 1 |
| 5 | [186032083](../../runs/2026-11-16/sol-high-186032083) | Loss | 1 |
| 6 | [186032758](../../runs/2026-11-16/sol-high-186032758) | Loss | 3 |
| 7 | [186033558](../../runs/2026-11-16/sol-high-186033558) | Win | 1 |
| 8 | [186034175](../../runs/2026-11-16/sol-high-186034175) | Win | 1 |
| 9 | [186034403](../../runs/2026-11-16/sol-high-186034403) | Win | 1 |
| 10 | [186034460](../../runs/2026-11-16/sol-high-186034460) | Win | 1 |
| 11 | [186034884](../../runs/2026-11-16/sol-high-186034884) | Win | 1 |
| 12 | [186034949](../../runs/2026-11-16/sol-high-186034949) | Win | 1 |
| 13 | [186035246](../../runs/2026-11-16/sol-high-186035246) | Win | 1 |
| 14 | [186035907](../../runs/2026-11-16/sol-high-186035907) | Win | 1 |
| 15 | [186036166](../../runs/2026-11-16/sol-high-186036166) | Loss | 1 |

## Preservation

All 17 local agent sessions are preserved losslessly, including retries. Every JSONL event parses cleanly. Extracted log sequences have no missing sequence numbers, but eight games have no finished-game notification in their agent trace. Authoritative final results are saved for every game. Original source archives and the separate local backup remain untouched.

`source-manifest.json` records source paths and per-session coverage. `series/status.json` preserves the final coordinator state and rating verification. `series/config.toml`, `series/rated_series.py` and `journals/` preserve the automation and the service logs. `deployment-history.json` distinguishes verified revisions from unknown versions; `harness-source/` contains published source snapshots for the known deployments. Initial games 1 and 2 have unknown exact deployment provenance. Complete API input bodies and unrecorded provider internals were not saved. The series used the direct OpenAI API, not Codex CLI or the older navigator runner.

Credentials and official session files are excluded; trace token fields were already redacted by the runner. Game 4 used an explicitly authorized manual official opponent timeout. Game 5 is retained as a loss after a connection failure; the operator did not resign.

Run `sha256sum -c SHA256SUMS` here to verify all shared files and game artifacts. The checksums of the uncompressed source journals are also recorded in each run.json.
