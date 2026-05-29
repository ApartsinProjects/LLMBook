"""Image discovery, optimization, and bundling."""
from __future__ import annotations

import hashlib
import io
import re
import unicodedata
from pathlib import Path

from PIL import Image


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text or "x"


def file_hash(p: Path) -> str:
    h = hashlib.md5()
    h.update(p.read_bytes())
    return h.hexdigest()[:10]


def sniff_image_type(data: bytes, declared_ext: str):
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return ("image/png", ".png")
    if data.startswith(b"\xff\xd8\xff"):
        return ("image/jpeg", ".jpg")
    if data.startswith(b"GIF87a") or data.startswith(b"GIF89a"):
        return ("image/gif", ".gif")
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        return ("image/webp", ".webp")
    if declared_ext == ".svg" or data.lstrip().startswith(b"<svg") or data.lstrip().startswith(b"<?xml"):
        return ("image/svg+xml", ".svg")
    return (None, None)


class ImageBundle:
    def __init__(self, source_root: Path, max_side: int = 1280, jpeg_quality: int = 78,
                 cache_dir: Path | None = None):
        self.source_root = source_root
        self.max_side = max_side
        self.jpeg_quality = jpeg_quality
        # On-disk cache: re-encoded bytes keyed by source-hash + (max_side, quality).
        # Set to None (default) to disable. Pass a Path to enable.
        self.cache_dir = cache_dir
        if cache_dir is not None:
            cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_hits = 0
        self.cache_misses = 0
        self.path_to_bundle: dict[str, str] = {}
        self.bundled_bytes: dict[str, bytes] = {}
        self.bundled_mime: dict[str, str] = {}
        self.skipped: list[tuple[str, str]] = []

    def _cache_key(self, src_hash: str, ext: str) -> str:
        # Cache invalidates when input hash OR processing params change
        import hashlib as _h
        params = f"{self.max_side}-{self.jpeg_quality}"
        param_hash = _h.md5(params.encode()).hexdigest()[:8]
        return f"{src_hash}-{param_hash}.{ext.lstrip('.')}"

    def add(self, src_rel: str) -> str | None:
        if not src_rel:
            return None
        if src_rel in self.path_to_bundle:
            return self.path_to_bundle[src_rel]
        full = self.source_root / src_rel
        if not full.exists() or not full.is_file():
            self.skipped.append((src_rel, "missing on disk"))
            return None
        ext = full.suffix.lower()
        if ext == ".svg":
            data = full.read_bytes()
            bundled = f"img/{file_hash(full)}_{slugify(full.stem)}.svg"
            mime = "image/svg+xml"
        elif ext in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
            try:
                data, bundled, mime = self._reencode(full)
            except Exception as e:
                self.skipped.append((src_rel, f"reencode failed: {e}"))
                return None
        else:
            self.skipped.append((src_rel, f"unsupported ext {ext}"))
            return None
        self.path_to_bundle[src_rel] = bundled
        self.bundled_bytes[bundled] = data
        self.bundled_mime[bundled] = mime
        return bundled

    def _reencode(self, full: Path):
        src_hash = file_hash(full)
        # Check cache for this src_hash + processing params
        cached_data = None
        cached_ext = None
        if self.cache_dir:
            for ext_try in ("jpg", "png"):
                cpath = self.cache_dir / self._cache_key(src_hash, ext_try)
                if cpath.exists():
                    cached_data = cpath.read_bytes()
                    cached_ext = ext_try
                    break
        if cached_data is not None:
            self.cache_hits += 1
            out_mime = "image/jpeg" if cached_ext == "jpg" else "image/png"
            bundled = f"img/{src_hash}_{slugify(full.stem)}.{cached_ext}"
            return cached_data, bundled, out_mime
        self.cache_misses += 1
        with Image.open(full) as im:
            im.load()
            w, h = im.size
            has_alpha = (im.mode in ("RGBA", "LA", "P")
                         and ("transparency" in im.info or im.mode in ("RGBA", "LA")))
            if has_alpha:
                out_mode, out_ext, out_mime = "RGBA", "png", "image/png"
            else:
                out_mode, out_ext, out_mime = "RGB", "jpg", "image/jpeg"
            im = im.convert(out_mode)
            if max(w, h) > self.max_side:
                scale = self.max_side / max(w, h)
                im = im.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.Resampling.LANCZOS)
            buf = io.BytesIO()
            if out_ext == "jpg":
                im.save(buf, format="JPEG", quality=self.jpeg_quality, optimize=True, progressive=False)
            else:
                im.save(buf, format="PNG", optimize=True)
            data = buf.getvalue()
        # Save to cache
        if self.cache_dir:
            try:
                (self.cache_dir / self._cache_key(src_hash, out_ext)).write_bytes(data)
            except Exception:
                pass
        bundled = f"img/{src_hash}_{slugify(full.stem)}.{out_ext}"
        return data, bundled, out_mime
