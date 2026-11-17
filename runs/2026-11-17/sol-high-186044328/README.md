# dominion.games:186044328

Finished official game, captured after the user stopped further Sol games. Its authoritative win is preserved; official profile count still reports24 at capture, so rating application for this25th result remains unverified.

`authoritative-result.json` preserves the result; `observed-game-log.*` contains observed entries, and `game-log-observations.jsonl.gz` preserves revisions.

All finished agent attempts are in `sessions/`, including every interaction journal, normalized transcript, native stdout/network journal and empty stderr file present. Gzip copies are byte-for-byte reversible; original SHA-256 values and coverage are in `run.json`. Authentication/work directories are excluded; original archives remain untouched. Reasoning includes only what the provider emitted.

[Series snapshot and provenance](../../../series/2026-11-17-sol-stopped-by-user/README.md).
