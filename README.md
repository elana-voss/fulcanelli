# Le Mystère des Cathédrales: an English Reading and Lorebook

An English digest of Fulcanelli's *Le Mystère des Cathédrales*, published as an mdBook, with a SillyTavern worldbook built from its lexicon. The French text is the only source: no outside knowledge about Fulcanelli, the monuments or alchemy, and no published translation was used. Quotations are in French, verbatim, with paragraph/footnote references and our own English.

Read the book online: <https://elana-voss.github.io/fulcanelli/>

## Contents

- `src/`: the book. One page per part, the book as a whole, how Fulcanelli reads the monuments and the Great Work that reading describes, each *in Plain Terms* (referenced) and *in Plain Language* (everyday words), the lexicon (English headword, the French form as the book spells it, how the English was arrived at) and the plate list.
- `lorebook/Fulcanelli_Mystere_des_Cathedrales.json`: the worldbook, English only, one entry per lexicon subject, keyed by the words a reader would type (English names, variants and spellings; persons also by surname; works by their cited and English titles). Import it in SillyTavern under World Info, Import.

## Rights

Fulcanelli's 1926 text is in the public domain. Canseliet's three prefaces and the Hendaye chapter are still protected: they are summarised in our words with at most one short quote per point. The plates are not reproduced. `RIGHTS.md` holds the register; `scripts/publish.py` refuses to build the book if a page breaks it.

## How it was made

The source text, its chunks and the agents' working files are in a private repository (`config.json` names its path). From it:

- `prompts/`: instructions for the writing and checking agents; `prompts/rules_core.md` holds the binding rules.
- `scripts/`: extraction, chunking, bundling, verbatim quote checks, lexicon and worldbook, plate list, rights gate and build.

Each page was written by one agent from the whole French part (or the whole book, for the method pages and lexicon), every quote was checked verbatim against the French by script, and a separate agent checked every page and lexicon batch; the Plain Language pages were checked sentence by sentence against the French by an independent reviewer against the source.

`PLAN.md`: requirements and decisions. `RUNBOOK.md`: how to run.
