"""Newell parametric glyph generator.

Builds a UFO font from declarative rail/diagonal primitives. See SPEC.md
for the typeface constitution. Stroke width is fixed at 110 units and
diagonals must be exactly 45 degrees.
"""

from newell.primitives import (
    STROKE_WIDTH,
    expand_primitive,
    expand_vline,
    expand_hline,
    expand_diag,
)

__version__ = "0.1.0"

__all__ = [
    "STROKE_WIDTH",
    "expand_primitive",
    "expand_vline",
    "expand_hline",
    "expand_diag",
]
