---
phase: 02
slug: fejlrettelser
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-18
---

# Phase 02 - Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | other - targeted local smoke scripts and app-near validation |
| **Config file** | none - Wave 0 installs lightweight validation helpers if needed |
| **Quick run command** | `py -3 -m py_compile main.pyw setupmanager.py outlookmanager.py aula\\aula_calendar.py aula\\aula_event.py aula\\aula_connection.py` |
| **Full suite command** | `py -3 -m pytest tests/phase02 -q` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `py -3 -m py_compile main.pyw setupmanager.py outlookmanager.py aula\\aula_calendar.py aula\\aula_event.py aula\\aula_connection.py`
- **After every plan wave:** Run `py -3 -m pytest tests/phase02 -q`
- **Before `$gsd-verify-work`:** Full suite must be green, plus documented manual validation for live Outlook/Aula-dependent behaviors
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 02-01-01 | 01 | 1 | BUG-01 | smoke | `py -3 -m pytest tests/phase02/test_dst_helpers.py -q` | ❌ W0 | ⬜ pending |
| 02-01-02 | 01 | 1 | BUG-02 | smoke | `py -3.12 -c "import setupmanager"` | ❌ W0 | ⬜ pending |
| 02-01-03 | 01 | 1 | BUG-01 | app-near | `py -3 -m pytest tests/phase02/test_aula_time_windows.py -q` | ❌ W0 | ⬜ pending |
| 02-02-01 | 02 | 2 | BUG-03 | app-near | `py -3 -m pytest tests/phase02/test_internet_notifications.py -q` | ❌ W0 | ⬜ pending |
| 02-02-02 | 02 | 2 | BUG-04 | app-near | `py -3 -m pytest tests/phase02/test_delete_failure_paths.py -q` | ❌ W0 | ⬜ pending |
| 02-02-03 | 02 | 2 | BUG-05 | smoke | `py -3 -m pytest tests/phase02/test_version_fallback.py -q` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/phase02/test_dst_helpers.py` - helper-level checks for Copenhagen DST offset boundaries
- [ ] `tests/phase02/test_aula_time_windows.py` - app-near validation of AULA lookup timestamp formatting across 2026 DST boundaries
- [ ] `tests/phase02/test_internet_notifications.py` - GUI-log and tray-throttle behavior checks for missing internet
- [ ] `tests/phase02/test_delete_failure_paths.py` - delete/update failure-path semantics and caller-side boolean handling
- [ ] `tests/phase02/test_version_fallback.py` - `.git` / `version.txt` / hidden-label fallback behavior
- [ ] `tests/phase02/conftest.py` - shared stubs/fixtures for Qt, GitPython, and file-system-backed startup scenarios
- [ ] `pytest` test runner setup - if missing, install/configure minimal test infrastructure for the phase

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Full sync against live Outlook and Aula after bug fixes | BUG-01, BUG-03, BUG-04 | Requires Outlook COM, stored credentials, and live Aula responses | Run the app in the real Windows environment, trigger a sync, and confirm no crash plus correct visible behavior in the affected paths |
| No-`.git` packaged or exe-near startup | BUG-05 | Packaging specs are stale and may require an environment-specific release check | Validate startup from a copied runtime directory without `.git`; if practical, also validate the packaged distribution includes `version.txt` fallback behavior |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
