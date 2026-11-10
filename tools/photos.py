"""Rohfotos aus fotos-neu/ für die Website aufbereiten (siehe CLAUDE.md, „Fotos einbauen“).

Nur technische Korrekturen: EXIF-Drehung, Metadaten weg, Begradigen (stürzende Linien),
Zuschnitt auf 3:4, dezente Tonwerte, Gelbstich moderat neutralisieren.

    python3 tools/photos.py            # alle PICKS verarbeiten
    python3 tools/photos.py t-flur     # nur bestimmte Namen

Ausgabe: assets/img/<name>-600.webp und -1200.webp (bzw. kleinere Breite, wenn das Original schmaler ist).
"""
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "fotos-neu"
OUT = ROOT / "assets" / "img"

# name, Quelldatei, Mitte x, Mitte y (0..1 im begradigten Bild), Zoom (1 = größtmöglicher 3:4-Ausschnitt)
PICKS = [
    ("t-flur-decke", "signal-2026-11-09-22-09-01-758_007.jpg", .5, .5, 1),
    ("t-trennwand-tuer", "signal-2026-11-09-22-09-01-758_016.jpg", .5, .5, 1),
    ("t-staenderwerk", "signal-2026-11-09-22-12-21-734_007.jpg", .5, .5, 1),
    ("t-keller-verkleidung", "signal-2026-11-09-22-09-01-758_023.jpg", .5, .5, 1),
    ("d-dampfbremse", "signal-2026-11-09-22-12-21-734_002.jpg", .5, .5, 1),
    ("d-dachfenster", "signal-2026-11-09-22-09-01-758_032.jpg", .5, .5, 1),
    ("d-lattung", "signal-2026-11-09-22-12-21-734_015.jpg", .56, .5, 1),  # rechts von der Kamera-Einblendung unten links
    ("d-gespachtelt", "signal-2026-11-09-22-11-57-148_022.jpg", .5, .5, 1),
    ("d-balken", "signal-2026-11-09-22-09-01-758_026.jpg", .4, .5, 1),
    ("d-fenster-gespachtelt", "signal-2026-11-09-22-12-21-734_003.jpg", .5, .5, 1),
    ("k-wc-umbau", "signal-2026-11-09-22-11-57-148_014.jpg", .5, .5, 1),
    ("k-wc-fertig", "signal-2026-11-09-22-11-57-148_008.jpg", .5, .62, 1),
    ("k-bad-platten", "signal-2026-11-09-22-11-57-148_012.jpg", .5, .5, 1),
    ("k-bad-gespachtelt", "signal-2026-11-09-22-11-57-148_024.jpg", .5, .5, 1),
]

STRENGTH = 0.8   # Anteil der Perspektivkorrektur (voll korrigiert wirkt bei Weitwinkel unnatürlich)
MAX_TILT = 12.0  # Grad; stärkere Abweichungen sind eher Absicht/Dachschrägen als Schiefstand


def vertical_segments(gray):
    h, w = gray.shape
    lsd = cv2.createLineSegmentDetector()
    lines = lsd.detect(gray)[0]
    if lines is None:
        return []
    segs = []
    for x1, y1, x2, y2 in lines[:, 0]:
        dx, dy = x2 - x1, y2 - y1
        length = np.hypot(dx, dy)
        if length < 0.08 * h:
            continue
        ang = np.degrees(np.arctan2(dx, dy))  # 0 = senkrecht
        ang = (ang + 90) % 180 - 90
        if abs(ang) > MAX_TILT:
            continue
        segs.append((x1, y1, x2, y2, length))
    return segs


def straighten(rgb):
    """Senkrechte Kanten senkrecht stellen.

    Für jede fast senkrechte Kante wird die Steigung k = dx/dy und ihre Lage x in Bildmitte bestimmt.
    Modell k(x) = k0 + k1 * (x - w/2): k0 = Schiefstand, k1 = stürzende Linien. Unplausible Werte
    (Dachschrägen, Weitwinkel-Ränder) werden nicht korrigiert.
    """
    h, w = rgb.shape[:2]
    small = cv2.resize(cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY), (w // 2, h // 2))
    segs = vertical_segments(small)
    ks, xs, wts = [], [], []
    for x1, y1, x2, y2, L in segs:
        x1, y1, x2, y2 = x1 * 2, y1 * 2, x2 * 2, y2 * 2
        k = (x2 - x1) / (y2 - y1)
        ks.append(k)
        xs.append(x1 + k * (h / 2 - y1) - w / 2)
        wts.append(L)
    if len(ks) < 6:
        return rgb, 0.0, 0.0
    ks, xs, wts = map(np.array, (ks, xs, wts))
    keep = np.ones(len(ks), bool)
    for _ in range(4):
        A = np.stack([np.ones(keep.sum()), xs[keep]], 1) * wts[keep, None]
        k0, k1 = np.linalg.lstsq(A, ks[keep] * wts[keep], rcond=None)[0]
        res = np.abs(ks - (k0 + k1 * xs))
        keep = res < max(2.5 * np.median(res[keep]), np.tan(np.radians(0.5)))
        if keep.sum() < 6:
            return rgb, 0.0, 0.0
    if abs(k0) > np.tan(np.radians(4)):
        k0 = 0.0
    if abs(k1 * w / 2) > np.tan(np.radians(7)):
        k1 = 0.0
    if k0 == 0 and k1 == 0:
        return rgb, 0.0, 0.0
    S = STRENGTH
    src, dst = [], []
    for xm in (-w / 2, w / 2):
        k = k0 + k1 * xm
        for y, sgn in ((0, -1), (h, 1)):
            src.append([xm + w / 2 + sgn * k * h / 2, y])
            dst.append([xm + w / 2 + sgn * (1 - S) * k * h / 2, y])
    H = cv2.getPerspectiveTransform(np.float32(src), np.float32(dst))
    corners = cv2.perspectiveTransform(np.float32([[[0, 0]], [[w, 0]], [[w, h]], [[0, h]]]), H)[:, 0]
    out = cv2.warpPerspective(rgb, H, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT)
    x0 = max(corners[0, 0], corners[3, 0], 0)
    x1 = min(corners[1, 0], corners[2, 0], w)
    y0 = max(corners[0, 1], corners[1, 1], 0)
    y1 = min(corners[2, 1], corners[3, 1], h)
    x0, y0, x1, y1 = int(np.ceil(x0)) + 2, int(np.ceil(y0)) + 2, int(x1) - 2, int(y1) - 2
    deg = lambda k: float(np.degrees(np.arctan(k)))
    return out[y0:y1, x0:x1], deg(k0 - k1 * w / 2), deg(k0 + k1 * w / 2)


def crop34(im, cx, cy, zoom):
    w, h = im.size
    cw = min(w, h * 3 / 4) / zoom
    ch = cw * 4 / 3
    left = min(max(cx * w - cw / 2, 0), w - cw)
    top = min(max(cy * h - ch / 2, 0), h - ch)
    return im.crop((round(left), round(top), round(left + cw), round(top + ch)))


def tone(im):
    # Tonwerte nur auf der Helligkeit strecken. ImageOps.autocontrast(preserve_tone=True) wendet die Kurve
    # auf jeden Kanal an und verstärkt so einen vorhandenen Gelbstich (Blau wird stärker abgesenkt).
    y, cb, cr = im.convert("YCbCr").split()
    im = Image.merge("YCbCr", (ImageOps.autocontrast(y, cutoff=0.4), cb, cr)).convert("RGB")
    im = ImageEnhance.Color(im).enhance(1.04)
    # Gelbstich moderat neutralisieren (nur wenn deutlich): Blau/Grün halb Richtung Grauwelt ziehen
    arr = np.asarray(im).astype(np.float32)
    r, g, b = arr[..., 0].mean(), arr[..., 1].mean(), arr[..., 2].mean()
    if b < 0.9 * r:
        gray = (r + g + b) / 3
        f = np.array([1 + 0.5 * (gray / r - 1), 1 + 0.5 * (gray / g - 1), 1 + 0.5 * (gray / b - 1)])
        arr = np.clip(arr * f, 0, 255)
        im = Image.fromarray(arr.astype(np.uint8))
    return im


def process(name, file, cx, cy, zoom):
    im = ImageOps.exif_transpose(Image.open(SRC / file)).convert("RGB")  # neues Bild ohne Metadaten
    arr, tl, tr = straighten(np.asarray(im))
    im = crop34(Image.fromarray(arr), cx, cy, zoom)
    im = tone(im)
    widths = []
    for wanted in (600, 1200):
        wd = min(wanted, im.width)
        out = im.resize((wd, round(wd * 4 / 3)), Image.LANCZOS)
        out.save(OUT / f"{name}-{wd}.webp", "WEBP", quality=78, method=6)
        widths.append(wd)
    print(f"{name:24s} {file[-12:]}  Neigung links {tl:+.1f}° rechts {tr:+.1f}°  -> {widths}")
    return widths


if __name__ == "__main__":
    only = set(sys.argv[1:])
    for p in PICKS:
        if not only or p[0] in only:
            process(*p)
