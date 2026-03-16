# O2A — Outlook til Aula

## Hvad er O2A?

O2A er et Windows-desktopprogram der automatisk holder dine Outlook-kalenderaftaler synkroniseret med Aula-kalenderen. Programmet overvåger din Outlook-kalender og sørger for, at alle aftaler mærket med kategorien "AULA" til enhver tid afspejler den korrekte tilstand i Aula — uden at du behøver gøre noget manuelt.

Kerneværdien er enkel: Du opretter og redigerer aftaler i Outlook som du plejer, og mærker dem blot med kategorien "AULA". O2A klarer resten — det opretter nye aftaler i Aula, opdaterer ændrede aftaler og fjerner aftaler du har slettet i Outlook.


## Sådan virker det

Synkroniseringen foregår automatisk i baggrunden. Her er hvad der sker trin for trin, hver gang O2A kører:

1. **Kørsel startes** — enten ved at du klikker "Kør O2A" i programmet, eller automatisk når timeren udløser en ny kørsel (op til hver 4. time, alt efter hvad du har indstillet)
2. **Login til Aula** — programmet logger automatisk ind på Aula via UNI-login (den nationale loginløsning for danske skoler) ved hjælp af dit gemte brugernavn og din adgangskode
3. **Outlook-kalender læses** — programmet henter dine kalenderaftaler fra Microsoft Outlook via Windows COM-integration (et Windows-interface der lader programmer tale med Outlook); kun aftaler mærket med kategorien "AULA" eller "AULA Institutionskalender" hentes
4. **Aula-kalender hentes** — programmet henter dine eksisterende aftaler fra Aula via Aulas REST API (programmeringsgrænsefladen til Aula, version 23); det genkender sine egne aftaler via skjulte mærker gemt i aftalebeskrivelserne (`o2a_outlook_GlobalAppointmentID`)
5. **Sammenligning og synkronisering** — de to kalendere sammenlignes: nye aftaler oprettes i Aula, ændrede aftaler opdateres, og aftaler du har slettet i Outlook fjernes fra Aula
6. **Fejlhåndtering** — eventuelle fejl under oprettelse eller opdatering vises i programmets logpanel og sendes som en HTML-fejlmail til dig via Outlook


## Hvad sker der ved fejl?

Alle hændelser og fejl under synkroniseringen skrives løbende til logfilen `o2a.log` og vises i realtid i programmets logpanel. Hvis der opstår fejl ved oprettelse eller opdatering af aftaler i Aula, sender programmet automatisk en detaljeret fejlmail til dig via Outlook, så du kan se præcis hvilke aftaler der ikke blev synkroniseret korrekt. Login-fejl afsluttes med en fejlstatus og notificeres ligeledes via e-mail.


## Begrænsninger

Det er vigtigt at kende disse begrænsninger, inden du bruger programmet:

- **Kun Windows** — programmet kræver Microsoft Outlook installeret på Windows og kan ikke bruges på Mac eller Linux
- **Tilbagevendende begivenheder synkroniseres ikke korrekt** — aftaler der gentager sig (f.eks. et ugentligt møde hver mandag) synkroniseres som separate enkeltaftaler i Aula i stedet for som én tilbagevendende begivenhed. Programmet viser ingen advarsel om dette i dag (kendt problem)
- **Ingen tovejs-synkronisering** — ændringer du foretager direkte i Aula-kalenderen overskrives ved næste synkronisering. Outlook er altid "sandheden"
- **Kun ca. 1 år frem** — programmet synkroniserer kun aftaler frem til cirka ét år fra dags dato
- **Kun AULA-mærkede aftaler** — kun Outlook-aftaler der er mærket med kategorien "AULA" (eller "AULA Institutionskalender") synkroniseres; alle andre aftaler ignoreres


## Mappestruktur (aktive filer)

Nedenstående tabel viser de vigtigste filer i projektet og hvad de gør:

| Fil / mappe | Formål |
|---|---|
| `main.pyw` | Programmets startpunkt — håndterer GUI, synkroniseringslogik og baggrundstråde |
| `aula/` | Pakke med al Aula API-kommunikation; `aula_calendar.py` er den aktive kode |
| `outlookmanager.py` | Læser kalenderaftaler fra Outlook og sender fejlmails via Windows COM |
| `calendar_comparer.py` | Sammenligner de to kalendere og finder hvilke aftaler der skal oprettes, opdateres eller slettes |
| `setupmanager.py` | Håndterer konfiguration, login-indstillinger og sikker opbevaring af adgangskode |
| `peoplecsvmanager.py` | Mapper Outlook-navne til Aula-navne via `personer.csv` |
| `configuration.ini` | Brugerkonfiguration (brugernavn, indstillinger) — oprettes automatisk |
| `personer.csv` | Navne-alias-liste: Outlook-navn → Aula-navn (vedligeholdes af dig) |
| `personer_ignorer.csv` | Navne der skal ignoreres ved synkronisering (vedligeholdes af dig) |
| `o2a.log` | Logfil med alle hændelser og fejl — oprettes automatisk ved kørsel |
| `updateandrun.bat` | Startscript — opdaterer programmet og starter det op |

**Bemærk:** Filerne `aulamanager.py`, `eventmanager.py` og `databasemanager.py` findes i kodebasen, men de er dødkode — de bruges ikke af den aktive synkronisering og kan ignoreres.


## Teknologi

Programmet er bygget med følgende teknologier:

- **Python 3** — Programmeringssprog som al logik er skrevet i
- **PySide6** — GUI-framework (Qt6; det grafiske bibliotek der bruges til vindue, systembakke-ikon og dialoger)
- **pywin32** — Windows-integration (bruges til at tale med Microsoft Outlook via COM-automation)
- **requests + BeautifulSoup** — HTTP-kommunikation og HTML-parsing (bruges til Aula-login via UNI-login)
- **keyring** — Sikker opbevaring af adgangskode i Windows Credential Manager (adgangskoden gemmes aldrig i klartekst)
- **configuration.ini** — Brugerkonfiguration i tekstformat (brugernavn og GUI-indstillinger)


## Opsætning og kørsel

Start programmet ved at dobbeltklikke på `updateandrun.bat`. Dette script håndterer automatisk:
- Hentning af seneste kode fra git-repositoriet
- Oprettelse af virtuelt Python-miljø (venv) hvis det ikke allerede eksisterer
- Installation af nødvendige pakker
- Opstart af O2A

Programmet vises herefter i Windows-systembakken (proceslinjen nede til højre). Du kan starte en manuel synkronisering ved at klikke på ikonet, eller lade programmet køre automatisk med det interval du har valgt.
