"""Render the generated UFO glyphs to PNG for visual inspection.

Quick-and-dirty: loads the UFO, extracts glyph contours, draws them
with matplotlib on a black background in Newell green. No font
rendering library required — we just draw the polygons.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PatchCollection
import ufoLib2
import xml.etree.ElementTree as ET

UFO_PATH = Path("sources/Newell-Regular.ufo")
OUT_DIR = Path("scripts/_preview")
OUT_DIR.mkdir(exist_ok=True)


def load_glyph_contours(font, glyph_name):
    """Read raw contour point data from the .glif XML.

    ufoLib2 doesn't expose a clean 'give me point list' API, so we
    parse the GLIF directly. Each contour is a list of (x, y, type).
    """
    # Look up the actual filename via contents.plist
    contents_path = UFO_PATH / "glyphs" / "contents.plist"
    contents_tree = ET.parse(contents_path)
    contents_root = contents_tree.getroot()
    main_dict = contents_root.find("dict")
    filename = None
    children = list(main_dict)
    for i, child in enumerate(children):
        if child.tag == "key" and child.text == glyph_name:
            filename = children[i + 1].text
            break
    if filename is None:
        raise KeyError(f"glyph {glyph_name!r} not in contents.plist")
    glif_path = UFO_PATH / "glyphs" / filename
    tree = ET.parse(glif_path)
    root = tree.getroot()
    contours = []
    for contour_el in root.iter("contour"):
        pts = []
        for pt in contour_el.findall("point"):
            x = float(pt.get("x"))
            y = float(pt.get("y"))
            pts.append((x, y))
        if len(pts) >= 3:
            contours.append(pts)
    return contours


def render(font, glyph_name, out_path, label=None):
    contours = load_glyph_contours(font, glyph_name)
    fig, ax = plt.subplots(figsize=(6, 6), facecolor="#111111")
    ax.set_facecolor("#111111")
    patches = []
    for c in contours:
        patches.append(MplPolygon(c, closed=True))
    pc = PatchCollection(patches, facecolor="#00FF66", edgecolor="#00FF66", linewidth=0)
    ax.add_collection(pc)

    # 1000-unit em; glyph lives roughly in 0..1000 x -200..800
    ax.set_xlim(-100, 1100)
    ax.set_ylim(-250, 850)
    ax.set_aspect("equal")
    ax.axis("off")
    if label:
        ax.set_title(label, color="#FFFFFF", fontsize=14, pad=10)
    plt.savefig(out_path, dpi=120, bbox_inches="tight",
                facecolor="#111111", pad_inches=0.2)
    plt.close()
    print(f"wrote {out_path}")


def render_all(width=1200, height_per=700):
    """Render all glyphs side-by-side."""
    font = ufoLib2.Font.open(str(UFO_PATH))
    glyphs = [n for n in font.keys() if n not in (".notdef", "space")]
    glyphs.sort()

    n = len(glyphs)
    fig, axes = plt.subplots(1, n, figsize=(3 * n, 4), facecolor="#111111")
    if n == 1:
        axes = [axes]
    for ax, name in zip(axes, glyphs):
        ax.set_facecolor("#111111")
        contours = load_glyph_contours(font, name)
        patches = [MplPolygon(c, closed=True) for c in contours]
        pc = PatchCollection(patches, facecolor="#00FF66",
                             edgecolor="#00FF66", linewidth=0)
        ax.add_collection(pc)
        ax.set_xlim(-100, 1100)
        ax.set_ylim(-250, 850)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(name, color="#FFFFFF", fontsize=18, pad=8)
    plt.tight_layout()
    out = OUT_DIR / "all.png"
    plt.savefig(out, dpi=110, facecolor="#111111")
    plt.close()
    print(f"wrote {out}")


def main():
    UFO_PATH.mkdir(parents=True, exist_ok=True)
    font = ufoLib2.Font.open(str(UFO_PATH))
    targets = sys.argv[1:] or ["N", "E", "I", "H"]
    for name in targets:
        if name in (".notdef", "space") or name not in font:
            continue
        render(font, name, OUT_DIR / f"{name}.png", label=f"Newell {name}")
    render_all()


if __name__ == "__main__":
    main()
