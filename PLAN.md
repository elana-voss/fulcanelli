# Plan — Fulcanelli, *Le Mystère des Cathédrales*

Briefing and fixed decisions: `HANDOFF.md` (sections 1, 2, 5). How to run: `RUNBOOK.md`. Rights: `RIGHTS.md`.

## Requirements (HANDOFF §1)
1. mdBook in English condensing the book, every claim referenced to the French source.
2. Two method pages in plain modern English, illustrated by the book's own veiled expressions: A, how Fulcanelli reads the monuments; B, the Great Work that reading describes.
3. One English lexicon: English headword, French original as the book spells it, how the rendering was derived.
4. One SillyTavern worldbook, English only, built by script from the lexicon.
5. Public/private split and rights per component enforced by script before any public render (`RIGHTS.md`).

## Milestones

| # | Milestone | Agents | Serves | Actual |
|---|---|---|---|---|
| 1 | Repos, extraction, witness corrections, chunking | — | 1–5 | done |
| 2 | Pilot of the Atwood method on 3 chunks (superseded) | 10 | — | 1.0M agent tokens |
| 3 | Part pages: 6 writers (Opus high), quote check, 6 checkers (Opus medium) | 12 | 1, 5 | 11 agents (Hendaye and Conclusion share writer and checker), 1.04M tokens; 225 quotes, 0 not found |
| 4 | Book synthesis (Opus medium), method pages A and B (Fable max), 3 checkers | 6 | 1, 2 | done; method B rewritten after the session limit; 8 agents; method pages 314 + 272 quotes, 0 not found |
| 5 | Lexicon: headword list (Opus high), 4 writer batches (Opus high), 4 checkers | 9 | 3 | done; 546 headwords in 6 batches (4 were too many for the output cap); 6 checkers + 1 restore agent (checkers given only cited paragraphs had removed true facts); 720 entry quotes, 0 not found |
| 6 | Plates page (Opus medium + script) | 1 | 1 | done |
| 7 | Worldbook by script; rights gate; mdBook build | — | 4, 5, 1 | done; 546 worldbook entries; gate passed; mdBook builds, 0 broken links |
| 8 | Public repo ready to publish | — | 5 | done; README; repos on GitHub (public and private); book built by GitHub Actions at https://elana-voss.github.io/fulcanelli/ |
| | Total | 28 + 10 | | |

## Decisions
- Driving question: both tracks A and B; two method pages, one per track (the owner, 2026-10-14).
- Method (the owner, 2026-10-14: "the book has only 70 pages … It has to differ from the Atwood approach"; plan accepted with "go"): no chunk readings; each writer reads whole parts of the French text and writes its page directly; a script checks every quote; one checker per page or batch.
- Rights gate counts each list item as its own point, as RIGHTS.md's "one short quote per point" (Claude).
- Worldbook: a work is keyed by its title as the book cites it (e.g. *Atalanta Fugiens*); our English title heads the entry (Claude).
