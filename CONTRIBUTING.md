# Contributing

Thanks for considering a contribution to **Newell** — a geometric
display typeface built from parallel rails and decisive 45° diagonals.
This doc covers dev setup, the build pipeline, the testing convention
(automated generator tests + manual visual review), glyph-design
workflow, and PR expectations.

Newell is **opinionated software**: glyphs follow a three-primitive
vocabulary (rail, diagonal, junction) defined in
[`SPEC.md`](SPEC.md). Contributions that violate the spec — adding
curves, non-45° angles, or rounded terminals — will not merge without
a spec amendment first. Open an issue to scope that conversation
before sending code.

## Project layout

```
.
├── OFL.txt                           SIL Open Font License 1.1
├── AUTHORS.txt                       Attribution
├── SOURCES.txt                       Provenance (original work)
├── SPEC.md                           Typeface DNA constitution
├── ROADMAP.md                        v0.2 → v1.0 plan
├── CHANGELOG.md                      Release history
├── requirements.txt                  Python build deps
│
├── src/newell/                       Parametric glyph generator (Python)
│   ├── primitives.py                 vline / hline / diag expanders
│   ├── generator.py                  Boolean union + UFO assembly
│   ├── font.py                       UFO metadata
│   ├── glyphs.py                     Declarative glyph definitions
│   └── test_generator.py             Test suite (pytest-collectable)
│
├── scripts/
│   ├── build.py                      Generate UFO only
│   ├── build_all.py                  UFO → OTF + TTF + WOFF2 (end-to-end)
│   ├── preview.py                    Render glyph PNGs from UFO
│   ├── screenshot.py                 Playwright HTML screenshots
│   ├── render_assets.py              Re-render OG / wordmark / N-mark
│   └── render_favicons.py            Resize N-mark → favicon variants
│
├── sources/                          Generated UFO masters (gitignored)
├── releases/                         Built font binaries (OTF/TTF/WOFF2)
├── specimen/                         Technical specimen page
├── assets/                           Logo, OG image, favicons, wordmark
└── .github/workflows/                ci.yml (test+build) + release.yml (tag→binaries)
```

Glyphs are **generated, not hand-drawn**. You write declarative rules in
`src/newell/glyphs.py`; the generator expands them into outlines. Don't
edit UFO files directly — they're regenerated on every build.

## Dev setup

Requires **Python 3.10+**. On Windows, use `py` (the Python launcher),
not `python`.

```bash
git clone https://github.com/JordanNewell/newell-typeface.git
cd newell-typeface
py -m pip install -r requirements.txt
```

Dependencies (from `requirements.txt`):

- `fontTools[woff]` — UFO/TTF/OTF r/w + WOFF2 compression
- `ufoLib2` — UFO source format
- `booleanOperations` — polygon union for stroke expansion
- `ufo2ft` + `fontmake` — UFO → OpenType compilation
- `brotli` — required by fontTools for WOFF2 (Linux CI breaks without it)

CI runs on Python 3.13.

## Building

```bash
py scripts/build_all.py        # UFO → OTF + TTF + WOFF2, into releases/
py scripts/build.py            # UFO only, into sources/Newell-Regular.ufo
py scripts/preview.py          # render glyph PNGs from the generated UFO
```

To regenerate brand assets after a glyph change:

```bash
py scripts/render_assets.py    # OG image + wordmark + N-mark via Playwright
py scripts/render_favicons.py  # favicon variants via Pillow
```

Build output sizes (current, for orientation):

| Format | Size   |
|--------|--------|
| OTF    | ~5.0 KB |
| TTF    | ~6.4 KB |
| WOFF2  | ~2.1 KB |

## Testing

There is **no formal pytest suite required to run tests** —
`src/newell/test_generator.py` is written with bare `assert` statements
so it runs directly:

```bash
py src/newell/test_generator.py    # bare asserts, exits non-zero on failure
python -m pytest src/newell/       # alternatively, pytest will collect test_* funcs
```

CI runs `python src/newell/test_generator.py` (see
`.github/workflows/ci.yml`).

### What the generator tests check

- Primitive expanders produce the expected corner counts and coordinates
- Stroke widths are constant (110 units, per `SPEC.md` §3)
- All declared glyphs in `glyphs.py` resolve to non-empty outlines
- Boolean union doesn't produce degenerate polygons
- The assembled UFO passes `validate_ufo()` (fontTools sanity checks)

### What the tests **don't** check

Visual legibility. There is no automated "does this S read as an S?"
test. The known v0.1 limitations in `README.md` (S reads as Z, C/D/O
rectilinear, etc.) are deliberate trade-offs against the three-primitive
vocabulary, not bugs.

### Visual review checklist (manual, every glyph PR)

When your PR changes a glyph's outlines:

- [ ] Render at multiple sizes via `py scripts/preview.py`
- [ ] Check at **display size** (≥48px) — does it read as the target letter?
- [ ] Check at **body size** (~16px) — note any collapse (expected for v0.1)
- [ ] Verify on **light and dark backgrounds** (the typeface is monoline;
      stroke contrast can shift)
- [ ] Verify in **context** alongside 3+ neighboring glyphs from the same
      family — the recurring 45° N-diagonal is the family resemblance
- [ ] If touching kerning-relevant geometry, sanity-check side bearings

Include **before/after PNGs** in the PR description. Visual diffs that
can't be seen can't be reviewed.

## Glyph-design workflow

To add or change a glyph:

1. **Read [`SPEC.md`](SPEC.md).** Every glyph answers to the constitution.
   If your change requires a new primitive (e.g. v0.2's planned
   step-diagonal for the S family), the spec amendment lands **first**,
   as its own PR.
2. **Edit `src/newell/glyphs.py`.** Add or modify the declarative rule
   using only `vline` / `hline` / `diag` primitives.
3. **Run the generator tests** — `py src/newell/test_generator.py`.
4. **Build + preview** — `py scripts/build_all.py` then
   `py scripts/preview.py`.
5. **Visual review** per the checklist above.
6. **Update docs** — `SPEC.md` if metrics change, `README.md` glyph
   table if a new glyph is added, `CHANGELOG.md` with a one-liner.
7. **Open the PR** with before/after PNGs attached.

Do **not** hand-edit files under `sources/` (UFO) or `releases/` (binaries)
— both are build outputs. The generator is the source of truth.

## Code style

- **Python 3.10+** for the generator. Type hints encouraged but not
  enforced (`mypy` is not currently in CI).
- **Bare asserts in `test_generator.py`** — the file is designed to run
  directly without pytest. Don't introduce a hard pytest dependency.
- **Declarative glyph rules** — keep `glyphs.py` readable. If a glyph's
  rule needs more than ~30 lines, factor a helper into `primitives.py`
  or `generator.py` rather than inlining.
- **Comments explain *why*, not *what*** — especially around
  coordinate math, which is easy to get wrong and hard to review by eye.

## Commits

- Subject ≤ 72 chars, imperative mood (`Add X`, `Fix Y`).
- Conventional-commit prefixes (`feat:`, `fix:`, `docs:`, `chore:`) are
  used in this repo — match them when you can.
- Reference the issue number in the body if applicable.
- **No `Co-Authored-By: Claude` or any AI-attribution trailer.** Tools
  don't get attribution; humans do.

## Pull requests

Open a PR against `master`. CI must pass — `lint-and-test` (runs the
generator tests) followed by `build` (regenerates all binaries).

Before requesting review:

- [ ] `py src/newell/test_generator.py` passes (CI gate)
- [ ] `py scripts/build_all.py` produces OTF, TTF, and WOFF2 under `releases/`
- [ ] No new files under `sources/` or `releases/` committed (build outputs)
- [ ] `SPEC.md` updated if metrics or the vocabulary changed
- [ ] `README.md` glyph table updated if a glyph was added or removed
- [ ] `CHANGELOG.md` has a one-line entry under the next version
- [ ] Before/after PNGs attached for any visually-impacting glyph change

### Release flow

Releases are automated via `release.yml` on `v*` tag push. The workflow
builds all three formats, verifies they exist, and attaches them to a
GitHub Release. **Don't push tags as part of a PR** — a maintainer cuts
the release.

To bump the version, edit `font.py`'s UFO `versionMajor` / `versionMinor`
and add a `CHANGELOG.md` entry. The release workflow picks it up.

## Filing issues

- 🐛 **Generator bugs** — paste the Python traceback, the input that
  triggered it, and the offending glyph definition from `glyphs.py`.
- 🎨 **Legibility feedback** — for v0.1 limitations already documented
  in `README.md` (S-as-Z, rectilinear C/D/O, etc.), they're tracked in
  `ROADMAP.md` for v0.2. New ones not yet listed are welcome as issues.
- ✨ **Glyph requests** — name the glyph, link to a usage example, note
  whether it's plausibly expressible in pure rail+diagonal+junction
  vocabulary. (Curves are out until v0.2 at earliest.)
- 📚 **Docs** — typos in `SPEC.md`, dead links, missing metric tables.

## Security disclosures

Newell ships no executable code in the font binaries, but the build
pipeline runs Python and Playwright. Do **not** open a public issue for
vulnerabilities in the build scripts (e.g., unsafe deserialization of
UFO input, SSRF in screenshot.py). See [`SECURITY.md`](SECURITY.md)
for the private reporting path.

## License

By contributing, you agree your contributions are licensed under the
[SIL Open Font License 1.1](OFL.txt). Code in `src/` and `scripts/`
is also OFL-1.1 (the repo is single-license by design — see
`SOURCES.txt`).
