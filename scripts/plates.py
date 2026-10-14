"""Plates page, by script.
  python plates.py extract  French captions (archive.org transcription) + citing paragraphs (chunks)
                            -> PRIVATE/work/plates/plates.json
  python plates.py render   plates.json + en.json ({plate: English caption}) -> PRIVATE/work/pages/12_Plates.md
Images are not shown (RIGHTS.md): the page links to the plate images on the blog named there."""
import glob, json, os, re, sys
import pymupdf
from paths import CHUNKS, PRIVATE, WITNESS_PDF, write

OUT = os.path.join(PRIVATE, 'work', 'plates')
BLOG = 'https://le-miroir-alchimique.blogspot.com/2015/03/fulcanelli-le-mystere-des-cathedrales.html'
ROMAN = re.compile(r'\b([IVXL]+)\b')


def extract():
    doc = pymupdf.open(WITNESS_PDF)
    plates = {}
    for page in doc:
        lines = [l.strip() for l in page.get_text().split('\n')]
        for j, l in enumerate(lines):
            m = re.fullmatch(r'(Planche ([IVXL]+)|Frontispice)', l)
            if not m: continue
            cap, k = [], j - 1
            while k >= 0 and lines[k] and not re.fullmatch(r'\d+|.*\)\.', lines[k]):
                cap.insert(0, lines[k]); k -= 1
            text = ''
            for c in cap: text += (' ' if c[:1].islower() else ' — ') + c if text else c
            plates.setdefault(m.group(2) or 'frontispiece', text.replace('PÖRCHE', 'PORCHE'))  # OCR slip
    refs = {p: [] for p in plates}
    for f in sorted(glob.glob(os.path.join(CHUNKS, '*.md'))):
        for m in re.finditer(r'^\[([^\]]+)\] (.*)$', open(f, encoding='utf-8').read(), re.M):
            for pl in re.findall(r'\(pl\.\s*([^)]*)\)', m.group(2)):
                for r in ROMAN.findall(pl):
                    if r in refs and m.group(1) not in refs[r]: refs[r].append(m.group(1))
    order = lambda p: (0, 0) if p == 'frontispiece' else (1, roman(p))
    data = [dict(plate=p, fr=plates[p], refs=refs[p]) for p in sorted(plates, key=order)]
    write(os.path.join(OUT, 'plates.json'), json.dumps(data, ensure_ascii=False, indent=1) + '\n')
    print(len(data), 'plates;', sum(1 for d in data if not d['refs']), 'not cited in the text')


def roman(s):
    v = dict(I=1, V=5, X=10, L=50); n = 0
    for a, b in zip(s, s[1:] + ' '):
        n += -v[a] if b in v and v[b] > v[a] else v[a]
    return n


def render():
    data = json.load(open(os.path.join(OUT, 'plates.json'), encoding='utf-8'))
    en = json.load(open(os.path.join(OUT, 'en.json'), encoding='utf-8'))
    L = ['# Plates', '', 'The plates of the book with their French captions and our English, and the passages that cite them. '
         f'The images are not reproduced here; they can be seen on [Le Miroir alchimique]({BLOG}).', '',
         '| Plate | French caption | English | Cited in |', '|---|---|---|---|']
    for d in data:
        name = 'Frontispiece' if d['plate'] == 'frontispiece' else f"pl. {d['plate']}"
        L.append(f"| {name} | {d['fr']} | {en.get(d['plate'], '')} | {', '.join(d['refs']) or '—'} |")
    write(os.path.join(PRIVATE, 'work', 'pages', '12_Plates.md'), '\n'.join(L) + '\n')
    print(len(data), 'plates rendered; missing English:', [d['plate'] for d in data if d['plate'] not in en] or 'none')


if __name__ == '__main__':
    {'extract': extract, 'render': render}[sys.argv[1]]()
