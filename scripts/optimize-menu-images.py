"""Convert generated menu JPG files to compact 640x480 WebP assets."""
from pathlib import Path
from PIL import Image

folder = Path(__file__).resolve().parents[1] / "assets" / "images" / "menu"
for source in sorted(folder.glob("*.jpg")):
    with Image.open(source) as image:
        image.convert("RGB").resize((640, 480), Image.Resampling.LANCZOS).save(
            source.with_suffix(".webp"), "WEBP", quality=80, method=6
        )
print(f"Optimized {len(list(folder.glob('*.webp')))} images")
