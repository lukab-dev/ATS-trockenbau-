"""Erklär-Zeichnungen der Leistungsseiten: Wand, Dachschräge, Kernsanierung.

Ein Stil für alle drei: feine Linien wie im Werkplan, flache Flächen, nummerierte Marken,
die zur Schrittliste daneben gehören. Jede Gruppe mit data-s="n" erscheint mit Schritt n.
"""
import math

W, H = 640, 440


def _wrap(label, body):
    return (f'<svg class="xp" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">'
            '<defs><pattern id="xh" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            '<line x1="0" y1="0" x2="0" y2="8" class="hl"/></pattern></defs>' + body + "</svg>")


def _badge(n, x, y):
    return (f'<g class="bg" data-s="{n}"><circle cx="{x:.1f}" cy="{y:.1f}" r="12"/>'
            f'<text x="{x:.1f}" y="{y + 4.2:.1f}" text-anchor="middle">{n}</text></g>')


def _zig(x0, x1, y0, y1, step, vertical=True):
    pts, i = [], 0
    if vertical:
        y = y0
        while y <= y1 + .01:
            pts.append(f"{x0 if i % 2 == 0 else x1:.1f},{y:.1f}"); y += step; i += 1
    else:
        x = x0
        while x <= x1 + .01:
            pts.append(f"{x:.1f},{y0 if i % 2 == 0 else y1:.1f}"); x += step; i += 1
    return f'<polyline class="ln dr wo" pathLength="1" points="{" ".join(pts)}"/>'


def _g(n, inner):
    return f'<g data-s="{n}">{inner}</g>'


def wall():
    studs = [50, 185, 320, 455, 582]
    base = ('<rect x="20" y="24" width="600" height="26" fill="url(#xh)"/><rect x="20" y="390" width="600" height="26" fill="url(#xh)"/>'
            '<line class="ln" x1="20" y1="50" x2="620" y2="50"/><line class="ln" x1="20" y1="390" x2="620" y2="390"/>')
    s1 = ('<rect class="ln dr" pathLength="1" x="50" y="50" width="540" height="8"/><rect class="ln dr" pathLength="1" x="50" y="382" width="540" height="8"/>'
          + "".join(f'<rect class="ln dr" pathLength="1" x="{x}" y="58" width="8" height="324"/>' for x in studs)
          + '<g class="mk"><path class="ln" d="M54 96H189M50 100l8-8M185 100l8-8"/><text x="121.5" y="88" text-anchor="middle">62,5 cm</text></g>')
    s2 = "".join(_zig(studs[i] + 18, studs[i + 1] - 10, 68, 374, 15.3) for i in range(4))
    cut = lambda y: 480 - 40 * (y - 50) / 340
    screws = [(x, y) for x in (54, 189, 314, 326, 459) for y in range(80, 380, 56) if x < cut(y) - 8]
    s3 = ('<rect class="ln dr bd" pathLength="1" x="50" y="50" width="270" height="340"/>'
          '<polygon class="ln dr bd" pathLength="1" points="320,50 480,50 440,390 320,390"/>'
          + "".join(f'<circle class="sc" cx="{x}" cy="{y}" r="2"/>' for x, y in screws))
    s4 = ('<rect class="jf" x="306" y="51" width="28" height="338"/>'
          + "".join(f'<circle class="jf" cx="{x}" cy="{y}" r="4.5"/>' for x, y in screws if x not in (314, 326)))
    s5 = ('<polygon class="pt" points="50,50 480,50 440,390 50,390"/>'
          '<rect class="ln dk" x="150" y="296" width="24" height="24" rx="3"/><circle class="dkf" cx="158" cy="308" r="1.6"/><circle class="dkf" cx="166" cy="308" r="1.6"/>')
    body = (base + _g(1, s1) + _g(2, s2) + _g(3, s3) + _g(4, s4) + _g(5, s5)
            + _badge(1, 586, 150) + _badge(2, 522, 230) + _badge(3, 400, 120) + _badge(4, 320, 250) + _badge(5, 140, 200))
    return _wrap("Zeichnung einer Trockenbauwand, die in fünf Schritten entsteht: Ständerwerk, Dämmung, Beplankung, Spachteln, fertige Fläche", body)


def roof():
    a = math.radians(-18); cx, cy = 320, 220; dy0 = 40

    def rot(x, y):
        dx, dy = x - cx, y - cy
        return cx + dx * math.cos(a) - dy * math.sin(a), cy + dx * math.sin(a) + dy * math.cos(a) + dy0

    rafters = [-210, -10, 190, 390, 590, 790]
    tiles = "".join(f'<path class="ln dm" d="M{x} 120q22-15 44 0"/>' for x in range(-124, 800, 44))
    base = (tiles + '<line class="ln dm" x1="-120" y1="127" x2="800" y2="127"/><line class="ln dm da" x1="-120" y1="134" x2="800" y2="134"/>'
            + "".join(f'<rect class="ln bd" x="{x}" y="138" width="36" height="100"/><path class="ln dm" d="M{x} 138l36 100M{x + 36} 138l-36 100"/>' for x in rafters))
    s1 = "".join(_zig(rafters[i] + 44, rafters[i + 1] - 8, 148, 228, 13.2, vertical=False) for i in range(5))
    s2 = '<line class="ln mb" x1="-120" y1="243" x2="800" y2="243"/><rect class="tp" x="292" y="239.5" width="30" height="7"/>'
    s3 = "".join(f'<rect class="ln dr bd" pathLength="1" x="{x}" y="248" width="34" height="14"/>' for x in range(-110, 800, 125))
    s4 = '<rect class="ln dr bd" pathLength="1" x="-120" y="264" width="920" height="14"/><line class="ln" x1="332" y1="264" x2="332" y2="278"/>'
    s5 = '<rect class="pt" x="-120" y="279.5" width="920" height="5"/>'
    body = ('<text class="nt" x="28" y="44">außen</text><text class="nt" x="612" y="412" text-anchor="end">innen</text>'
            f'<g transform="translate(0 {dy0}) rotate(-18 {cx} {cy})">' + base + _g(1, s1) + _g(2, s2) + _g(3, s3) + _g(4, s4) + _g(5, s5) + "</g>"
            + "".join(_badge(n, *rot(x, y)) for n, x, y in ((1, 308, 188), (2, 120, 243), (3, 282, 255), (4, 450, 271), (5, 575, 282))))
    return _wrap("Schnitt durch eine Dachschräge, die in fünf Schritten ausgebaut wird: Dämmung, Dampfbremse, Unterkonstruktion, Beplankung, fertige Oberfläche", body)


def reno():
    base = ('<path fill="url(#xh)" fill-rule="evenodd" d="M30 30H610V410H30ZM70 66H570V372H70Z"/>'
            '<rect class="ln" x="30" y="30" width="580" height="380"/><rect class="ln" x="70" y="66" width="500" height="306"/>')
    old = ('<g data-old><rect class="ln" x="236" y="66" width="12" height="306"/><line class="ln" x1="70" y1="364" x2="570" y2="364"/>'
           '<rect class="ln" x="462" y="296" width="78" height="52"/><path class="ln" d="M475 296v52M488 296v52M501 296v52M514 296v52M527 296v52M470 348v16M532 348v16"/>'
           '<path class="ln" d="M340 66v32"/><circle class="ln" cx="340" cy="108" r="10"/>'
           '<path class="ln" d="M70 250h34v26h-34M104 263h14v101"/></g>')
    s2 = ('<polyline class="ln dr" pathLength="1" points="80,372 80,250 100,250"/><polyline class="ln dr" pathLength="1" points="87,372 87,258 100,258"/>'
          '<polyline class="ln dr" pathLength="1" points="95,372 95,330 100,330"/>'
          '<polyline class="ln dr" pathLength="1" points="100,78 540,78 540,300"/>'
          '<path class="ln dr" pathLength="1" d="M180 78v16M300 78v16M480 78v16"/><rect class="ln" x="532" y="300" width="16" height="16"/>')
    s3 = ('<rect class="ln dr bd" pathLength="1" x="70" y="96" width="500" height="6"/>'
          '<path class="ln dm" d="M130 66v30M230 66v30M330 66v30M430 66v30M530 66v30"/>'
          '<rect class="ln dr bd" pathLength="1" x="102" y="102" width="8" height="262"/>'
          '<rect class="ln dr bd" pathLength="1" x="376" y="102" width="10" height="262"/>'
          '<path class="ln dm" d="M376 150h10M376 210h10M376 270h10M376 330h10"/>')
    s4 = (_zig(110, 376, 356, 364, 9, vertical=False) + _zig(386, 570, 356, 364, 9, vertical=False)
          + '<rect class="jf" x="110" y="350" width="266" height="4"/><rect class="jf" x="386" y="350" width="184" height="4"/>')
    s5 = ('<rect class="pt" x="110" y="102" width="266" height="248"/><rect class="pt" x="386" y="102" width="184" height="248"/>'
          '<circle class="lt" cx="180" cy="105" r="4"/><circle class="lt" cx="300" cy="105" r="4"/><circle class="lt" cx="480" cy="105" r="4"/>'
          '<rect class="ln dk" x="532" y="300" width="16" height="16" rx="2"/>'
          '<path class="ln dk" d="M110 250h36v10h-36M128 260v14"/>')
    body = (base + old + _g(2, s2) + _g(3, s3) + _g(4, s4) + _g(5, s5)
            + _badge(1, 242, 190) + _badge(2, 540, 180) + _badge(3, 381, 230) + _badge(4, 250, 357) + _badge(5, 470, 230))
    return _wrap("Schnitt durch einen Raum, der in fünf Schritten kernsaniert wird: Rückbau, Installationen, Wände und Decken, Böden, fertige Oberflächen", body)
