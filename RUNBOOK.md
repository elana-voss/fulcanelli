# Run procedure (how to run and resume)

Requirements, milestones, account and decisions: `PLAN.md`. Original briefing: `HANDOFF.md`. Rights: `RIGHTS.md`. Private repo path: `config.json` (`private_root`, or env `FULCANELLI_PRIVATE`); every script reads it via `scripts/paths.py` and writes LF. `PRIVATE` below means that folder.

## Scripts
- Run from the public repo root as `python scripts/<name>.py` (not `python -I`: it drops `scripts/` from the import path and `paths.py` is not found). Needs PyMuPDF (`pip install pymupdf`).
- Extraction: `extract.py` → `PRIVATE/input/NN_<ID>.txt` (one paragraph per line, blank line between), `NN_<ID>_footnotes.txt` (`[nK] text`), `sections.json` (id, rights, PDF pages, counts). Prints acceptance checks; `-v` lists line-break hyphen joins. Paragraph breaks come from first-line indents; lines on the same baseline, lines starting lowercase and centred epigraph lines are joined.
- Corrections: `PRIVATE/input/corrections.json` (section, old, new), applied last by `extract.py`; each must match exactly once or it is reported. Generic typing artefacts (`Notre- Dame`, `l’ art`, Symbol-font ∆/µ, final ζ for ς, words split at an original page marker) are fixed by the `CLEAN` rules in `extract.py`.
- Witness check: `witness_diff.py` → `PRIVATE/work/witness_diff.txt` (word alignment of Intro–Conclusion against the archive.org transcription; small differences only).
- Chunking: `chunk.py` → `PRIVATE/chunks/<PART>_<nn>.md` + `index.json` (rights tag per chunk). Context: `context.py` → `PRIVATE/work/context/<id>.md`.

## Source format facts
- Markup in `input/` and chunks: italics `*…*` (the book's own emphasis); footnote markers `[^K]` numbered per section; original-edition page markers `(48)`…`(224)` inline (158 present; the source omits some, e.g. 59, 74, 88); plate refs `(pl. VI)`.
- Paragraph IDs `[PARIS.3 ¶5]` count per section; notes `[PARIS.3 n2]`. A chunk holds consecutive sections of one part; `### <section>` lines mark section starts inside a chunk.

## Stage 1 — chunk readings (state = files in `PRIVATE/work/`)
- Bundle per agent: `python scripts/bundle.py PRIVATE/work/bundles/<name>.md RULES=prompts/rules_core.md TASK=prompts/chunk_reader.md [RECONCILER=…|CHECKER=…] CHUNK=PRIVATE/chunks/<id>.md …` (reader adds `CONTEXT=PRIVATE/work/context/<id>.md`; reconciler adds `READING_A`, `READING_B`; checker adds `QUOTE_REPORT=PRIVATE/work/qc/<id>.R.txt` and edits the reading in place).
- Main text and Hendaye: readers A and B (Opus, high) → `readings/<id>.A/.B.json` → `qc_batch.py` → reconciler (Opus, high) → `readings/<id>.R.json` → `qc_batch.py` → copy to `final/<id>.json` → checker (Opus, medium, targeted Edits) → `qc_batch.py final/<id>.json` → `render_chunk.py final/<id>.json final/<id>.md`.
- Prefaces: one reader → `qc_batch.py` → copy to `final/` → checker → same.
- Agent prompt: read the bundle once (allow_large, offset if cut), read nothing else, one Write, no rewrite passes, no self-checking of quotes; reconcilers: keep thinking brief. At most 8 agents at once. An interrupted agent is resumed with SendMessage (its transcript is kept), not restarted.
- Done when every id in `chunks/index.json` has `final/<id>.json` with 0 quotes not found.
