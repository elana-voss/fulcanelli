"""French source PDF -> PRIVATE/input/: one file per section (one paragraph per line,
blank line between), <id>_footnotes.txt ("[nK] text" per note), sections.json.

Column-aware: per page, lines left of the gutter, then right of it; elements that
straddle the gutter (headings, centred lines) cut the page into bands read in order.
Removed: running header/footer, cover page, ornaments. Kept: original-edition page
markers "(48)", plate refs "(pl. VI)", Greek. Italics -> *...*. Footnote markers
(superscript digits, numbered per page in the PDF) -> [^K], numbered per section.
Corrections (input/corrections.json, OCR slips found against the 2nd witness) are
applied last; each must match exactly as often as stated."""
import re, json, os, sys
import pymupdf
from paths import SOURCE_PDF, INPUT, PRIVATE, write

GUTTER, COLX, FOOTER_Y, INDENT = 300, (57, 305), 795, 8
MAJOR = [('PREMIÈRE', 'PREF1'), ('SECONDE', 'PREF2'), ('TROISIÈME', 'PREF3'),
         ('MYSTÈRE', 'INTRO'), ('PARIS', 'PARIS'), ('AMIENS', 'AMIENS'),
         ('BOURGES', 'BOURGES'), ('HENDAYE', 'HENDAYE'), ('CROIX', 'HENDAYE'),
         ('CONCLUSION', 'CONCL')]
RIGHTS = {'PREF1': 'pref_1', 'PREF2': 'pref_2', 'PREF3': 'pref_3', 'HENDAYE': 'hendaye'}
ROMAN = {r: i for i, r in enumerate('I II III IV V VI VII VIII IX X'.split(), 1)}


def kind(line):
    spans = [s for s in line['spans'] if s['text'].strip()]
    if not spans or all(s['font'].startswith('Wingdings') for s in spans): return None
    size = max(s['size'] for s in spans)
    if size >= 18: return 'head'
    if abs(spans[0]['size'] - 9) < .5: return 'foot'
    return 'body'


def runs_to_text(runs):
    """runs: (text, italic) with italic None for whitespace-only -> markdown string."""
    flags = [r[1] for r in runs]
    for i, f in enumerate(flags):            # whitespace inside an italic stretch stays italic
        if f is None:
            prev = next((flags[j] for j in range(i - 1, -1, -1) if flags[j] is not None), False)
            nxt = next((flags[j] for j in range(i + 1, len(flags)) if flags[j] is not None), False)
            flags[i] = bool(prev and nxt)
    merged = []
    for (t, _), f in zip(runs, flags):
        if merged and merged[-1][1] == f: merged[-1][0] += t
        else: merged.append([t, f])
    out = ''
    for t, f in merged:
        if f and t.strip():
            core = t.strip(); lead = t[:len(t) - len(t.lstrip())]; trail = t[len(t.rstrip()):]
            out += f'{lead}*{core}*{trail}'
        else: out += t
    return re.sub(r'\s+', ' ', out).strip()


def extract():
    doc = pymupdf.open(SOURCE_PDF)
    sections, order = {}, []                    # id -> dict(paras, notes, pages)
    major = sub = None
    para = None                                 # current paragraph runs
    cur_note = None                             # [section id, gid, runs]
    marker_ids = {}                             # (page, local n) -> (sec, gid)
    hyphen_joins, problems = [], []

    def sec():
        sid = f'{major}.{sub}' if sub else major
        if sid not in sections:
            sections[sid] = dict(paras=[], notes={}, pages=[], nmax=0); order.append(sid)
        return sections[sid]

    def flush():
        nonlocal para
        if para:
            t = runs_to_text(para)
            if t: sec()['paras'].append(t)
        para = None

    def add_line(runs, target):
        """append a line's runs to a paragraph/note run list, joining hyphenated breaks"""
        if target:
            last = ''.join(r[0] for r in target).rstrip()
            first = ''.join(r[0] for r in runs).lstrip()
            if last.endswith('-') and first[:1].islower():
                hyphen_joins.append(last[-15:] + '|' + first[:15])
                while target and not target[-1][0].strip(): target.pop()
                target[-1] = (target[-1][0].rstrip(), target[-1][1])
            else: target.append((' ', None))
        target.extend(runs)

    for pno, page in enumerate(doc, 1):
        if pno == 1: continue                   # cover
        lines = []
        for b in page.get_text('dict')['blocks']:
            if b['type']: continue
            for l in b['lines']:
                x0, y0, x1, _ = l['bbox']
                k = kind(l)
                if k is None or y0 >= FOOTER_Y: continue
                col = 'span' if x0 < GUTTER < x1 else (0 if x0 < GUTTER else 1)
                lines.append(dict(l=l, k=k, col=col, x0=x0, y0=y0))
        spans_ = sorted((d for d in lines if d['col'] == 'span'), key=lambda d: d['y0'])
        cuts = [d['y0'] for d in spans_]
        seq = []
        for band in range(len(cuts) + 1):
            lo = cuts[band - 1] if band else -1
            hi = cuts[band] if band < len(cuts) else 1e9
            for c in (0, 1):
                seq += sorted((d for d in lines if d['col'] == c and lo < d['y0'] < hi),
                              key=lambda d: (round(d['y0']), d['x0']))
            if band < len(cuts): seq.append(spans_[band])
        page_markers, prev_span, prev_y = 0, None, -100
        for d in seq:
            l, k = d['l'], d['k']
            text = ''.join(s['text'] for s in l['spans']).strip()
            if k == 'head':
                flush()
                up = text.upper()
                hit = next((sid for key, sid in MAJOR if key in up), None)
                if hit and hit != major: major, sub = hit, None
                elif text in ROMAN: sub = ROMAN[text]
                elif not hit: problems.append(f'p{pno}: unknown heading {text!r}')
                continue
            s = sec()
            if pno not in s['pages']: s['pages'].append(pno)
            colx = COLX[0] if d['col'] in (0, 'span') else COLX[1]
            if k == 'foot':
                m = re.fullmatch(r'(\d+)', text)
                if m and d['x0'] < colx + 6:
                    n = int(m.group(1))
                    if (pno, n) not in marker_ids:
                        problems.append(f'p{pno}: footnote {n} without marker')
                        sid0 = order[-1]; sections[sid0]['nmax'] += 1
                        marker_ids[(pno, n)] = (sid0, sections[sid0]['nmax'])
                    sid0, gid = marker_ids[(pno, n)]
                    cur_note = [sid0, gid, []]
                    sections[sid0]['notes'][gid] = cur_note[2]
                    continue
                if cur_note is None:
                    problems.append(f'p{pno}: footnote text without number: {text[:40]!r}'); continue
                runs = [(sp['text'], None if not sp['text'].strip() else bool(sp['flags'] & 2))
                        for sp in l['spans']]
                add_line(runs, cur_note[2])
                continue
            # body
            runs = []
            for sp in l['spans']:
                t = sp['text']
                if sp['size'] < 7 and t.strip():
                    if t.strip().isdigit():
                        s['nmax'] += 1
                        marker_ids[(pno, int(t.strip()))] = (order[-1], s['nmax'])
                        runs.append((f'[^{s["nmax"]}]', False)); page_markers += 1
                    else: runs.append((t.strip(), False))   # ordinal: XVIe, 1er
                    continue
                runs.append((t, None if not t.strip() else bool(sp['flags'] & 2)))
            if d['col'] == 'span':
                # centred epigraphs: a line continues the previous one when it starts no further
                # right and follows it closely; attributions (shifted right) and gaps break
                if not (prev_span and para is not None and d['x0'] <= prev_span[0] + 4
                        and d['y0'] - prev_span[1] < 20):
                    flush(); para = []
                prev_span = (d['x0'], d['y0'])
            elif (prev_span and para is not None and abs(d['x0'] - prev_span[0]) <= 4
                  and d['y0'] - prev_span[1] < 20):
                prev_span = (d['x0'], d['y0'])        # short last line of a centred epigraph
            elif para is not None and (abs(d['y0'] - prev_y) < 2 or text[:1].islower()):
                prev_span = None                      # same baseline as the previous line, or a lowercase start
            else:
                if prev_span or d['x0'] - colx >= INDENT or para is None:
                    flush(); para = []
                prev_span = None
            add_line(runs, para)
            prev_y = d['y0']
    flush()
    return sections, order, hyphen_joins, problems


GREEK = 'Ͱ-Ͽἀ-῿'
CLEAN = [  # typing artefacts of the source, fixed everywhere
    # word split at an original page break: syno- (110) nyme -> synonyme (110); Saint- (189) Esprit -> Saint-Esprit (189)
    (re.compile(r'(\w+)- (\(\d+\)) (\w+)'),
     lambda m: m[1] + ('-' if m[3][0].isupper() else '') + m[3] + ' ' + m[2]),
    (re.compile(r'(?<=\w)- (?=\w)'), '-'),                                   # Notre- Dame
    (re.compile(r"\b([lLdDnNsSjJmMtTcC]|[Qq]u|[Jj]usqu|[Ll]orsqu|[Pp]uisqu|[Qq]uoiqu)’ (?=\w)"), r'\1’'),  # l’ art
    (re.compile('∆'), 'Δ'), (re.compile('µ'), 'μ'),                          # Symbol-font code points
    (re.compile(''), '✮'),                                              # Wingdings star (rebus at AMIENS ¶40; witness has ✮)
    (re.compile(f'(?<=[{GREEK}])ζ(?![{GREEK}])'), 'ς'),                      # final sigma typed as zeta
]


def note_text(runs):
    return runs_to_text(runs)


def clean(text):
    for rx, rep in CLEAN: text = rx.sub(rep, text)
    return text


def main():
    sections, order, hyphen_joins, problems = extract()
    corr_path = os.path.join(INPUT, 'corrections.json')
    corrections = json.load(open(corr_path, encoding='utf-8')) if os.path.exists(corr_path) else []
    texts = {}
    for sid in order:
        s = sections[sid]
        notes = {g: note_text(r) for g, r in sorted(s['notes'].items())}
        texts[sid] = [clean('\n\n'.join(s['paras']) + '\n'),
                      clean(''.join(f'[n{g}] {t}\n' for g, t in notes.items()))]
        missing = set(range(1, s['nmax'] + 1)) - set(notes)
        if missing: problems.append(f'{sid}: markers without note text {sorted(missing)}')
    for c in corrections:
        sid, old, new, n = c['section'], c['old'], c['new'], c.get('n', 1)
        found = sum(t.count(old) for t in texts[sid])
        if found != n:
            problems.append(f'correction {sid} {old!r}: found {found}, expected {n}'); continue
        texts[sid] = [t.replace(old, new) for t in texts[sid]]
    index = []
    for i, sid in enumerate(order, 1):
        body, notes = texts[sid]
        base = f'{i:02d}_{sid}'
        write(os.path.join(INPUT, base + '.txt'), body)
        write(os.path.join(INPUT, base + '_footnotes.txt'), notes)
        index.append(dict(id=sid, file=base + '.txt', rights=RIGHTS.get(sid.split('.')[0], 'main'),
                          pdf_pages=[sections[sid]['pages'][0], sections[sid]['pages'][-1]],
                          paragraphs=body.count('\n\n') + 1, words=len(body.split()),
                          footnotes=sections[sid]['nmax']))
    write(os.path.join(INPUT, 'sections.json'), json.dumps(index, ensure_ascii=False, indent=1) + '\n')
    # acceptance checks
    alltext = ''.join(b + n for b, n in texts.values())
    if re.search(r'– \d+ –', alltext): problems.append('running header/page number left')
    pm = re.findall(r'\((\d{2,3})\)', ''.join(b for b, _ in texts.values()))
    pairs = json.load(open(os.path.join(PRIVATE, 'plates_check', 'pairs.json'), encoding='utf-8'))
    plates = {p for e in pairs['pairs'] for p in e['plates']} | set(pairs['drawings_without_photo'].values())
    refs = set()
    for m in re.finditer(r'\(pl\.\s*([^)]*)\)', alltext):
        refs |= set(re.findall(r'\b[IVXLC]+\b', m.group(1)))
    for sid in order: print(f"{sid:10} pages {index[order.index(sid)]['pdf_pages']} "
                            f"paras {index[order.index(sid)]['paragraphs']:3} words {index[order.index(sid)]['words']:5} "
                            f"notes {sections[sid]['nmax']}")
    print(f'page markers: {len(pm)} ({pm[0]}..{pm[-1]}); plate refs: {len(refs)}, unresolved: {sorted(refs - plates) or "none"}')
    print(f'hyphen joins: {len(hyphen_joins)}; corrections applied: {len(corrections)}')
    if '-v' in sys.argv: print('\n'.join(hyphen_joins))
    print('problems:', '\n'.join(problems) if problems else 'none')


if __name__ == '__main__':
    main()
