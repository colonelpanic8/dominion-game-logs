# dominion-game-logs

Games of Dominion played by AI agents on dominion.games, with everything needed to read each decision and to know exactly what played it.

An agent runs in [dominion-playbook](https://github.com/colonelpanic8/dominion-playbook) (its context and skills) and plays through the MCP server in [dominion-navigator](https://github.com/colonelpanic8/dominion-navigator).

Official matches played through dominion-arena are also archived here. The
[Sol High rated series](series/2026-11-16-sol-high-rated-15/README.md) contains
15 games and all 17 agent sessions, with deployment provenance, service journals,
and the verified final rating. Each game's directory contains the observed game
log, authoritative result, and losslessly compressed interaction journals.

**Model identity:** the Fable-labelled g69 and g71 sessions switched to Opus 5.
See the [model-identity correction](series/2026-11-16-fable-model-identity/README.md)
before treating their results as Fable–Astra comparisons.

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
| [2026-11-17/sol-high-186044328](runs/2026-11-17/sol-high-186044328) | gpt-6.1-sol high | human | 186044328: mayumaro1 0, SolDominion 0 | 6863517 | ? |  |
| [2026-11-17/sol-high-186043435](runs/2026-11-17/sol-high-186043435) | gpt-6.1-sol high | human | 186043435: thepilferer 4, SolDominion 18 | 6863517 | ? |  |
| [2026-11-17/sol-high-186043033](runs/2026-11-17/sol-high-186043033) | gpt-6.1-sol high | human | 186043033: SolDominion 30, Kaityo_777 28 | 6863517 | ? |  |
| [2026-11-17/sol-high-186042551](runs/2026-11-17/sol-high-186042551) | gpt-6.1-sol high | human | 186042551: wyan 34, SolDominion 46 | e565fe8 | ? |  |
| [2026-11-17/sol-fable-g83](runs/2026-11-17/sol-fable-g83) | Sol High vs Fable High high | agent | g83: Sol High 42, Fable High 36 | 6863517 | ? |  |
| [2026-11-17/sol-fable-g82](runs/2026-11-17/sol-fable-g82) | Sol High vs Fable High high | agent | g82: Fable High 35, Sol High 41 | 6863517 | ? |  |
| [2026-11-17/sol-fable-g81](runs/2026-11-17/sol-fable-g81) | Sol High vs Fable High high | agent | g81: Sol High 35, Fable High 12 | 6863517 | ? |  |
| [2026-11-17/sol-fable-g80](runs/2026-11-17/sol-fable-g80) | Sol High vs Fable High high | agent | g80: Fable High 24, Sol High 40 | 6863517 | ? |  |
| [2026-11-17/sol-fable-g79](runs/2026-11-17/sol-fable-g79) | Sol High vs Fable High high | agent | g79: Sol High 55, Fable High 35 | 6863517 | ? |  |
| [2026-11-17/sol-fable-g78](runs/2026-11-17/sol-fable-g78) | Sol High vs Fable High high | agent | g78: Fable High 23, Sol High 40 | 6863517 | ? |  |
| [2026-11-17/sol-fable-g77](runs/2026-11-17/sol-fable-g77) | Sol High vs Fable High high | agent | g77: Sol High 23, Fable High 37 | 6863517 | ? |  |
| [2026-11-17/fable-astra-g76](runs/2026-11-17/fable-astra-g76) | Fable High vs Astra High high | agent | g76: Fable High 39, Astra High 8 | 6863517 | ? |  |
| [2026-11-17/fable-astra-g75](runs/2026-11-17/fable-astra-g75) | Fable High vs Astra High high | agent | g75: Astra High 14, Fable High 45 | 6863517 | ? |  |
| [2026-11-17/fable-astra-g74](runs/2026-11-17/fable-astra-g74) | Fable High vs Astra High high | agent | g74: Fable High 46, Astra High 34 | 6863517 | ? |  |
| [2026-11-17/fable-astra-g73](runs/2026-11-17/fable-astra-g73) | Fable High vs Astra High high | agent | g73: Astra High 36, Fable High 27 | 6863517 | ? |  |
| [2026-11-17/fable-astra-g72](runs/2026-11-17/fable-astra-g72) | Fable High vs Astra High high | agent | g72: Fable High 35, Astra High 37 | 6863517 | ? |  |
| [2026-11-16/sol-high-186042286](runs/2026-11-16/sol-high-186042286) | gpt-6.1-sol high | human | 186042286: 34msms 49, SolDominion 15 | e565fe8 | ? |  |
| [2026-11-16/sol-high-186041689](runs/2026-11-16/sol-high-186041689) | gpt-6.1-sol high | human | 186041689: SolDominion 28, ryutake 42 | e565fe8 | ? |  |
| [2026-11-16/sol-high-186041530](runs/2026-11-16/sol-high-186041530) | gpt-6.1-sol high | human | 186041530: SolDominion 2, Stemar 2 | e565fe8 | ? |  |
| [2026-11-16/sol-high-186041477](runs/2026-11-16/sol-high-186041477) | gpt-6.1-sol high | human | 186041477: rainshifter 0, SolDominion 0 | e565fe8 | ? |  |
| [2026-11-16/sol-high-186040335](runs/2026-11-16/sol-high-186040335) | gpt-6.1-sol high | human | 186040335: SolDominion 39, everybell 31 | ? | ? |  |
| [2026-11-16/sol-high-186039786](runs/2026-11-16/sol-high-186039786) | gpt-6.1-sol high | human | 186039786: Noboyuki 35, SolDominion 42 | ? | ? |  |
| [2026-11-16/sol-high-186036166](runs/2026-11-16/sol-high-186036166) | gpt-6.1-sol high | human | 186036166: Relicdog 30, SolDominion 19 | ? | ? |  |
| [2026-11-16/sol-high-186035907](runs/2026-11-16/sol-high-186035907) | gpt-6.1-sol high | human | 186035907: SolDominion 18, Rok3 2 | ? | ? |  |
| [2026-11-16/sol-high-186035246](runs/2026-11-16/sol-high-186035246) | gpt-6.1-sol high | human | 186035246: SolDominion 35, dtbomber 26 | ? | ? |  |
| [2026-11-16/sol-high-186034949](runs/2026-11-16/sol-high-186034949) | gpt-6.1-sol high | human | 186034949: yukkiboi 0, SolDominion 0 | ? | ? |  |
| [2026-11-16/sol-high-186034884](runs/2026-11-16/sol-high-186034884) | gpt-6.1-sol high | human | 186034884: SolDominion 3, nateopp 3 | ? | ? |  |
| [2026-11-16/sol-high-186034460](runs/2026-11-16/sol-high-186034460) | gpt-6.1-sol high | human | 186034460: SolDominion 0, GameBot3000 3 | ? | ? |  |
| [2026-11-16/sol-high-186034403](runs/2026-11-16/sol-high-186034403) | gpt-6.1-sol high | human | 186034403: SolDominion 3, nateopp 3 | ? | ? |  |
| [2026-11-16/sol-high-186034175](runs/2026-11-16/sol-high-186034175) | gpt-6.1-sol high | human | 186034175: hangdong69 1, SolDominion 1 | ? | ? |  |
| [2026-11-16/sol-high-186033558](runs/2026-11-16/sol-high-186033558) | gpt-6.1-sol high | human | 186033558: SolDominion 29, Pitstop363 8 | ? | ? |  |
| [2026-11-16/sol-high-186032758](runs/2026-11-16/sol-high-186032758) | gpt-6.1-sol high | human | 186032758: SolDominion 45, mdwicker 46 | ? | ? |  |
| [2026-11-16/sol-high-186032083](runs/2026-11-16/sol-high-186032083) | gpt-6.1-sol high | human | 186032083: GameBot3000 10, SolDominion 11 | ? | ? |  |
| [2026-11-16/sol-high-186031039](runs/2026-11-16/sol-high-186031039) | gpt-6.1-sol high | human | 186031039: dominiondominion 0, SolDominion 0 | ? | ? |  |
| [2026-11-16/sol-high-186030563](runs/2026-11-16/sol-high-186030563) | gpt-6.1-sol high | human | 186030563: SolDominion 36, amiwan 5 | ? | ? |  |
| [2026-11-16/sol-high-186029319](runs/2026-11-16/sol-high-186029319) | gpt-6.1-sol high | human | 186029319: SolDominion 37, weitzy 3 | ? | ? |  |
| [2026-11-16/sol-high-186028514](runs/2026-11-16/sol-high-186028514) | gpt-6.1-sol high | human | 186028514: Quen_tin_Zug 18, SolDominion 36 | ? | ? |  |
| [2026-11-16/fable-high-playbook-6863517-opening](runs/2026-11-16/fable-high-playbook-6863517-opening) | claude-fable-5-2 (both seats) high | Fable High diagnostic seat | isolated-g1 (opening diagnostic only): Test (1) 2, Test (2) 3 | 6863517 | ? |  |
| [2026-11-16/fable-astra-g71](runs/2026-11-16/fable-astra-g71) | Fable High vs Astra High high | agent | g71: Fable High 27, Astra High 47 | ? | ? |  |
| [2026-11-16/fable-astra-g70](runs/2026-11-16/fable-astra-g70) | Fable High vs Astra High high | agent | g70: Astra High 2, Fable High 3 | ? | ? |  |
| [2026-11-16/fable-astra-g69](runs/2026-11-16/fable-astra-g69) | Fable High vs Astra High high | agent | g69: Fable High 18, Astra High 21 | ? | ? |  |
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
