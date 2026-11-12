I won, 92 VP to 39. The game ended after my turn 21 because three Supply piles ran out (Estate, Duchy, Marchland). Both of us played 21 turns.

**Kingdom:** Vampire, Oasis, Imperial Envoy, Displace, Moat, Wayfarer, Marchland, City Quarter, Mountain Village, Catacombs, plus the Events Deliver and Invasion. The bot played Catacombs with money.

**Plan:** an engine built around Vampire, which costs no Action. Each Vampire play gains a $5 card and hits the bot with a Hex, then it turns into a Bat, which trashes cards. Draw came from Envoy and Wayfarer, Actions from Mountain Village, and Deliver supplied extra Buys. I kept to the plan, with two additions:
- **Free Wayfarer:** Wayfarer costs whatever the last gained card cost, so buying a Copper made it free.
- **Marchlands to finish:** they weren't in the plan, but they won the endgame.

**What decided it:**
- **Turns 9–10:** my deck drew itself. Turn 10 made $17 for two Provinces, which put me ahead 13–9.
- **Hexes:** Vampire plays cut the bot to a 3-card hand, trashed one of its Silvers and gave it a Curse. It managed only one Province in turns 12–14.
- **Marchlands:** each one's gain gave +1 Buy and $1 per card discarded from hand, so most turns from 15 on I bought two VP cards. Each Marchland is worth 1 VP per 3 Victory cards I own, so they reached 7 VP each and I could end on piles.

**Tool problems:**
1. **A purchase I never chose.** On turn 21 I sent `choose: ["how-much-repay:2"]` for d106. The reply was `Answer rejected: decision d106 is not open (open decisions: d107)`, yet the log showed `repays 2 debt. buys and gains a Wayfarer`, and the next decision offered only `$0` cards. My next answer was rejected too, and the view then reverted to `coins 9, debt 2`. But it still listed `discard 1 (Wayfarer)` and `owns ... 3 Wayfarer` while the Supply showed `Wayfarer $6 x8`. The final result still lists 3 Wayfarers. Sending the repay as the plain number 18 worked.
2. **Missing card text:** `Hex Drawpile (Hex): no card text on record` and `Loot Pile: no card text on record`. I couldn't judge Vampire's attack or Invasion's Loot from the tools.
3. **Auto-skipped Action phase:** after an Envoy used my last Action, the view jumped straight to the buy phase. I could see the Mountain Village I'd drawn but had no Action left to play it, and nothing flagged that.
