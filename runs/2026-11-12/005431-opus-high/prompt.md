Play a real game of Dominion on dominion.games through the `dominion` MCP tools. You are trying to win. Use this repository's context (already loaded) and its skills.

1. Call `new_game` with 1 bot(s) and a random kingdom. Its result lists the kingdom and the card text.
2. Analyze the kingdom with the kingdom-analysis skill (the quick version) and settle on a plan. Keep the write-up short.
3. Play the whole game to its end with `step`, applying the play-turn skill to each turn. Do not resign. Choose options by label rather than by number where you can. Give every `step` a `reason`: one or two sentences on why this choice beats the alternatives, naming the plan, the money or the endgame count it rests on. The reasons are recorded in a game log that people will read.
4. Do not use `inspect`; it shows information a player may not have. Do not read anything under evals/.
5. When the game is over, report in under 300 words: the kingdom, your plan and whether you kept to it, the result (scores and turns), what decided the game, and up to five concrete problems with the tools that made a decision harder, quoting the output.
