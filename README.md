# ATS Trockenbau – Website

Statische Website (HTML/CSS, kein Build-Schritt). Deutsch, DSGVO-freundlich:
keine Cookies, kein Tracking, Schriften lokal eingebunden (SIL Open Font License).

## Dateien
- `index.html` – Startseite (Leistungen, Q1–Q4, Ablauf, Einsatzgebiet, Kontakt)
- `impressum.html` – Impressum nach § 5 DDG
- `datenschutz.html` – Datenschutzerklärung
- `assets/` – Stylesheet, Favicon, Schriften

## Vor dem Livegang
1. Alle Platzhalter `[...]` ersetzen (`grep -n '\[' *.html`).
2. In `index.html` beim Formular `data-mail="..."` die E-Mail-Adresse eintragen
   (oder einen Formular-Dienst/Backend anbinden).
3. Testhinweis (`<div class="testbar">`) entfernen.
4. `<meta name="robots" content="noindex, nofollow">` aus allen Seiten entfernen
   und `robots.txt` auf `Allow: /` umstellen.
5. Rechtstexte prüfen lassen (Anwalt oder Handwerkskammer).

## Hosting
Den Ordner auf einen beliebigen statischen Host laden (z. B. Cloudflare Pages,
Netlify, oder Webspace eines deutschen Anbieters) und die eigene Domain verbinden.
Für maximale DSGVO-Sicherheit einen Hoster mit Serverstandort in der EU wählen.
