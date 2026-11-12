I lost 31–51 to the bot. The game ended on its turn 20, when it bought the last Province.

**Kingdom:** Market, Smithy, Artisan, Remodel, Militia, Workshop, Poacher, Moat, Moneylender, Bandit. There were no landscapes and no villages, so an engine wasn't possible.

**Plan:** Smithy and money with one more terminal, Market at $5, Gold at $6–7, and Duchies once about 4 Provinces were left. I mostly stuck to it. I opened Smithy/Silver, but I picked Bandit as the second terminal instead of Militia, then bought a second Bandit and one Market.

**What decided the game:**
- **Opening:** my turn 2 and 3 hands each made only $3. The bot opened Silver/Militia, hit $7 on turn 3 and had 4 Golds and 2 Smithies by turn 10.
- **Provinces:** I bought the first one on turn 8, but the bot took four between turns 8 and 15. I was behind 9–21 by turn 13.
- **Endgame:** after that I could only buy Duchies and Estates and hope the bot missed $8, which it didn't.
- **My mistakes:** Bandit's Golds came too slowly. Buying a second Bandit instead of Gold or a second Smithy was probably wrong.

**Problems with the tools:**
1. During the buy phase the header shows `coins 0` until treasures are played, so the decision never states how much money I have. I worked it out by hand every turn.
2. Choosing a card plays only the treasures it needs, and the log then understates the hand. For example, it showed `plays a Silver and a Copper. (+$3)` when the hand held $4. On a turn with 2 Buys I had to pick "Autoplay Treasures" first so the second buy wouldn't come up short.
3. The opponent's cards stay hidden even after they were bought in public. The view showed `discard 6 (3 Copper, Estate, Silver; 1 unknown)` on turn 2, and on turn 20 still showed `discard 18 (...; 5 unknown)`. That made counting the bot's deck harder.
4. The final view said `Card tracking is 69 event(s) behind this view.` with no explanation of what that means or whether earlier views were stale.
5. `step` doesn't show the score difference or how many Provinces are left next to the decision. I had to rebuild these from the YOU, OPPONENT and SUPPLY lines each turn, and it mattered most in the endgame.
