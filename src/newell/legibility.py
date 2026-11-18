"""Legibility regression checks (issue #11).

Hard heuristics that run as part of the test suite so a glyph change
that breaks legibility gets caught before merge:

1. bbox bounds — every glyph's geometry must sit inside its declared
   side bearings and the em box (baseline/descender to cap height,
   with the documented +-2 unit tolerance from _DIAG_OVERLAP). This
   caught the v0.1.1 A leaning 350 units into the previous character's
   space on the harness's first run (fixed 2026-11-18).

2. pairwise distinctness — two glyphs are near-identical when BOTH
   hold:
     a. their absolute ink bboxes match within 2 units (position-aware,
        so period vs middledot — same 110x110 mark at different
        heights — compares as distinct), AND
     b. their 12x12 ink-coverage grid signatures are EXACTLY equal
        (every cell). The grid separates glyphs with
        equal ink area but different distribution (M vs N have the
        exact same total ink; the grid sees the V). Even-odd fill at
        cell centers handles counters (O's hole) without winding
        machinery.
   A documented allowlist covers intentional look-alikes — mirrors
   and the rectilinear-frame limitations ruled permanent on 2026-11-18
   (issues #3/#4/#5 closed, curves moved to a sibling family).

3. contour sanity — no glyph may union into more than 16 contours
   (catches boolean-union explosions after primitive edits).

run_checks(glyph_defs) returns a list of human-readable failure
strings; an empty list means all clear.
"""

from newell.generator import union_primitives
from newell.primitives import STROKE_WIDTH

_EPS = 2            # matches _DIAG_OVERLAP epsilon
_GRID = 12          # grid resolution for the ink signature
MAX_CONTOURS = 16

# Intentional look-alikes, each with the ruling that allows it.
# Mirror pairs: same shape, flipped — that is what the glyphs mean.
# Frame look-alikes: v0.1 rectilinear-frame limitations, ruled
# PERMANENT 2026-11-18 (curves belong to the sibling family, never to
# Newell; see vault ROADMAP + closed issues #3/#4/#5).
KNOWN_DUPLICATES = {
    # Mirrors
    frozenset(("parenleft", "parenright")),
    frozenset(("less", "greater")),
    frozenset(("quotedblleft", "quotedblright")),
    frozenset(("six", "nine")),
    # Rectilinear-frame family (D == O == 0; B == 8 == @ constructions)
    frozenset(("D", "O")),
    frozenset(("D", "zero")),
    frozenset(("O", "zero")),
    frozenset(("B", "eight")),
    frozenset(("B", "at")),
    frozenset(("eight", "at")),
    # Curly quotes: straight/open quote render as the same square mark —
    # documented v0.1.1 trade-off (see glyphs.py quoteleft comment;
    # open/closed distinction is a ROADMAP stretch goal).
    frozenset(("quotesingle", "quoteleft")),
}


def _glyph_geometry(glyph_def):
    """Union a glyph's primitives; return (contours, advance, name)."""
    contours = union_primitives(glyph_def.get("primitives", []),
                            glyph_def.get("_stroke", 110))
    return contours, glyph_def["advance"], glyph_def["name"]


def _bbox(contours):
    pts = [p for c in contours for p in c]
    if not pts:
        return None
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return (min(xs), min(ys), max(xs), max(ys))


def _point_in_contour(pt, contour):
    """Ray-casting even-odd test (exact for rectilinear polygons)."""
    x, y = pt
    inside = False
    n = len(contour)
    for i in range(n):
        x0, y0 = contour[i]
        x1, y1 = contour[(i + 1) % n]
        if (y0 > y) != (y1 > y):
            t = (y - y0) / (y1 - y0)
            if x < x0 + t * (x1 - x0):
                inside = not inside
    return inside


def _ink_signature(contours, box):
    """6x6 ink-coverage grid over the glyph's absolute ink bbox.

    Cell value 1 = even-odd filled at the cell center (all contours
    tested, parity across contours handles counters). Returned as a
    flat tuple; all-ones offset keeps zero-ink glyphs comparable.
    """
    x0, y0, x1, y1 = box
    w = x1 - x0
    h = y1 - y0
    if w <= 0 or h <= 0:
        return tuple([0] * (_GRID * _GRID))
    sig = []
    for row in range(_GRID):
        for col in range(_GRID):
            cx = x0 + (col + 0.5) * w / _GRID
            cy = y0 + (row + 0.5) * h / _GRID
            parity = False
            for c in contours:
                if _point_in_contour((cx, cy), c):
                    parity = not parity
            sig.append(1 if parity else 0)
    return tuple(sig)


def check_bbox_bounds(glyph_def, contours):
    failures = []
    name = glyph_def["name"]
    advance = glyph_def["advance"]
    width = glyph_def.get("_stroke", 110)
    if not contours:
        return failures
    x0, y0, x1, y1 = _bbox(contours)
    if x0 < -_EPS:
        failures.append(f"{name}: bbox left {x0} < -{_EPS}")
    if x1 > advance - 90 + _EPS:
        failures.append(
            f"{name}: bbox right {x1} > advance {advance} - right_bearing 90 + {_EPS}"
        )
    if y0 < -202 - _EPS:
        failures.append(f"{name}: bbox bottom {y0} below descender limit")
    # Vertical convention: rails are CENTERED on the metric lines, so a
    # cap-height rail's ink reaches 700 + stroke/2 (755). NOTE: this makes
    # ink overshoot font.info.capHeight (700) by half a stroke -- a
    # font-wide metadata-vs-ink discrepancy surfaced to the maintainer
    # 2026-11-18 (fixing it means re-drawing every glyph; out of sweep
    # scope). The check encodes the shipped convention, not the ideal.
    # One's flag legitimately reaches the SPEC ascender (800); a
    # cap-centered rail's ink reaches 700 + stroke/2. Ceiling = the
    # larger of the two, per the glyph's own stroke width.
    top_limit = max(800, 700 + width / 2) + _EPS
    if y1 > top_limit:
        failures.append(f"{name}: bbox top {y1} above cap overshoot limit {top_limit}")
    return failures


def check_contour_count(name, contours):
    if len(contours) > MAX_CONTOURS:
        return [
            f"{name}: {len(contours)} contours exceeds max {MAX_CONTOURS} "
            "(union explosion?)"
        ]
    return []


def check_pairwise_distinct(geometries):
    """geometries: list of (name, contours, advance). Returns failures."""
    failures = []
    infos = []
    for name, contours, _advance in geometries:
        box = _bbox(contours)
        if box is None:
            continue
        infos.append((name, box, _ink_signature(contours, box)))
    for i in range(len(infos)):
        for j in range(i + 1, len(infos)):
            name_a, box_a, sig_a = infos[i]
            name_b, box_b, sig_b = infos[j]
            if any(abs(a - b) > _EPS for a, b in zip(box_a, box_b)):
                continue
            # Near-identical means INDISTINGUISHABLE: every grid cell
            # matches exactly. "Similar" glyphs (B vs O share the outer
            # frame; M vs N share the ink budget) differ in enough cells
            # to read as different at display size — a typeface is
            # allowed to have similar glyphs, not identical ones.
            if sig_a != sig_b:
                continue
            pair = frozenset((name_a, name_b))
            if pair in KNOWN_DUPLICATES:
                continue
            failures.append(
                f"near-identical glyphs: {name_a} vs {name_b} "
                f"(bbox {box_a}, identical 12x12 ink signature). "
                "If intentional, add to legibility.KNOWN_DUPLICATES "
                "with a comment citing the ruling that allows it."
            )
    return failures


def run_checks(glyph_defs):
    """Run all heuristics; return list of failure strings (empty = ok)."""
    failures = []
    geometries = []
    for glyph_def in glyph_defs:
        contours, _advance, name = _glyph_geometry(glyph_def)
        geometries.append((name, contours, _advance))
        failures.extend(check_bbox_bounds(glyph_def, contours))
        failures.extend(check_contour_count(name, contours))
    failures.extend(check_pairwise_distinct(geometries))
    return failures
