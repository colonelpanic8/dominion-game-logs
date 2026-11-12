I won **49 to 24**, ending the game on my turn 22 by buying the last Province. The bot went first, so we each had 22 turns.

**Kingdom:** Old Witch (with the Reckless trait), Familiar, Hunting Lodge, Crew, Ranger, Figurine, Artificer, Buried Treasure, Duplicate, Bauble. Landscapes: Dominate, Architects' Guild.

**Plan:** money, plus a Reckless Old Witch bought at $5 while Curses lasted. Each one draws 6 and gives 2 Curses, then goes back to its pile. Otherwise Gold at $6–7 and Province at $8. I kept to it and added one Hunting Lodge and one Buried Treasure late. The bot played Familiar plus money.

**What decided it:** Curses went 8–2 in my favour from four Old Witch plays. The big turn was turn 11: Hunting Lodge discarded a junk hand, then two Old Witches drew $15 and emptied most of the Curse pile. I spent it on Dominate, a Province plus 9 VP, which took the score from 8–1 to 22–1. Two early mistakes cost a little: I twice drew Hunting Lodge only after playing my one Action. Buying Old Witch at $6 on turn 8 instead of Gold paid off.

**Tool problems:**
1. In the buy phase, buying a card directly "plays only the treasures that card needs and leaves the rest in hand". That would have left Buried Treasure unplayed and lost its +$3 next turn. The NOTE warning only appears when you have 2 Buys, and a non-money Treasure needs the same warning.
2. "unplayed treasures in hand make $3 plus Buried Treasure (varies)": Buried Treasure always makes $0 the turn it's played, so "varies" is misleading.
3. The Reckless trait shows only under ALSO ("Reckless is attached to Old Witch"). The supply and buy list just say "Old Witch $5", so a card with doubled effects looks normal.
4. "Journey token is on SetAsideZone" exposes an internal zone name and means nothing to a player.
5. The first `state` call showed my previous finished game instead of a lobby, which was harmless but needed an extra step before `new_game`.
