# Beslutningslog

Log over tekniske valg i O2A-projektet med begrundelse. Dokumenterer kun valg der ikke er selvindlysende.

---

## BESLUTNING-01: AulaCalendar bruges — ikke AulaManager

**Dato:** Forud for kortlægning (historisk beslutning, dokumenteret 2026-03-16)

**Kontekst:** Der eksisterer to parallelle implementationer af Aula API-klienten i kodebasen: `AulaManager` (`aulamanager.py`) og `AulaCalendar` (`aula/aula_calendar.py`). De indeholder næsten identisk kode og implementerer de samme metoder — heriblandt hentning, oprettelse, opdatering og sletning af kalenderbegivenheder i Aula.

**Valg:** `main.pyw` bruger udelukkende `AulaCalendar` via `aula/`-pakken.

**Begrundelse:** `AulaCalendar` bruger den nyeste Aula API-version (v23) og er organiseret som en ordentlig Python-pakke med adskilt ansvar. Det er den kodegren der aktivt vedligeholdes og er i brug. `AulaManager` bruger den ældre API-version v22 og er dødkode — ingen del af den aktive synkroniseringssti kalder `AulaManager`. At bruge begge parallelt ville betyde at fejlrettelser skal laves to steder, hvilket er uholdbart.

**Alternativer overvejet:** At bruge `AulaManager` i stedet eller at flette de to implementationer — fravalgt fordi det ville kræve en stor refaktorering uden gevinst i den nuværende fase. Prioriteten er at rette fejl og dokumentere, ikke at omstrukturere.

**Konsekvenser:** `AulaManager`, `EventManager` og `DatabaseManager` bør fjernes i Fase 3 (QUAL-01) for at undgå forvirring og dobbeltvejledning for fremtidige vedligeholdere.

---

## BESLUTNING-02: Synkroniseringsidentitet gemmes i Aulas begivenhedsbeskrivelser

**Dato:** Forud for kortlægning (historisk beslutning, dokumenteret 2026-03-16)

**Kontekst:** Programmet skal på tværs af kørsler vide hvilke Aula-begivenheder der svarer til hvilke Outlook-aftaler, og om en aftale er ændret siden sidst. En ekstern database (SQLite) var implementeret til dette formål men er nu deaktiveret. Der er heller ingen server-side tilstand at læne sig op ad.

**Valg:** Outlook-aftalens `GlobalAppointmentID` (globalt unikt ID tildelt af Outlook) og `LastModificationTime` (tidsstempel for seneste ændring) indlejres som skjulte mærker direkte i Aula-begivenhedens beskrivelsestekst — som linjerne `o2a_outlook_GlobalAppointmentID=...` og `o2a_outlook_LastModificationTime=...`.

**Begrundelse:** Denne løsning eliminerer behovet for en lokal database der skal holdes synkron med Aulas faktiske tilstand. Programmet er tilstandsløst (eng. *stateless*) mellem kørsler — al nødvendig information hentes fra Aula ved hver kørsel. Det gør programmet mere robust, fordi Aula altid er "sandheden" og der er ingen lokal tilstand der kan komme ud af synk. Det var sandsynligvis fravalget af SQLite-løsningen der førte til dette design.

**Alternativer overvejet:** SQLite `DatabaseManager` (`databasemanager.py`) — fravalgt fordi den kræver vedligeholdelse og kan komme ud af synk med Aulas faktiske tilstand, f.eks. hvis begivenheder slettes direkte i Aula uden om programmet.

**Konsekvenser:** Begivenhedsbeskrivelserne i Aula indeholder disse mærker synligt hvis Ole ser dem i Aulas kalendervisning. Mærkerne er nødvendige for korrekt funktion og må ikke slettes manuelt — programmet vil ellers oprette duplikatbegivenheder.

---

## BESLUTNING-03: Login via HTML-formular-scraping

**Dato:** Forud for kortlægning (historisk beslutning, dokumenteret 2026-03-16)

**Kontekst:** Aula tilbyder ikke et offentligt login-API til programmatisk adgang. Programmet skal logge ind som Ole via UNI-Login (den nationale identitetsudbyder til det danske uddannelsessystem) for at tilgå kalender-API'et.

**Valg:** Programmet simulerer en browser ved at analysere og indsende HTML-loginformularer trin for trin (form scraping via `BeautifulSoup` og `requests`). Løsningen understøtter to loginveje: standard UNI-Login (STIL) og en kommunal IDP-løsning for Sønderborg-konti.

**Begrundelse:** Der er ingen officiel API-løsning til programmatisk login på Aula/UNI-Login. Form scraping er den eneste tilgængelige metode der ikke kræver en rigtig browser. Alternativet — browser-automatisering via Selenium eller Playwright — ville tilføje betydelig kompleksitet og afhængigheder til en applikation der ellers er selvstændig og let at distribuere.

**Alternativer overvejet:** Officielt login-API — eksisterer ikke. Browser-automatisering (Selenium/Playwright) — fravalgt som unødvendig kompleksitet og tung distribution. OAuth/SAML-integration — ikke tilgængeligt uden officielt samarbejde med Aula/UNI-Login.

**Konsekvenser:** Login er skrøbelig — ændringer i Aulas eller UNI-Logins HTML-struktur kan bryde login uden advarsel. Der er ingen automatiserede tests af login-flowet. Kræver manuel test mod live Aula ved enhver ændring af login-koden (`aula/aula_connection.py`).

---

## BESLUTNING-04: GitPython bruges til versionsnummer

**Dato:** Forud for kortlægning (historisk beslutning, dokumenteret 2026-03-16)

**Kontekst:** Programmet viser et versionsnummer i GUI'en for at Ole kan se hvilken version der kører. Der eksisterer ikke en separat versionsfil i kodebasen.

**Valg:** `GitPython`-pakken bruges til at læse den seneste git commit-hash og dato direkte fra `.git`-mappen ved opstart. Versionsnummeret vises i GUI'en som f.eks. `2026-03-15 (abc1234)`.

**Begrundelse:** Automatisk versionering uden at skulle opdatere en versionsfil manuelt ved hver ændring. Under normal udvikling via git er dette elegant — versionen afspejler altid præcist hvad der er deployed. Det undgår den typiske glemmefejl hvor kode frigives med et forældet versionsnummer.

**Alternativer overvejet:** En statisk versionsfil (`version.txt`) — ville ikke kræve en git-dependency og ville fungere uanset om `.git`-mappen er til stede. Fravalgt på tidspunktet, sandsynligvis fordi git altid er til stede under udvikling.

**Konsekvenser:** Programmet crasher ved opstart hvis det køres uden en `.git`-mappe — f.eks. som kompileret `.exe` distribueret via PyInstaller. Dette er registreret som BUG-05 og er planlagt rettet i Fase 2 ved at erstatte `GitPython` med en statisk `version.txt`-fil.

---

*Nye beslutninger tilføjes i dette dokument med et stigende BESLUTNING-nummer.*
