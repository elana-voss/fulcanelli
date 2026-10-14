# Lexicon Headword List — instructions

You make the headword list for the English lexicon of Fulcanelli's *Le Mystère des Cathédrales*, from the whole French text. Writers will later write one entry per headword; a script builds a SillyTavern worldbook from the entries.

## Input
- `TEXT`: the whole book in French, paragraphs marked `[PARIS.3 ¶12]`, footnotes `[PARIS.3 n2]`.
- `RULES`: the binding rules (no outside knowledge; names spelled as the text spells them).

## What gets an entry
- **term**: the specialised vocabulary — alchemical, symbolic, architectural, iconographic, heraldic — and ordinary words used in a special sense (e.g. *Corbeau*, *Rebis*, *Athanor*, *art gothique*, *langue des oiseaux*, *voie sèche*).
- **person**: every author, adept, artist or figure the text names and says something about.
- **work**: every book, treatise or inscription the text cites by title.
- **place**: every monument, building or motif-bearing site the text describes (e.g. Notre-Dame de Paris, Hôtel Lallemant, croix d'Hendaye).
One entry per thing, keyed by the French form the text uses most; other spellings or grammatical forms of the same word go in `forms`. A different name for the same thing gets its own entry, linked in `same_as` only when the text asserts the identity.

## Output
Write one JSON array once, with a single Write, to the path you are given:

```json
[
  {"id": "e001", "kind": "term", "fr": "Corbeau", "forms": ["corbeau"], "en": "Raven",
   "rendering": "literal", "refs": ["PARIS.3 ¶2", "PARIS.3 ¶3"], "same_as": []}
]
```
- `en`: the English headword. `rendering`: `literal` (plain translation), `established` (the usual English term for this French term, e.g. *Grand Œuvre* → "Great Work"), `gloss` (the text's own explanation gives the English), `coined` (ours, because no plain English carries the sense), or `name` (persons, works and places keep the text's spelling; works keep the French title as `en` with an English title after " — ").
- `refs`: up to 6 references, the most telling first (where the text defines, explains or decodes it).
- `same_as`: ids of entries the text says are the same thing.
- Ids `e001`… in order of first appearance in the text.

No rewrite passes. Reply with only the path and the count of entries per kind.
