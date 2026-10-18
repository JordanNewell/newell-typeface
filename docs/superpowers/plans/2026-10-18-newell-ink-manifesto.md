# newell.ink Manifesto Edition — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (inline — chosen by Jordan's "execute") to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn newell.ink from a product page into the artwork's canonical statement (spec: `docs/superpowers/specs/2026-10-18-newell-ink-manifesto-design.md`).

**Architecture:** Static HTML at repo root (existing pattern). Anatomy plates are GENERATED from `src/newell/glyphs.py` by a new script (project philosophy: glyphs are generated, not hand-drawn — plates inherit that). Poster is `poster.html` → headless-Chrome print-to-PDF. All content sourced from SPEC.md/glyphs.py.

**Tech Stack:** Plain HTML/CSS/JS (existing), Python + fontTools (existing `scripts/` infra), headless Chrome (CDP, existing harness pattern), wrangler Pages (existing `newell-ink` project).

**Working rules:** No worktree (single session, repo shared — per memory: check `git status` before cleanup; do NOT touch untracked `AGENTS.md`). Commit after each task. Body prose never set in Newell (uppercase-only). Site palette stays black/`#00FF66` (own vibe). Push only on Jordan's word.

---

### Task 1: Manifesto hero (index) — remove product machinery

**Files:**
- Modify: `index.html` (hero block ~line 663–712, CSS `.signup` block, nav ~line 649–658, `<title>`/OG head)

- [x] **Step 1: Nav labels** — all 4 pages' navs become: Home→`Specimen`, About→`Score`, Try→`Try`, new `Print` → `print.html`, keep GitHub. Drop `specimen/` link (its content = index evidence). Update `<title>` everywhere to `Newell — A Typeface That Refuses Curves`; OG title/description to match; canonical stays `https://newell.ink/...`.

- [x] **Step 2: Hero rewrite (index)** — replace eyebrow + tagline + signup + CTA block with:

```html
<div class="eyebrow">v0.1.1-<span class="accent">alpha</span> &nbsp;·&nbsp; an edition, not a release</div>
<!-- logo-stage unchanged -->
<p class="tagline">
  Newell is a typeface that <strong>refuses curves</strong>. Three
  primitives — rail, diagonal, junction. Uppercase only. The S is
  Z's diagonal wearing S's name, <strong>on the record</strong>.
</p>
<div class="cta-row">
  <a class="btn btn--ghost" href="about.html">Read the score →</a>
  <a class="btn btn--ghost" href="print.html">Edition 001 →</a>
</div>
```

Delete the entire `<form class="signup">…</form>` block AND its JS wiring (`signup`, `signup-msg` listeners) AND the `.signup` CSS rules. Keep the meta strip (License/Files/Size/Designed by).

- [x] **Step 3: Verify** — `grep -c "signup" index.html` → `0`; `grep -c "refuses curves" index.html` → `≥1`; `grep -c "news.jordannewell.com" index.html` → `0`.

- [x] **Step 4: Commit** — `git add -A index.html && git commit -m "manifesto: hero becomes the statement, product machinery removed"`

### Task 2: Anatomy plates (index) — generated, not hand-drawn

**Files:**
- Create: `scripts/gen_plates.py`
- Modify: `index.html` (new `<section class="plates">` after `.dna`; CSS block)

- [x] **Step 1: Write generator** — `scripts/gen_plates.py` imports glyph dicts from `src/newell/glyphs.py` (same import pattern `build.py` uses), and for each hero glyph (A, E, M, N, R, S, W) emits one plate: large SVG rendering of the glyph's primitives (reuse the renderer used by `render_assets.py` — do NOT re-implement geometry), plus an annotation column: primitive counts (`3 RAILS · 2 DIAGONALS · 1 JUNCTION`), one-line role note from SPEC §7. Emits `docs/generated/plates.html` fragment. Print a summary line per glyph for eyeball check.

- [x] **Step 2: Run + verify** — `python scripts/gen_plates.py` → 7 plates emitted; S plate's note is the ruling line: `Z's diagonal wearing S's name`. Spot-check N shows the signature diagonal, W shows `4 DIAGONALS · 0 RAILS`.

- [x] **Step 3: Include in index** — `{% include %}` doesn't exist in plain HTML: inline the generated fragment into the new section (script prints to stdout → paste, or script writes fragment file and a one-liner in `build.py` splices it; choose fragment-file + documented splice command `python scripts/gen_plates.py --splice index.html` that replaces markers `<!-- PLATES:START -->…<!-- PLATES:END -->`).

- [x] **Step 4: Visual check** — serve locally (`python -m http.server`), headless-Chrome screenshot at 1440px: 7 plates, asymmetric grid, Newell glyphs render from `releases/Newell-Regular.woff2` (not system fallback — check a plate glyph vs `try.html` rendering).

- [x] **Step 5: Commit** — `git add scripts/gen_plates.py index.html && git commit -m "manifesto: anatomy plates generated from glyphs.py"`

### Task 3: Score page (about.html rewrite)

**Files:**
- Modify: `about.html` (hero + DNA + v0.1 + ROADMAP sections ~lines 452–586)

- [x] **Step 1: Hero stays, retitled** — keep `ENGINEERED,<br>NOT DRAWN.` (it's already the piece's voice). Sub-line becomes: "The score. Every glyph answers to it."

- [x] **Step 2: Score copy** — restructure sections:
  1. `THE INTENT` — SPEC §1 verbatim-faithful: three primitives, no curves, "closer to a barcode or a circuit diagram than to a humanist serif", the N diagonal as signature gesture.
  2. `THE GRAMMAR` — rail/diagonal/junction definitions + the generator assertion ("`abs(dx) == abs(dy)` — the generator refuses anything else. If a glyph cannot be expressed in rails + 45° diagonals, it does not belong in Newell.").
  3. `THE MEASURES` — metrics table from SPEC §2/§3 (UPM 1000, cap 700, x-height 500 reserved, stroke 110, gap 130, side bearing 90) in JetBrains Mono.
  4. `THE S RULING` — the approved blockquote: "Newell's S has no curve to hide behind — it's Z's diagonal wearing S's name. Same 45° spine as the N, half-bars for the terminals. v0.2 buys it back with a step-diagonal. Until then, squint."
  5. `WHO` — keep as-is.
  - DELETE: `WHAT'S IN v0.1` feature-list framing and `ROADMAP` roadmap framing (roadmap lives in the repo, not the artwork; v0.2 appears only inside the S ruling).

- [x] **Step 3: Verify** — `grep -c "ROADMAP\|Get notified\|signup" about.html` → `0`; `grep -c "squint" about.html` → `1`; local screenshot 1440px.

- [x] **Step 4: Commit** — `git commit -m "manifesto: about.html becomes the score"`

### Task 4: Edition 001 — poster page + PDF pipeline

**Files:**
- Create: `poster.html` (A3 sheet, not linked in nav directly — `/print` is the page)
- Create: `print.html` (edition page)
- Create: `scripts/render_poster.py`
- Modify: `releases/` (add generated PDF)

- [x] **Step 1: poster.html** — full-viewport A3-ratio sheet (`@page { size: A3; margin: 0 }`), black bg, containing: hero alphabet `AE MNRS W` set huge in Newell; NEWELL wordmark (N mark construction per brand rules — bars + diagonal, existing asset); colophon in JetBrains Mono:

```
NEWELL — A TYPEFACE THAT REFUSES CURVES
v0.1.1-ALPHA · 3 PRIMITIVES · 45° ONLY · NO CURVES
EDITION 001 — UNLIMITED DIGITAL, PRINTED ON DEMAND
DESIGNED + ENGINEERED BY JORDAN NEWELL · NEWELL.INK
```

- [x] **Step 2: render_poster.py** — headless Chrome `--print-to-pdf` on `poster.html` → `releases/newell-edition-001.pdf`. Assert PDF exists, `file` size < 2MB, page count = 1. Pattern: same Chrome invocation style as `scripts/screenshot.py`.

- [x] **Step 3: print.html** — small page: poster preview image (render page → PNG screenshot asset `assets/poster-preview.png`), download button → `releases/newell-edition-001.pdf`, "print your own" note (browser print on `poster.html` gives clean A3/A2 via scale-to-fit), edition line. Nav gets `Print`.

- [x] **Step 4: Verify** — PDF opens, 1 page, A3 dims (1191×842pt); `poster.html` in browser renders full sheet, no scrollbars at 210:297 aspect.

- [x] **Step 5: Commit** — `git add poster.html print.html scripts/render_poster.py releases/newell-edition-001.pdf assets/poster-preview.png && git commit -m "manifesto: Edition 001 poster + print page"`

### Task 5: Responsive QC sweep

**Files:** none (verification only; fix-forward if issues found)

- [x] **Step 1:** CDP width-override sweep (AEON headless gotcha: min-width ~469px — probe via `Emulation.setDeviceMetricsOverride`, not screenshots alone) at **1440px and 390px** for `/`, `/about`, `/try`, `/print`: no horizontal overflow (`scrollWidth <= clientWidth`), plates grid stacks to single column on 390, poster preview scales, nav wraps gracefully.
- [x] **Step 2:** Contrast of annotation text (`--text-dim` on black) ≥ 4.5:1 for score copy; adjust to `#a0a0a0`+ if not.
- [x] **Step 3:** Fix findings, re-sweep, commit any fixes: `git commit -m "manifesto: responsive QC fixes"`

### Task 6: Deploy + live smoke

**Files:** none in repo (deploy dir rebuild)

- [x] **Step 1: Rebuild deploy dir INCLUDING specimen/** — `rm -rf /c/tmp/newell-ink-deploy && mkdir -p /c/tmp/newell-ink-deploy && cp -r index.html about.html try.html print.html poster.html specimen assets releases favicon-32.png favicon-512.png favicon.ico apple-touch-icon.png /c/tmp/newell-ink-deploy/` (canonical URLs already point at newell.ink in repo files).

- [x] **Step 2: Deploy** — `cd /c/tmp/newell-ink-deploy && npx wrangler pages deploy . --project-name newell-ink --branch main --force` (wrangler 4.15x gotcha: `--force` needed; delegation fails otherwise). If project-create is ever needed again: `--force` there too.

- [x] **Step 3: Live smoke** — `curl -s -o /dev/null -w "%{http_code}"` → 200 for `newell.ink`, `/about`, `/try`, `/print`, `/releases/newell-edition-001.pdf`, `/releases/Newell-Regular.woff2`, `/specimen/`. `curl -s https://newell.ink | grep -c "signup\|news.jordannewell.com"` → `0`. `grep -c "refuses curves"` → `≥1`.

- [x] **Step 4: Report to Jordan** — live URLs + screenshot; **ask before `git push`** (gitleaks hook will run; GH Pages mirror updates on push).

---

## Self-review

- **Spec coverage:** §1 concept → Tasks 1/3; §2 anatomy plates → Task 2; score → Task 3; §3 poster/edition → Task 4; §4 visual language → Tasks 2/3 (Newell-uppercase-only enforced by plates + hero strings; prose stays neutral sans — existing site CSS already does this); §5 nav/meta → Task 1; deploy → Task 6; §6 Route B dormant → no task (correct); §7 acceptance → Task 5 + Task 6 Step 3. Spec's "specimen grid stays below as evidence" → existing index content below hero remains (Task 1 keeps principles/dna sections; plates ADD on).
- **Placeholder scan:** Task 2 Step 1 delegates geometry to existing renderer (named), not "implement later". Task 3 copy is specified. No TBDs.
- **Type consistency:** `gen_plates.py` markers `PLATES:START/END` used only in Task 2; nav labels consistent across Tasks 1/4 (`Print`); deploy paths match repo root file names.
