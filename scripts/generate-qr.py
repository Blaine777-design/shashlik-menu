"""Generate print-safe PNG and SVG QR files from assets/qr/production-url.txt."""
from pathlib import Path
import qrcode
import qrcode.image.svg

ROOT = Path(__file__).resolve().parents[1]
qr_dir = ROOT / "assets" / "qr"
url = (qr_dir / "production-url.txt").read_text(encoding="utf-8").strip()
if not url.startswith("https://"):
    raise SystemExit("Production URL must start with https://")

qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_H,
                   box_size=32, border=4)
qr.add_data(url)
qr.make(fit=True)
qr.make_image(fill_color="#24221f", back_color="white").save(qr_dir / "menu-qr.png")

svg = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_H,
                    box_size=10, border=4)
svg.add_data(url)
svg.make(fit=True)
svg.make_image(image_factory=qrcode.image.svg.SvgPathImage,
               fill_color="#24221f", back_color="white").save(qr_dir / "menu-qr.svg")
print(url)
