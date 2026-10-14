"""PRIVATE/input/ sections -> PRIVATE/chunks/<PART>_<nn>.md + index.json.
Paragraph IDs per section ([PARIS.3 ¶5]); each footnote ([PARIS.3 n2]) goes with the
paragraph citing it. A chunk holds consecutive sections of one part (INTRO, PARIS, ...;
every preface and Hendaye are parts of their own, so a chunk has one rights tag);
it breaks at ~TARGET words of text, preferably at a section boundary."""
import re, json, os
from paths import INPUT, CHUNKS, write

TARGET, HARDMAX, SOFT = 2200, 3800, 1500    # words of text / text+notes / break at section start
wc = lambda s: len(s.split())

secs = json.load(open(os.path.join(INPUT, 'sections.json'), encoding='utf-8'))
paras = []                                   # dict(sec, n, text, notes=[(k, text)], part, rights)
problems = []
for s in secs:
    body = open(os.path.join(INPUT, s['file']), encoding='utf-8').read().strip().split('\n\n')
    notes = {}
    for l in open(os.path.join(INPUT, s['file'][:-4] + '_footnotes.txt'), encoding='utf-8'):
        m = re.match(r'\[n(\d+)\] (.*)', l)
        if m: notes[int(m.group(1))] = m.group(2)
    used = []
    for i, t in enumerate(body, 1):
        ks = [int(k) for k in re.findall(r'\[\^(\d+)\]', t)]
        used += ks
        paras.append(dict(sec=s['id'], n=i, text=t, notes=[(k, notes[k]) for k in ks],
                          part=s['id'].split('.')[0], rights=s['rights']))
    if sorted(used) != sorted(notes): problems.append(f"{s['id']}: note coverage")

groups, cur = [], []
for p in paras:
    if cur:
        tw = sum(wc(q['text']) for q in cur)
        nw = tw + sum(wc(t) for q in cur for _, t in q['notes'])
        add = wc(p['text']) + sum(wc(t) for _, t in p['notes'])
        if (p['part'] != cur[-1]['part'] or tw >= TARGET or nw + add > HARDMAX
                or (p['n'] == 1 and tw >= SOFT)):
            groups.append(cur); cur = []
    cur.append(p)
groups.append(cur)
for i in range(len(groups) - 1, 0, -1):     # merge a tiny tail into its predecessor of the same part
    g, h = groups[i - 1], groups[i]
    if g[0]['part'] == h[0]['part'] and sum(wc(q['text']) for q in h) < 500:
        groups[i - 1] = g + h; del groups[i]

os.makedirs(CHUNKS, exist_ok=True)
for f in os.listdir(CHUNKS):
    if f.endswith('.md'): os.remove(os.path.join(CHUNKS, f))
index, count = [], {}
for g in groups:
    part = g[0]['part']; count[part] = count.get(part, 0) + 1
    cid = f'{part}_{count[part]:02d}'
    body, prev = [], None
    for p in g:
        if p['sec'] != prev: body.append(f"### {p['sec']}"); prev = p['sec']
        body.append(f"[{p['sec']} ¶{p['n']}] {p['text']}")
    notes = [f"[{p['sec']} n{k}] {t}" for p in g for k, t in p['notes']]
    span = f"{g[0]['sec']} ¶{g[0]['n']} – {g[-1]['sec']} ¶{g[-1]['n']}"
    words_text = sum(wc(p['text']) for p in g); words_notes = sum(wc(t) for p in g for _, t in p['notes'])
    hdr = (f"---\nchunk: {cid}\nrights: {g[0]['rights']}\nspan: {span}\n"
           f"sections: {sorted(set(p['sec'] for p in g), key=[s['id'] for s in secs].index)}\n"
           f"footnotes: {len(notes)}\nwords_text: {words_text}\nwords_notes: {words_notes}\n---\n\n")
    doc = hdr + '## Text\n\n' + '\n\n'.join(body) + ('\n\n## Footnotes\n\n' + '\n\n'.join(notes) if notes else '') + '\n'
    write(os.path.join(CHUNKS, cid + '.md'), doc)
    index.append(dict(chunk=cid, part=part, rights=g[0]['rights'], span=span,
                      sections=sorted(set(p['sec'] for p in g), key=[s['id'] for s in secs].index),
                      paragraphs=len(g), footnotes=len(notes), words_text=words_text, words_notes=words_notes))
write(os.path.join(CHUNKS, 'index.json'), json.dumps(index, ensure_ascii=False, indent=1) + '\n')
if sum(len(g) for g in groups) != len(paras): problems.append('paragraph coverage')
for c in index: print(f"{c['chunk']:11} {c['rights']:8} {c['words_text']:5} +{c['words_notes']:4}  {c['span']}")
print(len(index), 'chunks;', 'problems:', problems or 'none')
