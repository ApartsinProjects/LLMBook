"""Inspect IMAGE_OPPORTUNITY false positives: sections flagged as missing
figures might actually have <figure>, <img>, or <svg> markup that the
detector regex doesn't recognize."""
import json
import subprocess
from pathlib import Path
from collections import Counter

REPO_ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")
PY = r"C:/Python314/python.exe"

out = subprocess.run(
    [PY, str(REPO_ROOT / "scripts/run_book_audit.py"),
     "--checks", "IMAGE_OPPORTUNITY", "--json"],
    capture_output=True, text=True, cwd=str(REPO_ROOT),
)
data = json.loads(out.stdout)

# Two categories: missing figure/diagram, missing fun-note
missing_figure = [i for i in data["issues"] if "figure or diagram" in i["message"]]
missing_fun_note = [i for i in data["issues"] if "fun-note" in i["message"]]
print(f"Missing figure/diagram: {len(missing_figure)}")
print(f"Missing fun-note: {len(missing_fun_note)}")

patterns = {
    '<figure class="diagram"': "fig-diagram",
    '<figure class="illustration"': "fig-illustration",
    '<figure>': "fig-plain",
    '<svg': "svg",
    'class="diagram-container"': "diagram-container",
    '<img': "img",
}
counts = Counter()
sample_diagram = []
for iss in missing_figure:
    fp = REPO_ROOT / iss["file"].replace("\\", "/")
    if not fp.exists():
        continue
    content = fp.read_text(encoding="utf-8")
    found_any = False
    for pat, key in patterns.items():
        if pat in content:
            counts[key] += 1
            found_any = True
    if not found_any:
        counts["none"] += 1
    # If has <figure>, log it
    if "<figure" in content and "<figure class=\"illustration\"" not in content and "<svg" not in content:
        if len(sample_diagram) < 10:
            sample_diagram.append(iss["file"])

print("\nMarkup found:")
for k, v in counts.most_common():
    print(f"  {k}: {v}")
print("\nFiles with <figure> but no illustration class and no svg:")
for s in sample_diagram:
    print(f"  {s}")
