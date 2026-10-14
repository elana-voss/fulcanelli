# Method Page — instructions

You write one of the two method pages of an English edition of Fulcanelli's *Le Mystère des Cathédrales*, from the whole French text. These pages are the primary deliverable: they state plainly, for a modern reader, what the book teaches under its veils, illustrated by the book's own expressions.

## Input
- `TEXT`: the whole book in French (prefaces, introduction, Paris, Amiens, Bourges, Hendaye, Conclusion), paragraphs marked `[PARIS.3 ¶12]`, footnotes `[PARIS.3 n2]`; each file's header gives its `rights:` tag.
- `RULES`: the binding rules. They bind you fully; above all, no outside knowledge and no decoding the text does not make.
- `TRACK`: which page you write (below).

## Track A — How Fulcanelli reads the monuments
What the key is and how it is used: the claim that the cathedrals are books in stone; *art gothique* / *argot*; the *langue des oiseaux* and phonetic cabala; etymology; how a carved or painted motif is read (what is looked at, in what order, what counts as evidence); numbers, colours, heraldry, inscriptions; who used this language and why it is veiled; where Fulcanelli declines to decode or warns against arbitrary reading. Organise by principle, each with the clearest worked examples from the text.

## Track B — The Great Work
The account of the Work the readings yield, as laboratory practice: the matter and its preparation, the solvent, the secret fire and the outer fire, the vessel and furnace, the operations in their order, the colours and other signs, proportions and times, the dry and humid ways, the result and its uses, and what is required of the worker. Organise in the order of the Work as far as the text allows; where the text leaves the order open or contradicts itself, say so.

## How to write
- Plain modern English, one claim at a time. Each step says whether the text **states** it (the text itself explains or identifies) or whether it is **interpreted** (your inference, with the passages it rests on). Where several readings are defensible, give each with its basis.
- Illustrate each point with Fulcanelli's own veiled expressions: verbatim French in « », our English in parentheses and italics, reference: `«le sceau canonique de l'Œuvre» (*the canonical seal of the Work*) [PARIS.3 ¶3]`. Quote format exactly as in RULES; write quotation marks inside a quote as “ ”.
- Every sentence that states something from the text ends with its reference in square brackets.
- Say what the text does not say: gaps, deliberate silences, points it declines to reveal.
- Canseliet's prefaces are a later layer in another voice: use them only in a final section "What Canseliet adds", labelled as his.
- Rights: from files tagged `pref_1`, `pref_2`, `pref_3` or `hendaye` use at most one short quote (one sentence) per point, otherwise your own words.
- Length: as long as the content needs; no padding, no repetition.

## Output
Write the page in Markdown once, with a single Write, to the path you are given; title `# <A or B>: <title of your own>`. No rewrite or compression passes, no checking of your own quotes (a script and a checker do that). Reply with only the path and the word count.
