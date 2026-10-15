"""Lexicon and worldbook, by script.
  python lex.py batches N     headwords.json -> batch_1..N.json (balanced, in id order)
  python lex.py check FILE..  quote check of writer output out_K.json -> PRIVATE/work/qc/<name>.txt
  python lex.py render        headwords + out_*.json -> PRIVATE/work/pages/11_Lexicon.md + lexicon.json
  python lex.py worldbook     lexicon.json + scripts/worldbook_rules.json -> lorebook/Fulcanelli_Mystere_des_Cathedrales.json
                              (English only) and worldbook_report.txt; exit 1 on a failed check
  python lex.py fire TEXT     entries SillyTavern would trigger on TEXT
Lexicon files live in PRIVATE/work/lexicon/."""
import glob, json, os, re, sys, unicodedata
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


def st_match(key, text):
    """SillyTavern's default key matching (world-info.js): case-insensitive, whole words, JS \\W (ASCII)."""
    if key.startswith('/') and key.rfind('/') > 0:
        end = key.rfind('/')
        return re.search(key[1:end], text, re.I if 'i' in key[end + 1:] else 0) is not None
    key, text = key.lower(), text.lower()
    if len(key.split()) > 1: return key in text
    return re.search(r'(?:^|\W)' + re.escape(key) + r'(?:$|\W)', text, re.A) is not None


ART = re.compile(r'^(?:the|a|an|some|these|those|our)\s+', re.I)
FR_ART = re.compile(r"^(?:(?:le|la|les)\s+|l['’])", re.I)
PLURAL_SKIP = ('s', 'x', 'z', 'ch', 'sh', 'y', 'f', 'fe', 'al', 'ed', 'ic', 'ous', 'ive', 'ism', 'ry', 'a', 'i', 'um')


def clean(c, kind, keep):
    """A candidate as keys: no brackets, split on ' / ' and ';', no leading article; unusable ones dropped."""
    out = []
    for c in re.split(r'\s+/\s+|;', re.sub(r'\s*\([^)]*\)', '', c)):
        c = c.strip()
        if c not in keep:
            c = ART.sub('', c)
            if kind == 'work': c = FR_ART.sub('', c)
        if re.search(r'[(),:;/"“”«»…]', c) or len(c) < 3 or c.isdigit() or len(c.split()) > 6: continue
        out.append(c)
    return out


def variants(k):
    """The key as typed on any keyboard: straight and curly apostrophes, no accents or ligatures."""
    out = [k, k.replace('’', "'"), k.replace("'", '’')]
    for v in out[:]:
        v = v.replace('’', "'").replace('œ', 'oe').replace('Œ', 'Oe').replace('æ', 'ae').replace('Æ', 'Ae')
        out.append(unicodedata.normalize('NFKD', v).encode('ascii', 'ignore').decode())
    return [v for v in out if len(v) >= 3]


def entry_keys(e, R, log):
    """Keys of one lexicon entry, before the redundancy pass (lorebook guide, section 4)."""
    keep, kind = set(R['article_keep']), e['kind']
    names = [x.strip() for x in e['en'].split(' — ')]  # a work: title as cited — our English title
    head = (clean(names[-1], kind, keep) or [names[-1]])[0]
    keys = [k for n in names for k in clean(n, kind, keep)]
    if kind != 'term':  # names and titles as the book spells them; French forms of terms are not keys
        keys += [k for f in e['forms'] for k in clean(f, kind, keep)]
    words = head.split()
    if kind == 'term' and len(words) == 1 and head not in R['no_plural'] and not head.lower().endswith(PLURAL_SKIP):
        keys.append(head + 's')
    if kind == 'person' and len(words) > 1 and words[0] not in ('Saint', 'King', 'Dr', 'Monsieur') \
            and not re.search(r'\b(of|the|and)\b', head) and len(words[-1]) >= 3:
        keys.append(words[-1]); log['surnames'].append(f"{e['id']} {head} -> {words[-1]}")
    everyday = set(R['everyday'])
    keys = [k for k in keys if k == head or k.lower() not in everyday]
    rule = R['entries'].get(e['id'], {})
    for r in rule.get('remove', []):
        if not any(k.lower() == r.lower() for k in keys): log['unused'].append(f"{e['id']} remove {r}")
        keys = [k for k in keys if k.lower() != r.lower()]
    keys += rule.get('add', [])
    return head, keys


def block(e, name):
    strip = lambda s: re.sub(r'\s*\[[^\]]*(?:¶|n\d)[^\]]*\]', '', s).strip()
    names = [x.strip() for x in e['en'].split(' — ')]
    c = f"[{e['kind'].capitalize()}: {names[-1]}{f' ({names[0]})' if len(names) > 1 else ''}]\n{strip(e['body'])}"
    quotes = [q['en'] for q in e.get('quotes', [])]
    if quotes: c += '\n\nIn the book\'s words: ' + ' / '.join(f'“{q}”' for q in quotes)
    same = [name[s] for s in e.get('same_as', []) if s in name]
    if same: c += '\n\nIdentified in the text with: ' + ', '.join(same)
    return c, strip(e['body'])


README = ('This lorebook holds the terms, persons, works and places of Fulcanelli\'s Le Mystère des Cathédrales, '
          'as the book itself explains them. Recommended SillyTavern World Info settings: Recursive Scan on, '
          'Max Recursion Steps 2-3; Match Whole Words on and Case-sensitive off (the defaults). '
          'This entry is disabled and never sent to the model.')


def worldbook():
    entries = load(os.path.join(LEX, 'lexicon.json'))
    R = load(os.path.join(ROOT, 'scripts', 'worldbook_rules.json'))
    name = {e['id']: e['en'].split(' — ')[-1] for e in entries}
    merged = {m: g[0] for g in R['merge'] for m in g[1:]}
    groups = {}
    for e in entries: groups.setdefault(merged.get(e['id'], e['id']), []).append(e)
    log = {'surnames': [], 'unused': []}
    base = dict(constant=False, addMemo=True, order=100, position=1, excludeRecursion=False, preventRecursion=False,
                delayUntilRecursion=False, probability=100, useProbability=False, depth=4)
    wb = {'name': 'Fulcanelli — Le Mystère des Cathédrales',
          'description': 'Terms, persons, works and places of Fulcanelli\'s Le Mystère des Cathédrales, '
                         'as the book itself explains them (English).',
          'entries': {'0': dict(base, uid=0, key=[], keysecondary=[], comment='READ ME', content=README,
                                selective=False, selectiveLogic=0, disable=True)}}
    bodies, report, merges = [], [], []
    for gid, members in groups.items():
        keys, contents, head = [], [], None
        for e in members:
            h, k = entry_keys(e, R, log)
            head, keys = head or h, keys + k
            c, b = block(e, name); contents.append(c); bodies.append((len(wb['entries']), e['id'], b))
        seen, ks = set(), []
        for k in keys:
            for v in variants(k):
                if v.lower() not in seen: seen.add(v.lower()); ks.append(v)
        ks = [k for k in ks if not any(len(s) < len(k) and st_match(s, k) for s in ks)]  # redundancy pass, last
        gated = head.lower() in R['everyday']
        own = {k.lower() for k in ks}
        uid = len(wb['entries'])
        comment = ' + '.join(f"{name[e['id']]} ({e['kind']}; {e['id']})" for e in members)
        if len(members) > 1: merges.append(comment)
        wb['entries'][str(uid)] = dict(base, uid=uid, key=ks, comment=comment, content='\n\n'.join(contents),
                                       keysecondary=[c for c in R['context'] if c.lower() not in own] if gated else [],
                                       selective=gated, selectiveLogic=0, disable=False)
        report.append(f"{comment} | {'GATED' if gated else 'open'} | {' ; '.join(ks)}")
    # checks (lorebook guide, section 9)
    keep, bad = set(R['article_keep']), []
    E = [e for e in wb['entries'].values() if not e['disable']]
    for e in E:
        if not e['key']: bad.append(f"no keys: {e['comment']}")
        for k in e['key']:
            if re.search(r'[(),/;:]', k): bad.append(f"punctuation: {k}")
            if ART.match(k) and k not in keep: bad.append(f"article: {k}")
            if any(len(s) < len(k) and st_match(s, k) for s in e['key']): bad.append(f"redundant: {k}")
        if e['selective'] and (not e['keysecondary'] or {k.lower() for k in e['key']} & {c.lower() for c in e['keysecondary']}):
            bad.append(f"gate: {e['comment']}")
    ids = {i for e in E for i in re.findall(r'\b(e\d{3})\)', e['comment'])}
    bad += [f"missing: {e['id']}" for e in entries if e['id'] not in ids]
    bad += [f"text changed: {i}" for uid, i, b in bodies if b not in wb['entries'][str(uid)]['content']]
    shared = {}
    for e in E:
        for k in e['key']: shared.setdefault(k.lower(), []).append(e['comment'].split(' (')[0])
    shared = {k: v for k, v in shared.items() if len(v) > 1}
    path = os.path.join(ROOT, 'lorebook', 'Fulcanelli_Mystere_des_Cathedrales.json')
    write(path, json.dumps(wb, ensure_ascii=False, indent=1) + '\n')
    rep = (['# Entries (comment | gate | keys)'] + report + ['', '# Merges'] + merges +
           ['', '# Automatic surnames'] + log['surnames'] + ['', '# Removes that matched no key'] + log['unused'] +
           ['', '# Keys shared by several entries'] + [f"{k}: {', '.join(v)}" for k, v in sorted(shared.items())] +
           ['', '# Failed checks'] + bad)
    write(os.path.join(LEX, 'worldbook_report.txt'), '\n'.join(rep) + '\n')
    nk = sum(len(e['key']) for e in E)
    print(f"{len(E)} entries, {nk} keys, {sum(e['selective'] for e in E)} gated, {len(merges)} merges, "
          f"{len(shared)} shared keys, {len(log['unused'])} unused removes, {len(bad)} failed checks -> {path}")
    return not bad


def fire(text):
    """Entries SillyTavern would trigger on text (no recursion)."""
    wb = load(os.path.join(ROOT, 'lorebook', 'Fulcanelli_Mystere_des_Cathedrales.json'))
    for e in wb['entries'].values():
        if e['disable'] or not any(st_match(k, text) for k in e['key']): continue
        if e['selective'] and not any(st_match(k, text) for k in e['keysecondary']): continue
        print(e['comment'])


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'batches': batches(int(sys.argv[2]))
    elif cmd == 'check': sys.exit(0 if check(sys.argv[2:]) else 1)
    elif cmd == 'render': render()
    elif cmd == 'worldbook': sys.exit(0 if worldbook() else 1)
    elif cmd == 'fire': fire(' '.join(sys.argv[2:]))
