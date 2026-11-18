"""UFO font assembly.

Builds a complete UFO font at sources/Newell-Regular.ufo with metadata
matching SPEC.md section 11, plus .notdef and space base glyphs.
"""

import os

import ufoLib2

from newell.generator import build_glyph, draw_contours_into_glyph
from newell.primitives import expand_primitive

FAMILY_NAME = "Newell"
STYLE_NAME = "Regular"
# UFO fontTools only exposes versionMajor.versionMinor (no third field), so
# v0.1.1 of the project maps to versionMajor=0, versionMinor=2 in the font
# binary metadata (the minor field bumps on each post-v0.1 update; the third
# digit is implicit and tracked in CHANGELOG.md / git tags).
VERSION_MAJOR = 0
VERSION_MINOR = 2
COPYRIGHT = "Copyright 2026 Jordan Newell"
DESIGNER = "Jordan Newell"
MANUFACTURER = "Jordan Newell"
PROJECT_URL = "https://jordannewell.github.io/newell-typeface/"
DESIGNER_URL = "https://jordannewell.com"
LICENSE_URL = "https://openfontlicense.org"
LICENSE_NAME = (
    "This Font Software is licensed under the SIL Open Font License, "
    "Version 1.1. This license is available with a FAQ at: "
    "https://openfontlicense.org"
)
DESCRIPTION = (
    "Newell is an original geometric display typeface built from parallel "
    "rails and 45-degree diagonals with squared terminals. No curves. "
    "Engineered, not drawn. https://jordannewell.github.io/newell-typeface/"
)
TRADEMARK = "Newell is a trademark of Jordan Newell."
VENDOR_ID = "JNEW"  # 4-character OS/2 vendor ID
# Unique font identifier (nameID 3). Format: version;vendor;PostScript name
UNIQUE_ID = f"{VERSION_MAJOR}.{VERSION_MINOR:03d};{VENDOR_ID};{FAMILY_NAME}-{STYLE_NAME}"
VERSION_STRING = f"Version {VERSION_MAJOR}.{VERSION_MINOR:03d}"

UNITS_PER_EM = 1000
ASCENDER = 800
CAP_HEIGHT = 700
X_HEIGHT = 500
DESCENDER = -200

NOTDEF_ADVANCE = 500
SPACE_ADVANCE = 250


def build_font(glyph_defs, glyph_order=None, style_name=STYLE_NAME,
               union_outlines=True):
    """Construct a ufoLib2 Font object from glyph definitions.

    glyph_defs: iterable of declarative glyph dicts (see newell.glyphs).
    glyph_order: optional explicit public.glyphOrder list. When None the
                 order is [.notdef, space] + names in glyph_defs order.
    style_name: subfamily for the name table (variable-font masters
                pass Light/Bold/Black; see scripts/build_variable.py).
    union_outlines: when False, emit the raw expanded primitives as
                 separate overlapping contours instead of boolean-unioning.
                 Overlaps render identically under nonzero winding, and
                 raw primitives keep contour/point counts identical across
                 stroke widths -- required for varLib master compatibility
                 (union topology shifts with width; see #8).
    """
    font = ufoLib2.Font()
    _set_info(font, style_name=style_name)

    _add_notdef(font)
    _add_space(font)

    built_names = []
    for glyph_def in glyph_defs:
        if union_outlines:
            build_glyph(font, glyph_def)
        else:
            _build_glyph_raw(font, glyph_def)
        built_names.append(glyph_def["name"])

    if glyph_order is None:
        glyph_order = [".notdef", "space"] + built_names
    else:
        # Always include the two base glyphs at the front if not present.
        prefix = [g for g in (".notdef", "space") if g not in glyph_order]
        glyph_order = prefix + list(glyph_order)
    font.lib["public.glyphOrder"] = glyph_order

    return font


def _set_info(font, style_name=STYLE_NAME):
    font.info.familyName = FAMILY_NAME
    font.info.styleName = style_name
    font.info.unitsPerEm = UNITS_PER_EM
    font.info.ascender = ASCENDER
    font.info.capHeight = CAP_HEIGHT
    font.info.xHeight = X_HEIGHT
    font.info.descender = DESCENDER
    font.info.openTypeOS2WidthClass = 5  # Medium per SPEC/task brief.
    font.info.openTypeOS2VendorID = VENDOR_ID
    font.info.versionMajor = VERSION_MAJOR
    font.info.versionMinor = VERSION_MINOR
    font.info.copyright = COPYRIGHT
    font.info.trademark = TRADEMARK
    font.info.postscriptFontName = f"{FAMILY_NAME}-{style_name}"
    font.info.postscriptFullName = f"{FAMILY_NAME} {style_name}"
    font.info.openTypeNameDesigner = DESIGNER
    font.info.openTypeNameDescription = DESCRIPTION
    font.info.openTypeNameManufacturer = MANUFACTURER
    font.info.openTypeNameManufacturerURL = PROJECT_URL
    font.info.openTypeNameDesignerURL = DESIGNER_URL
    font.info.openTypeNameLicense = LICENSE_NAME
    font.info.openTypeNameLicenseURL = LICENSE_URL
    font.info.openTypeNameVersion = VERSION_STRING
    font.info.openTypeNameUniqueID = UNIQUE_ID
    font.info.openTypeNamePreferredFamilyName = FAMILY_NAME
    font.info.openTypeNamePreferredSubfamilyName = STYLE_NAME
    font.info.openTypeOS2Selection = [7]  # USE_TYPO_METRICS, harmless default.


def _build_glyph_raw(font, glyph_def):
    """Emit a glyph's expanded primitives WITHOUT boolean union.

    Each primitive becomes its own closed contour; overlaps are left
    in place (nonzero winding renders them as solid). Used for
    variable-font masters, where identical point/contour counts across
    weights matter more than merged outlines.
    """
    from newell.generator import _parse_unicode

    name = glyph_def["name"]
    glyph = font.newGlyph(name)
    glyph.width = glyph_def["advance"]
    if "unicode" in glyph_def and glyph_def["unicode"] is not None:
        glyph.unicode = _parse_unicode(glyph_def["unicode"])
    width = glyph_def.get("_stroke", 110)
    pen = glyph.getPointPen()
    for spec in glyph_def.get("primitives", []):
        poly = expand_primitive(spec, width)
        pen.beginPath()
        pen.addPoint(poly[0], segmentType="line")
        for pt in poly[1:]:
            pen.addPoint(pt, segmentType="line")
        pen.endPath()


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


def build_and_save(glyph_defs, path, glyph_order=None, style_name=STYLE_NAME,
                   union_outlines=True):
    """Build a font from glyph defs and write it to `path`. Returns font."""
    font = build_font(glyph_defs, glyph_order=glyph_order,
                      style_name=style_name, union_outlines=union_outlines)
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
