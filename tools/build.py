#!/usr/bin/env python3
"""Erzeugt alle HTML-Seiten von atstrockenbau.com.

Kopf, Navigation, Kontaktbereich und Fuß stehen hier genau einmal und landen
in jeder Seite. Aufruf im Projektordner:  python3 tools/build.py
Die erzeugten .html-Dateien werden mit eingecheckt; GitHub Pages braucht keinen Build.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import drawings  # noqa: E402
from html import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent
PART = ROOT / "tools" / "partials"
SITE = "https://atstrockenbau.com/"
TEL = "+4917624142472"
TEL_TXT = "0176 24142472"
MAIL = "info@atstrockenbau.com"
WA = "https://wa.me/4917624142472?text=Hallo%20ATS%20Trockenbau%2C%20ich%20habe%20eine%20Anfrage%3A%20"
MAPS = "https://maps.app.goo.gl/Ezn3jDMWya7vSVKD6"
TRUST = "https://trustlocal.de/bayern/augsburg/trockenbauer/ats-trockenbau/"
INSTA = "https://www.instagram.com/atstrockenbau/"
ENDPOINT = "https://script.google.com/macros/s/AKfycbwngl3Et6BfFfZKfRIKbPxXA-DeIiUj3oE42NermPm-164dwrAZ7GG8veVldZRNOR8a/exec"
CTA = "Besichtigung anfragen"

ICO_TEL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6.6 3.5h2.6l1.4 4-2 1.4a11 11 0 0 0 6.5 6.5l1.4-2 4 1.4v2.6a2 2 0 0 1-2.2 2A17 17 0 0 1 4.6 5.7a2 2 0 0 1 2-2.2z"/></svg>'
ICO_WA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4.5 19.5l1.2-3.6A8 8 0 1 1 8.6 18.6z"/><path d="M9 9.2c.2 1.7 2.1 3.8 4 4.3l1-1 1.6.8c-.2 1-1 1.6-2 1.5-2.7-.3-5.6-3.2-5.8-5.9-.1-1 .5-1.8 1.5-2l.8 1.6z" fill="currentColor" stroke="none"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17L17 7M8 7h9v9"/></svg>'
ICO = {
    "decke": '<path d="M2 4h20M6 4v5M12 4v5M18 4v5M3 9h18"/><path d="M12 13v2.5M8.5 20h7l-1-3h-5z"/>',
    "brand": '<path d="M12 21c-3.9 0-6.5-2.6-6.5-6.1 0-3.7 3.1-5.6 3.8-9.4 2 1.6 2.8 3.5 2.8 5.3 1-.8 1.6-2 1.7-3.3 2.4 2 3 4.7 3 7.4 0 3.5-2.4 6.1-4.8 6.1z"/>',
    "schall": '<path d="M3 12h1.5M7 8.5v7M11 5v14M15 8v8M19 10.5v3M21 12h.5"/>',
    "vorsatz": '<rect x="3" y="3" width="7" height="18" rx="1.5"/><path d="M14 3v8a3 3 0 0 0 3 3h4M14 21v-3.5"/>',
    "spachtel": '<path d="M3.5 15.5l7.5-7.5 5 5-7.5 7.5H3.5z"/><path d="M14 6l3-3 4 4-3 3"/>',
    "boden": '<path d="M12 4L2 8.5l10 4.5 10-4.5z"/><path d="M2 12.5l10 4.5 10-4.5M2 16.5l10 4.5 10-4.5"/>',
    "maler": '<rect x="3" y="3.5" width="15" height="5" rx="1.5"/><path d="M18 6h2.5v5H11v3"/><rect x="9.5" y="14" width="3" height="7" rx="1"/>',
    "fassade": '<path d="M3 21h18M5 21V8l7-4.5L19 8v13"/><path d="M9 21v-5h6v5M8.5 10.5h2M13.5 10.5h2"/>',
}
STAR = '<svg viewBox="0 0 24 24"><path d="M12 2.8l2.8 5.9 6.4.8-4.7 4.4 1.2 6.4L12 17.2l-5.7 3.1 1.2-6.4-4.7-4.4 6.4-.8z"/></svg>'

# Fotos: name -> (kleine Breite, große Breite, Breite, Höhe der kleinen Datei)
IMG = {
    "hero-bad": (640, 930, 640, 800),
    "kern-vorher": (640, 1200, 640, 480),
    "kern-bau": (640, 1200, 640, 480),
    "kern-fertig": (640, 1125, 640, 853),
    "p-trennwand": (600, 1200, 600, 800),
    "p-dach-gkf": (600, 1200, 600, 800),
    "p-bad-schraege": (600, 1200, 600, 800),
    "p-install-1": (600, 1200, 600, 800),
    "p-install-2": (600, 1200, 600, 800),
    "p-dach-beplankt": (600, 1200, 600, 800),
    "p-dach-holz": (600, 1200, 600, 800),
    "van": (600, 768, 600, 484),
}
REAL_W = {"hero-bad": 900}  # tatsächliche Pixelbreite der großen Datei, falls abweichend
CAP = {
    "hero-bad": "Fertiges Bad im Dachgeschoss mit Einbauleuchten",
    "kern-vorher": "Bad im Dachgeschoss beim Rückbau",
    "kern-bau": "Dasselbe Bad, neu beplankt mit imprägnierten Platten",
    "kern-fertig": "Das fertige Bad mit Dusche und Wand-WC",
    "p-trennwand": "Trennwand mit Lichtband im Dachgeschoss",
    "p-dach-gkf": "Dachausbau mit Feuerschutzplatten",
    "p-bad-schraege": "Kleines Bad unter der Dachschräge, fertig",
    "p-install-1": "Installationswand: Unterkonstruktion, mit Laser ausgerichtet",
    "p-install-2": "Dieselbe Wand beplankt, mit Revisionsöffnungen",
    "p-dach-beplankt": "Dachgeschoss beplankt, bereit zum Spachteln",
    "p-dach-holz": "Holzkonstruktion und Beplankung unter dem Dach",
}

NAV = [("trockenbau.html", "Trockenbau"), ("dachausbau.html", "Dachausbau"),
       ("kernsanierung.html", "Kernsanierung"), ("index.html#projekte", "Projekte"),
       ("index.html#bewertungen", "Bewertungen"), ("index.html#faq", "FAQ")]


def img(name, sizes, alt=None, cls="", eager=False):
    s, l, w, h = IMG[name]
    alt = CAP.get(name, "") if alt is None else alt
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="assets/img/{name}-{s}.webp" srcset="assets/img/{name}-{s}.webp {s}w, '
            f'assets/img/{name}-{l}.webp {REAL_W.get(name, l)}w" sizes="{sizes}" width="{w}" height="{h}" '
            f'alt="{escape(alt)}" {load} decoding="async">')


def shot(name):
    cap = escape(CAP[name])
    l = IMG[name][1]
    return (f'<figure class="shot"><button type="button" class="shot-btn" data-full="assets/img/{name}-{l}.webp" '
            f'data-cap="{cap}" aria-label="Bild vergrößern: {cap}">{img(name, "(min-width: 48rem) 33vw, 50vw")}</button>'
            f'<figcaption>{cap}</figcaption></figure>')


def gallery(names, cols4=False):
    c = "gallery gallery--4" if cols4 else "gallery"
    return f'<div class="{c}">' + "".join(shot(n) for n in names) + "</div>"


def art(main, cap, sub):
    return (f'<div class="art"><figure class="art-main">{img(main, "(min-width: 62rem) 30rem, 100vw", eager=True)}<figcaption>{cap}</figcaption></figure>'
            f'<figure class="art-sub">{img(sub, "14rem", "")}</figure>'
            f'<div class="art-card"><b>5,0 <span class="stars" aria-hidden="true">{STAR * 5}</span></b><span>32 Bewertungen · Google, Trustlocal</span></div></div>')


def stats(items):
    return '<dl class="stats">' + "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in items) + "</dl>"


def cells(items):
    return '<ul class="cells">' + "".join(
        f'<li><svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICO[i]}</svg>'
        f'<h3>{t}</h3><p>{p}</p><span class="spec">{sp}</span></li>' for t, p, sp, i in items) + "</ul>"


def bento(names):
    return '<div class="bento">' + "".join(shot(n) for n in names) + "</div>"


def build_section(eyebrow, title, story, svg, note):
    items = "".join(f'<li class="story-item"><span class="story-num">{i}</span><h3>{t}</h3><p>{p}</p></li>'
                    for i, (t, p) in enumerate(story, 1))
    return f'''<section class="build on-dark" aria-labelledby="build-title">
    <div class="build-stage">
      <div class="wrap">
        <div class="build-copy">
          <p class="eyebrow">{eyebrow}</p>
          <h2 id="build-title">{title}</h2>
          <ol class="story">{items}</ol>
          <div class="build-progress" aria-hidden="true"><i></i></div>
        </div>
        <figure class="build-visual">{svg}<figcaption class="build-note">{note}</figcaption></figure>
      </div>
    </div>
  </section>'''


def faq_html(items):
    return '<div class="faq">' + "".join(
        f'<details><summary>{q}</summary><div class="answer"><p>{a}</p></div></details>' for q, a in items) + "</div>"


def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def rows(items, one=False):
    out = []
    for it in items:
        spec = f'<span class="spec">{it[2]}</span>' if len(it) > 2 and it[2] else ""
        out.append(f"<li><h3>{it[0]}</h3><p>{it[1]}</p>{spec}</li>")
    return f'<ul class="rows{" rows--one" if one else ""}">' + "".join(out) + "</ul>"


def steps(items, cols=False):
    return f'<ol class="steps{" steps--cols" if cols else ""}">' + "".join(
        f'<li><span class="num">{i:02d}</span><h3>{t}</h3><p>{p}</p></li>' for i, (t, p) in enumerate(items, 1)) + "</ol>"


def review(q, who, where):
    return f'<figure class="review"><blockquote><p>„{q}“</p></blockquote><figcaption><b>{who}</b><span>{where}</span></figcaption></figure>'


def quote(q, who, where):
    return (f'<section class="section section--tint"><div class="wrap"><figure class="quote"><p class="eyebrow">Kundenstimme</p><span class="stars" aria-hidden="true">{STAR * 5}</span>'
            f'<blockquote><p>„{q}“</p></blockquote><figcaption><b>{who}</b> · {where} · '
            f'<a class="link" href="index.html#bewertungen">Alle Bewertungen</a></figcaption></figure></div></section>')


def cta_actions():
    return (f'<div class="actions"><a class="btn" href="#kontakt">{CTA}</a>'
            f'<a class="btn btn--line" href="tel:{TEL}">{ICO_TEL}{TEL_TXT}</a></div>')


BUSINESS_LD = {
    "@context": "https://schema.org", "@type": "GeneralContractor", "@id": SITE + "#betrieb",
    "name": "ATS Trockenbau", "url": SITE, "logo": SITE + "assets/logo/ats-logo-gold.png",
    "image": SITE + "assets/img/og-ats-trockenbau.jpg",
    "description": "Trockenbau, Kernsanierung und Innenausbau schlüsselfertig aus einer Hand in Augsburg und 100 km Umkreis.",
    "telephone": "+49 176 24142472", "email": MAIL, "vatID": "DE359550560", "foundingDate": "2023-03-01",
    "numberOfEmployees": {"@type": "QuantitativeValue", "value": 4},
    "founder": {"@type": "Person", "name": "Milos Pekovic"},
    "address": {"@type": "PostalAddress", "streetAddress": "Droste-Hülshoff-Straße 26", "postalCode": "86157",
                "addressLocality": "Augsburg", "addressRegion": "Bayern", "addressCountry": "DE"},
    "areaServed": {"@type": "GeoCircle", "geoMidpoint": {"@type": "GeoCoordinates", "latitude": 48.3705, "longitude": 10.8978},
                   "geoRadius": 100000},
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                                   "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                                   "opens": "07:00", "closes": "17:00"}],
    "knowsAbout": ["Trockenbau", "Kernsanierung", "Dachgeschossausbau", "Brandschutz", "Akustikdecken",
                   "Spachtelarbeiten Q1–Q4", "Malerarbeiten"],
    "sameAs": [INSTA, TRUST, MAPS],
}


def service_ld(name, desc, url):
    return [{"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": name, "description": desc,
             "url": SITE + url, "provider": {"@id": SITE + "#betrieb"},
             "areaServed": {"@type": "City", "name": "Augsburg"}},
            {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Startseite", "item": SITE},
                {"@type": "ListItem", "position": 2, "name": name, "item": SITE + url}]}]


def header(current, legal=False):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a>' for h, t in NAV)
    items = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a></li>'
                    for h, t in [("index.html", "Startseite")] + NAV)
    kontakt = "index.html#kontakt" if legal else "#kontakt"
    return f'''<header class="site-header">
  <div class="bar">
    <a class="brand" href="index.html" aria-label="ATS Trockenbau – Startseite"><img src="assets/logo/ats-logo-gold.png" width="520" height="238" alt="ATS Trockenbau"></a>
    <nav class="nav-links" aria-label="Hauptnavigation">{links}</nav>
    <a class="btn btn--small" href="{kontakt}">Anfragen</a>
    <button class="menu-btn" type="button" aria-label="Menü" aria-expanded="false" aria-controls="menu"><span></span><span></span></button>
  </div>
</header>
<div class="menu on-dark" id="menu" inert>
  <ul>{items}</ul>
  <div class="menu-foot">
    <a class="btn" href="{kontakt}">{CTA}</a>
    <a class="btn btn--line" href="tel:{TEL}">{ICO_TEL}{TEL_TXT}</a>
  </div>
</div>'''


def contact(preselect):
    opts = ["Trockenbau (Wände, Decken)", "Dachausbau", "Kernsanierung", "Brand- oder Schallschutz",
            "Spachtel- oder Malerarbeiten", "Sonstiges"]
    options = "".join(f'<option{" selected" if o.startswith(preselect) else ""}>{o}</option>' for o in opts)
    return f'''<section class="contact" id="kontakt">
    <div class="wrap">
      <div class="panel on-dark">
        <div>
          <div class="head">
            <p class="eyebrow">Kontakt</p>
            <h2 class="h-l">Erzählen Sie uns von Ihrem Projekt.</h2>
            <p class="lead">Wir melden uns innerhalb von zwei Werktagen, oft früher, und vereinbaren eine kostenlose Besichtigung.</p>
          </div>
          <dl class="ways">
            <div><dt>Telefon</dt><dd><a href="tel:{TEL}">{TEL_TXT}</a></dd></div>
            <div><dt>WhatsApp</dt><dd><a href="{WA}" target="_blank" rel="noopener">Nachricht schreiben</a></dd></div>
            <div><dt>E-Mail</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd></div>
            <div><dt>Anschrift</dt><dd>Droste-Hülshoff-Straße 26<br>86157 Augsburg</dd></div>
            <div><dt>Erreichbar</dt><dd>Mo–Fr 07:00–17:00 Uhr</dd></div>
          </dl>
          <figure class="van">{img("van", "(min-width: 62rem) 24rem, 100vw", "Firmenwagen von ATS Trockenbau mit Logo")}</figure>
        </div>
        <form class="form" id="anfrage" novalidate data-mail="{MAIL}" data-endpoint="{ENDPOINT}">
          <h3>Anfrage senden</h3>
          <div class="hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
          <div class="field"><label for="f-type">Worum geht es?</label><select id="f-type" name="projekt">{options}</select></div>
          <div class="form-row">
            <div class="field"><label for="f-name">Name *</label><input id="f-name" name="name" autocomplete="name" required></div>
            <div class="field"><label for="f-phone">Telefon</label><input id="f-phone" name="telefon" type="tel" autocomplete="tel"></div>
          </div>
          <div class="form-row">
            <div class="field"><label for="f-mail">E-Mail *</label><input id="f-mail" name="email" type="email" autocomplete="email" required></div>
            <div class="field"><label for="f-plz">Ort der Baustelle</label><input id="f-plz" name="ort" placeholder="z. B. 86152 Augsburg"></div>
          </div>
          <div class="field"><label for="f-msg">Ihr Vorhaben *</label><textarea id="f-msg" name="nachricht" required placeholder="Was soll gebaut werden? Ungefähre Fläche in m², gewünschter Zeitraum."></textarea></div>
          <label class="check" for="f-ok"><input id="f-ok" name="datenschutz" type="checkbox" required><span>Ich bin einverstanden, dass meine Angaben zur Bearbeitung der Anfrage verwendet werden. Mehr in der <a href="datenschutz.html">Datenschutzerklärung</a>. *</span></label>
          <div><button class="btn" type="submit">Anfrage senden</button></div>
          <p class="form-status" id="form-status" role="status" aria-live="polite"></p>
        </form>
      </div>
    </div>
  </section>'''


def footer():
    return f'''<footer class="site-footer on-dark">
  <div class="wrap">
    <div class="foot-col">
      <img src="assets/logo/ats-logo-gold.png" width="520" height="238" alt="ATS Trockenbau">
      <span>Trockenbau, Dachausbau und Kernsanierung in Augsburg und 100 km Umkreis. Gegründet 2023, Erfahrung seit 2014, 4 Mitarbeiter.</span>
    </div>
    <div class="foot-col"><b>Leistungen</b><a href="trockenbau.html">Trockenbau</a><a href="dachausbau.html">Dachausbau</a><a href="kernsanierung.html">Kernsanierung</a><a href="index.html#leistungen">Alle Leistungen</a></div>
    <div class="foot-col"><b>Betrieb</b><a href="index.html#projekte">Projekte</a><a href="index.html#bewertungen">Bewertungen</a><a href="index.html#ablauf">Ablauf</a><a href="index.html#gebiet">Einsatzgebiet</a></div>
    <div class="foot-col"><b>Kontakt</b><a href="tel:{TEL}">{TEL_TXT}</a><a href="mailto:{MAIL}">{MAIL}</a><a href="{WA}" target="_blank" rel="noopener">WhatsApp</a><a href="{INSTA}" target="_blank" rel="noopener">Instagram</a><a href="{MAPS}" target="_blank" rel="noopener">Google Maps</a></div>
    <div class="foot-legal">
      <span>© <span id="year">2026</span> ATS Trockenbau · Inhaber Milos Pekovic</span>
      <nav aria-label="Rechtliches"><a href="impressum.html">Impressum</a><a href="datenschutz.html">Datenschutz</a></nav>
    </div>
  </div>
  <div class="foot-mark" aria-hidden="true"><img src="assets/logo/ats-ant-gold.png" width="600" height="366" alt="">ATS Trockenbau</div>
</footer>'''


DOCK = f'''<div class="dock" aria-label="Schnellkontakt">
  <a class="btn btn--line on-dark" href="tel:{TEL}">{ICO_TEL}Anrufen</a>
  <a class="btn btn--line on-dark" href="{WA}" target="_blank" rel="noopener">{ICO_WA}WhatsApp</a>
  <a class="btn" href="#kontakt">Anfragen</a>
</div>'''

LIGHTBOX = '''<dialog class="lightbox on-dark" id="lightbox" aria-label="Bildansicht">
  <button class="lb-close" type="button" aria-label="Schließen"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
  <button class="lb-nav lb-prev" type="button" aria-label="Vorheriges Bild"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"/></svg></button>
  <figure><img alt=""><figcaption></figcaption></figure>
  <button class="lb-nav lb-next" type="button" aria-label="Nächstes Bild"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 5l7 7-7 7"/></svg></button>
</dialog>'''


def page(file, title, desc, body, ld=(), current=None, legal=False):
    url = SITE + ("" if file == "index.html" else file)
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld)
    og = "" if legal else f'''<meta property="og:type" content="website">
<meta property="og:locale" content="de_DE">
<meta property="og:site_name" content="ATS Trockenbau">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}assets/img/og-ats-trockenbau.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
'''
    d = f'<meta name="description" content="{escape(desc)}">\n' if desc else ""
    extras = "" if legal else DOCK + "\n\n" + LIGHTBOX + "\n\n"
    html = f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
{d}<link rel="canonical" href="{url}">
{og}{lds}<meta name="theme-color" content="#121211">
<link rel="icon" href="assets/favicon-64.png" type="image/png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/archivo.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/style.css">
<script>document.documentElement.classList.add('js')</script>
</head>
<body>

{header(current, legal)}

{body}

{footer()}

{extras}<script src="assets/app.js" defer></script>
</body>
</html>
'''
    (ROOT / file).write_text(html, encoding="utf-8")
    print("geschrieben:", file, len(html))


# ------------------------------------------------------------------ Startseite
FAQ_HOME = [
    ("Was kostet die Besichtigung?", "Nichts. Wir kommen kostenlos zu Ihnen, nehmen Maß und besprechen, was Sie vorhaben. Danach erhalten Sie ein schriftliches Angebot, in dem jede Position nachvollziehbar aufgeführt ist."),
    ("Machen Sie auch Komplettsanierungen schlüsselfertig?", "Ja. Vom Abbruch und Abtransport über Wände, Decken und Böden bis zu Malerarbeiten und Fassade. Elektro und Sanitär übernehmen unsere Partner-Fachbetriebe, abgestimmt durch uns. Sie haben einen Ansprechpartner für alles."),
    ("Arbeiten Sie auch für Firmen und Hausverwaltungen?", "Ja. Wir arbeiten für Privatkunden, Firmen und Hausverwaltungen."),
    ("Wie weit fahren Sie?", "Wir arbeiten in Augsburg und im Umkreis von rund 100 km, also in ganz Schwaben und weiten Teilen Oberbayerns bis Ulm, München, Ingolstadt und ins Allgäu."),
    ("Wie wird abgerechnet?", "Kleinere Aufträge rechnen wir nach Fertigstellung ab. Bei größeren Projekten stellen wir Abschlagsrechnungen nach Baufortschritt."),
    ("Wie schnell melden Sie sich?", "Innerhalb von zwei Werktagen, oft schon am selben Tag. Am schnellsten erreichen Sie uns per Telefon oder WhatsApp."),
]
ABLAUF = [
    ("Anfrage", "Sie beschreiben Ihr Vorhaben per Formular, Telefon oder WhatsApp, gern mit Fotos oder Grundriss."),
    ("Besichtigung", "Wir kommen kostenlos vor Ort, nehmen Maß und klären Details wie Brand- oder Schallschutz."),
    ("Angebot", "Sie erhalten ein schriftliches Angebot mit klarer Leistungsbeschreibung und Termin."),
    ("Ausführung", "Sauber und termingerecht, mit Schutz von Boden und Möbeln. Abfall nehmen wir mit."),
    ("Abnahme", "Gemeinsame Begehung und Übergabe. Kleine Aufträge rechnen wir danach ab, größere in Abschlägen."),
]
MORE = [
    ("Abgehängte Decken", "Glatte Decken unter Altbau- oder Betondecken, mit Platz für Leitungen, Lüftung und Einbauleuchten.", "CD-Profil · Direktabhänger · Nonius", "decke"),
    ("Brandschutz", "Brandwände, Decken, Schächte und Stahlträgerbekleidungen bis F90 und darüber. Dazu Abschottungen für Kabel und Rohre, geschult bei ZAPP-ZIMMERMANN.", "F30 · F60 · F90 und höher", "brand"),
    ("Schall- und Akustikdecken", "Ruhe zwischen Räumen und bessere Sprachverständlichkeit in Büro, Praxis und Gastronomie.", "Lochplatten · Mineralfaser", "schall"),
    ("Vorsatzschalen und Installationswände", "Leitungen verschwinden hinter der Wand, alte Mauern werden gerade. Ideal für Bad und Küche.", "GKBI imprägniert für Feuchträume", "vorsatz"),
    ("Spachtel- und Oberflächenarbeiten", "Fugen, Kanten und Flächen streichfertig, von der Grundverspachtelung bis Q4.", "Q1 · Q2 · Q3 · Q4", "spachtel"),
    ("Böden und Trockenestrich", "Neue Böden und schnell belegbarer Trockenestrich ohne Trocknungszeit. Gut für Holzbalkendecken im Altbau.", "Unterböden · Trockenestrich · Beläge", "boden"),
    ("Maler- und Glättarbeiten", "Streichen, Spachteln und Glätten, damit die Räume nach dem Umbau fertig sind.", "Innenanstrich · Q3/Q4-Flächen", "maler"),
    ("Fassade", "Auch außen aus einer Hand: Arbeiten an der Fassade im Rahmen einer Sanierung.", "Sanierung · Anstrich", "fassade"),
]
REVIEWS = [
    ("Das Trockenbau-Team hat bei uns hervorragende Arbeit geleistet.", "Gabriel J.", "Google, Okt. 2026"),
    ("Herausragende Arbeit und absolute Zuverlässigkeit!", "S. D.", "Dachgeschossausbau · Google, Apr. 2026"),
    ("Super Arbeit, auch die kniffligere Seite mit 2 Dachschrägen wurde korrekt abgehängt.", "Matthias T.", "Badezimmerdecke · Google, Nov. 2025"),
    ("Wir hatten einen Plan von einer Innendesignerin und die Firma ATS hat sich sehr präzise an den Plan gehalten …", "Vivienne B.", "Wohnzimmer · Google, Nov. 2025"),
    ("Klasse Arbeit von Milos bei der Dämmung unseres Dachbodens, freundliches Team, gutes Preis-/Leistungsverhältnis.", "Rainer S.", "Dachbodendämmung · Trustlocal, Jan. 2026"),
    ("Zeitplan und Preis wurde wie besprochen eingehalten", "Tatjana G.", "Trustlocal, Aug. 2025"),
]


def tile(i, href, name, title, text):
    return (f'<a class="tile" href="{href}">{img(name, "(min-width: 48rem) 33vw, 100vw", "")}'
            f'<span class="go">{ARROW}</span>'
            f'<h3>{title}</h3><p>{text}</p><span class="more">Mehr erfahren</span></a>')


MARQUEE = ["Trennwände", "Abgehängte Decken", "Dachausbau", "Brandschutz F90", "Kernsanierung", "Spachteln bis Q4"]


def marquee():
    row = "".join(f"<span>{w}</span>" for w in MARQUEE)
    return f'<div class="marquee" aria-hidden="true"><div>{row}{row}</div></div>'


def home():
    body = f'''<main id="top">

  <section class="hero on-dark grain">
    <span class="dim-note" aria-hidden="true"><span>62,5</span></span>
    <div class="wrap">
      <div class="hero-grid">
        <div class="hero-copy">
          <h1 class="h-xl"><span class="eyebrow h1-kicker">Trockenbau &amp; Kernsanierung in Augsburg</span>Trockenbau, <span class="mark">der sitzt.</span></h1>
          <p class="lead">Trockenbau, Dachausbau und Kernsanierung, schlüsselfertig aus einer Hand. Für Privat, Gewerbe und Hausverwaltungen in Augsburg und 100 km Umkreis.</p>
          {cta_actions()}
        </div>
        {art("hero-bad", "Badsanierung im Dachgeschoss", "kern-bau")}
      </div>
      {stats([("Seit <em>2014</em>", "Erfahrung im Trockenbau"), ("<em>5,0</em> von 5", "bei 32 Bewertungen"), ("<em>100</em> km", "Umkreis um Augsburg"), ("<em>0</em> €", "kostet die Besichtigung")])}
    </div>
  </section>

  <section class="section" id="leistungen">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Leistungen</p>
        <h2 class="h-l">Drei Dinge machen wir am häufigsten.</h2>
      </div>
      <div class="trio">
        {tile(1, "trockenbau.html", "p-trennwand", "Trockenbau", "Trennwände, Decken, Vorsatzschalen und Brandschutz. Gespachtelt bis Q4.")}
        {tile(2, "dachausbau.html", "p-dach-gkf", "Dachausbau", "Dämmung, Dampfbremse und Verkleidung. Aus dem Speicher wird Wohnraum.")}
        {tile(3, "kernsanierung.html", "kern-fertig", "Kernsanierung", "Vom Abbruch bis zur schlüsselfertigen Übergabe, mit einem Ansprechpartner.")}
      </div>
    </div>
  </section>

  <section class="section section--tint">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Außerdem</p>
        <h2 class="h-l">Alles, was trocken gebaut wird.</h2>
        <p class="lead">Vom einzelnen Durchbruch im Altbau bis zum kompletten Büroausbau. Mit geprüften Systemen der bekannten Plattenhersteller.</p>
      </div>
      {cells(MORE)}
    </div>
  </section>

  <section class="section on-dark" id="projekte">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Projekte</p>
        <h2 class="h-l">Aus unseren Baustellen.</h2>
        <p class="lead">Echte Aufträge, vom Ständerwerk bis zur fertigen Fläche. Zum Vergrößern antippen.</p>
      </div>
      {bento(["p-trennwand", "p-bad-schraege", "p-dach-gkf", "p-install-2", "p-dach-beplankt"])}
      <p class="note">Mehr Bilder zeigen wir auf <a class="link link--arrow" href="{INSTA}" target="_blank" rel="noopener">Instagram @atstrockenbau</a></p>
    </div>
  </section>

  <section class="section" id="bewertungen">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Bewertungen</p>
        <h2 class="h-l">Was Kunden sagen.</h2>
      </div>
      <div class="rev">
        <div class="score on-dark">
          <span class="score-num">5,0</span>
          <span class="stars" aria-hidden="true">{STAR * 5}</span>
          <p>32 Bewertungen auf Google, MyHammer und Trustlocal. Top Score 2025 und 2026 auf Trustlocal.</p>
          <ul><li><a class="link link--arrow" href="{MAPS}" target="_blank" rel="noopener">Alle Bewertungen auf Google</a></li><li><a class="link link--arrow" href="{TRUST}" target="_blank" rel="noopener">Auf Trustlocal ansehen</a></li></ul>
        </div>
        <div class="reviews">{"".join(review(*r) for r in REVIEWS)}</div>
      </div>
      <p class="small">Auszüge aus öffentlichen Bewertungen, gekürzt, Namen abgekürzt. Gesamtwertung laut Trustlocal, Stand November 2026. Wir prüfen nicht selbst, ob jede Bewertung von einem Kunden stammt, der die Leistung genutzt hat.</p>
    </div>
  </section>

  <section class="section section--tint" id="ablauf">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Ablauf</p>
        <h2 class="h-l">Von der Anfrage bis zur Abnahme.</h2>
      </div>
      {steps(ABLAUF, cols=True)}
    </div>
  </section>

  <section class="section" id="gebiet">
    <div class="wrap area">
      <div>
        <div class="head">
          <p class="eyebrow">Einsatzgebiet</p>
          <h2 class="h-l">Augsburg und 100 km Umkreis.</h2>
          <p class="lead">Von Augsburg aus arbeiten wir in ganz Schwaben und weiten Teilen Oberbayerns.</p>
        </div>
        <p class="places"><b>Augsburg</b>, Friedberg, Königsbrunn, München, Dachau, Fürstenfeldbruck, Starnberg, Freising, Ingolstadt, Neuburg a. d. Donau, Schrobenhausen, Donauwörth, Dillingen, Günzburg, Ulm / Neu-Ulm, Landsberg am Lech, Mindelheim, Kaufbeuren, Memmingen, Kempten und Weilheim.</p>
      </div>
      <figure class="map">{(PART / "map.svg").read_text(encoding="utf-8")}</figure>
    </div>
  </section>

  <section class="section" id="faq">
    <div class="wrap split">
      <div class="head">
        <p class="eyebrow">Häufige Fragen</p>
        <h2 class="h-l">Gut zu wissen.</h2>
        <p class="lead">Fragen zu einer bestimmten Leistung beantworten wir auf den Seiten <a class="link" href="trockenbau.html#faq">Trockenbau</a>, <a class="link" href="dachausbau.html#faq">Dachausbau</a> und <a class="link" href="kernsanierung.html#faq">Kernsanierung</a>.</p>
      </div>
      {faq_html(FAQ_HOME)}
    </div>
  </section>

  {contact("Trockenbau")}

</main>'''
    page("index.html", "Trockenbau & Kernsanierung in Augsburg | ATS Trockenbau",
         "Trockenbau und Kernsanierung in Augsburg: Wände, Decken, Dachausbau, Brandschutz bis F90. Schlüsselfertig, kostenlose Besichtigung, 100 km Umkreis.",
         body, ld=[BUSINESS_LD, faq_ld(FAQ_HOME)], current="index.html")


# ------------------------------------------------------------------ Leistungsseiten
def service_hero(name, h1, lead, photo, caption, sub, st):
    return f'''<section class="hero on-dark grain">
    <span class="dim-note" aria-hidden="true"><span>62,5</span></span>
    <div class="wrap">
      <div class="hero-grid">
        <div class="hero-copy">
          <ol class="crumbs" aria-label="Sie sind hier"><li><a href="index.html">Startseite</a></li><li aria-current="page">{name}</li></ol>
          <h1 class="h-xl">{h1}</h1>
          <p class="lead">{lead}</p>
          {cta_actions()}
        </div>
        {art(photo, caption, sub)}
      </div>
      {stats(st)}
    </div>
  </section>'''


def faq_section(items, name):
    return f'''<section class="section" id="faq">
    <div class="wrap split">
      <div class="head">
        <p class="eyebrow">Häufige Fragen</p>
        <h2 class="h-l">Fragen zu {name}.</h2>
        <p class="lead">Ihre Frage ist nicht dabei? Rufen Sie an unter <a class="link" href="tel:{TEL}">{TEL_TXT}</a>.</p>
      </div>
      {faq_html(items)}
    </div>
  </section>'''


CROSS = {
    "trockenbau.html": ("p-trennwand", "Trockenbau", "Wände, Decken, Brandschutz, Spachteln bis Q4"),
    "dachausbau.html": ("p-dach-gkf", "Dachausbau", "Dämmung, Dampfbremse, Verkleidung"),
    "kernsanierung.html": ("kern-fertig", "Kernsanierung", "Schlüsselfertig vom Abbruch bis zur Übergabe"),
}


def cross(current):
    cards = "".join(
        f'<a href="{h}">{img(n, "6.5rem", "")}<span><b>{t}</b><span>{d}</span></span></a>'
        for h, (n, t, d) in CROSS.items() if h != current)
    return f'''<section class="section section--tint">
    <div class="wrap">
      <div class="head"><p class="eyebrow">Weitere Leistungen</p><h2 class="h-m">Das machen wir auch.</h2></div>
      <div class="cross">{cards}</div>
    </div>
  </section>'''


def q_swatch(i, scale, joint, screws):
    s = ""
    if screws:
        s = "".join(f'<circle cx="{x}" cy="{y}" r="3.2" fill="#d2cdc1"/>' for x in (100, 220) for y in (40, 110, 180, 250))
    return f'''<svg viewBox="0 0 300 300" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Wandfläche in Stufe Q{i} im Streiflicht">
<filter id="lit{i}" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.022 0.03" numOctaves="4" seed="{6 + i}"/><feDiffuseLighting lighting-color="#f3f0e8" surfaceScale="{scale}" diffuseConstant="1.05"><feDistantLight azimuth="180" elevation="28"/></feDiffuseLighting></filter>
<rect width="300" height="300" fill="#e8e5dd"/><rect width="300" height="300" filter="url(#lit{i})"/>
<g opacity="{joint}"><rect x="78" width="44" height="300" fill="#f7f5ef" opacity=".55"/><rect x="198" width="44" height="300" fill="#f7f5ef" opacity=".55"/><line x1="100" x2="100" y2="300" stroke="#c8c2b5" stroke-width="1.5"/><line x1="220" x2="220" y2="300" stroke="#c8c2b5" stroke-width="1.5"/></g>{s}</svg>'''


def trockenbau():
    faq = [
        ("Was kostet Trockenbau pro Quadratmeter?", "Das hängt vom Aufbau, der Fläche und der gewünschten Oberfläche ab. Nach der kostenlosen Besichtigung bekommen Sie ein schriftliches Angebot, in dem jede Position nachvollziehbar aufgeführt ist."),
        ("Wie lange dauert eine neue Trennwand?", "Eine einzelne Wand steht oft in wenigen Tagen, inklusive Spachteln. Den genauen Zeitplan finden Sie in unserem Angebot."),
        ("Wie viel Schmutz entsteht dabei?", "Trockenbau ist deutlich sauberer als Mauern und Putzen. Wir decken Böden und Möbel ab, nehmen den Schutt mit und übergeben die Baustelle besenrein."),
        ("Brauche ich eine Genehmigung für eine Trennwand?", "Für nichttragende Innenwände in der Regel nicht. In Mietwohnungen braucht es die Zustimmung des Vermieters. Bei Brandschutzanforderungen stimmen wir den Aufbau vorab mit Ihnen ab."),
        ("Kann ich an einer Trockenbauwand schwere Dinge aufhängen?", "Ja. Bilder und Regale halten mit Hohlraumdübeln. Für Hängeschränke, Waschtische oder Fernseher bauen wir an der richtigen Stelle Verstärkungen in die Wand ein. Sagen Sie uns bei der Besichtigung, was wohin soll."),
        ("Geht Trockenbau auch im Bad?", "Ja. In Feuchträumen verwenden wir imprägnierte Platten. Leitungen und Spülkästen verschwinden in einer Installationswand, Revisionsöffnungen halten sie zugänglich."),
        ("Welche Qualitätsstufe brauche ich?", "Q2 ist der Standard und reicht für Raufaser, grobe Tapeten und matte Farbe. Für feine Anstriche empfehlen wir Q3. Bei Glanzlack, Metalltapeten oder großen Fensterflächen mit Streiflicht lohnt sich Q4."),
        ("Wie gut ist der Schallschutz einer Trockenbauwand?", "Das hängt vom Aufbau ab. Mineralwolle im Hohlraum, doppelte Beplankung und entkoppelte Anschlüsse verbessern den Schallschutz deutlich. Wir schlagen den Aufbau passend zur Nutzung vor."),
    ]
    umfang = [
        ("Trenn- und Ständerwände", "Neue Raumaufteilung ohne Nassarbeiten. Einfach oder doppelt beplankt, mit Türzargen und Revisionsöffnungen.", "CW 50 · 75 · 100"),
        ("Abgehängte Decken", "Glatte Decken unter Altbau- oder Betondecken, mit Platz für Leitungen, Lüftung und Einbauleuchten.", "CD-Profil · Direktabhänger · Nonius"),
        ("Vorsatzschalen und Installationswände", "Leitungen verschwinden hinter der Wand, alte Mauern werden gerade. Ideal für Bad und Küche.", "GKBI imprägniert für Feuchträume"),
        ("Brandschutz", "Brandwände, Decken, Schächte und Stahlträgerbekleidungen bis F90 und darüber, dazu Abschottungen für Kabel und Rohre.", "F30 · F60 · F90 und höher"),
        ("Schall- und Akustikdecken", "Ruhe zwischen Räumen und bessere Sprachverständlichkeit in Büro, Praxis und Gastronomie.", "Lochplatten · Mineralfaser"),
        ("Spachteln und Malerarbeiten", "Fugen, Kanten und Flächen streichfertig oder fertig gestrichen, in der Stufe, die Sie brauchen.", "Q1 · Q2 · Q3 · Q4"),
    ]
    story = [
        ("Ständerwerk", "UW-Profile an Boden und Decke, CW-Ständer im Raster von 62,5 cm. Das Gerüst entscheidet, wie gerade die Wand wird."),
        ("Dämmung", "Mineralwolle zwischen den Ständern bringt Schallschutz und, je nach Aufbau, Brandschutz."),
        ("Beplankung", "Gipsplatten 12,5 mm, einfach oder doppelt verschraubt. Im Bad mit imprägnierten Platten."),
        ("Spachteln", "Fugen und Schraubköpfe werden gespachtelt und geschliffen, in der Qualitätsstufe, die Sie brauchen."),
        ("Fertig", "Eine glatte Fläche, bereit für Farbe, Tapete oder Fliesen. Übergabe besenrein."),
    ]
    q = [
        (1, "5.0", ".95", True, "Q1 · Grundverspachtelung", "Fugen gefüllt, Schraubköpfe überspachtelt. Beides bleibt im Licht sichtbar.", "Fliesen, weitere Verkleidung"),
        (2, "2.6", ".45", False, "Q2 · Standard", "Fugen nachgespachtelt und stufenlos an die Plattenfläche angeglichen.", "Raufaser, grobe Tapeten, matte Farbe"),
        (3, "1.2", ".18", False, "Q3 · Sonderverspachtelung", "Fugen breit ausgespachtelt, die ganze Fläche scharf abgezogen.", "Feine Tapeten, feine matte Anstriche"),
        (4, "0.35", "0", False, "Q4 · Vollflächig", "Die gesamte Fläche wird überzogen und geglättet. Keine Spuren, auch nicht im Streiflicht.", "Glanzlack, Metalltapete, große Fensterflächen"),
    ]
    q_html = "".join(f'<li>{q_swatch(i, sc, j, scr)}<h3>{t}</h3><p>{p}</p><p class="fit"><b>Geeignet für:</b> {fit}</p></li>'
                     for i, sc, j, scr, t, p, fit in q)
    desc = "Trockenbau in Augsburg: Trennwände, abgehängte Decken, Vorsatzschalen, Brandschutz bis F90 und Spachteln bis Q4. Kostenlose Besichtigung vor Ort."
    body = f'''<main id="top">

  {service_hero("Trockenbau", "Trockenbau <span class=\"mark\">in Augsburg.</span>", "Neue Wände, glatte Decken und saubere Oberflächen, ohne Nassarbeiten und ohne lange Trocknungszeit. Für Wohnung, Haus, Büro und Praxis.", "p-trennwand", "Trennwand mit Lichtband", "p-install-1", [("<em>Q1</em> bis <em>Q4</em>", "Oberflächen nach Wunsch"), ("Bis <em>F90</em>", "Brandschutz und höher"), ("<em>62,5</em> cm", "Ständerraster, mit Laser ausgerichtet"), ("<em>0</em> €", "kostet die Besichtigung")])}

  <section class="section section--tint">
    <div class="wrap split">
      <div class="head">
        <p class="eyebrow">Leistungsumfang</p>
        <h2 class="h-l">Was wir im Trockenbau machen.</h2>
        <p class="lead">Mit geprüften Systemen der bekannten Plattenhersteller. Brandschutz-Abschottungen geschult bei ZAPP-ZIMMERMANN.</p>
      </div>
      {rows(umfang, one=True)}
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Fotos von der Baustelle</p>
        <h2 class="h-l">So sieht das bei uns aus.</h2>
      </div>
      {gallery(["p-install-1", "p-install-2", "p-trennwand", "p-dach-beplankt"], cols4=True)}
    </div>
  </section>

  {build_section("So entsteht eine Wand", "In fünf Schritten zur fertigen Fläche.", story, drawings.wall(),
                  "<b>Was Sie am Ende sehen, ist nur die Oberfläche.</b> Wie gerade, ruhig und sicher die Wand ist, entscheiden die Schichten dahinter.")}

  <section class="section" id="qualitaet">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Oberflächen Q1 bis Q4</p>
        <h2 class="h-l">Wie glatt soll es werden?</h2>
        <p class="lead">Die Qualitätsstufen legen fest, wie eben eine Gipsplattenwand gespachtelt wird. So sehen die vier Stufen bei seitlichem Licht aus.</p>
      </div>
      <ul class="qgrid">{q_html}</ul>
      <p class="small">Simulation bei Streiflicht. Grundlage: Merkblatt Nr. 2 der Industriegruppe Gipsplatten.</p>
    </div>
  </section>

  {quote("Wir hatten einen Plan von einer Innendesignerin und die Firma ATS hat sich sehr präzise an den Plan gehalten …", "Vivienne B.", "Wohnzimmer, Google, Nov. 2025")}

  {faq_section(faq, "Trockenbau")}

  {cross("trockenbau.html")}

  {contact("Trockenbau")}

</main>'''
    page("trockenbau.html", "Trockenbau Augsburg: Wände, Decken, Brandschutz | ATS Trockenbau", desc, body,
         ld=service_ld("Trockenbau", desc, "trockenbau.html") + [faq_ld(faq)], current="trockenbau.html")


def dachausbau():
    faq = [
        ("Brauche ich für den Dachausbau eine Baugenehmigung?", "Das hängt vom Gebäude und der geplanten Nutzung ab. Wird aus einem Speicher Wohnraum, kann eine Genehmigung nötig sein. Fragen Sie früh beim Bauamt oder bei Ihrem Architekten nach. Wir richten den Ausbau nach den Vorgaben."),
        ("Was kostet ein Dachausbau?", "Das hängt von der Fläche, dem Zustand des Dachs und vom Umfang ab, zum Beispiel ob ein Bad dazukommt. Nach der kostenlosen Besichtigung erhalten Sie ein schriftliches Angebot mit allen Positionen."),
        ("Wie lange dauert ein Dachausbau?", "Das richtet sich nach Größe und Umfang. Reine Dämm- und Trockenbauarbeiten gehen deutlich schneller als ein Ausbau mit Bad und neuen Installationen. Den Zeitplan finden Sie in unserem Angebot."),
        ("Welche Dämmung verwenden Sie?", "Meist Mineralwolle zwischen den Sparren, bei Bedarf ergänzt durch eine zweite Lage darunter. Die Stärke richtet sich nach der Sparrenhöhe und den Anforderungen an den Wärmeschutz."),
        ("Warum ist die Dampfbremse so wichtig?", "Sie verhindert, dass feuchte Raumluft in die Dämmung zieht und dort zu Feuchteschäden führt. Wir verkleben alle Stöße und Anschlüsse luftdicht nach DIN 4108-7."),
        ("Kann unter dem Dach ein Bad entstehen?", "Ja. Wir bauen Installationswände, verkleiden die Schrägen mit imprägnierten Platten und stimmen Sanitär und Elektro mit unseren Partner-Fachbetrieben ab."),
        ("Dämmen Sie auch nur den Dachboden?", "Ja. Wenn der Speicher nicht bewohnt werden soll, dämmen wir die oberste Geschossdecke. Das ist oft die schnellste Art, Heizwärme im Haus zu halten."),
        ("Wie viel Schmutz entsteht im Rest des Hauses?", "Wir decken Treppenhaus und Laufwege ab und nehmen Abfall mit. Trockenbau kommt ohne Mörtel und Putz aus, das hält die Baustelle sauber."),
    ]
    umfang = [
        ("Dämmung zwischen den Sparren", "Mineralwolle, passgenau geklemmt, bei Bedarf mit einer zweiten Lage unter den Sparren.", "Zwischen- und Untersparrendämmung"),
        ("Dampfbremse", "Folie auf der warmen Seite, alle Stöße und Anschlüsse verklebt.", "Luftdicht nach DIN 4108-7"),
        ("Verkleidung von Schrägen und Kehlbalken", "Unterkonstruktion ausgerichtet, dann beplankt. Wo es gefordert ist, mit Feuerschutzplatten.", "GKB · GKF · GKBI"),
        ("Drempel, Trennwände und Decken", "Neue Raumaufteilung unter dem Dach, mit Abseiten als Stauraum und Platz für Einbauleuchten.", "CW- und CD-Profile"),
        ("Bad im Dachgeschoss", "Installationswände, imprägnierte Platten und Revisionsöffnungen. Sanitär und Elektro über unsere Partner-Fachbetriebe.", "Feuchtraumgeeignet"),
        ("Dachbodendämmung", "Dämmung der obersten Geschossdecke, wenn der Speicher unbewohnt bleibt.", "Oberste Geschossdecke"),
    ]
    aufbau = [
        ("Dämmen", "Mineralwolle zwischen die Sparren, lückenlos bis in die Ecken. Ob der Raum später warm und ruhig ist, entscheidet sich hier."),
        ("Abdichten", "Dampfbremse verlegen und an Wänden, Fenstern und Durchdringungen luftdicht verkleben."),
        ("Ausrichten", "Unterkonstruktion aus Latten oder Profilen. Hier werden krumme Sparren ausgeglichen."),
        ("Beplanken", "Gipsplatten verschrauben, im Bad imprägniert, bei Brandschutz als Feuerschutzplatte."),
        ("Spachteln und streichen", "Fugen und Flächen in der gewünschten Qualitätsstufe, auf Wunsch fertig gestrichen."),
    ]
    desc = "Dachausbau in Augsburg: Dämmung, Dampfbremse und verkleidete Dachschrägen, auf Wunsch mit Bad. Aus dem Speicher wird Wohnraum. Besichtigung kostenlos."
    body = f'''<main id="top">

  {service_hero("Dachausbau", "Dachausbau <span class=\"mark\">in Augsburg.</span>", "Aus dem Speicher wird Wohnraum. Wir dämmen, dichten ab und verkleiden Schrägen und Kehlbalken, auf Wunsch bis zum fertigen Zimmer oder Bad.", "p-dach-gkf", "Dachausbau mit Feuerschutzplatten", "p-dach-holz", [("DIN <em>4108-7</em>", "luftdicht verklebte Dampfbremse"), ("<em>5</em> Schichten", "von der Dämmung bis zur Farbe"), ("Mit <em>Bad</em>", "auf Wunsch unter der Schräge"), ("<em>0</em> €", "kostet die Besichtigung")])}

  <section class="section section--tint">
    <div class="wrap split">
      <div class="head">
        <p class="eyebrow">Leistungsumfang</p>
        <h2 class="h-l">Was zum Dachausbau gehört.</h2>
        <p class="lead">Sie bekommen alles aus einer Hand, von der Dämmung bis zur gestrichenen Fläche.</p>
      </div>
      {rows(umfang, one=True)}
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Fotos von der Baustelle</p>
        <h2 class="h-l">Vom Dachstuhl zum fertigen Raum.</h2>
      </div>
      {gallery(["p-dach-holz", "p-dach-gkf", "p-dach-beplankt", "p-trennwand", "p-bad-schraege", "hero-bad"])}
    </div>
  </section>

  {build_section("Aufbau der Dachschräge", "Fünf Schichten, eine Reihenfolge.", aufbau, drawings.roof(),
                  "<b>Jede Schicht hat eine Aufgabe:</b> Die Dämmung hält die Wärme, die Dampfbremse hält Feuchte fern, die Unterkonstruktion macht die Fläche gerade.")}

  {quote("Super Arbeit, auch die kniffligere Seite mit 2 Dachschrägen wurde korrekt abgehängt.", "Matthias T.", "Badezimmerdecke, Google, Nov. 2025")}

  {faq_section(faq, "Dachausbau")}

  {cross("dachausbau.html")}

  {contact("Dachausbau")}

</main>'''
    page("dachausbau.html", "Dachausbau Augsburg: Dämmung & Dachgeschossausbau | ATS Trockenbau", desc, body,
         ld=service_ld("Dachausbau", desc, "dachausbau.html") + [faq_ld(faq)], current="dachausbau.html")


def kernsanierung():
    faq = [
        ("Was gehört zu einer Kernsanierung?", "Das Gebäude oder die Wohnung wird bis auf den Rohbau zurückgebaut und neu aufgebaut: Installationen, Wände, Decken, Böden, Oberflächen und Malerarbeiten. Auf Wunsch kümmern wir uns auch um die Fassade."),
        ("Was kostet eine Kernsanierung?", "Das hängt von Fläche, Zustand und Ausstattung ab. Nach der kostenlosen Besichtigung erhalten Sie ein schriftliches Angebot, in dem jede Position nachvollziehbar aufgeführt ist."),
        ("Wie lange dauert eine Kernsanierung?", "Das richtet sich nach Größe und Umfang. Ein einzelnes Bad ist deutlich schneller fertig als ein ganzes Haus. Den Zeitplan mit den einzelnen Abschnitten finden Sie in unserem Angebot."),
        ("Kann ich während der Sanierung wohnen bleiben?", "Bei einer vollständigen Kernsanierung in der Regel nicht, weil Wasser und Strom zeitweise abgestellt sind und Staub und Lärm entstehen. Bei einzelnen Räumen, etwa einem Bad, ist es meist möglich."),
        ("Wer koordiniert Elektriker und Installateur?", "Wir. Elektro und Sanitär übernehmen unsere Partner-Fachbetriebe, abgestimmt durch uns. Sie haben einen Ansprechpartner für das ganze Projekt."),
        ("Brauche ich eine Genehmigung?", "Für reine Innenarbeiten meist nicht. Anders kann es bei Eingriffen in tragende Wände, bei einer Nutzungsänderung oder bei denkmalgeschützten Häusern sein. In Eigentumswohnungen ist oft die Zustimmung der Eigentümergemeinschaft nötig."),
        ("Was passiert mit dem Bauschutt?", "Wir transportieren den Schutt ab und entsorgen ihn fachgerecht. Das ist Teil des Angebots."),
        ("Sanieren Sie auch nur einzelne Räume?", "Ja, zum Beispiel ein Bad oder ein Dachgeschoss. Der Ablauf bleibt gleich: raus, neu, fertig."),
        ("Wie wird abgerechnet?", "Bei größeren Projekten stellen wir Abschlagsrechnungen nach Baufortschritt. Kleinere Aufträge rechnen wir nach Fertigstellung ab."),
    ]
    phases = [
        ("kern-vorher", "", "Raus", ["Kompletter Abbruch bis auf den Rohbau", "Alte Wände, Decken, Böden und Leitungen raus", "Schutt abtransportieren und fachgerecht entsorgen"]),
        ("kern-bau", "", "Neu", ["Neue Elektro- und Sanitärinstallationen mit unseren Partner-Fachbetrieben", "Wände nach neuem Grundriss", "Dämmung, Brand- und Schallschutz", "Decken, Dachschrägen und Böden"]),
        ("kern-fertig", "focus-low", "Fertig", ["Spachteln und Glätten bis Q4", "Malerarbeiten, auf Wunsch Fassade", "Schlüsselfertige Übergabe"]),
    ]
    ph = "".join(
        f'<li class="phase">{img(n, "(min-width: 52rem) 33vw, 100vw", cls=c)}<span class="num">{i:02d}</span><h3>{t}</h3>'
        f'<ul>{"".join(f"<li>{x}</li>" for x in li)}</ul></li>' for i, (n, c, t, li) in enumerate(phases, 1))
    fuer = [
        ("Eigentumswohnung und Einfamilienhaus", "Neuer Grundriss, neue Leitungen, neue Oberflächen. Nach der Übergabe können Sie einziehen."),
        ("Altbau", "Krumme Wände, Holzbalkendecken, alte Leitungen: Trockenbau und Trockenestrich gleichen aus, ohne viel Gewicht und Feuchte einzubringen."),
        ("Mietobjekte und Hausverwaltungen", "Wohnungen zwischen zwei Mietern zügig wieder vermietbar machen, mit festem Ansprechpartner."),
        ("Büro und Praxis", "Umbau nach neuem Raumkonzept, inklusive Brand- und Schallschutz sowie Akustikdecken."),
    ]
    schritte = [
        ("Rückbau", "Alte Wände, Decken, Böden und Leitungen kommen raus, bis nur der Rohbau steht. Den Schutt entsorgen wir fachgerecht."),
        ("Installationen", "Neue Elektro- und Sanitärleitungen, verlegt von unseren Partner-Fachbetrieben und abgestimmt durch uns."),
        ("Wände und Decken", "Wände nach neuem Grundriss, Vorsatzschalen vor den Leitungen und abgehängte Decken. Mit Dämmung, Brand- und Schallschutz."),
        ("Böden", "Neuer Bodenaufbau, zum Beispiel mit Trockenestrich, der ohne Trocknungszeit belegt werden kann."),
        ("Oberflächen", "Spachteln und Glätten bis Q4, Malerarbeiten und die schlüsselfertige Übergabe."),
    ]
    desc = "Kernsanierung in Augsburg, schlüsselfertig: Abbruch, Wände, Decken, Böden, Malerarbeiten, Elektro und Sanitär mit Partnern. Ein Ansprechpartner."
    body = f'''<main id="top">

  {service_hero("Kernsanierung", "Kern&shy;sanierung <span class=\"mark\">in Augsburg.</span>", "Bei einer Kernsanierung bleibt nur der Rohbau stehen. Danach bauen wir alles neu auf, schlüsselfertig und mit einem Ansprechpartner für das ganze Projekt.", "hero-bad", "Badsanierung im Dachgeschoss", "kern-vorher", [("<em>1</em> Kontakt", "ein Ansprechpartner für alles"), ("<em>3</em> Phasen", "raus, neu, fertig"), ("Schlüssel&shy;fertig", "bis zur Übergabe"), ("<em>0</em> €", "kostet die Besichtigung")])}

  {build_section("So läuft eine Kernsanierung", "Einmal alles neu, in fünf Schritten.", schritte, drawings.reno(),
                  "<b>Die Reihenfolge zählt:</b> Erst wenn alle Leitungen liegen, werden Wände und Decken geschlossen. Deshalb plant bei uns ein Ansprechpartner alle Gewerke.")}

  <section class="section section--tint">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Ein Projekt, drei Phasen</p>
        <h2 class="h-l">Vom Rohbau zum Zuhause.</h2>
        <p class="lead">Dreimal dasselbe Bad im Dachgeschoss: beim Rückbau, im Ausbau und nach der Übergabe.</p>
      </div>
      <ol class="phases">{ph}</ol>
    </div>
  </section>

  <section class="section">
    <div class="wrap split">
      <div class="head">
        <p class="eyebrow">Für wen</p>
        <h2 class="h-l">Wo wir kernsanieren.</h2>
        <p class="lead">Vom einzelnen Bad bis zum ganzen Haus, für Privat, Gewerbe und Hausverwaltungen.</p>
      </div>
      {rows(fuer, one=True)}
    </div>
  </section>

  <section class="section section--tint">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Fotos von der Baustelle</p>
        <h2 class="h-l">Weitere Baustellen.</h2>
      </div>
      {gallery(["p-bad-schraege", "p-install-1", "p-install-2", "p-dach-beplankt"], cols4=True)}
    </div>
  </section>

  {quote("Zeitplan und Preis wurde wie besprochen eingehalten", "Tatjana G.", "Trustlocal, Aug. 2025")}

  {faq_section(faq, "Kernsanierung")}

  {cross("kernsanierung.html")}

  {contact("Kernsanierung")}

</main>'''
    page("kernsanierung.html", "Kernsanierung Augsburg: schlüsselfertig aus einer Hand | ATS Trockenbau", desc, body,
         ld=service_ld("Kernsanierung", desc, "kernsanierung.html") + [faq_ld(faq)], current="kernsanierung.html")


def legal(name, title):
    body = f'<main class="legal"><div class="wrap">\n{(PART / (name + ".html")).read_text(encoding="utf-8")}</div></main>'
    page(name + ".html", title, "", body, legal=True)


if __name__ == "__main__":
    home()
    trockenbau()
    dachausbau()
    kernsanierung()
    legal("impressum", "Impressum – ATS Trockenbau")
    legal("datenschutz", "Datenschutz – ATS Trockenbau")
