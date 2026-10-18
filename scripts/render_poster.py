"""Render poster.html to releases/newell-edition-001.pdf (A3, 1 page).

Uses Playwright's headless Chromium page.pdf() — same engine/harness as
scripts/screenshot.py. Asserts the PDF exists, is one page, and is
small enough to ship (plan gate: < 2MB).
"""
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "releases" / "newell-edition-001.pdf"
URL = "http://127.0.0.1:8765/poster.html"
MAX_BYTES = 2 * 1024 * 1024


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(500)  # let fonts settle
        page.pdf(
            path=str(OUT),
            width="297mm",
            height="420mm",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()

    data = OUT.read_bytes()
    pages = len(re.findall(rb"/Type\s*/Page[^s]", data))
    assert pages == 1, f"expected 1 page, found {pages}"
    assert len(data) < MAX_BYTES, f"PDF too large: {len(data)} bytes"
    print(f"wrote {OUT} ({len(data)} bytes, {pages} page)")


if __name__ == "__main__":
    sys.exit(main())
