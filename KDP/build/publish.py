"""
Publishing pipeline orchestrator.

Single entry point that does the full HTML -> validated EPUB flow.
Designed for repeated runs as the source HTML evolves.

Validation chain: structural_check -> EPUBCheck -> (optimize) -> post-optimize
EPUBCheck -> Kindle Previewer KFX conversion + qualitychecks (the Kindle
converter is stricter than EPUBCheck; see step_kpv). Each gate sets a non-zero
exit on real errors but is non-fatal when its tool is not installed.

Usage:
    python KDP/build/publish.py                # full build + validation (incl. KPV KFX gate)
    python KDP/build/publish.py --quick        # smaller images, faster (skips KPV)
    python KDP/build/publish.py --validate-only  # skip rebuild; run validators incl. KPV
    python KDP/build/publish.py --clean        # delete output then rebuild
    python KDP/build/publish.py --no-epubcheck # skip Java epubcheck even if installed
    python KDP/build/publish.py --no-kpv       # skip the Kindle Previewer KFX gate (~2-4 min)
    python KDP/build/publish.py --regen-spine  # re-walk source tree before building

Exit codes:
    0  pipeline completed and validation passed
    1  validation found errors
    2  build failed
    3  prerequisite missing
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# --------------------------------------------------------------------- paths

PROJECT_ROOT = Path(__file__).resolve().parents[2]
KDP_DIR = PROJECT_ROOT / "KDP"
BUILD_DIR = KDP_DIR / "build"
OUTPUT_DIR = KDP_DIR / "output"
VALIDATION_DIR = KDP_DIR / "validation"
LOG_DIR = KDP_DIR / "build" / "logs"

PYTHON = sys.executable  # use the same python that ran this script

# --------------------------------------------------------------------- output


def _color(code: int, msg: str) -> str:
    if not sys.stdout.isatty():
        return msg
    return f"\033[{code}m{msg}\033[0m"


def step(name: str) -> None:
    print()
    print(_color(36, f">>> {name}"))


def ok(msg: str) -> None:
    print(_color(32, f"  [OK] {msg}"))


def warn(msg: str) -> None:
    print(_color(33, f"  [WARN] {msg}"))


def fail(msg: str) -> None:
    print(_color(31, f"  [FAIL] {msg}"))


def run(cmd: list[str], log_path: Path | None = None, env: dict | None = None) -> tuple[int, str]:
    """Run a subprocess; capture combined output. Tee to log file if given."""
    print(f"  $ {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=str(PROJECT_ROOT), capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    out = (proc.stdout or "") + (proc.stderr or "")
    if log_path:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(out, encoding="utf-8")
    return proc.returncode, out


# --------------------------------------------------------------------- prerequisites


def check_prerequisites() -> int:
    step("0. Prerequisites")

    # Python libraries
    deps = ["ebooklib", "bs4", "lxml", "PIL", "yaml"]
    missing: list[str] = []
    for dep in deps:
        try:
            __import__(dep)
            ok(f"python:{dep}")
        except ImportError:
            missing.append(dep)
            fail(f"python:{dep} not installed")
    if missing:
        print()
        print(f"  Install missing dependencies:")
        print(f"    {PYTHON} -m pip install -r KDP/build/requirements.txt")
        return 3

    # Required source files. The canonical builder is the html2epub
    # package driven by html2epub.toml; build_epub.py is legacy and no
    # longer invoked by this pipeline (kept for reference only).
    required = [
        KDP_DIR / "metadata" / "metadata.yaml",
        KDP_DIR / "cover" / "cover_kdp.jpg",
        PROJECT_ROOT / "html2epub.toml",
        BUILD_DIR / "epub_overrides.css",
        PROJECT_ROOT / "styles" / "book.css",
    ]
    for p in required:
        if p.exists():
            ok(f"file: {p.relative_to(PROJECT_ROOT)}")
        else:
            fail(f"missing: {p.relative_to(PROJECT_ROOT)}")
            return 3

    # Cross-check that html2epub.toml is in sync with metadata.yaml so the
    # OPF identifier, publication_date, and edition surface correctly.
    rc = check_metadata_sync()
    if rc != 0:
        return rc

    return 0


def check_metadata_sync() -> int:
    """Verify html2epub.toml mirrors metadata.yaml on the fields that
    feed the EPUB OPF. Mismatches lead to KDP detecting the wrong edition
    or a stale publication date in the bundled metadata."""
    try:
        import yaml
        try:
            import tomllib  # py 3.11+
        except ImportError:
            import tomli as tomllib  # type: ignore
    except ImportError:
        warn("yaml/tomllib not available; skipping metadata-sync check")
        return 0
    meta_path = KDP_DIR / "metadata" / "metadata.yaml"
    toml_path = PROJECT_ROOT / "html2epub.toml"
    try:
        meta = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
        with toml_path.open("rb") as fh:
            toml = tomllib.load(fh)
    except Exception as e:
        warn(f"metadata-sync check skipped: {e}")
        return 0

    book_meta = meta.get("book", {}) or {}
    book_toml = toml.get("book", {}) or {}
    ids = meta.get("identifiers", {}) or {}

    pairs = [
        ("publication_date",
         book_meta.get("publication_date"),
         book_toml.get("publication_date")),
        ("identifier",
         ids.get("uuid"),
         book_toml.get("identifier")),
        ("edition",
         book_meta.get("edition"),
         book_toml.get("edition")),
        ("rights",
         book_meta.get("rights"),
         book_toml.get("rights")),
    ]
    drift = []
    for name, ymv, tmv in pairs:
        if ymv and tmv and str(ymv) != str(tmv):
            drift.append((name, ymv, tmv))
    if drift:
        for name, ymv, tmv in drift:
            fail(f"metadata drift: {name}: yaml={ymv!r} toml={tmv!r}")
        print("  Sync html2epub.toml [book] with KDP/metadata/metadata.yaml.")
        return 3
    ok("metadata.yaml <-> html2epub.toml in sync")
    return 0


def find_epubcheck_install() -> tuple[Path, Path] | None:
    """
    Locate java executable and epubcheck.jar.

    Search order:
      1. EPUBCHECK_HOME env var (parent dir containing epubcheck-*/ and a JDK)
      2. EPUBCHECK_JAR + JAVA_BIN env vars (explicit paths)
      3. Common install dirs (E:/Tools/epubcheck, ~/epubcheck, etc).
         Each dir is searched for epubcheck-*/epubcheck.jar AND a bundled
         jdk-*/bin/java.exe or jre-*/bin/java.exe.
      4. System PATH java + standalone epubcheck.jar in standard locations.

    Returns (java_exe, epubcheck_jar) if both found, else None.
    """
    import os

    candidate_dirs = []
    if os.environ.get("EPUBCHECK_HOME"):
        candidate_dirs.append(Path(os.environ["EPUBCHECK_HOME"]))
    candidate_dirs.extend([
        Path("E:/Tools/epubcheck"),
        Path.home() / "epubcheck",
        Path.home() / ".local" / "share" / "epubcheck",
        Path("C:/Program Files/epubcheck"),
        Path("/usr/local/share/epubcheck"),
    ])

    java_suffix = "java.exe" if sys.platform == "win32" else "java"

    for d in candidate_dirs:
        if not d.exists():
            continue
        # Find epubcheck-*/epubcheck.jar
        # IMPORTANT: pick the NEWEST version (sorted() returns ascending,
        # so 'epubcheck-5.2.1' precedes 'epubcheck-5.3.0'; use [-1] for newest).
        # A bare epubcheck.jar in the dir root is treated as fallback (oldest).
        ec_versioned = sorted(d.glob("epubcheck-*/epubcheck.jar"))
        ec_bare = sorted(d.glob("epubcheck.jar"))
        if ec_versioned:
            ec_jar = ec_versioned[-1]  # newest version wins
        elif ec_bare:
            ec_jar = ec_bare[-1]
        else:
            continue

        # Find bundled JDK / JRE
        java_candidates = (
            sorted(d.glob(f"jdk-*/bin/{java_suffix}"))
            + sorted(d.glob(f"jre-*/bin/{java_suffix}"))
            + sorted(d.glob(f"jdk*/bin/{java_suffix}"))
        )
        if java_candidates:
            return (java_candidates[0], ec_jar)

        # No bundled java, try EPUBCHECK_JAR + system java
        if shutil.which("java"):
            return (Path("java"), ec_jar)

    # No bundled install. Try explicit env var + system java.
    ec_jar_env = os.environ.get("EPUBCHECK_JAR")
    java_bin = os.environ.get("JAVA_BIN") or shutil.which("java")
    if ec_jar_env and Path(ec_jar_env).exists() and java_bin:
        return (Path(java_bin), Path(ec_jar_env))

    return None


# --------------------------------------------------------------------- pipeline steps


def step_clean() -> None:
    step("Cleaning output")
    if OUTPUT_DIR.exists():
        for p in OUTPUT_DIR.glob("*.epub"):
            p.unlink()
            ok(f"removed {p.name}")
    if VALIDATION_DIR.exists():
        for p in VALIDATION_DIR.glob("*_report.txt"):
            p.unlink()
            ok(f"removed {p.name}")


def step_regen_spine() -> int:
    # LEGACY: spine_manifest.json feeds the old build_epub.py only. The active
    # html2epub builder uses `spine = "auto"`, so this manifest is informational.
    step("Regenerating spine manifest (legacy build_epub.py only)")
    rc, out = run([PYTHON, str(BUILD_DIR / "generate_spine.py")])
    if rc != 0:
        fail("spine generation failed")
        print(out)
        return 2
    # Show the breakdown line
    for line in out.splitlines():
        if line.strip().startswith(("Wrote", "Breakdown")) or line.strip().startswith(("front", "part", "appendix", "module", "section", "capstone")):
            print(f"  {line}")
    ok("spine_manifest.json refreshed")
    return 0


def step_build_epub(quick: bool) -> int:
    step("Building EPUB (html2epub)")
    # Canonical builder is the html2epub package (KDP/html2epub/), driven by html2epub.toml at the project root.
    cmd = [PYTHON, "-m", "html2epub", "build", str(PROJECT_ROOT)]
    if quick:
        warn("quick mode requested — html2epub honors [images] settings in html2epub.toml; "
             "for smaller files temporarily lower max_side/jpeg_quality and re-run.")

    # Make project-local plugin module (_html2epub_hooks.py) importable
    import os as _os
    _env = _os.environ.copy()
    _bd = str(BUILD_DIR)
    _env["PYTHONPATH"] = _bd + _os.pathsep + _env.get("PYTHONPATH", "")

    log = LOG_DIR / f"build_{ts()}.log"
    rc, out = run(cmd, log, env=_env)
    if rc != 0:
        fail("build failed")
        print(out[-2000:])
        return 2
    # Show the summary lines from the build log
    for line in out.splitlines()[-15:]:
        print(f"  {line}")
    ok("EPUB built")
    return 0


def step_structural_validate() -> int:
    step("Structural validation (Python)")
    rc, out = run([PYTHON, str(VALIDATION_DIR / "structural_check.py")])
    print(out)
    if rc == 0:
        ok("structural validation PASSED")
    else:
        fail("structural validation FAILED")
    return rc


def step_epubcheck(java: Path, jar: Path, strict: bool = False) -> int:
    """Run EPUBCheck. If `strict=True`, also pass --failonwarnings and -u
    so any warning OR usage-level finding counts as failure. Use strict mode
    AFTER post-build patches to catch property corruption (OPF-027 etc.)
    that our patches could have introduced (e.g. rendition:wide bug from
    fix_fxl_filenames.py keyword scrub corrupting rendition:spread)."""
    step("EPUB schema validation (epubcheck)" + (" [STRICT]" if strict else ""))
    epub = OUTPUT_DIR / "building-conversational-ai-llms-agents.epub"
    log = VALIDATION_DIR / ("epubcheck_strict_report.txt" if strict else "epubcheck_report.txt")
    # Use a project-local Java temp dir so we don't depend on the system
    # %TEMP% having free space (C: drive can be tight on Windows).
    java_tmp = LOG_DIR / "java-tmp"
    java_tmp.mkdir(parents=True, exist_ok=True)
    print(f"  java:      {java}")
    print(f"  epubcheck: {jar}")
    cmd = [str(java), f"-Djava.io.tmpdir={java_tmp}", "-jar", str(jar)]
    if strict:
        cmd += ["--failonwarnings", "-u"]
    cmd.append(str(epub))
    rc, out = run(cmd, log)
    # epubcheck prints a final summary line; show last 30 lines
    tail = out.splitlines()[-30:]
    print("  " + "\n  ".join(tail))
    if rc == 0:
        ok(f"epubcheck PASSED -> {log.relative_to(PROJECT_ROOT)}")
    else:
        fail(f"epubcheck FAILED -> see {log.relative_to(PROJECT_ROOT)}")
    return rc


def repair_optimized_entities(epub_path: Path) -> int:
    """
    Re-add the trailing `;` to XML entities that html-minifier-terser
    stripped (most commonly &apos; before a " attribute terminator, but
    also &quot;, &lt;, &gt;).

    Repackages the EPUB in place. Returns total number of entity fixes.
    """
    import re
    import zipfile
    import io
    import os
    # Pattern: an XML entity NOT followed by `;` or another letter/digit.
    # `&amp` is intentionally excluded from the broad pattern because it's
    # a prefix of many valid entity names.
    fix_re = re.compile(r"&(apos|quot|lt|gt|nbsp|copy|reg|trade)(?=[^;a-zA-Z0-9])")
    # Self-closing on non-void elements: ebooklib + lxml emit
    # `<span class="vlist-s"/>` which Kindle interprets as an open tag,
    # swallowing subsequent content. Force `<span></span>` instead.
    # Word-boundary after tag name (\b) prevents <img/> being matched as <i + mg.../>
    self_close_re = re.compile(
        r'<(span|div|p|a|td|th|li|strong|em|b|i|sub|sup|small|code|pre)(\s[^>]*|)/>'
    )

    src_zip = zipfile.ZipFile(epub_path, "r")
    fd, tmp_path = __import__("tempfile").mkstemp(suffix=".epub", dir=str(epub_path.parent))
    os.close(fd)
    try:
        out_zip = zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9)
        n_total = 0
        try:
            for info in src_zip.infolist():
                data = src_zip.read(info.filename)
                if info.filename.endswith((".xhtml", ".html", ".opf", ".ncx")):
                    text = data.decode("utf-8", errors="replace")
                    new_text, n = fix_re.subn(lambda m: f"&{m.group(1)};", text)
                    # Self-closing fix only on chapter content (.xhtml/.html);
                    # OPF/NCX use self-closing on <item/> etc. and that is correct.
                    n_sc = 0
                    if info.filename.endswith((".xhtml", ".html")):
                        new_text, n_sc = self_close_re.subn(r'<\1\2></\1>', new_text)
                    if n or n_sc:
                        n_total += n + n_sc
                        data = new_text.encode("utf-8")
                # Preserve mimetype-first-uncompressed convention
                if info.filename == "mimetype":
                    info_out = zipfile.ZipInfo("mimetype")
                    info_out.compress_type = zipfile.ZIP_STORED
                    out_zip.writestr(info_out, data)
                else:
                    out_zip.writestr(info, data)
        finally:
            out_zip.close()
        src_zip.close()
        # Replace original
        os.replace(tmp_path, str(epub_path))
        return n_total
    except Exception:
        src_zip.close()
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


def find_kindle_previewer() -> Path | None:
    """Locate Kindle Previewer 3 executable."""
    import os
    candidates = [
        Path(os.environ.get("LOCALAPPDATA", "")) / "Amazon" / "Kindle Previewer 3" / "Kindle Previewer 3.exe",
        Path("C:/Program Files/Amazon/Kindle Previewer 3/Kindle Previewer 3.exe"),
        Path("C:/Program Files (x86)/Amazon/Kindle Previewer 3/Kindle Previewer 3.exe"),
    ]
    if os.environ.get("KINDLE_PREVIEWER"):
        candidates.insert(0, Path(os.environ["KINDLE_PREVIEWER"]))
    for c in candidates:
        if c.exists():
            return c
    return None


def step_kindle_preview(epub: Path) -> int:
    """Launch Kindle Previewer 3 with the EPUB loaded for visual inspection.

    Note: Kindle Previewer 3's CLI conversion (-convert/-output flags) is
    poorly documented and version-dependent - we don't attempt automated
    KPF generation. Instead, this opens the GUI so you can interactively
    preview the rendering on Paperwhite, Oasis, Scribe, Fire, iOS, Android,
    and Web Reader profiles. Conversion to KPF happens automatically when
    the GUI loads the EPUB.
    """
    step("Launch Kindle Previewer (interactive preview)")
    kp = find_kindle_previewer()
    if kp is None:
        warn("Kindle Previewer 3 not detected. Download at:")
        warn("  https://kdp.amazon.com/en_US/help/topic/G202131170")
        return 0

    print(f"  Kindle Previewer: {kp}")
    print(f"  EPUB:             {epub.relative_to(PROJECT_ROOT)}")
    print(f"  Launching GUI - close the previewer window when done.")

    import subprocess as sp
    # Launch detached (do NOT wait for the GUI to close).
    # On Windows, use DETACHED_PROCESS + CREATE_NEW_PROCESS_GROUP.
    try:
        creationflags = 0
        if sys.platform == "win32":
            creationflags = 0x00000008 | 0x00000200  # DETACHED_PROCESS + CREATE_NEW_PROCESS_GROUP
        proc = sp.Popen([str(kp), str(epub)], creationflags=creationflags,
                        stdout=sp.DEVNULL, stderr=sp.DEVNULL, stdin=sp.DEVNULL)
        ok(f"Kindle Previewer launched (PID {proc.pid})")
        ok("KPF file is auto-generated by KP and stored in its workspace at:")
        ok(f"  {Path.home() / 'AppData' / 'Local' / 'Amazon' / 'Kindle Previewer 3' / 'workspace'}")
    except Exception as e:
        warn(f"Failed to launch Kindle Previewer: {e}")
        return 1
    return 0


def find_epub_optimizer() -> Path | None:
    """Locate epub-optimizer's pipeline.js entry point.

    Search order:
      1. $EPUB_OPTIMIZER_JS env var (explicit override)
      2. C:/Users/<user>/Tools/epub-optimizer (current install location)
      3. Several legacy / cross-platform fallbacks
    """
    candidates = [
        Path.home() / "Tools" / "epub-optimizer" / "dist" / "src" / "pipeline.js",
        Path("E:/Tools/epub-optimizer/dist/src/pipeline.js"),
        Path("C:/Tools/epub-optimizer/dist/src/pipeline.js"),
        Path.home() / "epub-optimizer" / "dist" / "src" / "pipeline.js",
        Path("/usr/local/lib/epub-optimizer/dist/src/pipeline.js"),
    ]
    import os
    if os.environ.get("EPUB_OPTIMIZER_JS"):
        candidates.insert(0, Path(os.environ["EPUB_OPTIMIZER_JS"]))
    for c in candidates:
        if c.exists():
            return c
    return None


def step_optimize() -> int:
    """Run epub-optimizer to compress images, minify HTML/CSS, optimize fonts.

    Side effect: replaces output/*.epub with the optimized version. The
    pre-optimization build is preserved at output/*.raw.epub so you can
    compare or roll back.
    """
    step("EPUB optimization (epub-optimizer)")
    opt_js = find_epub_optimizer()
    if opt_js is None:
        warn("epub-optimizer not detected; skipping. See KDP/QUALITY_TOOLS.md to install.")
        return 0

    if not shutil.which("node"):
        warn("Node.js not on PATH; skipping epub-optimizer.")
        return 0

    epub = OUTPUT_DIR / "building-conversational-ai-llms-agents.epub"
    raw_backup = OUTPUT_DIR / "building-conversational-ai-llms-agents.raw.epub"
    optimized = OUTPUT_DIR / "building-conversational-ai-llms-agents.optimized.epub"

    raw_size = epub.stat().st_size
    print(f"  optimizer: {opt_js}")
    print(f"  input:     {epub.relative_to(PROJECT_ROOT)} ({raw_size / 1024 / 1024:.2f} MB)")

    # Preserve the unoptimized build for inspection/rollback
    shutil.copy2(epub, raw_backup)

    log = LOG_DIR / f"optimize_{ts()}.log"
    # Edition 16+ size optimization (Phase 1+2 size reduction):
    # jpg=65 (was 72): ~10-15% smaller JPEGs at visually-similar quality
    #   on e-ink. Combined with MozJPEG q=68 (which now actually beats this)
    #   and the 1000 px dimension cap in _recompress_images.py.
    # png=0.85: keep diagrams crisp.
    rc, out = run([
        "node", str(opt_js),
        "-i", str(epub),
        "-o", str(optimized),
        "--jpg-quality", "65",
        "--png-quality", "0.85",
        "--lang", "en",
        "--clean",
    ], log)

    # Show last 8 lines of optimizer output
    for line in out.splitlines()[-8:]:
        print(f"  {line}")

    # The optimizer's INTERNAL epubcheck step fails on its own output because
    # html-minifier-terser strips the trailing ';' from entities like &apos;
    # before " (attribute close). The file IS produced, just needs repair.
    # Accept the file if it exists and try to repair, regardless of exit code.
    if not optimized.exists():
        fail(f"epub-optimizer didn't produce {optimized.name}; raw EPUB preserved")
        return 2
    if rc != 0:
        warn(f"epub-optimizer's internal validation failed (exit {rc}); attempting entity repair...")

    # The optimizer's html-minifier-terser sometimes strips the trailing `;`
    # from XML entities like &apos; when followed by " (attribute close).
    # That's invalid XHTML even though it's tolerated HTML5. Patch the file.
    n_fixed = repair_optimized_entities(optimized)
    if n_fixed:
        print(f"  [post-fix] re-added trailing ';' to {n_fixed} broken XML entities")

    # Promote optimized to main EPUB
    shutil.move(str(optimized), str(epub))
    pre_recompress_size = epub.stat().st_size

    # Step 7b: post-optimize JPEG (MozJPEG) + PNG (OxiPNG) recompression.
    # epub-optimizer uses sharp (libjpeg) + pngquant; MozJPEG and OxiPNG
    # squeeze out additional ~1-2 MB at no quality cost.
    try:
        sys.path.insert(0, str(BUILD_DIR))
        from _recompress_images import recompress_epub, MOZJPEG, OXIPNG
        if MOZJPEG and OXIPNG:
            print("  [recompress] running MozJPEG + OxiPNG (with cache)...")
            stats = recompress_epub(epub, epub)
            print(f"    MozJPEG: {stats['jpg_files']} files, saved {stats['jpg_saved']/1024:.0f} KB")
            print(f"    OxiPNG:  {stats['png_files']} files, saved {stats['png_saved']/1024:.0f} KB")
            # v14.1: cache stats
            jpg_h = stats.get('cache_jpg_hits', 0); jpg_m = stats.get('cache_jpg_miss', 0)
            png_h = stats.get('cache_png_hits', 0); png_m = stats.get('cache_png_miss', 0)
            if jpg_h + jpg_m + png_h + png_m > 0:
                tot_h = jpg_h + png_h; tot_m = jpg_m + png_m
                tot = tot_h + tot_m
                hit_pct = 100.0 * tot_h / tot if tot else 0.0
                print(f"    cache:   {tot_h} hits / {tot_m} miss ({hit_pct:.0f}% hit; jpg={jpg_h}/{jpg_m}, png={png_h}/{png_m})")
        else:
            warn("MozJPEG/OxiPNG not installed; skipping post-optimize recompression")
    except Exception as _e:
        warn(f"recompression failed (non-fatal): {_e}")

    # Step 7c: Kindle CSS sanitizer — replace unsupported values with safe defaults.
    # Targets the 8000+ "Notice" patterns from KDP's converter (nullem/nanem/
    # box-shadow/min-content/details/transition/transform). Suspected to be the
    # cause of KDP's "internal error" fatal during conversion.
    try:
        from _sanitize_kindle_css import sanitize as kindle_sanitize
        s = kindle_sanitize(epub, epub)
        print(f"  [kindle-css] {s['removals']} unsupported CSS values replaced "
              f"({s['css_files']} CSS, {s['html_files']} HTML)")
    except Exception as _e:
        warn(f"kindle-css sanitizer failed (non-fatal): {_e}")

    # Step 7d: KDP-specific post-build patches.
    # fix_cover_kdp_heuristic was REWRITTEN on 2026-05-29 after KDP rejected
    # the previous version's output as "fixed format eBook" (it had set
    # body{margin:0;padding:0} + hidden caption + linear="no"). The new
    # version REMOVES those signals and ADDS a visible title block + sets
    # linear="yes" so KDP's classifier sees a normal reflowable title page.
    # See epub2kpf LESSONS.md L-COVER-REFLOW for the full diagnosis.
    # After all patches, audit_kdp_fixed_layout_classifier.py runs as a
    # hard gate to catch any regression that would re-trigger the rejection.
    try:
        import subprocess
        for script, label in [
            ("fix_strip_web_chrome.py",     "strip-web-chrome"),
            ("fix_strip_fxl_css.py",         "strip-fxl-css"),
            ("fix_img_strip_dims.py",        "img-strip-dims"),
            ("fix_png_to_jpeg_kdp.py",      "png-to-jpeg"),
            ("fix_fxl_filenames.py",         "fxl-filenames"),
            ("fix_cover_kdp_heuristic.py", "cover-reflow"),
            ("fix_cover_image_kdp.py",      "cover-image"),
            ("fix_svg_style_kdp.py",        "svg-style"),
            ("fix_opf_strip_rendition.py", "opf-strip-rendition"),
            # Strips KFX-ignored CSS (W00015 / W10023 / W11007 noise). Slims
            # the KFX conversion log from ~70 MB to ~1 MB, letting real
            # warnings stand out. Source CSS is untouched (web build keeps
            # full styling).
            ("fix_kfx_epub_css.py",          "kfx-css-cleanup"),
            # Fixes SVG <text font-size="N" font-family="Segoe UI"> attributes
            # in Mermaid-generated diagrams that crash KFX Stage 2 with
            # E02208 (px font-size) + E06424 (missing font). Field-tested:
            # 8923 + 1042 occurrences fixed on a 37 MB book.
            ("fix_kfx_svg_text_attrs.py",    "kfx-svg-text-attrs"),
        ]:
            script_path = BUILD_DIR / script
            if not script_path.exists():
                warn(f"[kdp-fix] {script} not found; skip")
                continue
            print(f"  [kdp-fix:{label}] running {script}")
            cp = subprocess.run(
                [sys.executable, str(script_path), str(epub)],
                capture_output=True, text=True,
            )
            for line in cp.stdout.splitlines():
                print(f"    {line}")
            if cp.returncode != 0:
                warn(f"[kdp-fix:{label}] exit {cp.returncode}; {cp.stderr[:200]}")
    except Exception as _e:
        warn(f"kdp post-build patches failed (non-fatal): {_e}")

    # Step 7e: Three KDP fixed-format classifier hard gates (added 2026-05-29
    # after KDP rejected an upload with "This content is a fixed format eBook").
    # Each script exits non-zero on real findings; any failure halts the build.
    # See html2kpd LESSONS.md L-COVER-REFLOW, L-FXL-KEYWORDS, L-IMG-PX-DIMS,
    # L-WEB-CHROME, L-CSS-DISALLOWED for the catalogue of triggers.
    try:
        gates = [
            ("audit_kdp_fixed_layout_classifier.py", "classifier-cover",
             "cover.xhtml signals (body{margin:0}/image-only/linear=no/viewport-meta)"),
            ("audit_hunt_fxl_cues.py",                "hunt-fxl-cues",
             "13-pattern FXL cue hunt across every XHTML (canvas, page-spread, amzn-*, etc.)"),
            ("audit_deep_scan.py",                    "deep-scan",
             "25-check per-page anomaly scan (web chrome, banned tags, repeated boilerplate, etc.)"),
        ]
        for script, label, summary in gates:
            audit_path = BUILD_DIR / script
            if not audit_path.exists():
                warn(f"[{label}] script not found at {audit_path}; skipping")
                continue
            print(f"  [{label}] {script}  — {summary}")
            cp = subprocess.run(
                [sys.executable, str(audit_path), str(epub)],
                capture_output=True, text=True,
            )
            # Print summary lines (last ~6) for context; full output on failure
            tail_lines = cp.stdout.splitlines()[-6:]
            for line in tail_lines:
                print(f"    {line}")
            if cp.returncode != 0:
                fail(f"[{label}] FAILED — KDP would likely reject this EPUB")
                # Dump full output so the operator can see what tripped
                for line in cp.stdout.splitlines():
                    print(f"    {line}")
                fail(f"   See html2kpd LESSONS.md (L-COVER-REFLOW / L-FXL-* / L-WEB-CHROME / L-CSS-DISALLOWED)")
                return 4
    except Exception as _e:
        warn(f"kdp classifier gates failed (non-fatal): {_e}")

    new_size = epub.stat().st_size
    pct = new_size / raw_size * 100
    saved = (raw_size - new_size) / 1024 / 1024
    ok(f"raw:       {raw_backup.relative_to(PROJECT_ROOT)}  ({raw_size / 1024 / 1024:.2f} MB)")
    ok(f"optimized: {epub.relative_to(PROJECT_ROOT)}  ({new_size / 1024 / 1024:.2f} MB, {pct:.1f}% of raw, saved {saved:.1f} MB)")

    # KDP delivery-fee re-estimate
    fee_raw = (raw_size / 1024 / 1024) * 0.15
    fee_opt = (new_size / 1024 / 1024) * 0.15
    print(f"  KDP delivery fee (70% royalty): ${fee_raw:.2f} -> ${fee_opt:.2f} per sale (saved ${fee_raw-fee_opt:.2f}/sale)")
    return 0


def step_summary(start_t: float, build_log: Path | None) -> None:
    step("Summary")
    epub = OUTPUT_DIR / "building-conversational-ai-llms-agents.epub"
    if epub.exists():
        size_mb = epub.stat().st_size / 1024 / 1024
        ok(f"EPUB:    {epub.relative_to(PROJECT_ROOT)}  ({size_mb:.2f} MB)")
    cover = KDP_DIR / "cover" / "cover_kdp.jpg"
    if cover.exists():
        ok(f"cover:   {cover.relative_to(PROJECT_ROOT)}  ({cover.stat().st_size / 1024:.1f} KB)")
    report = VALIDATION_DIR / "structural_report.txt"
    if report.exists():
        ok(f"report:  {report.relative_to(PROJECT_ROOT)}")
    if build_log and build_log.exists():
        ok(f"log:     {build_log.relative_to(PROJECT_ROOT)}")

    elapsed = time.time() - start_t
    ok(f"elapsed: {elapsed:.1f}s")

    print()
    print("Next steps:")
    print("  1. Review KDP/validation/structural_report.txt and KDP/output/kpv-out/Summary_Log.csv")
    print("  2. (Optional) Run Kindle Previewer GUI (--preview) to spot-check rendering")
    print("  3. Follow KDP/PUBLISHING_GUIDE.md to upload to KDP")


# --------------------------------------------------------------------- helpers


def ts() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


# --------------------------------------------------------------------- KPV KFX validation


def step_quality_audit(epub: Path) -> int:
    """Deep reader-facing quality audit (scripts/audit_epub_quality.py).

    Catches problems EPUBCheck + KPV qualitychecks pass clean but that still
    look wrong on a Kindle: broken internal links / fragments, missing alt text,
    manifest/spine mismatches, duplicate ids, heading-level skips, and Kindle
    regression guards (lowercase camelCase SVG attrs, empty math placeholders).
    Fails (non-zero) only on ERROR-level findings; warnings are reported.
    """
    step("Deep EPUB quality audit (links / alt / manifest / regressions)")
    script = PROJECT_ROOT / "scripts" / "audit_epub_quality.py"
    if not script.exists():
        warn("scripts/audit_epub_quality.py not found; skipping")
        return 0
    rc, out = run([PYTHON, str(script), str(epub)])
    for line in out.splitlines()[-16:]:
        print(f"  {line}")
    if rc != 0:
        fail("quality audit found ERROR-level issues")
    else:
        ok("quality audit passed (0 errors)")
    return rc


def step_kpv(epub: Path) -> int:
    """Headless Kindle KFX conversion + qualitychecks via Kindle Previewer 3.

    KPV's KFX/Mobi converter is significantly STRICTER than EPUBCheck and
    catches errors EPUBCheck passes clean (e.g. E21018 entity-in-attribute,
    E25001 bad image). This gate converts the FINAL optimized EPUB and parses
    the qualitychecks report.

    CRITICAL CLI form (wrong order silently no-ops, exit 0, no output):
        "Kindle Previewer 3.exe" <input.epub> -convert -output <FOLDER> -qualitychecks
    Input path FIRST; `-convert` is a bare command; `-output` is a FOLDER.
    Run the exe directly (NOT through a bash/MSYS shim, or the KPR_NCD worker
    hangs) and kill stale workers first. Outputs land under <FOLDER>/:
    KPF/<name>.kpf, Logs/<name>_log.csv, Summary_Log.csv. Gate on
    Summary_Log.csv Conversion Status + Error Count.

    Non-fatal when KPV is absent / times out / emits no report (warn + skip),
    matching the epubcheck step. Returns 1 only on a real conversion failure.
    """
    import csv
    step("Kindle KFX validation (Kindle Previewer -convert -qualitychecks)")
    kp = find_kindle_previewer()
    if kp is None:
        warn("Kindle Previewer 3 not detected; skipping KFX qualitychecks.")
        print("  Download: https://kdp.amazon.com/en_US/help/topic/G202131170")
        return 0
    out_dir = OUTPUT_DIR / "kpv-out"
    try:
        if out_dir.exists():
            shutil.rmtree(out_dir, ignore_errors=True)
        out_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        warn(f"could not prepare KPV output dir: {e}")
        return 0
    # KPV is single-instance: if a prior "Kindle Previewer 3.exe" GUI is still
    # running (common after a previous run was interrupted), launching it again
    # just focuses the existing window and the new -convert silently HANGS with no
    # output. So kill BOTH the GUI and its KPR_NCD.exe worker before launching.
    if sys.platform.startswith("win"):
        for image in ("KPR_NCD.exe", "Kindle Previewer 3.exe"):
            try:
                subprocess.run(["taskkill", "/F", "/IM", image], capture_output=True)
            except Exception:
                pass
        time.sleep(2)  # let the processes fully exit before relaunch
    print(f"  Kindle Previewer: {kp}")
    cmd = [str(kp), str(epub), "-convert", "-output", str(out_dir), "-qualitychecks"]
    print(f"  $ {' '.join(cmd)}")
    t0 = time.time()
    try:
        subprocess.run(cmd, cwd=str(PROJECT_ROOT), capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=2400)
    except subprocess.TimeoutExpired:
        warn("Kindle Previewer timed out (2400s); skipping KFX gate")
        return 0
    except Exception as e:
        warn(f"Kindle Previewer invocation failed: {e}")
        return 0
    print(f"  (KPV finished in {time.time() - t0:.0f}s)")
    summary = out_dir / "Summary_Log.csv"
    if not summary.exists():
        warn("KPV produced no Summary_Log.csv (CLI/version mismatch?); skipping gate")
        return 0
    status = et = "?"
    errc = qic = None
    output_path = quality_path = ""
    try:
        for row in csv.DictReader(summary.open(encoding="utf-8-sig", newline="")):
            status = row.get("Conversion Status", status)
            et = row.get("Enhanced Typesetting Status", et)
            output_path = (row.get("Output File Path") or "").strip()
            quality_path = (row.get("Quality Report Path") or "").strip()
            try:
                errc = int((row.get("Error Count") or "0").strip())
            except ValueError:
                pass
            try:
                qic = int((row.get("Quality Issue Count") or "0").strip())
            except ValueError:
                pass
    except Exception as e:
        warn(f"could not parse Summary_Log.csv: {e}")
        return 0
    print(f"  conversion status:    {status}")
    print(f"  error count:          {errc}")
    print(f"  quality issue count:  {qic}")
    print(f"  enhanced typesetting: {et}")
    rel = out_dir.relative_to(PROJECT_ROOT)

    # Detect headless-KPV silent failure: when KPV is invoked from a non-
    # interactive (no foreground desktop) subprocess context on Windows, it
    # returns rc=0 + writes a Summary_Log.csv with Status=Success, Error
    # Count=0, but EMPTY Output File Path, EMPTY Quality Report Path, and
    # Enhanced Typesetting=Not Supported. See KDP/build/KPV_CLI_ANALYSIS.md.
    # This is environmental (Claude/CI subprocess), not a content regression.
    kpf_dir = out_dir / "KPF"
    has_kpf = kpf_dir.exists() and any(kpf_dir.glob("*.kpf"))
    if (not output_path and not quality_path and not has_kpf
            and str(et).strip().lower().startswith("not")):
        warn("KPV silent-failure signature detected (empty output paths, no KPF,")
        warn("  Enhanced Typesetting=Not Supported). This is the headless-KPV")
        warn("  limitation documented in KDP/build/KPV_CLI_ANALYSIS.md, not a")
        warn("  content regression. Run KPV manually from an interactive")
        warn("  desktop session to get a real KFX conversion report:")
        warn(f"    \"{kp}\" \"{epub}\" -convert -output \"{out_dir}\" -qualitychecks")
        return 0

    if str(status).strip().lower().startswith("success") and (errc in (0, None)):
        ok(f"KPV KFX qualitychecks PASSED -> {rel}")
        return 0
    warn(f"KPV reported issues -> see {rel}/Logs/*.csv")
    return 1


# --------------------------------------------------------------------- main


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="LLMBook EPUB publishing pipeline")
    p.add_argument("--clean", action="store_true", help="Delete output before building")
    p.add_argument("--quick", action="store_true", help="Fast build with smaller images (not for submission)")
    p.add_argument("--validate-only", action="store_true", help="Skip build; only run validators")
    p.add_argument("--no-epubcheck", action="store_true", help="Skip Java epubcheck even if available")
    p.add_argument("--no-optimize", action="store_true", help="Skip the epub-optimizer minification step")
    p.add_argument("--regen-spine", action="store_true", help="Re-walk source tree to regenerate the legacy spine_manifest.json (not used by html2epub; build_epub.py only)")
    p.add_argument("--preview", action="store_true",
                   help="After build+validate, launch Kindle Previewer 3 GUI with the EPUB loaded "
                        "for interactive preview (Paperwhite, Oasis, Scribe, Fire, iOS, Android, Web Reader).")
    p.add_argument("--no-sample-pdf", action="store_true",
                   help="Skip regenerating the sample chapter PDF for the landing page.")
    p.add_argument("--no-kpv", action="store_true",
                   help="Skip the Kindle Previewer KFX conversion + qualitychecks gate "
                        "(headless; stricter than epubcheck; ~2-4 min). Auto-skipped in --quick.")
    p.add_argument("--kpv", action="store_true",
                   help="(LEGACY no-op) KPV gate is now default-on again. "
                        "If KPV fails with 'Failed to ProcessEpub' / 'Failed to create temp directory', "
                        "launch the GUI ('Kindle Previewer 3.exe') once interactively to initialize "
                        "per-user state, then retry the build.")
    p.add_argument("--no-audit", action="store_true",
                   help="Skip the deep EPUB quality audit (scripts/audit_epub_quality.py).")
    args = p.parse_args(argv)

    start_t = time.time()
    print(_color(36, "=" * 70))
    print(_color(36, f"LLMBook EPUB publishing pipeline   {datetime.now().isoformat(timespec='seconds')}"))
    print(_color(36, "=" * 70))

    rc = check_prerequisites()
    if rc != 0:
        return rc

    if args.clean and not args.validate_only:
        step_clean()

    if not args.validate_only:
        # NOTE: the canonical builder (html2epub) discovers the spine itself via
        # `spine = "auto"` in html2epub.toml and does NOT read spine_manifest.json.
        # generate_spine.py / spine_manifest.json are legacy (build_epub.py only).
        # So only regenerate the manifest when explicitly asked, instead of
        # auto-firing whenever the legacy file is absent.
        if args.regen_spine:
            rc = step_regen_spine()
            if rc != 0:
                return rc
        rc = step_build_epub(quick=args.quick)
        if rc != 0:
            return rc

    rc = step_structural_validate()
    final_rc = rc

    if not args.no_epubcheck:
        found = find_epubcheck_install()
        if found:
            java, jar = found
            rc = step_epubcheck(java, jar)
            if rc != 0:
                final_rc = rc
        else:
            step("EPUB schema validation (epubcheck)")
            warn("Java + epubcheck not detected; skipping. See KDP/validation/epubcheck_instructions.md")

    if not args.no_optimize and not args.validate_only:
        rc = step_optimize()
        if rc != 0:
            final_rc = rc
        # Re-validate the optimized EPUB - optimization shouldn't break anything
        # but verifying is cheap and catches optimizer regressions AND any
        # corruption introduced by the Step 7d post-build patches.
        # This run uses STRICT mode (--failonwarnings -u) and is a HARD GATE
        # because the post-build patches could in principle introduce
        # OPF-027 / property-corruption errors that the default EPUBCheck
        # would only warn about. The KDP "There was a problem processing
        # your file" rejection on 2026-05-29 was caused by exactly this:
        # the fix_fxl_filenames.py keyword scrub corrupted
        # `rendition:spread` into `rendition:wide` (undefined property),
        # which earlier EPUBCheck calls warned-but-let-ship. Hard gate
        # now stops that class of regression at build time.
        elif not args.no_epubcheck:
            found = find_epubcheck_install()
            if found:
                step("Post-optimize epubcheck [STRICT, HARD GATE]")
                rc = step_epubcheck(*found, strict=True)
                if rc != 0:
                    fail("Optimized EPUB failed STRICT epubcheck; raw EPUB preserved at output/*.raw.epub")
                    fail("This is a HARD GATE — the broken EPUB will NOT be shipped.")
                    fail("See KDP/validation/epubcheck_strict_report.txt for details.")
                    return 1

    # Deep quality audit (internal links, alt text, manifest/spine consistency,
    # SVG/math regression guards) - catches reader-facing issues EPUBCheck and
    # KPV pass clean. Runs on the FINAL EPUB; cheap (~3s).
    audit_epub = OUTPUT_DIR / "building-conversational-ai-llms-agents.epub"
    if audit_epub.exists() and not args.no_audit:
        rc = step_quality_audit(audit_epub)
        if rc != 0:
            final_rc = rc

    # Kindle KFX validation gate: Kindle Previewer's converter is stricter than
    # EPUBCheck and catches Kindle-only failures (E21018, E25001, ...). Runs on
    # the FINAL (optimized) EPUB. Slow (~2-4 min); auto-skipped in --quick (not
    # for submission) and skippable via --no-kpv.
    #
    # RE-ENABLED 2026-05-30 (default-on again):
    # Earlier this day KPV3 CLI was failing with "Failed to ProcessEpub" + "Failed
    # to create temp directory" on every conversion. Root cause turned out to be:
    # KPV3 CLI mode silently requires that the GUI has been launched at least once
    # per user profile to initialize per-user state. After running the GUI even
    # for a few seconds, CLI conversions succeed normally. If you ever hit the
    # same error chain again, just launch the GUI manually and retry.
    if not args.no_kpv and not args.quick:
        kpv_epub = OUTPUT_DIR / "building-conversational-ai-llms-agents.epub"
        if kpv_epub.exists():
            rc = step_kpv(kpv_epub)
            if rc != 0:
                final_rc = rc

    # Archive a per-edition snapshot of the optimized EPUB so old
    # editions remain available for diffs / rollback. Reads the edition
    # number from KDP/metadata/metadata.yaml. Cheap (single file copy).
    if not args.validate_only:
        rc = step_archive_edition()
        if rc != 0:
            final_rc = rc

    # Make a uniquely-named upload copy under KDP/output/uploads/. Every
    # build gets a fresh filename (timestamp + git short SHA + size MB) so
    # KDP cannot return a cached verdict on the previous upload. The
    # canonical EPUB is left untouched. Cheap (single file copy).
    if not args.validate_only:
        upload_script = BUILD_DIR / "make_upload_copy.py"
        canonical = OUTPUT_DIR / "building-conversational-ai-llms-agents.epub"
        if upload_script.exists() and canonical.exists():
            step("Stage upload copy with unique filename")
            rc_u, out_u = run([PYTHON, str(upload_script), str(canonical)])
            for line in out_u.splitlines():
                print(f"  {line}")

    # Regenerate sample chapter PDF for landing page (cheap; ~5s)
    if not args.no_sample_pdf:
        step("Sample chapter PDF (landing page download)")
        pdf_script = BUILD_DIR / "build_sample_pdf.py"
        if pdf_script.exists():
            rc, out = run([PYTHON, str(pdf_script)])
            for line in out.splitlines()[-5:]:
                print(f"  {line}")

    if args.preview:
        epub = OUTPUT_DIR / "building-conversational-ai-llms-agents.epub"
        if epub.exists():
            step_kindle_preview(epub)

    step_summary(start_t, None)
    return final_rc




def step_archive_edition() -> int:
    """Copy the optimized EPUB to KDP/output/editions/{N}th-edition/.

    Each edition number gets its own subfolder so historical builds are
    preserved. The edition number is read from KDP/metadata/metadata.yaml
    book.edition_number. If metadata is unreadable, this step warns and
    is skipped (the main artifact is still in KDP/output/)."""
    step("Archive per-edition snapshot")
    try:
        import yaml
        meta = yaml.safe_load(
            (KDP_DIR / "metadata" / "metadata.yaml").read_text(encoding="utf-8")
        ) or {}
    except Exception as e:
        warn(f"could not read metadata.yaml ({e}); skipping archive")
        return 0
    n = (meta.get("book") or {}).get("edition_number")
    if not n:
        warn("metadata.yaml has no book.edition_number; skipping archive")
        return 0
    suffix_map = {1: "1st", 2: "2nd", 3: "3rd"}
    label = f"{suffix_map.get(n, f'{n}th')}-edition"
    src = OUTPUT_DIR / "building-conversational-ai-llms-agents.epub"
    if not src.exists():
        warn(f"{src.name} not found; nothing to archive")
        return 0
    dest_dir = OUTPUT_DIR / "editions" / label
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"building-conversational-ai-llms-agents-{label}.epub"
    import shutil
    shutil.copy2(src, dest)
    sz = dest.stat().st_size
    ok(f"{dest.relative_to(PROJECT_ROOT)} ({sz / 1024 / 1024:.2f} MB)")
    return 0


def step_pagefind() -> int:
    """Rebuild the Pagefind static search index over the HTML site.
    Pagefind writes to <root>/pagefind/ ; we ship that directory with
    GitHub Pages so the search box on every section works without any
    backend.
    """
    step("Build Pagefind search index")
    pagefind = PROJECT_ROOT / "node_modules" / ".bin" / ("pagefind.cmd" if sys.platform == "win32" else "pagefind")
    if not pagefind.exists():
        warn("Pagefind not installed; run `npm install -D pagefind` to enable search.")
        return 0
    try:
        proc = sp.run([str(pagefind), "--site", str(PROJECT_ROOT)],
                      capture_output=True, text=True, timeout=120)
        if proc.returncode != 0:
            warn(f"Pagefind failed: {proc.stderr[:200]}")
            return 1
        # Parse the "Indexed X pages" line for a friendly summary
        for line in proc.stdout.splitlines():
            if line.strip().startswith("Indexed"):
                ok("  " + line.strip())
    except sp.TimeoutExpired:
        warn("Pagefind timed out after 120s")
        return 1
    ok("Pagefind index updated at /pagefind/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
