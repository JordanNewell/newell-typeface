"""Render brand assets: OG image, favicons, README wordmark.

Uses Playwright to screenshot styled HTML so we get the actual Newell
font rendering (no Matplotlib approximation).
"""
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)
BASE = "http://127.0.0.1:8765"


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(device_scale_factor=2)

        # --- OG image: 1200x630 social card ---
        page = ctx.new_page()
        page.set_viewport_size({"width": 1200, "height": 630})
        page.goto(f"{BASE}/og-image.html", wait_until="networkidle")
        page.wait_for_timeout(500)
        og_path = OUT / "og.png"
        page.screenshot(path=str(og_path), clip={"x": 0, "y": 0, "width": 1200, "height": 630})
        print(f"wrote {og_path}  ({og_path.stat().st_size:,} bytes)")

        # --- N-mark favicon at high res (512x512 source) ---
        page.set_viewport_size({"width": 512, "height": 512})
        page.set_content("""<!DOCTYPE html><html><head><style>
          @font-face {
            font-family: "Newell";
            src: url("releases/Newell-Regular.woff2") format("woff2");
            font-display: block;
          }
          * { box-sizing: border-box; margin: 0; padding: 0; }
          html, body { width: 512px; height: 512px; }
          body {
            background: #000;
            display: flex; align-items: center; justify-content: center;
          }
          .mark {
            font-family: "Newell", sans-serif;
            font-size: 380px;
            line-height: 1;
            color: #00FF66;
            text-shadow: 0 0 30px rgba(0,255,102,0.3);
          }
        </style></head><body><div class="mark">N</div></body></html>""")
        page.wait_for_timeout(300)
        n512_path = OUT / "n-mark.png"
        page.screenshot(path=str(n512_path), clip={"x": 0, "y": 0, "width": 512, "height": 512})
        print(f"wrote {n512_path}  ({n512_path.stat().st_size:,} bytes)")

        # --- README wordmark: wide NEWELL on black ---
        page.set_viewport_size({"width": 1600, "height": 400})
        page.set_content("""<!DOCTYPE html><html><head><style>
          @font-face {
            font-family: "Newell";
            src: url("releases/Newell-Regular.woff2") format("woff2");
            font-display: block;
          }
          * { box-sizing: border-box; margin: 0; padding: 0; }
          html, body { width: 1600px; height: 400px; }
          body {
            background: #000;
            display: flex; align-items: center; justify-content: center;
          }
          .mark {
            font-family: "Newell", sans-serif;
            font-size: 280px;
            line-height: 1;
            color: #00FF66;
            letter-spacing: 0.02em;
            text-shadow: 0 0 40px rgba(0,255,102,0.2);
          }
        </style></head><body><div class="mark">NEWELL</div></body></html>""")
        page.wait_for_timeout(300)
        readme_path = OUT / "wordmark.png"
        page.screenshot(path=str(readme_path), clip={"x": 0, "y": 0, "width": 1600, "height": 400})
        print(f"wrote {readme_path}  ({readme_path.stat().st_size:,} bytes)")

        browser.close()


if __name__ == "__main__":
    main()
