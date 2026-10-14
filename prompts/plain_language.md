# Plain Language pages — instructions

Two pages, one per track, each made from its referenced page as Atwood's *The Method in Plain Language* was made from *The Method in Plain Terms*:

| Track | Referenced page (source and index) | Plain Language page (to write) | Title |
|---|---|---|---|
| A | `PRIVATE/work/pages/09_Method_A.md` | `PRIVATE/work/pages/09a_Monuments_Plain_Language.md` | Reading the Monuments in Plain Language |
| B | `PRIVATE/work/pages/10_Method_B.md` | `PRIVATE/work/pages/10a_Great_Work_Plain_Language.md` | The Great Work in Plain Language |

`PRIVATE` is `C:\Users\theco\ai\software\fulcanelli-private`. The binding rules are `prompts/rules_core.md` in the public repo (`C:\Users\theco\ai\software\fulcanelli`).

## 1. Goal

One Markdown page per track that states, for a modern reader:
- **A:** how Fulcanelli reads the monuments: what a reader needs before starting, and the reading itself, step by step.
- **B:** the Great Work the book describes: what a practitioner needs before starting, and the Work itself, step by step.

It must be:
- **In plain, modern English.** No special vocabulary of the book: no symbolic names, no technical or alchemical terms, no foreign-language words. Do not define terms either; describe the thing itself in everyday words. No glossary-style "X, i.e. Y". **One exception, page A only:** the method turns on French words that sound alike, so page A may show a few such French word pairs as the book's own examples (e.g. *gothique* heard in *argotique*), each followed at once by what the sound-play does, in English. No other French, and none on page B.
- **Without references.** No section, paragraph or footnote numbers, no citation brackets. The only pointer allowed is one sentence in the introduction naming the referenced page (*Reading the Monuments in Plain Terms* or *The Great Work in Plain Terms*) as the place where the passages are given.
- **Without quotations.** Say it in your own plain words.
- **From the book only.** No outside knowledge (history, art history, architecture, alchemy, chemistry, religion, psychology, scholarship), no speculation, no opinions of others presented as Fulcanelli's.
- **Honest about gaps.** Where the book leaves something open, withholds it or contradicts itself, say so plainly in the text, without references.

Length: about 3,500–4,500 words (Atwood's came out at about 3,900).

## 2. Inputs (read in this order)

1. **The referenced page of your track**, in full. It is the main source and the index to the passages. Note its labels: **Stated** / **Interpreted**, and the voice of each quote (Fulcanelli's own, `QUOTED: name`, endorsed or not, `UNCLEAR`, `CANSELIET`), and its section *What Canseliet adds* (the later layer).
2. **The part pages and the book synthesis**: `PRIVATE/work/pages/02_Introduction.md` … `07_Conclusion.md`, `08_Synthesis.md`. Use them where the referenced page is too compressed to see the plain meaning. For track B, also read the other track's referenced page where it helps, and vice versa.
3. **The French text itself**, in `PRIVATE/chunks/*.md`: one paragraph per line, each starting with its id (`[PARIS.3 ¶12]`, footnotes `[PARIS.3 n2]`); the `rights:` line names the layer. Go to it whenever a point is opaque and before writing any sentence whose voice or wording you are not sure of. Search by phrase or id with Grep. Check four things: who is speaking (Fulcanelli, or a cited author he reports); whether a hedge is present (*on dit*, *dit-on*, *semble*, *peut-être*, *sans doute*, *selon*, *si l'on en croit*, conditionals); what conditions are attached; what the surrounding context is.

Do not open the lexicon or anything else before you have this material in hand.

## 3. Writing rules (from the errors Atwood's review actually caught; apply them while writing)

1. **Base every point on Fulcanelli's own voice or on a view he clearly endorses.** If a point rests only on a quoted author he does not endorse, leave it out; if it is needed anyway, mark it in words ("the book quotes the view that…", "an old author whom Fulcanelli follows says…"). Check the voice in the French even where the referenced page labels it: labels can be wrong.
2. **Keep every hedge and condition.** "is said to" stays; "perhaps" stays; "if one believes the old masters" becomes "according to the old masters"; a condition stays a condition.
3. **Keep what the book means, not what you expect it to mean.** Do not reverse a relation, drop a limit, widen a statement about one stage, one monument or one author into a general rule, or move a remark about history or society into the practice.
4. **Add no connective reasoning the book does not make.** No "which is why", "so", "this means" unless the book itself draws that conclusion.
5. **Bring in no outside phrases** and do not identify old practices or things with modern equivalents.
6. **Do not fill in what the text leaves blank** (whose hand, which vessel, what the contact is with, who the subject is).
7. **Do not settle what the book leaves open.** Where it says two things, give both in plain words in the main text and list the point again in the closing section on what the book leaves open. Where the book itself relates the two sides, say how; do not call it open. Where Fulcanelli says he withholds something, say that it is withheld; do not guess it.
8. **Keep the later layer separate.** Canseliet's three prefaces are a later layer. Points resting only on them go in their own section near the end, not in the requisites or steps. Describe the layer only as the book does (the prefaces by Canseliet to the first, second and third editions), nothing more.
9. **Keep the order honest.** State which order the book gives firmly; say that the remaining steps follow the book's main line; where the book places a moment differently from your step order, say so in that step.
10. **Plain wording.** "You" for the requisites, plain descriptive sentences for the steps. Short paragraphs; bullets inside steps (how it is done, what happens, cautions, signs). No praise, no assessment of your own.

## 4. Page structure

Adapt the section names to the track, keep the order and the kinds of sections.

```
# <Title from the table>

<Intro paragraph: what the page is; from the French text only; no passage numbers, none of the
book's symbolic names (page A: except a few French sound-alike pairs, shown as the book's examples);
one sentence naming the referenced page for the passages; the book never gives the method as one
list and Fulcanelli withholds part of it, so the order follows the book's main line; open points
are said; Canseliet's prefaces are kept in their own section.>

## What the work is          (A: What the reading is)
  What is worked on / What does the work / What it is for   (3 short bold-led paragraphs;
  A: what is read / what reads it, or what key opens it / what it is for)

## What you need before you begin
### <subsections fitting the track, e.g. Understanding, Motive, Character, Practice>
  (numbered requisites, bold lead sentence + 1–4 sentences; numbering continuous)

## The method, step by step   (A: How a monument is read, step by step; B: The Work, step by step)
  <short paragraph: which order the book states firmly; the rest follows the main line>
### Step 1: …   (1 short paragraph, then bullets: How it is done / What happens / Cautions / Signs)
  …

## What it leads to          (bullets)
## The rules behind the whole work   (bullets: bold rule + 1 sentence)
## Mistakes and dangers      (bullets: bold mistake + 1–2 sentences)
## What Canseliet adds       (bullets; only the prefaces' own material)
## What the book leaves open (bullets: bold question + both sides in plain words)
```

## 5. Procedure (writer agent, reviewer agent, main session)

1. **Writer:** read the inputs (§2), verifying in the French every passage whose voice, hedge or context is unsure. Write the whole page once to its path (§1 table), following §3 and §4; reread it against §3 and §7 and fix anything obvious. Reply with only the path and the word count.
2. **Reviewer** (a separate agent that has not seen the writing): the prompt in §6. It writes its findings to `PRIVATE/work/plain/review_<A|B>_<pass>.md` and does not edit the page.
3. **Writer** (same agent, continued): for each finding, look at the quoted evidence in the French. Apply it if the book bears it out, otherwise leave the sentence. Reword only with wording the book supports; recheck every new sentence against §3. If a finding shows a wrong voice label in the referenced page, verify it in the French and fix it there by exact string replacement. Write one line per finding (applied / rejected + why; and any referenced-page fix) to `PRIVATE/work/plain/fixes_<A|B>_<pass>.md`. Reply with only the counts.
4. **Reviewer, second pass** (same agent, continued): the message in §6. Then the writer fixes again (step 3). Repeat while a pass finds substantive problems.
5. **Main session:** mechanical checks: no references left (regex for `¶`, section ids such as `PARIS.2`, footnote refs `n12`, square brackets), no `«`, word count; page B: no French words beyond names of places, monuments and persons; then the rights gate and book build (`scripts/publish.py`, which lists each Plain Language page right after its referenced page). Commit the two pages and the contents change together, with a message saying they were checked sentence by sentence against the French text by an independent reviewer; commit any fixes to the referenced pages separately, so they can be reverted on their own. Then delete `PRIVATE/TEMP_How_to_Write_the_Plain_Language_Method.md`.

## 6. Reviewer prompt (fill in the <…>)

```
You are an independent fact-checker. You have not seen this document being written. Your job is to check a draft page against the book it claims to summarize and report every problem. Do not edit the draft; report findings only.

## The draft to check
<absolute path of the page>

It restates, in plain modern English and without references or special vocabulary, <A: how Fulcanelli reads the monuments | B: the Great Work> as Fulcanelli sets it out in Le Mystère des Cathédrales: the requisites (what a <reader | practitioner> needs) and the <reading | Work> itself, step by step. <A: It may show a few French sound-alike word pairs as the book's own examples; that is allowed.>

## The source (the only permitted source)
- The book text, in French: C:\Users\theco\ai\software\fulcanelli-private\chunks\*.md — one paragraph per line, each starting with its id ([PARIS.3 ¶12] = section PARIS.3, paragraph 12; [PARIS.3 n2] = its footnote 2); the rights: line of each file names its layer (pref_1/2/3 = Canseliet's prefaces, a later layer; hendaye; main). Search by phrase or id with Grep.
- A referenced index to help you find passages fast: <referenced page path>. Its references use the same ids. Its labels say whose voice a quote is: Fulcanelli's own, QUOTED: name (a cited author; "endorsed" if adopted), CANSELIET, UNCLEAR; and Stated / Interpreted. Use it to locate passages, but verify against the French text, since the book is the authority. Also available: the part pages and synthesis C:\Users\theco\ai\software\fulcanelli-private\work\pages\02_Introduction.md … 08_Synthesis.md, and the binding rules C:\Users\theco\ai\software\fulcanelli\prompts\rules_core.md.

## What to check — every sentence of the draft
1. **Support.** Is the claim actually stated in the book? Flag anything not found, overstated, made more certain than the book is, or changed in meaning by the plain-language rewording (a hedge dropped, a reversed relation, a condition turned into a rule, a "said to be" turned into a fact).
2. **No speculation.** Flag any inference, interpretation, connecting "which is why"/"so" that the book does not itself make, or any filled-in detail. Where the referenced page or the part pages mark a point as Interpreted, the draft must not present it as plain fact.
3. **No outside sources.** Flag anything that seems to come from general knowledge of the subject, history, art history, religion, scholarship or modern psychology rather than from this book.
4. **No opinions of others.** The draft states Fulcanelli's method. Flag any point that rests only on a cited author whom Fulcanelli does not clearly endorse, if the draft presents it as his view or as part of the method.
5. **Voice and layer.** Flag misattribution (a quoted author's words given as Fulcanelli's, or the reverse; Canseliet's given as Fulcanelli's). Points in the main sections must not rest solely on Canseliet's prefaces; the section on what Canseliet adds must contain only the prefaces' material. Also flag any wrong voice label you notice in the referenced page.
6. **Plain language.** Flag any remaining reference, any quotation, and any special or symbolic vocabulary of the book used as jargon or explained as a glossary term. Ordinary English words in their ordinary sense are fine.
7. **Omissions that distort.** Flag only omissions that make a statement misleading, or a major requisite or step (as given in the referenced page) that is missing entirely.

## Output
Write the findings with a single Write to <PRIVATE\work\plain\review_X_1.md>: a numbered list, most serious first. For each: the exact draft sentence (quoted), the category (1–7), what is wrong, the evidence (a verbatim French quote with its id), and a concrete suggested rewording in plain English that the book supports (or "delete"). Be precise and exhaustive; do not pad with praise or with points that pass. If a sentence is fine, say nothing about it. End the file with a one-line count of findings by category. Reply with only that count line.
```

Second-pass message to the same reviewer:

```
Please do a second fact-check pass: the page at the same path has been revised in response to your findings (the writer's decisions are in <PRIVATE\work\plain\fixes_X_1.md>). Do two things: (1) for each of your earlier findings, confirm it is fixed or say what is still wrong (a rejection with a reason the French bears out counts as resolved); (2) check every sentence that is new or reworded with the same seven criteria, against the French text. Write only problems that remain or are new, in the same format, to <PRIVATE\work\plain\review_X_2.md>; if nothing remains, write one line saying so. Reply with only the count line.
```

## 7. Checklist of error kinds (Atwood's review)

- **Wrong voice:** a cited author's or "the philosophers'" words given as the author's; a name the author only sets beside his own term given as his own; a later-layer view given as his.
- **Dropped hedges:** "is said to", "probably", "if one believes", "more or less", "as we are taught".
- **Dropped conditions or limits.**
- **Over-generalising:** a remark about one author's book applied to all old writers; one stage's timing applied to all; a remark about society moved into the practice.
- **Reversed or shifted meaning; words read in the wrong sense.**
- **Filled-in details:** whose gaze, who the subject is, what the contact is with.
- **Imported phrases** from outside the book.
- **An open question settled, or a settled one called open.**
- **A later layer leaking into the main steps.**
- **Glosses presented as the text.**
- **Remaining jargon.**
