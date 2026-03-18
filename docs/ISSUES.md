# Kendte problemer

Oversigt over kendte fejl og teknisk gæld i O2A pr. 2026-03-18. Sorteret efter prioritet. BUG-01 til BUG-05 er rettet i Fase 2; teknisk gæld og kendte begrænsninger er stadig åbne.

---

## Rettet i Fase 2

### BUG-01: Hardkodet sommertidstabel virker kun til og med 2025

**Status:** Rettet 2026-03-18 i Fase 2, plan 02-01  
**Tidligere prioritet:** KRITISK  
**Tidligere symptom:** Begivenheder i Aula fra 29. marts 2026 og frem blev vist med forkert klokkeslæt - én time forskudt.  
**Årsag:** `outlookmanager.py` brugte en hardkodet liste over sommertidsperioder fra 2021 til 2025, og den aktive Aula-opslagssti brugte samtidig ét daylight-flag for hele syncvinduet.  
**Berørte filer:** `outlookmanager.py`, `aula/aula_calendar.py`, `main.pyw`  
**Rettet ved:** Delt `zoneinfo`-baseret helper i `aula/timezone_utils.py` bruges nu til både Outlook-konvertering og Aula lookup-vinduer.  
**Verifikation:** Lokale tests dækker mindst `2026-03-28 -> +01:00`, `2026-03-29 -> +02:00`, `2026-07-15 -> +02:00` og `2026-10-25 -> +01:00`.

### BUG-02: Programmet starter ikke på Python 3.12 eller nyere

**Status:** Rettet 2026-03-18 i Fase 2, plan 02-01  
**Tidligere prioritet:** HØJ  
**Tidligere symptom:** Programmet kastede ImportError ved opstart på Python 3.12+.  
**Årsag:** `setupmanager.py` importerede `distutils`, som er fjernet fra standardbiblioteket i Python 3.12.  
**Berørte filer:** `setupmanager.py`  
**Rettet ved:** Den ubrugte `distutils`-import er fjernet.  
**Verifikation:** Lokal smoke-test på Python 3.12. Python 3.13 er stadig en miljøafhængig verifikation der mangler en lokal interpreter.

### BUG-03: Manglende internetforbindelse crasher med fejl i stedet for at vise besked

**Status:** Rettet 2026-03-18 i Fase 2, plan 02-02  
**Tidligere prioritet:** HØJ  
**Tidligere symptom:** Hvis der ingen internetforbindelse var når synkronisering startede, kastede programmet en NameError og viste ingen besked i GUI-logpanelet.  
**Årsag:** `main.pyw` brugte en forkert logger-reference i sync-knapperne, og startup-rækkefølgen gjorde logger-adgang sårbar tidligt i `MainWindow`.  
**Berørte filer:** `main.pyw`  
**Rettet ved:** Internetfejl går nu gennem én helper i `main.pyw` med altid-on GUI-log, throttlet tray-popup og reset efter vellykket sync.  
**Verifikation:** `tests/phase02/test_internet_notifications.py` dækker GUI-log, tray-throttle, reset efter succes og fælles helper-brug i begge sync-knapper.

### BUG-04: Sletning af Aula-begivenhed fejler med NameError

**Status:** Rettet 2026-03-18 i Fase 2, plan 02-02  
**Tidligere prioritet:** HØJ  
**Tidligere symptom:** Hvis en begivenhed ikke kunne slettes fra Aula første forsøg, kastede programmet en NameError og kunne samtidig logge falsk succes i callerne.  
**Årsag:** `aula/aula_calendar.py` indeholdt `s#elf.logger.warning(...)` i `deleteEvent()`-fejlstien, og `main.pyw` behandlede `False` som succes i nogle delete/update-stier.  
**Berørte filer:** `aula/aula_calendar.py`, `main.pyw`  
**Rettet ved:** Typoen i `deleteEvent()` er rettet, og callerne behandler nu kun `True` som succes. `False` og `None` behandles som fejl.  
**Verifikation:** `tests/phase02/test_delete_failure_paths.py` reproducerer failure-pathen og beviser at `False` ikke logges som succes.

### BUG-05: Programmet crasher ved opstart hvis .git-mappen mangler

**Status:** Rettet 2026-03-18 i Fase 2, plan 02-02  
**Tidligere prioritet:** HØJ  
**Tidligere symptom:** Programmet startede ikke hvis det blev kørt udenfor et git-repository, f.eks. som kompileret `.exe` eller i en kopieret runtime-map.  
**Årsag:** `main.pyw` brugte GitPython til at læse version direkte fra `.git` under startup. Hvis `.git` manglede, fejlede appen før GUI'en var klar.  
**Berørte filer:** `main.pyw`, `version.txt`  
**Rettet ved:** Programmet bruger nu git commit-dato hvis `.git` findes, ellers `version.txt`, ellers skjules versionsfeltet helt.  
**Verifikation:** `tests/phase02/test_version_fallback.py` samt lokal no-`.git`-simulation med og uden `version.txt`.

---

## Teknisk gæld

Følgende punkter er ikke akutte fejl men sænker kodekvalitet og vedligeholdelsesevne. Planlagt adresseret i Fase 3.

| ID | Beskrivelse | Berørte filer | Fase |
|----|-------------|---------------|------|
| QUAL-01 | AulaManager, EventManager og DatabaseManager er dødkode der kopierer AulaCalendar-logikken. Bug-rettelser skal i dag laves to steder. | `aulamanager.py`, `eventmanager.py`, `databasemanager.py` | Fase 3 |
| QUAL-02 | Flere steder i koden bruger `except: pass` eller tilsvarende meget brede fejlgreb, så fejl forsvinder uden tydelig logning. | `aula_connection.py`, `aula_calendar.py`, `aulamanager.py`, `outlookmanager.py` | Fase 3 |
| QUAL-03 | Hjælpefunktioner som `url_fixer`, `teams_url_fixer` og `calulate_day_of_the_week_mask` er kopieret mellem flere filer. | `aula_calendar.py`, `aulamanager.py`, `eventmanager.py`, `aula/utils.py` | Fase 3 |

## Ydeevne

| ID | Beskrivelse | Berørte filer | Fase |
|----|-------------|---------------|------|
| PERF-01 | Deltager-navne slås op via Aulas søge-API for hver begivenhed, og der er indlagt pauser mellem forsøg. En lokal cache er implementeret men deaktiveret, så synkronisering bliver langsom ved mange deltagere. | `aula_calendar.py`, `databasemanager.py` | Fase 4 |

## Sikkerhedsnoter

Disse punkter er ikke akutte for et lokalt desktopprogram men er dokumenteret for fuldstændighedens skyld:

- Fejlnotifikationsmails CC'er en hardkodet e-mailadresse (`olex3397@skolens.net`) - potentielt fortrolige begivenhedsoplysninger videresendes til tredjemand.
- Adgangskode printes til terminal under det gamle CLI-setup-flow i `setupmanager.py` - benyttes ikke via GUI-opstartsstien, men bør stadig fjernes ved lejlighed.

## Begrænsninger (by design)

Disse punkter er kendte begrænsninger der ikke er planlagt rettet i den nuværende roadmap:

- Tilbagevendende begivenheder synkroniseres ikke korrekt - de oprettes som enkeltbegivenheder uden tydelig brugeradvarsel.
- Synkroniseringsvinduet er hardkodet til cirka 1 år frem - begivenheder langt ude i fremtiden synkroniseres ikke.
- Maksimalt synkroniseringsinterval via GUI er 4 timer.
