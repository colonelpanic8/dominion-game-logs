I won 43–16. The game ended on turn 18 when I bought the last Province. Both of us took 18 turns.

**Kingdom:** Chapel, Fishing Village, Wharf, Militia, Market, Workshop, Bureaucrat, Moat, Harbinger, Remodel.

**Plan:** a thin Chapel/Wharf/Fishing Village engine, with Militia and Gold as payload and +Buy from Wharf. It beats Wharf-Big Money's one-Province-a-turn limit. I opened Militia/Chapel on a 4/3 split, Chapel'd down to a single Estate and 3 Coppers, then bought 3 Wharfs, 4 Fishing Villages and 1 Gold. I started on Provinces at turn 12, when I had $14 and 3 Buys. I mostly kept to the plan. Market never got bought, because Fishing Villages were the scarcer piece.

**What decided it:** on turns 13–14, Wharfs and Fishing Villages carried over from the previous turn. Turn 14 opened with 11 cards, $15 and 4 Buys, and Chapel trashed two Coppers to buy two Provinces with exactly $16. That made it 24–8 with 3 left. The bot opened Chapel/Moat and built Markets, but its first Province came only on turn 13, and from turn 15 it bought Duchies and Estates. Its Moat blocked my Militia three times.

**Tool problems:**
1. The `OPPONENT TURNS` totals leave out $ from Actions. On turn 9 it says "made $4, bought Market", but the bot's Market gave +$1 and it spent $5. Turn 13's "made $7, bought Province" has the same gap.
2. In the `[play]` group, Treasures show their price, not what they produce: "Silver $3" and "Gold $6" appear right beside "$9 available". That is easy to read as coin value.
3. When buying a card plays only the Treasures it needs, the log line understates the turn's money. On turn 7, "plays a Silver and a Copper. (+$3)" is followed by buying a $5 Wharf, with Militia's $2 shown only in the header.
4. I had to work out by hand that a Wharf left in hand when my turn ended is discarded and misses the next turn. On turn 10 nothing in the view warned that it would miss the reshuffle.
5. One rejection was my own mistake: I sent option 4 to a 3-option decision before reading it. The error message and the re-sent decision were clear.
