"""Load .env.all (or .env) into os.environ.

Used by scripts that need GEMINI_API_KEY or other secrets. Idempotent.

Format: KEY=value lines, # comments, blank lines.
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_env(filename: str = ".env.all") -> int:
    """Load key=value pairs from <root>/<filename> into os.environ. Returns count loaded."""
    p = ROOT / filename
    if not p.exists():
        # Fallback: try .env
        p = ROOT / ".env"
        if not p.exists():
            return 0
    n = 0
    for raw_line in p.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' not in line:
            continue
        key, _, value = line.partition('=')
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value
            n += 1
    return n


if __name__ == '__main__':
    n = load_env()
    print(f'Loaded {n} env vars from .env.all')
    for k in sorted(os.environ):
        if k.endswith('_KEY') or k.endswith('_TOKEN') or 'API' in k:
            v = os.environ[k]
            masked = v[:4] + '...' + v[-4:] if len(v) > 12 else '***'
            print(f'  {k} = {masked}')
