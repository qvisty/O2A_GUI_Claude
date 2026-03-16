# Coding Conventions

**Analysis Date:** 2026-03-16

## Naming Patterns

**Files:**
- Module files use lowercase `snake_case`: `aulamanager.py`, `outlookmanager.py`, `databasemanager.py`, `peoplecsvmanager.py`, `calendar_comparer.py`
- Subpackage files are prefixed with the package name: `aula/aula_calendar.py`, `aula/aula_connection.py`, `aula/aula_event.py`
- Generated UI files are prefixed with `ui_`: `ui_mainwindow.py`, `ui_unilogindialog.py`
- Entry point uses `.pyw` extension for windowless execution: `main.pyw`

**Classes:**
- PascalCase: `AulaCalendar`, `AulaConnection`, `AulaEvent`, `EventManager`, `OutlookManager`, `DatabaseManager`, `SetupManager`, `PeopleCsvManager`
- Signal wrapper classes are named `<ClassName>Signals`: `WorkerSignals`, `EventMangerSignals`, `AulaMangerSignals`
- Note: `AulaMangerSignals` contains a typo (missing 'a' in Manager) — follow the existing typo in that class

**Methods:**
- camelCase for public methods: `getEvents`, `createSimpleEvent`, `findRecipient`, `deleteEvent`, `getAulaApiUrl`
- snake_case for some newer methods: `update_calendar`, `find_recipient_alias`, `should_ignore_recipient`, `get_atendees_ids`
- Private methods use double-underscore prefix: `__remove_html_tags`, `__from_outlookobject_to_aulaevent`, `__read_config_file`, `__write_config_file`
- Dunder-prefixed single-word helpers nest inside outer methods as closures: `get_daylight_timezone`, `format_as_aula_date`, `day_of_week_convert`

**Variables:**
- camelCase is common for local variables: `aulaEvents`, `startTimeFormattet`, `monthsDiff`, `lookUp_begin`
- snake_case also used: `aula_event`, `login_response`, `error_messages_string`
- Naming is inconsistent — both styles coexist within same files

**Constants / Outlook day-of-week codes:**
- Prefixed with `ol` followed by PascalCase: `olFriday = 32`, `olMonday = 2`, defined as local variables rather than module-level constants

**Instance attributes on data objects:**
- snake_case on data model classes (`AulaEvent`, `AulaEventCreationErrors`): `start_date_time`, `attendee_ids`, `outlook_global_appointment_id`

## Code Style

**Formatting:**
- No automated formatter detected (no `.prettierrc`, `pyproject.toml` with Black, or `setup.cfg` with flake8 settings)
- Indentation: 4 spaces throughout
- Trailing whitespace present in several files
- Inconsistent blank lines between methods (1–2 lines)

**Linting:**
- No linting configuration detected (no `.flake8`, `.pylintrc`, `pyproject.toml`, or `tox.ini`)
- Code contains unused imports (e.g., duplicate `import re` in `aulamanager.py`, `from sys import getprofile` imported but never used)
- Dead code exists: unreachable code after `return` statements (e.g., `aula/aula_calendar.py` line 736, `aulamanager.py` line 151)

## Import Organization

**Pattern observed:**
1. Standard library imports (`import json`, `import re`, `import logging`, `import datetime`)
2. Third-party imports (`import requests`, `from bs4 import BeautifulSoup`, `from PySide6.QtCore import ...`)
3. Local imports (`from aula.aula_event import AulaEvent`, `from setupmanager import SetupManager`)

**No formal ordering enforced** — imports are not always grouped and some are placed inside functions (e.g., `import re` inside `__remove_html_tags`, `import os` inside `create_task`).

**Package exports:**
- `aula/__init__.py` explicitly re-exports: `AulaConnection`, `AulaEvent`, `AulaCalendar`, `utils`, `aula_common`
- All other modules are imported directly by filename at the project root level (no package structure for root modules)

## Error Handling

**Patterns:**
- Specific exception types caught where known: `requests.exceptions.ConnectionError`, `sqlite3.OperationalError`, `configparser.DuplicateSectionError`, `TypeError`, `UnboundLocalError`, `OSError`
- Bare `except:` clauses are common — used to silently swallow all errors in login loops (`aula/aula_connection.py` lines 93, 192, 219, 339): `except: pass`
- `try/except Exception` used broadly in `databasemanager.py` for database init
- Functions signal failure via return values (`None`, `False`, `True`) rather than raising exceptions
- HTTP responses checked by comparing `response["status"]["message"] == "OK"` rather than HTTP status codes
- `requests.exceptions.Timeout` caught specifically in `aula/aula_calendar.py` for API POST calls

**Do not:**
- Do not raise exceptions from business logic — follow the existing return-value pattern
- Do not replace bare `except:` blocks in login flows with specific exceptions without understanding the original intent (they protect multi-step web scraping loops)

## Logging

**Framework:** Python standard library `logging` module

**Logger name:** All components use the named logger `'O2A'`:
```python
self.logger = logging.getLogger('O2A')
```

**Handler setup** (in `main.pyw`):
- `FileHandler` at DEBUG level → `o2a.log`
- `StreamHandler` at DEBUG level → stdout
- Custom `QtHandler` at INFO level → GUI text widget

**Log level usage:**
- `logger.debug()` — field-level detail, loop internals, lookup tracing
- `logger.info()` — normal operation events ("Begivenheden blev oprettet", "Login lykkedes")
- `logger.warning()` — recoverable failures ("Springer over grundet fejl", failed event creation)
- `logger.critical()` — unrecoverable conditions (login failure, connection error)

**Mixed language:** Log messages alternate between Danish and English within the same file. Danish is more prevalent in user-facing messages; English appears in older/debug sections.

**`print()` calls:** `print()` remains in several places alongside logger calls, particularly in `aulamanager.py`, `aula/aula_connection.py`, `setupmanager.py`, and `main.pyw`. These are debug remnants, not the primary logging mechanism. New code should use `self.logger` instead.

## Comments

**When to Comment:**
- Inline comments explain non-obvious Outlook COM constants: `# Værdien 2 betyder privat`, `# olFriday = 32  # Friday`
- API format strings documented inline: `#FORMAT:"2021-05-17 08:00:00.0000+02:00"`
- TODO comments present for known deferred work (see CONCERNS.md)
- Source attribution comments used: `#FROM: https://...`

**Comment style:**
- `#` inline comments for most code
- Docstrings used in some Signal classes (`WorkerSignals`, `AulaMangerSignals`) but absent from most methods
- No type annotation docstrings — type hints used sparingly (return types on a few newer methods: `-> LoginStatus`, `-> str|str`, `-> bool`)

## Function Design

**Size:** Functions range from 5 to 100+ lines. Large functions like `getEvents` (~90 lines), `login_with_stil` (~130 lines), and `update_aula_calendar` (~65 lines) are not broken down.

**Parameters:** Typically 0–4 parameters. Data objects (`AulaEvent`) passed as single parameter rather than individual fields.

**Return Values:**
- Boolean (`True`/`False`) for success/failure of API mutations
- `None` for not-found lookups or failures
- Tuples for dual-outcome: `createSimpleEvent` returns `(event_id, "SUCCESS")` or `(None, json_response_dump)`
- Domain objects (`AulaEvent`, `LoginStatus`) for login and conversion operations

**Nested functions:** Closures defined inside methods are used for local helper conversions (e.g., `outlook_pattern_to_aula_pattern`, `get_daylight_timezone`, `format_as_aula_date`). This pattern is acceptable but makes testing harder.

## Module Design

**Exports:**
- `aula/` is the only proper Python package; all root `.py` files are scripts imported by direct name
- `aula/__init__.py` provides clean public API for the package

**Class design:**
- Most classes hold a `self.logger` instance obtained via `logging.getLogger('O2A')`
- `AulaCalendar` depends on `AulaConnection` injected via constructor — dependency injection pattern used here
- Other managers (`OutlookManager`, `SetupManager`) are instantiated inline within methods rather than injected

**Qt signals:**
- Worker threads communicate results via `QObject`-based signal classes
- Signal class is always a separate inner `QObject` subclass named `<Worker>Signals`
- `@Slot()` decorator used on thread `run()` methods

---

*Convention analysis: 2026-03-16*
