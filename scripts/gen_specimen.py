"""Regenerate the glyph-derived blocks of specimen/index.html (issue #9).

The specimen page's hand-written layout is never touched. Only the four
blocks wrapped in marker comments are regenerated from the glyph
definitions:

    <!-- BEGIN GENERATED:<name> --> ... <!-- END GENERATED:<name> -->

  count        the "<b>N glyphs</b>" figure in the hero meta
  alphabet     the A-Z cell grid
  numerals     the 0-9 row
  punctuation  the punctuation sampler row (every non-letter/non-digit
               glyph, sorted by codepoint)

Usage:
    py scripts/gen_specimen.py           # regenerate in place
    py scripts/gen_specimen.py --check   # exit 1 if the committed page is stale (CI)

After #6/#7 land new glyphs, running this once refreshes the page; CI
fails if the committed page is stale, and the Pages workflow
regenerates fresh at deploy time regardless.
"""

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from newell.glyphs import GLYPHS  # noqa: E402

SPECIMEN = ROOT / "specimen" / "index.html"

BEGIN = "<!-- BEGIN GENERATED:{name} -->"
END = "<!-- END GENERATED:{name} -->"


def _char(glyph_def):
    code = glyph_def.get("unicode")
    if code is None:
        return None
    if isinstance(code, str):
        from newell.generator import _parse_unicode
        code = _parse_unicode(code)
    return chr(code)


def block_count():
    return f"<span><b>v0.1.1-alpha</b></span>\n        <span>{len(GLYPHS)} glyphs</span>"


def _cells(glyph_defs, cls):
    out = []
    for g in glyph_defs:
        ch = _char(g)
        if ch is None:
            continue
        label = html.escape(g["name"], quote=True)
        out.append(f'<span class="{cls}" data-name="{label}">{html.escape(ch)}</span>')
    return "\n        ".join(out)


def block_alphabet():
    letters = [g for g in GLYPHS
               if (_char(g) or "").isalpha() and (_char(g) or "").isupper()]
    letters.sort(key=lambda g: _char(g))
    return _cells(letters, "alphabet__cell")


def block_numerals():
    digits = [g for g in GLYPHS if (_char(g) or "").isdigit()]
    digits.sort(key=lambda g: _char(g))
    return "".join(f"<span>{html.escape(_char(g))}</span>" for g in digits)


def block_punctuation():
    punct = [g for g in GLYPHS
             if not ((_char(g) or "").isalnum())]
    punct = [g for g in punct if _char(g) not in (None,)]
    punct.sort(key=lambda g: ord(_char(g)))
    return "\n        ".join(f"<span>{html.escape(_char(g))}</span>" for g in punct)


BLOCKS = {
    "count": block_count,
    "alphabet": block_alphabet,
    "numerals": block_numerals,
    "punctuation": block_punctuation,
}


def regenerate(text):
    for name, builder in BLOCKS.items():
        pattern = re.compile(
            re.escape(BEGIN.format(name=name)) + r"(.*?)" + re.escape(END.format(name=name)),
            re.DOTALL,
        )
        if not pattern.search(text):
            raise SystemExit(f"marker block {name!r} missing from {SPECIMEN}")
        text = pattern.sub(
            lambda m, b=builder: BEGIN.format(name=name) + "\n        "
            + b() + "\n      " + END.format(name=name),
            text,
        )
    return text


def main():
    original = SPECIMEN.read_text(encoding="utf-8")
    fresh = regenerate(original)
    if "--check" in sys.argv:
        if fresh != original:
            sys.exit(
                f"{SPECIMEN} is stale relative to the glyph definitions — "
                "run `py scripts/gen_specimen.py` and commit."
            )
        print(f"specimen up to date ({len(GLYPHS)} glyphs)")
        return
    SPECIMEN.write_text(fresh, encoding="utf-8")
    print(f"regenerated {SPECIMEN} ({len(GLYPHS)} glyphs)")


if __name__ == "__main__":
    main()
