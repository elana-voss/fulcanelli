# Handoff — Fulcanelli, *Le Mystère des Cathédrales*

Written 2026-10-14 at the end of the planning session (Claude desktop app). This file is the complete briefing for the Claude Code session that runs the project. Read it fully, then `RIGHTS.md`, then the Atwood files named below. Nothing from the planning conversation is needed beyond this file.

## 0. Start here
1. **Confirm the driving question with the owner** (section 3). It is proposed, not yet approved. It shapes the reader prompt, the method track and the method page, so nothing agent-based starts before he confirms.
2. While waiting: do section 7 step 1 (repo setup) and step 2 (extraction). Both are script-only, no agents.
3. Then adapt the Atwood pipeline (section 6), run the pilot (3 chunks), and review it with the owner before the full run, exactly as in Atwood.

The owner is the product manager: he wants short, decision-level reports, conclusions first, no padding, no questions Claude can answer itself, no files he did not ask for (pipeline files are part of this job and fine). He is on Claude Max; usage is a real constraint (section 8).

## 1. Goal and deliverables
Process Fulcanelli's book the same way as Atwood's *A Suggestive Inquiry into the Hermetic Mystery* (`C:\Users\theco\ai\software\atwood`, published at <https://elana-voss.github.io/suggestive-inquiry/>):
1. An mdBook in English condensing the book bottom-up (chunk → section chapter → book), every claim referenced to the source.
2. The method page(s) answering the driving question (section 3), in plain modern English, illustrated by the book's own veiled expressions. Primary deliverable, as in Atwood.
3. **One English lexicon.** Each entry: English headword, **the French original term as the book spells it**, and a short note on how the English rendering was derived (literal, established English term, or our coinage, with the textual basis). Translating obscure terms is the hard part; the reader must see where a headword came from.
4. **One SillyTavern worldbook, English only**, built by script from the lexicon data (as Atwood's `dict_worldbook_v2.py`).

Output language: English. Source language: French.

## 2. Decisions already made (do not reopen)
- **The French text is the only source.** No outside knowledge about Fulcanelli, his identity, Canseliet, alchemy, the monuments, or later commentary. Same rule as Atwood (`atwood/prompts/rules_core.md`).
- **Clean room:** the English translation (Sworder) is never used: no agent reads it, no English wording from it enters any file. The English PDF exists in the private folder only so the owner can look at the photographic plates. Do not use it to check our translations either: that would import another person's interpretation.
- **Translations are ours,** made from the French, marked as ours.
- **Public/private split** (copyright, see `RIGHTS.md`): the public repo holds only our derived work (summaries, analysis, lexicon, worldbook, short quotes). Source text, chunks, full-quote working files, PDFs and plates live in the private repo.
- **Rights are enforced by script, per component** (`RIGHTS.md` table): Fulcanelli's 1926 main text is public domain (quote as in Atwood). The Hendaye chapter (first published 1957) and Canseliet's three prefaces are **restricted** in public output until 2053. Photographs: never published. Drawings: private for now; public pages link to <https://le-miroir-alchimique.blogspot.com/2015/03/fulcanelli-le-mystere-des-cathedrales.html> instead.
- **Plates:** pairing of drawings ↔ photographs and plate numbers (pl. I–XLIX + frontispiece) are done: `fulcanelli-private/plates_check/pairs.json`. Plate numbers come from the French captions of the archive.org transcription, never from the English PDF.
- **Worldbook English only; one lexicon (English with French originals).** Not two lexicons.
- The Atwood user decisions on the worldbook carry over unless the owner says otherwise: bias toward triggering over precision; keys are what a roleplayer would actually type; lexicon keeps research granularity, worldbook merges for everyday use; mechanical script edits over agent rewrites.

## 3. Driving question (PROPOSED — confirm with the owner first)
Atwood's book is about a method, so her driving question was the method. Fulcanelli's book is mainly an argument that the Gothic cathedrals are hermetic books in stone ("art gothique" = "art argotique"; the key is the phonetic cabala / *Langue des Oiseaux*, e.g. Christophe → Chrysophe). Through that reading he describes the operations of the Great Work as laboratory practice (matter, dissolvant, mercure, soufre, fire, voie sèche/humide, colours, vessel); the Conclusion addresses the disciple and the "manuel opératoire".

Proposed question, two tracks:
- **Track A — the key:** how does Fulcanelli decode the monuments (phonetic cabala, Langue des Oiseaux, argot, symbol and iconography reading)?
- **Track B — the Work:** what account of the Great Work does that reading yield (matter, solvent, fire, operations, stages, signs, requirements of the worker)?

Consequence for the pipeline: the reader records hints for both tracks (Atwood had one `method` list); two track summaries per section; two plain-language pages at the end (or one page with two parts — the owner's choice).

## 4. Folders and repos
- `C:\Users\theco\ai\software\fulcanelli` — **public repo** (to be created on GitHub). Contains: `HANDOFF.md`, `RIGHTS.md`, `PLAN.md`, `RUNBOOK.md`, `README.md`, `prompts/`, `scripts/`, `src/` (mdBook), `lorebook/`, `book.toml`, and only those parts of `work/` that hold our own derived output without long source quotes (decide per directory; when in doubt keep it private).
- `C:\Users\theco\ai\software\fulcanelli-private` — **private repo** (set to private on GitHub). Contains now:
  - `Fulcanelli - Le Mystère des Cathédrales.pdf` — **main source**: 3rd ed. (Pauvert), text layer, 70 pp., ~55,700 words incl. prefaces.
  - `Le Mystère des Cathédrales - archive.org transcription (2nd witness).pdf` — independent typed transcription (124 pp., ~47,700 words, no prefaces, includes Hendaye, French plate captions, 53 low-resolution drawings). Use only (a) as a second witness to catch OCR slips in the main source and (b) for plate captions. Not a source for content beyond that.
  - `Fulcanelli - The Mystery of the Cathedrals.pdf` — English (Sworder). **Never open in the pipeline.**
  - `plates_check/` — `pairs.json` (final pairing + plate numbers + provenance warning), `fr_1926_drawings/`, `en_pages/`, `block1_check.html` (the owner's check sheet; can go).
  - To be added: `input/`, `chunks/`, agent working files with full quotes, `work/bundles/`.
- Scripts in the public repo read the private repo by a configured path (e.g. env var or `config.json`: `PRIVATE_ROOT=../fulcanelli-private`). Atwood's scripts assume `chunks/` inside the repo; change that.
- Atwood reference: `C:\Users\theco\ai\software\atwood` (`PLAN.md`, `RUNBOOK.md`, `README.md`, `prompts/`, `scripts/`). Read `RUNBOOK.md` fully: it records every failure and fix (output-cap failure of a full-list merge agent, 8-agent parallel limit, exceptions-only outputs, bundle method).

## 5. Source facts (French main source)
- **Layout:** two columns with a clear gutter; reading-order extraction (`pdftotext` without `-layout`) works mostly but interleaves columns in places (seen in the Conclusion). Extract column-aware: per page, split at the gutter by x-coordinate (PyMuPDF `page.get_text("blocks")` / `"words"`, or `pdftotext -layout` and cut at the gutter column), left column then right column.
- **Remove:** running headers (`LE MYSTÈRE DES CATHÉDRALES`, `FULCANELLI`), page numbers (`– 12 –`).
- **Keep:** the inline original-edition page markers `(48)` … `(224)` (160 of them). They are the book's own pagination and useful in references.
- **Footnotes:** superscript digits inline in the text (extracted as plain digits glued to words, e.g. `Golfs1`, `Bigarne2`); the note texts sit at the foot of the column. Separate them into `_footnotes` files and attach to the citing paragraph, as Atwood's `chunk.py` does.
- **Plate references:** `(pl. XLIX)` etc. in the text; map to `pairs.json`.
- **Sections and PDF pages** (approximate, verify): Préface à la première édition p2; seconde édition p3; troisième édition p8; *Le Mystère des Cathédrales* (intro, I–IX) from p12; PARIS (I–VIII) p27; AMIENS p50; BOURGES (I–II) p56; LA CROIX CYCLIQUE D'HENDAYE p67; CONCLUSION p70 (ends "FIN DE L'OUVRAGE"). Heading letter-spacing in the PDF is irregular (`P RÉ F AC E …`).
- **Known OCR slips** (examples): `p|us`, `Fulcanellli`, `ellemême`, `pourrionsnous` (lost hyphens at line breaks), `soi` for `soit`. Fix by diffing against the 2nd witness: align word sequences (difflib), list differences, apply only obvious slips. Store corrections as data (`input/corrections.json`, applied by script) so the extraction is reproducible.
- **Greek** passages exist (e.g. `Χρυσοϕορος`); keep as is.
- **French typography for quote checks:** normalise to NFC, treat `’`/`'` and non-breaking/thin spaces before `; : ! ?` and inside `« »` as equal, keep `œ`/`æ` ligatures. Atwood's `quote_check*.py` were written for English; adapt the normaliser.
- Size: ~55,700 words incl. prefaces → about 23–25 chunks at Atwood's chunk size (Atwood: 81 chunks, ~197k words).

## 6. Pipeline: reuse from Atwood
Same architecture: **one bundle per agent** (`scripts/bundle.py`: rules + task prompt + inputs in one file; agent prompt says "read the bundle once, read nothing else, write once"), files as state, scripts for everything mechanical, a separate checker agent per output, verbatim quote check by script. Subagents run via Claude Code's Agent tool with the model and effort from the table below; max 8 in parallel.

| Atwood file | Fulcanelli |
|---|---|
| `prompts/rules_core.md` | adapt: source-only rule names Fulcanelli; voices `FULCANELLI` / `QUOTED: <name>` / `CANSELIET` (prefaces) / `UNCLEAR`; quotes verbatim **French**, each with an English rendering `by: "ours"` (no book translation exists); references (section IDs below); footnotes; rights tag of the chunk carried on every item |
| `prompts/chunk_reader.md` | rewrite method part for tracks A and B; keep notes/terms/sources/ambiguity sections; term candidates carry the French form |
| `reconciler.md`, `checker.md`, `doc_checker.md` | adapt names, voices, French quotes |
| `chapter_writer.md`, `chapter_method.md` | adapt: section chapters; method summary per track |
| `part_writer.md`, `part_method.md` | probably not needed (no Parts); book synthesis directly from section chapters |
| `book_writer.md`, `method_statement.md` | adapt to two tracks |
| `dict_merge.md`, `dict_writer.md` | adapt: entry = English headword + French original + derivation note + body |
| `scripts/chunk.py` | rewrite input side (new file naming, headings); keep paragraph IDs, footnote attachment, ~2.2k-word target |
| `scripts/bundle.py`, `context.py`, `qc_batch.py`, `render_chunk.py` | reuse; private path |
| `scripts/quote_check.py`, `quote_check_doc.py` | adapt normaliser (section 5), private path |
| `scripts/dict_*.py`, `lexicon_rules.json` | reuse structure; `lexicon_rules.json` is Atwood-specific editorial data — start empty; worldbook keys English |
| new: `scripts/extract.py` | PDF → `input/` (column split, header removal, footnotes, page markers, corrections) |
| new: public-render gate | before any public render: every quote's rights tag checked against `RIGHTS.md`; restricted = summary + at most one short quote (one sentence) per point; drawings/photos not embedded; fail the render on violation |

**Section IDs** (proposal): `PREF1`, `PREF2`, `PREF3`, `INTRO` (Le Mystère des Cathédrales I–IX → `INTRO.1`…`INTRO.9`), `PARIS.1`…`PARIS.8`, `AMIENS`, `BOURGES.1`, `BOURGES.2`, `HENDAYE`, `CONCL`. References `PARIS.3 ¶12`, notes `PARIS.3 n2`; the original page marker may be added (`p. 87`).

**Rights tags per section:** `PREF1–3` → pref_1..3 (restricted), `HENDAYE` → hendaye (restricted), all others → main (free). The prefaces are a later layer in Canseliet's voice — treat like Atwood's Appendix: read and summarised, labelled, kept apart from Fulcanelli's voice.

**Models and effort** (Atwood's, unchanged):

| Step | Model | Effort |
|---|---|---|
| Chunk readers, reconciler | Opus | high |
| Checker | Opus | medium |
| Section / book synthesis | Opus | medium |
| Method statement(s), dictionary merge | Fable (fallback Opus high, same prompt) | max |
| Dictionary writers | Opus | high |
| Quote check, worldbook, lexicon render, rights gate | script | — |

**Double reading:** Atwood used two readers + reconciler for its hardest parts; the pilot showed clearly better results. Proposal for Fulcanelli: double reading for all main-text chunks (≈ 20 chunks → still far fewer agent runs than Atwood), single reader for the prefaces. Confirm with the owner at the pilot review.

**mdBook `src/` (proposal):** introduction; one page per section (INTRO, PARIS, AMIENS, BOURGES, HENDAYE, CONCL; PARIS may need several pages); prefaces page (restricted); book synthesis; method page(s) for tracks A and B; lexicon; plates page (list of plates with French captions, our English rendering, the passages that cite them, link to the blog images).

## 7. Steps
1. **Repo setup.** `git init` both folders; `.gitignore` in public repo excludes anything with source text; `.gitattributes` LF as in Atwood. The owner creates the GitHub repos (public / private).
2. **Extraction** (`scripts/extract.py`): French PDF → `fulcanelli-private/input/` one file per section + `_footnotes`. Diff against the 2nd witness, write `input/corrections.json`, re-run. Acceptance: no running headers/page numbers left; column order correct (spot-check the Conclusion and 3 random pages); footnote count per section plausible; all `(pl. …)` refs resolvable in `pairs.json`.
3. **Chunking** (`chunk.py` adapted) → `fulcanelli-private/chunks/` + `index.json`; rights tag per chunk.
4. **Adapt prompts** (section 6) after the owner confirms the driving question.
5. **Pilot:** 3 chunks — suggestion: one INTRO chunk (Langue des Oiseaux / argot — track A), one PARIS porch chunk (medallions — track B), and `PREF2` (Canseliet voice, restricted). Double reading where planned, checker, quote check. **Review with the owner**; fix formats before the full run.
6. **Full run:** chunks → section chapters + track summaries → book synthesis → method page(s) → dictionary (extract by script → merge Fable max, exceptions-only output → packets → writer batches → checker) → lexicon render → worldbook by script.
7. **Public render** through the rights gate; mdBook build; the owner publishes.
8. Keep `RUNBOOK.md` current after every stage (state, how to resume), as in Atwood.

## 8. Usage and token rules (the owner's standing rules)
- Before launching any agent: estimate its input and output tokens; output including thinking must stay well under the 64k per-agent cap. Design compact outputs (exceptions/deltas; scripts do the rest).
- Find savings before spending, never by lowering quality. After a failure, never rerun the same expensive setup unchanged.
- From Atwood: every agent prompt says read the bundle once, write once, no rewrite or compression passes, no self-verification of quotes (script + checker do that). Length targets are guides, not reasons to rewrite. A merge agent asked for a full entry list hit the output cap — ask for exceptions only. Max 8 agents in parallel (a 24-wide wave hit the session limit).
- This session runs locally on Windows in VS Code, so files are edited directly; Atwood's staging/commit steps (`device_stage_files`, tgz syncs) are not needed. Scripts must write LF on every OS.

## 9. Open items (also in `RIGHTS.md`)
- Driving question: the owner to confirm (section 3).
- Double reading scope: confirm at pilot review.
- Drawings: which are Champagne's 1926 plates (BnF record: 36 plates; our set has 46 non-Hendaye plates). Until proven: private, link to the blog.
- Possible changes to Fulcanelli's main text in the 1957/1964 editions (would be restricted like Hendaye): only checkable against a 1926 witness.
- Hendaye first-publication year (1957): from Grok, not verified against a primary source.
