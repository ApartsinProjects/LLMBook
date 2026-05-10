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
    def __init__(self, source_root: Path, max_side: int = 1280, jpeg_quality: int = 78):
        self.source_root = source_root
        self.max_side = max_side
        self.jpeg_quality = jpeg_quality
        self.path_to_bundle: dict[str, str] = {}
        self.bundled_bytes: dict[str, bytes] = {}
        self.bundled_mime: dict[str, str] = {}
        self.skipped: list[tuple[str, str]] = []

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
        bundled = f"img/{file_hash(full)}_{slugify(full.stem)}.{out_ext}"
        return data, bundled, out_mime
