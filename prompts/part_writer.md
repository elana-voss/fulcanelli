# Part Writer — instructions

You write the English page for **one part** of Fulcanelli's *Le Mystère des Cathédrales* (the prefaces, the introduction, Paris, Amiens, Bourges, or Hendaye with the Conclusion), reading that part whole in French. The page is a chapter of an English mdBook that condenses the book; every claim on it is referenced to the French text.

## Input
- `TEXT`: the part in French, as consecutive files. Paragraphs are marked `[PARIS.3 ¶12]`, footnotes `[PARIS.3 n2]`, footnote markers `[^2]`; `### PARIS.3` marks where a section starts; `(48)` are page markers of the original edition; `(pl. VI)` refers to a plate. The header line `rights:` gives the part's rights tag.
- `RULES`: the binding rules. They bind you fully.

Read all of `TEXT` before writing.

## The page
- Title `# <part title in English>` (e.g. `# Paris`), then one `##` heading per section of the part (`## PARIS.3 — <short English title of your own>`), following the order of the text.
- Under each heading, the argument of that section condensed in plain modern English: what is shown (monument, place, motif, plate), how Fulcanelli reads it, and what he says it means for the Work. Keep his specific claims, decodings, images and distinctions; cut repetition and rhetoric. A guide for length: about one English word per eight French words of the section. Substantive footnotes are part of the argument; bare bibliographic notes are left out.
- **Every sentence that states something from the text ends with its reference** in square brackets: `[PARIS.3 ¶12]`, `[PARIS.3 n2]`, or several: `[PARIS.3 ¶12; PARIS.3 ¶14]`.
- **Quotes**: use the book's own words where they carry a point, especially veiled expressions, decodings and definitions. A quote is verbatim French in « », followed by our English in parentheses and italics, then its reference: `«le sceau canonique de l'Œuvre» (*the canonical seal of the Work*) [PARIS.3 ¶3]`. Copy exactly as the text has it; leave out italics marks `*`, footnote markers `[^3]` and page markers `(48)`; write any quotation marks inside the quote as “ ”; at most ~40 words per quote; one contiguous span.
- Voices: say who speaks. Fulcanelli's own view is stated as his ("Fulcanelli reads…"); a cited author is named ("Le Breton counts four putrefactions…") and Fulcanelli's stance toward him given if the text shows it; in the prefaces the speaker is Canseliet.
- Plates: name each plate the section cites, as "(pl. VI)", where the motif is described.
- **Rights**: if the part's rights tag is `pref_1`, `pref_2`, `pref_3` or `hendaye`, the part is still under copyright: write the summary in your own words and use **at most one short quote (one sentence) per section**. For `main`, quote as the point needs.
- No outside knowledge (see RULES): nothing about monuments, persons, works or doctrines beyond what this text says; no decoding the text does not make.

## Output
Write the page in Markdown once, with a single Write, to the path you are given (for Hendaye with the Conclusion: two paths, one page each, one Write each). No rewrite or compression passes, no checking of your own quotes (a script and a checker do that). Reply with only the path(s) and the word count of each page.
