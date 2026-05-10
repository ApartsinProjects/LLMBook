"""EPUB assembly. The core of html2pub."""
from __future__ import annotations

import io
import re
import uuid
from pathlib import Path

from bs4 import BeautifulSoup
from ebooklib import epub
from PIL import Image

from html2pub import content as content_mod
from html2pub import math_render
from html2pub import nav as nav_mod
from html2pub.config import Config
from html2pub.fonts import FONT_MIME, discover as discover_fonts, rewrite_katex_css_to_woff2
from html2pub.images import ImageBundle, slugify, sniff_image_type
from html2pub.spine import build_spine

DEFAULT_OVERRIDES_CSS = Path(__file__).parent / "default_overrides.css"


def _resolve_relative(from_rel: str, href: str) -> str:
    href = (href or "").strip()
    if not href or href.startswith(("http://", "https://", "mailto:", "javascript:", "data:", "#", "tel:")):
        return ""
    href = href.split("#", 1)[0].split("?", 1)[0]
    if not href:
        return ""
    base = Path(from_rel).parent
    try:
        # use posix logic: simple resolution
        parts = (base / href).as_posix().split("/")
        out: list[str] = []
        for p in parts:
            if p == "..":
                if out:
                    out.pop()
            elif p in ("", "."):
                continue
            else:
                out.append(p)
        return "/".join(out)
    except Exception:
        return ""


def _fragment_of(href: str) -> str:
    if "#" in href:
        return "#" + href.split("#", 1)[1]
    return ""


def _chapter_id(spine_index: int, src_rel: str) -> str:
    base = slugify(src_rel.replace("/", "_").replace(".html", ""))
    return f"ch_{spine_index:04d}_{base}"[:80]


def _chapter_filename(cid: str) -> str:
    return f"chapters/{cid}.xhtml"


def _extract_title(soup: BeautifulSoup, fallback: str) -> str:
    h1 = soup.find("h1")
    if h1 and h1.get_text(strip=True):
        return h1.get_text(strip=True)
    t = soup.find("title")
    if t and t.get_text(strip=True):
        s = t.get_text(strip=True)
        if "|" in s:
            s = s.split("|", 1)[0].strip()
        return s
    return fallback


def build(cfg: Config) -> Path:
    """Build the EPUB. Returns the output path."""
    print(f"[html2pub] project root: {cfg.project_root}")
    print(f"[html2pub] source dir: {cfg.content.source_dir}")

    spine_entries = build_spine(cfg)
    if not spine_entries:
        raise RuntimeError("Spine is empty -- check [content] section of html2pub.toml")
    print(f"[html2pub] spine entries: {len(spine_entries)}")

    images = ImageBundle(
        source_root=cfg.content.source_dir,
        max_side=cfg.images.max_side,
        jpeg_quality=cfg.images.jpeg_quality,
    )

    # Pre-pass: chapter id assignment
    chapter_map: dict[str, dict] = {}
    for i, entry in enumerate(spine_entries):
        cid = _chapter_id(i, entry["path"])
        chapter_map[entry["path"]] = {
            "id": cid,
            "file": _chapter_filename(cid),
            "title": entry.get("title_hint") or entry["path"],
            "kind": entry["kind"],
            "spine_index": i,
        }

    # Dropped fragments from config (basename -> set of ids)
    dropped_frags: dict[str, set[str]] = {
        k: set(v) for k, v in cfg.transforms.fragment_drop.items()
    }

    # Build the body of every chapter
    print("[html2pub] processing chapters...")
    chapter_xhtml: dict[str, str] = {}
    n_links_rewritten = 0
    n_links_dropped = 0
    n_imgs_seen = 0
    n_math_rendered = 0

    for i, entry in enumerate(spine_entries):
        src_rel = entry["path"]
        full = cfg.content.source_dir / src_rel
        try:
            html = full.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            print(f"  [skip] {src_rel}: {e}")
            continue

        soup = BeautifulSoup(html, "lxml")
        content_mod.clean_html(soup, cfg.transforms)
        n_math_rendered += math_render.render(soup, cfg.math)

        title = _extract_title(soup, fallback=src_rel)
        chapter_map[src_rel]["title"] = title

        # Rewrite anchor hrefs
        for a in soup.find_all("a"):
            href = a.get("href", "")
            if not href or href.startswith(("http://", "https://", "mailto:", "javascript:", "tel:", "data:")):
                continue
            if href.startswith("#"):
                continue
            target = _resolve_relative(src_rel, href)
            frag = _fragment_of(href)
            if target and target in chapter_map:
                tgt_basename = target.rsplit("/", 1)[-1].replace(".html", "")
                eff_frag = frag
                if frag and tgt_basename in dropped_frags:
                    if frag.lstrip("#") in dropped_frags[tgt_basename]:
                        eff_frag = ""
                a["href"] = chapter_map[target]["file"].rsplit("/", 1)[-1] + eff_frag
                n_links_rewritten += 1
            else:
                a.unwrap()
                n_links_dropped += 1

        # Rewrite img srcs
        for img in soup.find_all("img"):
            n_imgs_seen += 1
            src = img.get("src", "")
            if not src or src.startswith(("http://", "https://", "data:")):
                continue
            target = _resolve_relative(src_rel, src)
            bundled = images.add(target)
            if bundled is None:
                img.decompose()
                continue
            img["src"] = "../" + bundled

        # Strip <link rel="stylesheet"> from source -- we register them on the EpubHtml below.
        for link in soup.find_all("link", rel=lambda v: v and "stylesheet" in v):
            link.decompose()

        body = soup.find("body")
        body_inner = "".join(str(c) for c in body.children) if body is not None else str(soup)

        xhtml = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            "<!DOCTYPE html>\n"
            '<html xmlns="http://www.w3.org/1999/xhtml" '
            'xmlns:epub="http://www.idpf.org/2007/ops" '
            f'lang="{nav_mod.escape_xml(cfg.book.language)}">\n'
            "<head>\n"
            '<meta charset="utf-8" />\n'
            f"<title>{nav_mod.escape_xml(title)}</title>\n"
            "</head>\n"
            f"<body>\n{body_inner}\n</body>\n</html>\n"
        )
        chapter_xhtml[src_rel] = xhtml

        if (i + 1) % 25 == 0 or i == len(spine_entries) - 1:
            print(f"  [{i+1}/{len(spine_entries)}] {src_rel}")

    print(f"[html2pub] links: {n_links_rewritten} rewritten, {n_links_dropped} dropped")
    print(f"[html2pub] images: {n_imgs_seen} seen, {len(images.bundled_bytes)} bundled, {len(images.skipped)} skipped")
    if n_math_rendered:
        print(f"[html2pub] math: {n_math_rendered} expressions rendered via KaTeX")

    # ---- Assemble EPUB
    print("[html2pub] assembling EPUB...")
    book = epub.EpubBook()

    ident = cfg.book.identifier
    if not ident:
        ident = f"urn:uuid:{uuid.uuid4()}"
    book.set_identifier(ident)
    book.set_language(cfg.book.language)

    full_title = cfg.book.title
    if cfg.book.subtitle:
        book.set_title(f"{cfg.book.title}: {cfg.book.subtitle}")
    else:
        book.set_title(cfg.book.title)

    for i, au in enumerate(cfg.book.authors):
        cid = f"creator_{i:02d}"
        book.add_metadata("DC", "creator", au["name"], {"id": cid})
        book.add_metadata(
            None, "meta", au.get("file_as", au["name"]),
            {"refines": f"#{cid}", "property": "file-as"},
        )
        book.add_metadata(
            None, "meta", au.get("role", "aut"),
            {"refines": f"#{cid}", "property": "role", "scheme": "marc:relators"},
        )

    if cfg.book.description:
        book.add_metadata("DC", "description", cfg.book.description)
    if cfg.book.rights:
        book.add_metadata("DC", "rights", cfg.book.rights)
    if cfg.book.publication_date:
        book.add_metadata("DC", "date", cfg.book.publication_date)
    if cfg.book.publisher:
        book.add_metadata("DC", "publisher", cfg.book.publisher)
    for kw in cfg.book.keywords:
        book.add_metadata("DC", "subject", kw)

    # Cover
    if cfg.cover.path:
        cover_path = (cfg.project_root / cfg.cover.path).resolve()
        if cover_path.exists():
            cover_bytes = cover_path.read_bytes()
            ext = cover_path.suffix.lower().lstrip(".")
            book.set_cover(f"cover.{ext}", cover_bytes)

    # ---- Stylesheets
    stylesheet_links: list[str] = []  # hrefs to add via add_link on each chapter

    # Blitz baseline
    if cfg.styling.blitz and cfg.styling.blitz_path:
        bp = (cfg.project_root / cfg.styling.blitz_path).resolve()
        if bp.exists():
            book.add_item(epub.EpubItem(
                uid="css_blitz", file_name="styles/blitz.css",
                media_type="text/css", content=bp.read_bytes(),
            ))
            stylesheet_links.append("../styles/blitz.css")

    # KaTeX CSS + fonts (if math is on)
    if cfg.math.render == "katex" and cfg.math.katex_path:
        katex_css = Path(cfg.math.katex_path) / "katex" / "dist" / "katex.min.css"
        if katex_css.exists():
            css_text = katex_css.read_text(encoding="utf-8")
            if cfg.fonts.rewrite_katex_to_woff2_only:
                css_text = rewrite_katex_css_to_woff2(css_text)
            css_text = css_text.replace("url(fonts/", "url(../fonts/")
            book.add_item(epub.EpubItem(
                uid="css_katex", file_name="styles/katex.min.css",
                media_type="text/css", content=css_text.encode("utf-8"),
            ))
            stylesheet_links.append("../styles/katex.min.css")
            fonts_dir = katex_css.parent / "fonts"
            if fonts_dir.exists():
                for font in fonts_dir.iterdir():
                    suf = font.suffix.lower()
                    if suf not in FONT_MIME:
                        continue
                    if cfg.fonts.rewrite_katex_to_woff2_only and suf != ".woff2":
                        continue
                    book.add_item(epub.EpubItem(
                        uid=f"katex_font_{slugify(font.stem)}_{suf[1:]}",
                        file_name=f"fonts/{font.name}",
                        media_type=FONT_MIME[suf],
                        content=font.read_bytes(),
                    ))

    # User stylesheets — also bundle any url(...) referenced assets (icons, bg images)
    import re as _re
    _css_url_re = _re.compile(r"""url\(\s*['"]?([^'")]+)['"]?\s*\)""")
    _bundled_css_assets: set[str] = set()
    for i, css_rel in enumerate(cfg.styling.stylesheets):
        css_path = (cfg.project_root / css_rel).resolve()
        if not css_path.exists():
            print(f"  [warn] stylesheet not found: {css_rel}")
            continue
        css_name = css_path.name
        css_text = css_path.read_text(encoding="utf-8", errors="replace")
        book.add_item(epub.EpubItem(
            uid=f"css_user_{i}", file_name=f"styles/{css_name}",
            media_type="text/css", content=css_text.encode("utf-8"),
        ))
        stylesheet_links.append(f"../styles/{css_name}")
        # Bundle assets referenced via url(...)
        css_dir = css_path.parent
        for url in _css_url_re.findall(css_text):
            if url.startswith(("data:", "http:", "https:", "//")):
                continue
            url_clean = url.split("#")[0].split("?")[0]
            if not url_clean:
                continue
            asset_path = (css_dir / url_clean).resolve()
            if not asset_path.exists():
                print(f"  [warn] css asset missing: {url_clean} (referenced from {css_name})")
                continue
            # Asset goes under EPUB/styles/<relative_path_from_css>
            try:
                rel_in_styles = asset_path.relative_to(css_dir).as_posix()
            except ValueError:
                rel_in_styles = asset_path.name
            target = f"styles/{rel_in_styles}"
            if target in _bundled_css_assets:
                continue
            _bundled_css_assets.add(target)
            ext = asset_path.suffix.lower().lstrip(".")
            mime = {
                "png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
                "gif": "image/gif", "svg": "image/svg+xml", "webp": "image/webp",
            }.get(ext, "application/octet-stream")
            book.add_item(epub.EpubItem(
                uid=f"css_asset_{slugify(rel_in_styles)}", file_name=target,
                media_type=mime, content=asset_path.read_bytes(),
            ))
    if _bundled_css_assets:
        print(f"[html2pub] bundled {len(_bundled_css_assets)} CSS-referenced asset(s)")

    # EPUB overrides (user-supplied or built-in default)
    if cfg.styling.epub_overrides:
        ovr = (cfg.project_root / cfg.styling.epub_overrides).resolve()
    else:
        ovr = DEFAULT_OVERRIDES_CSS
    if ovr.exists():
        book.add_item(epub.EpubItem(
            uid="css_overrides", file_name="styles/epub_overrides.css",
            media_type="text/css", content=ovr.read_bytes(),
        ))
        stylesheet_links.append("../styles/epub_overrides.css")

    # User fonts
    for fpath in discover_fonts(cfg.fonts):
        suf = fpath.suffix.lower()
        book.add_item(epub.EpubItem(
            uid=f"font_{slugify(fpath.stem)}_{suf[1:]}",
            file_name=f"fonts/{fpath.name}",
            media_type=FONT_MIME[suf],
            content=fpath.read_bytes(),
        ))

    # Image items
    for bundled, data in images.bundled_bytes.items():
        mime = images.bundled_mime[bundled]
        uid = "img_" + slugify(bundled)
        book.add_item(epub.EpubItem(uid=uid, file_name=bundled, media_type=mime, content=data))

    # Chapter items -- CRITICAL: register stylesheets via ch.add_link()
    chapter_items: list[epub.EpubHtml] = []
    for entry in spine_entries:
        src_rel = entry["path"]
        if src_rel not in chapter_xhtml:
            continue
        info = chapter_map[src_rel]
        ch = epub.EpubHtml(
            uid=info["id"],
            file_name=info["file"],
            title=info["title"],
            lang=cfg.book.language,
            content=chapter_xhtml[src_rel].encode("utf-8"),
        )
        # The lesson: ebooklib's set_content() ignores <link> tags in <head>.
        # Stylesheets MUST be registered through add_link() to render in EPUB.
        for href in stylesheet_links:
            ch.add_link(href=href, rel="stylesheet", type="text/css")
        if "<svg" in chapter_xhtml[src_rel].lower():
            ch.properties = ["svg"]
        book.add_item(ch)
        chapter_items.append(ch)

    # Make ebooklib's auto cover.xhtml linear
    cover_html = book.get_item_with_id("cover")
    if cover_html is not None:
        cover_html.is_linear = True

    # Custom nav.xhtml
    nav_html = nav_mod.build_nav_xhtml(spine_entries, chapter_map, full_title)
    nav_item = epub.EpubItem(
        uid="nav", file_name="nav.xhtml",
        media_type="application/xhtml+xml",
        content=nav_html.encode("utf-8"),
    )
    nav_item.properties = ["nav"]
    book.add_item(nav_item)

    # Populate book.toc so EpubNcx() renders non-empty navMap (epubcheck RSC-005)
    toc_entries = []
    for ent in spine_entries:
        src_rel = ent.get("path") if isinstance(ent, dict) else None
        info = chapter_map.get(src_rel) if src_rel else None
        if not info:
            continue
        title = (info.get("title") or src_rel).strip() or src_rel
        toc_entries.append(epub.Link(info["file"], title, info["id"]))
    book.toc = tuple(toc_entries)
    book.add_item(epub.EpubNcx())

    # Spine
    spine_seq: list = []
    if cover_html is not None:
        spine_seq.append("cover")
    spine_seq.append("nav")
    spine_seq.extend(chapter_items)
    book.spine = spine_seq

    # Write
    out_path = (cfg.project_root / cfg.output.epub).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    epub.write_epub(str(out_path), book, {})
    size_mb = out_path.stat().st_size / (1024 * 1024)
    print(f"[html2pub] wrote {out_path} ({size_mb:.2f} MB, {len(chapter_items)} chapters)")
    return out_path
