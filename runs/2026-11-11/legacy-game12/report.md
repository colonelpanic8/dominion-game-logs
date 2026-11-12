I lost the game, 19 VP to the bot's 30. We each had 16 turns, and the bot ended it by buying the last Province.

**Kingdom:** Steward, Workers Village, Laboratory, Militia, Remodel, Masquerade, Patrol, Cellar, Bridge, Moat. No landscapes. I went first with a 4/3 opening.

**Plan:** an engine of Workers Villages for Actions and Buys, Labs and Masquerades for draw, Masquerade to trash, with Bridges and Militia as the payload. I opened Militia and Masquerade. I only partly kept to it. My first Bridge came on turn 10, I bought Gold over a Lab on turn 11, and I started buying Provinces on turn 12 because I was already down 0–12.

**What decided it:** the bot played money with Labs and a Patrol. It took its first Province on turn 7 and made $8 or more almost every other turn after that. My engine never drew its whole deck, and I had 0 VP until turn 12. Payload came too late: one Bridge, and no double-Province turn ever.

I also helped the bot. I passed it an Estate with Masquerade six times, and it trashed every one, so my "junk" thinned its deck. Against a money deck, a Masquerade/Militia/Lab deck that greened early would probably have done better than the engine. By the end, a Province on turn 16 only tied 24–24, and ties go to the player with fewer turns. So I played Militia and bought an Estate, hoping the bot would miss $8. It drew a Lab and made exactly $8.

**Tool problems:**
1. The opponent-turn summary leaves out $ from Action cards. It printed `turn 6 Lord Rattington: made $3, bought Laboratory`, but the log also shows `plays a Militia… gets +$2`, so the real total was $5.
2. Card names don't match: the options say `Workers Village`, but the log says `buys and gains a Worker's Village`. That makes text searches miss.
3. After a Masquerade swap, the next decision (`d46: You may play Actions`) didn't reprint my hand, so I had to work out which card I'd received.
4. While it's the bot's turn, the header shows bare counters (`turn 3, Lord Rattington's turn, actions 0, buys 1, coins 0`) without saying whose they are.
