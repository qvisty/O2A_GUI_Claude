# Phase 3: Kodekvalitet - Context

**Gathered:** 2026-03-20
**Status:** Ready for planning

<domain>
## Phase Boundary

Ryd kodebasen for dødkode, gør fejlhåndtering eksplicit og logget, og saml duplikerede hjælpefunktioner ét sted. Fasen dækker QUAL-01, QUAL-02 og QUAL-03. Ny funktionalitet og ydeevneforbedringer hører til Fase 4.

</domain>

<decisions>
## Implementation Decisions

### Dødkode-sletning (QUAL-01)
- Slet komplet: `aulamanager.py`, `eventmanager.py`, `databasemanager.py`, `databaseevent.py`, `test.py`
- Ingen stubs — filerne fjernes helt; Git-historik bevarer konteksten
- `ui_mainwindow.py` og `ui_unilogindialog.py` undersøges først (grep for imports); slettes kun hvis bekræftet dead code
- Kommenterede `dbManager`-linjer i `main.pyw` fjernes også

### Login-fejlhåndtering (QUAL-02)
- Fejlkanal for login-fejl: **GUI-log + tray-popup** (samme mønster som Fase 2's internetfejl-håndtering)
- Fejlbesked indeholder: exception-type + besked (f.eks. `"Login fejlede: ConnectionError – Unable to reach aula.dk"`)
- Timing: GUI-log + tray kun ved **endelig fejl** (alle 10 login-forsøg opbrugt); hvert enkelt forsøg logges kun til `self.logger` (o2a.log)
- De 5 bare `except` blocks i `aula/aula_connection.py` erstattes med `except Exception as e:` + logning

### API- og runtime-fejlhåndtering (QUAL-02)
- De 2 bare `except` blocks i `aula/aula_calendar.py` og 1 i `outlookmanager.py` erstattes med `except Exception as e:`
- Disse logges **kun til `self.logger`** (o2a.log) — ikke til GUI-log/tray
- CC-email: slet den hardkodede `mail.CC = "olex3397@skolens.net"` linje i `outlookmanager.py` (ingen erstatning, ikke konfigurerbar endnu)

### Hjælperfunktioner (QUAL-03)
- `url_fixer` og `teams_url_fixer`: fjern instansmetoderne fra `aula_calendar.py`; importer fra `aula/utils.py` i stedet (`from aula.utils import url_fixer, teams_url_fixer`)
- `calulate_day_of_the_week_mask`: flyt fra instansmetode i `aula_calendar.py` til modulniveau-funktion i `aula/utils.py`
  - Ret stavefejl i samme omgang: `calulate` → `calculate`
  - Ny signatur: `def calculate_day_of_the_week_mask(...)` uden `self`
  - Opdater alle call sites i `aula_calendar.py`

### Claude's Discretion
- Præcis exception-type for hver enkelt bare except block (f.eks. `requests.RequestException` vs. `Exception`)
- Konkret format for GUI-log-beskeder (konsistens med Fase 2's mønstre)
- Om tray-throttling fra Fase 2 gælder for login-fejl eller kun internetfejl

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `aula/utils.py`: Indeholder allerede `url_fixer` og `teams_url_fixer` som modulniveau-funktioner — importeres bare ikke endnu
- `main.pyw` `self.logger` + GUI-log + tray-mønster: etableret i Fase 2 via `on_runO2A_clicked` — brug samme mønstre for login-fejl
- `aula_connection.py` bruger sin egen `self.logger` — fejl logges herfra, GUI-signal sendes via return-kode til `main.pyw`

### Established Patterns
- Aktiv runtime-sti: `main.pyw` → `AulaConnection` / `AulaCalendar` → `OutlookManager`
- `aulamanager.py` og `eventmanager.py` er **ikke** autoritativ for nogen aktiv kode
- Logging namespace: `'O2A'` bruges i både `main.pyw` og `aula_calendar.py`

### Integration Points
- Dead code-sletning: ingen importering afbrydes i `main.pyw` (eventmanager/aulamanager er aldrig importeret der)
- CC-email: ét sted, `outlookmanager.py` linje 185
- Helper-konsolidering: call sites kun i `aula_calendar.py`

</code_context>

<specifics>
## Specific Ideas

- Fejlhåndteringsmønsteret fra Fase 2 (GUI-log + tray) skal genbruges for login-fejl — Ole ser det i statuslinjen selv når vinduet er skjult
- Stavefejl-rettelse (`calulate` → `calculate`) tages med nu da vi alligevel rører call sites
- ui_-filerne tjekkes og slettes kun ved bekræftelse — undgå at røre ved Qt-genererede filer uden grund

</specifics>

<deferred>
## Deferred Ideas

- CC-email gøres konfigurerbar (SEC-01 i v2) — fjernes nu, konfigurabilitet til v2
- Gentagne begivenheder (REC-01, REC-02) — v2
- Automatiserede tests — separat milestone (nævnt i REQUIREMENTS.md Out of Scope for v1)

</deferred>

---

*Phase: 03-kodekvalitet*
*Context gathered: 2026-03-20*
