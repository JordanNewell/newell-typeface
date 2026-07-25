# Newell Roadmap

Forward-looking. Not commitments — priorities shift based on what
the typeface needs and how it gets used in the wild.

## v0.2 — "Reads like a typeface"

**Theme:** fix the v0.1 limitations that prevent Newell from being
used for real text. The goal is a typeface that can be set in a
paragraph and still read as English.

### Ship-blockers for v0.2

These must land before v0.2 ships:

1. **A legible S.** Add a third primitive — most likely a controlled
   "step-diagonal" or a single-bend curve segment — specifically
   scoped to S/s/2/3/5/8/$. Spec amendment required.

2. **Lowercase Latin (a-z).** Cannot ship a "real" typeface without
   it. Inherits the rail+diagonal DNA. New metrics: x-height = 500
   (already reserved in SPEC.md). Watch for: a (must distinguish from
   o in v0.1's rectilinear vocabulary), e, g (especially hard — needs
   the same step-diagonal as S), s (same legibility issue as S).

3. **Class-based kerning.** Default side bearings leave ugly gaps in
   problem pairs (AV, AT, PA, YA, etc.). Implement as a UFO kerning
   table with class-based rules.

4. **0 / O disambiguation.** Either a slash through zero (programming
   font convention) or a different bbox. Pick one and document.

### Stretch goals for v0.2

- Curly quote open/closed distinction.
- Basic Latin diacritics (A-Z + a-z with grave, acute, circumflex,
  tilde, umlaut) — adds ~80 glyphs.

---

## v0.3 — "A type system"

**Theme:** Newell becomes more than one weight and more than one
shape. Starts to feel like a *type family* rather than a single font.

- **Variable font axes.** Ship a single `.otf` with weight (Light 70 →
  Regular 110 → Bold 170 → Black 220) interpolated parametrically.
  Since the generator already takes stroke width as a constant, this
  should be a small change.
- **Custom axis: `NDI` (Newell Diagonal Intensity).** Controls how
  visible the decorative 45° diagonals are. At NDI=0, the typeface is
  pure rails (very plain). At NDI=100, extra decorative diagonals
  appear (very expressive). This is the *signature* axis — no other
  typeface has it.
- **Italic.** Probably a true oblique (slant the rails) rather than a
  designed italic. Debate.
- **Extended Latin diacritics complete.** Vietnamese, Pinyin, etc.

---

## v0.4 — "A brand system"

**Theme:** Newell extends past typography into a broader visual
language. Inspired by the concept art that started the project.

- **Icon system.** Analytics, speed, connect, cloud, search, etc. —
  all built from the same rail+diagonal DNA. Match the icon grid from
  the original concept art.
- **Logo lockup variants.** Horizontal, stacked, monogram, favicon,
  app icon. Defined as SVG components.
- **Motion language.** Rail appearance, diagonal slide, glyph lock —
  the animation principles for assembly.
- **Codified in Figma.** Every glyph becomes a reusable component
  built from rail/diagonal/junction primitives. New characters are
  Lego, not calligraphy.

---

## v1.0 — "Production"

**Theme:** ready for professional typography use without apology.

- Full character set: extended Latin, Cyrillic, Greek.
- Hinting for small sizes (15px and below).
- OpenType features: smart ligatures, contextual alternates,
  small caps, tabular figures.
- Manually tuned per-glyph optical corrections.
- Comprehensive specimen book.

---

## What won't happen

- **No rounded terminals.** Ever. That's a different typeface.
- **No non-45° diagonals.** Same.
- **No curved letters (in the v0.1 DNA sense).** Letters that
  traditionally curve (C, O, S) will always be approximations of some
  kind, even after v0.2 adds a step-diagonal primitive. The
  approximation may get better but it stays geometric.
- **No backwards-compatibility for binary font files.** Each major
  version is allowed to break the OTF/TTF/WOFF2 byte format. Source
  UFO is the long-term-stable format.

---

## How to contribute

The typeface is generated from rules in `SPEC.md`. To propose a
change:

1. Amend `SPEC.md` with rationale.
2. Update the generator if needed.
3. Rebuild with `py scripts/build_all.py`.
4. Iterate on glyph definitions in `src/newell/glyphs.py` until the
   visual result matches the spec.
5. Bump version in `font.py` metadata.
6. Tag a new release.

The font is original work. Do not import outlines or metrics from
other typefaces — see `SOURCES.txt`.
