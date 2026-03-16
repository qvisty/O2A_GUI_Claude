# Technology Stack

**Analysis Date:** 2026-03-16

## Languages

**Primary:**
- Python 3 - All application logic, GUI, API integration

**Secondary:**
- Batch Script (`.bat`) - Startup, update, and environment bootstrap (`updateandrun.bat`)

## Runtime

**Environment:**
- CPython (Windows only - requires `pywin32`, `winshell`, `win32com`)
- Minimum Python 3 required (f-strings, type hints used throughout)

**Package Manager:**
- pip - Standard CPython package manager
- Lockfile: `Requirements.txt` present (pinned with `>=` minimum versions, not exact pins)

**Virtual Environment:**
- `venv` - Created automatically by `updateandrun.bat` if not present at `venv/`

## Frameworks

**Core:**
- PySide6 >= 6.9.0 - Qt6 GUI framework for main window, system tray, dialogs, threading

**Build/Distribution:**
- PyInstaller - Spec file at `O2A.spec` and `main.spec`; produces `O2A` executable
  - UPX compression enabled
  - Console window disabled (`console=False`)

## Key Dependencies

**Critical:**
- `PySide6 >= 6.9.0` - Entire GUI layer; `QMainWindow`, `QThreadPool`, `QRunnable`, `QSystemTrayIcon`
- `pywin32` (latest) - Windows COM automation for Microsoft Outlook integration via `win32com.client`
- `requests >= 2.32.3` - All HTTP communication with Aula REST API
- `beautifulsoup4 >= 4.13.4` - HTML parsing of Aula login page forms during authentication
- `keyring >= 25.6.0` - Secure OS keyring storage for Aula password (`o2a` service name)
- `GitPython >= 3.1.44` - Used at runtime in `main.pyw` to read git commit SHA/date for version display

**Data Handling:**
- `python-dateutil >= 2.9.0` - `relativedelta` for date arithmetic (last Sunday calculation, month stepping)
- `pytz >= 2025.2` - Timezone support
- `winshell` - Windows shell operations (startup folder path, shortcut creation)

**Infrastructure:**
- `configparser` (stdlib) - INI file config at `configuration.ini`
- `sqlite3` (stdlib) - Local SQLite database (`database.db`) via `databasemanager.py`
- `csv` (stdlib) - CSV reading for name alias files (`personer.csv`, `personer_ignorer.csv`)
- `logging` (stdlib) - Structured logging to file (`o2a.log`), console, and GUI widget

## Configuration

**Application Config:**
- `configuration.ini` - INI format, managed by `setupmanager.py`
  - `[AULA]` section: `username` key (plaintext username only)
  - `[GUI]` section: `hideonstartup` boolean
- Password stored separately in OS keyring: service `o2a`, key `aula_password`

**User Data Files (runtime, not committed):**
- `personer.csv` - Outlook-to-Aula name alias mapping (`Outlook navn;AULA navn` columns)
- `personer_ignorer.csv` - Names to silently skip (`Outlook navn` column)
- `o2a.log` - Runtime log file

**Build:**
- `O2A.spec` / `main.spec` - PyInstaller build specs
- `O2A.pyproject` - Project file listing all source files (not a standard pyproject.toml)

## Platform Requirements

**Development:**
- Windows only (hard dependency on `pywin32`, `winshell`, `win32com.client`, `ctypes.windll`)
- Microsoft Outlook must be installed and configured (COM automation required)
- Python 3 installed system-wide or via `py` launcher

**Production:**
- Windows desktop machine with Outlook running
- Internet access to `www.aula.dk`, `login.aula.dk`
- `updateandrun.bat` handles `git pull`, venv creation, pip install, and launch

---

*Stack analysis: 2026-03-16*
