"""UFO font assembly.

Builds a complete UFO font at sources/Newell-Regular.ufo with metadata
matching SPEC.md section 11, plus .notdef and space base glyphs.
"""

import os

import ufoLib2

from newell.generator import build_glyph, draw_contours_into_glyph, union_primitives

FAMILY_NAME = "Newell"
STYLE_NAME = "Regular"
# UFO fontTools only exposes versionMajor.versionMinor (no third field), so
# v0.1.1 of the project maps to versionMajor=0, versionMinor=2 in the font
# binary metadata (the minor field bumps on each post-v0.1 update; the third
# digit is implicit and tracked in CHANGELOG.md / git tags).
VERSION_MAJOR = 0
VERSION_MINOR = 2
COPYRIGHT = "Copyright 2026 Jordan Newell"

UNITS_PER_EM = 1000
ASCENDER = 800
CAP_HEIGHT = 700
X_HEIGHT = 500
DESCENDER = -200

NOTDEF_ADVANCE = 500
SPACE_ADVANCE = 250


def build_font(glyph_defs, glyph_order=None):
    """Construct a ufoLib2 Font object from glyph definitions.

    glyph_defs: iterable of declarative glyph dicts (see newell.glyphs).
    glyph_order: optional explicit public.glyphOrder list. When None the
                 order is [.notdef, space] + names in glyph_defs order.
    """
    font = ufoLib2.Font()
    _set_info(font)

    _add_notdef(font)
    _add_space(font)

    built_names = []
    for glyph_def in glyph_defs:
        build_glyph(font, glyph_def)
        built_names.append(glyph_def["name"])

    if glyph_order is None:
        glyph_order = [".notdef", "space"] + built_names
    else:
        # Always include the two base glyphs at the front if not present.
        prefix = [g for g in (".notdef", "space") if g not in glyph_order]
        glyph_order = prefix + list(glyph_order)
    font.lib["public.glyphOrder"] = glyph_order

    return font


def _set_info(font):
    font.info.familyName = FAMILY_NAME
    font.info.styleName = STYLE_NAME
    font.info.unitsPerEm = UNITS_PER_EM
    font.info.ascender = ASCENDER
    font.info.capHeight = CAP_HEIGHT
    font.info.xHeight = X_HEIGHT
    font.info.descender = DESCENDER
    font.info.openTypeOS2WidthClass = 5  # Medium per SPEC/task brief.
    font.info.versionMajor = VERSION_MAJOR
    font.info.versionMinor = VERSION_MINOR
    font.info.copyright = COPYRIGHT
    font.info.postscriptFontName = f"{FAMILY_NAME}-{STYLE_NAME}"
    font.info.openTypeOS2Selection = [7]  # USE_TYPO_METRICS, harmless default.


def _add_notdef(font):
    """Empty box outline glyph. Advance 500; box inset 50 from sides."""
    glyph = font.newGlyph(".notdef")
    glyph.width = NOTDEF_ADVANCE
    # A simple box outline: rectangle from (50, -50) to (450, 750),
    # stroke 50. Emitted as the outline of a hollow rectangle using two
    # concentric contours (outer CW, inner CCW) so the fill rule leaves
    # the interior empty. Coordinates snapped to integers.
    outer = [(50, -50), (450, -50), (450, 750), (50, 750)]
    inner = [(100, 0), (100, 700), (400, 700), (400, 0)]
    draw_contours_into_glyph(glyph, [outer, inner])


def _add_space(font):
    glyph = font.newGlyph("space")
    glyph.width = SPACE_ADVANCE
    glyph.unicode = 0x0020
    # No contours; advance-only.


def save_font(font, path, overwrite=True):
    """Save `font` to `path`, removing an existing UFO directory first.

    ufoLib2.Font.save(..., overwrite=True) handles overwrite, but only
    if the destination is an existing UFO. We delete to be safe so two
    consecutive runs produce byte-identical output.
    """
    if overwrite and os.path.exists(path):
        import shutil

        shutil.rmtree(path)
    font.save(path, overwrite=True)


def build_and_save(glyph_defs, path, glyph_order=None):
    """Build a font from glyph defs and write it to `path`. Returns font."""
    font = build_font(glyph_defs, glyph_order=glyph_order)
    save_font(font, path, overwrite=True)
    return font


def validate_ufo(path, expected_glyph_names):
    """Load the UFO back and assert it matches expectations.

    Returns the loaded Font for further inspection. Asserts:
      - all expected glyph names are present
      - .notdef and space exist
      - core metadata matches SPEC
      - every real glyph has at least one contour (except space)
    """
    font = ufoLib2.Font.open(path)
    names = set(font.keys())

    assert ".notdef" in names, "missing .notdef"
    assert "space" in names, "missing space"
    for name in expected_glyph_names:
        assert name in names, f"missing glyph {name!r}"

    # Metadata.
    assert font.info.familyName == FAMILY_NAME
    assert font.info.styleName == STYLE_NAME
    assert font.info.unitsPerEm == UNITS_PER_EM
    assert font.info.ascender == ASCENDER
    assert font.info.capHeight == CAP_HEIGHT
    assert font.info.xHeight == X_HEIGHT
    assert font.info.descender == DESCENDER
    assert font.info.openTypeOS2WidthClass == 5
    assert font.info.versionMajor == VERSION_MAJOR
    assert font.info.versionMinor == VERSION_MINOR
    assert font.info.copyright == COPYRIGHT

    # Every defined letter should have geometry; space should not.
    for name in expected_glyph_names:
        glyph = font[name]
        assert len(glyph) >= 1, f"{name} has no contours"
    assert len(font["space"]) == 0, "space should have no contours"
    assert len(font[".notdef"]) >= 1, ".notdef should have a box outline"

    return font
