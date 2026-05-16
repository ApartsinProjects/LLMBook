"""Rasterize SVG to PNG using resvg_py. Usage: python rasterize_diagram.py input.svg output.png [width]"""
import sys
import resvg_py

def rasterize(svg_path: str, png_path: str, width: int = 1200) -> None:
    with open(svg_path, "rb") as f:
        svg_bytes = f.read()
    png_bytes = resvg_py.svg_to_bytes(svg_string=svg_bytes.decode("utf-8"), width=width)
    with open(png_path, "wb") as f:
        f.write(bytes(png_bytes))
    print(f"wrote {png_path}")

if __name__ == "__main__":
    svg = sys.argv[1]
    png = sys.argv[2]
    width = int(sys.argv[3]) if len(sys.argv) > 3 else 1200
    rasterize(svg, png, width)
