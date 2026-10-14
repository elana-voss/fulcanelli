# Plan — Fulcanelli, *Le Mystère des Cathédrales*

Briefing and fixed decisions: `HANDOFF.md` (sections 1, 2, 5, 6). How to run: `RUNBOOK.md`. Rights: `RIGHTS.md`.

## Requirements (HANDOFF §1)
1. mdBook in English condensing the book bottom-up (chunk → section → book), every claim referenced to the French source.
2. Two method pages in plain modern English, illustrated by the book's own veiled expressions: A, how Fulcanelli reads the monuments; B, the Great Work that reading describes.
3. One English lexicon: English headword, French original as the book spells it, how the rendering was derived.
4. One SillyTavern worldbook, English only, built by script from the lexicon.
5. Public/private split and rights per component enforced by script before any public render (`RIGHTS.md`).

## Milestones
Money is the API-price equivalent (Opus 5.5 $4/$20, Fable 5.1 $10/$50 per M input/output tokens; the owner runs on Claude Max), Claude's estimate from the pilot's measured agent tokens (1.0M tokens for 10 agent runs ≈ $5).

| # | Milestone | Serves | Estimate | Actual |
|---|---|---|---|---|
| 1 | Repos, extraction, witness corrections, chunking | 1–5 | 1.5 h, $5 | 1.3 h (16:05–17:25), session tokens not measured (est. $5) |
| 2 | Prompts and scripts adapted; pilot on INTRO_02, PARIS_02, PREF2_01 | 1–3 | 1.5 h, $8 | 0.5 h; 10 agent runs, 1.0M tokens (est. $5) + session (est. $3); in review |
| 3 | All 26 chunks read, reconciled, checked; quote check 0 not found | 1–3 | 2 h, $45 | |
| 4 | Section pages + per-part summaries for tracks A and B (writer + checker each) | 1, 2 | 1.5 h, $20 | |
| 5 | Book synthesis (Opus) and the two method pages (Fable max), each checked | 1, 2 | 1 h, $10 | |
| 6 | Lexicon: script extraction → merge (Fable max, exceptions only) → writer and checker batches → render | 3 | 2 h, $20 | |
| 7 | Worldbook by script; plates page; rights gate; full mdBook build | 4, 5, 1 | 2 h, $7 | |
| 8 | Public repo ready to publish: rights gate passes, mdBook builds, README | 5 | 1 h, $5 | |
| | Total | | 12.5 h, $120 | |

## Decisions
- Driving question: both tracks A and B; two method pages, one per track (the owner, 2026-10-14, answering "ok").
- Pilot findings (Claude's): readers keep every quote verbatim (0 of 332 quotes not found across the three final readings); the reconciler resolved real disagreements in both double-read chunks (stated vs interpreted, a decoding of `Χο` the text does not make, variants that were different words); the checkers removed outside knowledge in all three (e.g. "ankh" for the text's "ank", a gloss of the lamb "on crossed spits"). Notes run longer than 1 word per 5 of source (INTRO_02: 621 words for 2,064); kept, since nothing is padded.

## Questions for the owner
- Pilot review, double reading for all main-text chunks, and this milestone list with its total.
