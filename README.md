# ATS Trockenbau – Website

Statische Website (HTML/CSS, kein Build-Schritt). Deutsch, DSGVO-freundlich:
keine Cookies, kein Tracking, Schriften lokal eingebunden (SIL Open Font License).

## Dateien
- `index.html` – Startseite (Leistungen, Q1–Q4, Ablauf, Einsatzgebiet, Kontakt)
- `impressum.html` – Impressum nach § 5 DDG
- `datenschutz.html` – Datenschutzerklärung
- `assets/` – Stylesheet, Favicon, Schriften

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
