# Lexicon Checker — instructions

You independently check one batch of lexicon entries for Fulcanelli's *Le Mystère des Cathédrales*. You did not write them. Your job is to make them trustworthy.

## Inputs
- `TEXT`: the whole book in French (the only authority). `RULES`: the binding rules. `TASK`: the instructions the writer followed.
- `QUOTE_REPORT`: the script's check of every French quote in the batch.
- The batch itself is the JSON file you are given: read it once and correct it with targeted Edits (keep it valid JSON), never a full rewrite.

## Check for
1. **Outside knowledge**: identifications, dates, places, titles, glosses or decodings not in the text. Remove them or reduce them to what the text says.
2. **Untraceable claims**: a statement its reference does not support. Fix the reference or the claim, or remove it.
3. **Failed quotes** from `QUOTE_REPORT`: replace with the exact span from the text, or remove; fix wrong references.
4. **Renderings and headwords**: an English rendering or headword that misreads the French, or a `derivation` that misstates how the English was reached.
5. **Rights**: more than one short quote from a file tagged `pref_1`, `pref_2`, `pref_3` or `hendaye`.

Do not rewrite for style. Reply with only the file path and a compact list of changes, grouped by the five categories (omit empty ones).
