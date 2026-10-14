# Run procedure (state and how to resume)

Plan and decisions: `HANDOFF.md`. Rights: `RIGHTS.md`. Private repo path: `config.json` (`private_root`, or env `FULCANELLI_PRIVATE`); every script reads it via `scripts/paths.py` and writes LF.

## How to run
- Run scripts from the public repo root as `python scripts/<name>.py` (not `python -I`: it drops `scripts/` from the import path and `paths.py` is not found). Needs PyMuPDF (`pip install pymupdf`).
- Extraction: `python scripts/extract.py` → `PRIVATE/input/NN_<ID>.txt` (one paragraph per line, blank line between), `NN_<ID>_footnotes.txt` (`[nK] text`), `sections.json` (id, rights, PDF pages, counts). Prints acceptance checks; `-v` lists line-break hyphen joins.
- Corrections: `PRIVATE/input/corrections.json` (section, old, new), applied last by `extract.py`; each must match exactly once or it is reported. Generic typing artefacts (`Notre- Dame`, `l’ art`, Symbol-font ∆/µ, final ζ for ς, words split at an original page marker) are fixed by the `CLEAN` rules in `extract.py`.
- Witness check: `python scripts/witness_diff.py` → `PRIVATE/work/witness_diff.txt` (word alignment of Intro–Conclusion against the archive.org transcription; small differences only).
- Chunking: `python scripts/chunk.py` → `PRIVATE/chunks/<PART>_<nn>.md` + `index.json` (rights tag per chunk).

## Source format facts
- Text markup in `input/` and chunks: italics `*…*` (the book's own emphasis, kept); footnote markers `[^K]` numbered per section; original-edition page markers `(48)`…`(224)` inline (158 present; the source omits some, e.g. 59, 74, 88); plate refs `(pl. VI)`.
- Paragraph IDs `[PARIS.3 ¶5]` count per section; notes `[PARIS.3 n2]`. A chunk holds consecutive sections of one part; `### <section>` lines mark section starts inside a chunk.

## State 2026-10-14
- Done: repo setup (both repos `git init`, LF); extraction (25 sections, 0 problems: no headers/page numbers left, column order confirmed by the witness alignment, all footnote markers matched, all 49 plate refs resolve in `pairs.json`); 90 slip corrections (only obvious typing errors the witness confirms; wording variants between the editions are left as the 3rd ed. has them); chunking (26 chunks: 5 preface, 20 main, 1 Hendaye; ~2.2k words each).
- Waiting: the owner's confirmation of the driving question (HANDOFF §3) and one or two method pages.
- Next: adapt prompts (HANDOFF §6) and `bundle.py`, `context.py`, `qc_batch.py`, `quote_check*.py`, `render_chunk.py` from Atwood; then the pilot (HANDOFF §7 step 5).
