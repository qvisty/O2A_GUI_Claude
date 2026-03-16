# Phase 1: Dokumentation - Research

**Researched:** 2026-03-16
**Domain:** Technical documentation authoring (Danish-language, markdown, project knowledge capture)
**Confidence:** HIGH

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| DOCS-01 | Ole kan læse en overordnet projektforståelse på dansk i docs/PROJECT_OVERVIEW.md | Architecture, integrations, and stack analysis fully documented in .planning/codebase/ — all content is available and verified |
| DOCS-02 | Ole kan følge en løbende arbejdslog i docs/WORK_LOG.md med beskrivelse af analyser og ændringer | STATE.md records session history and the codebase mapping was completed 2026-03-16 — first entry is ready to write |
| DOCS-03 | Ole kan læse en beslutningslog i docs/DECISIONS.md med begrundelse for tekniske valg | ARCHITECTURE.md and CONCERNS.md document why AulaCalendar is canonical, why descriptions carry sync markers, why form-scraping is used, why GitPython was added |
| DOCS-04 | Ole kan se en opdateret problemliste i docs/ISSUES.md med kendte fejl og teknisk gæld | CONCERNS.md contains five named bugs (BUG-01 through BUG-05), eight tech-debt items, four security notes, and two performance bottlenecks — all with file and line references |
</phase_requirements>

---

## Summary

Phase 1 is a documentation-creation phase with no code changes. All source material already exists in `.planning/codebase/` — the task is to transform that analysis into four human-readable Danish markdown files inside a new `docs/` folder at the project root. No external research, library lookups, or API calls are needed; the domain is document authoring, not software implementation.

The audience is Ole, the project owner and sole maintainer, who reads Danish. The docs must be self-contained enough that Ole can understand the project's current state, priorities, and risks without reading any source code. The most time-sensitive piece is ISSUES.md: BUG-01 (hardcoded DST table) will produce wrong event times in Aula from 29 March 2026 onward — 13 days away at research time.

The three plans already sketched in ROADMAP.md (01-01 creates PROJECT_OVERVIEW.md, 01-02 creates WORK_LOG.md and DECISIONS.md, 01-03 creates ISSUES.md) are an appropriate split. Each plan corresponds to one or two requirements and can be verified immediately by reading the output file.

**Primary recommendation:** Write all four docs in a single sequential pass, deriving content exclusively from the `.planning/codebase/` analysis documents. No code reading is needed during this phase.

---

## Standard Stack

### Core
| Tool | Version | Purpose | Why Standard |
|------|---------|---------|--------------|
| Markdown (.md) | CommonMark | Documentation format | Already used throughout .planning/; renders on GitHub and in editors |
| Danish (da) | — | Language for all docs | Ole is a Danish speaker; requirement explicitly states dansk |

### Supporting
| Tool | Version | Purpose | When to Use |
|------|---------|---------|-------------|
| Tables (GFM) | GitHub Flavored Markdown | Structured comparison (bugs by severity, decisions) | Where list-of-items would be harder to scan |
| Admonitions (blockquotes) | Standard markdown `>` | Call out time-critical items like BUG-01 | Use sparingly — only for urgent/critical notices |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Markdown | reStructuredText or AsciiDoc | No benefit; markdown is already the project standard |
| Danish | English | Ole is the explicit audience; Danish is locked |

**Installation:** None required. Plain text files only.

---

## Architecture Patterns

### Recommended Project Structure
```
docs/
├── PROJECT_OVERVIEW.md    # What O2A is, how it works, limitations (DOCS-01)
├── WORK_LOG.md            # Dated entries for work done (DOCS-02)
├── DECISIONS.md           # Why specific technical choices were made (DOCS-03)
└── ISSUES.md              # Known bugs and tech debt, prioritized (DOCS-04)
```

### Pattern 1: Project Overview Document
**What:** A single Danish narrative document explaining the project to a non-developer owner.
**When to use:** DOCS-01
**Structure:**
```
# O2A — Outlook til Aula

## Hvad er O2A?
[1-2 afsnit om kernefunktion og kerneværdi]

## Sådan virker det
[Trin-for-trin synkroniseringsflow på dansk, baseret på ARCHITECTURE.md Data Flow]

## Begrænsninger
[Windows-only, ingen tilbagevendende begivenheder, ingen tovejs-sync]

## Mappestruktur
[Forenklet version af STRUCTURE.md — kun de aktive filer]

## Teknologi
[Forenklet STACK.md — PySide6, pywin32, requests, BeautifulSoup, keyring]
```

### Pattern 2: Work Log Document
**What:** Dated log entries, newest first, each describing what was done and why.
**When to use:** DOCS-02
**Structure:**
```
# Arbejdslog

## 2026-03-16 — Kortlægning af kodebase
**Hvad:** [Beskrivelse af analysen]
**Findings:** [Nøglefund som bullet-liste]
**Konsekvenser:** [Hvad det betyder for videre arbejde]
```

### Pattern 3: Decision Log Document
**What:** One entry per architectural decision, explaining the context, the choice made, and the rationale.
**When to use:** DOCS-03
**Structure per entry:**
```
## BESLUTNING-XX: [Kort titel]
**Dato:** YYYY-MM-DD
**Kontekst:** [Baggrund — hvad var situationen?]
**Valg:** [Hvad blev valgt]
**Begrundelse:** [Hvorfor dette valg]
**Alternativer overvejet:** [Hvad blev fravalgt og hvorfor]
**Konsekvenser:** [Hvad betyder det for fremtidigt arbejde]
```

### Pattern 4: Issues Document
**What:** Organized list of known bugs and tech debt, grouped by severity and category.
**When to use:** DOCS-04
**Structure:**
```
# Kendte problemer

## Kritiske fejl (blokerende)
[BUG-01 DST-tabel — med tidsfriste-advarsel]

## Høj-prioritets fejl
[BUG-02 through BUG-05]

## Teknisk gæld
[Tech debt items from CONCERNS.md]

## Sikkerhed
[Security considerations]

## Skaleringsgrænser
[Scaling limits]
```

### Anti-Patterns to Avoid
- **Writing in English:** All four docs must be in Danish — Ole is the audience, not a developer
- **Copying raw analysis verbatim:** The .planning/codebase/ files are for AI context; docs/ files must be human-readable narratives, not analyst bullet dumps
- **Omitting severity signals:** ISSUES.md must make BUG-01's urgency (DST deadline: 29 March 2026) immediately visible, not buried in a flat list
- **Over-documenting inactive code:** PROJECT_OVERVIEW.md should describe how the system works today (AulaCalendar path), not the dead AulaManager/EventManager paths
- **Creating docs/ inside .planning/:** The docs/ folder goes at the project root, not inside .planning/

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Content for docs | Inferring from source code | .planning/codebase/ analysis documents | The analysis is already complete and verified — re-reading source code wastes time and risks missing nuance already captured |
| Bug severity classification | Guessing priority | REQUIREMENTS.md + CONCERNS.md | BUG-01 through BUG-05 are already named and mapped to Phase 2; severity is clear from impact descriptions |
| Decision rationale | Reconstructing from code | ARCHITECTURE.md + CONCERNS.md | These documents contain explicit statements about why AulaCalendar is canonical, why markers in descriptions, etc. |

**Key insight:** All research for the documentation content is already done. The planning phase should treat this as a content-assembly and writing task, not a research task.

---

## Common Pitfalls

### Pitfall 1: Writing for a developer audience
**What goes wrong:** Docs use technical jargon (HTTP sessions, COM automation, QThreadPool) without explanation, making them inaccessible to Ole as a project owner.
**Why it happens:** The writer is a developer using developer source material.
**How to avoid:** Use Danish lay terms where possible. When technical terms are unavoidable, add a one-sentence explanation. "HTTP-session (forbindelsen til Aulas hjemmeside)" is better than "HTTP session."
**Warning signs:** More than 3 acronyms unexplained on a page.

### Pitfall 2: Missing the DST urgency signal
**What goes wrong:** BUG-01 is listed alongside other bugs without indicating that it triggers in 13 days.
**Why it happens:** Alphabetical or flat bug listing buries time-critical issues.
**How to avoid:** BUG-01 must appear at the top of ISSUES.md under a "Kritisk / Tidskritisk" heading, with an explicit date ("Sommertid 2026 starter 29. marts 2026 — fejlen vil ramme alle begivenheder fra den dato").
**Warning signs:** BUG-01 is not the first item in ISSUES.md.

### Pitfall 3: Documenting AulaManager as an active component
**What goes wrong:** PROJECT_OVERVIEW.md describes both AulaManager and AulaCalendar as live code paths, confusing Ole about what actually runs.
**Why it happens:** Both files exist in the repo and look similar.
**How to avoid:** PROJECT_OVERVIEW.md describes only the active code path (AulaCalendar via aula/ package). DECISIONS.md explains why AulaManager exists but is inactive (BESLUTNING-01 candidate).
**Warning signs:** The word "AulaManager" appears in PROJECT_OVERVIEW.md without being labelled as dødkode (dead code).

### Pitfall 4: Work log entry too vague to be useful
**What goes wrong:** WORK_LOG.md entry reads "Analyserede kodebasen 16. marts" — no findings, no consequences.
**Why it happens:** The writer treats it as a changelog rather than a knowledge log.
**How to avoid:** Each entry must include: what was done, key findings (bullet list), and what this means for Ole (consequences/actions).
**Warning signs:** An entry has no bullet points and is under 5 lines.

### Pitfall 5: Decisions log lists only obvious choices
**What goes wrong:** DECISIONS.md documents "valgte Python fordi det var det eksisterende sprog" — entries that add no value.
**Why it happens:** Padding to reach a certain number of entries.
**How to avoid:** Only document decisions where the rationale is non-obvious or where a future maintainer might reasonably question the choice. The four decisions in the additional context are the right targets: AulaCalendar over AulaManager, sync markers in descriptions, form-scraping for login, GitPython dependency.
**Warning signs:** An entry's "Begrundelse" section is one sentence with no tradeoffs.

---

## Code Examples

This phase has no code. The equivalent "examples" are document structure templates — covered under Architecture Patterns above.

### Key Content Blocks by Document

**PROJECT_OVERVIEW.md — Synkroniseringsflow (from ARCHITECTURE.md):**
```
1. Brugeren klikker "Kør O2A" (eller timeren udløser automatisk kørsel)
2. Programmet logger ind på Aula via UNI-login HTML-formular
3. Outlook-kalender læses via Windows COM-integration — kun aftaler mærket "AULA"
4. Aula-kalender hentes via Aulas REST API — synkroniseringsmærker i aftalebeskrivelserne bruges til at identificere kendte aftaler
5. De to kalendere sammenlignes: nye aftaler oprettes i Aula, ændrede opdateres, slettede fjernes
6. Ved fejl sendes en fejlmail til brugeren via Outlook
```

**DECISIONS.md — Beslutning om AulaCalendar (from ARCHITECTURE.md + CONCERNS.md):**
```
## BESLUTNING-01: AulaCalendar (aula/-pakken) bruges — ikke AulaManager
**Dato:** Forud for kortlægning (historisk beslutning, dokumenteret 2026-03-16)
**Kontekst:** Der eksisterer to parallelle implementationer af Aula API-klienten: AulaManager (aulamanager.py) og AulaCalendar (aula/aula_calendar.py). De indeholder næsten identisk kode.
**Valg:** main.pyw bruger udelukkende AulaCalendar.
**Begrundelse:** AulaCalendar bruger den nyeste API-version (v23), er organiseret som en proper Python-pakke, og er den kodegren der er blevet vedligeholdt. AulaManager bruger v22 og er dødkode.
**Konsekvenser:** AulaManager, EventManager og DatabaseManager bør fjernes i en fremtidig fase (QUAL-01).
```

**ISSUES.md — BUG-01 urgent entry:**
```
## KRITISK — Tidskritisk

### BUG-01: Hardkodet sommertidstabel virker kun til og med 2025
**Prioritet:** KRITISK
**Deadline:** Sommertid 2026 starter 29. marts 2026
**Symptom:** Begivenheder i Aula fra 29. marts 2026 og frem vises med forkert klokkeslæt (én time forskudt).
**Årsag:** outlookmanager.py linje 16–45 bruger en hardkodet liste over sommertidsperioder fra 2021–2025. Begivenheder i 2026 får tildelt vintertids-offset (+01:00) i stedet for sommertids-offset (+02:00).
**Berørte filer:** outlookmanager.py (linje 16–45)
**Løsning (Fase 2):** Erstat hardkodet tabel med Pythons zoneinfo-modul til dynamisk beregning.
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| AulaManager (aulamanager.py) as primary API client | AulaCalendar (aula/aula_calendar.py) | Historical — before this roadmap | Active sync path uses AulaCalendar exclusively; AulaManager is dead code |
| SQLite DatabaseManager for event tracking | Sync markers embedded in Aula event descriptions | Historical | No persistent local state; markers in descriptions are the only cross-run state |
| Tkinter dialog for credentials (in setupmanager.py) | PySide6 UniloginDialog | Historical | GUI credentials flow is now Qt-based; old Tkinter path remains in setupmanager.py CLI flow |

**Deprecated/outdated in the codebase (relevant for docs):**
- AulaManager (aulamanager.py): Parallel API client, uses API v22, dead code — document as such
- EventManager (eventmanager.py): Contains duplicate orchestration logic, not called from main.pyw
- DatabaseManager (databasemanager.py): SQLite recipient/event cache, exists but all calls commented out

---

## Open Questions

1. **Does docs/ already exist at the project root?**
   - What we know: STRUCTURE.md does not list a docs/ directory; it is not in the directory layout
   - What's unclear: Whether any partial docs/ folder was created between codebase mapping and now
   - Recommendation: Plan should include a step to create docs/ before writing files; git mkdir or simply write files with the path

2. **Should WORK_LOG.md have oldest-first or newest-first ordering?**
   - What we know: Common convention is newest-first for changelogs and work logs (easier to read current state)
   - What's unclear: Ole's preference
   - Recommendation: Use newest-first (most recent entry at top) — standard for work logs and easier to maintain

3. **Should ISSUES.md link to specific source files/lines?**
   - What we know: CONCERNS.md includes exact file and line references for every bug and debt item
   - What's unclear: Whether Ole wants/needs source line references or finds them confusing
   - Recommendation: Include file references (e.g., "outlookmanager.py linje 16–45") but skip line numbers for tech debt items that span multiple locations — keep it readable

---

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | None — documentation-only phase |
| Config file | N/A |
| Quick run command | Manual: open each file and verify existence and section headings |
| Full suite command | Manual: read each file end-to-end and check against success criteria in ROADMAP.md |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| DOCS-01 | docs/PROJECT_OVERVIEW.md exists with Danish content covering O2A purpose, sync flow, and limitations | smoke | `test -f docs/PROJECT_OVERVIEW.md` | ❌ Wave 0 — file does not exist yet |
| DOCS-02 | docs/WORK_LOG.md exists with at least one dated entry for 2026-03-16 | smoke | `test -f docs/WORK_LOG.md` | ❌ Wave 0 |
| DOCS-03 | docs/DECISIONS.md exists with entries for AulaCalendar choice, sync markers, form-scraping, and GitPython | smoke | `test -f docs/DECISIONS.md` | ❌ Wave 0 |
| DOCS-04 | docs/ISSUES.md exists with BUG-01 as the first critical item with deadline date | smoke | `test -f docs/ISSUES.md` | ❌ Wave 0 |

Because this is a documentation phase, automated verification is limited to file existence checks. Content quality is verified manually against the success criteria in ROADMAP.md Fase 1.

### Sampling Rate
- **Per task commit:** `test -f docs/PROJECT_OVERVIEW.md && test -f docs/WORK_LOG.md && test -f docs/DECISIONS.md && test -f docs/ISSUES.md`
- **Per wave merge:** Full manual review against ROADMAP.md success criteria
- **Phase gate:** All four files present, all in Danish, BUG-01 prominently flagged with 29 March 2026 date

### Wave 0 Gaps
- [ ] `docs/` directory — does not exist yet; must be created before any file writes
- [ ] `docs/PROJECT_OVERVIEW.md` — covers DOCS-01
- [ ] `docs/WORK_LOG.md` — covers DOCS-02
- [ ] `docs/DECISIONS.md` — covers DOCS-03
- [ ] `docs/ISSUES.md` — covers DOCS-04

All four files are the deliverables of this phase, not pre-existing test infrastructure. Wave 0 for this phase = creating the docs/ folder and the four files.

---

## Sources

### Primary (HIGH confidence)
- `.planning/codebase/ARCHITECTURE.md` — sync flow, layers, key abstractions, error handling strategy
- `.planning/codebase/CONCERNS.md` — all five named bugs (BUG-01 through BUG-05), tech debt, security considerations, performance bottlenecks
- `.planning/codebase/STACK.md` — Python + PySide6 + pywin32 + requests + keyring stack details
- `.planning/codebase/CONVENTIONS.md` — naming patterns, logging conventions, mixed Danish/English log messages
- `.planning/codebase/INTEGRATIONS.md` — Aula REST API (v23), UNI-Login form scraping, Outlook COM, data storage
- `.planning/codebase/STRUCTURE.md` — directory layout, active vs. legacy files
- `.planning/REQUIREMENTS.md` — DOCS-01 through DOCS-04 requirement text and acceptance criteria
- `.planning/ROADMAP.md` — Fase 1 success criteria and plan breakdown
- `.planning/STATE.md` — current project position, known blockers

### Secondary (MEDIUM confidence)
- Additional context provided in the research prompt — confirmed against source documents above

### Tertiary (LOW confidence)
- None

---

## Metadata

**Confidence breakdown:**
- Document content: HIGH — all source material is in .planning/codebase/ analysis documents, fully read and cross-referenced
- Document structure: HIGH — markdown is the established project standard; four-document split matches ROADMAP.md plans exactly
- Validation approach: HIGH — documentation phase has no automated tests; existence checks are the correct smoke test

**Research date:** 2026-03-16
**Valid until:** This research is based on static analysis documents; valid until the codebase changes materially (next meaningful invalidation: after Phase 2 bug fixes land)
