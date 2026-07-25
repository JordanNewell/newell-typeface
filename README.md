# Newell

> A display typeface built from parallel rails and decisive 45° diagonals.
> Precision. Movement. Connection.

**Newell** is an original geometric display typeface. Every glyph is
assembled from the same vocabulary — vertical rails, horizontal bars,
and 45° diagonals — joined with squared terminals. The system is
parametric: glyphs are generated from a declarative spec, not
hand-drawn, so the entire alphabet inherits one visual grammar.

This is the typeface used by **[jordannewell.com](https://jordannewell.com)**.

---

## Status

**v0.1.0-alpha** — uppercase A–Z, digits 0–9, basic punctuation.
Single weight. Static build (variable axes planned for v0.2).

The first release is functional and usable but unpolished — each glyph
follows the rules, but the rules themselves will tighten as the
typeface matures. Treat v0.x as a tech preview.

### Known v0.1 limitations

The v0.1 DNA (see SPEC.md) forbids curves, rounded terminals, and any
angle other than 45°. This makes several traditional letterforms
impossible to render cleanly. Known issues:

- **S** reads as **Z**. Two design attempts (full-width horizontals +
  short verticals + diagonal spine; "thunderbird" with offset half-
  horizontals) both fail to read as S in this vocabulary. v0.2 will
  likely add a third primitive type (step-diagonal or controlled curve)
  specifically for S/s/8/3/5/2.
- **C, D, G, O, P, Q, R, B** are rectilinear approximations of curved
  letters. They render as squared frames rather than curved bowls.
  Topology is correct; the visual reading is geometric rather than
  humanist.
- **A, V, W** are wider than the alphabet average because each leg is
  a full-cap-height 45° diagonal (geometrically forced).
- **M, W** inner notches reach only mid-height (y=350), not baseline.
  A baseline-reaching inner notch would require non-45° angles.
- **Digits** share the S-family legibility issue. **2, 5** inherit the
  diagonal-spine construction; **3, 8** are stacked right-opening /
  closed bowls that read as chunky frames. **0** is visually identical
  to **O** and **D** — readers rely on context to disambiguate.
- **$, @** are particularly hard in this vocabulary. **$** inherits S's
  readability issue; **@** is a closed frame approximation that does
  not read clearly as @. Both are best-effort v0.1 approximations.
- **Curly quotes** (' " ") lose their open/closed distinction — both
  render as small squares at cap height.

These are deliberate v0.1 trade-offs documented per-glyph in
`src/newell/glyphs.py`. The typeface is recommended for **display
and headline use**, not long-form body text.

---

## License

Released under the [SIL Open Font License 1.1](./OFL.txt).
You are free to use, embed, modify, and redistribute — including
commercially — provided the font and any derivatives remain under the
OFL. Attribution appreciated but not required.

Copyright © 2026 Jordan Newell.

---

## Repository layout

```
newell-typeface/
├── OFL.txt              SIL Open Font License 1.1
├── AUTHORS.txt          Attribution
├── SOURCES.txt          Provenance statement
├── SPEC.md              Typeface DNA (grid, strokes, primitives)
├── src/newell/          Parametric glyph generator (Python)
├── sources/             UFO masters (generated)
├── releases/            Built font binaries (OTF, TTF, WOFF2)
├── specimen/            Static specimen page
└── scripts/             Build + publish helpers
```

---

## Building

Requires Python 3.10+ and `fontTools`, `ufoLib2`, `booleanOperations`,
`ufo2ft`, `fontmake`.

```bash
py -m pip install -r requirements.txt
py scripts/build.py           # generates UFO + compiles OTF/TTF/WOFF2
```

Output appears under `releases/`.

---

## The DNA in one paragraph

All glyphs live on a 1000-unit em. Cap height is 700, x-height 500,
descender -200. Strokes are 110 units wide with squared terminals.
Diagonals are exactly 45°. The vocabulary is three primitives:
**rail** (a vertical or horizontal bar), **diagonal** (a 45° stroke),
and **junction** (a squared connection between two primitives). Every
letter is a composition. The signature diagonal of the `N` logo — the
one that connects the top of one rail to the bottom of another —
reappears in `M`, `R`, `K`, `V`, `W`, `X`, `Y`, `Z`, and the digits
`1`, `2`, `4`, `7`. That recurring diagonal is the family resemblance.

See [SPEC.md](./SPEC.md) for the full constitution.
