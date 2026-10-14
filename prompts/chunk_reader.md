# Chunk Reader — instructions

You are reading **one chunk** of Fulcanelli's *Le Mystère des Cathédrales* (French). The book reads Gothic cathedrals and other monuments as hermetic books in stone. Independent readers each handle one chunk; later stages build section summaries, two plain-language accounts (A: how Fulcanelli reads the monuments; B: the Great Work that reading describes), a lexicon and a worldbook, all from your output. What you miss is lost; what you invent poisons everything above you. You write in English; quotes stay French.

## Inputs
- `CHUNK`: header (chunk id, `rights` tag) and text. Paragraphs are marked `[PARIS.3 ¶12]`, footnotes `[PARIS.3 n2]`, footnote markers in the text `[^2]`; `### PARIS.3` marks where a section starts; `(48)` are page markers of the original edition; `(pl. VI)` refers to a plate.
- `CONTEXT`: the table of contents and the last paragraph of the preceding chunk. Context only — do not summarize it, do not take terms or claims from it.

Read the whole chunk, footnotes included, before writing anything.

## Output
Write **one JSON file** to the path you are given, valid UTF-8 JSON, exactly this shape (empty arrays are fine; don't pad):

```json
{
  "chunk": "PARIS_02",
  "rights": "main",
  "gist": "One or two sentences: what this chunk does in the book.",
  "notes": [
    {"point": "Condensed statement of one step of the argument.", "refs": ["PARIS.3 ¶12"], "voice": "FULCANELLI"}
  ],
  "key": [
    {
      "device": "sound | root | argot | image | number | rule",
      "object": "what is read: a word, a monument and its motif as the text names them (with plate, if any), or null",
      "veiled": "verbatim French span",
      "en": "our English rendering",
      "ref": "PARIS.3 ¶3",
      "decoded": "How the text reads it, in plain English: what stands for what, and why the text says so.",
      "status": "stated | interpreted",
      "basis": "Where the text supports this reading (refs + brief reason). Required for interpreted.",
      "voice": "FULCANELLI",
      "also": [{"text": "another verbatim span making the same point", "en": "...", "ref": "PARIS.3 ¶5"}]
    }
  ],
  "work": [
    {
      "aspect": "matter | solvent | agent | fire | vessel | operation | stage | sign | proportion | time | worker | result | principle",
      "veiled": "verbatim French span",
      "en": "our English rendering",
      "ref": "PARIS.3 ¶4",
      "plain": "What it means for the work, in plain modern terms.",
      "status": "stated | interpreted",
      "basis": "Required for interpreted.",
      "voice": "FULCANELLI",
      "also": [{"text": "...", "en": "...", "ref": "..."}]
    }
  ],
  "terms": [
    {
      "fr": "Corbeau",
      "variants": ["corbeau", "Tête de Corbeau"],
      "en": "Raven",
      "rendering": "literal | gloss | coined",
      "rendering_basis": "Why this English: literal translation of the French word; or the text's own gloss (cite ref); or our coinage because no literal English carries the sense (say why).",
      "meaning": "What the term means according to this chunk only.",
      "equivalences": [{"with": "couleur noire", "quote": "verbatim span asserting the identity", "en": "...", "ref": "PARIS.3 ¶4"}],
      "quotes": [{"text": "verbatim span", "en": "...", "ref": "PARIS.3 ¶4"}],
      "voice": "FULCANELLI"
    }
  ],
  "sources": [
    {"name": "as spelled in the text", "work": "title as given, or null", "quote": "short verbatim span attributed to it, or null", "en": "rendering of the quote, or null", "use": "What the text uses it for: supports / illustrates / contrasts / is criticized — and what point.", "refs": ["PARIS.3 n1"]}
  ],
  "plates": [
    {"plate": "VI", "ref": "PARIS.3 ¶3", "monument": "monument and place as the text names them", "shows": "what the text says the motif shows and means, in brief"}
  ],
  "ambiguities": [
    {"quote": "verbatim span", "en": "...", "ref": "PARIS.3 ¶15", "readings": ["reading A", "reading B"], "basis": "textual support for each"}
  ],
  "translations": [
    {"ref": "PARIS.3 ¶11", "original": "verbatim Latin/Greek/old-French passage", "book_fr": "the book's own French rendering, or null", "en": "our English rendering", "by": "ours"}
  ],
  "threads": [
    {"ref": "PARIS.3 ¶16", "note": "Points to something outside this chunk (\"comme nous l'avons dit\", \"nous verrons\") — what it points to, as stated."}
  ]
}
```

Copy `chunk` and `rights` from the chunk header.

### What goes where
- **notes**: the argument in order, condensed but complete, in English. Cover footnotes that carry substance; bare bibliographic references go only in `sources`. Length: at most 1 word of notes per 5 words of substantive source text (main text plus substantive footnotes), never more than 900 words. Keep the specific claims, images, monuments and distinctions; cut repetition instead.
- **key** (track A: how the text reads): every place where the text decodes a word, a name, an image or a carving, and every statement about how such reading works or why it is veiled.
  - `device`: `sound` (phonetic cabala, *langue des oiseaux*, puns, assonance), `root` (etymology the text gives), `argot` (slang, *langue verte*), `image` (a carved or painted motif read as a symbol), `number`, `rule` (a statement about the method of reading itself, its tradition, its users, why it is hidden).
  - `object`: the word or motif being read, e.g. "medallion of the raven, central porch, Notre-Dame de Paris (pl. VI)".
- **work** (track B: the Great Work): what the work is done on, with what solvent and agent, in what vessel, with what fire, by what operations and stages, with what signs (colours, appearances), proportions and times, what the worker needs, to what result. Include veiled images (raven, lion, salamander, dragon) when the text relates them to the work. A motif read for the work gets one entry in `key` (how it is read) and one in `work` (what it says about the work) only when both are substantive; otherwise one.
  - For both lists: **one entry per distinct point, not per sentence.** When several expressions make the same point, put the most telling one in `veiled` and the others in `also`.
  - **Prioritize decoding.** The most valuable entries are those where the text itself explains, glosses or identifies something. Never skip one of these.
  - A veiled image the chunk does not explain gets an entry only if it marks a recognizable step, sign or agent of the work; then say that this chunk does not explain it.
  - Typical result: 10–25 entries in each list; fewer when the chunk has fewer distinct points.
- **terms**: the specialized vocabulary (alchemical, symbolic, architectural, heraldic, and ordinary words used in a special sense), keyed by the French form the text uses. `en` is the English headword you propose; `rendering` says how you got it. Record identities the text asserts ("X, c'est-à-dire Y") in `equivalences`. `variants` holds only other spellings or forms of the same French word in this chunk; a different name for the same thing goes in `equivalences`, and only when the text asserts the identity. Persons and works go in `sources`, not here.
- **sources**: every author, work, inscription, scripture or tradition cited, including bare footnote references (then `use` is "reference only").
- **plates**: every `(pl. …)` reference in the chunk.
- **translations**: every non-French passage (Latin, Greek, old French verse or prose longer than a phrase).
- **threads**: cross-references the later section stage will need.

When done, reply with only: the output path and a one-line count (notes / key / work / terms / sources / plates / ambiguities).
