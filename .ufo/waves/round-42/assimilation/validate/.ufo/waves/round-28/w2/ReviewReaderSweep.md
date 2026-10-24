# ReviewReaderSweep — QUALITY 77 reader-sentence sweep

**partial** — attacked the QUALITY 77 repoint of the eight superseded rows in live readers at
`f2de0eedcd60d2e354da75265ea6122bc3896073`. One structural miss and three wording defects exist at the
attack revision; all were independently fixed by `ac696ad` ("round-28: wave-2 corrections"), whose
presence at the tip corroborates them. Two residual defect classes survive at the tip (`ac696ad`).

## Method (all committed bytes)

- `git grep -n -w -E 'S096|S097|S101|S127|S128|S129|S131|S140' f2de0ee… -- SKILL.md PROVINCE.md
  corpus/README.md corpus/knowledge` → exactly one hit: `oom-victim-selection-r27.md:203`, a
  tsukuroi-namespace sentence ("tsukuroi S115, S118, S120 and S127"), correctly left un-repointed.
- `git diff 6ebd518f f2de0ee…` → 26 repointed lines across 6 files (SKILL 2, PROVINCE 4, README 1,
  harness-job-capacity 4, oom-victim-selection 9, system-pressure 6).
- `bash .ufo/waves/round-28/count-c1.sh <rev>` at three revisions; `git log` topology read-only.
- Each repointed line checked against its new row's `teaches` (full text read at `f2de0ee`; S147's
  at `ac696ad` because the row is absent at the attack revision).

## Findings (severity order)

### F1 — critical at the attack revision, resolved at tip: two repointed citations are dangling

`corpus/knowledge/harness-job-capacity-r25.md:1` and `:47` cite **S147**, but `corpus/SOURCES.md` at
`f2de0ee` holds no S147 row (rows run S146→S148 at consecutive lines 152–153). Observed:
`count-c1.sh f2de0ee` prints `superseding=7/8`, `fail S147 row_absent`, `C1=unmet`, exit 1.
Topology: the repoint and rows S148–S150 landed in `f2de0ee` itself; row S147 landed one commit
later in `6b695b0` ("S147 (supersedes S101), last C1 row"), and `count-c1.sh` at `84abe93` and at
tip `ac696ad` prints `superseding=8/8`, `readers_left=0`, `C1=met`, exit 0. So at the assigned
revision the reader was repointed to a row that did not yet exist — the counter caught it (`fail
S147 row_absent`), and `6b695b0` is evidence the omission was repaired the commit after.

### F2 — wording contradicting the new row, fixed at tip (three defects)

1. **`S146` labelled "rejected" although the row is `mined`.** `PROVINCE.md:258` ("`proc_pressure(5)`
   does not exist (S146, rejected)"), `system-pressure-r24.md:1` ("Rejected candidate: S146"),
   `:224` ("S146, rejected: HTTP 404"). S146's status at `f2de0ee` is `mined` (SOURCES:152); it
   supersedes the rejected *candidate* S097 but is itself an admitted tier-A row. Tip `ac696ad`
   rewrites all three ("S146: no such page in the man-pages 6.20 release; the man7 URL returns HTTP
   404" / "Absence source: S146 (… mined, supersedes the round-24 rejected candidate…)"), confirming
   the defect.
2. **`harness-job-capacity-r25.md` paragraph keeps S140's superseded floor teaching.** With the
   paragraph repointed to S152, it still read "the explicit floor `Math.max(1, …)` did not survive
   that rewrite — neither the clamp expression nor the accessor … carries a floor at v18.12.6"
   (`:282-283` at `f2de0ee`). S152 teaches the opposite: the floor moved into the per-check getter
   (`job-manager.ts:305`, quote `return Math.max(1, Math.floor(value ?? DEFAULT_MAX_RUNNING_JOBS));`)
   — "the cap never lost it". Tip fixes: "…but the job manager's own cap getter still floors the cap
   at 1 (S152 …; wave-2 CriticC1Admission F1)". The U1 changelog line at `:330` carried the same
   superseded reading ("the explicit floor of 1 did not survive the rewrite. The round-26 draft's
   'floor of 1 held' was false"); tip rewrites it to "left the sdk clamp … while the job manager's
   getter kept it" and "'floor of 1 held' was imprecise rather than false".
3. **`oom-victim-selection-r27.md` sibling-commentary prose carries S129's superseded reading.** At
   `f2de0ee` `:200` the file read "the `systemd.exec` default quoted at `kill-event-deep-r8.md:142`
   describes the system manager". S150 teaches the page names **no manager type**
   (`systemd.exec.xml:1299-1300`). This line cited no id, so no diff line reached it; tip `ac696ad`
   corrects to "names no manager type (S150; round-28 correction of 'describes the system manager',
   wave-2 ReopenS150)" — confirming it was a live contradiction at the attack revision.

### F3 — residual at tip: range citations still reach superseded rows (word-grep blind spot)

`readers_left` counts `-w` matches; ranges containing a superseded id are invisible to it. Still
present at `ac696ad` (untouched by wave-2 corrections):

- `corpus/knowledge/harness-job-capacity-r25.md:3` — "re-open S098–S103, S112–S113 and S138–S141"
  covers S101 and S140; after supersession the live rows are S147 and S152.
- `corpus/knowledge/harness-job-capacity-r25.md:232` — "re-open S098–S103".
- `SKILL.md:646` — "(sources S098–S104, S112–S113)" no longer matches the entry's own source list
  (which names S147, not S101) and still reaches restored S101.
- `PROVINCE.md:318` — "the upstream sources opened this round are S098–S103 and S112–S113".

Re-opening the restored rows' URLs is still workable, so this is a staleness, not a wrong claim —
but a future recheck would read the superseded teaching, which is what QUALITY 77 exists to prevent.

### F4 — residual at tip: "sources opened this round" now misdates the new rows

- `PROVINCE.md:257` — "sources opened this round … (S090–S095, S145)": the section describes the
  round-24 landing; S145 was opened in round 28 (lesson Gate `corpus/lessons/round-28.md:65`,
  2026-10-22T17:59:57Z). Same shape at `PROVINCE.md:318` (S098–S103 opened round 25 vs S147 opened
  round 28). Present at `f2de0ee` and at `ac696ad`.

### F5 — minor pointer trim: `systemd-system.conf.xml:305-306` vs S150's `:305-307`

`oom-victim-selection-r27.md:78` (at `f2de0ee` and tip) cites "the manual sentence is S150
`systemd-system.conf.xml:305-306`". The cited sentence runs to `:307` — upstream v262 bytes show the
closing parenthetical "(this makes service processes slightly more likely …)" on the line after
`:306` (fetched 2026-10-22T19:04:09Z, sha256 `16135998…0c58`, matching S150's anchor digest), and
S150's own anchor is `:305-307`. The citation truncates the sentence's tail.

## Repointed lines verified to hold (24 of 26)

SKILL.md:619 (S145 = PSI_IRQ commit), SKILL.md:722 (S148, S150 swap), PROVINCE.md:377-378 and
README.md:36 (old `S127–S132` correctly re-listed as S148, S149, S150, S130, S151, S132, S142),
system-pressure :30, :41, :61, :110, :177 (S145 rationale = "we only use PSI_IRQ_FULL", patch
:15-17), system-pressure :1 (supersede notes, minus the F2.1 status word), oom-victim-selection :1,
:37 (S148 base.c:597 formula :592-597), :48 (S151 `earlyoom.default:5` = the only active
`EARLYOOM_ARGS=-r 3600`), :55, :63, :66 (S149 adj :86-88/:102-103 anchors match), :72, :84
(fork.c:1768-1769,1949-1966 = S148 anchors), :89 (base.c:1131-1133,1156-1157 inside S148's
:1131-1135/:1155-1158), harness :277 (S152's `() => Math.min(100, cfgAsyncMaxJobs.get(settings) ??
100)` at `6962d5cd:1949` is consistent with "?? 100 fallback dropped the same day" via S141), and
the quote at harness :47 — verified verbatim against upstream bytes: `docs/settings.md:623`
"`async.maxJobs` | number | `100` | Running background-job cap, floored to at least 1; parked/queued
jobs do not consume execution slots." (fetched 2026-10-22T19:05:20Z, sha256
`0b2e1457021fa526f2c35015672f1d7ccbac95e7b9f217528ab8022c55ed5883` — matches S147's anchor).

## Non-findings checked

- `oom-victim-selection-r27.md:203` "tsukuroi S115, S118, S120 and S127": sibling-lane ids, not
  mori rows; correctly excluded from the repoint and from `readers_left`.
- `README.md:36` "S148–S151 supersede the round-27 rows": range covers exactly the four needed ids.
- S147 teaching (at tip, `SOURCES.md:153`) is omission-not-contradiction ("the page omits the
  maximum, it does not contradict it"); both S147-citing sentences are descriptive and consistent
  with it once the row exists.

## Tooling / bounds

No installs or upgrades (pacman is paused host-wide; nothing was needed beyond git, curl, sha256sum,
sed). Read-only git only; no lane writes except this file. External sources: two upstream fetches
recorded above (URL, UTC time, sha256). Time: ~12 min.

## Verification gaps

- I did not re-derive every in-line file anchor in S148/S151 against upstream bytes (spot-checked
  only the two flagged pointers); the rows' own digests and the lesson Gate cover the rest.
- Whether F3/F4 warrant a wave-2 correction at the tip is for the integrator; both survive `ac696ad`.
