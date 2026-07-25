"""End-to-end build: generate UFO from glyph defs, compile to OTF/TTF/WOFF2.

Usage:
    py scripts/build_all.py

Outputs:
    sources/Newell-Regular.ufo/    (UFO source, also version-controlled)
    releases/Newell-Regular.otf
    releases/Newell-Regular.ttf
    releases/Newell-Regular.woff2
"""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "sources"
RELEASES = ROOT / "releases"
UFO = SOURCES / "Newell-Regular.ufo"


def step(label, cmd):
    print(f"\n=== {label} ===")
    print("$ " + " ".join(str(c) for c in cmd))
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        sys.exit(f"{label} failed (exit {result.returncode})")


def main():
    RELEASES.mkdir(parents=True, exist_ok=True)

    # 1. Generate UFO from declarative glyph definitions.
    step("Generate UFO", [sys.executable, "scripts/build.py"])

    # 2. Compile OTF (CFF PostScript outlines).
    step("Compile OTF",
         [sys.executable, "-m", "fontmake",
          "-u", str(UFO), "-o", "otf",
          "--output-dir", str(RELEASES)])

    # 3. Compile TTF (TrueType outlines).
    step("Compile TTF",
         [sys.executable, "-m", "fontmake",
          "-u", str(UFO), "-o", "ttf",
          "--output-dir", str(RELEASES)])

    # 4. Compress TTF -> WOFF2 for web use.
    step("Compress WOFF2",
         [sys.executable, "-m", "fontTools.ttLib.woff2",
          "compress", str(RELEASES / "Newell-Regular.ttf")])

    # 5. Summary.
    print("\n=== Build summary ===")
    for fmt in ("otf", "ttf", "woff2"):
        p = RELEASES / f"Newell-Regular.{fmt}"
        if p.exists():
            size = p.stat().st_size
            print(f"  {p.name:30s}  {size:>8,} bytes")
        else:
            print(f"  {p.name:30s}  MISSING")


if __name__ == "__main__":
    main()
