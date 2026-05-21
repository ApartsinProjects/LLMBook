"""V10: Split Distributed ML into Data Engineering + Distributed ML; add MLOps.

Production Infrastructure group grows from 3 to 5 appendices:

  Before (v9):                       After (v10):
  L  Inference Serving               L  Inference Serving
  M  Distributed ML  (M.1-M.7)       M  Data Engineering    (NEW; was M.1/M.2/M.6/M.7)
  N  Docker                          N  Distributed ML       (was M.3/M.4/M.5 + new N.1)
                                     O  MLOps                (NEW; 5 sections)
                                     P  Docker               (was N)

For Instructors letters cascade up by 2:
  O  Course Syllabi      -> Q
  P  Reading Pathways    -> R
  Q  Intermediate Projects -> S
  R  Capstone Project    -> T
  S  War Stories         -> U

Content move within old appendix-m-distributed-ml:
  M.1 PySpark              -> new M.1 (Data Engineering)
  M.2 Delta Lake           -> new M.2 (Data Engineering)
  M.3 Databricks Workspace -> new N.2 (Distributed ML)
  M.4 Databricks AI        -> new N.3 (Distributed ML)
  M.5 Ray Train/Serve/Data -> new N.4 (Distributed ML)
  M.6 Feature Stores       -> new M.3 (Data Engineering)
  M.7 Production Pipelines -> new M.4 (Data Engineering)
  NEW                       -> new N.1 (Distributed Training: DDP/FSDP/ZeRO)

New O MLOps sections (all start as stubs, content authored separately):
  O.1 Observability for LLM systems
  O.2 Monitoring and drift detection
  O.3 Deployment patterns (canary, blue-green, shadow, A/B)
  O.4 Model registry & lifecycle
  O.5 SLOs, alerting, FinOps

Idempotent. Run once with --apply.
"""
from __future__ import annotations
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPS = ROOT / "appendices"
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude", ".book-update"}

# Pure letter renames (entire dir rename + section file rename inside)
# Old M Distributed ML and the For Instructors letters
LETTER_RENAMES = [
    ("N", "P", "docker-containers"),
    ("O", "Q", "course-syllabi"),
    ("P", "R", "reading-pathways"),
    ("Q", "S", "intermediate-projects"),
    ("R", "T", "capstone-project"),
    ("S", "U", "war-stories"),
]

# Within old M (Distributed ML), which sections go to NEW M (Data Eng) and
# which to NEW N (Distributed ML), and at what new section numbers.
# (old_section_num -> (new_appendix_letter, new_section_num))
M_SPLIT = {
    "1": ("M", "1"),   # PySpark         -> M.1 Data Eng
    "2": ("M", "2"),   # Delta Lake      -> M.2 Data Eng
    "3": ("N", "2"),   # Databricks WS   -> N.2 Distributed ML
    "4": ("N", "3"),   # Databricks AI   -> N.3 Distributed ML
    "5": ("N", "4"),   # Ray             -> N.4 Distributed ML
    "6": ("M", "3"),   # Feature Stores  -> M.3 Data Eng
    "7": ("M", "4"),   # Prod Pipelines  -> M.4 Data Eng
}


def run_git(args: list[str], dry_run: bool) -> tuple[int, str]:
    if dry_run:
        return 0, ""
    res = subprocess.run(["git"] + args, cwd=ROOT,
                          capture_output=True, text=True)
    return res.returncode, res.stdout + res.stderr


def step1_split_old_m(dry_run: bool) -> list[str]:
    """Split appendix-m-distributed-ml into new M (Data Eng) and new N
    (Distributed ML). Old M goes away."""
    msgs: list[str] = []
    old_m = APPS / "appendix-m-distributed-ml"
    new_m = APPS / "appendix-m-data-engineering"
    new_n = APPS / "appendix-n-distributed-ml"

    if not old_m.exists():
        return [f"  SKIP: {old_m.name} missing; v10 may have already run"]

    # Rename old M to temp so we can create both new dirs at letter M and N.
    tmp_dir = APPS / "_v10-tmp-old-m"
    rc, out = run_git(["mv", str(old_m), str(tmp_dir)], dry_run)
    msgs.append(f"  git mv {old_m.name} -> {tmp_dir.name}"
                 f"{'' if rc == 0 else ' FAILED: ' + out}")

    if dry_run:
        return msgs

    new_m.mkdir(exist_ok=True)
    new_n.mkdir(exist_ok=True)
    (new_m / "images").mkdir(exist_ok=True)
    (new_n / "images").mkdir(exist_ok=True)

    # Move section files
    for old_num, (new_letter, new_num) in M_SPLIT.items():
        src = tmp_dir / f"section-m.{old_num}.html"
        dst_dir = new_m if new_letter == "M" else new_n
        dst = dst_dir / f"section-{new_letter.lower()}.{new_num}.html"
        if src.exists():
            rc, out = run_git(["mv", str(src), str(dst)], dry_run)
            msgs.append(f"    section-m.{old_num} -> "
                         f"section-{new_letter.lower()}.{new_num} "
                         f"({'M Data Eng' if new_letter == 'M' else 'N Distributed ML'})")

    # Move old M's index.html as the new M Data Engineering index (will
    # be retitled below); we'll create a fresh new N index.
    old_index = tmp_dir / "index.html"
    if old_index.exists():
        # Just move it; content will need authoring/retitling
        new_m_index = new_m / "index.html"
        rc, out = run_git(["mv", str(old_index), str(new_m_index)], dry_run)
        msgs.append(f"    index.html -> {new_m.name}/index.html "
                     f"(needs retitle to Data Engineering)")

    # Move shared images dir from old M to new M (Data Eng) by default;
    # author can hand-move any Distributed-ML-specific images later.
    old_images = tmp_dir / "images"
    if old_images.exists() and old_images.is_dir():
        for img in old_images.iterdir():
            dst_img = new_m / "images" / img.name
            if not dst_img.exists():
                shutil.move(str(img), str(dst_img))
        try:
            old_images.rmdir()
        except OSError:
            pass

    # Remove the temp dir
    try:
        # If anything's left, leave it but warn
        leftover = list(tmp_dir.iterdir())
        if leftover:
            msgs.append(f"    LEFTOVER in {tmp_dir.name}: "
                         f"{[p.name for p in leftover]}")
        else:
            tmp_dir.rmdir()
            msgs.append(f"    Removed empty {tmp_dir.name}")
    except OSError as e:
        msgs.append(f"    WARNING: {tmp_dir.name} cleanup: {e}")

    return msgs


def step2_create_mlops_appendix(dry_run: bool) -> list[str]:
    """Create new appendix-o-mlops/ with 5 section stubs."""
    msgs: list[str] = []
    new_o = APPS / "appendix-o-mlops"

    if new_o.exists():
        return [f"  SKIP: {new_o.name} already exists"]

    if dry_run:
        return [f"  WOULD create {new_o.name}/ + 5 section stubs"]

    new_o.mkdir()
    (new_o / "images").mkdir()

    sections = [
        ("1", "Observability for LLM Systems",
         "Metrics, traces, logs for LLM applications. "
         "OpenLLMetry, Phoenix, LangSmith, Helicone."),
        ("2", "Monitoring and Drift Detection",
         "Quality degradation, distribution shift, "
         "automated regression detection for production models."),
        ("3", "Deployment Patterns",
         "Canary releases, blue-green deployment, shadow mode, "
         "A/B testing for model rollouts."),
        ("4", "Model Registry and Lifecycle",
         "MLflow Model Registry, W&amp;B Registry, HuggingFace Hub. "
         "Versioning, staging, promotion, rollback."),
        ("5", "SLOs, Alerting, and FinOps",
         "Service-level objectives for LLM endpoints. PagerDuty / "
         "Opsgenie wiring. Per-request cost attribution and "
         "GPU-utilization FinOps for inference."),
    ]

    # Write index.html
    section_cards = "\n".join(
        f'<a class="section-card" href="section-o.{n}.html">'
        f'<span class="section-num">Section O.{n}</span>'
        f'<span class="section-title">{title}</span></a>'
        for n, title, _ in sections
    )

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="Appendix O: MLOps. Observability, monitoring, deployment patterns, model registry, and FinOps for LLM systems in production." name="description"/>
<title>Appendix O: MLOps | Building Conversational AI with LLMs and Agents</title>
<link href="../../styles/book.css" rel="stylesheet"/>
<link href="../../pagefind/pagefind-ui.css" rel="stylesheet"/>
<script defer="" src="../../pagefind/pagefind-ui.js"></script>
<script defer="" src="../../scripts/book.js"></script>
</head>
<body>
<header class="chapter-header">
<nav class="header-nav">
<a class="book-title-link" href="../../index.html">Building Conversational AI with LLMs and Agents</a>
<a class="toc-link" href="../../toc.html" title="Table of Contents"><span class="toc-icon">&#9776;</span> Contents</a>
</nav>
<div class="header-search"><div id="search"></div></div>
<div class="page-breadcrumb" data-pagefind-meta="chapter"><a href="../index.html">Appendices</a><span class="bc-sep">&rsaquo;</span><span class="bc-current">Appendix O</span></div>
<h1>MLOps</h1>
<p class="chapter-subtitle">Observability, monitoring, deployment patterns, model registry, and FinOps: the production lifecycle for LLM systems.</p>
</header>
<main class="content"><span class="pagefind-meta-injected" data-pagefind-meta="part:Appendices" hidden=""></span><span class="pagefind-meta-injected" data-pagefind-meta="chapter:Appendix O: MLOps" hidden=""></span>
<div class="callout big-picture">
<div class="callout-title">What this appendix is</div>
<p>The other Production Infrastructure appendices (<a href="../appendix-l-inference-serving/index.html">L Inference Serving</a>, <a href="../appendix-m-data-engineering/index.html">M Data Engineering</a>, <a href="../appendix-n-distributed-ml/index.html">N Distributed ML</a>, <a href="../appendix-p-docker-containers/index.html">P Docker</a>) cover the <em>build-and-deploy</em> half of running LLM systems. This appendix covers the <em>operate</em> half: observability so you can see what is happening, monitoring so you find out before users do, deployment patterns so you can roll out safely, a registry so you know which version is in production, and FinOps so you do not get fired for the bill.</p>
<p>MLOps for LLMs differs from classical MLOps in three ways. (1) The unit of cost is the token, not the request, which changes how you attribute spend. (2) Drift detection has to handle distributional shifts in <em>prompts</em>, not just inputs. (3) The model registry must version prompts and adapters alongside weights, not just weights. Each section below addresses these shifts where they matter.</p>
</div>
<div class="callout library-shortcut">
<div class="callout-title">Library Shortcut</div>
<pre><code class="lang-bash">pip install openllmetry            # OpenTelemetry for LLM apps
pip install arize-phoenix          # open-source LLM observability
pip install langsmith              # LangChain-native tracing + eval
pip install helicone               # LLM gateway with cost / latency / cache
pip install mlflow                 # registry + lifecycle (use 2.x with LLM extras)
pip install evidently              # drift detection for tabular + text
</code></pre>
</div>
<h2>Sections in This Appendix</h2>
<div class="section-card-list">
{section_cards}
</div>
<div class="whats-next">
<h2>What Comes Next</h2>
<p><a href="../appendix-p-docker-containers/index.html">Appendix P</a> covers the container layer that wraps everything you have just operationalized. The four appendices in this group (L through P) together describe a production-ready LLM stack.</p>
</div>
<nav class="chapter-nav">
<a class="prev" href="../appendix-n-distributed-ml/index.html"><span class="nav-label">Previous</span><span class="nav-num">Appendix N</span><span class="nav-title">Distributed ML</span></a>
<a class="up" href="../index.html"><span class="nav-label">Appendices</span><span class="nav-num">Appendices</span></a>
<a class="next" href="../appendix-p-docker-containers/index.html"><span class="nav-label">Next</span><span class="nav-num">Appendix P</span><span class="nav-title">Docker &amp; Containers</span></a>
</nav>
<footer><p>Fifteenth Edition, 2026 &middot; <a href="../../toc.html">Contents</a></p></footer>
</main>
</body>
</html>
"""
    (new_o / "index.html").write_text(index_html, encoding="utf-8")
    msgs.append(f"  created {new_o.name}/index.html")

    # Write section stubs
    for n, title, subtitle in sections:
        stub = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="Section O.{n}: {title}. {subtitle}" name="description"/>
<title>Section O.{n}: {title} | Building Conversational AI with LLMs and Agents</title>
<link href="../../styles/book.css" rel="stylesheet"/>
<link href="../../pagefind/pagefind-ui.css" rel="stylesheet"/>
<script defer="" src="../../pagefind/pagefind-ui.js"></script>
<script defer="" src="../../scripts/book.js"></script>
</head>
<body>
<header class="chapter-header">
<nav class="header-nav">
<a class="book-title-link" href="../../index.html">Building Conversational AI with LLMs and Agents</a>
<a class="toc-link" href="../../toc.html" title="Table of Contents"><span class="toc-icon">&#9776;</span> Contents</a>
</nav>
<div class="header-search"><div id="search"></div></div>
<div class="page-breadcrumb" data-pagefind-meta="chapter"><a href="../index.html">Appendices</a><span class="bc-sep">&rsaquo;</span><a href="index.html">Appendix O: MLOps</a></div>
<h1>{title}</h1><div class="page-current">Section O.{n}</div>
</header>
<main class="content"><span class="pagefind-meta-injected" data-pagefind-meta="part:Appendices" hidden=""></span><span class="pagefind-meta-injected" data-pagefind-meta="chapter:Appendix O: MLOps" hidden=""></span>
<div class="callout big-picture">
<div class="callout-title">What this section is</div>
<p>{subtitle}</p>
</div>
<p><em>This section is a planned-coverage stub. Content authoring queued.</em></p>
<nav class="chapter-nav">
<a class="prev" href="index.html"><span class="nav-label">Previous</span><span class="nav-num">Appendix O</span><span class="nav-title">MLOps</span></a>
<a class="up" href="index.html"><span class="nav-label">In Appendix</span><span class="nav-num">Appendix O</span><span class="nav-title">MLOps</span></a>
<a class="next" href="index.html"><span class="nav-label">Next</span><span class="nav-num">Appendix O</span><span class="nav-title">MLOps</span></a>
</nav>
<footer><p>Fifteenth Edition, 2026 &middot; <a href="../../toc.html">Contents</a></p></footer>
</main>
</body>
</html>
"""
        (new_o / f"section-o.{n}.html").write_text(stub, encoding="utf-8")
        msgs.append(f"  created section-o.{n}.html ({title})")
    return msgs


def step3_letter_renames(dry_run: bool) -> list[str]:
    """Rename N->P (Docker), and O-S -> Q-U (For Instructors) via temp."""
    msgs: list[str] = []
    # Pass A: rename to temp
    for old, new, slug in LETTER_RENAMES:
        src = APPS / f"appendix-{old.lower()}-{slug}"
        dst = APPS / f"_tmp10-{new.lower()}-{slug}"
        if not src.exists():
            msgs.append(f"  SKIP: {src.name} missing")
            continue
        rc, out = run_git(["mv", str(src), str(dst)], dry_run)
        msgs.append(f"  git mv {src.name} -> {dst.name}")
    # Pass B: temp -> final
    for old, new, slug in LETTER_RENAMES:
        src = APPS / f"_tmp10-{new.lower()}-{slug}"
        dst = APPS / f"appendix-{new.lower()}-{slug}"
        if not src.exists():
            continue
        rc, out = run_git(["mv", str(src), str(dst)], dry_run)
        msgs.append(f"  git mv {src.name} -> {dst.name}")
    # Rename section files inside each renamed appendix (Docker has N.1-N.4)
    if not dry_run:
        for old, new, slug in LETTER_RENAMES:
            d = APPS / f"appendix-{new.lower()}-{slug}"
            if not d.exists():
                continue
            for sec in sorted(d.glob(f"section-{old.lower()}.*.html")):
                new_name = sec.name.replace(
                    f"section-{old.lower()}.", f"section-{new.lower()}.")
                new_path = sec.parent / new_name
                if new_path == sec or new_path.exists():
                    continue
                subprocess.run(["git", "mv", str(sec), str(new_path)],
                                cwd=ROOT, check=False)
                msgs.append(f"    section {sec.name} -> {new_name}")
    return msgs


def step4_book_wide_rewrite(dry_run: bool) -> int:
    """Rewrite cross-refs book-wide. Two passes via § markers.

    Letter renames in this v10 (forward map):
      M -> M (no letter change, but content split; URL paths within old M
              need to be split — handled by the URL-level rewrites)
      N -> P  (Docker)
      O -> Q  (Course Syllabi)
      P -> R  (Reading Pathways)
      Q -> S  (Intermediate Projects)
      R -> T  (Capstone)
      S -> U  (War Stories)

    Old M section file URLs need split:
      appendix-m-distributed-ml/section-m.1.html -> appendix-m-data-engineering/section-m.1.html
      appendix-m-distributed-ml/section-m.2.html -> appendix-m-data-engineering/section-m.2.html
      appendix-m-distributed-ml/section-m.3.html -> appendix-n-distributed-ml/section-n.2.html
      appendix-m-distributed-ml/section-m.4.html -> appendix-n-distributed-ml/section-n.3.html
      appendix-m-distributed-ml/section-m.5.html -> appendix-n-distributed-ml/section-n.4.html
      appendix-m-distributed-ml/section-m.6.html -> appendix-m-data-engineering/section-m.3.html
      appendix-m-distributed-ml/section-m.7.html -> appendix-m-data-engineering/section-m.4.html
      appendix-m-distributed-ml/index.html -> appendix-m-data-engineering/index.html
    """
    letter_forward = {old: new for old, new, _ in LETTER_RENAMES}  # N->P, O->Q, etc.
    # Plus the m-distributed-ml URL renames
    m_url_map = [
        ("appendix-m-distributed-ml/section-m.1.html",
         "appendix-m-data-engineering/section-m.1.html"),
        ("appendix-m-distributed-ml/section-m.2.html",
         "appendix-m-data-engineering/section-m.2.html"),
        ("appendix-m-distributed-ml/section-m.6.html",
         "appendix-m-data-engineering/section-m.3.html"),
        ("appendix-m-distributed-ml/section-m.7.html",
         "appendix-m-data-engineering/section-m.4.html"),
        ("appendix-m-distributed-ml/section-m.3.html",
         "appendix-n-distributed-ml/section-n.2.html"),
        ("appendix-m-distributed-ml/section-m.4.html",
         "appendix-n-distributed-ml/section-n.3.html"),
        ("appendix-m-distributed-ml/section-m.5.html",
         "appendix-n-distributed-ml/section-n.4.html"),
        ("appendix-m-distributed-ml/index.html",
         "appendix-m-data-engineering/index.html"),
        ("appendix-m-distributed-ml/",
         "appendix-m-data-engineering/"),
    ]

    n_files = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        text = p.read_text(encoding="utf-8")
        orig = text

        # 1. Old M URL splits (must come before any letter-cascade)
        for old_url, new_url in m_url_map:
            text = text.replace(old_url, new_url)

        # 2. Letter cascade via § markers
        for old in letter_forward:
            text = re.sub(rf"\bAppendix\s+{old}\b",
                           f"Appendix §{old}§", text)
            for kind in ("Code Fragment", "Figure", "Table", "Pseudocode",
                          "Listing"):
                text = re.sub(rf"\b{kind}\s+{old}\.(\d+(?:\.\d+)?)\b",
                               rf"{kind} §{old}§.\1", text)
            text = re.sub(rf"\bSection\s+{old}\.(\d+(?:\.\d+)?)\b",
                           rf"Section §{old}§.\1", text)
            text = re.sub(rf"appendix-{old.lower()}-",
                           f"appendix-§{old}§-", text)
            text = re.sub(rf"section-{old.lower()}\.(\d+(?:\.\d+)?)\.html",
                           rf"section-§{old}§.\1.html", text)
            text = re.sub(rf"section-{old.lower()}\.(\d+(?:\.\d+)?)#",
                           rf"section-§{old}§.\1#", text)
        for old, new in letter_forward.items():
            text = text.replace(f"§{old}§", new)
        for old, new in letter_forward.items():
            text = text.replace(f"appendix-{new}-", f"appendix-{new.lower()}-")
            text = text.replace(f"section-{new}.", f"section-{new.lower()}.")

        if text != orig:
            n_files += 1
            if not dry_run:
                p.write_text(text, encoding="utf-8")
    return n_files


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply
    mode = "DRY-RUN" if dry_run else "APPLY"

    print(f"=== {mode}: Step 1 - Split old M into new M (Data Eng) + N (Distributed ML) ===")
    for m in step1_split_old_m(dry_run):
        print(m)
    print(f"\n=== {mode}: Step 2 - Create new O MLOps appendix ===")
    for m in step2_create_mlops_appendix(dry_run):
        print(m)
    print(f"\n=== {mode}: Step 3 - Letter renames (N->P Docker, O-S->Q-U) ===")
    for m in step3_letter_renames(dry_run):
        print(m)
    print(f"\n=== {mode}: Step 4 - Book-wide cross-ref rewrite ===")
    n = step4_book_wide_rewrite(dry_run)
    print(f"  {n} files updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
