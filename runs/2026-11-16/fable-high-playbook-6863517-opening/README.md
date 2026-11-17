# Fable High revised-playbook opening validation

Both fresh Fable High sessions completed successfully with playbook `6863517`, high effort, and the kingdom/seed from the g70 technical forfeit. Every emitted assistant message identifies `claude-fable-5-2`; neither session refused or fell back to Opus.

The in-memory test ended after two total turns (one per seat). This is opening-only evidence, not a full-game reliability result, and is excluded from every series. Production games, services and playbook were untouched.

`provenance.json` records the immutable source and limitations; `test-harness.patch` records the diagnostic adjustments. The underlying native harness is byte-identical to production. All completed raw journals are stored losslessly under `sessions/`, with original SHA-256 values in `run.json`. Credential and work directories are excluded.
