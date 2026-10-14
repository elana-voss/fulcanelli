"""Per-chunk context: table of contents + last paragraph of the preceding chunk -> PRIVATE/work/context/<id>.md"""
import json, os, re
from paths import INPUT, CHUNKS, PRIVATE, write

TITLES = {'PREF1': 'Préface à la première édition (E. Canseliet, 1925)',
          'PREF2': 'Préface à la seconde édition (E. Canseliet, 1957)',
          'PREF3': 'Préface à la troisième édition (E. Canseliet, 1964)',
          'INTRO': 'Le Mystère des Cathédrales', 'PARIS': 'Paris', 'AMIENS': 'Amiens',
          'BOURGES': 'Bourges', 'HENDAYE': 'La Croix cyclique d’Hendaye', 'CONCL': 'Conclusion'}
secs = json.load(open(os.path.join(INPUT, 'sections.json'), encoding='utf-8'))
parts = {}
for s in secs: parts.setdefault(s['id'].split('.')[0], []).append(s['id'])
toc = '\n'.join(f"- {TITLES[p]}: {', '.join(ids)}" for p, ids in parts.items())
idx = json.load(open(os.path.join(CHUNKS, 'index.json'), encoding='utf-8'))
prev = None
for c in idx:
    doc = f"# Context for {c['chunk']}\n\n## Table of contents (section ids)\n\n{toc}\n\n## Last paragraph of the preceding chunk\n\n"
    if prev:
        body = open(os.path.join(CHUNKS, prev + '.md'), encoding='utf-8').read().split('## Footnotes')[0]
        paras = re.split(r'\n\n(?=\[)', body.strip())
        doc += f"(from {prev})\n\n{paras[-1].strip()}\n"
    else:
        doc += "(none: this is the first chunk of the book)\n"
    write(os.path.join(PRIVATE, 'work', 'context', c['chunk'] + '.md'), doc)
    prev = c['chunk']
print(len(idx), 'context files')
