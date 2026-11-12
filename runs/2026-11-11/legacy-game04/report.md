I won **38 VP to 17**. I bought the last Province on turn 17, which ended the game, after 17 turns each.

**Kingdom:** Legionary, Cellar, Astrolabe, Pillage, Crypt, Swamp Hag, Coven, Trickster, Dismantle, Altar, plus the Events Dominate and Mirror.

**Plan:** The board has no draw and no village, so an engine wasn't possible. I played Big Money with junkers: open Dismantle/Silver, then Swamp Hag, then Covens (non-terminal +$2 that gives a Curse), then Gold and Provinces. I kept to it: Dismantle/Silver, Swamp Hag on turn 5, Covens on turns 6, 7 and 9, Golds, then six Provinces from turn 12 on.

**What decided it:**
- **Dismantle:** it turned both Estates into Golds by turn 6, so I had 6 Golds by turn 11.
- **Curses:** Coven and Swamp Hag gave the bot 8 Curses. It took 6 into exile from Coven and gained 2 from Swamp Hag. They still count −1 VP each, so they cost it 8 VP, and the Swamp Hag ones also clogged its deck.
- **My mistake:** on turn 9 I trashed a Gold to Dismantle when I meant a Silver. I took a Coven and a Gold as compensation, so it cost me little.

**Tool problems:**
1. **Trash prompt lists no costs.** d60 printed `0: Copper 1: Copper 2: Silver 3: Gold` while the gain prompt shows `$` costs. With the indices shuffling every decision, this is exactly where I misread. Showing costs, or confirming an irreversible trash of your best card, would help.
2. **Money is split across two fields.** `coins 2, unplayed treasures in hand make $6`: I had to add these myself on every buy. A single "total available $8" would be clearer.
3. **Buying plays only part of the hand.** It reported `plays a Silver and a Copper. (+$3)` while `$4` sat in hand. That's harmless here, but it would matter with Treasures that do something when played or when order matters, and nothing warns about it.
4. **Unclear status lines.** `ALSO nothing any more` and `Lord Rattington has reminders up for Swamp Hag.` don't say what the reminder means.
5. **Old game shown on startup.** `state` first showed a finished earlier game (`GAME 185829637 (over)`), with nothing saying it was stale.
