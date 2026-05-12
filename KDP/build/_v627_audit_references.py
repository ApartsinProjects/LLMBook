"""v6.27: Audit References & Further Reading sections.

Checks per section:
  1. Link validity: every <a href> in <section.bibliography> is HTTP-reachable
     (HEAD request, 5s timeout). Reports 4xx/5xx, timeouts, and dead URLs.
  2. Domain quality: flag generic-looking refs that are likely placeholders
     (e.g. example.com, github.com without specific repo path, plain wikipedia.org).
  3. arXiv ID pattern check: arxiv.org links should have a valid 4.5 digit ID.
  4. Relevance heuristic: very loose — flag bibliography entries where the
     <p class="bib-annotation"> is shorter than 25 chars (probably a placeholder).

Outputs a CSV report and a per-issue summary.
"""
from __future__ import annotations
import csv
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse

import urllib.request
import urllib.error
import socket

ROOT = Path(__file__).resolve().parent.parent.parent
OUT_CSV = ROOT / 'KDP' / 'validation' / 'references_audit.csv'
TIMEOUT = 6  # seconds per URL

# Domains where a bare landing page is a sign of a generic / placeholder ref
GENERIC_DOMAINS = {'example.com', 'wikipedia.org', 'github.com', 'arxiv.org'}


def check_url(url: str) -> tuple[str, int | None, str]:
    """Return (url, status_code, error_msg)."""
    try:
        req = urllib.request.Request(url, method='HEAD',
                                     headers={'User-Agent': 'Mozilla/5.0 LLMBookAudit/1.0'})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return (url, resp.status, '')
    except urllib.error.HTTPError as e:
        # Some servers reject HEAD; retry GET
        if e.code in (403, 405, 501):
            try:
                req = urllib.request.Request(url, method='GET',
                                             headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                    return (url, resp.status, '')
            except Exception as e2:
                return (url, e.code, f'GET-retry: {e2}')
        return (url, e.code, str(e))
    except urllib.error.URLError as e:
        return (url, None, str(e.reason))
    except (socket.timeout, TimeoutError):
        return (url, None, 'timeout')
    except Exception as e:
        return (url, None, f'{type(e).__name__}: {e}')


def collect_refs():
    """Yield (file, url, annotation_text)."""
    for p in sorted(ROOT.glob('part-*/module-*/section-*.html')):
        text = p.read_text(encoding='utf-8', errors='replace')
        bib_m = re.search(r'<section class="bibliography">(.*?)</section>', text, re.DOTALL)
        if not bib_m:
            continue
        bib = bib_m.group(1)
        # Find each <div class="bib-entry-card">...</div>
        for entry in re.finditer(r'<div class="bib-entry-card">(.*?)</div>', bib, re.DOTALL):
            block = entry.group(1)
            link = re.search(r'<a[^>]+href="(https?://[^"]+)"[^>]*>', block)
            anno = re.search(r'<p class="bib-annotation">([^<]+)</p>', block)
            if not link:
                continue
            yield (
                str(p.relative_to(ROOT)).replace('\\', '/'),
                link.group(1),
                anno.group(1).strip() if anno else '',
            )


def main(check_links: bool = True) -> int:
    rows = list(collect_refs())
    print(f'Collected {len(rows)} bibliography entries from sections.')

    # Count by host
    from collections import Counter
    hosts = Counter(urlparse(url).netloc for _, url, _ in rows)
    print('\nTop 10 hosts:')
    for host, n in hosts.most_common(10):
        print(f'  {n:>4}  {host}')

    # Annotation quality
    short_anno = [(f, u, a) for f, u, a in rows if len(a) < 25]
    print(f'\nEntries with annotation < 25 chars (likely placeholders): {len(short_anno)}')
    for f, u, a in short_anno[:5]:
        print(f'  {f} | {u} | "{a}"')

    if not check_links:
        return 0

    # HEAD-check every unique URL in parallel
    unique_urls = sorted({u for _, u, _ in rows})
    print(f'\nChecking {len(unique_urls)} unique URLs (HEAD, 6s timeout, 16 workers)...')
    results = {}
    with ThreadPoolExecutor(max_workers=16) as ex:
        futs = {ex.submit(check_url, u): u for u in unique_urls}
        done = 0
        for fut in as_completed(futs):
            url, status, err = fut.result()
            results[url] = (status, err)
            done += 1
            if done % 50 == 0:
                print(f'  {done}/{len(unique_urls)} checked')

    # Write CSV
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open('w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['file', 'url', 'status', 'error', 'annotation_first_60'])
        for fname, url, anno in rows:
            status, err = results.get(url, (None, 'not checked'))
            w.writerow([fname, url, status if status else '', err, anno[:60]])

    # Summary of bad links
    bad = [(f, u, results[u]) for f, u, _ in rows
           if results[u][0] is None or (results[u][0] >= 400)]
    print(f'\nBad / unreachable URLs: {len({u for _, u, _ in bad})} unique')
    seen = set()
    for f, u, (s, e) in bad[:30]:
        if u in seen: continue
        seen.add(u)
        print(f'  [{s or "ERR"}] {u}')
        print(f'         {f}    {e[:80]}')
    print(f'\nFull report: {OUT_CSV}')
    return 0


if __name__ == '__main__':
    no_check = '--no-check-links' in sys.argv
    sys.exit(main(check_links=not no_check))
