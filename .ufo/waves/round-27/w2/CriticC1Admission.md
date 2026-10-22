# CriticC1Admission — round 27, wave 2: C1 admission as a whole

Seat: MoriR27.CriticC1Admission (critic, leaf). Subject: landed tip `5f00fd045c137b7e3835506d69946cfd9d010eb5`,
entering tip `fc09f96c`. I wrote nothing in the lane except this file. Scratch: `/fast/scratch/hyaku/mori-r27/CriticC1Admission/`.

## Verdict: verified (C1 is met for the right reasons), with six fixable defects

The counter's `C1=met` rests on real work. Six new rows (S127–S132) were really opened, and every recorded per-file
sha256 matches a fresh fetch. The entry body uses all six. Every contract topic is covered. There are 7 real decision
rows. Privacy is clean, the retention scan stays at 4, and no row S001–S126 changed identity. C1 is new knowledge on
FR10 and depth is the right axis. No held axis is measurably harmed: tools, selftests, retention and identity are all
unchanged.

The six defects are all fixable, and none changes the count:
- one wrong kernel statement (medium);
- inference markers dropped in the SKILL table, the entry's decision table and the lesson (medium, calibration);
- the entry is missing from the `corpus/README.md` index and the FR10 row (medium, coverage);
- the S131 URL does not reproduce its recorded bytes (low);
- S114's used-by names an entry that does not cite it (low);
- S082 and S092 are used outside their scope cells (low, lane rule).

Smallest corrections are in §6.

## 1. Counter run (frozen bytes)

- `sha256sum .ufo/waves/round-27/count-c1.sh` and `git show 5f00fd0:.ufo/waves/round-27/count-c1.sh | sha256sum` both
  give `697fb7d7…4c01c`. This matches wave-1 CriticC1Counter §header.
- `bash .ufo/waves/round-27/count-c1.sh 5f00fd045c137b7e3835506d69946cfd9d010eb5` →
  `entry=present new_rows_cited=6 skill_rows=10`, `C1=met`, exit 0.
- Wave-1 trap check at the tip (CriticC1Counter §2a):
  - all six rows sit inside `## Registry` (`corpus/SOURCES.md:3-149`; rows at :133-138);
  - each row has exactly 11 cells, no id is duplicated, status is `mined`, and used-by is the exact entry path (G1–G4);
  - no fenced block is in the Round27 section, and the table header carries no entry path (G7a, G7b);
  - no new row reuses a URL from fc09f96c except S133 (G5b; see H6).

## 2. Hand-check list (CriticC1Counter §3a)

| # | Check | Result | Evidence |
|---|---|---|---|
| H1 | each counted row really opened | holds (S131 low defect) | re-fetch 2026-10-22, table below |
| H2 | entry body uses each counted row | holds | entry lines 39, 65, 92, 97 (S127); 70-72 (S128); 85 (S129); 81, 84 (S130); 51 (S131); 89 (S132) |
| H3 | each contract topic covered | holds (one wrong line) | §3 |
| H4 | ≥3 real decision rows under `## Round27` | holds: 7 decision rows plus 3 error-pattern rows | `SKILL.md:727-733`, `:739-741` at 5f00fd0 |
| H5 | privacy; retention ≤ 4 | holds | §4 |
| H6 | S001–S126 identity | holds | §4 |

H1 re-fetch: plain `curl -sS -L` on each URL in the row, on 2026-10-22, then `sha256sum`.

| Row | File | Recorded sha256 (prefix) | Re-fetch | Line check (grep -n or sed -n on the fetched bytes) |
|---|---|---|---|---|
| S127 | base.c / oom.h / fork.c | cef1a2cf / 6b00b4d0 / 359882ea | equal ×3 | base.c:597 formula, :1131-1133 floor, :1275-1279 range; fork.c:1768-1769, :1949-1966 |
| S128 | adj page / score page | 769edf3b / 6169628d | equal ×2 | adj :86-88 "root processes are given 3% extra memory", :102-103 "is added to the badness score"; footers :175 / :120 "Linux man-pages 6.19" |
| S129 | systemd.exec.xml / systemd-system.conf.xml | 44b89bff / 16135998 | equal ×2 | exec :1299-1300 "normally at 0"; conf :305-306 "plus 100" |
| S130 | user@.service.in / main.c | 72c2f40d / 5ecdca43 | equal ×2 | unit :35 `OOMScoreAdjust=100`; main.c:3063 `saturate_add(a, 100, …)`; patch :4, :12-16 (0/100/200 placement) |
| S131 | earlyoom.default / tree listing | c0770413 / 8b3c95cf | equal / **differs** | default :5 `EARLYOOM_ARGS="-r 3600"` holds. See the S131 note below. |
| S132 | five files + tag tarballs | tarballs d5c557d2 / 2366bc56 | tarballs equal | shell.rs:134, c-bindings.cpp:58 verbatim. Whole-tree `rg -l -uu -e oom_score_adj -e OOMScoreAdjust`: 9,294 omp files and 20,093 Bun files, 0 hits, and 0 for `-i 'oom[_ -]?score'`. |

S131 note: the row's URL `…/git/trees/v1.9.0` returns 8,757 B, 31 entries and sha256 `92f8c2c9…`. Only
`…/git/trees/v1.9.0?recursive=1` returns the recorded 19,112 B, `8b3c95cf…`, 67 entries and 60 blobs, with
`earlyoom.default` at :375 and `"truncated": false` at :535.

Other H1 notes:
- S132 records no per-file hash and no tarball URL. The hashes reproduce from
  `github.com/<owner>/<repo>/archive/refs/tags/<tag>.tar.gz`.
- Installed versions: `bun --version` → `1.4.3`. `strings` on the installed omp binary finds `18.12.6` (3 hits). omp was
  not run.
- Re-opened rows the entry relies on also match: S003 `452f1348`, S082 `e760f716`, S092 `a9433bb0`, S118 `b32e0fad`.
  Their cited lines hold: oom_kill.c:160-167, :216-222, :228-234, :998-1006, :1040-1053; proc.rst:1761-1763 "0 (never
  kill) to 1000"; cgroup-v2.rst:1450-1466 memory.oom.group; kill.c:24-32, :357-359, :391-401, :404-427, :429-465,
  :467-478, :587-592, :627, :652-657; main.c:289, 292, 302; MANPAGE.md:19-21, 89-90, 177-203; earlyoom.service.in:12, 14.

## 3. Entry statements attacked (H3)

| Statement (entry line at 5f00fd0) | Verdict | Severity | Evidence |
|---|---|---|---|
| "The kernel keeps the highest score; a tie keeps the first task scanned (`:340`)" (:64) | **wrong** | medium | See the tie note below. |
| earlyoom key is `oom_score`; exact tie goes to larger RSS (:25-29) | holds | — | kill.c:457-465 |
| prefer/avoid ±300, `--sort-by-rss` ±3,145,728 KiB, comm-only match (:30-37) | holds | — | kill.c:24-32, :404-427 |
| exported score `(1000 + badness*1000/totalpages)*2/3`, range 0–2000 (:65-68) | holds | — | base.c:583-597 |
| v7.2 has no 3% root discount (:69-73) | holds | — | oom_kill.c:226-235 has none; man page :86-88 claims it |
| user manager 100, children +100 (:81-86) | holds | — | unit :35; main.c:3045-3063; patch :12-16 |
| fleet runtimes set no `oom_score_adj` (:87-91) | holds | — | whole-tree negative re-run (§2) |
| `memory.oom.group` 0 at every measured level (:76-77) | holds now host-wide | — | 90 of 90 cgroup `memory.oom.group` files read `0` |
| unprivileged writes can lower down to the floor; only legacy `oom_adj` ratchets (SKILL `:741`) | holds | — | base.c:1117-1122 (legacy branch refuses below the current value), :1131-1135 (floor) |
| "only earlyoom's +300 `--prefer` adjustment can produce that" (:135; entry decision row :159; SKILL :728) | holds as marked [INFERENCE] at :135; **overstated** at :159, SKILL :728 and lesson :20 | medium (calibration) | See the ceiling note below. |
| "here the floor is 100, because PID 1 wrote the user manager's 100 with privilege" (:98) | wording | low | See the floor note below. |
| contract topic "share of sends that hit fleet processes" (:129-131) | holds, honestly bounded | — | see the share note below |

Tie note: in `mm/oom_kill.c` v7.2, `oom_evaluate_task` at :339-341 skips only `points < oc->chosen_points`, and an
equal score falls through to `select:` (:343-348), which replaces `oc->chosen`. A tie therefore goes to the task
scanned **later**. The adjacency correction at :188 and the SKILL "+200 band" row are unaffected.

Ceiling note: the "kernel ceiling" assumes RSS ≤ RAM. RSS is counted once per mapping: `finish_fault` adds `nr_pages`
to the mm counter for every PTE range it maps (`mm/memory.c:5724-5726` at v7.2, fetched from git.kernel.org,
sha256 `97da178d…c8a1`). So a page mapped twice in one mm counts twice [INFERENCE: a double-mapping on the scale
needed to exceed RAM plus swap is unlikely, so the reading is probably right, but it is not a bound].

Floor note: the floor-setting write comes from the privileged process systemd forks for the unit before exec, not
from the init process itself. base.c:1156-1157 sets the floor when the writer (`current`) holds CAP_SYS_RESOURCE.
This is [INFERENCE] on systemd's exec path; ReviewEntryFact3 owns the detail. The probe result stands.

Share note: the topic is answered by class (python 27, other 11, omp 1), with the caveat that a class is not
membership. The fleet share is between 1/39 and 28/39 [INFERENCE]; the entry never writes that bound.

The send-class evidence prints `unparsed_send_lines=1` in boots -2, -1 and 0
(`evidence/boot-send-classes.txt`). The script counts any non-matching `sending SIG…` line
(`boot-send-classes.py:46-47`), which is earlyoom's startup threshold banner (`corpus/lessons/round-26.md`, boot-0
note). This is consistent with "boot -1 holds all 39". The entry does not explain the counter [low].

## 4. Privacy, retention, identity (H5, H6)

Retention:
- Command: `python3 -I -B tools/mori-retention-gate.py scan --repo <lane> --rev <R> --policy
  .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json`.
- Result: `metric 4` at fc09f96c and at 5f00fd0 (`unallowlisted_hits 4`, the same four paths under
  `.ufo/waves/round-20/falsify/NoHarmRun/`), with `hits 113` at both.
- The contract bound "no landed tip may exceed 4" holds.

Privacy sweep over the added lines of `git diff fc09f96c 5f00fd0` (56 files):
- `user-[0-9]{3,}\.slice|user@[0-9]{3,}\.service|uid[ =:][0-9]{3,}` → 0 lines.
- The pid pattern hits only the init process as a class (two lines).
- No earlyoom send line with a real command line appears. The `sending SIG` hits are format strings, the startup banner
  and the parser regex.
- `oom-score-classes.txt` and `boot-send-classes.txt` hold counts, classes, scores and hours only.
- The entry, its SKILL rows and the six counted rows hold no uid number, pid, command line, `MESSAGE` text or host
  prefer/avoid/ignore value.
- Letter-of-rule note (low): `w1/SrcEarlyoomManpageOptions.md` quotes the *upstream* README's example
  `EARLYOOM_ARGS` line, which contains prefer and avoid expressions. That is public upstream text, not a host value.
  The contract bans "any `--prefer`/`--avoid`/`--ignore` expression", so the closure should rule on it. I do not
  repeat the text here.

Identity:
- `python3 -I -B .ufo/waves/round-27/check-row-identity.py 5f00fd0` → `rows=141 changed=5`, exit 1. The five are S090,
  S093, S096, S097 and S101, all inherited from rounds 24–25 and routed to wave-2 supersede seats.
- At fc09f96c the same check gave `changed=6`, the sixth being S124. This round removes one change and adds none.
- My own column-wise diff, which parses `## Registry` by cells, finds no `source` cell changed for any id up to S126.
  The only non-used-by changes are S124 scope/anchor/teaches, restored to first-published text. S133 reuses S124's
  two URLs as a `supersedes S124 —` row, which `CORPUS.md` Rule 2 (fleet root `CORPUS.md:116-118`) requires. The
  reuse is by design, not a novelty breach.

## 5. Learning claim, axis, held axes

New knowledge on FR10: yes.
- The contract's sweep `git grep -n -i -E 'oom_score|OOMScoreAdjust' <rev> -- corpus/knowledge SKILL.md PROVINCE.md |
  wc -l` gives 0 at fc09f96c and 38 at 5f00fd0.
- Before this round the lane held only one sentence (`corpus/lessons/round-26.md:67`, S114 quote) and S120's -100.
- The entry adds the selection rules, the score scaling, the 200 band's origin, the fleet's rank and the boot -1 class
  split. It also adds a negative result: no fleet record can attribute a kill (Fact 6). Fact 6 directly answers the
  FR10 remainder "fleet attribution of a victim" (`corpus/README.md:342`), as far as host evidence allows.
- It corrects a sibling model. tsukuroi `oom-event-plane.md:116` says the +200 band is "the band the kernel scans
  first", and the S003 code refutes that. The sibling's files were read, not edited.

Depth is the right axis.
- The depth row's evidence is "source-linked knowledge entries with `source:`/`verified-at:`/`recheck:` lines"
  (`SCORECARD.md:12`), and the entry has all three (entry :1-3).
- Facts 4–6 are host measurement, which is coverage-like. They are bounded aggregates that serve the sourced core, so
  they do not change the axis.

Held axes:

| Axis | Harmed? | Evidence |
|---|---|---|
| operability 7 | no | `git diff --quiet fc09f96c 5f00fd0 -- tools` → identical, and the working tree equals the tip. Tallies keep: oom-killers `PASS 32/32`, job-runway `PASS 21/21`, pressure `PASS 12/12` with `MATCHER: rejected 48/48`, census `PASS (134 cases, 134 passed, 0 failed)`; also journal-window 16/16, wave-settlement 23/23, seat-terminal 49/49, all exit 0. The contract does not name "the five", so I ran all of these. |
| freshness 5 | no | the entry carries `verified-at` and per-source `recheck` (:2-3). The S131 URL defect makes one recheck non-reproducible as written (low). |
| calibration 5 | slight, fixable | three places state as fact what the entry marks [INFERENCE] (§3 and the fix below) |
| coverage 6 | no regression; one omission | the entry is the only one of 36 `corpus/knowledge/*.md` files missing from `corpus/README.md` (loop over `git ls-tree`; the r26 precedent is indexed at README:35). README:342 (FR10 row) and `PROVINCE.md:53` still list "fleet attribution of a victim" with no pointer to the r27 entry. |
| adjacency 6 | no | the tsukuroi claim is cited, not absorbed (entry :185-190); source ids are marked lane-local |

## 6. Smallest safe corrections (exact old → new; for agent://MoriR27)

1. Entry `corpus/knowledge/oom-victim-selection-r27.md:64`:
   - old: `The kernel keeps the highest score; a tie keeps the first task scanned (`:340`).`
   - new: `The kernel keeps the highest score; an equal score replaces the earlier pick, so a tie goes to the task scanned later (`:340` skips only a strictly lower score).`
2. `SKILL.md:728` and entry decision row `:159`:
   - old: `a `--prefer` match added 300 to that victim`
   - new: `a `--prefer` match added 300 to that victim [INFERENCE: assumes the victim's resident set, swap entries and page tables fit within RAM plus swap]`
3. `corpus/lessons/round-27.md`, two edits:
   - line 18, old `The in-session seats live inside one `omp` process,` → new `The in-session seats live inside one `omp` process [INFERENCE, entry Fact 4],`
   - line 20, old `carry a score only a prefer match can produce` → new `carry a score that only a prefer match can produce under the entry's stated assumption [INFERENCE]`
4. `corpus/README.md`: insert after the r26 index row (line 35) a new row. Then, in the FR10 row (line 342), change
   old `and fleet attribution of a victim. |` → new `and fleet attribution of a victim (round 27: selection rules and process-class attribution in `knowledge/oom-victim-selection-r27.md`; seat- or lane-level attribution stays frontier). |`. The new index row:
   ```text
   | `knowledge/oom-victim-selection-r27.md` | how earlyoom 1.9.0 and the Linux 7.2 kernel choose an OOM victim (`oom_score`, `--prefer`/`--avoid`/`--ignore`, `--sort-by-rss`, `memory.oom.group`), where the fleet's `oom_score_adj` 200 comes from (user manager 100 plus 100), the fleet's place in the host ranking and the boot -1 send classes (counts and classes only); no fleet record attributes a kill to a seat | S127–S132 (with S003, S082, S092, S115, S118–S120); `.ufo/waves/round-27/evidence/` |
   ```
5. S131 (the row is append-only, so do not edit its source cell). Change the lesson Gate row at
   `corpus/lessons/round-27.md:74`:
   - old: `(with the v1.9.0 tag tree)`
   - new: `(with the v1.9.0 tag tree, fetched as `https://api.github.com/repos/rfjakob/earlyoom/git/trees/v1.9.0?recursive=1`; the row's URL omits `?recursive=1`, and only the recursive listing reproduces its sha256 and line anchors)`
   - A superseding row is the heavier alternative.
6. S114 used-by (mutable, logged), `corpus/SOURCES.md:120`:
   - old: `corpus/knowledge/userspace-oom-killers-r26.md, corpus/knowledge/oom-victim-selection-r27.md`
   - new: `corpus/knowledge/userspace-oom-killers-r26.md`
   - Then drop S114 from the list at `corpus/lessons/round-27.md:94`. The entry never cites S114
     (`grep -c 'S114\|README'` → 0), and `CORPUS.md:107` defines used-by as the entries "citing the row".
7. Optional (low): S082's scope cell reads "textual mountinfo field layout only" and S092's reads the pressure files
   only, yet both now list the r27 entry. Lesson :83-87 already records why no anchor was added (Rule 2), so this is
   a documented tradeoff, not a defect.

None of 1–7 changes `count-c1.sh` output: none touches line 1 of the entry, rows S127–S132, or the row-counting
lines of the Round27 section. Re-run the counter after applying them.

## 7. Notes

- Not re-run: the S130 `units/` tarball sweep, the S132 per-file anchors beyond the two quoted lines, the host
  process sample and the journal aggregates. Re-running the journal read would only reproduce counts the entry
  already commits.
- The lane working tree showed uncommitted edits to `SKILL.md` and the entry by the integrator during this review.
  I attacked committed bytes at 5f00fd0 only.
- Tooling: nothing installed or upgraded. I used curl, sha256sum, git (read-only), rg, tar, python3 and strings
  already on the host. No subagents and no background jobs.
