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
| 4 | Book synthesis (Opus medium), method pages A and B (Fable max), 3 checkers | 6 | 1, 2 | |
| 5 | Lexicon: headword list (Opus high), 4 writer batches (Opus high), 4 checkers | 9 | 3 | |
| 6 | Plates page (Opus medium + script) | 1 | 1 | |
| 7 | Worldbook by script; rights gate; mdBook build | — | 4, 5, 1 | |
| 8 | Public repo ready to publish | — | 5 | |
| | Total | 28 + 10 | | |

## Decisions
- Driving question: both tracks A and B; two method pages, one per track (the owner, 2026-10-14).
- Method (the owner, 2026-10-14: "the book has only 70 pages … It has to differ from the Atwood approach"; plan accepted with "go"): no chunk readings; each writer reads whole parts of the French text and writes its page directly; a script checks every quote; one checker per page or batch.
