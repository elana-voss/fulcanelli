# Rights register

Decides what the public repo may contain. The pipeline's public renderers read the table below; the restricted rows are applied by script, never by agent judgement. Re-check this file before every public regeneration; when a "free from" date has passed, change the row to `free` and regenerate.

Public repo: summaries, analysis, lexicon, worldbook, short quotes. Private repo (`fulcanelli-private`): PDFs, extracted text, chunks, full-quote working files, plates.

## Status per component

| id | component | rights holder / basis | first published | protected until (FR) | protected until (US) | public use now |
|---|---|---|---|---|---|---|
| main | Fulcanelli's text (Intro, Paris, Amiens, Bourges, Conclusion) | pseudonymous, author never disclosed: L123-3 al. 1 | 1926 | expired 1 Jan 1997 | expired 1 Jan 2022 | free: quote as needed (French verbatim + our translation) |
| hendaye | La Croix cyclique d'Hendaye | pseudonymous, staggered publication: L123-3 al. 2 (own clock per element) | 1957, 2nd ed. (per Grok; not independently verified) | 31 Dec 2027 | 31 Dec 2052 (URAA; see note US) | restricted until 2053 |
| later_changes | any changes to the main text in the 1957/1964 editions | as hendaye | 1957 / 1964 | 31 Dec 2027 / 31 Dec 2034 | see note US | unknown: check by comparing against a 1926 witness |
| pref_1 | Canseliet, preface to the 1st ed. (Oct 1925) | named author, d. 1982: L123-1 life + 70 | 1926 | 31 Dec 2052 | expired 1 Jan 2022 | restricted |
| pref_2 | Canseliet, preface to the 2nd ed. (Aug 1957) | as pref_1 | 1957 | 31 Dec 2052 | see note US | restricted |
| pref_3 | Canseliet, preface to the 3rd ed. (Jul 1964) | as pref_1 | 1964 | 31 Dec 2052 | see note US | restricted |
| drawings | plate drawings, archive.org transcription (pl. I–XLIX + frontispiece; pairing and plate numbers in `fulcanelli-private/plates_check/pairs.json`) | Champagne (1877–1932), life + 70, for drawings proven his | 1926 (BnF: 36 plates) / later | expired for Champagne's | expired for Champagne's | **private for now** (user decision 2026-10-14). Public pages link to the plate images at <https://le-miroir-alchimique.blogspot.com/2015/03/fulcanelli-le-mystere-des-cathedrales.html> instead. Unresolved: BnF lists 36 plates for 1926, the set has 46 non-Hendaye plates; pl. XLVII–XLIX (Hendaye) are not 1926. Publish a drawing once its authorship is proven (1926 copy, facsimile or reliable plate list). |
| photos | 3rd-ed. photographic plates, mostly Pierre Jahan (d. 2003, per Grok, unverified) | life + 70 | 1964 | 31 Dec 2073 | see note US | never publish; link only to legitimate sources |
| sworder | English translation, Mary Sworder (1971; this edition © 1990) | translator / publisher | 1971 | protected | protected | never used, never given to any agent |

**Restricted** = in public output: summary and analysis in our own words; at most one short quote (one sentence) per point, French + our translation; no long passages. Enforced by a section tag on every chunk and a script check before public render.

**Free date rule:** a component becomes free on the later of its FR and US dates, because the public repo is hosted in the US (GitHub).

**Note US (our analysis, Grok concurs; not legal advice):** a French work first published 1927 or later and still protected in France on 1 Jan 1996 was likely restored in the US (URAA) for 95 years from publication: 1957 → end of 2052, 1964 → end of 2059. So `hendaye` stays restricted in the public repo until 1 Jan 2053, not 2028.

## Source law
CPI art. L123-3 (Légifrance, version in force 2026-10-14): pseudonymous/anonymous works, 70 years from 1 January after publication; staggered publication runs per element; if the author makes themselves known, L123-1/L123-2 (life + 70) applies.

## Clean-room rules
- Only the French text is a source. The English PDF is used only by the user to view plates; no agent reads it, nothing derived from its text enters the process.
- Plate numbers in the 3rd-ed. text and the archive.org transcription differ; plates are paired by eye (`fulcanelli-private/plates_check/`).

## Open items
- Establish which drawings are Champagne's (1926 copy, facsimile or reliable plate list; BnF says 36 plates); then switch those to public and replace the blog links with the images.
- Confirm `hendaye` publication year (1957) from a primary source (legal deposit / BnF catalogue).
- Check for 1957/1964 changes to the main text. Data point: the archive.org transcription (contains Hendaye, so a 1957 or later text) differs from our 3rd-ed. source in about 240 small wording variants besides typing slips (`fulcanelli-private/work/witness_diff.txt`, from `scripts/witness_diff.py`); if that transcription is the 1957 text, these are 1964 changes.
