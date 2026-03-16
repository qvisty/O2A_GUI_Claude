# Testing Patterns

**Analysis Date:** 2026-03-16

## Test Framework

**Runner:**
- No test framework detected. No `pytest`, `unittest`, `nose`, or any other test runner is configured.
- No `pytest.ini`, `setup.cfg [tool:pytest]`, `pyproject.toml [tool.pytest]`, `tox.ini`, or `jest.config.*` files exist.

**Assertion Library:**
- Not applicable — no automated tests present.

**Run Commands:**
```bash
# No test commands configured
```

## Test File Organization

**Location:**
- `test.py` exists at the project root but is a manual integration script, not an automated test suite.

**`test.py` content:**
- Reads credentials from `SetupManager`
- Instantiates `AulaConnection`, logs in
- Manually constructs an `AulaEvent` with hardcoded data
- Calls `AulaCalendar.createSimpleEvent(aula_event)`
- No assertions, no test framework, no teardown
- Functions as an ad-hoc smoke test requiring live AULA credentials and network access

**Naming:**
- No `*.test.py` or `*_test.py` files exist
- No `tests/` directory exists

## Test Structure

**Suite Organization:**
- Not applicable. There is no test suite.

**Patterns:**
- No `setUp`/`tearDown`, no fixtures, no mocks, no assertions

## Mocking

**Framework:** Not applicable — no mocking framework in use.

**Current approach to manual validation:**
- Debug is done by temporarily uncommenting `print(json.dumps(response, indent=4))` statements left throughout the codebase
- Numerous commented-out `print()` calls serve as the residue of ad-hoc debugging
- `aulamanager.test_run()` method (line 831 of `aulamanager.py`) is a manually-invoked integration runner that logs in and calls `updateEvent` with hardcoded IDs

## Fixtures and Factories

**Test Data:**
- Not applicable. No fixture files or factory functions exist.

**Hardcoded test data observed in scripts:**
```python
# In test.py
aula_event.title = "TEST"
aula_event.start_date_time = "2024-11-01T22:00:00.0000+01:00"
aula_event.description = "BESKRIVELSE"
```

**Location:**
- Hardcoded data lives inline in `test.py` and `aulamanager.py:test_run()`

## Coverage

**Requirements:** None enforced.

**View Coverage:**
```bash
# Not configured
```

## Test Types

**Unit Tests:**
- None present.
- Candidates for unit testing: `AulaEvent` property calculations (`start_date_time`, `end_date_time`, `description` getters in `aula/aula_event.py`), regex helpers (`teams_url_fixer`, `url_fixer` in `aula/aula_calendar.py`), day-of-week mask logic (`calulate_day_of_the_week_mask`, `get_day_of_the_week_mask`), CSV lookup (`PeopleCsvManager.getPersonData` in `peoplecsvmanager.py`), daylight detection (`OutlookManager.is_in_daylight` in `outlookmanager.py`).

**Integration Tests:**
- None automated. Manual testing done via `test.py` against live AULA API.
- Login flow tested manually via `aula/aula_connection.py:login()` called from `test.py`.

**E2E Tests:**
- Not used.

## Common Patterns

**Async Testing:**
- Not applicable. No async code or test infrastructure.

**Error Testing:**
- Not applicable. No error-path tests exist.

## Adding Tests — Recommended Starting Point

Given the absence of any test infrastructure, if tests are to be added:

**Install:**
```bash
pip install pytest
```

**Suggested test file location:**
```
tests/
  test_aula_event.py         # Property getter logic (no external deps)
  test_people_csv_manager.py # CSV lookup (file I/O only)
  test_url_fixer.py          # Regex transformations (pure functions)
  test_calendar_comparer.py  # Calendar diff logic
```

**Most testable modules (no Windows/COM/network deps):**
- `aula/aula_event.py` — `AulaEvent` property getters use pure string operations
- `peoplecsvmanager.py` — `PeopleCsvManager` reads CSV files, easily mockable with `tmp_path`
- `aula/aula_calendar.py` — `teams_url_fixer`, `url_fixer`, `calulate_day_of_the_week_mask` are pure functions
- `calendar_comparer.py` — calendar diff logic operates on plain dicts

**Hard to test without mocking:**
- `OutlookManager` — requires `win32com.client` and a running Outlook instance
- `AulaConnection`, `AulaCalendar` API methods — require live AULA session
- `SetupManager` — requires `keyring` and Windows registry access
- `MainWindow` in `main.pyw` — requires a running Qt application

**Example test structure (not yet implemented):**
```python
# tests/test_aula_event.py
import pytest
from aula.aula_event import AulaEvent

def test_start_date_time_non_allday():
    event = AulaEvent()
    event.start_date = "2024-11-01"
    event.start_time = "10:00:00"
    event.start_timezone = "+01:00"
    event.all_day = False
    assert event.start_date_time == "2024-11-01T10:00:00+01:00"

def test_start_date_time_allday():
    event = AulaEvent()
    event.start_date = "2024-11-01"
    event.all_day = True
    assert event.start_date_time == "2024-11-01"
```

---

*Testing analysis: 2026-03-16*
