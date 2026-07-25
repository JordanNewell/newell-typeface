"""Tests for the Newell generator.

Written with bare assert statements so the file runs directly with
`py src/newell/test_generator.py` (no pytest required). pytest will also
collect the test_* functions if available.

Run:
    py src/newell/test_generator.py
"""

import os
import sys

# Ensure src/ is importable when run directly.
_HERE = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.dirname(_HERE)
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from newell.primitives import STROKE_WIDTH, expand_diag, expand_hline, expand_primitive, expand_vline
from newell.generator import union_primitives
from newell.font import build_and_save, validate_ufo
from newell.glyphs import GLYPHS


def test_vline_corners():
    poly = expand_vline({"type": "vline", "x": 200, "y0": 0, "y1": 700})
    assert len(poly) == 4
    half = STROKE_WIDTH / 2
    expected = [
        (200 - half, 0),
        (200 + half, 0),
        (200 + half, 700),
        (200 - half, 700),
    ]
    assert poly == expected, poly


def test_vline_y0_y1_order_invariant():
    # Specifying y1 < y0 should still produce the same rectangle.
    a = expand_vline({"type": "vline", "x": 200, "y0": 0, "y1": 700})
    b = expand_vline({"type": "vline", "x": 200, "y0": 700, "y1": 0})
    assert a == b


def test_hline_corners():
    poly = expand_hline({"type": "hline", "y": 350, "x0": 100, "x1": 500})
    assert len(poly) == 4
    half = STROKE_WIDTH / 2
    expected = [
        (100, 350 - half),
        (500, 350 - half),
        (500, 350 + half),
        (100, 350 + half),
    ]
    assert poly == expected, poly


def test_diag_horizontal_terminal_corners():
    # A valid 45-degree diag with horizontal terminals.
    # top edge at y=700, x=90..200 (width 110)
    # bot edge at y=0,   x=790..900 (width 110)
    # left side from (90,700) to (790,0): dx=700, dy=700 -> 45 degrees
    # right side from (200,700) to (900,0): dx=700, dy=700 -> 45 degrees
    poly = expand_diag({
        "type": "diag",
        "top_y": 700, "top_x0": 90, "top_x1": 200,
        "bot_y": 0,   "bot_x0": 790, "bot_x1": 900,
    })
    assert len(poly) == 4
    expected = [(90, 700), (200, 700), (900, 0), (790, 0)]
    assert poly == expected, poly


def test_diag_unequal_terminal_lengths_raises():
    try:
        expand_diag({
            "type": "diag",
            "top_y": 700, "top_x0": 90, "top_x1": 200,  # length 110
            "bot_y": 0,   "bot_x0": 790, "bot_x1": 920,  # length 130
        })
    except ValueError:
        return
    raise AssertionError("expected ValueError for unequal terminal lengths")


def test_diag_non_45_left_side_raises():
    try:
        expand_diag({
            "type": "diag",
            "top_y": 700, "top_x0": 90, "top_x1": 200,
            "bot_y": 0,   "bot_x0": 890, "bot_x1": 1000,  # left dx=800 != dy=700
        })
    except ValueError:
        return
    raise AssertionError("expected ValueError for non-45-degree left side")


def test_diag_via_expand_primitive_raises():
    try:
        expand_primitive({
            "type": "diag",
            "top_y": 700, "top_x0": 90, "top_x1": 200,
            "bot_y": 0,   "bot_x0": 890, "bot_x1": 1000,
        })
    except ValueError:
        return
    raise AssertionError("expected ValueError for non-45-degree diag")


def test_unknown_primitive_type_raises():
    try:
        expand_primitive({"type": "squiggle", "x": 0})
    except ValueError:
        return
    raise AssertionError("expected ValueError for unknown primitive type")


def test_union_two_overlapping_vlines_single_contour():
    # Two vlines that overlap on x; union should produce one contour.
    specs = [
        {"type": "vline", "x": 200, "y0": 0, "y1": 700},
        {"type": "vline", "x": 220, "y0": 0, "y1": 700},
    ]
    contours = union_primitives(specs)
    assert len(contours) == 1, f"expected 1 contour, got {len(contours)}"
    assert len(contours[0]) == 4, f"expected 4 corners, got {len(contours[0])}"


def test_union_n_covers_expected_bbox():
    # The N glyph: two rails + a diagonal. booleanOperations splits
    # shapes that touch only at edges, so we may get up to 3 contours
    # (left rail + diag top-left corner, middle of diag, right rail +
    # diag bottom-right corner). What matters for rendering is that
    # the bbox is correct and the union fills the expected area.
    # OTF/CFF and TrueType use non-zero winding by default, so
    # touching contours render as a single connected shape.
    n = next(g for g in GLYPHS if g["name"] == "N")
    contours = union_primitives(n["primitives"])
    assert 1 <= len(contours) <= 4, f"unexpected contour count: {len(contours)}"

    all_x = [p[0] for c in contours for p in c]
    all_y = [p[1] for c in contours for p in c]
    bbox = (min(all_x), min(all_y), max(all_x), max(all_y))
    # Cap height and baseline bounds (allow small overshoot from the
    # _DIAG_OVERLAP epsilon used to ensure clean unions).
    assert -2 <= bbox[1] <= 0, f"bbox bottom out of range: {bbox}"
    assert 700 <= bbox[3] <= 702, f"bbox top out of range: {bbox}"
    assert bbox[0] < 200, f"bbox left out of range: {bbox}"
    assert bbox[2] > 800, f"bbox right out of range: {bbox}"


def test_build_and_validate_ufo(tmp_path=None):
    # Use a temp dir if pytest gives us one, else build inside sources/.
    import tempfile

    tmp = tmp_path or tempfile.mkdtemp(prefix="newell_test_")
    out = os.path.join(tmp, "Newell-Regular.ufo")
    names = [g["name"] for g in GLYPHS]
    build_and_save(GLYPHS, out)
    font = validate_ufo(out, names)
    assert set(names).issubset(set(font.keys()))
    assert ".notdef" in font.keys()
    assert "space" in font.keys()


def test_deterministic_two_runs():
    import tempfile

    tmp = tempfile.mkdtemp(prefix="newell_det_")
    a = os.path.join(tmp, "a.ufo")
    b = os.path.join(tmp, "b.ufo")
    build_and_save(GLYPHS, a)
    build_and_save(GLYPHS, b)
    # Compare glif file contents for each glyph.
    for sub in ("glyphs",):
        a_files = sorted(os.listdir(os.path.join(a, sub)))
        b_files = sorted(os.listdir(os.path.join(b, sub)))
        assert a_files == b_files, (a_files, b_files)
        for fname in a_files:
            with open(os.path.join(a, sub, fname), "rb") as fa, \
                 open(os.path.join(b, sub, fname), "rb") as fb:
                assert fa.read() == fb.read(), f"non-deterministic: {fname}"


def run_all():
    tests = [
        name for name in globals()
        if name.startswith("test_") and callable(globals()[name])
    ]
    tests.sort()
    failed = 0
    for name in tests:
        try:
            globals()[name]()
            print(f"PASS  {name}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"FAIL  {name}: {type(exc).__name__}: {exc}")
    print()
    print(f"{len(tests) - failed}/{len(tests)} passed")
    return failed


if __name__ == "__main__":
    sys.exit(1 if run_all() else 0)
