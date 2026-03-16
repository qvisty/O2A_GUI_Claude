# Codebase Concerns

**Analysis Date:** 2026-03-16

## Tech Debt

**Duplicate AulaManager vs AulaCalendar:**
- Issue: `aulamanager.py` (AulaManager) and `aula/aula_calendar.py` (AulaCalendar) are two parallel implementations of almost the same API client. Both implement `getEvents`, `getEventById`, `getEventsForInstitutions`, `getEventsByProfileIdsAndResourceIds`, `findRecipient`, `deleteEvent`, `createSimpleEvent`, `updateEvent`, `teams_url_fixer`, `url_fixer`, `__remove_html_tags`, `find_unilogin_button`, and `getProfile*`. The logic is substantially identical.
- Files: `aulamanager.py`, `aula/aula_calendar.py`
- Impact: Bug fixes must be applied in two places. The active code path in `main.pyw` uses `AulaCalendar`, making `AulaManager` effectively dead code for the main flow.
- Fix approach: Remove `aulamanager.py` or reduce it to a thin wrapper; consolidate on `AulaCalendar`.

**Recurring events forcibly disabled:**
- Issue: In both `eventmanager.py` and the `main.pyw` update path, recurring event handling is explicitly forced off with `is_Recurring = False`, overriding the value read from Outlook. The `createRecuringEvent` and `updateRecuringEvent` methods in `aulamanager.py` are never called from the main flow.
- Files: `eventmanager.py` lines 231 and 256, `aulamanager.py` lines 437–650
- Impact: All recurring Outlook events are silently converted to simple (non-recurring) events in AULA. Users are not informed.
- Fix approach: Implement proper recurring event support or explicitly warn users in the UI.

**`EventManager` class is largely dead code:**
- Issue: `EventManager` (`eventmanager.py`) contains full calendar comparison and update logic including `compare_calendars` and `update_aula_calendar`, but these are not called from `main.pyw`. The `main.pyw` `MainWindow` class re-implements the same logic inline in `update_calendar`, `__create_aula_events`, `__update_aula_events`, and `__delete_aula_events`.
- Files: `eventmanager.py`, `main.pyw`
- Impact: Code duplication, confusion about which path is authoritative. Maintenance changes made in one place may not carry to the other.
- Fix approach: Remove `EventManager` or route `main.pyw` through it.

**`calulate_day_of_the_week_mask` duplicated three times:**
- Issue: The method `calulate_day_of_the_week_mask` (and `get_day_of_the_week_mask`) is identical in `eventmanager.py`, `aula/aula_calendar.py`, and also referenced from `aulamanager.py`. The weekday constants (`olFriday`, `olMonday`, etc.) are redefined in at least three separate files/methods.
- Files: `eventmanager.py` lines 93–145, `aula/aula_calendar.py` lines 135–187, `aulamanager.py` lines 438–446
- Impact: All three must be kept in sync.
- Fix approach: Move to a shared utility module (e.g., `aula/utils.py` already exists but is near-empty).

**Hardcoded daylight saving time table:**
- Issue: `outlookmanager.py` `is_in_daylight()` uses a hardcoded list of DST periods from 2021 to 2025. Any event in 2026 or later will receive the wrong timezone offset (+01:00 instead of +02:00 during summer).
- Files: `outlookmanager.py` lines 16–45
- Impact: Events in summer 2026 and beyond will have incorrect start/end times in AULA (one hour off).
- Fix approach: Replace the hardcoded table with Python's `zoneinfo` or `pytz` module to compute DST dynamically. A `TODO` comment at line 16 acknowledges this.

**Hard-coded Aula API version mismatch:**
- Issue: `aulamanager.py` `getAulaApiUrl()` returns `v22`, while `aula/aula_connection.py` returns `v23`. The active code path (via `AulaCalendar` using `AulaConnection`) uses v23. `AulaManager` uses v22 which is the older, inactive version.
- Files: `aulamanager.py` line 77, `aula/aula_connection.py` line 54
- Impact: If `AulaManager` methods are ever invoked they will call an outdated API endpoint.

**`responseRequired` field forced to `True`:**
- Issue: In both `AulaCalendar.createSimpleEvent` and `AulaCalendar.updateEvent` (and their `AulaManager` counterparts), the `responseRequired` field is hardcoded to `True`, ignoring `aula_event.response_required`. A `TODO` comment acknowledges this at multiple locations.
- Files: `aula/aula_calendar.py` line 490, `aulamanager.py` lines 313 and 391
- Impact: All created/updated events always request a response from attendees, regardless of the Outlook setting.

**`__from_outlookobject_to_aulaevent` duplicated:**
- Issue: The function converting an Outlook appointment object to an `AulaEvent` is implemented identically in both `eventmanager.py` (`__from_outlookobject_to_aulaevent`, lines 284–328) and `aula/aula_calendar.py` (`convert_outlook_appointmentitem_to_aula_event`, lines 89–133).
- Files: `eventmanager.py`, `aula/aula_calendar.py`
- Fix approach: Keep one implementation; call it from both places.

**`teams_url_fixer` and `url_fixer` duplicated four times:**
- Issue: Both URL-fixing functions are defined identically in `aulamanager.py`, `aula/aula_calendar.py`, and `aula/utils.py`. A module-level utility already exists in `aula/utils.py` but is not imported anywhere.
- Files: `aulamanager.py` lines 219–273, `aula/aula_calendar.py` lines 32–86, `aula/utils.py`

**SQLite DatabaseManager is unused in the active code path:**
- Issue: `databasemanager.py` implements recipient and event caching in a local SQLite database, but all calls to `dbManager` in `eventmanager.py` and `main.pyw` are commented out.
- Files: `databasemanager.py`, `eventmanager.py` lines 209–210 and 244–246 and 268–271, `main.pyw`
- Impact: Each sync run re-fetches all attendee IDs from the AULA search API rather than using cached values, adding substantial network overhead.

**`AulaEvent` mutable default instance attributes:**
- Issue: `AulaEvent.__init__` initialises `attendee_ids`, `outlook_required_attendees`, `recurrence_pattern`, `aula_recurrence_pattern`, `week_mask`, and `day_of_week_mask_list` as instance-level lists/values, which is correct. However, `private` and `is_private` are both set separately with the same value, indicating a rename that was never cleaned up.
- Files: `aula/aula_event.py` lines 37 and 57
- Impact: Confusion about which field is the canonical privacy flag. Both are sent to the API independently.

**`AulaEvent.start_date_time` property triggers infinite recursion potential:**
- Issue: The `start_date_time` getter at `aula/aula_event.py` line 73 calls `self.start_date_time = ...` (the setter) inside the getter body, which works but is confusing and unusual. The `end_date_time` property has the same pattern at line 86.
- Files: `aula/aula_event.py` lines 70–94
- Impact: Fragile property pattern; setting `start_date_time` directly in `__init__` before the backing `_start_date_time` attribute is created will cause an `AttributeError` if the getter is called before the setter.

## Known Bugs

**`CalendarComparer.are_calendars_identical` references undefined attributes:**
- Symptoms: Calling `are_calendars_identical()` raises `AttributeError: 'CalendarComparer' object has no attribute 'calendar1'`
- Files: `calendar_comparer.py` line 20
- Trigger: Calling `are_calendars_identical()` on any `CalendarComparer` instance.
- Workaround: Method is not called from any active code path.

**Dead code after `return` in `getEventById`:**
- Symptoms: Lines 736–742 in `aula/aula_calendar.py` and lines 151–158 in `aulamanager.py` are unreachable; a `return response` statement appears before a `try/except` block that was meant to process the response.
- Files: `aula/aula_calendar.py` lines 735–742, `aulamanager.py` lines 151–158
- Impact: The additional ID-extraction logic is silently never executed.

**`deleteEvent` contains a syntax error in commented-out logging:**
- Symptoms: `aula/aula_calendar.py` line 365 contains `s#elf.logger.warning(...)` — the `s` is outside the comment marker, causing a bare expression `s` that evaluates a variable named `s`, which will raise `NameError` at runtime if that branch is reached.
- Files: `aula/aula_calendar.py` line 365
- Trigger: Any failed event deletion.

**`on_runO2A_clicked` and `on_forcerunO2A_clicked` reference undefined `logger`:**
- Symptoms: If the internet check fails, `main.pyw` lines 538 and 554 call `logger.critical(...)`, but `logger` is only assigned later in the module-level `__main__` block. Inside the method scope, the logger is accessed as `self.logger`. The bare `logger` name will raise `NameError`.
- Files: `main.pyw` lines 538, 554
- Trigger: Running sync when there is no internet connection.

**Duplicate detection in `getEvents` does not de-duplicate:**
- Symptoms: When a duplicate event is detected (`outlook_GlobalAppointmentID in aula_events.keys()`), the code executes `pass` and then immediately overwrites the dict entry with the new event. The `isDuplicate` flag is always `False` at the point of assignment.
- Files: `aula/aula_calendar.py` lines 645–654, `aulamanager.py` lines 804–812
- Impact: Duplicate events in AULA are silently overwritten instead of being flagged for removal.

**`AulaConnection.login_with_idp` uses `self.session.get` instead of local `session`:**
- Symptoms: `aula/aula_connection.py` line 112 calls `self.session.get(url)` during the initial page fetch, but then assigns the result to `response` and passes it to `find_unilogin_button(response, session)` where `session` is the same `self.session`. The initial fetch bypasses the local `session` variable returned from `getSession()`.
- Files: `aula/aula_connection.py` lines 107–113

## Security Considerations

**Password printed to terminal during setup:**
- Risk: `setupmanager.py` line 201 prints `"UNI-password: " + str(passwd)` directly to the terminal during the CLI setup flow.
- Files: `setupmanager.py` line 201
- Current mitigation: Only invoked via the old CLI setup path, not the GUI.
- Recommendations: Remove the password `print` statement entirely.

**Credentials displayed in plain text in the GUI login dialog:**
- Risk: `main.pyw` `UniloginDialog.__init__` at line 598 sets `self.password.setText(password)` — this loads the stored password into the plain-text password field so it is readable before the user edits it. There is no masking applied on initial population.
- Files: `main.pyw` lines 595–599
- Current mitigation: The field uses `show="*"` mask in the `.ui` definition, so characters are visually masked after entry, but the password is present in the widget's text buffer.
- Recommendations: Acceptable risk for a local desktop tool, but worth documenting.

**Broad `except:` clauses swallow all exceptions silently:**
- Risk: Multiple bare `except: pass` blocks (11 occurrences across `aula_connection.py`, `aula_calendar.py`, `aulamanager.py`, `outlookmanager.py`) suppress all exceptions including `KeyboardInterrupt` and `SystemExit`. Login failures, network errors, and unexpected API shape changes are silently ignored, causing the loop to exhaust its counter limit and return a failed status with no diagnostic information.
- Files: `aula/aula_connection.py` lines 93, 192, 219, 339, 352; `aula/aula_calendar.py` lines 342, 742; `aulamanager.py` lines 157, 193, 696; `outlookmanager.py` line 120
- Recommendations: Replace with specific exception types and add logging within each handler.

**Error notification emails CC a personal address:**
- Risk: `outlookmanager.py` line 185 hard-codes `mail.CC = "olex3397@skolens.net"` on every internal program error email, forwarding potentially sensitive event information and error diagnostics to a third party.
- Files: `outlookmanager.py` line 185
- Recommendations: Remove the hard-coded CC or make it configurable.

**URL construction via string concatenation (potential injection):**
- Risk: `aula/aula_calendar.py` lines 328 and 686 and `aulamanager.py` lines 92 and 179 construct API URLs by direct string concatenation of user-derived values (recipient names, institution codes) rather than using `requests` parameter encoding. A name containing `&` or `?` could corrupt the query string.
- Files: `aula/aula_calendar.py` line 328, `aulamanager.py` line 179
- Recommendations: Remove manual URL construction; let `requests` encode parameters via the `params` dict (already provided but ignored in these cases).

## Performance Bottlenecks

**Per-attendee AULA search with `time.sleep` delays:**
- Problem: For every attendee on every event being created or updated, the code performs a live AULA API search and then sleeps 1 second between attempts (`aula/aula_calendar.py` line 304) and 0.5 seconds after each lookup (line 259 in `handle_recipients`). With many attendees across many events, sync time grows linearly.
- Files: `aula/aula_calendar.py` lines 283–308
- Cause: No caching layer (the SQLite `DatabaseManager` caching is commented out).
- Improvement path: Re-enable `DatabaseManager` recipient caching so each name is only resolved once per session.

**`getEvents` fetches every event individually:**
- Problem: `getEvents` first retrieves a list of event IDs via `getEventsForInstitutions` and `getEventsByProfileIdsAndResourceIds`, then calls `getEventById` for each one individually inside the loop (line 600 in `aula_calendar.py`). For a calendar with 50 events over 12 months, this results in 50 individual HTTP requests.
- Files: `aula/aula_calendar.py` lines 596–668
- Improvement path: Check whether the AULA API supports batch fetching; otherwise, parallelize with `concurrent.futures`.

**`calulate_day_of_the_week_mask` computes all 128 weekday combinations on every call:**
- Problem: Called once per event during conversion, this function computes all 128 subsets of 7 days via `itertools.combinations` each time, then linearly searches for the matching entry.
- Files: `aula/aula_calendar.py` lines 135–178, `eventmanager.py` lines 93–136
- Improvement path: Replace with a direct bitmask lookup dictionary computed once at module level.

## Fragile Areas

**Login scraping depends on Aula HTML form structure:**
- Files: `aula/aula_connection.py` (entire `login_with_stil` and `login_with_idp`)
- Why fragile: The login flow scrapes HTML forms using BeautifulSoup and submits them iteratively. Any change to the Aula or UNI-login HTML structure (new form fields, changed action URLs, additional redirect steps) will silently fail, exhausting the 10-iteration loop and returning a failed login with no diagnostic detail.
- Safe modification: Always test against a live Aula login before releasing changes to login code.
- Test coverage: None.

**`AulaConnection.ProfileinstitutionCode` property contains a nested dead function definition:**
- Files: `aula/aula_connection.py` lines 35–49
- Why fragile: The `ProfileinstitutionCode` property body contains an inner `def getProfileId(self)` function that is never called and shadows the outer method of the same name. The commented-out return at line 49 suggests the property is incomplete.
- Safe modification: The outer `getProfileId` method at line 21 is what is actually used. Do not call the version defined inside the property.

**`getProfileinstitutionCode` in `aulamanager.py` has the same nested dead function:**
- Files: `aulamanager.py` lines 58–72
- Why fragile: Same pattern as above — an inner `def getProfileId(self)` is defined inside `getProfileinstitutionCode` and is never executed.

**`AulaEvent` instance `attendee_ids` list is shared across calls if not re-initialised:**
- Files: `aula/aula_event.py` line 34
- Why fragile: `AulaEvent.__init__` initialises `self.attendee_ids = []` as a fresh list each time, which is correct. However, if any code ever passes `AulaEvent` as a default argument (`def createSimpleEvent(self, aula_event = AulaEvent)` in `aulamanager.py` line 349), the class itself (not an instance) is used as the default, so `aula_event.attendee_ids` would access the class body, not an instance list.
- Safe modification: Always pass instantiated `AulaEvent()` objects, never the class itself.

**`CalendarComparer` operates on raw key sets, not event objects:**
- Files: `calendar_comparer.py`
- Why fragile: `CalendarComparer` receives `aula_events` and `outlook_events` dictionaries but converts them to `set()` of keys directly. The `find_unique_events` method returns sets of key strings that must then be used to look up events in the original dicts by callers in `main.pyw`. If the dict changes between construction and lookup, events could be missed or cause `KeyError`.
- Safe modification: Pass the full dicts and avoid external re-lookup patterns.

## Scaling Limits

**End-date hardcoded to `today.year+1, July 1`:**
- Current capacity: Looks forward approximately 6–18 months from any given run date.
- Limit: Events scheduled more than ~18 months in the future are never synced.
- Files: `main.pyw` line 354
- Scaling path: Make the look-ahead window configurable in `configuration.ini`.

**`runFrequency` spinbox maximum is 4 hours:**
- Files: `mainwindow.py` line 145 (`self.runFrequency.setMaximum(4)`)
- Limit: Users cannot set a sync interval longer than 4 hours through the GUI.
- Scaling path: Expose the maximum value as a configuration option.

## Dependencies at Risk

**`distutils` imported in `setupmanager.py`:**
- Risk: `from distutils.core import run_setup` is imported at line 1 of `setupmanager.py`. `distutils` was removed from the Python standard library in Python 3.12. This import will cause an `ImportError` on Python 3.12+.
- Files: `setupmanager.py` line 1
- Impact: The entire `SetupManager` class fails to import on Python 3.12+.
- Migration plan: Remove the import (it is not actually used anywhere in the file) or replace with `setuptools`.

**`winshell` and `pywin32` make the application Windows-only:**
- Risk: These packages have no cross-platform alternative and have historically lagged behind new Python releases.
- Files: `main.pyw` line 6, `setupmanager.py` line 9, `outlookmanager.py` line 1
- Impact: The application cannot run on macOS or Linux. Windows-only is intentional by design, but any major Windows API deprecation could break COM automation.
- Migration plan: Not applicable for current use; document the Windows-only constraint explicitly.

**`GitPython` used only for version display:**
- Risk: `GitPython` (imported as `git` in `main.pyw` line 30) is used solely to read the latest commit hash and date for the version label. This creates a dependency on a git repository being present at runtime. If the application is distributed without a `.git` directory (e.g., as a compiled executable), it will crash on startup.
- Files: `main.pyw` lines 156–163
- Impact: Application fails to initialise if run outside a git repository.
- Migration plan: Store version in a static file (e.g., `version.txt`) and remove the `GitPython` dependency.

## Missing Critical Features

**No handling for annual recurring events:**
- Problem: Outlook recurrence type 5 (yearly) is explicitly skipped with a log message but no user notification via the GUI or email.
- Blocks: Users with annual recurring meetings (e.g., yearly school events) receive no feedback that these are not being synced.
- Files: `eventmanager.py` line 383, `main.pyw` (the `compare_calendars` logic is re-implemented inline without this guard at all in `main.pyw`)

**No user feedback when internet check fails:**
- Problem: `has_internet_connection()` in `main.pyw` returns `False` on connection failure, and the run is silently aborted. The log message is written via the undefined `logger` variable (a bug; see Known Bugs), so in practice no message is displayed.
- Files: `main.pyw` lines 537–539, 552–554

## Test Coverage Gaps

**No test suite exists:**
- What's not tested: All core logic — login flow, event conversion, calendar comparison, attendee lookup, event creation/update/deletion.
- Files: `test.py` is present but empty (contains no test cases).
- Risk: Any change to the Aula API response shape, Outlook COM object behaviour, or internal data transformation logic will fail silently at runtime with no automated detection.
- Priority: High

---

*Concerns audit: 2026-03-16*
