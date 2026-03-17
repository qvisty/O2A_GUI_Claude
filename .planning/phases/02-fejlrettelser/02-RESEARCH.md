# Phase 02 Research: fejlrettelser

**Gathered:** 2026-03-18
**Phase:** 02-fejlrettelser
**Requirements covered:** BUG-01, BUG-02, BUG-03, BUG-04, BUG-05
**Question answered:** What do I need to know to PLAN this phase well?

## Executive Summary

Plan this phase around the active runtime path only:

- `main.pyw` is the real startup and sync orchestrator.
- `setupmanager.py` blocks Python 3.12+ startup because it imports `distutils` at module import time.
- `main.pyw` blocks no-`.git` startup because version lookup runs inside `MainWindow.setup_gui()` before the app is fully ready.
- `outlookmanager.py` contains the hardcoded DST table, but BUG-01 also reaches into `aula/aula_calendar.py` because AULA event lookup currently uses one DST flag for the whole sync window.
- `aula/aula_calendar.py` has the BUG-04 `deleteEvent()` failure path, and `main.pyw` has adjacent caller-side checks that currently treat `False` as success.

The phase should stay focused on BUG-01 to BUG-05, but it should include the nearby follow-up fixes that are required for truthful validation:

- Startup-safe logger/bootstrap ordering in `MainWindow`
- Caller-side success checks for `deleteEvent()` and `updateEvent()`
- A real `version.txt` fallback strategy, not only a try/except around GitPython

## What Matters For Planning

### 1. BUG-01 is bigger than one function

The visible bug is the hardcoded DST table in [outlookmanager.py](/c:/Users/Jesper/Documents/jq%20Code/O2A_GUI_Claude/outlookmanager.py), but the active code path also passes a single `is_in_daylight` boolean from `main.pyw` into `AulaCalendar.getEvents()` for the entire sync range. That means a sync window that crosses 2026-03-29 or 2026-10-25 can still use the wrong offset after the first month.

Planning implication:

- Treat BUG-01 as a shared time-offset problem, not only an Outlook conversion problem.
- Use one helper to derive Copenhagen offset dynamically per datetime.
- Apply it both when converting Outlook events and when building AULA query timestamps.

### 2. BUG-02 is an import-time blocker

`setupmanager.py` imports `from distutils.core import run_setup`, but the symbol is unused. On Python 3.12+ that import fails before the GUI can start.

Planning implication:

- Fix BUG-02 early, because it unlocks every other validation path.
- Do not replace it with more packaging work unless needed; removal is enough unless a later call site actually needs replacement.

### 3. BUG-03 needs a central notification design, not only `self.logger`

The immediate crash is from bare `logger.critical(...)` in `on_runO2A_clicked()` and `on_forcerunO2A_clicked()` in [main.pyw](/c:/Users/Jesper/Documents/jq%20Code/O2A_GUI_Claude/main.pyw). Replacing `logger` with `self.logger` fixes the NameError, but the phase context requires one central channel choice with default `GUI + tray`, GUI log always on, tray throttled to first repeated internet failure, and reset after a successful sync.

Planning implication:

- Plan a small helper or method for runtime notifications.
- Keep the channel choice in one code location.
- Separate "write to GUI log" from "show tray popup now".

### 4. BUG-04 has a hidden second bug at the caller

`aula/aula_calendar.py` contains the `s#elf.logger.warning(...)` typo in `deleteEvent()`, which triggers NameError on the failure branch. But `main.pyw` also checks delete/update results with `if not ... == None`, so `False` is currently treated as success.

Planning implication:

- The plan must fix both the callee and the call sites.
- Otherwise validation will produce false positives even after the NameError is gone.

### 5. BUG-05 is a startup resilience problem, not just a git exception

`MainWindow.setup_gui()` calls `git.Repo(search_parent_directories=True)` during window setup. If `.git` is missing, startup fails before the logger and the rest of the window are safely initialized. The agreed fallback is:

- use git commit date when `.git` exists
- else read `version.txt`
- else hide the version label

Planning implication:

- Treat version display as optional metadata.
- Make version lookup lazy and failure-tolerant.
- Decide who owns `version.txt` creation/update.
- If PyInstaller validation is attempted, bundle `version.txt`; current spec files are stale and point at `main.py`, not `main.pyw`.

### 6. Bootstrap ordering is part of this phase whether you name it or not

`MainWindow.__init__()` calls `setup_gui()` and `initial_o2a_check()` before assigning `self.logger`. That is already fragile for startup-time failures near BUG-03 and BUG-05.

Planning implication:

- Either initialize `self.logger` before those calls, or keep new helpers logger-free until UI/logging is ready.
- This is a nearby startup fix and should be planned together with BUG-03 and BUG-05.

## Requirement-to-Code Map

| Requirement | Primary files | Hidden dependency to plan for |
|---|---|---|
| BUG-01 | [outlookmanager.py](/c:/Users/Jesper/Documents/jq%20Code/O2A_GUI_Claude/outlookmanager.py), [aula/aula_calendar.py](/c:/Users/Jesper/Documents/jq%20Code/O2A_GUI_Claude/aula/aula_calendar.py), [main.pyw](/c:/Users/Jesper/Documents/jq%20Code/O2A_GUI_Claude/main.pyw) | Shared timezone helper and AULA query timestamp formatting |
| BUG-02 | [setupmanager.py](/c:/Users/Jesper/Documents/jq%20Code/O2A_GUI_Claude/setupmanager.py) | Python 3.12/3.13 smoke validation |
| BUG-03 | [main.pyw](/c:/Users/Jesper/Documents/jq%20Code/O2A_GUI_Claude/main.pyw) | Central notification helper, tray throttling, reset after successful sync |
| BUG-04 | [aula/aula_calendar.py](/c:/Users/Jesper/Documents/jq%20Code/O2A_GUI_Claude/aula/aula_calendar.py), [main.pyw](/c:/Users/Jesper/Documents/jq%20Code/O2A_GUI_Claude/main.pyw) | Caller-side boolean handling for delete/update results |
| BUG-05 | [main.pyw](/c:/Users/Jesper/Documents/jq%20Code/O2A_GUI_Claude/main.pyw), optionally `version.txt`, possibly spec files | Startup-safe version resolution and package/runtime fallback |

## Standard Stack

- Use Python stdlib `zoneinfo` with `Europe/Copenhagen` for DST logic.
- Keep PySide6 as the GUI/tray mechanism; do not introduce a second notification framework.
- Keep GitPython only as an optional metadata source, not a startup requirement.
- Use a plain text `version.txt` fallback with the same date-shaped display string that the GUI already expects.
- Prefer helper extraction and local smoke validation over trying to add a full automated test suite in this phase.

## Architecture Patterns

### Startup-safe optional metadata

Use a helper for version resolution that can return:

- git-based date string
- fallback `version.txt` date string
- `None` to mean "hide label"

The GUI should consume the result and decide whether to set or hide the label. Version lookup must never crash the app.

### Single source of truth for timezone offset

Use one helper that answers "what UTC offset string should AULA get for this local datetime?" and reuse it from:

- `OutlookManager.get_aulaevents_from_outlook()`
- `AulaCalendar.getEvents()`

If a second helper is useful, make it format complete AULA datetime strings from a datetime plus offset helper. That avoids repeating string assembly.

### Single source of truth for internet-failure notification

Put the internet-failure handling behind one method in `MainWindow`, for example:

- always log to GUI/internal logger
- optionally show tray message if channel config allows it
- suppress repeated tray popups until a successful sync resets the state

This matches the locked phase decisions without adding new UI scope.

### Explicit success semantics

Use explicit result handling:

- `True` = success
- `False` = known failure
- `None` = timeout/unknown failure only if the callee already uses it

Callers should test these explicitly. Do not use `!= None` when `False` is meaningful.

## Don't Hand-Roll

- Do not extend the hardcoded DST table to 2026/2027. Replace the table entirely.
- Do not duplicate fixes into legacy `aulamanager.py` or `eventmanager.py`; the active flow does not use them.
- Do not add a user-facing config screen for notification channels in this phase.
- Do not let version display stay in the critical startup path.
- Do not rely on the current PyInstaller spec files as proof that exe validation is already ready.

## Common Pitfalls

- `AulaCalendar.getEvents()` currently applies one daylight flag to the full sync range. That can still be wrong even after `OutlookManager.is_in_daylight()` is fixed.
- `AulaCalendar.getEvents()` currently formats timestamps with an extra literal `T` before the UTC offset. Verify and normalize this while touching the timezone logic.
- `MainWindow.__init__()` creates a startup window where logger-dependent code can run before `self.logger` exists.
- `__delete_aula_events()` and `__update_aula_events()` can log success on `False` returns.
- There is no automated suite, so plans that depend on broad end-to-end regression coverage will be unrealistic.
- `.git`-less validation should use a copied runtime directory, not destructive renaming inside the working repo.

## Code Examples

These are planning seams, not final code.

```python
from zoneinfo import ZoneInfo

CPH = ZoneInfo("Europe/Copenhagen")

def aula_utc_offset_for_local_dt(local_dt) -> str:
    aware = local_dt.replace(tzinfo=CPH)
    return aware.strftime("%z")[:3] + ":" + aware.strftime("%z")[3:]
```

```python
def resolve_program_version_text(app_dir) -> str | None:
    # 1. Try git commit date if repo exists
    # 2. Else try version.txt
    # 3. Else return None and hide the label
```

```python
def notify_internet_failure(self):
    self.logger.critical("Det var ikke muligt at oprette forbindelse til internettet!")
    if self._internet_tray_allowed and not self._internet_failure_announced:
        tray.showMessage("O2A", "Ingen internetforbindelse")
        self._internet_failure_announced = True
```

## Recommended Plan Shape

Keep the roadmap's two-plan shape, but make the scope boundaries explicit.

### Recommended 02-01

Focus:

- BUG-01 dynamic DST/timezone logic
- BUG-02 Python 3.12+ startup unblock

Include:

- shared Copenhagen offset helper
- fix `OutlookManager` conversion path
- fix `AulaCalendar.getEvents()` query timestamp path
- normalize AULA datetime formatting while already touching that code
- remove unused `distutils` import
- smoke validation on Python 3.12 and Python 3.13

### Recommended 02-02

Focus:

- BUG-03 internet failure handling
- BUG-04 deletion failure path
- BUG-05 no-`.git` startup fallback

Include:

- initialize startup-safe logger state earlier
- central runtime notification method with default `GUI + tray`
- tray throttling and reset after successful sync
- fix `deleteEvent()` NameError path
- fix caller-side `False`/`None` handling for delete/update
- implement `version.txt` fallback and hide-label behavior
- if practical, include package-near validation path for `version.txt`

## Open Decisions The Planner Should Lock Early

- Where should the notification channel choice live?
  Recommendation: code-level constant/helper in `main.pyw`, not persistent config.

- What exact format should `version.txt` store?
  Recommendation: the same human-readable date format already shown in the label.

- Is PyInstaller spec work in scope?
  Recommendation: only if needed to bundle `version.txt` for exe-near verification. Do not expand packaging scope otherwise.

## Validation Architecture

Validation should be layered so the phase can produce real evidence without requiring full live-system automation.

### 1. Helper-level validation

Create or extract helpers that can be checked locally without Outlook or Aula:

- timezone offset helper
- version resolution helper
- notification state helper if tray throttling logic becomes non-trivial

Minimum DST date cases to validate:

- 2026-03-28 -> `+01:00`
- 2026-03-29 -> `+02:00`
- 2026-07-15 -> `+02:00`
- 2026-10-25 -> `+01:00`

These should be checked both for single-event conversion logic and for AULA lookup window formatting.

### 2. Import/startup smoke validation

Run local startup-oriented checks that do not require live sync:

- Python 3.12 import/startup smoke after BUG-02
- Python 3.13 import/startup smoke after BUG-02
- copied runtime directory without `.git` but with `version.txt`
- copied runtime directory without `.git` and without `version.txt`

Expected results:

- app starts
- no GitPython crash
- label shows fallback date when `version.txt` exists
- label is hidden when both git metadata and `version.txt` are absent

### 3. App-near behavior validation

Validate the exact user-visible bug paths:

- internet unavailable at sync start logs a visible GUI error instead of crashing
- repeated internet failures show at most one tray popup until a successful sync
- successful sync resets the tray-throttle state
- failed AULA deletion returns a visible failure status instead of crashing or logging success

If full live Aula validation is impractical, stub or monkeypatch the relevant methods and document the limit.

### 4. Evidence the phase should capture

The eventual plan should require concrete evidence for each bug:

- BUG-01: date examples showing correct 2026 offsets/timestamps
- BUG-02: Python 3.12 and 3.13 startup/import proof
- BUG-03: GUI-log and tray-throttle proof
- BUG-04: deletion failure-path proof and corrected caller status handling
- BUG-05: no-`.git` startup proof with and without `version.txt`

### 5. Known validation limits

- Full end-to-end sync depends on live Outlook COM and live Aula login.
- Current packaging specs are stale, so exe-near validation may require a small packaging adjustment or a copied-source runtime simulation instead.
- There is no existing automated test suite; if helper extraction is skipped, validation becomes much weaker.

## Planning Recommendation

Plan this phase as "startup resilience plus time correctness", not as five isolated one-line bug fixes. The code already shows that BUG-01, BUG-03, BUG-04, and BUG-05 each have adjacent hidden issues that will otherwise undermine verification. The best plan is the one that fixes those adjacent seams on purpose while still staying inside the Phase 02 boundary.
