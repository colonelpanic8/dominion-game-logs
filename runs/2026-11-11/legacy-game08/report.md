I lost **73–93** to Lord Rattington (bot). The game ended on the bot's turn 27, when the Duchy pile became the third empty pile after Ruins and Estates.

**Kingdom:** Corsair, Gatekeeper, Candlestick Maker, Temple, Witch's Hut, Grand Market, Modify, Cargo Ship, Cultist, Devil's Workshop. Landscapes were Quest and Museum (2 VP for each differently named card), with Colony and Platinum in the game.

**Plan:** Money with chained Cultists for draw and Ruins junking, Devil's Workshop for free Gold, and Temple to trim. Platinum and Colony after that, then cheap new names for Museum. I kept to it until turn 11, when the bot started buying Provinces; from then on I bought points.

**What decided it:**
- **My economy was too thin.** I took Silver plus a $4 card from Devil's Workshop over a plain Gold three times. I never had more than 2 Golds or any Platinum, and my best turn was $10. The bot made $8–12 from turn 7, when it bought Platinum, and finished with 5 Provinces and 2 Colonies.
- **Cultist backfired under Museum.** Its junking gave the bot 4 Ruins names, about 8 VP.
- **Smaller misses:** a 5-card Quest discard went unused in several weak hands. On turn 21 I picked the wrong option number and ended Actions without playing Ruined Market, which cost almost nothing.

**Problems with the tools:**
1. The first `new_game` after a finished game failed: `Could not start a game: the table's kingdom editor is not available`. An identical retry worked.
2. Under `[play]`, Treasures show their cost, not what they make: `Silver $3`, `Gold $6`.
3. Cards the bot topdecked showed without names: `deck 9 (2 card; 7 unknown)`.
4. The Ruins pile has no card text: `Ruin Pile ($0, Action-Ruins-Randomizer): no card text on record`.
5. The Temple line was ambiguous: `ALSO VP Tokens 1 on Temple.` I couldn't tell if that was my token count or the VP on the pile. Also, the same card's option number moves between decisions (Ruined Market was 0, then 1), which caused my mistake on turn 21.
