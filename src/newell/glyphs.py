"""Declarative glyph definitions for the full uppercase A-Z alphabet.

v0.1 ships the 26 uppercase Latin letters per SPEC.md section 10. The
seven hero glyphs (A, E, M, N, R, S, W) establish the personality; the
rest inherit their proportions and stroke treatment.

Metrics (SPEC.md sections 2-6):
  cap height 700, baseline 0, stroke width 110, default side bearing 90.

The N diagonal is the family signature (SPEC section 1). It must be 45
degrees, which forces the two vertical rail centers to be exactly cap-
height (700) apart: dx = dy = 700. The diagonal runs from the top of
the left rail down to the bottom of the right rail.

Diagonal letters (A, K, M, R, V, W, X, Y, Z, Q) inherit the 45-degree
vocabulary. Some letters that are traditionally curved (B, D, O, P, C,
G, J, S) are approximated by rectilinear frames -- a deliberate v0.1
trade-off documented per-glyph below. SPEC.md section 7 explicitly
permits this.

Advance widths use the SPEC formula: advance = left_bearing + bbox_width
+ right_bearing, where bbox_width is the horizontal extent of the
glyph's primitives (edge to edge, not center to center).
"""

CAP_HEIGHT = 700
BASELINE = 0
STROKE = 110
HALF = STROKE / 2  # 55
SIDE_BEARING = 90

# When a diagonal's horizontal terminal coincides exactly with a rail's
# top/bottom edge, booleanOperations.union() treats them as touching but
# not overlapping (zero-width intersection) and emits them as separate
# contours. We extend each diag terminal by _DIAG_OVERLAP units on each
# side so the union has a small but non-zero overlap region. The
# resulting 1-unit protrusions at the corners are sub-pixel at any
# reasonable render size (1/1000 of the em).
_DIAG_OVERLAP = 1.0

# Standard column centers. Most rectilinear letters use NARROW rails
# (E/H/L/T/U family); N/M-style diagonals force WIDE spacing (700 apart).
_COL_L = SIDE_BEARING + HALF          # 145 -- left rail center
_COL_R_NARROW = 475                   # right rail center for E/H-style
_COL_R_WIDE = _COL_L + CAP_HEIGHT     # 845 -- right rail center for N
_LEFT_EDGE = _COL_L - HALF            # 90
_RIGHT_EDGE_NARROW = _COL_R_NARROW + HALF  # 530
_RIGHT_EDGE_WIDE = _COL_R_WIDE + HALF      # 900
_MID_Y = CAP_HEIGHT / 2               # 350


def _advance(bbox_width):
    """Default advance = left + bbox_width + right side bearings."""
    return SIDE_BEARING + bbox_width + SIDE_BEARING


def _bbox(left_edge, right_edge):
    return right_edge - left_edge


# ---------------------------------------------------------------------------
# A: two 45-degree diagonals meeting at apex (cap height), crossbar rail
# at y=200. The diagonals form an inverted-V; the crossbar connects the
# two legs at the height where their inner edges intersect. Each leg is
# full cap height (dy=700) so dx=700 per leg; total width 1510. This is
# geometrically forced -- a true 45-degree A spans 2x the diagonal
# throw. Width is wider than the average cap; advance ~1690. Hero glyph.
# ---------------------------------------------------------------------------
_A_APEX_X = _COL_L + CAP_HEIGHT / 2     # 495 -- apex centerline
_A_LEG_DX = CAP_HEIGHT                   # 700 -- horizontal throw per leg
_A_LEFT_EDGE = _A_APEX_X - _A_LEG_DX - HALF  # -260
_A_RIGHT_EDGE = _A_APEX_X + _A_LEG_DX + HALF  # 1250
# At crossbar y=200, leg centers are at apex +/- (700-200) = apex +/- 500
_A_CROSSBAR_Y = 200
_A_CROSSBAR_DX = CAP_HEIGHT - _A_CROSSBAR_Y  # 500
A = {
    "name": "A",
    "unicode": "U+0041",
    "advance": _advance(_bbox(_A_LEFT_EDGE, _A_RIGHT_EDGE)),
    "primitives": [
        # Left leg: apex top, bottom-left terminal
        {"type": "diag",
         "top_y": CAP_HEIGHT,
         "top_x0": _A_APEX_X - HALF - _DIAG_OVERLAP,
         "top_x1": _A_APEX_X + HALF + _DIAG_OVERLAP,
         "bot_y": BASELINE,
         "bot_x0": _A_APEX_X - _A_LEG_DX - HALF - _DIAG_OVERLAP,
         "bot_x1": _A_APEX_X - _A_LEG_DX + HALF + _DIAG_OVERLAP},
        # Right leg: apex top, bottom-right terminal
        {"type": "diag",
         "top_y": CAP_HEIGHT,
         "top_x0": _A_APEX_X - HALF - _DIAG_OVERLAP,
         "top_x1": _A_APEX_X + HALF + _DIAG_OVERLAP,
         "bot_y": BASELINE,
         "bot_x0": _A_APEX_X + _A_LEG_DX - HALF - _DIAG_OVERLAP,
         "bot_x1": _A_APEX_X + _A_LEG_DX + HALF + _DIAG_OVERLAP},
        # Crossbar at y=200, centerline-to-centerline between the legs
        {"type": "hline", "y": _A_CROSSBAR_Y,
         "x0": _A_APEX_X - _A_CROSSBAR_DX,
         "x1": _A_APEX_X + _A_CROSSBAR_DX},
    ],
}


# ---------------------------------------------------------------------------
# B: rectilinear approximation of a curved letter. Left vertical rail
# full height; three horizontal rails (top, mid, bottom) extending to a
# right column; one short right-side vertical rail from top to mid
# (upper bowl), and one from mid to bottom (lower bowl). The bowls are
# open on the right -- they read as squared-off B counter-shapes.
# ---------------------------------------------------------------------------
_B_LEFT_X = _COL_L                        # 145
_B_RIGHT_X = _COL_R_NARROW                # 475
_B_BBOX = _bbox(_LEFT_EDGE, _RIGHT_EDGE_NARROW)  # 440
_B_MID_Y = _MID_Y                         # 350
B = {
    "name": "B",
    "unicode": "U+0042",
    "advance": _advance(_B_BBOX),
    "primitives": [
        # Left vertical rail, full height
        {"type": "vline", "x": _B_LEFT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        # Top horizontal
        {"type": "hline", "y": CAP_HEIGHT, "x0": _B_LEFT_X, "x1": _B_RIGHT_X},
        # Mid horizontal
        {"type": "hline", "y": _B_MID_Y, "x0": _B_LEFT_X, "x1": _B_RIGHT_X},
        # Bottom horizontal
        {"type": "hline", "y": BASELINE, "x0": _B_LEFT_X, "x1": _B_RIGHT_X},
        # Right vertical rail, top half (upper bowl closure)
        {"type": "vline", "x": _B_RIGHT_X, "y0": _B_MID_Y, "y1": CAP_HEIGHT},
        # Right vertical rail, bottom half (lower bowl closure)
        {"type": "vline", "x": _B_RIGHT_X, "y0": BASELINE, "y1": _B_MID_Y},
    ],
}


# ---------------------------------------------------------------------------
# C: open rectilinear frame. Top + left + bottom rails form three sides
# of a rectangle (the right side is open). Reads as a squared C.
# ---------------------------------------------------------------------------
_C_LEFT_X = _COL_L
_C_RIGHT_X = _COL_R_NARROW
_C_BBOX = _bbox(_LEFT_EDGE, _RIGHT_EDGE_NARROW)
C = {
    "name": "C",
    "unicode": "U+0043",
    "advance": _advance(_C_BBOX),
    "primitives": [
        {"type": "vline", "x": _C_LEFT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "hline", "y": CAP_HEIGHT, "x0": _C_LEFT_X, "x1": _C_RIGHT_X},
        {"type": "hline", "y": BASELINE, "x0": _C_LEFT_X, "x1": _C_RIGHT_X},
    ],
}


# ---------------------------------------------------------------------------
# D: closed rectilinear frame (a square). Left vertical + top + bottom +
# right vertical rails. v0.1 accepts D as a square with no curves; a
# future revision may add a 45-degree chamfer on the top-right and
# bottom-right corners to suggest a D curve (would require SPEC
# amendment for partial diagonals).
# ---------------------------------------------------------------------------
_D_LEFT_X = _COL_L
_D_RIGHT_X = _COL_R_NARROW
_D_BBOX = _bbox(_LEFT_EDGE, _RIGHT_EDGE_NARROW)
D = {
    "name": "D",
    "unicode": "U+0044",
    "advance": _advance(_D_BBOX),
    "primitives": [
        {"type": "vline", "x": _D_LEFT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "vline", "x": _D_RIGHT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "hline", "y": CAP_HEIGHT, "x0": _D_LEFT_X, "x1": _D_RIGHT_X},
        {"type": "hline", "y": BASELINE, "x0": _D_LEFT_X, "x1": _D_RIGHT_X},
    ],
}


# ---------------------------------------------------------------------------
# E: hero glyph. One vertical rail on the left; three horizontal rails
# (top/mid/bottom). bbox 90..530 = 440 -> advance 620.
# ---------------------------------------------------------------------------
_E_LEFT_X = _COL_L                        # 145
_E_RIGHT_X = _COL_R_NARROW                # 475
_E_BBOX = _bbox(_LEFT_EDGE, _RIGHT_EDGE_NARROW)
E = {
    "name": "E",
    "unicode": "U+0045",
    "advance": _advance(_E_BBOX),
    "primitives": [
        {"type": "vline", "x": _E_LEFT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "hline", "y": CAP_HEIGHT, "x0": _E_LEFT_X, "x1": _E_RIGHT_X},
        {"type": "hline", "y": _MID_Y, "x0": _E_LEFT_X, "x1": _E_RIGHT_X},
        {"type": "hline", "y": BASELINE, "x0": _E_LEFT_X, "x1": _E_RIGHT_X},
    ],
}


# ---------------------------------------------------------------------------
# F: E minus the bottom horizontal. Top + mid arms only.
# ---------------------------------------------------------------------------
_F_LEFT_X = _COL_L
_F_RIGHT_X = _COL_R_NARROW
_F_BBOX = _bbox(_LEFT_EDGE, _RIGHT_EDGE_NARROW)
F = {
    "name": "F",
    "unicode": "U+0046",
    "advance": _advance(_F_BBOX),
    "primitives": [
        {"type": "vline", "x": _F_LEFT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "hline", "y": CAP_HEIGHT, "x0": _F_LEFT_X, "x1": _F_RIGHT_X},
        {"type": "hline", "y": _MID_Y, "x0": _F_LEFT_X, "x1": _F_RIGHT_X},
    ],
}


# ---------------------------------------------------------------------------
# G: C (open rectilinear frame: top + left + bottom rails) plus an inward
# horizontal tongue at mid-height, with a short vertical tip descending
# from the tongue's right end. The descending tip is what distinguishes
# G from E-with-an-extra-arm -- without it, the crossbar reads as E's
# middle arm rather than as G's tongue. We extend the tongue only part-
# way across (not all the way to the left rail) so the C's open right
# side remains readable above and below the tongue.
# ---------------------------------------------------------------------------
_G_LEFT_X = _COL_L
_G_RIGHT_X = _COL_R_NARROW
_G_BBOX = _bbox(_LEFT_EDGE, _RIGHT_EDGE_NARROW)
# Tongue extends inward from the right column to about a third of the
# way across. Length matches E's mid-arm family proportions.
_G_BAR_X0 = _COL_L + (CAP_HEIGHT / 4)   # 320 -- inner end of tongue
_G_BAR_X1 = _G_RIGHT_X                  # 475 -- right end (outer)
# Tongue tip descends from the crossbar down by a quarter of cap height.
_G_TONGUE_TIP_Y = _MID_Y - (CAP_HEIGHT / 4)  # 175
G = {
    "name": "G",
    "unicode": "U+0047",
    "advance": _advance(_G_BBOX),
    "primitives": [
        {"type": "vline", "x": _G_LEFT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "hline", "y": CAP_HEIGHT, "x0": _G_LEFT_X, "x1": _G_RIGHT_X},
        {"type": "hline", "y": BASELINE, "x0": _G_LEFT_X, "x1": _G_RIGHT_X},
        # Inward tongue at mid-height
        {"type": "hline", "y": _MID_Y, "x0": _G_BAR_X0, "x1": _G_BAR_X1},
        # Descending tongue tip at the right end of the crossbar
        {"type": "vline", "x": _G_RIGHT_X, "y0": _G_TONGUE_TIP_Y, "y1": _MID_Y},
    ],
}


# ---------------------------------------------------------------------------
# H: hero glyph family member. Two vertical rails + mid horizontal.
# ---------------------------------------------------------------------------
_H_LEFT_X = _COL_L
_H_RIGHT_X = _COL_R_NARROW
_H_BBOX = _bbox(_LEFT_EDGE, _RIGHT_EDGE_NARROW)
H = {
    "name": "H",
    "unicode": "U+0048",
    "advance": _advance(_H_BBOX),
    "primitives": [
        {"type": "vline", "x": _H_LEFT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "vline", "x": _H_RIGHT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "hline", "y": _MID_Y, "x0": _H_LEFT_X, "x1": _H_RIGHT_X},
    ],
}


# ---------------------------------------------------------------------------
# I: single vertical rail. Hero glyph family member. bbox = STROKE.
# ---------------------------------------------------------------------------
_I_X = _COL_L
I = {
    "name": "I",
    "unicode": "U+0049",
    "advance": _advance(STROKE),
    "primitives": [
        {"type": "vline", "x": _I_X, "y0": BASELINE, "y1": CAP_HEIGHT},
    ],
}


# ---------------------------------------------------------------------------
# J: I (vertical rail) plus a bottom horizontal rail extending to the
# right, with a short right-side vertical going up to suggest a hook.
# Reads as a squared J with a flat foot. We widen the bbox to make room
# for the foot; the vertical rail sits on the left like I.
# ---------------------------------------------------------------------------
_J_LEFT_X = _COL_L
_J_RIGHT_X = _COL_R_NARROW
_J_FOOT_TOP_Y = CAP_HEIGHT / 4           # 175 -- where the right riser stops
_J_BBOX = _bbox(_LEFT_EDGE, _RIGHT_EDGE_NARROW)
J = {
    "name": "J",
    "unicode": "U+004A",
    "advance": _advance(_J_BBOX),
    "primitives": [
        # Main vertical stem on the left (full height, like I)
        {"type": "vline", "x": _J_LEFT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        # Bottom horizontal extending right
        {"type": "hline", "y": BASELINE, "x0": _J_LEFT_X, "x1": _J_RIGHT_X},
        # Short right-side riser going up from the foot
        {"type": "vline", "x": _J_RIGHT_X, "y0": BASELINE, "y1": _J_FOOT_TOP_Y},
    ],
}


# ---------------------------------------------------------------------------
# K: left vertical rail + two 45-degree diagonals meeting at the mid-
# left (the diagonals emanate from the rail's mid-right toward top-right
# and bottom-right corners). Each diagonal spans half cap height (350)
# horizontally and vertically. The diagonals' left terminals land on
# the right edge of the vertical rail with _DIAG_OVERLAP.
# ---------------------------------------------------------------------------
_K_LEFT_X = _COL_L
_K_DIAG_DX = CAP_HEIGHT / 2               # 350 -- half cap for 45deg over half height
_K_TOP_RIGHT_X = _K_LEFT_X + _K_DIAG_DX   # 495 -- centerline of upper-right terminal
_K_BOT_RIGHT_X = _K_LEFT_X + _K_DIAG_DX   # 495 -- centerline of lower-right terminal
_K_RIGHT_EDGE = _K_TOP_RIGHT_X + HALF     # 550
_K_BBOX = _bbox(_LEFT_EDGE, _K_RIGHT_EDGE)
_K_LEFT_RIGHT_EDGE = _K_LEFT_X + HALF     # 200 -- right edge of vertical rail
_K_MID_Y = _MID_Y                          # 350
_K_TOP_Y = CAP_HEIGHT                      # 700
_K_DIAG_HALF_HEIGHT = CAP_HEIGHT / 2       # 350
K = {
    "name": "K",
    "unicode": "U+004B",
    "advance": _advance(_K_BBOX),
    "primitives": [
        {"type": "vline", "x": _K_LEFT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        # Upper diagonal: bot terminal anchored on the left rail
        # (rail-width 110, center x=145); top terminal at (495, 700).
        # dx=350, dy=350 -> 45deg.
        {"type": "diag",
         "top_y": _K_TOP_Y,
         "top_x0": _K_TOP_RIGHT_X - HALF - _DIAG_OVERLAP,
         "top_x1": _K_TOP_RIGHT_X + HALF + _DIAG_OVERLAP,
         "bot_y": _K_MID_Y,
         "bot_x0": _K_LEFT_X - HALF - _DIAG_OVERLAP,
         "bot_x1": _K_LEFT_X + HALF + _DIAG_OVERLAP},
        # Lower diagonal: top terminal anchored on left rail; bot at (495, 0)
        {"type": "diag",
         "top_y": _K_MID_Y,
         "top_x0": _K_LEFT_X - HALF - _DIAG_OVERLAP,
         "top_x1": _K_LEFT_X + HALF + _DIAG_OVERLAP,
         "bot_y": BASELINE,
         "bot_x0": _K_BOT_RIGHT_X - HALF - _DIAG_OVERLAP,
         "bot_x1": _K_BOT_RIGHT_X + HALF + _DIAG_OVERLAP},
    ],
}


# ---------------------------------------------------------------------------
# L: left vertical rail + bottom horizontal. Minimal rectilinear letter.
# ---------------------------------------------------------------------------
_L_LEFT_X = _COL_L
_L_RIGHT_X = _COL_R_NARROW
_L_BBOX = _bbox(_LEFT_EDGE, _RIGHT_EDGE_NARROW)
L = {
    "name": "L",
    "unicode": "U+004C",
    "advance": _advance(_L_BBOX),
    "primitives": [
        {"type": "vline", "x": _L_LEFT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "hline", "y": BASELINE, "x0": _L_LEFT_X, "x1": _L_RIGHT_X},
    ],
}


# ---------------------------------------------------------------------------
# M: hero glyph. Two outer vertical rails + two 45-degree diagonals
# meeting at center-baseline (inverted-V inside the frame). Each diagonal
# spans half the cap width (350 horizontal x 700 vertical is NOT 45deg;
# we use 350x350 with the apex at mid-height). To match the N rail
# spacing and form a recognizable M, the diagonals descend from each
# rail's top to a center point at the baseline; this forces dx=dy=350
# (half cap), so the diagonals meet at center-baseline only if the rails
# are 700 apart. With rails at 145 and 845 (N spacing), the center is at
# 495 -- half way is 350 from each rail top. The diagonals form a V from
# (145,700) and (845,700) meeting at (495, 0). dx=350, dy=700 -- NOT
# 45deg. So we either shorten the V (meet at y=350) or accept wider M.
# We meet at y=350 (mid-height): each diagonal is dx=350, dy=350, 45deg.
# Reads as M with the V notch reaching the midline.
# ---------------------------------------------------------------------------
_M_LEFT_X = _COL_L                         # 145
_M_RIGHT_X = _COL_R_WIDE                   # 845
_M_LEFT_EDGE = _LEFT_EDGE                  # 90
_M_RIGHT_EDGE = _RIGHT_EDGE_WIDE           # 900
_M_BBOX = _bbox(_M_LEFT_EDGE, _M_RIGHT_EDGE)
_M_CENTER_X = (_M_LEFT_X + _M_RIGHT_X) / 2  # 495
_M_NOTCH_Y = _MID_Y                         # 350 -- V meets at midline
_M_DIAG_DX = (_M_RIGHT_X - _M_LEFT_X) / 2   # 350
_M_LEFT_RIGHT_EDGE = _M_LEFT_X + HALF       # 200
_M_RIGHT_LEFT_EDGE = _M_RIGHT_X - HALF      # 790
M = {
    "name": "M",
    "unicode": "U+004D",
    "advance": _advance(_M_BBOX),
    "primitives": [
        {"type": "vline", "x": _M_LEFT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "vline", "x": _M_RIGHT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        # Left diagonal: from left rail top-right (x=145, y=700) down to
        # center (x=495, y=350). dx=350, dy=350 -> 45deg.
        {"type": "diag",
         "top_y": CAP_HEIGHT,
         "top_x0": _M_LEFT_X - HALF - _DIAG_OVERLAP,
         "top_x1": _M_LEFT_X + HALF + _DIAG_OVERLAP,
         "bot_y": _M_NOTCH_Y,
         "bot_x0": _M_CENTER_X - HALF - _DIAG_OVERLAP,
         "bot_x1": _M_CENTER_X + HALF + _DIAG_OVERLAP},
        # Right diagonal: from right rail top-left (x=845, y=700) down to
        # center (x=495, y=350). dx=350, dy=350 -> 45deg.
        {"type": "diag",
         "top_y": CAP_HEIGHT,
         "top_x0": _M_RIGHT_X - HALF - _DIAG_OVERLAP,
         "top_x1": _M_RIGHT_X + HALF + _DIAG_OVERLAP,
         "bot_y": _M_NOTCH_Y,
         "bot_x0": _M_CENTER_X - HALF - _DIAG_OVERLAP,
         "bot_x1": _M_CENTER_X + HALF + _DIAG_OVERLAP},
    ],
}


# ---------------------------------------------------------------------------
# N: hero glyph, family signature. Two vertical rails 700 apart + one
# 45-degree diagonal from top-of-left to bottom-of-right.
# ---------------------------------------------------------------------------
_N_LEFT_X = _COL_L
_N_RIGHT_X = _COL_R_WIDE
_N_BBOX = _bbox(_LEFT_EDGE, _RIGHT_EDGE_WIDE)
N = {
    "name": "N",
    "unicode": "U+004E",
    "advance": _advance(_N_BBOX),
    "primitives": [
        {"type": "vline", "x": _N_LEFT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "vline", "x": _N_RIGHT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        # Diagonal: top edge sits on cap height across the left rail
        # (x=90 to 200); bottom edge sits on baseline across the right
        # rail (x=790 to 900). Terminals extend _DIAG_OVERLAP past the
        # rail width on each side so union() merges cleanly with the
        # rails (no zero-width intersection). dx=dy=700 on both sides.
        {"type": "diag",
         "top_y": CAP_HEIGHT,
         "top_x0": _LEFT_EDGE - _DIAG_OVERLAP,
         "top_x1": _N_LEFT_X + HALF + _DIAG_OVERLAP,
         "bot_y": BASELINE,
         "bot_x0": _N_RIGHT_X - HALF - _DIAG_OVERLAP,
         "bot_x1": _RIGHT_EDGE_WIDE + _DIAG_OVERLAP},
    ],
}


# ---------------------------------------------------------------------------
# O: closed rectilinear frame (a square). Same construction as D; v0.1
# accepts O as a square per SPEC section 7. The "rounded" O of humanist
# typefaces has no analogue in pure rails + 45-degree diagonals.
# ---------------------------------------------------------------------------
_O_LEFT_X = _COL_L
_O_RIGHT_X = _COL_R_NARROW
_O_BBOX = _bbox(_LEFT_EDGE, _RIGHT_EDGE_NARROW)
O = {
    "name": "O",
    "unicode": "U+004F",
    "advance": _advance(_O_BBOX),
    "primitives": [
        {"type": "vline", "x": _O_LEFT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "vline", "x": _O_RIGHT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "hline", "y": CAP_HEIGHT, "x0": _O_LEFT_X, "x1": _O_RIGHT_X},
        {"type": "hline", "y": BASELINE, "x0": _O_LEFT_X, "x1": _O_RIGHT_X},
    ],
}


# ---------------------------------------------------------------------------
# P: left vertical rail + two horizontals (top, mid) + short right-side
# vertical (top half only). Like B without the lower bowl. Rectilinear
# approximation of curved P.
# ---------------------------------------------------------------------------
_P_LEFT_X = _COL_L
_P_RIGHT_X = _COL_R_NARROW
_P_BBOX = _bbox(_LEFT_EDGE, _RIGHT_EDGE_NARROW)
P = {
    "name": "P",
    "unicode": "U+0050",
    "advance": _advance(_P_BBOX),
    "primitives": [
        {"type": "vline", "x": _P_LEFT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "hline", "y": CAP_HEIGHT, "x0": _P_LEFT_X, "x1": _P_RIGHT_X},
        {"type": "hline", "y": _MID_Y, "x0": _P_LEFT_X, "x1": _P_RIGHT_X},
        # Right vertical, top half only (closes the bowl)
        {"type": "vline", "x": _P_RIGHT_X, "y0": _MID_Y, "y1": CAP_HEIGHT},
    ],
}


# ---------------------------------------------------------------------------
# Q: O (square frame) + a 45-degree diagonal tail. The tail exits the
# frame at the bottom-right corner and extends down-right to (x, y<0).
# We anchor the tail's interior end at the inside of the bottom rail
# (so it appears to emerge from the letter), then run dx=dy=200 to a
# terminal below baseline at y=-200 (matches descender metric).
# ---------------------------------------------------------------------------
_Q_LEFT_X = _COL_L
_Q_RIGHT_X = _COL_R_NARROW
_Q_BBOX_WIDTH = _bbox(_LEFT_EDGE, _RIGHT_EDGE_NARROW)
# Tail: starts inside frame at (x=400, y=0); ends outside at (x=600, y=-200)
# dx=200, dy=200 -> 45deg.
_Q_TAIL_DX = 200
_Q_TAIL_INTERIOR_X = (_Q_LEFT_X + _Q_RIGHT_X) / 2 + 50  # 410 -- slightly right of center
_Q_TAIL_INTERIOR_Y = BASELINE
_Q_TAIL_EXTERIOR_X = _Q_TAIL_INTERIOR_X + _Q_TAIL_DX     # 610
_Q_TAIL_EXTERIOR_Y = BASELINE - _Q_TAIL_DX                # -200
_Q_RIGHT_EDGE_FOR_BBOX = max(_RIGHT_EDGE_NARROW, _Q_TAIL_EXTERIOR_X + HALF)
_Q_BOTTOM_EDGE_FOR_BBOX = _Q_TAIL_EXTERIOR_Y - HALF
# bbox spans original frame width PLUS the tail extension below baseline.
# Advance uses only horizontal bbox; vertical descender doesn't affect advance.
_Q_BBOX = _bbox(_LEFT_EDGE, _Q_RIGHT_EDGE_FOR_BBOX)
Q = {
    "name": "Q",
    "unicode": "U+0051",
    "advance": _advance(_Q_BBOX),
    "primitives": [
        {"type": "vline", "x": _Q_LEFT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "vline", "x": _Q_RIGHT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "hline", "y": CAP_HEIGHT, "x0": _Q_LEFT_X, "x1": _Q_RIGHT_X},
        {"type": "hline", "y": BASELINE, "x0": _Q_LEFT_X, "x1": _Q_RIGHT_X},
        # Diagonal tail emerging from the bottom-right of the frame
        {"type": "diag",
         "top_y": _Q_TAIL_INTERIOR_Y,
         "top_x0": _Q_TAIL_INTERIOR_X - HALF,
         "top_x1": _Q_TAIL_INTERIOR_X + HALF,
         "bot_y": _Q_TAIL_EXTERIOR_Y,
         "bot_x0": _Q_TAIL_EXTERIOR_X - HALF,
         "bot_x1": _Q_TAIL_EXTERIOR_X + HALF},
    ],
}


# ---------------------------------------------------------------------------
# R: hero glyph. P (left vertical + top + mid horizontals + right-top
# vertical) + a 45-degree diagonal leg from the mid-right junction down
# to the bottom-right. The leg spans half cap height (350x350, 45deg).
# Reads as a squared R with a diagonal kick.
# ---------------------------------------------------------------------------
_R_LEFT_X = _COL_L
_R_RIGHT_X = _COL_R_NARROW
_R_MID_Y = _MID_Y
_R_LEG_DX = CAP_HEIGHT / 2               # 350
_R_LEG_BOT_X = _R_RIGHT_X + _R_LEG_DX     # 825 -- centerline of leg's bottom terminal
_R_RIGHT_EDGE = _R_LEG_BOT_X + HALF       # 880
_R_BBOX = _bbox(_LEFT_EDGE, _R_RIGHT_EDGE)
_R_LEFT_RIGHT_EDGE = _R_LEFT_X + HALF     # 200 -- right edge of vertical rail
R = {
    "name": "R",
    "unicode": "U+0052",
    "advance": _advance(_R_BBOX),
    "primitives": [
        {"type": "vline", "x": _R_LEFT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "hline", "y": CAP_HEIGHT, "x0": _R_LEFT_X, "x1": _R_RIGHT_X},
        {"type": "hline", "y": _R_MID_Y, "x0": _R_LEFT_X, "x1": _R_RIGHT_X},
        {"type": "vline", "x": _R_RIGHT_X, "y0": _R_MID_Y, "y1": CAP_HEIGHT},
        # Diagonal leg from (right rail x, mid y) down-right to baseline.
        # Both terminals 110 wide; top terminal overlaps right rail.
        {"type": "diag",
         "top_y": _R_MID_Y,
         "top_x0": _R_RIGHT_X - HALF - _DIAG_OVERLAP,
         "top_x1": _R_RIGHT_X + HALF + _DIAG_OVERLAP,
         "bot_y": BASELINE,
         "bot_x0": _R_LEG_BOT_X - HALF - _DIAG_OVERLAP,
         "bot_x1": _R_LEG_BOT_X + HALF + _DIAG_OVERLAP},
    ],
}


# ---------------------------------------------------------------------------
# S: hero glyph. The hardest letter in a pure rail+diagonal vocabulary.
# A true S-curve requires either curves or non-45 diagonals, both
# forbidden by SPEC. The v0.1 construction is a "thunderbird S": the
# top arm is the right half of a horizontal rail (so it reads as
# extending RIGHT from the spine); the bottom arm is the left half of a
# horizontal rail (extending LEFT); a single 45-degree diagonal spine
# connects the right end of the top arm to the left end of the bottom
# arm via two short verticals that drop/rise to the diagonal terminals.
#
# Reading the outline: top horizontal from center to right, drop down
# the right vertical to the diagonal's top, diagonal down-left to the
# bottom-left vertical's top, descend that vertical to the baseline,
# bottom horizontal from left to center. The result reads as a squared
# S -- not a Z -- because the top arm extends right-of-center and the
# bottom arm extends left-of-center, breaking the Z's symmetry.
#
# This is a documented v0.1 trade-off. SPEC section 7 explicitly permits
# omitting or approximating S; we chose to approximate.
# ---------------------------------------------------------------------------
_S_LEFT_X = _COL_L                          # 145
_S_RIGHT_X = _COL_R_NARROW                  # 475
_S_MID_X = (_S_LEFT_X + _S_RIGHT_X) / 2     # 310 -- centerline
_S_MID_Y = _MID_Y                           # 350
# Diagonal spans the full column width (dx=330) so dy=330. The verticals
# absorb the remaining 370 units of cap height, split as 185 each.
_S_DIAG_DX = _S_RIGHT_X - _S_LEFT_X         # 330
_S_DIAG_DY = _S_DIAG_DX                     # 330
_S_DIAG_TOP_Y = _S_MID_Y + _S_DIAG_DY / 2   # 515
_S_DIAG_BOT_Y = _S_MID_Y - _S_DIAG_DY / 2   # 185
_S_RIGHT_EDGE = _RIGHT_EDGE_NARROW          # 530
_S_BBOX = _bbox(_LEFT_EDGE, _S_RIGHT_EDGE)
S = {
    "name": "S",
    "unicode": "U+0053",
    "advance": _advance(_S_BBOX),
    "primitives": [
        # Top horizontal: right half only (center to right column)
        {"type": "hline", "y": CAP_HEIGHT, "x0": _S_MID_X, "x1": _S_RIGHT_X},
        # Bottom horizontal: left half only (left column to center)
        {"type": "hline", "y": BASELINE, "x0": _S_LEFT_X, "x1": _S_MID_X},
        # Top-right vertical: cap down to top of diagonal
        {"type": "vline", "x": _S_RIGHT_X, "y0": _S_DIAG_TOP_Y, "y1": CAP_HEIGHT},
        # Bottom-left vertical: bot of diagonal down to baseline
        {"type": "vline", "x": _S_LEFT_X, "y0": BASELINE, "y1": _S_DIAG_BOT_Y},
        # Diagonal spine: top-right (515) -> bot-left (185). dx=330, dy=330.
        {"type": "diag",
         "top_y": _S_DIAG_TOP_Y,
         "top_x0": _S_RIGHT_X - HALF - _DIAG_OVERLAP,
         "top_x1": _S_RIGHT_X + HALF + _DIAG_OVERLAP,
         "bot_y": _S_DIAG_BOT_Y,
         "bot_x0": _S_LEFT_X - HALF - _DIAG_OVERLAP,
         "bot_x1": _S_LEFT_X + HALF + _DIAG_OVERLAP},
    ],
}


# ---------------------------------------------------------------------------
# T: top horizontal rail (full width) + centered vertical rail. The
# vertical sits at the horizontal's midpoint.
# ---------------------------------------------------------------------------
_T_LEFT_X = _COL_L
_T_RIGHT_X = _COL_R_NARROW
_T_CENTER_X = (_T_LEFT_X + _T_RIGHT_X) / 2  # 310
_T_BBOX = _bbox(_LEFT_EDGE, _RIGHT_EDGE_NARROW)
T = {
    "name": "T",
    "unicode": "U+0054",
    "advance": _advance(_T_BBOX),
    "primitives": [
        {"type": "hline", "y": CAP_HEIGHT, "x0": _T_LEFT_X, "x1": _T_RIGHT_X},
        {"type": "vline", "x": _T_CENTER_X, "y0": BASELINE, "y1": CAP_HEIGHT},
    ],
}


# ---------------------------------------------------------------------------
# U: two vertical rails + bottom horizontal. Square frame minus the top.
# ---------------------------------------------------------------------------
_U_LEFT_X = _COL_L
_U_RIGHT_X = _COL_R_NARROW
_U_BBOX = _bbox(_LEFT_EDGE, _RIGHT_EDGE_NARROW)
U = {
    "name": "U",
    "unicode": "U+0055",
    "advance": _advance(_U_BBOX),
    "primitives": [
        {"type": "vline", "x": _U_LEFT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "vline", "x": _U_RIGHT_X, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "hline", "y": BASELINE, "x0": _U_LEFT_X, "x1": _U_RIGHT_X},
    ],
}


# ---------------------------------------------------------------------------
# V: two 45-degree diagonals meeting at bottom-center (apex at baseline).
# Each leg spans full cap height (dy=700), so dx=700 per leg. Total
# width 1510 -- geometrically forced, same constraint as A. Reads as a
# wide, sharp V. Hero glyph family member.
# ---------------------------------------------------------------------------
_V_APEX_X = _COL_L + CAP_HEIGHT / 2         # 495 -- apex centerline
_V_LEG_DX = CAP_HEIGHT                       # 700
_V_LEFT_EDGE = _V_APEX_X - _V_LEG_DX - HALF  # -260
_V_RIGHT_EDGE = _V_APEX_X + _V_LEG_DX + HALF  # 1250
V = {
    "name": "V",
    "unicode": "U+0056",
    "advance": _advance(_bbox(_V_LEFT_EDGE, _V_RIGHT_EDGE)),
    "primitives": [
        # Left leg: top edge at cap height (left side), bottom at apex
        {"type": "diag",
         "top_y": CAP_HEIGHT,
         "top_x0": _V_APEX_X - _V_LEG_DX - HALF - _DIAG_OVERLAP,
         "top_x1": _V_APEX_X - _V_LEG_DX + HALF + _DIAG_OVERLAP,
         "bot_y": BASELINE,
         "bot_x0": _V_APEX_X - HALF - _DIAG_OVERLAP,
         "bot_x1": _V_APEX_X + HALF + _DIAG_OVERLAP},
        # Right leg: top edge at cap height (right side), bottom at apex
        {"type": "diag",
         "top_y": CAP_HEIGHT,
         "top_x0": _V_APEX_X + _V_LEG_DX - HALF - _DIAG_OVERLAP,
         "top_x1": _V_APEX_X + _V_LEG_DX + HALF + _DIAG_OVERLAP,
         "bot_y": BASELINE,
         "bot_x0": _V_APEX_X - HALF - _DIAG_OVERLAP,
         "bot_x1": _V_APEX_X + HALF + _DIAG_OVERLAP},
    ],
}


# ---------------------------------------------------------------------------
# W: hero glyph. Four 45-degree diagonals forming two V-shapes side by
# side. The two outer legs descend full cap height (dy=700, dx=700) to
# the two bottom apexes. The two inner legs RISE from those apexes to a
# shared center peak -- but to stay at 45 degrees, the inner peak must
# sit at mid-height (y=350), not cap height. (A W whose inner notch
# reaches all the way down to baseline with a cap-height center peak is
# impossible in a pure 45-degree vocabulary: it would require dx=350
# with dy=700.) The result reads as a W with a shallower inner V than a
# humanist W; this is a documented v0.1 trade-off.
# ---------------------------------------------------------------------------
_W_APEX1_X = _COL_L + CAP_HEIGHT / 2          # 495 -- left V apex (baseline)
_W_APEX2_X = _W_APEX1_X + CAP_HEIGHT          # 1195 -- right V apex (baseline)
_W_LEG_DX = CAP_HEIGHT                         # 700 -- outer leg horizontal throw
_W_INNER_DX = CAP_HEIGHT / 2                   # 350 -- inner leg horizontal throw
_W_CENTER_TOP_X = (_W_APEX1_X + _W_APEX2_X) / 2  # 845 -- shared inner peak (mid-height)
_W_INNER_TOP_Y = _MID_Y                        # 350 -- inner peak y (45deg constraint)
_W_LEFT_EDGE = _W_APEX1_X - _W_LEG_DX - HALF - _DIAG_OVERLAP  # -261
_W_RIGHT_EDGE = _W_APEX2_X + _W_LEG_DX + HALF + _DIAG_OVERLAP  # 1951
W = {
    "name": "W",
    "unicode": "U+0057",
    "advance": _advance(_bbox(_W_LEFT_EDGE, _W_RIGHT_EDGE)),
    "primitives": [
        # Left-V outer leg: top-left (cap) -> apex1 (baseline). dx=700, dy=700.
        {"type": "diag",
         "top_y": CAP_HEIGHT,
         "top_x0": _W_APEX1_X - _W_LEG_DX - HALF - _DIAG_OVERLAP,
         "top_x1": _W_APEX1_X - _W_LEG_DX + HALF + _DIAG_OVERLAP,
         "bot_y": BASELINE,
         "bot_x0": _W_APEX1_X - HALF - _DIAG_OVERLAP,
         "bot_x1": _W_APEX1_X + HALF + _DIAG_OVERLAP},
        # Inner leg apex1 (baseline) -> center peak (mid). dx=350, dy=350.
        {"type": "diag",
         "top_y": _W_INNER_TOP_Y,
         "top_x0": _W_CENTER_TOP_X - HALF - _DIAG_OVERLAP,
         "top_x1": _W_CENTER_TOP_X + HALF + _DIAG_OVERLAP,
         "bot_y": BASELINE,
         "bot_x0": _W_APEX1_X - HALF - _DIAG_OVERLAP,
         "bot_x1": _W_APEX1_X + HALF + _DIAG_OVERLAP},
        # Inner leg center peak (mid) -> apex2 (baseline). dx=350, dy=350.
        {"type": "diag",
         "top_y": _W_INNER_TOP_Y,
         "top_x0": _W_CENTER_TOP_X - HALF - _DIAG_OVERLAP,
         "top_x1": _W_CENTER_TOP_X + HALF + _DIAG_OVERLAP,
         "bot_y": BASELINE,
         "bot_x0": _W_APEX2_X - HALF - _DIAG_OVERLAP,
         "bot_x1": _W_APEX2_X + HALF + _DIAG_OVERLAP},
        # Right-V outer leg: apex2 (baseline) -> top-right (cap). dx=700, dy=700.
        {"type": "diag",
         "top_y": CAP_HEIGHT,
         "top_x0": _W_APEX2_X + _W_LEG_DX - HALF - _DIAG_OVERLAP,
         "top_x1": _W_APEX2_X + _W_LEG_DX + HALF + _DIAG_OVERLAP,
         "bot_y": BASELINE,
         "bot_x0": _W_APEX2_X - HALF - _DIAG_OVERLAP,
         "bot_x1": _W_APEX2_X + HALF + _DIAG_OVERLAP},
    ],
}


# ---------------------------------------------------------------------------
# X: two 45-degree diagonals crossing in the middle. Each spans full cap
# height (dy=700), so dx=700 per leg. Bbox = 1510 (same as V and A).
# Reads as a crisp X. Hero glyph family member by association.
# ---------------------------------------------------------------------------
_X_LEFT_EDGE = _LEFT_EDGE                    # 90
_X_RIGHT_EDGE = _COL_L + CAP_HEIGHT + HALF   # 900 -- symmetric to N width
_X_LEFT_CENTER_X = _COL_L                    # 145
_X_RIGHT_CENTER_X = _COL_R_WIDE              # 845
X = {
    "name": "X",
    "unicode": "U+0058",
    "advance": _advance(_bbox(_X_LEFT_EDGE, _X_RIGHT_EDGE)),
    "primitives": [
        # Backslash: top-left -> bottom-right
        {"type": "diag",
         "top_y": CAP_HEIGHT,
         "top_x0": _X_LEFT_CENTER_X - HALF - _DIAG_OVERLAP,
         "top_x1": _X_LEFT_CENTER_X + HALF + _DIAG_OVERLAP,
         "bot_y": BASELINE,
         "bot_x0": _X_RIGHT_CENTER_X - HALF - _DIAG_OVERLAP,
         "bot_x1": _X_RIGHT_CENTER_X + HALF + _DIAG_OVERLAP},
        # Forward slash: top-right -> bottom-left
        {"type": "diag",
         "top_y": CAP_HEIGHT,
         "top_x0": _X_RIGHT_CENTER_X - HALF - _DIAG_OVERLAP,
         "top_x1": _X_RIGHT_CENTER_X + HALF + _DIAG_OVERLAP,
         "bot_y": BASELINE,
         "bot_x0": _X_LEFT_CENTER_X - HALF - _DIAG_OVERLAP,
         "bot_x1": _X_LEFT_CENTER_X + HALF + _DIAG_OVERLAP},
    ],
}


# ---------------------------------------------------------------------------
# Y: lower half is a vertical rail; upper half is two 45-degree diagonals
# meeting at the top of the rail (at mid-height). Each diagonal spans
# half cap height (dy=350, dx=350). The two diagonals form an inverted-V
# whose apex sits on top of the vertical stem.
# ---------------------------------------------------------------------------
_Y_STEM_X = _COL_L + (CAP_HEIGHT / 4)         # 320 -- shift right to fit diagonals
_Y_MID_Y = _MID_Y                              # 350
_Y_DIAG_DX = CAP_HEIGHT / 2                    # 350
_Y_LEFT_TOP_X = _Y_STEM_X - _Y_DIAG_DX         # -30 -- outside bearing
_Y_RIGHT_TOP_X = _Y_STEM_X + _Y_DIAG_DX        # 670
_Y_LEFT_EDGE = _Y_LEFT_TOP_X - HALF            # -85
_Y_RIGHT_EDGE = _Y_RIGHT_TOP_X + HALF          # 725
# Shift the whole glyph right so the leftmost edge sits at SIDE_BEARING.
_Y_SHIFT = SIDE_BEARING - _Y_LEFT_EDGE         # 175
_Y_STEM_X_SHIFTED = _Y_STEM_X + _Y_SHIFT       # 495
_Y_LEFT_TOP_X_SHIFTED = _Y_LEFT_TOP_X + _Y_SHIFT  # 145
_Y_RIGHT_TOP_X_SHIFTED = _Y_RIGHT_TOP_X + _Y_SHIFT  # 845
_Y_LEFT_EDGE_SHIFTED = SIDE_BEARING            # 90
_Y_RIGHT_EDGE_SHIFTED = _Y_RIGHT_TOP_X_SHIFTED + HALF  # 900
_Y_BBOX = _bbox(_Y_LEFT_EDGE_SHIFTED, _Y_RIGHT_EDGE_SHIFTED)
Y = {
    "name": "Y",
    "unicode": "U+0059",
    "advance": _advance(_Y_BBOX),
    "primitives": [
        # Stem: vertical rail from baseline to mid
        {"type": "vline", "x": _Y_STEM_X_SHIFTED, "y0": BASELINE, "y1": _Y_MID_Y},
        # Left diagonal: top-left (cap) -> stem top (mid)
        {"type": "diag",
         "top_y": CAP_HEIGHT,
         "top_x0": _Y_LEFT_TOP_X_SHIFTED - HALF - _DIAG_OVERLAP,
         "top_x1": _Y_LEFT_TOP_X_SHIFTED + HALF + _DIAG_OVERLAP,
         "bot_y": _Y_MID_Y,
         "bot_x0": _Y_STEM_X_SHIFTED - HALF - _DIAG_OVERLAP,
         "bot_x1": _Y_STEM_X_SHIFTED + HALF + _DIAG_OVERLAP},
        # Right diagonal: top-right (cap) -> stem top (mid)
        {"type": "diag",
         "top_y": CAP_HEIGHT,
         "top_x0": _Y_RIGHT_TOP_X_SHIFTED - HALF - _DIAG_OVERLAP,
         "top_x1": _Y_RIGHT_TOP_X_SHIFTED + HALF + _DIAG_OVERLAP,
         "bot_y": _Y_MID_Y,
         "bot_x0": _Y_STEM_X_SHIFTED - HALF - _DIAG_OVERLAP,
         "bot_x1": _Y_STEM_X_SHIFTED + HALF + _DIAG_OVERLAP},
    ],
}


# ---------------------------------------------------------------------------
# Z: two horizontal rails (top, bottom) + one 45-degree diagonal
# connecting top-right to bottom-left. The diagonal spans full cap height
# (dy=700, dx=700), matching the N diagonal throw.
# ---------------------------------------------------------------------------
_Z_LEFT_X = _COL_L
_Z_RIGHT_X = _COL_R_WIDE                     # 845 -- match N width so diag is 45deg
_Z_BBOX = _bbox(_LEFT_EDGE, _RIGHT_EDGE_WIDE)
Z = {
    "name": "Z",
    "unicode": "U+005A",
    "advance": _advance(_Z_BBOX),
    "primitives": [
        {"type": "hline", "y": CAP_HEIGHT, "x0": _Z_LEFT_X, "x1": _Z_RIGHT_X},
        {"type": "hline", "y": BASELINE, "x0": _Z_LEFT_X, "x1": _Z_RIGHT_X},
        # Diagonal from top-right (x=845, y=700) down to bottom-left (x=145, y=0)
        {"type": "diag",
         "top_y": CAP_HEIGHT,
         "top_x0": _Z_RIGHT_X - HALF - _DIAG_OVERLAP,
         "top_x1": _Z_RIGHT_X + HALF + _DIAG_OVERLAP,
         "bot_y": BASELINE,
         "bot_x0": _Z_LEFT_X - HALF - _DIAG_OVERLAP,
         "bot_x1": _Z_LEFT_X + HALF + _DIAG_OVERLAP},
    ],
}


# Order matters: this is the order glyphs are emitted into the UFO and
# listed in public.glyphOrder. .notdef and space are prepended by the
# font builder; only the real letters go here. Alphabetical order makes
# the specimen page easy to scan.
GLYPHS = [A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z]
