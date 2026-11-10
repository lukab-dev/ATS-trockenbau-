# ATS Trockenbau – Website

Statische Website (HTML/CSS). Deutsch, DSGVO-freundlich:
keine Cookies, kein Tracking, Schriften lokal eingebunden (SIL Open Font License).

## Dateien
- `index.html` – Startseite (Leistungen, Projekte, Bewertungen, Ablauf, Einsatzgebiet, FAQ, Kontakt)
- `trockenbau.html`, `dachausbau.html`, `kernsanierung.html` – Leistungsseiten mit Fotos und FAQ
- `impressum.html`, `datenschutz.html` – Rechtstexte
- `assets/` – Stylesheet, Skript, Fotos, Logos, Schriften
- `tools/build.py` – erzeugt alle HTML-Seiten; Texte der Rechtsseiten und Zeichnungen liegen in `tools/partials/`

## Seiten ändern
Kopf, Navigation, Kontaktbereich und Fuß stehen einmal in `tools/build.py` und werden in jede Seite geschrieben.
Texte dort ändern, dann `python3 tools/build.py` ausführen und die erzeugten `.html`-Dateien mit einchecken.
GitHub Pages liefert die fertigen Dateien aus und braucht keinen Build.

## Schaltflächen
Eine Hauptaktion (gold, „Besichtigung anfragen“), eine Nebenaktion (Umriss, Telefonnummer), alles andere sind Textlinks.
Was nicht anklickbar ist, sieht auch nicht wie ein Knopf aus.

## Livegang (Stand November 2026)
- Testhinweis und `noindex` entfernt, `robots.txt` erlaubt Indexierung, `sitemap.xml` vorhanden.
- Strukturierte Daten (schema.org `GeneralContractor`) und Vorschaubild (`assets/img/og-ats-trockenbau.jpg`) im `<head>` von `index.html`.
- Domain: atstrockenbau.com über GitHub Pages (Einstellungen → Pages → Custom domain).

## DNS für atstrockenbau.com
| Typ | Name | Wert |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | lukab-dev.github.io |

MX-Einträge (Google Mail) und TXT (SPF) bleiben unverändert.
