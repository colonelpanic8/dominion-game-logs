# Coordinator live-journal reader recovery

During g72 the model guard stopped the coordinator with `Malformed complete archive record`. Both independent agents kept playing. Inspection found no malformed completed records in either journal. The live line iterator could read an incomplete tail, then treat its subsequently appended suffix as a separate complete line.

The reader now snapshots bytes and parses only newline-terminated records; it discards only the unfinished trailing fragment. Complete malformed records still fail closed. Five focused regression checks cover incomplete tails, subsequent completion, concurrent append, actual malformed records and incomplete UTF-8. The seven model checks, six lifecycle checks and Ruff also passed.

The coordinator resumed with the same active g72 and no creation pending. No journal, game, model, score or runner/server was modified. Sol was untouched. Exact recovery metadata and coordinator/test sources are preserved here.
