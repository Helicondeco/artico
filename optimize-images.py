#!/usr/bin/env python3
"""Optimize new photos for artico.rs.

Usage:
    python3 optimize-images.py photo.jpg [photo2.png ...]
    python3 optimize-images.py "IMG_1234.jpg:naziv-slike-na-srpskom"

Each image is rotated per EXIF, resized to max 1200px, saved as WebP
next to the original as assets/<name>.webp. Give it an SEO-friendly
Serbian name after a colon, otherwise the original filename is kept.
Requires: pip install Pillow
"""
import sys
from pathlib import Path
from PIL import Image, ImageOps

ASSETS = Path(__file__).parent / "assets"
MAX_SIDE = 1200
QUALITY = 82

if len(sys.argv) < 2:
    sys.exit(__doc__)

for arg in sys.argv[1:]:
    src_str, _, new_name = arg.partition(":")
    src = Path(src_str)
    if not src.exists():
        print(f"SKIP (not found): {src}")
        continue
    img = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    w, h = img.size
    if max(w, h) > MAX_SIDE:
        scale = MAX_SIDE / max(w, h)
        img = img.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
    out = ASSETS / f"{new_name or src.stem}.webp"
    img.save(out, "WEBP", quality=QUALITY, method=6)
    print(f"{src.name} ({src.stat().st_size // 1024} KB) -> {out.name} "
          f"({out.stat().st_size // 1024} KB, {img.size[0]}x{img.size[1]})")
    print(f'  HTML: <img src="assets/{out.name}" alt="OPIS" width="{img.size[0]}" height="{img.size[1]}" loading="lazy">')
