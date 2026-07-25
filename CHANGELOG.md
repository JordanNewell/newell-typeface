# Changelog

All notable changes to Newell are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Font releases use a `vMAJOR.MINOR.PATCH[-prerelease]` tag scheme.

## [Unreleased]

### Planned for v0.2
- Lowercase Latin alphabet (a-z)
- Class-based kerning for problem pairs (AV, AT, PA, YA, etc.)
- A third primitive type ("step-diagonal" or controlled curve) to
  enable legible S/s/2/3/5/8/$.
- Variable font axes (Light / Regular / Bold / Black weights).

## [v0.1.0-alpha] — 2026-07-25

First public release. Functional but unpolished — each glyph follows
the rules, but the rules themselves will tighten in subsequent
releases. Treat as a tech preview.

### Added
- Parametric glyph generator (Python) that compiles declarative JSON
  definitions to UFO via fontTools + booleanOperations.
- 26 uppercase Latin letters (A-Z).
- 10 Western Arabic numerals (0-9).
- 23 punctuation marks (. , ! ? ' " : ; - — ( ) / @ # $ % & + = < >).
- .notdef glyph (hollow box) and space.
- One weight (Regular). One style (Upright). Static (non-variable).
- Build pipeline: UFO -> OTF + TTF + WOFF2 in one command.
- Specimen page (single-file HTML, deployable to GitHub Pages).
- Brand DNA specification (SPEC.md).

### DNA
- 1000-unit em.
- Cap height 700, baseline 0, ascender 800, descender -200, x-height 500 (reserved).
- Monoline stroke 110 units, squared terminals.
- Only 45-degree diagonals (generator asserts).
- Three primitives: vertical rail, horizontal rail, diagonal.

### Known limitations
- **S reads as Z.** Pure rails + 45-degree vocabulary cannot render an
  unambiguous S.
- **C, D, G, O, P, Q, R, B** are rectilinear approximations of curved
  letters (squared frames, not curved bowls).
- **A, V, W** are wider than the alphabet average (each leg is a full
  cap-height 45-degree diagonal).
- **M, W** inner notches reach only mid-height (y=350), not baseline.
- **0 visually identical to O and D** — relies on context to disambiguate.
- **$, @** are best-effort approximations.
- **Curly quotes** (' " ") lose open/closed distinction.
- No kerning. Default side bearings only.
- No lowercase. No extended Latin diacritics.

### File sizes
- `Newell-Regular.otf` — 3,312 bytes
- `Newell-Regular.ttf` — 4,568 bytes
- `Newell-Regular.woff2` — 1,776 bytes

### License
SIL Open Font License 1.1. Free for commercial use, modification,
and redistribution. Copyright 2026 Jordan Newell.
