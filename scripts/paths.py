"""Repo paths. The private repo (source text, chunks, working files) is found via
env FULCANELLI_PRIVATE or config.json "private_root" (relative to this repo)."""
import os, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_cfg = json.load(open(os.path.join(ROOT, 'config.json'), encoding='utf-8'))
PRIVATE = os.path.normpath(os.environ.get('FULCANELLI_PRIVATE') or os.path.join(ROOT, _cfg['private_root']))
SOURCE_PDF = os.path.join(PRIVATE, 'Fulcanelli - Le Mystère des Cathédrales.pdf')
WITNESS_PDF = os.path.join(PRIVATE, 'Le Mystère des Cathédrales - archive.org transcription (2nd witness).pdf')
INPUT = os.path.join(PRIVATE, 'input')
CHUNKS = os.path.join(PRIVATE, 'chunks')


def write(path, text):
    """Write UTF-8 with LF line ends on every OS."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
