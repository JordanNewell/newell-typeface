"""Primitive expansion.

Each Newell primitive (vline, hline, diag) becomes a closed polygon of
constant width STROKE_WIDTH. Polygons are returned as a list of (x, y)
tuples in clockwise order starting at the lower-left corner.

All coordinates are in font units. Stroke width is fixed at 110 in v0.1
per SPEC.md section 3.
"""

STROKE_WIDTH = 110
_HALF = STROKE_WIDTH / 2.0


def expand_vline(spec):
    """Rectangle centered horizontally on x, extending y0 -> y1.

    Returns 4 corner points clockwise from lower-left.
    """
    x = spec["x"]
    y0 = spec["y0"]
    y1 = spec["y1"]
    lo, hi = (y0, y1) if y0 <= y1 else (y1, y0)
    left = x - _HALF
    right = x + _HALF
    return [
        (left, lo),
        (right, lo),
        (right, hi),
        (left, hi),
    ]


def expand_hline(spec):
    """Rectangle centered vertically on y, extending x0 -> x1.

    Returns 4 corner points clockwise from lower-left.
    """
    y = spec["y"]
    x0 = spec["x0"]
    x1 = spec["x1"]
    lo, hi = (x0, x1) if x0 <= x1 else (x1, x0)
    bottom = y - _HALF
    top = y + _HALF
    return [
        (lo, bottom),
        (hi, bottom),
        (hi, top),
        (lo, top),
    ]


def expand_diag(spec):
    """45-degree parallelogram of width STROKE_WIDTH.

    The diagonal runs from (x0, y0) to (x1, y1). The parallelogram is
    centered on that line. Raises ValueError if abs(dx) != abs(dy).
    """
    x0 = spec["x0"]
    y0 = spec["y0"]
    x1 = spec["x1"]
    y1 = spec["y1"]
    dx = x1 - x0
    dy = y1 - y0
    if abs(abs(dx) - abs(dy)) > 0:
        raise ValueError(
            "diag primitive must be exactly 45 degrees; "
            f"got dx={dx}, dy={dy} for {spec}"
        )

    # Direction along the stroke (unit vector).
    length = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / length, dy / length
    # Perpendicular (rotated 90 CCW). The sign choice just flips which
    # side the two offset corners land on; the polygon is closed either
    # way and union() does not care about winding.
    px, py = -uy, ux

    # The two endpoints of the centerline are the midpoint of each
    # squared terminal. Offset by +-perp * HALF on each side.
    a = (x0 + px * _HALF, y0 + py * _HALF)
    b = (x0 - px * _HALF, y0 - py * _HALF)
    c = (x1 - px * _HALF, y1 - py * _HALF)
    d = (x1 + px * _HALF, y1 + py * _HALF)
    return [a, b, c, d]


_PRIMITIVE_EXPANDERS = {
    "vline": expand_vline,
    "hline": expand_hline,
    "diag": expand_diag,
}


def expand_primitive(spec):
    """Dispatch on spec['type'] to the matching expander.

    Raises KeyError on unknown type (the spec dict lookup itself fails
    with a clear message before that for genuinely missing 'type').
    """
    try:
        kind = spec["type"]
    except (KeyError, TypeError) as exc:
        raise ValueError(f"primitive spec missing 'type': {spec!r}") from exc
    try:
        expander = _PRIMITIVE_EXPANDERS[kind]
    except KeyError:
        raise ValueError(f"unknown primitive type {kind!r}; spec={spec!r}")
    return expander(spec)
