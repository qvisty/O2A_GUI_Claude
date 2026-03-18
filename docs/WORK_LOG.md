# Arbejdslog

Kronologisk log over analyser og ændringer i O2A-projektet. Seneste indgang øverst.

---

## 2026-03-18 - Fase 2 afsluttet og dokumentation ryddet op

**Hvad:** Fase 2 blev færdiggjort med rettelser for internetfejl, delete/update-fejlstier og startup uden `.git`. Dokumentationen i `docs/` blev samtidig repareret efter tegnsætskorruption og opdateret til at afspejle den faktiske status.

**Resultat:**

- BUG-03 er rettet med central internetfejl-helper i `main.pyw`
- BUG-04 er rettet både i `deleteEvent()` og i caller-semantikken i `main.pyw`
- BUG-05 er rettet med fallback til `version.txt` og skjult versionslabel når metadata mangler
- `ISSUES.md`, `DECISIONS.md`, `PROJECT_OVERVIEW.md`, `WORK_LOG.md` og `DOCUMENTATION_GUIDELINES.md` er normaliseret tilbage til læsbart dansk

**Konsekvenser for videre arbejde:**

- Fase 2 kan nu læses og overdrages uden modstrid mellem kode og dokumentation
- Fremtidige docs-opdateringer bør verificeres for tegnsæt og statuskonsistens før commit

---

## 2026-03-18 - Fase 2 planlagt, workflow stabiliseret og Wave 1 gennemført

**Hvad:** GSD-forløbet for Fase 2 blev gennemført fra kontekstafklaring til planlægning og videre til eksekvering af første plan. Undervejs blev `.planning/STATE.md` tilpasset, så repoets state-fil igen virker sammen med GSD-helperne.

**Resultat:**

- `02-CONTEXT.md`, `02-RESEARCH.md`, `02-VALIDATION.md`, `02-01-PLAN.md` og `02-02-PLAN.md` er oprettet for Fase 2
- `STATE.md` er gjort helper-kompatibel, så `state record-session` og `state-snapshot` igen kan opdatere og læse sessionstilstand automatisk
- Fase 2 er planlagt som to arbejdsspor: `02-01` for BUG-01 + BUG-02 og `02-02` for BUG-03 + BUG-04 + BUG-05
- `02-01` er gennemført med delt timezone-helper (`aula/timezone_utils.py`), dynamisk DST-håndtering i Outlook- og Aula-stien og fjernet `distutils`-import i `setupmanager.py`
- Der er oprettet fokuserede tests for Fase 2 omkring DST og Aula lookup-vinduer

**Konsekvenser for videre arbejde:**

- BUG-01 og BUG-02 er ikke længere kun planlagte; de er implementeret og lokalt verificeret
- Wave 2 kunne fokusere på startup- og fejlsti-resiliens oven på en tidskorrekt og Python 3.12-sikker kodebase
- Dokumentation i `docs/` skal fremover opdateres som fast del af GSD-arbejdet, ikke bagefter som oprydning

---

## 2026-03-18 - Dokumentationspolitik formaliseret

**Hvad:** Der er oprettet en ny fil, `docs/DOCUMENTATION_GUIDELINES.md`, som formaliserer hvordan dokumentationen i `docs/` skal vedligeholdes fremover på baggrund af den praksis der allerede var etableret i projektet.

**Resultat:**

- `WORK_LOG.md` er defineret som løbende arbejdslog for analyser, ændringer og konsekvenser
- `DECISIONS.md` er defineret som log for ikke-selvindlysende tekniske valg
- `ISSUES.md` er defineret som log for fejl, begrænsninger og teknisk gæld
- `PROJECT_OVERVIEW.md` er defineret som vedligeholder- og brugerrettet systemforklaring

**Konsekvenser for videre arbejde:**

- Fremtidige ændringer skal vurderes mod disse fire dokumenttyper som en fast del af leverancen
- Dokumentation til Ole i `docs/` er nu eksplicit beskrevet og ikke kun implicit praksis

---

## 2026-03-16 - Kortlægning af kodebase

**Hvad:** Claude gennemgik hele kodebasen og kortlagde arkitektur, teknisk gæld, kendte fejl og integrationspunkter. Resultatet er gemt i `.planning/codebase/`-mappen og danner grundlag for de næste faser.

**Nøglefund:**

- AulaCalendar (`aula/aula_calendar.py`) er den aktive Aula API-klient - bruger API v23. AulaManager (`aulamanager.py`) er dødkode med næsten identisk logik, men bruger den ældre v22
- Synkroniseringsmærker er gemt direkte i Aulas begivenhedsbeskrivelser (`o2a_outlook_GlobalAppointmentID` og `o2a_outlook_LastModificationTime`) - det er programmets eneste hukommelse på tværs af kørsler
- Hardkodet sommertidstabel i `outlookmanager.py` virker kun til og med 2025 - kritisk fejl der ville ramme alle begivenheder fra 29. marts 2026
- GitPython-pakken crashede programmet ved opstart hvis `.git`-mappen manglede
- Deltager-caching i `databasemanager.py` er implementeret men deaktiveret - medfører langsom synkronisering
- Ingen automatiserede tests - `test.py` var tom ved kortlægningstidspunktet

**Konsekvenser for videre arbejde:**

- BUG-01 var tidskritisk og skulle rettes i Fase 2 inden 29. marts 2026
- Fase 2 (fejlrettelser) og Fase 3 (kodekvalitet) blev planlagt på baggrund af denne kortlægning
- `docs/`-mappen blev oprettet som første leverance af Fase 1

---

*Nye indgange tilføjes øverst i denne fil ved fremtidigt arbejde.*
