# Kendte problemer

Oversigt over kendte fejl og teknisk gæld i O2A pr. 2026-03-16. Sorteret efter prioritet. Fejlrettelser er planlagt i Fase 2.

---

## KRITISK — Tidskritisk

> **OBS:** BUG-01 vil begynde at ramme begivenheder fra 29. marts 2026 — om ca. 13 dage fra kortlægningstidspunktet. Begivenheder i sommertid vil have forkert tidspunkt i Aula hvis dette ikke rettes inden da.

### BUG-01: Hardkodet sommertidstabel virker kun til og med 2025

**Prioritet:** KRITISK
**Deadline:** Sommertid 2026 starter 29. marts 2026
**Symptom:** Begivenheder i Aula fra 29. marts 2026 og frem vises med forkert klokkeslæt — én time forskudt (vintertid +01:00 bruges i stedet for sommertid +02:00).
**Årsag:** outlookmanager.py bruger en hardkodet liste over sommertidsperioder fra 2021 til 2025. Begivenheder i 2026 er ikke i listen og får tildelt det forkerte tidszoneoffset. Der er en TODO-kommentar i koden ved linje 16 der erkender dette.
**Berørte filer:** outlookmanager.py (linje 16–45)
**Planlagt løsning (Fase 2 — BUG-01):** Erstat hardkodet tabel med Pythons zoneinfo-modul til dynamisk beregning af sommertid for et givent tidspunkt.

---

## Høj prioritet

### BUG-02: Programmet starter ikke på Python 3.12 eller nyere

**Prioritet:** HØJ
**Symptom:** Programmet kaster ImportError ved opstart på Python 3.12+. Hele SetupManager-klassen fejler at indlæse.
**Årsag:** setupmanager.py linje 1 importerer fra distutils-modulet (`from distutils.core import run_setup`). distutils blev fjernet fra Pythons standardbibliotek i version 3.12. Importen bruges ikke i resten af filen.
**Berørte filer:** setupmanager.py (linje 1)
**Planlagt løsning (Fase 2 — BUG-02):** Fjern den ubrugte distutils-import.

### BUG-03: Manglende internetforbindelse crasher med fejl i stedet for at vise besked

**Prioritet:** HØJ
**Symptom:** Hvis der ingen internetforbindelse er når synkronisering startes, kaster programmet en NameError og viser ingen besked i GUI-logpanelet.
**Årsag:** main.pyw linje 538 og 554 kalder `logger.critical(...)`, men `logger`-variablen er ikke defineret i den kontekst — den er kun tilgængelig i modulets `__main__`-blok. Den korrekte reference er `self.logger`.
**Berørte filer:** main.pyw (linje 538, 554)
**Planlagt løsning (Fase 2 — BUG-03):** Ret `logger` til `self.logger` på begge linjer.

### BUG-04: Sletning af Aula-begivenhed fejler med NameError

**Prioritet:** HØJ
**Symptom:** Hvis en begivenhed ikke kan slettes fra Aula første forsøg, kaster programmet en NameError og afsluttes fejlagtigt.
**Årsag:** aula/aula_calendar.py linje 365 indeholder `s#elf.logger.warning(...)` — tegnet `s` er ved en fejl havnet uden for kommentarsymbolet `#`, så Python evaluerer det som et udtryk der forsøger at finde en variabel ved navn `s`, som ikke eksisterer.
**Berørte filer:** aula/aula_calendar.py (linje 365)
**Planlagt løsning (Fase 2 — BUG-04):** Ret linje 365 til `#self.logger.warning(...)` (flyt `s` inden for kommentaren).

### BUG-05: Programmet crasher ved opstart hvis .git-mappen mangler

**Prioritet:** HØJ
**Symptom:** Programmet starter ikke hvis det køres udenfor et git-repository, f.eks. som kompileret .exe-fil.
**Årsag:** main.pyw bruger GitPython-pakken til at læse git commit-hash og dato for at vise versionsnummeret i GUI. Hvis .git-mappen ikke findes, kaster GitPython en fejl under opstarten.
**Berørte filer:** main.pyw (linje 156–163)
**Planlagt løsning (Fase 2 — BUG-05):** Gem versionsnummer i en statisk fil (f.eks. version.txt) og fjern GitPython-afhængigheden.

---

## Teknisk gæld

Følgende punkter er ikke akutte fejl men sænker kodekvalitet og vedligeholdelsesevne. Planlagt adresseret i Fase 3.

| ID | Beskrivelse | Berørte filer | Fase |
|----|-------------|---------------|------|
| QUAL-01 | AulaManager, EventManager og DatabaseManager er dødkode der kopierer AulaCalendar-logikken. Bug-rettelser skal i dag laves to steder. | aulamanager.py, eventmanager.py, databasemanager.py | Fase 3 |
| QUAL-02 | 11 steder i koden bruger `except: pass` som fanger alle fejl og kaster dem væk uden log-besked. Login-fejl og netværksfejl forsvinder lydløst. | aula_connection.py, aula_calendar.py, aulamanager.py, outlookmanager.py | Fase 3 |
| QUAL-03 | Hjælpefunktioner (url_fixer, teams_url_fixer, calulate_day_of_the_week_mask) er kopieret identisk til 3-4 filer. Ændringer skal laves alle steder. | aula_calendar.py, aulamanager.py, eventmanager.py, aula/utils.py | Fase 3 |

## Ydeevne

| ID | Beskrivelse | Berørte filer | Fase |
|----|-------------|---------------|------|
| PERF-01 | Deltager-navne slås op via Aulas søge-API ved hver begivenhed — med 1 sekunds forsinkelse mellem hvert opslag. En lokal cache er implementeret (databasemanager.py) men deaktiveret. Ved mange begivenheder med deltagere er synkronisering meget langsom. | aula_calendar.py (linje 283–308), databasemanager.py | Fase 4 |

## Sikkerhedsnoter

Disse punkter er ikke akutte for et lokalt desktopprogram men er dokumenteret for fuldstændighedens skyld:

- Fejlnotifikationsmails CC'er en hardkodet e-mailadresse (olex3397@skolens.net) — potentielt fortrolige begivenhedsoplysninger videresendes til tredjemand (outlookmanager.py linje 185)
- Adgangskode printes til terminal under det gamle CLI-setup-flow (setupmanager.py linje 201) — benyttes ikke via GUI-opstartsstien

## Begrænsninger (by design)

Disse punkter er kendte begrænsninger der ikke er planlagt rettet i den nuværende roadmap:

- Tilbagevendende begivenheder (f.eks. ugentlige møder) synkroniseres ikke korrekt — de oprettes som enkeltbegivenheder uden advarsel til brugeren
- Synkroniseringsvinduet er hardkodet til ca. 1 år frem — begivenheder mere end ~18 måneder ude synkroniseres aldrig
- Maksimalt synkroniseringsinterval via GUI er 4 timer (kan ikke øges)
