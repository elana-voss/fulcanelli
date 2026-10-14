"""Lexicon and worldbook, by script.
  python lex.py batches N     headwords.json -> batch_1..N.json (balanced, in id order)
  python lex.py check FILE..  quote check of writer output out_K.json -> PRIVATE/work/qc/<name>.txt
  python lex.py render        headwords + out_*.json -> PRIVATE/work/pages/11_Lexicon.md + lexicon.json
  python lex.py worldbook     lexicon.json -> lorebook/Fulcanelli_Mystere_des_Cathedrales.json (English only)
Lexicon files live in PRIVATE/work/lexicon/."""
import glob, json, os, re, sys
from paths import CHUNKS, PRIVATE, ROOT, write
from quote_check import norm, segments

LEX = os.path.join(PRIVATE, 'work', 'lexicon')
load = lambda p: json.load(open(p, encoding='utf-8'))
dump = lambda p, d: write(p, json.dumps(d, ensure_ascii=False, indent=1) + '\n')


def batches(n):
    hw = load(os.path.join(LEX, 'headwords.json'))
    size = -(-len(hw) // n)
    for k in range(n):
        dump(os.path.join(LEX, f'batch_{k + 1}.json'), hw[k * size:(k + 1) * size])
    print(len(hw), 'headwords ->', n, 'batches of', size)


def check(paths):
    segs = {}
    for f in glob.glob(os.path.join(CHUNKS, '*.md')): segs.update(segments(open(f, encoding='utf-8').read()))
    ok = True
    for p in paths:
        out, total, bad = load(p), 0, []
        for i, e in out.items():
            for q in e.get('quotes', []):
                total += 1
                nq = norm(q['fr'])
                if nq in segs.get(q['ref'], ''): continue
                hit = [k for k, v in segs.items() if nq in v]
                bad.append(f"  {'wrong ref ' + str(hit) if hit else 'NOT FOUND'} {i} [{q['ref']}]: \"{q['fr'][:80]}\"")
        rep = f'{p}: {len(out)} entries, {total} quotes, {len(bad)} problems\n' + '\n'.join(bad) + '\n'
        write(os.path.join(PRIVATE, 'work', 'qc', os.path.basename(p)[:-5] + '.txt'), rep)
        print(rep.splitlines()[0]); ok &= not bad
    return ok


def render():
    hw = {h['id']: h for h in load(os.path.join(LEX, 'headwords.json'))}
    out = {}
    for p in sorted(glob.glob(os.path.join(LEX, 'out_*.json'))): out.update(load(p))
    missing = sorted(set(hw) - set(out))
    entries = []
    for i, h in hw.items():
        if i not in out: continue
        e = dict(h, **out[i]); e['id'] = i
        entries.append(e)
    entries.sort(key=lambda e: re.sub(r'^(the|a|an) ', '', e['en'].lower()))
    name = {e['id']: e['en'] for e in entries}
    L = ['# Lexicon', '', 'English headword, the French form as the book spells it, how the English was arrived at, '
         'and what the book says. References point to the French text (section ¶ paragraph, n footnote).', '']
    letter = None
    for e in entries:
        first = e['en'][:1].upper()
        if first != letter: L += [f'## {first}', '']; letter = first
        L += [f"### {e['en']} — *{e['fr']}* {{#{e['id']}}}", '', f"*{e['kind']}; {e['derivation']}*", '', e['body'], '']
        for q in e.get('quotes', []): L += [f"> «{q['fr']}» (*{q['en']}*) [{q['ref']}]", '']
        same = [f"[{name[s]}](#{s})" for s in e.get('same_as', []) if s in name]
        if same: L += ['Identified in the text with: ' + ', '.join(same), '']
    write(os.path.join(PRIVATE, 'work', 'pages', '11_Lexicon.md'), '\n'.join(L))
    dump(os.path.join(LEX, 'lexicon.json'), entries)
    print(len(entries), 'entries rendered; missing:', missing or 'none')


def worldbook():
    entries = load(os.path.join(LEX, 'lexicon.json'))
    strip = lambda s: re.sub(r'\s*\[[^\]]*(?:¶|n\d)[^\]]*\]', '', s).strip()
    wb = {'name': 'Fulcanelli — Le Mystère des Cathédrales',
          'description': 'Terms, persons, works and places of Fulcanelli\'s Le Mystère des Cathédrales, '
                         'as the book itself explains them (English).', 'entries': {}}
    for uid, e in enumerate(entries):
        names = [x.strip() for x in e['en'].split(' — ')]  # a work: title as cited — our English title
        head = names[-1]
        keys = names[:1]  # a work is typed by its title as cited, not by our translation
        if e['kind'] == 'term' and ' ' not in head and not head.endswith('s'): keys.append(head + 's')
        content = f"[{e['kind'].capitalize()}: {head}{f' ({names[0]})' if len(names) > 1 else ''}]\n{strip(e['body'])}"
        quotes = [q['en'] for q in e.get('quotes', [])]
        if quotes: content += '\n\nIn the book\'s words: ' + ' / '.join(f'“{q}”' for q in quotes)
        wb['entries'][str(uid)] = dict(uid=uid, key=keys, keysecondary=[], comment=f"{head} ({e['kind']}; {e['id']})",
                                       content=content, constant=False, selective=False, selectiveLogic=0,
                                       addMemo=True, order=100, position=1, disable=False, excludeRecursion=False,
                                       preventRecursion=False, delayUntilRecursion=False, probability=100,
                                       useProbability=False, depth=4)
    path = os.path.join(ROOT, 'lorebook', 'Fulcanelli_Mystere_des_Cathedrales.json')
    write(path, json.dumps(wb, ensure_ascii=False, indent=1) + '\n')
    print(len(wb['entries']), 'worldbook entries ->', path)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'batches': batches(int(sys.argv[2]))
    elif cmd == 'check': sys.exit(0 if check(sys.argv[2:]) else 1)
    elif cmd == 'render': render()
    elif cmd == 'worldbook': worldbook()
