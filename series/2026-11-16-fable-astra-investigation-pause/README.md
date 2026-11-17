# Fable/Astra investigation pause

All three recorded games are finished. g69 ended Astra 21–18; g70 ended in a turn-1 technical Fable forfeit after three provider safeguard refusals; g71 ended Astra 47–27 after 17 turns each. The user excluded g70 from scoring and authorized a replay after Fable is healthy. The raw coordinator score is Astra 2–0. **g69 and g71 switched from Fable to Opus; this is not a clean Fable/Astra score. Their adjudication is pending.** No other score exclusion has been authorized.

The agent_failure hold remains, with active_game=null and no further creation pending. The Fable/Astra monitoring schedule is disabled pending the user decision; Sol continuation is untouched.

Every g70 attempt and both g71 sessions are preserved losslessly with original SHA-256 values. Actual native model identities and final provider errors are recorded per session. The immutable [g69 archive](../../runs/2026-11-16/fable-astra-g69/README.md) and its [model identity correction](../2026-11-16-fable-model-identity/README.md) remain unchanged.

Playbook PR4 is merged, but production still uses the old playbook. The separate [new-playbook opening validation](../../runs/2026-11-16/fable-high-playbook-6863517-opening/README.md) passed in two fresh Fable High sessions without refusal/fallback; that does not validate a full game or retroactively change these games.

Each game includes authoritative final-watch, observed logs and revisions, every finished session, and coverage limits. Native seed/configuration and exact CLI prompts are preserved. Only provider-emitted output is available; unrecorded provider internals and unrecorded playbook revisions cannot be recovered. Work/auth directories and credentials are excluded.
