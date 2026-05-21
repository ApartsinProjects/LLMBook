"""Phase 9.5: finalize cleanup of remaining broken refs.

Specific fixes:
  1. Bare same-folder section-X.Y refs in cross-part destinations where
     the target now lives in a DIFFERENT module of the same part.
     Rewrite to use `../module-X-slug/section-X.Y.html`.

  2. Refs to deleted modules' index.html (module-35-production-engineering,
     module-49-post-launch-monitoring) routed to a sensible successor:
       module-35-production-engineering -> module-51-production-engineering
       module-49-post-launch-monitoring -> module-37-online-eval-observability

  3. Refs to NOT-YET-AUTHORED stub sections (35.1, 35.2, 35.4, 35.5, 37.1, 37.2)
     routed to the source section they came from until split happens:
       35.1 (Testing Pyramid, from 34.3) -> module-34-evaluation-foundations/section-34.3.html
       37.1 (Tracing, from 34.6) -> module-34-evaluation-foundations/section-34.6.html
       37.2 (Observability Platforms, from 34.6) -> module-34-evaluation-foundations/section-34.6.html

DRY-RUN by default.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MAP = HERE / "migration-map.json"

SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude", ".book-update", "vendor", "docs",
              "_scratch_part8_new_sections"}

# Manual routes for stub / deleted-module refs.
# Key: target path component (last 2-3 segments or filename)
# Value: replacement path (full or relative to substitute)
STUB_ROUTES = {
    # Stub sections still routed to source until split is done
    "module-35-testing-quality-gates/section-35.1.html":
        "module-34-evaluation-foundations/section-34.3.html",
    "module-35-testing-quality-gates/section-35.2.html":
        "module-34-evaluation-foundations/section-34.3.html",
    "module-35-testing-quality-gates/section-35.4.html":
        "module-34-evaluation-foundations/section-34.3.html",
    "module-35-testing-quality-gates/section-35.5.html":
        "module-34-evaluation-foundations/section-34.3.html",
    "module-37-online-eval-observability/section-37.1.html":
        "module-34-evaluation-foundations/section-34.6.html",
    "module-37-online-eval-observability/section-37.2.html":
        "module-34-evaluation-foundations/section-34.6.html",
    "module-37-online-eval-observability/section-37.3.html":
        "module-34-evaluation-foundations/section-34.10.html",
    # Deleted module indexes -> successor
    "module-35-production-engineering/index.html":
        "module-51-production-engineering/index.html",
    "module-35-production-engineering/section-35.1.html":
        "module-50-shipping-deploying/section-50.5.html",
    "module-35-production-engineering/section-35.2.html":
        "module-50-shipping-deploying/section-50.6.html",
    "module-35-production-engineering/section-35.3.html":
        "module-51-production-engineering/section-51.1.html",
    "module-35-production-engineering/section-35.4.html":
        "module-51-production-engineering/section-51.2.html",
    "module-35-production-engineering/section-35.5.html":
        "module-51-production-engineering/section-51.3.html",
    "module-35-production-engineering/section-35.6.html":
        "module-51-production-engineering/section-51.4.html",
    "module-35-production-engineering/section-35.7.html":
        "module-51-production-engineering/section-51.5.html",
    "module-35-production-engineering/section-35.8.html":
        "module-51-production-engineering/section-51.6.html",
    "module-35-production-engineering/section-35.9.html":
        "module-51-production-engineering/section-51.7.html",
    "module-49-post-launch-monitoring/index.html":
        "module-37-online-eval-observability/section-37.4.html",
    "module-49-post-launch-monitoring/section-49.1.html":
        "module-37-online-eval-observability/section-37.4.html",
    "module-49-post-launch-monitoring/section-49.2.html":
        "module-37-online-eval-observability/section-37.5.html",
    "module-49-post-launch-monitoring/section-49.3.html":
        "module-37-online-eval-observability/section-37.6.html",
}

# Module -> part lookup
MODULE_PART = {
    "module-34-evaluation-foundations": "part-8-evaluation-production",
    "module-35-testing-quality-gates": "part-8-evaluation-production",
    "module-36-specialized-evaluation": "part-8-evaluation-production",
    "module-37-online-eval-observability": "part-8-evaluation-production",
    "module-38-tools-of-the-trade": "part-8-evaluation-production",
    "module-50-shipping-deploying": "part-10-idea-to-product",
    "module-51-production-engineering": "part-10-idea-to-product",
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply

    files_edited = 0
    total = 0

    # For each known stub/deleted route, rewrite all refs.
    # The regex catches: href="(prefix)?(old_path)" where old_path includes module + filename.
    for old_path, new_path in STUB_ROUTES.items():
        # Replace href="(./)?(./)?(old_path)" with appropriate new_path.
        # Handle 3 prefix forms: bare, ../, ../../
        # Compute the NEW relative target based on source file's location.
        old_mod = old_path.split("/")[0]
        new_mod = new_path.split("/")[0]
        old_part = MODULE_PART.get(old_mod) or {
            "module-35-production-engineering": "part-8-evaluation-production",
            "module-49-post-launch-monitoring": "part-10-idea-to-product",
        }.get(old_mod)
        new_part = MODULE_PART.get(new_mod)
        if not old_part or not new_part:
            continue
        new_fn = new_path.split("/")[1] if "/" in new_path else new_path

        for p in sorted(ROOT.rglob("*.html")):
            if set(p.parts) & SKIP_PARTS:
                continue
            text = p.read_text(encoding="utf-8")
            orig = text

            # Determine src file's part
            src_part = p.parts[len(ROOT.parts)] if p.is_relative_to(ROOT) else None

            # The new relative href depends on where src file is.
            if src_part == new_part:
                # Same part: use ../{new_mod}/{new_fn}
                # unless src IS in the new module already, in which case same-folder.
                src_mod = p.parts[len(ROOT.parts) + 1] if len(p.parts) > len(ROOT.parts) + 1 else None
                if src_mod == new_mod:
                    new_href = f"{new_fn}"  # same folder
                else:
                    new_href = f"../{new_mod}/{new_fn}"
            else:
                # Different part: use ../../{new_part}/{new_mod}/{new_fn}
                new_href = f"../../{new_part}/{new_mod}/{new_fn}"

            # Replace any href ending in old_path
            # Match various prefix forms
            pattern = re.compile(
                rf'href="((?:\.\./)*(?:{re.escape(old_part)}/)?){re.escape(old_path)}"'
            )
            def repl(m: re.Match) -> str:
                nonlocal total
                total += 1
                return f'href="{new_href}"'
            text = pattern.sub(repl, text)

            if text != orig:
                if not dry_run:
                    p.write_text(text, encoding="utf-8")
                files_edited += 1

    print(f"=== Summary ===")
    print(f"Files edited:    {files_edited}")
    print(f"Hrefs rewritten: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
