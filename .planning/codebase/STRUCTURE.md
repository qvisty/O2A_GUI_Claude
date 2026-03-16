# Codebase Structure

**Analysis Date:** 2026-03-16

## Directory Layout

```
O2A_GUI_Claude/                    # Project root
├── aula/                          # Aula API integration package
│   ├── __init__.py                # Package exports: AulaConnection, AulaEvent, AulaCalendar
│   ├── aula_calendar.py           # CRUD operations on Aula calendar events
│   ├── aula_common.py             # Shared constants (minimal, nearly empty)
│   ├── aula_connection.py         # HTTP session management and login
│   ├── aula_event.py              # AulaEvent and AulaEventCreationErrors domain models
│   └── utils.py                  # Utility helpers
├── images/                        # UI icon assets
│   ├── Aula-logo.jpg
│   ├── exchange.png
│   ├── icon.png
│   ├── ignore.png
│   ├── run.png
│   ├── runer-silhouette-running-fast.png
│   └── switch.png
├── .planning/                     # GSD planning documents (not shipped)
│   └── codebase/
├── main.pyw                       # Application entry point + MainWindow + Worker
├── mainwindow.py                  # Generated Qt UI code for MainWindow (from mainwindow.ui)
├── mainwindow.ui                  # Qt Designer UI definition for the main window
├── unilogindialog.py              # UniloginDialog class (wraps generated UI)
├── unilogindialog.ui              # Qt Designer UI definition for the login dialog
├── ui_mainwindow.py               # Alternate/older generated UI file (may be stale)
├── ui_unilogindialog.py           # Alternate/older generated UI file (may be stale)
├── outlookmanager.py              # Outlook COM integration: read calendar, send mail
├── setupmanager.py                # Credential storage, Outlook category setup, config file
├── calendar_comparer.py           # Set-diff between Outlook and Aula event dictionaries
├── peoplecsvmanager.py            # Reads personer.csv and personer_ignorer.csv
├── eventmanager.py                # Older orchestration class (not in active sync path)
├── aulamanager.py                 # Older Aula API class (not in active sync path)
├── databasemanager.py             # SQLite-backed event tracking (not in active sync path)
├── databaseevent.py               # DatabaseEvent data class
├── test.py                        # Ad-hoc test/scratch file
├── personer.csv                   # User-maintained name mapping (Outlook → Aula)
├── personer_skabelon.csv          # Template for personer.csv (copied on first run)
├── personer_ignorer.csv           # User-maintained ignore list
├── personer_ignorer_skabelon.csv  # Template for personer_ignorer.csv
├── configuration.ini              # Runtime config (username, GUI prefs) — git-ignored
├── o2a.log                        # Runtime log file — git-ignored
├── database.db                    # SQLite database — git-ignored
├── O2A.pyproject                  # PyCharm project file
├── O2A.spec                       # PyInstaller spec (older, references src/)
├── main.spec                      # PyInstaller spec for main.pyw
├── Requirements.txt               # pip dependency list
├── Requirements - Kopi.txt        # Duplicate/backup requirements file
├── updateandrun.bat               # Pulls latest git, then launches main.pyw
├── updateandrun - Kopi.bat        # Backup copy of update script
├── updateandrun_old_script.bat    # Old version of update script
├── starto2a.bat                   # Minimal launcher bat
├── pyinstaller_update.bat.txt     # PyInstaller build instructions (renamed .txt)
├── readme.md                      # Project readme
└── screenshot.PNG                 # Screenshot for documentation
```

## Directory Purposes

**`aula/`:**
- Purpose: Self-contained package for all Aula API interactions
- Contains: HTTP auth (`aula_connection.py`), calendar CRUD (`aula_calendar.py`), domain model (`aula_event.py`)
- Key files: `aula/__init__.py` (re-exports the three main classes), `aula/aula_connection.py`, `aula/aula_calendar.py`

**`images/`:**
- Purpose: Static UI assets bundled with the application
- Contains: PNG/JPG icons used by the Qt tray icon and window
- Generated: No — manually placed

**`.planning/codebase/`:**
- Purpose: GSD analysis documents for AI-assisted development
- Generated: Yes (by GSD tooling)
- Committed: Typically yes

## Key File Locations

**Entry Points:**
- `main.pyw`: Application start, `MainWindow` class, `Worker` threading class, `update_calendar` sync orchestration
- `updateandrun.bat`: Windows shortcut / startup target — runs `git pull` then `python main.pyw`

**Configuration:**
- `configuration.ini`: INI file with `[AULA]` username and `[GUI]` hide-on-startup flag (created at runtime by `SetupManager`)
- `Requirements.txt`: pip dependency declarations
- `main.spec`: PyInstaller packaging spec

**Core Logic:**
- `aula/aula_calendar.py`: All Aula API calls (getEvents, createSimpleEvent, updateEvent, deleteEvent, get_atendees_ids, convert_outlook_appointmentitem_to_aula_event)
- `aula/aula_connection.py`: Login flow and session management; `getAulaApiUrl()` returns `https://www.aula.dk/api/v23/`
- `outlookmanager.py`: Outlook COM reads and error email dispatch
- `calendar_comparer.py`: Set-diff logic for the two event dictionaries
- `setupmanager.py`: Credential read/write; Outlook category creation

**People Name Mapping:**
- `personer.csv`: Two-column CSV (`Outlook navn;AULA navn`) — maintained by the end user
- `personer_ignorer.csv`: Single-column CSV (`Outlook navn`) — attendees to skip silently
- `peoplecsvmanager.py`: Reads the above two files and provides `getPersonData(outlook_name)`

**UI Definitions:**
- `mainwindow.ui`: Qt Designer XML source for the main window layout
- `mainwindow.py`: Python code generated from `mainwindow.ui` — do not edit by hand
- `unilogindialog.ui`: Qt Designer XML source for the credentials dialog
- `unilogindialog.py`: Python code generated from `unilogindialog.ui` — do not edit by hand

**Testing:**
- `test.py`: Ad-hoc scratch file; no test framework present

## Naming Conventions

**Files:**
- Manager classes: `<subject>manager.py` (lowercase, no separator) — e.g., `outlookmanager.py`, `setupmanager.py`, `databasemanager.py`
- Aula sub-modules: `aula_<subject>.py` — e.g., `aula_calendar.py`, `aula_connection.py`
- Generated Qt files: `<windowname>.py` generated from `<windowname>.ui`

**Classes:**
- PascalCase: `OutlookManager`, `AulaCalendar`, `AulaConnection`, `SetupManager`, `CalendarComparer`
- Signal holder classes: `<Subject>Signals` or `<Subject>MangerSignals` — e.g., `WorkerSignals`, `EventMangerSignals`

**Methods:**
- snake_case for all methods
- Private methods prefixed with double underscore: `__delete_aula_events`, `__create_aula_events`, `__read_config_file`
- Qt slot handlers follow `on_<widget>_<signal>` pattern: `on_runO2A_clicked`, `on_runFrequency_valueChanged`

**Directories:**
- Single lowercase word or underscore-separated: `aula/`, `images/`, `.planning/`

## Where to Add New Code

**New Aula API capability (e.g., read messages, handle resources):**
- Add method to `aula/aula_calendar.py` using `self._session`, `self._aula_api_url`, `self._profile_id`
- Export from `aula/__init__.py` if needed externally

**New sync logic (e.g., recurring event handling improvements):**
- Modify `MainWindow.update_calendar` in `main.pyw` or the relevant private `__create/update/delete` methods in the same class

**New GUI dialog:**
- Create `<name>.ui` in the project root with Qt Designer
- Generate `<name>.py` from it: `pyside6-uic <name>.ui -o <name>.py`
- Create a dialog class in `main.pyw` following the `UniloginDialog` pattern (inherit from both the generated class and `QDialog`)

**New configuration setting:**
- Read/write via `SetupManager` in `setupmanager.py` using `self.config` (ConfigParser backed by `configuration.ini`)
- Sensitive values go to keyring: `keyring.set_password("o2a", "<key>", value)`

**Utilities shared across modules:**
- Add to `aula/utils.py` if Aula-specific, or create a new top-level module for cross-cutting helpers

**Name-mapping or filtering logic:**
- Extend `peoplecsvmanager.py` — it reads from CSV files that users edit directly

## Special Directories

**`aula/`:**
- Purpose: Installable Python package for Aula API
- Generated: No
- Committed: Yes

**`images/`:**
- Purpose: UI icon assets
- Generated: No
- Committed: Yes

**`.planning/`:**
- Purpose: GSD AI tooling documents
- Generated: Yes (GSD commands)
- Committed: Yes

---

*Structure analysis: 2026-03-16*
