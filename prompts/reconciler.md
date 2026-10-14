# Reconciler — instructions

Two readers independently read the same chunk of Fulcanelli's *Le Mystère des Cathédrales* following the Chunk Reader instructions. Your job: produce one reading that is better than either.

## Inputs
- `CHUNK` — the source chunk (the only authority).
- `READING_A`, `READING_B` — the two JSON readings.
- The Chunk Reader instructions (`TASK`) and the binding rules (`RULES`) — every rule there binds you too, and the output schema is the reader's.

## How
1. Read the chunk in full, footnotes included.
2. Take the **union** of what A and B found, merging duplicates into the better-phrased, better-referenced entry.
3. Where A and B **disagree** (voice, decoding, plain meaning, stated vs interpreted, a term's meaning or English rendering), go back to the cited passage and decide from the text. If the text genuinely supports both, move it to `ambiguities` with both readings and their basis.
4. **Drop** anything neither the text nor its reference supports, any outside knowledge, any decoding the text does not make, and any quote that is not verbatim — or fix the quote by copying it exactly from the chunk. Fix English renderings that misread the French.
5. Add anything important both readers missed, especially decodings, method points the text explains, and asserted equivalences between terms.
6. Keep `notes` in the order of the text.

Read the bundle once, write the result once (one Write); no rewrite or compression passes, no checking of quotes yourself (a script and a checker do that).

## Output
Write one JSON file in the Chunk Reader schema to the path you are given. Reply with only: the output path, and at most five short lines on the substantive disagreements you resolved and how.
