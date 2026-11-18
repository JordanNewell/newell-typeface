"""Generate the legibility manifest (issue #11 visual-diff gate).

The manifest records a deterministic hash of every glyph's unioned
contour geometry. CI regenerates it and fails if it differs from the
committed copy — forcing any glyph-geometry change to be conscious:
review the contact sheet, then re-run this script and commit.

Usage:
    py scripts/gen_manifest.py          # regenerate + write manifest
    py scripts/gen_manifest.py --check  # compare only (CI mode); exit 1 on drift

Also renders scripts/_preview/contact_sheet.png (all glyphs, fixed
grid) for human review when matplotlib is installed locally.
"""

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from newell.generator import union_primitives  # noqa: E402
from newell.glyphs import GLYPHS  # noqa: E402

MANIFEST_PATH = ROOT / "sources" / "legibility-manifest.json"
SHEET_PATH = ROOT / "scripts" / "_preview" / "contact_sheet.png"


def glyph_hash(glyph_def):
    contours = union_primitives(glyph_def.get("primitives", []),
                            glyph_def.get("_stroke", 110))
    canonical = json.dumps(
        [sorted(map(tuple, c)) for c in sorted(contours, key=lambda c: sorted(c)[0])],
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]


def build_manifest():
    return {
        "version": 1,
        "glyph_count": len(GLYPHS),
        "glyphs": {g["name"]: glyph_hash(g) for g in GLYPHS},
    }


def render_contact_sheet():
    """Best-effort contact sheet for human review (needs matplotlib)."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.patches import Polygon as MplPolygon
        import ufoLib2
    except ImportError:
        print("matplotlib/ufoLib2 not available — skipping contact sheet")
        return None

    import subprocess
    import tempfile

    ufo = ROOT / "sources" / "Newell-Regular.ufo"
    subprocess.run([sys.executable, "scripts/build.py"], cwd=ROOT, check=True)
    font = ufoLib2.Font.open(ufo)
    names = [g["name"] for g in GLYPHS]
    cols = 10
    rows = (len(names) + cols - 1) // cols
    fig, axes = plt.subplots(
        rows, cols, figsize=(1.4 * cols, 1.6 * rows), facecolor="#111111"
    )
    for ax in axes.ravel():
        ax.axis("off")
    sys.path.insert(0, str(ROOT / "scripts"))
    from preview import load_glyph_contours

    for ax, name in zip(axes.ravel(), names):
        for c in load_glyph_contours(font, name):
            ax.add_patch(MplPolygon(c, closed=True, facecolor="#00FF41"))
        ax.set_xlim(-60, font[name].width)
        ax.set_ylim(-100, 800)
        ax.set_aspect("equal")
        ax.set_title(name, color="white", fontsize=7)
    SHEET_PATH.parent.mkdir(exist_ok=True)
    fig.savefig(SHEET_PATH, dpi=50, facecolor="#111111")
    plt.close(fig)
    return SHEET_PATH


def main():
    manifest = build_manifest()
    canonical = json.dumps(manifest, sort_keys=True, separators=(",", ":"))
    if "--check" in sys.argv:
        if not MANIFEST_PATH.exists():
            sys.exit("legibility manifest missing — run py scripts/gen_manifest.py")
        committed = MANIFEST_PATH.read_text(encoding="utf-8")
        committed_canonical = json.dumps(
            json.loads(committed), sort_keys=True, separators=(",", ":")
        )
        if canonical != committed_canonical:
            try:
                sheet = render_contact_sheet()
            except Exception as exc:  # noqa: BLE001
                sheet = f"(contact sheet render failed: {exc})"
            print(
                "GLYPH GEOMETRY CHANGED since legibility-manifest.json was "
                "last committed.\n"
                f"Contact sheet: {sheet}\n"
                "If the change is intended and reviewed, re-run "
                "`py scripts/gen_manifest.py` and commit the manifest.\n"
                "If not, investigate the glyph change."
            )
            sys.exit(1)
        print(f"legibility manifest OK ({manifest['glyph_count']} glyphs)")
        return

    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    sheet = render_contact_sheet()
    print(f"manifest written: {MANIFEST_PATH}")
    if sheet:
        print(f"contact sheet:    {sheet} (review before committing manifest)")


if __name__ == "__main__":
    main()
