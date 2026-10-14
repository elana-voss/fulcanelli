# Page Checker — instructions

You independently check one English page written from Fulcanelli's *Le Mystère des Cathédrales*. You did not write it. Your job is to make it trustworthy.

## Inputs
- `TEXT`: the French source the page was written from (paragraph ids `[PARIS.3 ¶12]`, footnotes `[PARIS.3 n2]`). The only authority.
- `TASK`: the instructions the writer followed. `RULES`: the binding rules.
- `QUOTE_REPORT`: the script's check of every French quote on the page (quotes not found, wrong references).
- The page itself is the file you are given: read it once and correct it with targeted Edits, never a full rewrite.

## Check for
1. **Outside knowledge**: any identification, date, place, title, gloss or doctrine not in the French text, and any decoding (sound, root, argot) the text does not itself make. The most important check. Remove it or reduce it to what the text says.
2. **Untraceable claims**: a sentence its reference does not support, or a statement without a reference. Fix the reference or the claim, or remove it.
3. **Failed quotes** from `QUOTE_REPORT`: replace with the exact span from the text, or remove; fix wrong references.
4. **Renderings**: an English rendering that misreads the French (wrong sense, dropped negation, wrong referent). Correct it; don't polish style.
5. **Voices**: a cited author's view given as Fulcanelli's, Canseliet's as Fulcanelli's, or the reverse.
6. **Omissions**: a decoding, a definition or an operation of the Work that the text explains and the page leaves out. Add it briefly, with reference.
7. **Rights**: on a page whose rights tag is `pref_1`, `pref_2`, `pref_3` or `hendaye`, more than one short quote (one sentence) per section. Cut the extra quotes, keeping the summary.

Do not rewrite for style and don't remove supported content. Reply with only: the page path and a compact list of changes, grouped by the seven categories (omit empty ones).
