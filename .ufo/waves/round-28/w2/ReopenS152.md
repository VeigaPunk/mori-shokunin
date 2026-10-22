# Round 28, wave 2 — ReopenS152 (seat MoriR28.ReopenS152)

Verdict: **partial** — the S152 row and its Gate line verify byte-for-byte against a fresh curl fetch, and the
named defect is genuinely fixed *in the row*; but the r27 Low-1 defective wording still stands verbatim in the
live reader `corpus/knowledge/harness-job-capacity-r25.md` with no dated correction in `corpus/lessons/round-28.md`
(QUALITY 77). One low residual on a range citation.

Attacked at `f2de0eedcd60d2e354da75265ea6122bc3896073` (committed bytes via `git show <rev>:<path>`; lane untouched).

## Checks

### 1. Source re-open (curl now) — PASS

`curl -sf` each URL at 2026-10-22T18:55:06Z, digests recomputed locally:

| URL | my sha256 | row states |
|---|---|---|
| job-manager.ts @6962d5cd | f8851470a8bd953f25ab659c0d0aac2ea8c34df9a433e154ec4127c7683b70bd | same (matches) |
| sdk.ts @6962d5cd | 84f3a112a670f36de9c030756f4babc0ad83e37efeca99154ea4d4263423e633 | same (matches) |
| sdk.ts @d9bc4fbd | fde5a959e3a310be1d9fd291163dd817d2328d2b5a2012697b75b3205d592104 | same (matches) |
| job-manager.ts @d9bc4fbd | c417f63c7686e19ef9a0a658519de843e87dede6e23f73ee3ef1583f95e61aaf | same (matches) |

No drift. Commit metadata re-fetched via api.github.com (18:55Z): sole parent `d9bc4fbd`, author
2026-09-24T18:04:41Z, committer 2026-09-24T19:09:05Z, subject "feat: implemented centralized settings registry
and internal URL routing", 300 files +21217/−15807 — all as the scope cell states.

### 2. Gate line (`corpus/lessons/round-28.md:71`) — PASS

Verbatim located quote at `job-manager.ts:305`: "return Math.max(1, Math.floor(value ?? DEFAULT_MAX_RUNNING_JOBS));"
(5 words claimed; the quoted code is verbatim at :305 in my fetch, `cat -A` clean). sha256 cell
`f88514…b70bd` equals my fetch. Access time 2026-10-22T17:59:30Z predates my check; URL, 64-hex sha256 and
quoted span all present (counter `gate_line` shape met).

### 3. Every S152 cell vs bytes — PASS

`corpus/SOURCES.md:157`, 13 fields, `|` clean.
- **scope**: "clamp site moves from a static value to a per-check function, the manager option widens from a
  number to a function, and the cap's floor of 1 moves from session construction to a per-check getter" — all
  three verified: sdk.ts parent :1797 `const asyncMaxJobs = Math.min(100, Math.max(1, …))` vs :1949
  `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings) ?? 100),` (5-tab indent confirmed by
  `cat -A`); job-manager.ts :148 option type `number | (() => number)`; parent :284 constructor floor vs
  :302–306 getter floor. "that commit's clamp and floor only" scoping + 300-file/subject note verified (check 1).
- **anchor**: every cited line verified verbatim above; four sha256s verified (check 1); dates verified (API).
- **teaches**: opens `supersedes S140 — ` (em dash); body differs from S140's, byte-accurate (see check 4).
- **status/recheck/opened**: mined | 2026-10-22 | on-release — consistent.
- **used-by**: `corpus/knowledge/harness-job-capacity-r25.md, corpus/lessons/round-28.md` — both cite S152
  (knowledge :1, :277, :330; lesson :71). `git grep -w -F S140` over the live readers is clean; the counter's
  READERS scope (`SKILL.md PROVINCE.md corpus/README.md corpus/knowledge`) exempts history lessons by design.
- Not copied: S140's frozen `teaches` said "the explicit floor can vanish in the rewrite"; S152 says the floor
  *moved*, matching the bytes — the opposite, verified claim.

### 4. Named defect actually fixed in S152 — PASS (row); the r27 note itself corrected

r27 ReopenS140 Low-1 (`.ufo/waves/round-27/w2/ReopenS140.md:137-143`): the knowledge wording "can be read as
'the v18.12.6 cap has no floor'" since the floor left the sdk clamp site and reappeared in the manager getter.
S152's teaches states exactly that, and improves on Low-1's own phrasing: Low-1 said the commit "added" the
getter floor; the parent bytes show the floor pre-existed in the constructor (`d9bc4fbd job-manager.ts:284`),
so S152's "moves from session construction to a per-check getter" is the more precise claim — verified.

### 5. QUALITY 77 sweep — FAIL (one live defect)

The exact clause Low-1 named still stands verbatim at the attack rev:
- `corpus/knowledge/harness-job-capacity-r25.md:282-283`: "the explicit floor `Math.max(1, …)` did not survive
  that rewrite — neither the clamp expression nor the accessor (`tools/settings.ts:941-946`) carries a floor
  at v18.12.6." Unqualified; still reads as "the cap has no floor", and sits in a file whose own :70 quotes the
  getter that *does* carry the floor at v18.12.6 — internally contradicted.
- `:330` (round-27 corrections log): "the explicit floor of 1 did not survive the rewrite" — same defect. The
  wave-1 report prescribed a dated correction block in `corpus/lessons/round-28.md` for this history line;
  `grep -n 'floor\|correction\|S140' round-28.md` finds none — no dated correction exists at f2de0ee.

No other live reader states the wording: SKILL.md:658 `max(1, floor(min(100, async.maxJobs)))` is correct;
PROVINCE.md:297-313 "clamp lives at the manager's construction site" is accurate; corpus/README.md:490 is
accurate; grep of `corpus/knowledge` for floor/flat-floor phrasing finds only the two lines above.

**Why it matters**: the amended counter only tests *id citation* (`readers_left=0` measured — no live reader
cites S140 as a word). It cannot see that the reader's *wording* still carries the defect the supersede was
routed to fix. C1 can print `met` while QUALITY 77 is unmet.

### 6. Counter result at f2de0ee — consistent

`bash .ufo/waves/round-28/count-c1.sh f2de0ee…`: `row_identity=rows=151 changed=0 removed=0 bad=0`;
`superseding=7/8 ids=S096,S097,S127,S128,S129,S131,S140`; `fail S147 row_absent`; `readers_left=0`; `C1=unmet`.
For S152: no `fail S152` line — S140 is in the `ids=` admitted list, i.e. row present, used-by cites S152,
gate_line shape met. The `C1=unmet` is caused solely by missing row S147 (S101's supersedes; the knowledge
file :1 already cites S147, so the reader move ran ahead of the row — other seat's scope).

### 7. Residual / gaps

- **Low — invisible range citation**: `harness-job-capacity-r25.md:3` recheck line says "re-open S098–S103,
  S112–S113 and S138–S141" — the range covers superseded S140 without naming it; `git grep -w` cannot see it.
  Harmless as instruction but a channel a future sweep misses.
- Commit-page HTML not re-fetched for hashing (session-varying bytes; wave-1 noted the same). All stable
  endpoints verified.
- Verified fetches saved under `/fast/scratch/hyaku/mori-r28-w2/ReopenS152/`.

## Bounds, tools, installs

Lane writes: this report only. Read-only `git show/grep` in the lane; `curl -sf` and `sha256sum` for fetches;
`python3` for JSON parsing. No installs needed or run (pacman paused host-wide). Privacy: upstream code quotes,
digests and counts only; no OMP settings values, session ids, pids, uids, unit names or journal text.
