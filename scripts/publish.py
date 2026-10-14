"""Rights gate, then copy the finished pages into src/ and build the mdBook.
  python publish.py          gate PRIVATE/work/pages/*.md; on success copy to src/, write SUMMARY.md, run mdbook build
Gate (RIGHTS.md): a French quote whose reference lies in a restricted section (prefaces, Hendaye) must be one
sentence of at most 40 words, and there may be at most one such quote per paragraph or list item, and per heading block on the
restricted pages and the lexicon; no embedded images. Any violation fails the run and nothing is copied."""
import glob, os, re, shutil, subprocess, sys
from paths import PRIVATE, ROOT, write

PAGES = os.path.join(PRIVATE, 'work', 'pages')
SRC = os.path.join(ROOT, 'src')
RESTRICTED = re.compile(r'^(PREF\d|HENDAYE)\b')
PER_BLOCK = ('01_Prefaces.md', '06_Hendaye.md', '11_Lexicon.md')
QUOTE = re.compile(r'«([^»]+)»')
ONE = r'[A-Z0-9.]+ (?:¶|n)\d+(?:[–-]\d+)?'
REF = re.compile(rf'\[({ONE}(?:[;,] *{ONE})*)\]')
SUMMARY = [('Introduction', 'introduction.md'), None,
           ('Prefaces by Eugène Canseliet', '01_Prefaces.md'), ('The Mystery of the Cathedrals', '02_Introduction.md'),
           ('Paris', '03_Paris.md'), ('Amiens', '04_Amiens.md'), ('Bourges', '05_Bourges.md'),
           ('The Cyclic Cross of Hendaye', '06_Hendaye.md'), ('Conclusion', '07_Conclusion.md'), None,
           ('The Book as a Whole', '08_Synthesis.md'), ('A: How Fulcanelli Reads the Monuments', '09_Method_A.md'),
           ('B: The Great Work', '10_Method_B.md'), None, ('Lexicon', '11_Lexicon.md'), ('Plates', '12_Plates.md')]


def gate(path):
    text, name, problems = open(path, encoding='utf-8').read(), os.path.basename(path), []
    if re.search(r'!\[', text): problems.append('embedded image')
    for block in re.split(r'\n(?=#)', text):
        n_block = 0
        for para in re.split(r'\n\n|\n(?=[-*] |\d+\. )', block):  # a list item is its own point
            n_para = 0
            for m in QUOTE.finditer(para):
                r = REF.search(para, m.end())
                refs = re.split('[;,] *', r.group(1)) if r else []
                if not any(RESTRICTED.match(x) for x in refs): continue
                n_para += 1; n_block += 1
                q = m.group(1)
                if len(q.split()) > 40 or re.search(r'[.!?…] +[A-ZÀ-Ý«“]', q):
                    problems.append(f'restricted quote longer than one sentence: «{q[:60]}…»')
            if n_para > 1: problems.append(f'{n_para} restricted quotes in one paragraph: {para[:60]!r}')
        if name in PER_BLOCK and n_block > 1:
            problems.append(f'{n_block} restricted quotes under one heading: {block.splitlines()[0][:60]!r}')
    return problems


def main():
    files = sorted(glob.glob(os.path.join(PAGES, '*.md')))
    bad = {os.path.basename(f): p for f in files if (p := gate(f))}
    for f, ps in bad.items(): print(f, *ps, sep='\n  ')
    expected = {s[1] for s in SUMMARY if s and s[1] != 'introduction.md'}
    missing = expected - {os.path.basename(f) for f in files}
    if bad or missing:
        print('GATE FAILED' + (f'; missing pages: {sorted(missing)}' if missing else '')); sys.exit(1)
    for f in files: shutil.copy(f, os.path.join(SRC, os.path.basename(f)))
    lines = ['# Summary', '']
    for s in SUMMARY:
        lines.append('' if s is None else (f'[{s[0]}]({s[1]})' if s[1] == 'introduction.md' else f'- [{s[0]}]({s[1]})'))
    write(os.path.join(SRC, 'SUMMARY.md'), '\n'.join(lines) + '\n')
    print('gate passed;', len(files), 'pages copied')
    subprocess.run(['mdbook', 'build', ROOT], check=True)


if __name__ == '__main__':
    main()
