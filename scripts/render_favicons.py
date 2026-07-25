"""Generate favicon variants from the source n-mark.png (512x512).

Outputs:
  assets/apple-touch-icon.png   180x180 (iOS home screen)
  assets/favicon-32.png         32x32   (browser tab, modern)
  assets/favicon-16.png         16x16   (browser tab, legacy)
  assets/favicon.ico            multi-size ICO (legacy Windows)
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "n-mark.png"
OUT = ROOT / "assets"


def main():
    src = Image.open(SRC).convert("RGBA")
    print(f"source: {SRC} ({src.size})")

    # Apple touch icon (180x180). Apple recommends no transparency.
    apple = src.resize((180, 180), Image.LANCZOS)
    bg = Image.new("RGBA", apple.size, (0, 0, 0, 255))
    bg.paste(apple, mask=apple.split()[3])
    apple_path = OUT / "apple-touch-icon.png"
    bg.convert("RGB").save(apple_path, "PNG", optimize=True)
    print(f"wrote {apple_path}  ({apple_path.stat().st_size:,} bytes)")

    # 32x32 PNG
    small32 = src.resize((32, 32), Image.LANCZOS)
    p32 = OUT / "favicon-32.png"
    small32.save(p32, "PNG", optimize=True)
    print(f"wrote {p32}  ({p32.stat().st_size:,} bytes)")

    # 16x16 PNG
    small16 = src.resize((16, 16), Image.LANCZOS)
    p16 = OUT / "favicon-16.png"
    small16.save(p16, "PNG", optimize=True)
    print(f"wrote {p16}  ({p16.stat().st_size:,} bytes)")

    # Multi-size ICO (legacy Windows). Include 16, 32, 48, 64.
    ico_path = OUT / "favicon.ico"
    ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
    ico_images = [src.resize(s, Image.LANCZOS) for s in ico_sizes]
    ico_images[0].save(
        ico_path,
        format="ICO",
        sizes=ico_sizes,
        append_images=ico_images[1:],
    )
    print(f"wrote {ico_path}  ({ico_path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
