"""Render a chunk reading JSON as readable Markdown. Usage: python render_chunk.py READING.json OUT.md"""
import json, sys
from paths import write


def q(text, en):
    return f"“{text}” — *{en}*" if en else f"“{text}”"


def r(path, out):
    d = json.load(open(path, encoding='utf-8'))
    L = [f"# {d['chunk']} ({d.get('rights', '')})", '', f"*{d.get('gist', '')}*", '', '## Argument', '']
    L += [f"- {n['point']} `{', '.join(n.get('refs', []))}` — {n.get('voice', '')}" for n in d.get('notes', [])]
    L += ['', '## A. Reading the monuments', '']
    for m in d.get('key', []):
        obj = f" — {m['object']}" if m.get('object') else ''
        L += [f"- **{m.get('device')}**{obj}: {q(m.get('veiled'), m.get('en'))} `{m.get('ref')}` ({m.get('voice')})",
              f"  - **Decoded ({m.get('status')}):** {m.get('decoded')}"]
        if m.get('basis'): L.append(f"  - Basis: {m['basis']}")
        for a in m.get('also') or []: L.append(f"  - Also: {q(a['text'], a.get('en'))} `{a['ref']}`")
    L += ['', '## B. The Work', '']
    for m in d.get('work', []):
        L += [f"- **{m.get('aspect')}**: {q(m.get('veiled'), m.get('en'))} `{m.get('ref')}` ({m.get('voice')})",
              f"  - **Plain ({m.get('status')}):** {m.get('plain')}"]
        if m.get('basis'): L.append(f"  - Basis: {m['basis']}")
        for a in m.get('also') or []: L.append(f"  - Also: {q(a['text'], a.get('en'))} `{a['ref']}`")
    L += ['', '## Terms', '']
    for t in d.get('terms', []):
        v = f" (also: {', '.join(t['variants'])})" if t.get('variants') else ''
        L.append(f"- **{t.get('en')}** — *{t.get('fr')}*{v} [{t.get('rendering')}: {t.get('rendering_basis')}] — {t.get('meaning')} ({t.get('voice')})")
        for e in t.get('equivalences', []): L.append(f"  - = {e['with']}: {q(e['quote'], e.get('en'))} `{e['ref']}`")
        for x in t.get('quotes', []): L.append(f"  - {q(x['text'], x.get('en'))} `{x['ref']}`")
    L += ['', '## Sources cited', '']
    for s in d.get('sources', []):
        w = f", *{s['work']}*" if s.get('work') else ''
        qq = f" — {q(s['quote'], s.get('en'))}" if s.get('quote') else ''
        L.append(f"- **{s['name']}**{w}{qq} `{', '.join(s.get('refs', []))}` — {s.get('use')}")
    if d.get('plates'):
        L += ['', '## Plates', '']
        L += [f"- pl. {p['plate']} `{p['ref']}` — {p.get('monument')}: {p.get('shows')}" for p in d['plates']]
    if d.get('ambiguities'):
        L += ['', '## Ambiguities', '']
        for a in d['ambiguities']:
            L.append(f"- {q(a['quote'], a.get('en'))} `{a['ref']}`")
            L += [f"  - Reading: {x}" for x in a.get('readings', [])]
            L.append(f"  - Basis: {a.get('basis')}")
    if d.get('translations'):
        L += ['', '## Translations', '']
        for t in d['translations']:
            fr = f" (book: “{t['book_fr']}”)" if t.get('book_fr') else ''
            L.append(f"- `{t['ref']}` “{t['original']}”{fr} → {t['en']} *({t.get('by', 'ours')})*")
    if d.get('threads'):
        L += ['', '## Threads', '']
        L += [f"- `{t['ref']}` {t['note']}" for t in d['threads']]
    write(out, '\n'.join(L) + '\n')


if __name__ == '__main__':
    r(sys.argv[1], sys.argv[2])
