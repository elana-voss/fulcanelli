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

## Pipeline (state = files in `PRIVATE/work/`)
- Bundle per agent: `python scripts/bundle.py PRIVATE/work/bundles/<name>.md RULES=prompts/rules_core.md TASK=prompts/<task>.md [CHECKER=prompts/<checker>.md] TEXT=<chunk files, comma-separated> [QUOTE_REPORT=PRIVATE/work/qc/<x>.txt]`. Bundles are not tracked; rebuild them with this command.
- Agent prompt: read the bundle once (allow_large, offset if cut), read nothing else, one Write, no rewrite passes, no self-checking of quotes. Checkers correct with targeted Edits. At most 8 agents at once. An agent whose final report fails after its Write has still written its file: check the file before rerunning.
- Part pages: `part_writer.md` (Opus, high) on the part's chunks → `pages/0N_<Part>.md` → `quote_check_doc.py` → `page_checker.md` (Opus, medium).
- Synthesis: `synthesis.md` (Opus, medium) on the part pages → `pages/08_Synthesis.md`; its checker gets the part pages as TEXT.
- Method pages: `method_page.md` (Fable, max) on all chunks, track A or B named in the agent prompt → `pages/09_Method_A.md`, `10_Method_B.md` → `quote_check_doc.py` → `page_checker.md` (Opus, medium) on all chunks.
- Lexicon (`lex.py`): `lex_list.md` (Opus, high) → `lexicon/headwords.json` → `lex.py batches 6` → `lex_writer.md` (Opus, high) per batch → `lexicon/out_K.json` → `lex.py check` → `lex_checker.md` (Opus, medium) on all chunks (a checker given only the cited paragraphs removed true facts stated elsewhere in the book) → `lex.py render` → `pages/11_Lexicon.md` → `lex.py worldbook` → `lorebook/`.
- Plates: `plates.py extract`, English captions in `plates/en.json`, `plates.py render` → `pages/12_Plates.md`.
- Public render: `python scripts/publish.py` runs the rights gate on every page, copies them to `src/`, writes `SUMMARY.md` and runs `mdbook build` (output `book/`, not tracked).
