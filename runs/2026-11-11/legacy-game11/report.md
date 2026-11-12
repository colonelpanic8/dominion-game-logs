I lost by one point, 40–41. We both took 16 turns, and the game ended on Provinces when the bot bought the last one with $10.

**Kingdom:** Rabble, Guard Dog, Wheelwright, Quarry, Salvager, Expand, Livery, Fool, Conclave and Shepherd, plus the Commerce event and the Piazza project. Each deck started with a Lucky Coin and a Pasture.

**Plan:** Big Money with Shepherd and up to two Rabbles. There was no real village or strong trashing, so no engine. I opened Shepherd/Silver, bought Gold at $6–7, and switched to Duchies with 4 Provinces left. I kept to the plan, except that I never got the second Shepherd. Final deck: 3 Provinces, 4 Duchies, 5 Estates and Pasture.

**What decided it:** The bot's single Rabble discarded my Treasures three times, two Golds on turn 6 and a Gold and Silver on each of turns 11 and 14. My last two hands were $4 each, and Estates (worth 2 VP each with Pasture) couldn't hold off its final Province. One more VP would have tied it, since we took the same number of turns. In hindsight a Guard Dog or a second Shepherd might have bought that point, though I didn't test either.

**Tool problems:**
1. Before any Treasure is played, the buy list leaves out Lucky Coin. At turn 2, with "$3 available", the list stopped at "2: Estate $2". Silver only appeared after I played the Lucky Coin.
2. Autoplay skips Lucky Coin and Pasture, so playing them took an extra `step` most turns. The NOTE explains this, but it's a trap.
3. A bare label clashes between groups: "Gold" failed with "ambiguous in d11: buy:Gold (16), play:Gold (20)". Buy-phase labels could default to the buy group.
4. My deck tracking looked wrong on turn 10. After Rabble drew my last three known cards, the view showed `deck 1 (Province)`, with only one Province in my discard. By my count my deck should have been empty, with both Provinces in the discard.
5. Fool's Boons show `Boon Drawpile (Boon): no card text on record`, so I couldn't judge Fool.
