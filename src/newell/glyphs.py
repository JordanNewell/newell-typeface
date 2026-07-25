"""Declarative glyph definitions for the four starter letters.

v0.1 ships only N, E, I, H to prove the generator pipeline. The full
alphabet arrives in the next task.

Metrics (SPEC.md sections 2-6):
  cap height 700, baseline 0, stroke width 110, default side bearing 90.

The N diagonal is the family signature (SPEC section 1). It must be 45
degrees, which forces the two vertical rail centers to be exactly cap-
height (700) apart: dx = dy = 700. The diagonal runs from the top of
the left rail down to the bottom of the right rail.

Advance widths use the SPEC formula: advance = left_bearing + bbox_width
+ right_bearing, where bbox_width is the horizontal extent of the
glyph's primitives (edge to edge, not center to center).
"""

CAP_HEIGHT = 700
BASELINE = 0
STROKE = 110
SIDE_BEARING = 90


def _advance(bbox_width):
    """Default advance = left + bbox_width + right side bearings."""
    return SIDE_BEARING + bbox_width + SIDE_BEARING


# ---------------------------------------------------------------------------
# N: two vertical rails + signature 45-degree diagonal.
# Rail centers 700 units apart so the diagonal is exactly 45 degrees.
# ---------------------------------------------------------------------------
_N_LEFT_X = SIDE_BEARING + STROKE / 2          # 145
_N_RIGHT_X = _N_LEFT_X + CAP_HEIGHT            # 845
_N_BBOX = (_N_RIGHT_X + STROKE / 2) - (_N_LEFT_X - STROKE / 2)  # 810
N = {
    "name": "N",
    "unicode": "U+004E",
    "advance": _advance(_N_BBOX),              # 990
    "primitives": [
        {"type": "vline", "x": _N_LEFT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "vline", "x": _N_RIGHT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "diag", "x0": _N_LEFT_X, "y0": CAP_HEIGHT,
         "x1": _N_RIGHT_X, "y1": BASELINE},
    ],
}


# ---------------------------------------------------------------------------
# E: one vertical rail on the left; three horizontal rails (top/mid/bot).
# bbox spans from the left edge of the vertical rail (90) to the right
# edge of the horizontals (475), giving width 385 -> advance 565.
# ---------------------------------------------------------------------------
_E_LEFT_X = SIDE_BEARING + STROKE / 2          # 145
_E_RIGHT_X = 475                                # right edge of horizontals
_E_BBOX = _E_RIGHT_X - (_E_LEFT_X - STROKE / 2)  # 385
_E_MID_Y = CAP_HEIGHT / 2                       # 350
E = {
    "name": "E",
    "unicode": "U+0045",
    "advance": _advance(_E_BBOX),               # 565
    "primitives": [
        {"type": "vline", "x": _E_LEFT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "hline", "y": CAP_HEIGHT, "x0": _E_LEFT_X, "x1": _E_RIGHT_X},
        {"type": "hline", "y": _E_MID_Y, "x0": _E_LEFT_X, "x1": _E_RIGHT_X},
        {"type": "hline", "y": BASELINE, "x0": _E_LEFT_X, "x1": _E_RIGHT_X},
    ],
}


# ---------------------------------------------------------------------------
# I: a single vertical rail. bbox width = STROKE = 110 -> advance 290.
# ---------------------------------------------------------------------------
_I_X = SIDE_BEARING + STROKE / 2               # 145
I = {
    "name": "I",
    "unicode": "U+0049",
    "advance": _advance(STROKE),               # 290
    "primitives": [
        {"type": "vline", "x": _I_X, "y0": BASELINE, "y1": CAP_HEIGHT},
    ],
}


# ---------------------------------------------------------------------------
# H: two vertical rails + one horizontal rail connecting them at mid.
# Same rail geometry as E (centers 145 and 475); horizontal rail spans
# the same x range. bbox = 385 -> advance 565.
# ---------------------------------------------------------------------------
_H_LEFT_X = SIDE_BEARING + STROKE / 2          # 145
_H_RIGHT_X = 475
_H_BBOX = _H_RIGHT_X - (_H_LEFT_X - STROKE / 2)  # 385
H = {
    "name": "H",
    "unicode": "U+0048",
    "advance": _advance(_H_BBOX),               # 565
    "primitives": [
        {"type": "vline", "x": _H_LEFT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "vline", "x": _H_RIGHT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "hline", "y": CAP_HEIGHT / 2, "x0": _H_LEFT_X, "x1": _H_RIGHT_X},
    ],
}


# Order matters: this is the order glyphs are emitted into the UFO and
# listed in public.glyphOrder. .notdef and space are prepended by the
# font builder; only the real letters go here.
GLYPHS = [N, E, I, H]
