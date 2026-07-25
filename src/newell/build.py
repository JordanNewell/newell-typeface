"""CLI entry point: build the Newell-Regular UFO from declarative glyphs.

Usage:
    py -m newell.build [--out PATH] [--quiet]

Default output: sources/Newell-Regular.ufo under the project root
(determined by walking up from this file). Validates the result by
loading it back with ufoLib2.
"""

import argparse
import os
import sys

from newell.font import build_and_save, validate_ufo
from newell.glyphs import GLYPHS


def _project_root():
    here = os.path.dirname(os.path.abspath(__file__))
    # src/newell/build.py -> up twice to project root.
    return os.path.dirname(os.path.dirname(here))


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="newell.build",
        description="Build the Newell-Regular UFO from declarative glyphs.",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Output UFO path. Defaults to <root>/sources/Newell-Regular.ufo.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress informational output.",
    )
    args = parser.parse_args(argv)

    root = _project_root()
    out = args.out or os.path.join(root, "sources", "Newell-Regular.ufo")

    log = (lambda *a: None) if args.quiet else _print
    log(f"Building {len(GLYPHS)} glyphs ({[g['name'] for g in GLYPHS]})...")
    font = build_and_save(GLYPHS, out)

    expected = [g["name"] for g in GLYPHS]
    log(f"Validating {out}...")
    loaded = validate_ufo(out, expected)
    log(
        "OK: %d glyphs -> %s",
        len(loaded),
        sorted(loaded.keys()),
    )
    log("Done.")
    return 0


def _print(fmt, *args):
    if args:
        print(fmt % args)
    else:
        print(fmt)


if __name__ == "__main__":
    sys.exit(main())
