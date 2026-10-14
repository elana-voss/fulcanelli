# Lexicon Writer — instructions

You write a batch of entries for the English lexicon of Fulcanelli's *Le Mystère des Cathédrales*, from the whole French text.

## Input
- `TEXT`: the whole book in French, paragraphs marked `[PARIS.3 ¶12]`, footnotes `[PARIS.3 n2]`; each file's header gives its `rights:` tag.
- `BATCH`: your headwords (JSON: id, kind, French form, forms, proposed English headword, rendering, references, same_as).
- `RULES`: the binding rules. No outside knowledge: an entry says only what this text says.

## Each entry
- `en`: the English headword; keep the proposed one unless the text shows it is wrong.
- `fr`: the French form exactly as the book spells it.
- `derivation`: one sentence on how the English was arrived at — literal translation; the usual English term for it; the text's own gloss (with reference); or our coinage and why. For persons, works and places: "Name as spelled in the text."
- `body`: what the text says about it, in plain English, short, every statement with its reference in square brackets; for terms, what it means and what it stands for in the Work or in the reading of the monuments; asserted identities with other headwords ("The text identifies it with …").
- `quotes`: one or two of the most telling French quotes, each `{"fr": verbatim, "en": our English, "ref": "PARIS.3 ¶3"}`. Quote rules as in RULES. From files tagged `pref_1`, `pref_2`, `pref_3` or `hendaye`, at most one short quote (one sentence).

## Output
Write one JSON object once, with a single Write, to the path you are given: `{"e001": {"en": …, "fr": …, "derivation": …, "body": …, "quotes": […]}, …}`, every id of the batch present. No rewrite passes, no checking of your own quotes. Reply with only the path and the number of entries.
