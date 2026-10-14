"""Align the extracted main text (input/, Intro..Conclusion) with the archive.org
transcription (2nd witness) word by word; list small differences as candidates for
input/corrections.json. Output: PRIVATE/work/witness_diff.txt. Bodies and footnotes
are compared as separate streams (the witness has its notes inline in [...])."""
import re, json, os, difflib, unicodedata
import pymupdf
from paths import INPUT, WITNESS_PDF, PRIVATE, write

WORD = re.compile(r"[\w’'-]+")


def key(tok):
    """comparison form: ignore case, accents on capitals and in Greek, œ/æ ligatures"""
    d = unicodedata.normalize('NFD', tok)
    out, prev = '', ''
    for ch in d:
        if unicodedata.combining(ch) and (prev.isupper() or 'Ͱ' <= prev <= 'Ͽ'): continue
        out += ch; prev = ch
    return unicodedata.normalize('NFC', out).replace('œ', 'oe').replace('Œ', 'oe').replace('æ', 'ae').lower()


def toks(text):
    text = unicodedata.normalize('NFC', text).replace('’', "'")
    return WORD.findall(text)


def ours():
    secs = json.load(open(os.path.join(INPUT, 'sections.json'), encoding='utf-8'))
    body, notes = [], []
    for s in secs:
        if s['rights'].startswith('pref'): continue
        b = open(os.path.join(INPUT, s['file']), encoding='utf-8').read()
        n = open(os.path.join(INPUT, s['file'][:-4] + '_footnotes.txt'), encoding='utf-8').read()
        b = re.sub(r'\[\^\d+\]|\(\d{2,3}\)', ' ', b).replace('*', '')
        n = re.sub(r'^\[n\d+\]', ' ', n, flags=re.M).replace('*', '')
        body += [(t, s['id']) for t in toks(b)]
        notes += [(t, s['id']) for t in toks(n)]
    return body, notes


def witness():
    doc = pymupdf.open(WITNESS_PDF)
    lines = []
    for p in doc:
        for l in p.get_text().split('\n'):
            if re.fullmatch(r'\s*\d+\s*', l): continue           # page numbers
            lines.append(l)
    text = '\n'.join(lines)
    text = re.sub(r'-\n(?=[a-zà-ÿ])', '-', text)
    text = re.sub(r'(?<=\w)- (?=\w)', '-', text)
    notes = re.findall(r'\[([^\]]*)\]', text, re.S)
    body = re.sub(r'\[[^\]]*\]', ' ', text, flags=re.S)
    return toks(body), toks(' '.join(notes))


def report(a, b, label):
    sm = difflib.SequenceMatcher(None, [key(t) for t, _ in a], [key(t) for t in b], autojunk=False)
    out = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal' or max(i2 - i1, j2 - j1) > 3: continue
        ctx = ' '.join(t for t, _ in a[max(0, i1 - 4):i1])
        sid = a[min(i1, len(a) - 1)][1]
        out.append(f"{label} {sid:9} | {ctx} [[{' '.join(t for t, _ in a[i1:i2])}]] -> "
                   f"[[{' '.join(b[j1:j2])}]] | {' '.join(t for t, _ in a[i2:i2 + 3])}")
    return out, sm.ratio()


def main():
    ob, on = ours()
    wb, wn = witness()
    rb, ratio_b = report(ob, wb, 'BODY')
    rn, ratio_n = report(on, wn, 'NOTE')
    write(os.path.join(PRIVATE, 'work', 'witness_diff.txt'), '\n'.join(rb + rn) + '\n')
    print(f'body: {len(ob)} vs {len(wb)} words, ratio {ratio_b:.3f}, {len(rb)} small diffs; '
          f'notes: {len(on)} vs {len(wn)}, ratio {ratio_n:.3f}, {len(rn)} small diffs')


if __name__ == '__main__':
    main()
