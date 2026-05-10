"""
Publishing pipeline orchestrator.

Single entry point that does the full HTML -> validated EPUB flow.
Designed for repeated runs as the source HTML evolves.

Usage:
    python KDP/build/publish.py                # full build + validation
    python KDP/build/publish.py --quick        # smaller images, faster
    python KDP/build/publish.py --validate-only  # skip rebuild
    python KDP/build/publish.py --clean        # delete output then rebuild
    python KDP/build/publish.py --no-epubcheck # skip Java epubcheck even if installed
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


def run(cmd: list[str], log_path: Path | None = None) -> tuple[int, str]:
    """Run a subprocess; capture combined output. Tee to log file if given."""
    print(f"  $ {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=str(PROJECT_ROOT), capture_output=True, text=True, encoding="utf-8")
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

    # Required source files
    required = [
        KDP_DIR / "metadata" / "metadata.yaml",
        KDP_DIR / "cover" / "cover_kdp.jpg",
        BUILD_DIR / "build_epub.py",
        BUILD_DIR / "epub_overrides.css",
        PROJECT_ROOT / "styles" / "book.css",
    ]
    for p in required:
        if p.exists():
            ok(f"file: {p.relative_to(PROJECT_ROOT)}")
        else:
            fail(f"missing: {p.relative_to(PROJECT_ROOT)}")
            return 3

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
        ec_jars = sorted(d.glob("epubcheck-*/epubcheck.jar")) + sorted(d.glob("epubcheck.jar"))
        if not ec_jars:
            continue
        ec_jar = ec_jars[0]

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
    step("Regenerating spine manifest")
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
    step("Building EPUB (html2pub)")
    # Canonical builder is the html2pub package (KDP/html2pub/), driven by html2pub.toml at the project root.
    cmd = [PYTHON, "-m", "html2pub", "build", str(PROJECT_ROOT)]
    if quick:
        warn("quick mode requested — html2pub honors [images] settings in html2pub.toml; "
             "for smaller files temporarily lower max_side/jpeg_quality and re-run.")

    log = LOG_DIR / f"build_{ts()}.log"
    rc, out = run(cmd, log)
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


def step_epubcheck(java: Path, jar: Path) -> int:
    step("EPUB schema validation (epubcheck)")
    epub = OUTPUT_DIR / "building-conversational-ai-llms-agents.epub"
    log = VALIDATION_DIR / "epubcheck_report.txt"
    # Use a project-local Java temp dir so we don't depend on the system
    # %TEMP% having free space (C: drive can be tight on Windows).
    java_tmp = LOG_DIR / "java-tmp"
    java_tmp.mkdir(parents=True, exist_ok=True)
    print(f"  java:      {java}")
    print(f"  epubcheck: {jar}")
    rc, out = run(
        [str(java), f"-Djava.io.tmpdir={java_tmp}", "-jar", str(jar), str(epub)],
        log,
    )
    # epubcheck prints a final summary line; show last 30 lines
    tail = out.splitlines()[-30:]
    print("  " + "\n  ".join(tail))
    if rc == 0:
        ok(f"epubcheck PASSED -> {log.relative_to(PROJECT_ROOT)}")
    else:
        warn(f"epubcheck reported issues -> see {log.relative_to(PROJECT_ROOT)}")
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
                    if n:
                        n_total += n
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
    # Quality-conscious settings: optimizer defaults (jpg=70 / png=0.6) lose
    # too much fidelity on diagrams and photos. 80/0.85 keeps the file looking
    # right while still saving ~35% over the unoptimized build.
    rc, out = run([
        "node", str(opt_js),
        "-i", str(epub),
        "-o", str(optimized),
        "--jpg-quality", "80",
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
            print("  [recompress] running MozJPEG + OxiPNG...")
            stats = recompress_epub(epub, epub)
            print(f"    MozJPEG: {stats['jpg_files']} files, saved {stats['jpg_saved']/1024:.0f} KB")
            print(f"    OxiPNG:  {stats['png_files']} files, saved {stats['png_saved']/1024:.0f} KB")
        else:
            warn("MozJPEG/OxiPNG not installed; skipping post-optimize recompression")
    except Exception as _e:
        warn(f"recompression failed (non-fatal): {_e}")

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
    print("  1. Review KDP/validation/structural_report.txt")
    print("  2. (Optional) Run Kindle Previewer locally to spot-check rendering")
    print("  3. Follow KDP/PUBLISHING_GUIDE.md to upload to KDP")


# --------------------------------------------------------------------- helpers


def ts() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


# --------------------------------------------------------------------- main


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="LLMBook EPUB publishing pipeline")
    p.add_argument("--clean", action="store_true", help="Delete output before building")
    p.add_argument("--quick", action="store_true", help="Fast build with smaller images (not for submission)")
    p.add_argument("--validate-only", action="store_true", help="Skip build; only run validators")
    p.add_argument("--no-epubcheck", action="store_true", help="Skip Java epubcheck even if available")
    p.add_argument("--no-optimize", action="store_true", help="Skip the epub-optimizer minification step")
    p.add_argument("--regen-spine", action="store_true", help="Re-walk source tree to regenerate spine_manifest.json")
    p.add_argument("--preview", action="store_true",
                   help="After build+validate, launch Kindle Previewer 3 GUI with the EPUB loaded "
                        "for interactive preview (Paperwhite, Oasis, Scribe, Fire, iOS, Android, Web Reader).")
    p.add_argument("--no-sample-pdf", action="store_true",
                   help="Skip regenerating the sample chapter PDF for the landing page.")
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
        if args.regen_spine or not (BUILD_DIR / "spine_manifest.json").exists():
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
        # but verifying is cheap and catches optimizer regressions
        elif not args.no_epubcheck:
            found = find_epubcheck_install()
            if found:
                step("Post-optimize epubcheck")
                rc = step_epubcheck(*found)
                if rc != 0:
                    warn("Optimized EPUB failed epubcheck; raw EPUB preserved at output/*.raw.epub")
                    final_rc = rc

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


if __name__ == "__main__":
    raise SystemExit(main())
