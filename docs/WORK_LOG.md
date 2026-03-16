# Arbejdslog

Kronologisk log over analyser og ændringer i O2A-projektet. Seneste indgang øverst.

---

## 2026-03-16 — Kortlægning af kodebase

**Hvad:** Claude gennemgik hele kodebasen og kortlagde arkitektur, teknisk gæld, kendte fejl og integrationspunkter. Resultatet er gemt i `.planning/codebase/`-mappen og danner grundlag for de næste faser.

**Nøglefund:**

- AulaCalendar (`aula/aula_calendar.py`) er den aktive Aula API-klient — bruger API v23. AulaManager (`aulamanager.py`) er dødkode med næsten identisk logik, men bruger den ældre v22
- Synkroniseringsmærker er gemt direkte i Aulas begivenhedsbeskrivelser (`o2a_outlook_GlobalAppointmentID` og `o2a_outlook_LastModificationTime`) — det er programmets eneste hukommelse på tværs af kørsler
- Hardkodet sommertidstabel i `outlookmanager.py` virker kun til og med 2025 — kritisk fejl der vil ramme alle begivenheder fra 29. marts 2026
- GitPython-pakken crasher programmet ved opstart hvis `.git`-mappen mangler (f.eks. ved kørsel som `.exe`)
- Deltager-caching i `databasemanager.py` er implementeret men deaktiveret (udkommenteret) — medfører langsom synkronisering
- Ingen automatiserede tests — `test.py` er tom

**Konsekvenser for videre arbejde:**

- BUG-01 (sommertid 2026) er tidskritisk og skal rettes i Fase 2 inden 29. marts 2026
- Fase 2 (fejlrettelser) og Fase 3 (kodekvalitet) er planlagt på baggrund af denne kortlægning
- `docs/`-mappen (nuværende dokument) oprettes som første leverance af Fase 1

---

*Nye indgange tilføjes øverst i denne fil ved fremtidigt arbejde.*
