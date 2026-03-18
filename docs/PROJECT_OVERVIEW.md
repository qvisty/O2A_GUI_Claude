# O2A - Outlook til Aula

## Hvad er O2A?

O2A er et Windows-desktopprogram der automatisk holder dine Outlook-kalenderaftaler synkroniseret med Aula-kalenderen. Programmet overvåger din Outlook-kalender og sørger for, at alle aftaler mærket med kategorien "AULA" til enhver tid afspejler den korrekte tilstand i Aula - uden at du behøver gøre noget manuelt.

Kerneværdien er enkel: Du opretter og redigerer aftaler i Outlook som du plejer, og mærker dem blot med kategorien "AULA". O2A klarer resten - det opretter nye aftaler i Aula, opdaterer ændrede aftaler og fjerner aftaler du har slettet i Outlook.

## Sådan virker det

Synkroniseringen foregår automatisk i baggrunden. Her er hvad der sker trin for trin, hver gang O2A kører:

1. **Kørsel startes** - enten ved at du klikker "Kør O2A" i programmet, eller automatisk når timeren udløser en ny kørsel.
2. **Login til Aula** - programmet logger automatisk ind på Aula via UNI-login ved hjælp af dit gemte brugernavn og din adgangskode.
3. **Outlook-kalender læses** - programmet henter dine kalenderaftaler fra Microsoft Outlook via Windows COM-integration; kun aftaler mærket med kategorien "AULA" eller "AULA Institutionskalender" hentes.
4. **Aula-kalender hentes** - programmet henter dine eksisterende aftaler fra Aula via Aulas API og genkender sine egne aftaler via skjulte mærker i beskrivelserne (`o2a_outlook_GlobalAppointmentID` og `o2a_outlook_LastModificationTime`).
5. **Sammenligning og synkronisering** - de to kalendere sammenlignes: nye aftaler oprettes i Aula, ændrede aftaler opdateres, og aftaler du har slettet i Outlook fjernes fra Aula.
6. **Fejlhåndtering** - hændelser og fejl vises i programmets logpanel og skrives til `o2a.log`. Fejl under oprettelse eller opdatering kan også udløse fejlmail via Outlook.

Programmet beregner nu sommertid og vintertid dynamisk for danske datoer via Pythons tidszonebibliotek i stedet for en hardkodet tabel. Det betyder at begivenheder i 2026 og frem ikke længere er bundet til en manuelt vedligeholdt liste over sommertidsperioder.

## Hvad sker der ved fejl?

Alle hændelser og fejl under synkroniseringen skrives løbende til logfilen `o2a.log` og vises i realtid i programmets logpanel.

Hvis der ikke er internetforbindelse ved synkroniseringsstart, logges fejlen nu altid i GUI'en, og programmet kan samtidig vise en tray-notifikation uden at spamme brugeren ved gentagne fejl. Tray-notifikationen nulstilles igen efter en vellykket sync.

Hvis der opstår fejl ved oprettelse eller opdatering af aftaler i Aula, kan programmet sende en detaljeret fejlmail via Outlook, så du kan se hvilke aftaler der ikke blev synkroniseret korrekt.

## Begrænsninger

Det er vigtigt at kende disse begrænsninger, inden du bruger programmet:

- **Kun Windows** - programmet kræver Microsoft Outlook installeret på Windows og kan ikke bruges på Mac eller Linux.
- **Tilbagevendende begivenheder synkroniseres ikke korrekt** - aftaler der gentager sig synkroniseres ikke som ægte tilbagevendende Aula-begivenheder.
- **Ingen tovejs-synkronisering** - ændringer du foretager direkte i Aula kan blive overskrevet ved næste synkronisering. Outlook er altid "sandheden".
- **Kun cirka 1 år frem** - programmet synkroniserer kun aftaler frem til cirka ét år fra dags dato.
- **Kun AULA-mærkede aftaler** - kun Outlook-aftaler mærket med kategorien "AULA" eller "AULA Institutionskalender" synkroniseres.
- **Python 3.13 er ikke verificeret lokalt endnu** - Python 3.12-startblokkeringen er rettet, men 3.13 mangler stadig miljønær verifikation på en maskine hvor den interpreter findes.

## Mappestruktur (aktive filer)

Nedenstående tabel viser de vigtigste filer i projektet og hvad de gør:

| Fil / mappe | Formål |
|---|---|
| `main.pyw` | Programmets startpunkt. Håndterer GUI, synkroniseringslogik, tray-adfærd og startup-flow. |
| `aula/` | Pakke med al Aula-kommunikation. `aula_calendar.py` er den aktive kode. |
| `aula/timezone_utils.py` | Delt helper til dynamisk Copenhagen-offset og Aula-datetime-formattering. |
| `outlookmanager.py` | Læser kalenderaftaler fra Outlook og sender fejlmails via Windows COM. |
| `calendar_comparer.py` | Sammenligner Outlook- og Aula-kalendere og finder hvilke aftaler der skal oprettes, opdateres eller slettes. |
| `setupmanager.py` | Håndterer konfiguration, login-indstillinger og opbevaring af adgangskode. |
| `peoplecsvmanager.py` | Mapper Outlook-navne til Aula-navne via `personer.csv`. |
| `configuration.ini` | Brugerkonfiguration. |
| `personer.csv` | Navne-alias-liste fra Outlook-navn til Aula-navn. |
| `personer_ignorer.csv` | Navne der skal ignoreres ved synkronisering. |
| `version.txt` | Fallback-metadata til versionsvisning når `.git` ikke er til stede. |
| `o2a.log` | Logfil med hændelser og fejl. |
| `updateandrun.bat` | Startscript der opdaterer programmet og starter det. |

**Bemærk:** Filerne `aulamanager.py`, `eventmanager.py` og `databasemanager.py` findes stadig i repoet, men de er ikke den aktive kodevej og betragtes som teknisk gæld.

## Teknologi

Programmet er bygget med følgende teknologier:

- **Python 3** - al logik er skrevet i Python.
- **PySide6** - GUI-framework til vindue, systembakke-ikon og dialoger.
- **pywin32** - Windows-integration til Outlook via COM.
- **requests + BeautifulSoup** - HTTP-kommunikation og HTML-parsing til Aula-login.
- **keyring** - sikker opbevaring af adgangskode i Windows Credential Manager.
- **zoneinfo** - dynamisk beregning af dansk sommertid og vintertid.
- **configuration.ini** - tekstbaseret brugerkonfiguration.

## Opsætning og kørsel

Start programmet ved at dobbeltklikke på `updateandrun.bat`. Scriptet håndterer automatisk:

- hentning af seneste kode fra git-repositoriet
- oprettelse af virtuelt Python-miljø hvis det ikke allerede findes
- installation af nødvendige pakker
- opstart af O2A

Programmet vises herefter i Windows-systembakken. Du kan starte en manuel synkronisering fra programmet eller lade det køre automatisk med det interval du har valgt.
