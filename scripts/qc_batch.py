"""Quote-check readings: python qc_batch.py READING.json [...] -> PRIVATE/work/qc/<name>.txt, prints one line each."""
import io, os, re, sys, contextlib
import quote_check
from paths import CHUNKS, PRIVATE, write

for p in sys.argv[1:]:
    b = os.path.basename(p)[:-5]                       # PARIS_02.A  or  PARIS_02
    chunk = re.match(r'^(.*?_\d\d)', b).group(1)
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf): quote_check.check(os.path.join(CHUNKS, chunk + '.md'), p)
    except Exception as e:
        buf.write(f'{p}: ERROR {e}\n')
    write(os.path.join(PRIVATE, 'work', 'qc', b + '.txt'), buf.getvalue())
    print(buf.getvalue().splitlines()[0])
