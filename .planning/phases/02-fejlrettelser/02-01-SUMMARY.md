---
phase: 02-fejlrettelser
plan: 01
subsystem: testing
tags: [timezone, zoneinfo, python312, outlook, aula]
requires:
  - phase: 01-dokumentation
    provides: bug context and active runtime path documentation
provides:
  - Shared Copenhagen timezone helper for Outlook and Aula formatting
  - Dynamic Aula lookup-window formatting across DST boundaries
  - Python 3.12 startup unblock for setupmanager import
affects: [02-02, timezone handling, startup verification]
tech-stack:
  added: [pytest]
  patterns: [shared timezone helper, app-near DST verification]
key-files:
  created: [aula/timezone_utils.py, tests/phase02/test_dst_helpers.py, tests/phase02/test_aula_time_windows.py]
  modified: [outlookmanager.py, aula/aula_calendar.py, main.pyw, setupmanager.py]
key-decisions:
  - "Use aula/timezone_utils.py as the single offset source for both Outlook conversion and Aula lookup windows."
  - "Treat missing local test/runtime packages as blocking verification issues and install only the minimum needed to verify the plan."
patterns-established:
  - "Timezone formatting should flow through helper functions backed by zoneinfo instead of per-year DST tables."
  - "Aula lookup windows should compute offsets independently for each datetime boundary."
requirements-completed: [BUG-01, BUG-02]
duration: 25 min
completed: 2026-03-18
---

# Phase 02 Plan 01: DST and Python 3.12 startup fixes Summary

**Dynamic Copenhagen timezone handling for Outlook conversion and Aula lookup windows, plus a Python 3.12-safe setupmanager import**

## Performance

- **Duration:** 25 min
- **Started:** 2026-03-18T00:42:45+01:00
- **Completed:** 2026-03-18T01:07:45+01:00
- **Tasks:** 3
- **Files modified:** 7

## Accomplishments
- Replaced the hardcoded Outlook DST table with a shared `zoneinfo`-based helper in `aula/timezone_utils.py`.
- Updated `AulaCalendar.getEvents()` and `main.pyw` so Aula lookup windows format each boundary with its own Copenhagen offset.
- Removed the unused `distutils` import from `setupmanager.py` and verified import on local Python 3.12.

## Verified 2026 Date Evidence

- `2026-03-28 -> +01:00`
- `2026-03-29 -> +02:00`
- `2026-07-15 -> +02:00`
- `2026-10-25 -> +01:00`

These dates were verified in helper-level and app-near tests, including a monthly Aula lookup window that starts in DST and ends after the October DST change.

## Task Commits

Each task was committed atomically:

1. **Task 1: Indfoer delt Copenhagen-timezone-helper og brug den i Outlook-konverteringen** - `f3bb7d0` (fix)
2. **Task 2: Ret Aula lookup-vinduerne saa DST beregnes per lokal datetime** - `dd1cf68` (fix)
3. **Task 3: Fjern Python 3.12+-blokeringen og koer startup-smoke for BUG-02** - `634fadb` (fix)

## Files Created/Modified

- `aula/timezone_utils.py` - Shared Copenhagen offset and Aula datetime formatting helpers.
- `outlookmanager.py` - Replaced hardcoded DST logic with helper-based formatting for start and end metadata.
- `aula/aula_calendar.py` - Removed the single daylight flag and formatted lookup boundaries dynamically.
- `main.pyw` - Updated the active sync path to call `getEvents()` without a global DST boolean.
- `setupmanager.py` - Removed the unused `distutils` import that blocked Python 3.12+ imports.
- `tests/phase02/test_dst_helpers.py` - Added 2026 DST boundary checks for the shared helper.
- `tests/phase02/test_aula_time_windows.py` - Added app-near assertions for the exact Aula lookup strings used by `getEvents()`.

## Decisions Made

- Shared timezone formatting is now the single source of truth for both Outlook event conversion and Aula calendar lookups.
- Verification stayed local and concrete: helper tests for offset correctness, `getEvents()` tests for emitted lookup strings, and a real Python 3.12 import smoke check for `setupmanager`.
- Python 3.13 could not be smoketested because no local 3.13 interpreter is installed; that is documented as an environment limit rather than inferred as pass/fail.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Installed pytest for the local verification path**
- **Found during:** Task 1
- **Issue:** `py -3 -m pytest ...` failed because the default Python environment had no `pytest`.
- **Fix:** Installed `pytest` for the default `py -3` interpreter and Python 3.12.
- **Files modified:** none
- **Verification:** `py -3 -m pytest tests/phase02/test_dst_helpers.py -q`, `py -3 -m pytest tests/phase02/test_aula_time_windows.py -q`
- **Committed in:** not applicable (environment-only)

**2. [Rule 3 - Blocking] Installed import-time dependencies needed for app-near verification**
- **Found during:** Task 2 and Task 3
- **Issue:** The local interpreters were missing packages required to import the active runtime modules during tests and smoke checks.
- **Fix:** Installed `requests`, `python-dateutil`, and `beautifulsoup4` for the default interpreter, then installed `keyring` and `pywin32` for Python 3.12.
- **Files modified:** none
- **Verification:** `py -3 -c "from aula.aula_calendar import AulaCalendar; print(AulaCalendar.__name__)"`, `py -3.12 -c "import setupmanager"`
- **Committed in:** not applicable (environment-only)

---

**Total deviations:** 2 auto-fixed (2 blocking)
**Impact on plan:** Both deviations were verification-only environment fixes required to produce real local evidence. No product scope changed.

## Issues Encountered

- `py -3` resolves to Python 3.14 in this environment, which had no test tooling or app dependencies installed initially.
- Python 3.13 is not installed locally, so the requested `py -3.13 -c "import setupmanager"` smoke check could not be executed.
- `py_compile` passes, but it surfaces pre-existing `SyntaxWarning`s from legacy regex and Windows path strings in `aula/aula_calendar.py` and `setupmanager.py`.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- BUG-01 and BUG-02 now have concrete local verification and no open implementation blockers.
- Phase 02 plan 02 can build on the new tests and shared helper patterns.
- Python 3.13 still needs verification on a machine where that interpreter is installed.

## Self-Check: PASSED

---
*Phase: 02-fejlrettelser*
*Completed: 2026-03-18*
