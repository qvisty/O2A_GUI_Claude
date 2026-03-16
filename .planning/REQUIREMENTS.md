# Requirements: O2A — Outlook to Aula

**Defined:** 2026-03-16
**Core Value:** Outlook-aftaler mærket med "AULA" skal altid afspejle den korrekte tilstand i Aula — automatisk, uden manuel indgriben.

## v1 Requirements

### Dokumentation

- [ ] **DOCS-01**: Ole kan læse en overordnet projektforståelse på dansk i docs/PROJECT_OVERVIEW.md
- [ ] **DOCS-02**: Ole kan følge en løbende arbejdslog i docs/WORK_LOG.md med beskrivelse af analyser og ændringer
- [ ] **DOCS-03**: Ole kan læse en beslutningslog i docs/DECISIONS.md med begrundelse for tekniske valg
- [ ] **DOCS-04**: Ole kan se en opdateret problemliste i docs/ISSUES.md med kendte fejl og teknisk gæld

### Fejlrettelser

- [ ] **BUG-01**: Begivenheder i sommertid 2026 og frem har korrekte tidspunkter i Aula (erstatter hardkodet DST-tabel med dynamisk beregning)
- [ ] **BUG-02**: Applikationen starter og kører korrekt på Python 3.12+ (fjerner ubrugt distutils-import)
- [ ] **BUG-03**: Manglende internetforbindelse viser en fejlbesked i GUI i stedet for at crashe med NameError
- [ ] **BUG-04**: Sletning af Aula-begivenheder fejler ikke med NameError (retter syntaksfejl i deleteEvent)
- [ ] **BUG-05**: Applikationen starter korrekt når .git-mappen mangler, f.eks. ved kørsel som kompileret .exe (retter GitPython-crash)

### Kodekvalitet

- [ ] **QUAL-01**: Arkivet indeholder ikke ubenyttet arvekode (AulaManager, EventManager, DatabaseManager fjernes fra aktiv codebase)
- [ ] **QUAL-02**: Fejlhåndtering i login- og API-kald er eksplicit og loggede (erstatter bare `except: pass` med specifikke exceptions og log-beskeder)
- [ ] **QUAL-03**: Duplikerede hjælpefunktioner (url_fixer, teams_url_fixer, calulate_day_of_the_week_mask) er samlet i aula/utils.py

### Ydeevne

- [ ] **PERF-01**: Deltagernavne caches lokalt i databasen per sync-session, så hvert navn kun slås op én gang per kørsel

## v2 Requirements

### Sikkerhed

- **SEC-01**: Hardkodet CC-e-mailadresse i fejlnotifikationer fjernes eller gøres konfigurerbar
- **SEC-02**: Adgangskode printes ikke til terminalen i CLI-setup-flowet

### Gentagne begivenheder

- **REC-01**: Brugeren advares tydeligt i GUI når tilbagevendende Outlook-begivenheder springes over
- **REC-02**: Tilbagevendende begivenheder synkroniseres korrekt til Aula med den rette gentagelsesregel

### Konfiguration

- **CONF-01**: Fremtidsvinduet for synkronisering (standard: i dag + 1 år) kan konfigureres i configuration.ini
- **CONF-02**: Maksimalt sync-interval kan sættes til mere end 4 timer

## Out of Scope

| Feature | Reason |
|---------|--------|
| Tovejs-synkronisering (Aula → Outlook) | Designmæssigt udelukket; ændrer grundlæggende arkitektur |
| macOS/Linux-understøttelse | Afhænger af Windows COM/Outlook; ikke muligt uden stor omskrivning |
| Automatiserede tests | Høj kompleksitet (login scraping, COM interop); kræver separat milestone |
| Batch-hentning af Aula-begivenheder | Kræver Aula API-undersøgelse; udskydes til v2 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| DOCS-01 | Phase 1 | Pending |
| DOCS-02 | Phase 1 | Pending |
| DOCS-03 | Phase 1 | Pending |
| DOCS-04 | Phase 1 | Pending |
| BUG-01 | Phase 2 | Pending |
| BUG-02 | Phase 2 | Pending |
| BUG-03 | Phase 2 | Pending |
| BUG-04 | Phase 2 | Pending |
| BUG-05 | Phase 2 | Pending |
| QUAL-01 | Phase 3 | Pending |
| QUAL-02 | Phase 3 | Pending |
| QUAL-03 | Phase 3 | Pending |
| PERF-01 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 13 total
- Mapped to phases: 13
- Unmapped: 0 ✓

---
*Requirements defined: 2026-03-16*
*Last updated: 2026-03-16 after initial definition*
