# ATS Trockenbau – Projektleitfaden für Claude

Website von **ATS Trockenbau** (Inhaber Milos Pekovic, Augsburg), live unter **https://atstrockenbau.com**.
Statische Seite auf GitHub Pages. Sprache der Website: Deutsch. Der Nutzer schreibt meist Englisch,
der Inhaber Serbisch (informell, „ti“).

## Veröffentlichung – wichtig
- **Live-Branch:** `claude/trockenbau-augsburg-webpage-0jtph5` im Repo `lukab-dev/ATS-trockenbau-`.
  GitHub Pages veröffentlicht jeden Push auf diesen Branch nach 1–4 Minuten automatisch.
- **Nur auf diesen Branch pushen.** Ein anderer Branch geht nicht online (das ist schon einmal passiert).
- `CNAME` (Inhalt `atstrockenbau.com`) **nie löschen oder ändern** – sonst fällt die Domain weg.
- Vor dem Push: `git pull` (GitHub kann selbst Commits anlegen, z. B. für CNAME).

## Seiten ändern
- Alle HTML-Seiten werden von **`tools/build.py`** erzeugt. Nie die `.html`-Dateien direkt bearbeiten,
  sondern `tools/build.py` (bzw. `tools/partials/` für Impressum/Datenschutz) ändern und dann
  `python3 tools/build.py` ausführen. Erzeugte `.html`-Dateien mit einchecken.
- Neue Seite → auch in `sitemap.xml` eintragen und von der Startseite/Navigation verlinken.
- Danach lokal prüfen (z. B. `python3 -m http.server` im Projektordner) – Desktop und Handy-Breite.

## Fotos einbauen
- Rohfotos liegen in **`fotos-neu/`** (steht in `.gitignore`, wird **nicht** veröffentlicht).
- Auswahl: scharf, hell, aufgeräumt, echte eigene Baustellen. Vorher/Nachher aus gleichem Blickwinkel
  sind am wertvollsten (passen als Paar auf die Leistungsseiten).
- **Skript:** `tools/photos.py` erledigt Schritte 1–4. Neue Fotos dort in `PICKS` eintragen
  (Name, Datei, Ausschnitt-Mitte), `python3 tools/photos.py <name>` ausführen, Ergebnis ansehen.
  Tonwerte nur auf der Helligkeit strecken: `autocontrast(preserve_tone=True)` verstärkt in Pillow 10
  einen Gelbstich.
- Bearbeitung mit Pillow (`pip install pillow`, für Begradigen optional `opencv-python-headless`):
  1. EXIF-Drehung anwenden, **alle Metadaten entfernen** (GPS!).
  2. Begradigen: stürzende Linien/Schiefstand korrigieren (senkrechte Kanten senkrecht), danach zuschneiden.
  3. Dezente Tonwerte: `ImageOps.autocontrast(cutoff=0.4, preserve_tone=True)`, Farbe ×1.04,
     starken Gelbstich von Kellerlicht/Glühbirnen moderat neutralisieren.
  4. Als WebP (Qualität ~78) in zwei Breiten speichern: `assets/img/<name>-600.webp` und `-1200.webp`
     (Querformat: 640/1200). Hochformat-Galeriebilder im Format 3:4.
  5. In `tools/build.py` in `IMG` (Maße) und `CAP` (Bildunterschrift = Alt-Text) eintragen und in die
     passende `gallery([...])` / `bento([...])` aufnehmen.
- **Rechtlicher Rahmen (UWG § 5, EU AI Act):** nur technische Korrekturen (Licht, Farbe, Begradigen,
  Zuschnitt, kleiner Fremdkram wie Eimer/Kabel). **Nicht** das Arbeitsergebnis schöner machen
  (keine Risse/Fugen wegretuschieren), nichts hinzufügen, keine KI-generierten „Projektfotos“.
  Vorher/Nachher bleiben unverfälscht. Hausnummern, Gesichter, private Gegenstände weglassen/abschneiden.
- Bildunterschriften ehrlich und konkret (Gewerk, Situation). Keine Orte erfinden.

## SEO-Regeln (Stand 2026)
- Titel ≤ 60 Zeichen, Meta-Beschreibung ≤ 155 Zeichen, „Augsburg“ in H1 jeder Leistungsseite.
- **Keine Städte-Seiten** mit ausgetauschtem Ortsnamen (Doorway/Scaled Content → Abstrafung).
  Neue Seiten nur mit echtem Inhalt und eigenen Fotos.
- Strukturierte Daten (`GeneralContractor`, FAQ) liegen in `tools/build.py`. Keine `aggregateRating`
  für eigene Bewertungen.
- Google Search Console ist eingerichtet (Domain-Property, Sitemap eingereicht).

## Feste Firmendaten (nicht ändern ohne Rückfrage)
- ATS Trockenbau, Inhaber Milos Pekovic (Einzelunternehmen), Droste-Hülshoff-Straße 26, 86157 Augsburg
- Tel. 0176 24142472, WhatsApp gleiche Nummer, info@atstrockenbau.com, USt-IdNr. DE359550560
- Betriebshaftpflicht VHV Allgemeine Versicherung AG (FIRMENPROTECT). Nicht in der Handwerkskammer.
- Gegründet 01.03.2023, Erfahrung seit 2014, 4 Mitarbeiter, Einsatzgebiet 100 km um Augsburg.
- Elektro und Sanitär über Partner-Fachbetriebe. Brandschutz bis F90+, geschult bei ZAPP-ZIMMERMANN.
- Keine Festpreis-Versprechen (Preise sind nicht immer fix). Besichtigung kostenlos.
  Abrechnung: kleine Aufträge nach Fertigstellung, große mit Abschlagsrechnungen.
- Bewertungen: 5,0 aus 32 (Google, MyHammer, Trustlocal); Zitate nur wörtlich, Namen abgekürzt,
  mit Quellenhinweis.

## Technik
- Kontaktformular sendet per Google Apps Script (`ENDPOINT` in `tools/build.py`) an info@atstrockenbau.com.
  Im Datenschutz erwähnt. Honeypot-Feld `website` gegen Spam.
- Keine Cookies, kein Tracking, Schriften lokal. Externe Dienste nur als Links.
- DNS (Squarespace): 4× A auf GitHub Pages, `www` CNAME → `lukab-dev.github.io`. MX/SPF/Google-Verifizierung nicht anfassen.
