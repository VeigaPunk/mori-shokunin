# Index-clean dispatch-log check

**Result: FAIL (commit coverage).** The requested history range contains five commits, but `.ufo/waves/round-38/dispatch-log.txt` contains only one `landed` entry. That entry has the required clean-index record; the other four commits in the scored-tip history have no corresponding entry or recorded index state.

| Commit | Matching dispatch-log entry | Result |
|---|---|---|
| `f725f30` — round-38: C1 counter v4.1 + freeze v2 pins, C4 byte-capped reads, wave-1 spec/dispatch, attempt-2 evidence | None | Missing record — FAIL |
| `daa1d4d` — round-38 data: S226 + content-anchor/containment entries, timed supersede in the append-only gate, C1-C3 declaration and capability rows, README/QUALITY/SKILL, lesson, recipe fix | None | Missing record — FAIL |
| `8d26150` — round-38: before receipts (c4/c5/runnable before-arm) and the witness-sandbox control builder | None | Missing record — FAIL |
| `1f1e996` — round-38: freeze — contract (C1-C3), C1 counter v4, C4 counter, conformance checker, fixtures, pins, start census and gate-before receipts | None | Missing record — FAIL |
| `3501d4c` — round-37 erratum + LOG append-only amendment + inherited late seat reports | `dispatch-log.txt:3`; immediately followed at line 4 by `staged=0 intent_to_add=0 (exit 0)` | Recorded clean |

Evidence: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --format='%h %s' e33bb561712b32f46861362a3fa43762fa70ae4f..f725f3076972e6e70595b5ac8279be524a111ff8` returned the five commits above. The complete dispatch log read contained lines 1–4 only: one `landed` line (line 3, `3501d4c21f70e2ec2659c37c3f960b55f60cfea6`) and its clean-index record (line 4). Thus the explicit landed entry passes, but four commits in the requested range ending at the scored tip lack commit-to-log evidence and cannot be counted as having a recorded clean-index check.
