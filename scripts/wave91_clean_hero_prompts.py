"""Wave 91: Clean the leaked image-generation prompt from chapter-opener
figures.

Many chapter / module index pages have a hero illustration whose alt text
and figcaption were filled with the literal AI-image-generation prompt,
typically split at the prompt's max-alt-length boundary. Example:

  <figure class="illustration chapter-opener">
    <img alt="Warm cartoon-style hero illustration introducing chapter
      'Compute Planning &amp; Inf"
         aria-describedby="long-desc-44"/>
    <figcaption id="long-desc-44">rastructure', a Kurzgesagt-meets-XKCD
      visual metaphor with friendly characters and clear iconography,
      capturing the theme: Sizing infrastructure for the workload you'll
      actually run.</figcaption>
  </figure>

The alt and figcaption together read like a half-stitched prompt. Pull
out the chapter title and theme paraphrase, write a clean alt, and
DROP the figcaption (the image is decorative; the chapter h1 + Big
Picture below provide the topical context). For accessibility we still
keep an alt that names the chapter.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "node_modules", "KDP", "build", "source_fix_backups",
        "pagefind", ".book-update", "vendor", ".claude", "_archive",
        "agents", "templates", "docs", "scripts"}

# Whole figure block we want to rewrite. We capture:
#   - alt= (everything up to the next attribute or closing quote)
#   - the figcaption inside
# Match either chapter-opener OR part-opener OR plain illustration patterns.
FIGURE_PATTERNS = [
    # Inline alt with aria-describedby + figcaption with the continuation
    re.compile(
        r'(?P<pre><figure\s+class="illustration(?:\s+chapter-opener|\s+part-opener)?"\s*>)'
        r'(?P<img><img\s+alt="(?P<alt>[^"]*)"\s+aria-describedby="(?P<aid>[^"]+)"\s*/>)'
        r'(?P<fc><figcaption\s+id="(?P=aid)">(?P<figtxt>[^<]+)</figcaption>)'
        r'(?P<post>\s*</figure>)',
        re.IGNORECASE | re.DOTALL,
    ),
    # Variants where attributes are reordered (src first, then alt)
    re.compile(
        r'(?P<pre><figure\s+class="illustration(?:\s+chapter-opener|\s+part-opener)?"\s*>)'
        r'(?P<img><img\s+src="[^"]+"\s+(?:width="\d+"\s+height="\d+"\s+)?'
        r'alt="(?P<alt>[^"]*)"\s+aria-describedby="(?P<aid>[^"]+)"\s*/>)'
        r'(?P<fc><figcaption\s+id="(?P=aid)">(?P<figtxt>[^<]+)</figcaption>)'
        r'(?P<post>\s*</figure>)',
        re.IGNORECASE | re.DOTALL,
    ),
    # Inline alt only, no figcaption (the entire prompt fits in alt)
    re.compile(
        r'(?P<pre><figure\s+class="illustration(?:\s+chapter-opener|\s+part-opener)?"\s*>)'
        r'(?P<img><img\s+(?:src="[^"]+"\s+(?:width="\d+"\s+height="\d+"\s+)?)?'
        r'alt="(?P<alt>[^"]*(?:Kurzgesagt-meets-XKCD|cartoon-style hero illustration)[^"]*)"'
        r'(?:\s+src="[^"]+")?(?:\s+width="\d+")?(?:\s+height="\d+")?\s*/>)'
        r'(?P<post>\s*</figure>)',
        re.IGNORECASE | re.DOTALL,
    ),
    # Alt with aria-describedby pointing to a <span class="alt-supplemental"
    # hidden> sibling (NOT a figcaption). Used on part-index pages.
    re.compile(
        r'(?P<pre><figure\s+class="illustration(?:\s+chapter-opener|\s+part-opener)?"\s*>)'
        r'(?P<img><img\s+alt="(?P<alt>[^"]*)"\s+aria-describedby="(?P<aid>[^"]+)"'
        r'(?:\s+src="[^"]+")?(?:\s+width="\d+")?(?:\s+height="\d+")?\s*/>)'
        r'(?P<fc><span\s+class="alt-supplemental"\s+hidden=""\s+id="(?P=aid)">'
        r'(?P<figtxt>[^<]+)</span>)'
        r'(?P<post>\s*</figure>)',
        re.IGNORECASE | re.DOTALL,
    ),
]


def _extract_topic(alt: str, figtxt: str) -> str:
    """Extract the chapter/part/front-matter/appendix topic from the prompt.
    The alt+figtxt joined looks like:
       'Warm cartoon-style hero illustration introducing chapter
        'TITLE', a Kurzgesagt-meets-XKCD visual metaphor with friendly
        characters and clear iconography, capturing the theme: THEME.'
    """
    joined = (alt + figtxt).strip()
    # 'chapter '/'part '/'front-matter page '/'appendix 'X' substring
    m = re.search(
        r"introducing (?:chapter|part|front-matter page|appendix)\s+'([^']+)'",
        joined,
    )
    if m:
        return m.group(1).strip().rstrip('.')
    # Fallback: look for "capturing the theme: <theme>"
    m = re.search(r"capturing the theme:?\s*([^.]+)", joined)
    if m:
        return m.group(1).strip().rstrip('.')
    return ""


def rewrite_figure(m: re.Match) -> str:
    pre = m.group("pre")
    img_full = m.group("img")
    figtxt = m.groupdict().get("figtxt") or ""
    alt = m.group("alt")
    post = m.group("post")

    topic = _extract_topic(alt, figtxt)
    if not topic:
        # Could not derive a topic; keep original
        return m.group(0)
    new_alt = f"Chapter opener illustration: {topic}."
    if "part-opener" in pre.lower():
        new_alt = f"Part opener illustration: {topic}."
    # Front-matter pages use "introducing front-matter page 'X'"; we
    # already captured the X in topic, so reuse the front-matter label.
    if "front-matter page" in (alt + figtxt).lower():
        new_alt = f"Front-matter illustration: {topic}."

    # Replace alt= inside img_full
    new_img = re.sub(
        r'alt="[^"]*"',
        f'alt="{new_alt}"',
        img_full,
        count=1,
    )
    # Drop the aria-describedby attribute (no figcaption to point at)
    new_img = re.sub(
        r'\s+aria-describedby="[^"]+"',
        '',
        new_img,
        count=1,
    )
    # Reassemble figure WITHOUT the figcaption
    return f"{pre}{new_img}{post}"


FIGURE_BLOCK_RE = re.compile(
    r'<figure\s+class="illustration(?:\s+chapter-opener|\s+part-opener)?"\s*>'
    r'.*?</figure>',
    re.IGNORECASE | re.DOTALL,
)


def _fallback_clean(html: str) -> tuple[str, int]:
    """Find <figure>...Kurzgesagt...</figure> blocks where alt has broken
    inner quotes, and replace the whole figure with a minimal clean one.
    Topic is heuristically derived from the leaked prompt text using a
    permissive (?:") boundary instead of strict alt quoting.
    """
    n = 0
    out = []
    pos = 0
    for m in FIGURE_BLOCK_RE.finditer(html):
        block = m.group(0)
        if ("Kurzgesagt-meets-XKCD" not in block
                and "cartoon-style hero illustration" not in block):
            continue
        # Find the src
        sm = re.search(r'src="([^"]+)"', block)
        if not sm:
            continue
        src = sm.group(1)
        # Find width/height
        wm = re.search(r'width="(\d+)"', block)
        hm = re.search(r'height="(\d+)"', block)
        width = wm.group(1) if wm else None
        height = hm.group(1) if hm else None
        # Try to extract topic from the broken alt or surrounding text
        topic_m = re.search(
            r"introducing (?:chapter|part|front-matter page|appendix)[^A-Za-z0-9]+"
            r'([^",\.]+?)["\'",]',
            block,
        )
        if topic_m:
            topic = topic_m.group(1).strip().strip(".:'").strip()
        else:
            tm = re.search(r"capturing the theme:?\s*([^.]+)", block)
            topic = tm.group(1).strip().rstrip('.') if tm else ""
        if not topic:
            continue
        is_part = 'part-opener' in block.lower()
        is_fm = 'front-matter' in block.lower()
        is_app = 'appendix' in block.lower()
        if is_part:
            new_alt = f"Part opener illustration: {topic}."
            klass = 'illustration part-opener'
        elif is_fm:
            new_alt = f"Front-matter illustration: {topic}."
            klass = 'illustration chapter-opener'
        elif is_app:
            new_alt = f"Appendix opener illustration: {topic}."
            klass = 'illustration chapter-opener'
        else:
            new_alt = f"Chapter opener illustration: {topic}."
            klass = 'illustration chapter-opener'
        dims = ''
        if width:
            dims += f' width="{width}"'
        if height:
            dims += f' height="{height}"'
        new_block = (
            f'<figure class="{klass}">'
            f'<img src="{src}"{dims} alt="{new_alt}"/></figure>'
        )
        out.append(html[pos:m.start()])
        out.append(new_block)
        pos = m.end()
        n += 1
    out.append(html[pos:])
    return "".join(out), n


def fix_file(p: Path) -> int:
    html = p.read_text(encoding="utf-8")
    if "Kurzgesagt-meets-XKCD" not in html and "cartoon-style hero illustration" not in html:
        return 0
    new = html
    n = 0
    for pat in FIGURE_PATTERNS:
        new2, k = pat.subn(rewrite_figure, new)
        new = new2
        n += k
    # Fallback: brute-force clean any remaining figures with leaked prompts
    if "Kurzgesagt-meets-XKCD" in new or "cartoon-style hero illustration" in new:
        new2, k = _fallback_clean(new)
        new = new2
        n += k
    if n == 0 or new == html:
        return 0
    p.write_text(new, encoding="utf-8")
    return n


def main():
    n_files = 0
    n_total = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP:
            continue
        n = fix_file(p)
        if n:
            n_files += 1
            n_total += n
            print(f"  + {p.relative_to(ROOT)}: {n} figure(s)")
    print(f"\nFiles touched: {n_files}, figures cleaned: {n_total}")


if __name__ == "__main__":
    main()
