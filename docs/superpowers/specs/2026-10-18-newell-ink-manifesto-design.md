# newell.ink — Manifesto Edition — Design Spec

**Date:** 2026-10-18
**Status:** approved (Jordan: "sounds great")
**Scope:** rework newell.ink from specimen site into the artwork's canonical statement. Route A (manifesto edition) now; Route B (process serial) dormant until v0.2 S-work starts. No commerce.

---

## 1. Concept

newell.ink stops being a font page and becomes the piece:

> **Newell is a typeface that refuses curves.**

The v0.1 constraints — uppercase-only, S reads as Z, rectilinear C/D/O —
are presented as **rulings, never apologies**. The primitive grammar in
`SPEC.md` (rail / diagonal / junction; "if a glyph cannot be expressed in
rails + 45° diagonals, it does not belong in Newell") is the score of the
work. The site's voice is the SPEC's voice: declarative, engineered,
zero hedging.

Success = the site reads as a conceptual-art edition, not a product page.
Non-goal: retail font marketing, email capture, buy buttons, pricing.

## 2. Site structure

Still 3 existing pages + 1 new. No nav bloat.

| Page | Role | Change |
|---|---|---|
| `/` (index) | Manifesto hero + anatomy plates + evidence | Hero line becomes the manifesto line. NEW section: **anatomy plates**. Specimen grid stays below as "the evidence." |
| `/about` | The score (art-catalog page) | Rewritten: design intent, primitive grammar, the S ruling, grid/metrics. This page argues the constraints are the design. |
| `/try` | Interactive gallery piece | **Untouched.** |
| `/print` (new) | The edition | One poster — "Newell — Edition 001" — free PDF download + browser-print-to-A3/A2. Numbered-edition framing, print-on-demand, zero inventory. |

### Anatomy plates (index)

Hero alphabet **A E M N R S W**, one plate per glyph, each showing the
glyph large in Newell with its primitive decomposition annotated
(rail/diagonal/junction counts and roles), sourced from `SPEC.md` §7 and
`src/newell/glyphs.py` — no hand-invented anatomy. Layout: asymmetric
grid (anti-pattern: centered-symmetric), generous negative space.

### The S ruling (score page)

Documented as intent, grounded in the real primitive construction
(`glyphs.py`: half-rails + top-right→bottom-left 45° spine — Z's
diagonal, not a mirrored one). Draft voice:

> Newell's S has no curve to hide behind — it's Z's diagonal wearing
> S's name. Same 45° spine as the N, half-bars for the terminals.
> v0.2 buys it back with a step-diagonal. Until then, squint.

(Final wording may shift; register = declarative, first person, no marketing.)

## 3. The edition (poster)

`/print` serves `poster.html` — a single A3-ratio sheet containing:

- Hero alphabet set large in Newell
- The NEWELL wordmark (N mark per `logo/newell-n.svg` construction rules — bars + diagonal, no restyling)
- Colophon: version (v0.1.1-alpha), date, primitive count, "set in Newell"
- Edition line: "Edition 001 — unlimited digital, printed on demand"

**Pipeline:** headless Chrome print-to-PDF (matches the `og-image.html`
pattern; `scripts/screenshot.py` harness exists). New `scripts/render_poster.py`
or equivalent: render `poster.html` → `newell-edition-001.pdf`, PDF
committed to `releases/` and linked from `/print`. CSS `@page { size: A3 }`
so browser print dialog also produces a clean A3/A2 print without the PDF.

## 4. Visual language

- Site keeps its **own** black / `#00FF66` identity (project's own vibe — NOT NEWELL green, per own-vibe-per-project rule).
- **Newell set everywhere it can be** — showing the alpha IS the content. Uppercase display strings only.
- **JetBrains Mono** for annotations, metrics, colophon.
- **Body prose in a neutral sans** (system stack is fine) — Newell cannot render lowercase; faking it would undercut the honesty. This asymmetry (Newell voice / prose voice) is deliberate.
- Existing brand constraints apply: no gradients, no glow, 8px grid, ≥30% negative space, no centered-symmetric layouts.

## 5. Meta / plumbing

- `<title>`: `Newell — A Typeface That Refuses Curves`
- OG title/description/canonical all `https://newell.ink/...` (already flipped in `45bafa0`; keep consistent across new pages)
- Nav labels: `SPECIMEN · SCORE · TRY · PRINT` (uppercase; Newell where legible, mono fallback acceptable in nav)
- Deploy: CF Pages project `newell-ink` (direct upload). GH Pages subpath mirror keeps working — relative asset paths must stay relative.
- Commit locally; push only on Jordan's word (gitleaks hook runs).

## 6. Route B (process serial) — dormant by design

**No empty build-log page.** First entry ships when v0.2's S/step-diagonal
work actually starts; at that point a `/log` page joins the nav and the
first post documents the S battle. Until then B does not exist on the site.

## 7. Testing / acceptance

- All four pages render clean at 1440px and 390px (CDP sweep — width-override probe per AEON headless-chrome gotcha).
- Anatomy plates match `SPEC.md` §7 decompositions exactly (spot-check against `glyphs.py`).
- Poster PDF: correct A3 dimensions, glyphs render from `releases/Newell-Regular.woff2` (not fallback), file < 2MB.
- No page mixes Newell into lowercase body text.
- Smoke: 200s on `/`, `/about`, `/try`, `/print`, PDF, woff2 on newell.ink.
