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
    """45-degree parallelogram with horizontal terminal edges.

    The two terminals are horizontal edges (aligned with cap height /
    baseline) of equal length, connected by two 45-degree sides. This
    makes the diagonal join cleanly with vertical rails (no overshoot
    above cap height or below baseline).

    Required fields:
      top_y, top_x0, top_x1  -- the upper horizontal edge
      bot_y, bot_x0, bot_x1  -- the lower horizontal edge

    The generator validates that the four corners form a valid
    45-degree parallelogram with parallel horizontal terminals of
    equal length.
    """
    top_y = spec["top_y"]
    top_x0 = spec["top_x0"]
    top_x1 = spec["top_x1"]
    bot_y = spec["bot_y"]
    bot_x0 = spec["bot_x0"]
    bot_x1 = spec["bot_x1"]

    if top_y == bot_y:
        raise ValueError(f"diag degenerate: top_y == bot_y == {top_y}")

    top_len = top_x1 - top_x0
    bot_len = bot_x1 - bot_x0
    if top_len != bot_len:
        raise ValueError(
            f"diag terminals must be parallel and equal length; "
            f"top={top_len}, bot={bot_len}"
        )

    dy = abs(top_y - bot_y)
    left_dx = abs(top_x0 - bot_x0)
    right_dx = abs(top_x1 - bot_x1)
    if left_dx != dy:
        raise ValueError(
            f"diag left side must be 45 degrees; "
            f"|dx|={left_dx}, |dy|={dy}"
        )
    if right_dx != dy:
        raise ValueError(
            f"diag right side must be 45 degrees; "
            f"|dx|={right_dx}, |dy|={dy}"
        )

    # Return corners clockwise. The winding doesn't actually matter
    # because booleanOperations' union normalizes, but a consistent
    # order helps debugging.
    return [
        (top_x0, top_y),
        (top_x1, top_y),
        (bot_x1, bot_y),
        (bot_x0, bot_y),
    ]


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
