# Clean Fable/Astra best-of-five complete

Fable High wins **3–2**, coming back from 0–2. Every game was eligible: native Claude assistant messages stayed on claude-fable-5-2, and Astra direct requests stayed on gpt-6-astra; high effort was requested in every seat specification. Both trace writers finished for every game and no provider/model problems were recorded.

| Game | Winner | Fable VP | Astra VP |
| --- | --- | ---: | ---: |
| [g72](https://dominion-arena.duckdns.org/game/g72) | Astra | 35 | 37 |
| [g73](https://dominion-arena.duckdns.org/game/g73) | Astra | 27 | 36 |
| [g74](https://dominion-arena.duckdns.org/game/g74) | Fable | 46 | 34 |
| [g75](https://dominion-arena.duckdns.org/game/g75) | Fable | 45 | 14 |
| [g76](https://dominion-arena.duckdns.org/game/g76) | Fable | 39 | 8 |

The coordinator stopped successfully after the third eligible win with active_game=null and creation_pending=false. Public game inventory showed no running games and g76 as the highest native ID; no further game was created. Only the native monitoring schedule scheduled-task:7ced4cc8-466f-42bf-9f42-a81655a14e0d was disabled. Sol remained stopped by its user's earlier decision.

Application7d439ac and revised playbook6863517 were used throughout. The five-game manifest links immutable g72/g73 runs already archived in8b4a15d and new g74/g75/g76 runs. Configuration, coordinator source/state, public final-watch, requested seed and exact seat configuration, authoritative results, model identity evidence, every matching session/retry and all available root interaction/transcript/stdout/network journals are preserved. Gzip copies are byte-for-byte reversible, with original SHA256 and byte counts in run.json. Original sources were checked unchanged after copying. Work/auth directories and credentials are excluded; credential-bearing engine saves are not copied.

Coverage is limited to recorded provider output and observed game entries, whose revisions are retained. No absent final notification or private provider internals are fabricated. Native public final-watch contributes the complete public game log; individual per-run coverage reports sequence gaps. The old mixed-model g69/g70/g71 attempt remains preserved separately and contributes no wins here. Finished prior runs were not edited.
