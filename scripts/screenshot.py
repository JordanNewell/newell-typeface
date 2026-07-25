"""Screenshot the local Newell site for visual verification.

Renders index.html at desktop width and saves PNGs for inspection.

With --anim, captures the hero at three phases of the logo load
animation (immediately, after 1.5s, after 2.5s) plus a reduced-motion
pass that should show the logo instantly.
"""
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT_DIR = Path("scripts/_preview")
OUT_DIR.mkdir(exist_ok=True)

BASE = "http://127.0.0.1:8765"


def main():
    args = sys.argv[1:]
    anim_mode = "--anim" in args
    targets = [a for a in args if not a.startswith("--")] or ["", "about.html", "try.html"]
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=2,
        )
        page = ctx.new_page()
        for path in targets:
            url = f"{BASE}/{path}"
            name = path.rstrip("/") or "home"

            if anim_mode and name == "home":
                # Three-phase logo animation capture.
                # Cache-bust so each run starts the animation fresh.
                page.goto(f"{url}?cb={int(time.time()*1000)}", wait_until="domcontentloaded")
                page.evaluate("window.scrollTo(0, 0)")
                # Phase 1: immediately (~200ms in, rails should be appearing)
                page.wait_for_timeout(200)
                out = OUT_DIR / "home_anim_phase1.png"
                page.screenshot(path=str(out), full_page=False,
                                clip={"x": 0, "y": 0, "width": 1440, "height": 900})
                print(f"wrote {out}")
                # Phase 2: 1.5s total — logo should be fading/scaling in over rails
                page.wait_for_timeout(1300)
                out = OUT_DIR / "home_anim_phase2.png"
                page.screenshot(path=str(out), full_page=False,
                                clip={"x": 0, "y": 0, "width": 1440, "height": 900})
                print(f"wrote {out}")
                # Phase 3: 2.5s total — animation complete, tagline visible
                page.wait_for_timeout(1000)
                out = OUT_DIR / "home_anim_phase3.png"
                page.screenshot(path=str(out), full_page=False,
                                clip={"x": 0, "y": 0, "width": 1440, "height": 900})
                print(f"wrote {out}")

                # Reduced-motion: logo should appear instantly, no primitives.
                page.emulate_media(reduced_motion="reduce")
                page.goto(f"{url}?cb=reduced", wait_until="domcontentloaded")
                page.evaluate("window.scrollTo(0, 0)")
                page.wait_for_timeout(300)
                out = OUT_DIR / "home_anim_reduced.png"
                page.screenshot(path=str(out), full_page=False,
                                clip={"x": 0, "y": 0, "width": 1440, "height": 900})
                print(f"wrote {out}")
                continue

            page.goto(url, wait_until="networkidle")
            page.wait_for_timeout(500)  # let fonts settle
            # Full page
            out_full = OUT_DIR / f"{name}_full.png"
            page.screenshot(path=str(out_full), full_page=True)
            print(f"wrote {out_full}")
            # Hero only (first viewport)
            out_hero = OUT_DIR / f"{name}_hero.png"
            page.screenshot(path=str(out_hero), full_page=False, clip={"x": 0, "y": 0, "width": 1440, "height": 900})
            print(f"wrote {out_hero}")
        browser.close()


if __name__ == "__main__":
    main()
