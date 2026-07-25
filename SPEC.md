# Newell — Typeface Specification

> The constitution. Every glyph, every kerning pair, every future
> weight answers to this document.

## 1. Design intent

Newell is a geometric display typeface whose vocabulary is **three
primitives**:

1. **Rail** — a vertical or horizontal bar of constant width.
2. **Diagonal** — a 45° stroke of the same width.
3. **Junction** — the squared union of two primitives that meet.

No curves. No rounding. Every terminal is squared. Every corner is 90°
or 45°. The result reads as "engineered" rather than "drawn" — closer
to a barcode or a circuit diagram than to a humanist serif.

The signature gesture, inherited from the wordmark, is the **N
diagonal**: a 45° stroke that descends from the top of one vertical
rail to the bottom of another. That gesture recurs in M, K, R, V, W,
X, Y, Z and the digits 1, 2, 4, 7. It is the family resemblance.

## 2. Grid and metrics

All measurements in font units. Units-per-em **1000** (industry
standard, gives clean hinting).

| Metric            | Value | Notes                                   |
|-------------------|-------|-----------------------------------------|
| Units per em      | 1000  |                                         |
| Ascender          | 800   | Overshoots cap height for accents       |
| Cap height        | 700   | Top of A, B, C, …                       |
| x-height          | 500   | Top of a, c, e, m, … (Phase 2)          |
| Baseline          | 0     |                                         |
| Descender         | -200  | Bottom of g, j, p, q, y (Phase 2)       |

## 3. Strokes

**Monoline.** Every primitive has the same thickness.

| Parameter           | Value | Fraction of cap height |
|---------------------|-------|------------------------|
| Stroke width        | 110   | ~15.7%                 |
| Rail-to-rail gap    | 130   | Min spacing between parallel rails |
| Side bearing (L/R)  | 90    | Default left/right padding per glyph  |

Stroke ends are **squared**. No butt caps, no rounded caps, no
extended caps. The terminal is a 90° edge.

## 4. Angles

Diagonals are **exactly 45°**. The generator MUST assert
`abs(dx) == abs(dy)` for every diagonal primitive and refuse to emit a
non-conforming glyph. There are no 30° strokes, no 60° strokes, no
curved strokes. If a glyph cannot be expressed in rails + 45°
diagonals, it does not belong in Newell.

## 5. Primitive grammar

A glyph is a list of primitives. Each primitive is a thickened
rectangle (for rails) or parallelogram (for diagonals) of width `110`.
Primitives are unioned with `booleanOperations.union()` to produce the
final closed contour(s).

### 5.1 Vertical rail

```json
{"type": "vline", "x": 245, "y0": 0, "y1": 700}
```

A bar centered horizontally on `x`, extending from `y0` to `y1`.

### 5.2 Horizontal rail

```json
{"type": "hline", "y": 350, "x0": 100, "x1": 500}
```

A bar centered vertically on `y`, extending from `x0` to `x1`.

### 5.3 Diagonal

```json
{"type": "diag", "x0": 100, "y0": 700, "x1": 500, "y1": 0,
 "start": "top-left", "end": "top-right"}
```

A 45° stroke of width 110, from `(x0, y0)` to `(x1, y1)`. The
generator asserts `|x1 - x0| == |y1 - y0|`.

### 5.4 Junction

When two primitives overlap, their union forms a squared junction.
This is implicit — no separate primitive is needed. The generator's
job is to produce a clean single-contour (or correct multi-contour)
result after unioning.

## 6. Spacing

Default left and right side bearings are **90 units**. Glyphs may
override per-glyph. The advance width of a default letter is:

```
advance = left_bearing + glyph_width + right_bearing
advance = 90 + glyph_width + 90
```

For a glyph 420 units wide (typical uppercase), advance = 600.

## 7. The hero alphabet — A E M N R S W

These seven glyphs establish the typeface personality. They are
hand-tuned in the JSON source. Every other glyph inherits their
proportions and stroke treatment.

- **A** — Two diagonals meeting at apex; one horizontal rail (the bar)
  at y=200.
- **E** — One vertical rail (left); three horizontal rails (top, middle,
  bottom).
- **M** — Two outer vertical rails; two diagonals meeting at center
  (inverted-V).
- **N** — The signature. Two vertical rails; one diagonal from
  top-of-left to bottom-of-right.
- **R** — One vertical rail; one diagonal (leg); bowl approximated by
  two short horizontal rails + one short vertical rail.
- **S** — Two horizontal rails (top, bottom); two short vertical rails
  (left-of-top, right-of-bottom); one diagonal connecting them. No
  curves.
- **W** — Four diagonals, no vertical rails.

If a glyph cannot be expressed in this vocabulary while remaining
legible, it is acceptable for the v0.1 release to **omit** the glyph
rather than fake a curve. The font will report `.notdef` for missing
glyphs; the specimen page will mark them TBD.

## 8. Kerning

Phase 1 (v0.1): no kerning. Default side bearings only.
Phase 2 (v0.2): class-based kerning for problem pairs (AV, AT, PA,
YA, etc.).

## 9. Weights

v0.1 ships **Regular** only (stroke width 110).

Planned for v0.2 as a variable font:

| Weight   | Stroke | Use case              |
|----------|--------|-----------------------|
| Light    | 70     | Display, large sizes  |
| Regular  | 110    | Body, default         |
| Bold     | 170    | Emphasis              |
| Black    | 220    | Hero, signage         |

A custom `NDI` (Newell Diagonal Intensity) axis may be added in v0.3
to control the visibility of decorative diagonals.

## 10. Character set — v0.1

| Block                   | Glyphs                                         |
|-------------------------|------------------------------------------------|
| Uppercase Latin         | A B C D E F G H I J K L M N O P Q R S T U V W X Y Z |
| Digits                  | 0 1 2 3 4 5 6 7 8 9                            |
| Punctuation             | . , ! ? ' ' " " : ; - — ( ) / @ # $ % & + = < > |
| Space                   | space, nbsp                                    |
| Notdef + zero-width     | .notdef, null                                  |

v0.2 adds: lowercase Latin, extended punctuation, basic Latin
diacritics.

## 11. Naming

- Family: **Newell**
- Subfamily (v0.1): **Regular**
- PostScript name: **Newell-Regular**
- Version: 0.1.0
- Copyright: `Copyright 2026 Jordan Newell`
- License: OFL-1.1

## 12. Forbidden

- Curves of any kind (no Bézier control points).
- Rounded terminals.
- Stroke widths other than the spec value (in v0.1).
- Diagonals at angles other than 45°.
- Borrowing glyph outlines or metrics from any existing typeface.

If a future maintainer wants to break any of these rules, the rule
must first be amended in this document with rationale.
