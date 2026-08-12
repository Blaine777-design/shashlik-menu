"""Decode the full and reduced QR PNG and fail if either differs from configured URL."""
from pathlib import Path
import cv2
import numpy as np

root = Path(__file__).resolve().parents[1]
expected = (root / "assets/qr/production-url.txt").read_text(encoding="utf-8").strip()
image = cv2.imdecode(np.fromfile(root / "assets/qr/shashlik-menu-qr.png", dtype=np.uint8), cv2.IMREAD_COLOR)
detector = cv2.QRCodeDetector()
for label, candidate in (("full", image), ("96px", cv2.resize(image, (96, 96), interpolation=cv2.INTER_AREA))):
    decoded, _, _ = detector.detectAndDecode(candidate)
    if decoded != expected:
        raise SystemExit(f"{label}: QR decode failed ({decoded!r})")
    print(f"{label}: {decoded}")
