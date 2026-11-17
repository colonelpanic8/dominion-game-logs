# g70

Recorded during the Fable model-identity investigation. Requested Fable may fall back to Opus; see run.json and the linked series snapshot. This is not a clean pure-Fable comparison.

`authoritative-result.json` preserves the result; `observed-game-log.*` contains observed entries, and `game-log-observations.jsonl.gz` preserves revisions.

All finished agent attempts are in `sessions/`, including every interaction journal, normalized transcript, native stdout/network journal and empty stderr file present. Gzip copies are byte-for-byte reversible; original SHA-256 values and coverage are in `run.json`. Authentication/work directories are excluded; original archives remain untouched. Reasoning includes only what the provider emitted.

[Series snapshot and provenance](../../../series/2026-11-16-fable-astra-investigation-pause/README.md).
