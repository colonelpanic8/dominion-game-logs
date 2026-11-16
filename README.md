# dominion-game-logs

Games of Dominion played by AI agents on dominion.games, with everything needed to read each decision and to know exactly what played it.

An agent runs in [dominion-playbook](https://github.com/colonelpanic8/dominion-playbook) (its context and skills) and plays through the MCP server in [dominion-navigator](https://github.com/colonelpanic8/dominion-navigator).

## Playing a game

Start the navigator's Chrome first (`npm run launch:chrome` in dominion-navigator, logged in to dominion.games), then:

```sh
just play                                   # one game against a bot, random kingdom
just play --count 5 --effort xhigh          # five games in a row
just play --kingdom Chapel "Fishing Village" Wharf Militia Market
just play --help
```

Each game lands in `runs/<date>/<time>-<model>-<effort>/`:

| File | What it holds |
| --- | --- |
| `run.json` | Settings, versions of everything (harness, model, both repositories' commits and dirty state), cost and result |
| `<game>.md` | The decision log: one line per decision with the agent's reason |
| `<game>.jsonl` | The same log as data, including forced answers and the versions the server saw |
| `transcript.jsonl` | The agent's full Claude Code transcript |
| `report.md` | The agent's report after the game |
| `prompt.md` | The exact prompt |
| `*.diff` | Uncommitted changes in dominion-playbook or dominion-navigator when the game ran |

## Runs

A `*` after a commit means that repository had uncommitted changes, saved in the run's `.diff`.

<!-- runs:start -->
| Run | Model | Opponent | Games (final VP) | dominion-playbook | dominion-navigator | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| [2026-11-15/arena-g5](runs/2026-11-15/arena-g5) | Argon High vs Terra  | agent | g5: Argon High 27, Terra 13 | ? | ? |  |
| [2026-11-15/arena-g4](runs/2026-11-15/arena-g4) | Terra vs Sonnet High  | agent | g4: Terra 40, Sonnet High 23 | ? | ? |  |
| [2026-11-15/arena-g3](runs/2026-11-15/arena-g3) | Terra vs Sonnet Low  | agent | g3: Terra 36, Sonnet Low 28 | ? | ? |  |
| [2026-11-15/arena-g2](runs/2026-11-15/arena-g2) | Sonnet via Gemini vs Sol 6.1  | agent | g2: unfinished | ? | ? |  |
| [2026-11-15/arena-g1](runs/2026-11-15/arena-g1) | Sonnet via Gemini vs Sol 6.1  | agent | g1: Sonnet via Gemini 3, Sol 6.1 3 | ? | ? |  |
| [2026-11-12/005431-opus-high](runs/2026-11-12/005431-opus-high) | opus high | bot | 185832858: colonelpanic8 92, Lord Rattington 39 | fbad6da* | 4fa8d02 | $4.49 |
| [2026-11-11/legacy-game12](runs/2026-11-11/legacy-game12) | opus high | bot | 185831340: Lord Rattington 30, colonelpanic8 19 | fbad6da | f484287 | $2.84 |
| [2026-11-11/legacy-game11](runs/2026-11-11/legacy-game11) | opus high | bot | 185831262: Lord Rattington 41, colonelpanic8 40 | fbad6da | cdac4df | $1.83 |
| [2026-11-11/legacy-game10](runs/2026-11-11/legacy-game10) | opus high | bot | 185831104: colonelpanic8 43, Lord Rattington 16 | fbad6da | ea14cf8 | $2.46 |
| [2026-11-11/legacy-game09](runs/2026-11-11/legacy-game09) | opus high | bot | 185830949: colonelpanic8 44, Lord Rattington 37 | fbad6da | ea14cf8 | $2.57 |
| [2026-11-11/legacy-game08](runs/2026-11-11/legacy-game08) | opus default | bot | 185830292: Lord Rattington 93, colonelpanic8 73 | fbad6da | d7204d1 | $2.96 |
| [2026-11-11/legacy-game07](runs/2026-11-11/legacy-game07) | opus default | bot | 185830088: colonelpanic8 49, Lord Rattington 24 | fbad6da | 1505d0f | $1.73 |
| [2026-11-11/legacy-game06](runs/2026-11-11/legacy-game06) | opus default | bot | 185829955: colonelpanic8 48, Lord Rattington 18 | 046d67d | 1505d0f | $1.58 |
| [2026-11-11/legacy-game05](runs/2026-11-11/legacy-game05) | opus default | bot | 185829788: colonelpanic8 30, Lord Rattington 23 | 046d67d | e369ac1 | $1.88 |
| [2026-11-11/legacy-game04](runs/2026-11-11/legacy-game04) | opus default | bot | 185829721: colonelpanic8 38, Lord Rattington 17 | 046d67d | e369ac1 | $1.40 |
| [2026-11-11/legacy-game03](runs/2026-11-11/legacy-game03) | opus default | bot | 185829637: colonelpanic8 41, Lord Rattington 40 | 046d67d | e369ac1 | $1.39 |
| [2026-11-11/legacy-game02](runs/2026-11-11/legacy-game02) | opus default | bot | 185829476: EyeVanMaliceSon 41, Lord Rattington 26 | 046d67d | 16319cd | $1.30 |
| [2026-11-11/legacy-game01](runs/2026-11-11/legacy-game01) | opus default | bot | 185829326: Lord Rattington 51, EyeVanMaliceSon 31 | 046d67d | 763d953 | $1.55 |
<!-- runs:end -->
