"""Variable-font build: weight axis via fontTools varLib (issue #8).

Builds the four SPEC section 9 masters from the parametric glyph
definitions, writes a designspace, and runs fontmake twice:
  -o variable  -> releases/Newell-VF.ttf      (weight axis 300-900)
  -o ttf       -> releases/Newell-{Light,Bold,Black}.ttf (static
                  instances; the Regular TTF comes from the single-UFO
                  compile in build_all.py and is intentionally NOT
                  re-instantiated here)

Masters are written as RAW expanded primitives (no boolean union):
union topology shifts with stroke width (junctions split differently),
which breaks varLib master compatibility. Raw primitives keep
contour/point counts identical across weights; overlaps render the
same under nonzero winding. They live in the gitignored
sources/master_ufo/ dir — build intermediates, regenerated every run,
never overwriting the committed union-outline Newell-Regular.ufo.

Usage:
    py scripts/build_variable.py
"""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from newell.font import build_and_save  # noqa: E402
from newell.glyphs import build_glyph_defs  # noqa: E402

SOURCES = ROOT / "sources"
RELEASES = ROOT / "releases"
MASTERS_DIR = SOURCES / "master_ufo"

# SPEC section 9: stroke width -> wght axis value.
MASTERS = [
    ("Light", 70, 300),
    ("Regular", 110, 400),
    ("Bold", 170, 700),
    ("Black", 220, 900),
]

DESIGNSPACE_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<designspace format="5">
  <axes>
    <axis tag="wght" name="Weight" minimum="300" maximum="900" default="400" uservalue="400"/>
  </axes>
  <sources>
{sources}
  </sources>
  <instances>
{instances}
  </instances>
</designspace>
"""

SOURCE_TEMPLATE = """    <source familyname="Newell" stylename="{style}" filename="{ufo_name}">
      <location>
        <dimension name="Weight" xvalue="{wght}"/>
      </location>
    </source>"""

INSTANCE_TEMPLATE = """    <instance familyname="Newell" stylename="{style}" filename="{filename}">
      <location>
        <dimension name="Weight" xvalue="{wght}"/>
      </location>
    </instance>"""


def step(label, cmd):
    print(f"\n=== {label} ===")
    print("$ " + " ".join(str(c) for c in cmd))
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        sys.exit(f"{label} failed (exit {result.returncode})")


def main():
    RELEASES.mkdir(parents=True, exist_ok=True)

    # 1. Generate the master UFOs from the parametric glyph definitions.
    MASTERS_DIR.mkdir(parents=True, exist_ok=True)
    for style, stroke, _wght in MASTERS:
        ufo_name = f"Newell-{style}.ufo"
        print(f"master: {ufo_name} (stroke {stroke})")
        build_and_save(
            build_glyph_defs(stroke_width=stroke),
            str(MASTERS_DIR / ufo_name),
            style_name=style,
            union_outlines=False,
        )

    # 2. Write the designspace. Instances list only the non-default
    #    weights: the Regular instance must not clobber the unioned
    #    releases/Newell-Regular.ttf from the single-UFO compile.
    sources_xml = "\n".join(
        SOURCE_TEMPLATE.format(
            style=style, ufo_name=f"master_ufo/Newell-{style}.ufo", wght=wght
        )
        for style, _stroke, wght in MASTERS
    )
    instances_xml = "\n".join(
        INSTANCE_TEMPLATE.format(
            style=style, filename=f"../releases/Newell-{style}.ttf", wght=wght
        )
        for style, _stroke, wght in MASTERS
        if style != "Regular"
    )
    ds_path = SOURCES / "Newell.designspace"
    ds_path.write_text(
        DESIGNSPACE_TEMPLATE.format(sources=sources_xml, instances=instances_xml),
        encoding="utf-8",
    )
    print(f"designspace: {ds_path}")

    # 3. Compile the variable TTF (gvar interpolation of the 4 masters).
    step("Compile variable TTF",
         [sys.executable, "-m", "fontmake",
          str(ds_path),
          "-o", "variable",
          "--output-dir", str(RELEASES)])

    vf_out = RELEASES / "Newell-VF.ttf"
    vf_built = None
    for candidate in ("Newell-VF.ttf", "Newell-Regular-variable.ttf",
                      "Newell-Variable.ttf"):
        if (RELEASES / candidate).exists():
            vf_built = RELEASES / candidate
            break
    if vf_built is not None:
        shutil.move(vf_built, vf_out)
    else:
        sys.exit("variable font output not found (looked for "
                 "Newell-VF.ttf / Newell-Regular-variable.ttf / "
                 "Newell-Variable.ttf in releases/)")

    # 4. Compile static instances (Light/Bold/Black, TrueType).
    step("Compile static instances",
         [sys.executable, "-m", "fontmake",
          str(ds_path),
          "-o", "ttf",
          "--output-dir", str(RELEASES)])

    print("\n=== Variable build summary ===")
    for name in ("Newell-VF.ttf", "Newell-Light.ttf", "Newell-Bold.ttf",
                 "Newell-Black.ttf"):
        p = RELEASES / name
        if p.exists():
            print(f"  {p.name:24s} {p.stat().st_size:>8,} bytes")
        else:
            print(f"  {p.name:24s} MISSING")


if __name__ == "__main__":
    main()
