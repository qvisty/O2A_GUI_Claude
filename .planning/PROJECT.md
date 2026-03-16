# O2A — Outlook to Aula

## What This Is

O2A er en Windows-desktopapplikation (Python 3 / PySide6 / Qt6) som synkroniserer kalenderaftaler fra Microsoft Outlook til det danske skoleadministrationssystem Aula. Synkroniseringen er envejs — kun Outlook-aftaler mærket med kategorien "AULA" eller "AULA Institutionskalender" overføres. Applikationen understøtter oprettelse, opdatering og sletning af aftaler i Aula og kører som en systemstatusikon i Windows-proceslinjen.

Projektet er lavet af Ole og vedligeholdes/videreudvikles med hjælp fra Claude Code og GSD.

## Core Value

Outlook-aftaler mærket med "AULA" skal altid afspejle den korrekte tilstand i Aula — automatisk, uden manuel indgriben.

## Requirements

### Validated

<!-- Eksisterende funktionalitet — verificeret via kodeanalyse 2026-03-16 -->

- ✓ Synkronisering af AULA-mærkede Outlook-aftaler til Aula via REST API — eksisterende
- ✓ GUI med systemstatusikon, login-dialog og statuslog-panel — eksisterende
- ✓ Oprettelse, opdatering og sletning af Aula-aftaler baseret på diff mod Outlook — eksisterende
- ✓ Deltagernavne opløses via CSV-navnefiler (personer.csv, personer_ignorer.csv) — eksisterende
- ✓ Legitimationsoplysninger gemt sikkert (OS keyring + configuration.ini) — eksisterende
- ✓ Baggrundssynkronisering via QThreadPool (responsiv GUI) — eksisterende
- ✓ Fejlnotifikationer via e-mail gennem Outlook COM — eksisterende
- ✓ Automatisk synkronisering på konfigurerbart tidsinterval — eksisterende
- ✓ Tvungen synkronisering uden tidstjek — eksisterende

### Active

<!-- Ny funktionalitet og forbedringer som arbejdes på nu -->

- [ ] Opbygning af docs/-mappe med læsbar dansk dokumentation til Ole
- [ ] Ret kritisk fejl: hardkodet sommertidstabel virker kun til og med 2025
- [ ] Ret kritisk fejl: `distutils`-import crasher på Python 3.12+
- [ ] Ret fejl: `logger`-referencefejl ved manglende internetforbindelse
- [ ] Ret fejl: syntaksfejl i `deleteEvent` ved mislykkede sletninger
- [ ] Ret fejl: `GitPython` crasher ved kørsel uden .git-mappe
- [ ] Fjern hardkodet CC-e-mailadresse i fejlnotifikationer
- [ ] Ryd op i dødkode (AulaManager, EventManager, DatabaseManager)
- [ ] Erstat bare `except`-blokke med specifik fejlhåndtering og logging
- [ ] Forbedre ydeevne: genaktiver attendee-caching via DatabaseManager

### Out of Scope

- Understøttelse af macOS/Linux — applikationen er designet til Windows og afhænger af COM/Outlook
- Tovejs-synkronisering — ændringer i Aula skrives aldrig tilbage til Outlook

## Context

Kodebasen er fuldt kortlagt via GSD map-codebase (2026-03-16). Analysen er tilgængelig i `.planning/codebase/`. De vigtigste opmærksomhedspunkter:

- `aulamanager.py`, `eventmanager.py` og `databasemanager.py` er arvekode som ikke bruges i den aktive synkroniseringssti i `main.pyw`
- Gentagne begivenheder er slået fra med `is_Recurring = False` — brugere informeres ikke
- Login-flowet scraper HTML-formularer med BeautifulSoup og er skrøbeligt over for ændringer i Aulas loginside
- Der eksisterer ingen automatiserede tests

## Constraints

- **Platform**: Windows-only — afhænger af win32com (Outlook COM), pywin32 og OS keyring
- **Kode**: Python 3, PySide6/Qt6, requests + BeautifulSoup til Aula API
- **API**: Aula REST API v23 — login via HTML form scraping (fragilt)
- **Distribution**: Pakkes med PyInstaller til en enkelt .exe; .git-mappe er ikke til stede ved kørsel

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Synkroniseringsmarkører indlejres i Aula-begivenhedens beskrivelse | Ingen server-side tilstand nødvendig; identificerer Outlook-begivenheder i Aula | ✓ Fungerer i praksis |
| `AulaCalendar` (aula/-pakken) er den aktive kodevej fremfor `AulaManager` | Refaktorering undervejs; den nye pakke er renere struktureret | ✓ Bekræftet i kodeanalyse |
| Gentagne begivenheder deaktiveres | Kompleksitet; fuld support udestår | — Bør revurderes |

---
*Last updated: 2026-03-16 after initialization*
