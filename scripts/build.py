#!/usr/bin/env py
"""Thin wrapper so `py scripts/build.py` works without installing the package.

Adds the project's src/ directory to sys.path, then calls newell.build.main().
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
_SRC = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from newell.build import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
