# Fulcanelli project

- Requirements, milestones, account, decisions: `PLAN.md`. Original briefing: `HANDOFF.md`. How to run every step: `RUNBOOK.md`. Rights: `RIGHTS.md`.
- Private repo (source text, chunks, lexicon data): path in `config.json` (`../fulcanelli-private`).
- Build the book: `python scripts/publish.py` (rights gate + mdbook). Pushing `main` deploys to https://elana-voss.github.io/fulcanelli/.
- Worldbook: `python scripts/lex.py worldbook` reads `PRIVATE/work/lexicon/lexicon.json` and `scripts/worldbook_rules.json`, writes `lorebook/` and the report `PRIVATE/work/lexicon/worldbook_report.txt`; it fails on any broken check. `python scripts/lex.py fire "text"` lists the entries SillyTavern would trigger.
