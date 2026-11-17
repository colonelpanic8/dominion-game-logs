# Sol High: official game 186034884

Game 11/15 of SolDominion's rated two-player series on 2026-11-16.

`observed-game-log.txt` and `.json` contain observed official log entries. All observed sequences are contiguous from zero. `game-log-observations.jsonl.gz` retains revisions to those entries, with observation times and source sessions.

`sessions/*/interactions.jsonl.gz` are losslessly compressed, unchanged runner traces: model settings, tool calls/replies, legal views, usage and recorded reasoning summaries. `reasoning-and-report.md` makes those recorded summaries and the final agent report readable.

A finished-game view is not recorded in the trace. `authoritative-result.json` preserves the independently recorded final result. No unobserved final notification, raw WebSocket capture, complete API prompt or provider internals are invented.

[Series metadata, deployment provenance, config, journals and final rating](../../../series/2026-11-16-sol-high-rated-15/README.md).
