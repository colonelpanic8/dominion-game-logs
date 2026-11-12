I won, **41–26**, on turn 17. My buy of the last Province ended the game, and the bot had played 16 turns.

**Kingdom:** Harbinger, Moat, Militia, Bureaucrat, Gardens, Chapel, Poacher, Laboratory, Moneylender, Library. No Events or other landscapes.

**Plan:** there are no villages and no +Buy, so nobody can score more than one Province a turn. I chose Library Big Money. Library draws back up to 7 cards, so the bot's Militia cost me little. I opened Library with no buy on the $2 turn, then bought Gold and Provinces. I started on Duchies, Gardens and Estates with 4 Provinces left. I kept to the plan throughout.

**What decided it:** the bot opened Chapel/Militia and then Labs, but it trashed slowly. It had 1 VP on turn 10, when I already had 15, and I had my first Province on turn 6. In every Militia attack I kept Library, and it drew me back to $8 or more three times (turns 11, 14 and 17). Late on, Gardens was worth 2 VP for $4 at 19–24 cards, so I bought it twice instead of Estates. With 1 Province left I led 32–22, so the bot couldn't win by ending the game.

**Problems with the tools:**
1. Before `new_game`, `state` showed the previous finished game as if it were live: "GAME … (over): turn 1, your turn, actions 1… unplayed treasures in hand make $4", next to "RESULT … EyeVanMaliceSon 3 VP (resigned)".
2. Buy options have no prices ("6: Gardens", "11: Laboratory"), so I had to look costs up in `SUPPLY`.
3. Picking a card plays only the treasures it needs, and the log is the only place that shows which ones: "plays 6 Coppers. (+$6)" when my hand made $7. Nothing warns that the rest stay unplayed.
4. The bot's money was hard to follow. During its attack the view said "coins 2"/"coins 3", and its turn showed "plays 2 Silvers and a Copper. (+$5)" with no running total including its Poacher and Militia.
5. Gardens' current worth isn't shown anywhere, so I counted my cards by hand from the "owns" line.
