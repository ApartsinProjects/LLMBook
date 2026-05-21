"""Find HTML tags with leaked-prose attribute names.

Two source defects produce bogus attributes that EPUBCheck rejects:
  1. An unescaped '<' inside text/math (e.g. x_{<t})  -> parser starts a tag
     and the following words become boolean attributes.
  2. An unescaped '"' inside an attribute value (e.g. alt="he said "hi"")
     -> the value closes early and following words become attributes.

Both manifest as a start tag carrying attribute *names* that are ordinary
English words. We parse every source file with html.parser and report any tag
whose attribute names are not in the known-safe HTML/SVG/ARIA/EPUB set.
"""
from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = ("_archive/", "KDP/", "node_modules/", "pagefind/", "temp_epub/",
        "templates/", ".git/", "scripts/")

# Known-safe attribute names (lowercased). Anything else is suspicious.
SAFE = {
    # core HTML
    "id", "class", "style", "title", "lang", "dir", "hidden", "tabindex",
    "role", "src", "href", "alt", "width", "height", "rel", "target",
    "type", "name", "value", "content", "rev", "media", "scope", "colspan",
    "rowspan", "headers", "abbr", "axis", "for", "selected", "checked",
    "disabled", "readonly", "multiple", "size", "maxlength", "placeholder",
    "action", "method", "enctype", "accept", "cols", "rows", "wrap",
    "datetime", "cite", "open", "controls", "loop", "muted", "poster",
    "preload", "autoplay", "default", "kind", "srclang", "label", "span",
    "start", "reversed", "download", "ping", "referrerpolicy", "hreflang",
    "sizes", "srcset", "loading", "decoding", "fetchpriority", "crossorigin",
    "integrity", "nonce", "async", "defer", "charset", "http-equiv",
    "property", "itemprop", "itemscope", "itemtype", "itemref", "itemid",
    "draggable", "spellcheck", "translate", "contenteditable", "accesskey",
    "autocapitalize", "autofocus", "enterkeyhint", "inputmode", "is",
    "slot", "part", "exportparts", "inert", "popover", "frameborder",
    "allow", "allowfullscreen", "sandbox", "usemap", "ismap", "shape",
    "coords", "border", "align", "valign", "bgcolor", "color", "face",
    "nowrap", "cellpadding", "cellspacing", "summary", "frame", "rules",
    "high", "low", "optimum", "max", "min", "step", "pattern", "required",
    "list", "form", "formaction", "formmethod", "formtarget", "novalidate",
    "autocomplete", "dirname", "data",
    # SVG (lowercased by html.parser)
    "viewbox", "xmlns", "preserveaspectratio", "fill", "stroke", "d", "x",
    "y", "x1", "y1", "x2", "y2", "cx", "cy", "r", "rx", "ry", "points",
    "transform", "stroke-width", "stroke-linecap", "stroke-linejoin",
    "stroke-dasharray", "stroke-dashoffset", "stroke-opacity", "fill-opacity",
    "opacity", "offset", "stop-color", "stop-opacity", "gradientunits",
    "gradienttransform", "spreadmethod", "patternunits", "marker-end",
    "marker-start", "marker-mid", "markerwidth", "markerheight", "orient",
    "refx", "refy", "markerunits", "dx", "dy", "rotate", "textlength",
    "lengthadjust", "text-anchor", "dominant-baseline", "alignment-baseline",
    "baseline-shift", "font-family", "font-size", "font-weight", "font-style",
    "letter-spacing", "word-spacing", "writing-mode", "clip-path", "clip-rule",
    "fill-rule", "mask", "filter", "flood-color", "flood-opacity",
    "stddeviation", "in", "in2", "result", "mode", "values", "type2",
    "tablevalues", "slope", "intercept", "amplitude", "exponent", "k1", "k2",
    "k3", "k4", "operator", "radius", "stitchtiles", "basefrequency",
    "numoctaves", "seed", "scale", "xchannelselector", "ychannelselector",
    "primitiveunits", "filterunits", "color-interpolation-filters",
    "gradientunits", "href", "version", "baseprofile", "enable-background",
    "xml:space", "xml:lang", "xml:base", "overflow", "display", "visibility",
    "pointer-events", "shape-rendering", "text-rendering", "image-rendering",
    "vector-effect", "paint-order", "color-interpolation", "pathlength",
    "systemlanguage", "requiredfeatures", "requiredextensions",
    "aria-describedby", "aria-labelledby",
}


def is_safe(attr: str) -> bool:
    a = attr.lower()
    if a in SAFE:
        return True
    if a.startswith(("data-", "aria-", "on", "epub:", "xmlns:", "xlink:",
                     "xml:", "ns1:", "ns2:", "ns3:", "sodipodi:", "inkscape:")):
        return True
    return False


class Scan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.bad = []

    def handle_starttag(self, tag, attrs):
        for name, _ in attrs:
            if not is_safe(name):
                self.bad.append((self.getpos()[0], tag, name))


def main():
    total = 0
    files = 0
    for p in ROOT.rglob("*.html"):
        s = str(p).replace("\\", "/") + "/"
        if any(k in s for k in SKIP):
            continue
        files += 1
        try:
            t = p.read_text(encoding="utf-8")
        except Exception:
            continue
        sc = Scan()
        try:
            sc.feed(t)
        except Exception:
            continue
        if sc.bad:
            rel = str(p.relative_to(ROOT)).replace("\\", "/")
            # group by line
            seen = set()
            for ln, tag, name in sc.bad:
                key = (ln, tag)
                if key in seen:
                    continue
                seen.add(key)
                names = sorted({n for l, tg, n in sc.bad if l == ln and tg == tag})
                print(f"  {rel}:{ln} <{tag}> bad attrs: {names}")
                total += 1
    print(f"\nScanned {files} files; {total} tag(s) with leaked-prose attributes.")


if __name__ == "__main__":
    main()
