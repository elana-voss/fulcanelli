"""Check every French quote «…» on a Markdown page: it must be verbatim in one of the paragraphs/footnotes
named by the next reference [REF; REF] in the same paragraph of the page (PRIVATE/chunks/ is the text).
Usage: python quote_check_doc.py PAGE.md [...]  -> report per page (also to PRIVATE/work/qc/<page>.txt)."""
import glob, os, re, sys
from paths import CHUNKS, PRIVATE, write
from quote_check import norm, segments

SEGS = {}
for f in glob.glob(os.path.join(CHUNKS, '*.md')):
    SEGS.update(segments(open(f, encoding='utf-8').read()))
QUOTE = re.compile(r'«([^»]+)»')
ONE = r'[A-Z0-9.]+ (?:¶|n)\d+'
REF = re.compile(rf'\[({ONE}(?:[;,] *{ONE})*)\]')


def check(page):
    text = open(page, encoding='utf-8').read()
    total, bad, misref = 0, [], []
    for m in QUOTE.finditer(text):
        total += 1
        end = text.find('\n\n', m.end())
        r = REF.search(text, m.end(), len(text) if end < 0 else end)
        q = m.group(1)
        nq = norm(q)
        refs = [x.strip() for x in re.split('[;,]', r.group(1))] if r else []
        if any(nq in SEGS.get(x, '') for x in refs): continue
        hit = [k for k, v in SEGS.items() if nq in v]
        if hit: misref.append(f'  wrong ref: {refs or "none"} -> found in {hit}: "{q[:70]}"')
        else: bad.append(f'  NOT FOUND {refs}: "{q[:90]}"')
    out = f'{page}: {total} quotes, {len(bad)} not found, {len(misref)} wrong ref\n' + '\n'.join(bad + misref) + '\n'
    write(os.path.join(PRIVATE, 'work', 'qc', os.path.basename(page)[:-3] + '.txt'), out)
    print(out.splitlines()[0])
    return not bad


if __name__ == '__main__':
    ok = [check(p) for p in sys.argv[1:]]
    sys.exit(0 if all(ok) else 1)
