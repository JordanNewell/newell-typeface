"""Glyph generation: union primitives and draw into a UFO glyph.

booleanOperations.BooleanOperationManager.union(contours, outPen) expects
each input contour to be an object with a drawPoints(pointPen) method
(the UFO point-pen protocol), and writes the result to outPen via the
same protocol. We wrap each expanded polygon in a tiny _PolygonContour
shim that satisfies that interface, then collect the output into a list
of flat contours that we replay onto the ufoLib2 glyph pen.
"""

from booleanOperations import BooleanOperationManager

from newell.primitives import expand_primitive


class _Point:
    """Minimal point record compatible with the pointPen protocol."""

    __slots__ = ("coordinates", "segmentType")

    def __init__(self, coordinates, segmentType=None):
        self.coordinates = coordinates
        self.segmentType = segmentType


class _PolygonContour:
    """Wraps a flat (x, y) polygon so booleanOperations can read it.

    Implements drawPoints(pointPen) by emitting a single closed contour
    of on-curve line points.
    """

    def __init__(self, points):
        self._points = list(points)

    def __len__(self):
        return len(self._points)

    def __bool__(self):
        return bool(self._points)

    def drawPoints(self, pointPen):
        if len(self._points) < 3:
            return
        pointPen.beginPath()
        first = self._points[0]
        pointPen.addPoint(first, segmentType="line")
        for p in self._points[1:]:
            pointPen.addPoint(p, segmentType="line")
        pointPen.addPoint(first, segmentType="line")
        pointPen.endPath()


class _ContourCollector:
    """Point-pen sink that records union() output as flat contour lists.

    Each contour comes in as beginPath / addPoint(...)/... / endPath.
    We record only on-curve points (segmentType is not None), preserving
    the order booleanOperations emits.
    """

    def __init__(self):
        self.contours = []
        self._current = None

    def beginPath(self, **kwargs):
        self._current = []

    def endPath(self):
        if self._current is None:
            return
        # Drop trailing duplicate of the first point if present (closing
        # point emitted by some pens). Keep at least 3 points.
        pts = list(self._current)
        if len(pts) >= 2 and pts[0] == pts[-1]:
            pts = pts[:-1]
        if len(pts) >= 3:
            self.contours.append(pts)
        self._current = None

    def addPoint(self, coordinates, segmentType=None, smooth=False, **kwargs):
        if self._current is None:
            self._current = []
        if segmentType is not None:
            # On-curve point; record (x, y) as ints when possible to keep
            # UFO output clean and deterministic.
            x, y = coordinates
            if isinstance(x, float) and x.is_integer():
                x = int(x)
            if isinstance(y, float) and y.is_integer():
                y = int(y)
            self._current.append((x, y))

    def addComponent(self, *args, **kwargs):
        # Primitives never introduce components.
        raise NotImplementedError("components not supported in Newell generator")


def union_primitives(primitive_specs):
    """Union a list of primitive specs into a list of flat contours.

    Each input is a dict matching one of the vline/hline/diag shapes.
    Returns a list of contours; each contour is a list of (x, y) tuples.
    """
    polygons = [_PolygonContour(expand_primitive(s)) for s in primitive_specs]
    collector = _ContourCollector()
    BooleanOperationManager.union(polygons, collector)
    # Sort for determinism: by first-point coords so two runs produce
    # byte-identical output. Within a contour we preserve the winding
    # booleanOperations chose (it has its own correctness constraints).
    collector.contours.sort(
        key=lambda c: (min(p[1] for p in c), min(p[0] for p in c), len(c))
    )
    return collector.contours


def draw_contours_into_glyph(glyph, contours):
    """Replay flat contours onto a ufoLib2 glyph via its point pen.

    The glyph's pen is the standard UFO point pen. We emit each contour
    as a closed polyline of on-curve line points.
    """
    pen = glyph.getPointPen()
    for contour in contours:
        if len(contour) < 3:
            continue
        pen.beginPath()
        for (x, y) in contour:
            pen.addPoint((x, y), segmentType="line")
        pen.endPath()


def build_glyph(font, glyph_def):
    """Create a glyph in `font` from a declarative definition dict.

    The glyph is added with the given name, unicode, advance width, and
    primitives. Returns the new glyph object.
    """
    name = glyph_def["name"]
    advance = glyph_def["advance"]
    primitives = glyph_def.get("primitives", [])

    glyph = font.newGlyph(name)
    glyph.width = advance
    if "unicode" in glyph_def and glyph_def["unicode"] is not None:
        glyph.unicode = _parse_unicode(glyph_def["unicode"])

    contours = union_primitives(primitives) if primitives else []
    draw_contours_into_glyph(glyph, contours)
    return glyph


def _parse_unicode(value):
    """Accept 'U+004E' strings or ints; return a codepoint int."""
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        s = value.strip()
        if s.startswith("U+") or s.startswith("u+"):
            return int(s[2:], 16)
        if s.startswith("0x") or s.startswith("0X"):
            return int(s[2:], 16)
        # Plain decimal or single char.
        if len(s) == 1:
            return ord(s)
        return int(s, 16)
    raise ValueError(f"cannot parse unicode value: {value!r}")
