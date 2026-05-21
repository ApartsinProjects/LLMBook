"""Screenshot a region of a rendered HTML page (faithful Chromium) for visual
inspection via the Read tool. Usage: shot.py <file.html> <anchor-id|-> <out.png> [height]"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

f = Path(sys.argv[1]).resolve()
anchor = sys.argv[2]
out = sys.argv[3]
height = int(sys.argv[4]) if len(sys.argv) > 4 else 1500
url = f.as_uri()
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": height}, device_scale_factor=1.5)
    pg.goto(url, wait_until="networkidle")
    pg.wait_for_timeout(500)
    if anchor and anchor != "-":
        el = pg.query_selector(f'[id="{anchor}"]')
        if el:
            el.scroll_into_view_if_needed()
            pg.wait_for_timeout(400)
    pg.screenshot(path=out, full_page=False)
    b.close()
print("wrote", out)
