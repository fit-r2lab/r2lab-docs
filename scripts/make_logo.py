#!/usr/bin/env python3
"""
Compose the site logo: the 3 logos of the r2lab.inria.fr header
(SLICES-RI, FIT, R2lab) side by side, on a white rounded badge so that
it reads on both light and dark themes (slices-ri.png is opaque white
and the FIT logo is dark blue).

  uv run scripts/make_logo.py   ->   assets/logo.svg

The images are embedded as data URIs so that the result is a single file.
"""

import base64
from pathlib import Path

SRC = Path("assets/logos")
OUT = Path("assets/logo.svg")

H = 45          # height of each logo, as in the original header
GAP = 10
PAD = 6

# (file, mime, width/height ratio)
LOGOS = [
    ("slices-ri.png", "image/png", 408 / 124),
    ("fit-logo.svg", "image/svg+xml", 270 / 135),
    ("r2lab-icon-square.png", "image/png", 1),
]


def data_uri(name, mime):
    raw = (SRC / name).read_bytes()
    return f"data:{mime};base64,{base64.b64encode(raw).decode()}"


def main():
    x = PAD
    images = []
    for name, mime, ratio in LOGOS:
        w = round(H * ratio, 1)
        images.append(
            f'<image x="{x}" y="{PAD}" width="{w}" height="{H}" '
            f'preserveAspectRatio="xMidYMid meet" href="{data_uri(name, mime)}"/>'
        )
        x += w + GAP
    width = round(x - GAP + PAD, 1)
    height = H + 2 * PAD
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" width="{width}" height="{height}">\n'
        f'<title>SLICES-RI - FIT - R2lab</title>\n'
        f'<rect width="{width}" height="{height}" rx="8" fill="#ffffff"/>\n'
        + "\n".join(images)
        + "\n</svg>\n"
    )
    OUT.write_text(svg)
    print(f"make_logo: wrote {OUT} ({width} x {height})")


if __name__ == "__main__":
    main()
