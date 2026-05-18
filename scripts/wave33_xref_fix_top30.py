"""Apply only the top-30 bad anchor text fixes."""

import os
import re
import json

ROOT = r"E:\Projects\BookBlogsHome\LLMBook"
os.chdir(ROOT)

FINDINGS = json.load(open("docs/content-audit/_xref_findings.json", "r", encoding="utf-8"))

def skip_file(path):
    norm = path.replace("\\", "/")
    return "module-42" in norm or "module-44" in norm


def rewrite_anchor_text(content, href, old_text, new_text):
    """Find FIRST <a> with given href whose plain text matches old_text exactly,
    and replace text with new_text. Returns (new_content, changed_bool)."""
    href_re = re.escape(href)
    pattern = re.compile(
        rf'(<a\b[^>]*href\s*=\s*"{href_re}"[^>]*>)([\s\S]*?)(</a>)',
        re.IGNORECASE,
    )
    for m in pattern.finditer(content):
        opening = m.group(1)
        inner = m.group(2)
        closing = m.group(3)
        plain = re.sub(r"<[^>]+>", "", inner).strip()
        if plain == old_text.strip():
            if "<" in inner:
                if old_text in inner:
                    new_inner = inner.replace(old_text, new_text, 1)
                else:
                    continue
            else:
                new_inner = new_text
            new_content = content[:m.start()] + opening + new_inner + closing + content[m.end():]
            return new_content, True
    return content, False


FIXES_APPLIED = []


def apply_text_fix(fpath, href, old_text, new_text, category):
    if skip_file(fpath):
        return False
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    new_content, changed = rewrite_anchor_text(content, href, old_text, new_text)
    if not changed:
        return False
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(new_content)
    FIXES_APPLIED.append({
        "file": fpath,
        "category": category,
        "before": old_text,
        "after": new_text,
        "href": href,
    })
    return True


bad = FINDINGS["bad_anchor_text"]

def priority(it):
    cited_ch = int(it["cited_section"].split(".")[0])
    target_ch = int(it["target_section"].split(".")[0])
    return (0 if cited_ch != target_ch else 1, it["file"], it["href"])


bad_sorted = sorted(bad, key=priority)

candidates = []
seen = set()
for it in bad_sorted:
    if skip_file(it["file"]):
        continue
    # Skip index.html section-card cases (multiple bad ones from earlier are now filtered
    # but the index page false positives might still appear)
    if it["file"].endswith("/index.html"):
        # Only consider if anchor text is short (under 60 chars)
        if len(it["text"]) > 60:
            continue
    key = (it["file"], it["href"], it["text"])
    if key in seen:
        continue
    seen.add(key)
    candidates.append(it)
    if len(candidates) >= 30:
        break


top30_fixes = []
for it in candidates:
    cited = it["cited_section"]
    target = it["target_section"]
    old_text = it["text"].strip()
    # Build pattern that matches the cited section number safely
    pattern = re.compile(
        r"(?i)\b(section\s+)" + re.escape(cited) + r"\b"
    )
    def _sub(m, t=target):
        return m.group(1) + t
    new_text = pattern.sub(_sub, old_text, count=1)
    if new_text == old_text:
        continue
    ok = apply_text_fix(it["file"], it["href"], old_text, new_text, "bad_anchor_text")
    top30_fixes.append({
        "file": it["file"],
        "before": old_text,
        "after": new_text,
        "ok": ok,
        "href": it["href"],
    })


print()
print("Top 30 bad anchor text fixes:")
for f in top30_fixes:
    status = "OK" if f["ok"] else "MISS"
    print(f"  {status}: {f['file']}")
    print(f"      before: {f['before'][:80]!r}")
    print(f"      after:  {f['after'][:80]!r}")


with open("docs/content-audit/_xref_top30_fixes.json", "w", encoding="utf-8") as fh:
    json.dump({"top30_bad_anchor": top30_fixes, "applied": FIXES_APPLIED}, fh, indent=2)

print()
print(f"Successfully applied: {sum(1 for f in top30_fixes if f['ok'])} / {len(top30_fixes)}")
