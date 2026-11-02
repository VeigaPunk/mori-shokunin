source: S589 (docs.python.org — time — Time access and conversions, Python
3.15.2 documentation; pinned copy
`corpus/evidence/sources-r74/S589.html` sha256
c8cc430e04d232f9e67412eae254a2c67ad153b4bde78121f83f2389739e91c7, 129606
bytes, opened 2026-11-02; pre-row duplicate sweep receipted BEFORE the fetch
in `.ufo/waves/round-74/evidence/source-s589-r74.txt`). The instrument's
OBJECT pages stand on their own rows: S241 (the observed serving and the
compare pin) and S581 (the documented token-clock scale that sizes the
default windows).
verified-at: 2026-11-02 (round 74; the S589 clock claims below are
line-located against the pinned copy and machine-verified by the r72
anchor-checker — PASS items=2 with the able-to-fail mislocation arm FAIL
rc 1, `.ufo/waves/round-74/evidence/s589-anchor-check-r74.txt`; the
instrument's own verification is the selftest 13/13 x3 and the first live
schedule run, `.ufo/waves/round-74/evidence/rotation-schedule-selftest-r74.txt`
and `rotation-schedule-live-r74.txt`)
recheck: 180d, or when a re-fetch of the page changes its sha256 against the
pinned copy

# The rotation-recurrence schedule instrument (round 74)

Scope: detection and report only, counts and shapes only. The r70 round ran
three stated-window A/A pairs BY HAND at windows 31/91/304 s and read them
against the S581 documented token-clock scale; the r71 planned note called
that session "ONE session's observation". This round lands the instrument
that makes the schedule repeatable — `tools/mori-rotation-schedule.py` — so
the recurrence question (does a same-window classification reappear?) is a
re-run, not a re-derivation. Claims (K1–K5):

- **K1** — `S589.html:524` — "Return the value (in fractional seconds) of a monotonic clock, i.e. a clock" (13 words) and `:525` — "that cannot go backwards.  The clock is not affected by system clock updates." (13 words): the schedule's dwell deadline and the run's wall_s total run on `time.monotonic`, a clock the docs guarantee cannot go backwards and is unaffected by system-clock updates — the property a stated-window schedule needs (the summary line carries `clock=monotonic`).
- **K2** — `S589.html:526-527` — the reference point is undefined, so only the DIFFERENCE between two results is valid: the instrument prints differences only — every window's `window-s=<N>` computed from the two capture receipts' own `as-of=` stamps (QUALITY 161), and the summary's `wall_s=<T>` — never an absolute clock reading.
- **K3** — the classification grammar is fixed and honest-unavailable: `rotated=yes` when per-response>0 OR same-bytes=false (a body-level change the line-diff grammar cannot name is still rotation); `rotated=no` only when per-response=0 AND same-bytes=true; anything else (a dead capture leg, child setup failure, unparseable summary, child timeout) is `rotated=unavailable` with the reason on the line — never guessed. The only child is the REGISTERED ua-variance probe (the r71 composition precedent); no registered byte is edited, no second fetcher exists.
- **K4** — first live run (2026-11-02T07:55:33Z..08:02:42Z, wall_s=429, rc 0): 31s `rotated=no`, 91s `rotated=no`, 304s `rotated=yes` (per-response=4, sha 3e0ece8127c6 → 5d88b3cc6039), `window_s_computed=31,91,304`. The r70 session (2026-11-01T19:57–20:07Z) had classified 31s=no, 91s=YES, 304s=no under the same stated windows: the same schedule returned a DIFFERENT per-window classification — the per-window classes are not stable across runs. This is one more single-session observation, now cheap to re-run; no rotation clock value is decided (S580/S581 boundary untouched).
- **K5** — the served body states are session artifacts, never pinned content: this run's bodies (3e0ece81…/5d88b3cc…, 54340 bytes) differ from the r70 run's (e4bf924c…/6e7b906d…, 54343 bytes) — the serving rotates among body states over time, so no sha pair is durable and the instrument compares only WITHIN a run. The compare pin (S241's committed copy) grounds the stable-token set, not the serving's current bytes.

Limits (declared): the instrument decides NOTHING about the vendor's bot
management — no mechanism, no TTL, no verdict on the page's availability
(an `unavailable` window is a dead leg, not a page state); windows are
metadata per QUALITY 161, never lifetime measurements. Boundaries: the
schedule is the lane's own observation posture on a public vendor page
(read-only fetches through the registered child); stdout carries counts,
shapes, stamps and sha prefixes only — the children's output lines are
parsed, never echoed (the selftest redaction arm plants a marker token on a
non-grammar field and proves it cannot reach stdout); capture files land in
a scratch out-dir and are deleted at round end, their sha prefixes travel
on the receipt lines. Registration: the probe is registered at landing as
registry row 11 (`rotation-schedule probe (r74 tool)`, SKILL.md :1327) —
the D72-1 unregistered-instrument defect class pre-empted, and the standing
battery re-run 11/11 rc 0 at the landing bytes
(`.ufo/waves/round-74/evidence/selftests-battery-r74.txt`).
