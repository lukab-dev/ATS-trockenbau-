"""Erklär-Zeichnungen der Leistungsseiten: Wand, Dachschräge, Kernsanierung.

Ein Stil für alle drei: flache, gefüllte Materialien (Stahl, Mineralwolle, Gipsplatte, Holz) und
beschriftete Marken, die zur Schrittliste daneben gehören. Jede Gruppe mit data-s="n" erscheint
mit Schritt n. Der Endzustand ist ein Schnittbild, in dem alle Schichten sichtbar bleiben.
"""
import math

W, H = 640, 440
STEEL, STEEL_E = "#b3bbbf", "#7f878b"
BOARD, BOARD_E = "#cbc8bf", "#9d9a90"
FILL, PAINT = "#e3e0d7", "#f3f1ea"
WOOD, WOOD_E = "#b98d5f", "#8a6540"
CONC = "#2b2a27"


def _wrap(label, body):
    defs = ('<defs>'
            '<pattern id="xh" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<rect width="9" height="9" fill="{CONC}"/><line x1="0" y1="0" x2="0" y2="9" stroke="#3d3c37" stroke-width="2"/></pattern>'
            '<pattern id="xw" width="22" height="12" patternUnits="userSpaceOnUse">'
            '<rect width="22" height="12" fill="#c2a55a"/><path d="M0 6c4-5 7-5 11 0s7 5 11 0" fill="none" stroke="#a48840" stroke-width="1.3"/></pattern>'
            '<pattern id="xg" width="7" height="40" patternUnits="userSpaceOnUse">'
            f'<rect width="7" height="40" fill="{WOOD}"/><path d="M3.5 0c1 12-1 26 0 40" fill="none" stroke="{WOOD_E}" stroke-width=".8" opacity=".55"/></pattern>'
            '</defs>')
    return f'<svg class="xp" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">{defs}{body}</svg>'


def _chip(n, x, y, label, to=None, cls=""):
    w = 34 + len(label) * 7.6 + 16
    lead = ""
    if to:
        lead = f'<line class="ld" x1="{x:.1f}" y1="{y:.1f}" x2="{to[0]:.1f}" y2="{to[1]:.1f}"/><circle class="ldd" cx="{to[0]:.1f}" cy="{to[1]:.1f}" r="3.2"/>'
    return (f'<g class="bg{" " + cls if cls else ""}" data-s="{n}">{lead}'
            f'<rect class="cb" x="{x - 14:.1f}" y="{y - 14:.1f}" width="{w:.1f}" height="28" rx="14"/>'
            f'<circle class="cc" cx="{x:.1f}" cy="{y:.1f}" r="14"/>'
            f'<text class="cn" x="{x:.1f}" y="{y + 5:.1f}" text-anchor="middle">{n}</text>'
            f'<text class="ct" x="{x + 22:.1f}" y="{y + 4.5:.1f}">{label}</text></g>')


def _ly(n, how, inner):
    return f'<g class="ly {how}" data-s="{n}">{inner}</g>'


def wall():
    studs = [40 + i * 110.4 for i in range(6)]
    base = ('<rect x="10" y="20" width="620" height="32" fill="url(#xh)"/><rect x="10" y="388" width="620" height="32" fill="url(#xh)"/>'
            '<path class="ed" d="M10 52H630M10 388H630"/>')
    st = f'fill="{STEEL}" stroke="{STEEL_E}" stroke-width=".8"'
    s1 = (f'<rect x="40" y="52" width="560" height="7" {st}/><rect x="40" y="381" width="560" height="7" {st}/>'
          + "".join(f'<rect x="{x:.1f}" y="59" width="8" height="322" {st}/><line x1="{x + 2.5:.1f}" y1="60" x2="{x + 2.5:.1f}" y2="380" stroke="#dfe4e6" stroke-width="1"/>' for x in studs)
          + f'<g class="mk"><path d="M{studs[4] + 4:.1f} 112H{studs[5] + 4:.1f}M{studs[4]:.1f} 116l8-8M{studs[5]:.1f} 116l8-8"/>'
            f'<text x="{(studs[4] + studs[5]) / 2 + 4:.1f}" y="103" text-anchor="middle">62,5 cm</text></g>')
    s2 = "".join(f'<rect x="{studs[i] + 8:.1f}" y="59" width="102.4" height="322" fill="url(#xw)"/>' for i in range(4))
    cut = lambda y: 400 - 20 * (y - 52) / 336
    screws = [(x, y) for x in (44, 154.4, 259.3, 270.3, 375.2) for y in range(84, 380, 50) if x < cut(y) - 6]
    bd = f'fill="{BOARD}" stroke="{BOARD_E}" stroke-width="1"'
    s3 = (f'<rect x="40" y="52" width="224.8" height="336" {bd}/><polygon points="264.8,52 400,52 380,388 264.8,388" {bd}/>'
          + "".join(f'<circle cx="{x}" cy="{y}" r="2.1" fill="#6f6c64"/>' for x, y in screws))
    s4 = (f'<rect x="249.8" y="52.5" width="30" height="335" fill="{FILL}"/><line x1="264.8" y1="53" x2="264.8" y2="387" stroke="#cfccc2" stroke-width="1" stroke-dasharray="2 5"/>'
          + "".join(f'<circle cx="{x}" cy="{y}" r="5.5" fill="{FILL}"/>' for x, y in screws if x < 160))
    s5 = (f'<polygon points="40,52 236,52 216,388 40,388" fill="{PAINT}"/><path d="M236 52L216 388" stroke="#bfbcb2" stroke-width="1.2"/>'
          '<rect x="104" y="318" width="26" height="26" rx="4" fill="#fbfaf6" stroke="#c9c6bd"/><circle cx="112.5" cy="331" r="1.8" fill="#9d9a90"/><circle cx="121.5" cy="331" r="1.8" fill="#9d9a90"/>')
    body = (base + _ly(1, "up", s1) + _ly(2, "dn", s2) + _ly(3, "rt", s3) + _ly(4, "dn", s4) + _ly(5, "rt", s5)
            + _chip(1, 502, 250, "Ständerwerk") + _chip(2, 396, 320, "Dämmung") + _chip(3, 288, 130, "Beplankung")
            + _chip(4, 264.8, 232, "Spachteln") + _chip(5, 66, 180, "Fertige Fläche"))
    return _wrap("Schnittbild einer Trockenbauwand mit fünf Schichten von rechts nach links: Ständerwerk, Dämmung, Beplankung, gespachtelte Fuge, fertige Fläche", body)


def roof():
    a = math.radians(-18); c, s = math.cos(a), math.sin(a); cx, cy, dy0 = 320, 205, 30

    def rot(x, y):
        dx, dy = x - cx, y - cy
        return cx + dx * c - dy * s, cy + dx * s + dy * c + dy0

    def at(xf, ly):  # Punkt auf Schicht-Höhe ly, der im Bild bei x = xf liegt
        return rot(cx + (xf - cx + (ly - cy) * s) / c, ly)

    rafters = [-240, -30, 180, 390, 600, 810]
    tiles = "".join(f'<path d="M{x} 112q24-20 50 0v6h-50z" fill="#45433e" stroke="#5d5b54" stroke-width="1"/>' for x in range(-150, 860, 48))
    base = (tiles + '<rect x="-150" y="118" width="1000" height="5" fill="#5d5b54"/><line x1="-150" y1="127" x2="850" y2="127" stroke="#8a877e" stroke-width="1.2" stroke-dasharray="7 5"/>'
            + "".join(f'<rect x="{x}" y="130" width="40" height="108" fill="url(#xg)" stroke="{WOOD_E}" stroke-width="1"/>' for x in rafters))
    s1 = "".join(f'<rect x="{rafters[i] + 40}" y="134" width="170" height="104" fill="url(#xw)"/>' for i in range(5))
    s2 = ('<rect x="-150" y="239.5" width="1000" height="4.5" fill="#7fb0bd"/><rect x="250" y="238" width="36" height="7.5" rx="1" fill="#d7eef3"/>'
          '<rect x="640" y="238" width="36" height="7.5" rx="1" fill="#d7eef3"/>')
    s3 = "".join(f'<rect x="{x}" y="246" width="42" height="18" fill="#cfa77a" stroke="{WOOD_E}" stroke-width="1"/>' for x in range(-110, 860, 125))
    s4 = (f'<rect x="-150" y="265.5" width="1000" height="16" fill="{BOARD}" stroke="{BOARD_E}" stroke-width="1"/>'
          f'<line x1="268" y1="265.5" x2="268" y2="281.5" stroke="{BOARD_E}" stroke-width="1.2"/>')
    s5 = f'<rect x="-150" y="282" width="1000" height="6.5" fill="{PAINT}"/>'
    chips = _chip(1, *rot(196, 186), "Dämmung")
    for n, xf, ycp, ly, label in ((5, 478, 322, 285, "Oberfläche"), (4, 436, 352, 273.5, "Beplankung"),
                                   (2, 356, 382, 241.7, "Dampfbremse"), (3, 0, 412, 255, "Unterkonstruktion")):
        if n == 3:  # auf eine Latte zeigen
            xf = rot(-110 + 125 * 3 + 21, 255)[0]
        chips += _chip(n, xf, ycp, label, to=at(xf, ly))
    body = ('<text class="nt" x="24" y="38">außen</text><text class="nt" x="616" y="424" text-anchor="end">innen</text>'
            f'<g transform="translate(0 {dy0}) rotate(-18 {cx} {cy})">' + base + _ly(1, "dn", s1) + _ly(2, "rt", s2)
            + _ly(3, "rt", s3) + _ly(4, "rt", s4) + _ly(5, "rt", s5) + "</g>" + chips)
    return _wrap("Schnitt durch eine ausgebaute Dachschräge von außen nach innen: Dachziegel, Sparren mit Dämmung, Dampfbremse, Unterkonstruktion, Beplankung, fertige Oberfläche", body)


def reno():
    base = ('<path fill="url(#xh)" fill-rule="evenodd" d="M20 20H620V420H20ZM64 60H576V376H64Z"/>'
            '<path class="ed" d="M20 20H620V420H20ZM64 60H576V376H64Z"/>')
    o = 'fill="#57554f" stroke="#7d7a72" stroke-width="1"'
    old = (f'<g data-old><rect x="250" y="60" width="14" height="316" {o}/><rect x="64" y="367" width="512" height="9" fill="#6d5c47" stroke="#8a7760" stroke-width="1"/>'
           f'<rect x="470" y="296" width="82" height="56" rx="3" {o}/><path d="M484 296v56M497 296v56M510 296v56M523 296v56M536 296v56" stroke="#7d7a72" stroke-width="1" fill="none"/>'
           f'<rect x="478" y="352" width="5" height="15" {o}/><rect x="539" y="352" width="5" height="15" {o}/>'
           f'<rect x="348" y="60" width="4" height="30" {o}/><circle cx="350" cy="100" r="11" {o}/>'
           f'<rect x="64" y="250" width="38" height="13" rx="2" {o}/><rect x="80" y="263" width="5" height="104" {o}/></g>')
    wt, el = 'fill="none" stroke="#7fb0bd" stroke-width="3.2" stroke-linejoin="round"', 'fill="none" stroke="#e08a4a" stroke-width="2.4" stroke-linejoin="round"'
    s2 = (f'<path d="M76 376V242H100" {wt}/><path d="M87 376V256H100" {wt}/><path d="M98 376V332" fill="none" stroke="#9d9a90" stroke-width="5"/>'
          f'<path d="M104 80H520M383 80V300M180 80V98M300 80V98M480 80V98" {el}/>'
          '<circle cx="383" cy="80" r="4.5" fill="#e08a4a"/><rect x="379" y="294" width="8" height="12" fill="#e08a4a"/>')
    bd = f'fill="{BOARD}" stroke="{BOARD_E}" stroke-width=".8"'
    s3 = ("".join(f'<rect x="{x}" y="60" width="2.4" height="40" fill="{STEEL}"/>' for x in (130, 230, 330, 430, 530))
          + f'<rect x="64" y="100" width="512" height="7" {bd}/><rect x="104" y="107" width="8" height="269" {bd}/>'
          + f'<rect x="375" y="107" width="5" height="269" {bd}/><rect x="386" y="107" width="5" height="269" {bd}/>'
          + "".join(f'<rect x="380" y="{y}" width="6" height="3" fill="{STEEL}"/>' for y in (107, 180, 250, 373)))
    s4 = "".join(f'<rect x="{x}" y="366" width="{w}" height="10" fill="url(#xw)"/><rect x="{x}" y="358" width="{w}" height="8" fill="#8f8c82"/>'
                 f'<rect x="{x}" y="353" width="{w}" height="5" fill="{WOOD}"/>' for x, w in ((112, 263), (391, 185)))
    s5 = (f'<rect x="112" y="107" width="263" height="246" fill="{PAINT}"/><rect x="391" y="107" width="185" height="246" fill="{PAINT}"/>'
          + "".join(f'<polygon points="{x - 7},107 {x + 7},107 {x + 58},353 {x - 58},353" fill="#f0d98a" opacity=".2"/>'
                    f'<rect x="{x - 8}" y="105" width="16" height="5" rx="2" fill="#dcbc5e"/>' for x in (180, 300, 480))
          + '<rect x="391" y="292" width="5" height="16" rx="1" fill="#9d9a90"/>'
          '<rect x="112" y="240" width="40" height="10" rx="2" fill="#fbfaf6" stroke="#bdb9ae"/><rect x="118" y="250" width="5" height="14" fill="#bdb9ae"/>'
          '<rect x="112" y="150" width="4" height="60" fill="#c5dfe6"/>')
    body = (base + old + _ly(2, "rt", s2) + _ly(3, "dn", s3) + _ly(4, "rt", s4) + _ly(5, "dn", s5)
            + _chip(1, 257, 200, "Rückbau", cls="ob") + _chip(2, 200, 150, "Installationen", to=(200, 80))
            + _chip(3, 383, 215, "Wände und Decken") + _chip(4, 190, 364, "Böden") + _chip(5, 440, 270, "Oberflächen"))
    return _wrap("Schnitt durch zwei kernsanierte Räume: neue Leitungen in Decke und Wand, neue Wände und abgehängte Decke, neuer Bodenaufbau, fertige Oberflächen", body)
