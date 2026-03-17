# Phase 02: fejlrettelser - Context

**Gathered:** 2026-03-18
**Status:** Ready for planning

<domain>
## Phase Boundary

Ret BUG-01 til BUG-05, så applikationen starter stabilt, viser korrekte tider i 2026 og frem, og ikke crasher i de kendte fejlstier. Fasen afklarer hvordan fejlrettelserne skal implementeres og valideres, men udvider ikke scope med nye capabilities.

</domain>

<decisions>
## Implementation Decisions

### Internetfejl-feedback
- Fejlkanaler for manglende internet skal samles bag et centralt valg i koden, så appen er forberedt til GUI-log, tray-besked og modal.
- Standardvalg i koden skal være `GUI + tray`.
- GUI-log skal altid skrives internt, også når vinduet er skjult eller appen starter minimeret.
- Tray-besked skal kun vises første gang ved gentagne internetfejl, indtil en vellykket sync nulstiller tilstanden.
- Modal skal være implementerbar som mulighed, men ikke aktiv som default.

### Versionsvisning uden .git
- Versionsfeltet skal ligge så tæt som muligt på Oles eksisterende valg i koden.
- Versionsvisning skal derfor fortsat være datobaseret, ikke semver-baseret.
- Når `.git` findes, må appen fortsat bruge git-baseret dato.
- Når `.git` ikke findes, skal appen falde tilbage til en statisk metadatafil som `version.txt`.
- Hvis `version.txt` mangler, skal versionsfeltet skjules helt i stedet for at vise placeholder-tekst.

### Scope for fejlrettelser og nærliggende følgefejl
- Fase 2 fokuserer stadig på BUG-01 til BUG-05.
- Små, oplagte følgefejl tæt på samme arbejde må gerne rettes med det samme i samme fase.
- Packaging- eller opstartsfejl skal rettes i Fase 2, hvis de faktisk påvirker korrekt kørsel eller verificering af bugfixene.
- Teknisk gæld uden praktisk betydning for denne fase kan vente til senere.
- Tradeoffs afgøres fra sag til sag, men med bias mod at rette nærliggende fejl nu.

### Valideringsniveau
- Verifikation i Fase 2 skal være så grundig, som det giver mening.
- Standard er, at Claude skal køre noget lokalt for at validere ændringen.
- Når det er muligt, skal den konkrete bug reproduceres og derefter verificeres som rettet.
- For BUG-05 skal verifikation mindst omfatte no-`.git`-simulation og bekræftet Python-start; packaging-/exe-nær verificering skal også med, hvis det er praktisk muligt.
- For BUG-01 skal bevisniveauet være enhedsnær verifikation af tidszoneberegningen plus app-nær verifikation med konkrete 2026-datoeksempler.
- Hvis fuld verifikation ikke er mulig pga. live Outlook/Aula-afhængigheder, skal begrænsningen dokumenteres både i slutsvaret og i plan-/summary-verifikation.

### Claude's Discretion
- Den konkrete kodeform for det centrale valg af fejlkanaler.
- Detaljer om, hvordan tray-throttling nulstilles efter en vellykket sync.
- Den præcise balance mellem runtime-fix og mindre følgefejl, når flere små fejl dukker op i samme filområde.
- Hvor langt packaging-/exe-nær verificering af BUG-05 kan føres i praksis i dette miljø.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `main.pyw`: Aktiv entrypoint og stedet hvor BUG-03 og BUG-05 rammer den brugerrettede runtime.
- `setupmanager.py`: Centralt sted for app-konfiguration og naturligt integrationspunkt hvis en lille runtime-indstilling skal bæres videre i kode eller config.
- `aula/aula_calendar.py`: Aktiv Aula CRUD-klient; BUG-04 ligger her.
- `outlookmanager.py`: Aktiv Outlook-integration; BUG-01 ligger her.

### Established Patterns
- Den aktive runtime-sti er `main.pyw` -> `SetupManager` -> `AulaConnection` / `AulaCalendar` -> `OutlookManager`.
- Arvekode i `aulamanager.py` og `eventmanager.py` er ikke autoritativ for Fase 2-fixes.
- GUI-status og baggrundskørsel styres allerede i `main.pyw` via Qt-signaler, tray-ikon og logpanel.
- Kodebasen har ingen automatiseret test-suite; validering må derfor være målrettet lokal runtime-verifikation og dokumenteret manuel begrænsning.

### Integration Points
- Internetfejl-feedback integreres i `on_runO2A_clicked` og `on_forcerunO2A_clicked` i `main.pyw`.
- Versionsfallback uden `.git` integreres omkring `program_version_label`-sætningen i `MainWindow.setup_gui`.
- DST-fix integreres i `OutlookManager.is_in_daylight` eller en nærliggende helper med samme ansvar.
- Sletningsfix for BUG-04 integreres i `AulaCalendar.deleteEvent`.

</code_context>

<specifics>
## Specific Ideas

- Brugeren ønsker, at programmet forberedes til alle tre fejlkanaler for internetfejl, men at de aktive kanaler afgøres ét sted i koden via et valg.
- Fejlrettelser skal ikke være minimale bare for scope-disciplinens skyld; nærliggende fejl bør tages med, når det er billigt og sikkert.
- Målet for verifikation er fejlsikkerhed frem for minimumsdokumentation.

</specifics>

<deferred>
## Deferred Ideas

None - discussion stayed within phase scope.

</deferred>

---

*Phase: 02-fejlrettelser*
*Context gathered: 2026-03-18*
