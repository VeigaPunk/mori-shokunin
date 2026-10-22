# RerunC1Count: independent re-run of the C1 counting command (round 24, wave 2)

Seat: MoriR24.RerunC1Count (leaf; no subagents; no peer messages). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`. Measured tip: `a730ecfefbdb5c31b1db13aca2c40eecd5e97abc`. Lane HEAD moved during the review: `89849a7` at the first check, then `6a344d2`, then `a536b1844c99895d1b96a520d9a4cdd7fd3c85ea` at the final check. Scratch: `/fast/scratch/hyaku/mori-r24-a2/w2/RerunC1Count/`.

## Result

- **Declared after-value reproduces.** `python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-routed-check.py --repo /home/vgpnk/Projects/shokunin/mori-shokunin --rev a730ecfefbdb5c31b1db13aca2c40eecd5e97abc` (default round 24, the SCORECARD form) prints held 4, items 4, exit 0. Explicit `--round 24` gives the same output. The same holds at lane HEAD `a536b18` (held 4, items 4, exit 0).
- **Declared before-value reproduces.** At `c725aa37` (default round 24) the tool prints held 3, items 4, exit 1. The one red item is R4, reason `no_round_ledger`.
- **Real-defect measure reproduces (A4).** At `c725aa37 --round 23`: held 3, items 4, exit 1. R4 is red with 20 reasons. Eight rows precede dispatch commit `22772c1` (18:10:59Z).
- **Findings:** one Medium (a latent gap in the R2 added-line scan; not triggered at the tip), four Low, and informational items. None falsifies the declared after-value at `a730ecfe`.

## 1. Runs

Every run is `python3 -I <tool> --repo <repo> --rev <rev> [--round N]`. Stdout is one JSON line. Stderr was empty in every run. Output files are under the scratch directory.

| Run | Repo | Rev | Round | held/items | status | exit | R4 | Notes |
|---|---|---|---|---|---|---|---|---|
| A | lane | c725aa37 | 23 | 3/4 | failed | 1 | red, 20 reasons (section 2.1) | rows read; R1-R3 held |
| B | lane | c725aa37 | 24 | 3/4 | failed | 1 | red, `no_round_ledger` | rows read; R1-R3 held |
| C | lane | a730ecfe | 24 | 4/4 | held | 0 | held | rows read; R1-R3 held |
| D | lane | a730ecfe | default | 4/4 | held | 0 | held | declared form; stdout byte-identical to C (`cmp`) |
| E | lane | c725aa37 | default | 3/4 | failed | 1 | red, `no_round_ledger` | declared before form; stdout byte-identical to B (`cmp`) |
| F | lane tool pinned from `git show a730ecfe:tools/mori-routed-check.py` (sha256 64921a0c...), run from scratch | a730ecfe | 24 | 4/4 | held | 0 | held | stdout byte-identical to C (`cmp`) |
| G | no-checkout clone of the lane (no working tree) | a730ecfe | 24 | 4/4 | held | 0 | held | rows identical to C |
| H | no-checkout clone | c725aa37 | 23 / 24 | 3/4 / 3/4 | failed | 1 / 1 | as A / as B | rows identical to A and B |
| I | no-checkout clone | a730ecfe | 23 | 3/4 | failed | 1 | not row-compared | counts only |
| J | no-checkout clone | 89849a7 | 23 / 24 | 3/4 / 4/4 | failed / held | 1 / 0 | not row-compared / held | counts only |
| K | lane | 89849a7 | 24 | 4/4 | held | 0 | held | rows read; R1-R3 held |
| L | lane | a536b18 (HEAD) | 24 | 4/4 | held | 0 | held | rows read; R1-R3 held |

Negative controls (all stderr empty; exit codes match the contract: 0 held, 1 any item failed, 2 cannot evaluate; constants at `tools/mori-routed-check.py:42-44`):

| Control | Exit | status and error |
|---|---|---|
| `--rev 0000000000000000000000000000000000000001 --round 24` | 2 | could-not-evaluate; "revision does not resolve to a commit" |
| `--repo /nonexistent/path --rev a730ecfe --round 24` | 2 | could-not-evaluate; "repository path is not a directory" |
| `--round 0` | 2 | could-not-evaluate; "round must be a positive integer" |

R1, R2 and R3 are held with no reasons in every run where I read or row-compared the rows (A, B, C, E, G, H, K, L; F is byte-identical to C). Runs I and J were checked by counts only.

## 2. R4 reasons

### 2.1 Run A (c725aa37, round 23): 20 reasons, in output order

- `attempt_ledger_not_clean` x1
- `ledger_finding:AT_INVALID`, `ledger_finding:LEGACY_ROW_UNBOUND`, `ledger_finding:STARTED_MISSING`, one each
- `dispatch_path_missing` x8. These are rows 1-8 of `wave1-attempts.json`, which have no dispatch path.
- `dispatch_committed_after_dispatch` x8. These are rows 1-8 of `wave1-ledger.json`, which name `wave1-run.json`.

Ledgers found: `wave1-attempts.json` (verify exit 1, failed), `wave1-ledger.json` (clean, 8 rows), `wave2-ledger.json` (clean, 1 row, bound before call). Specs `wave1-spec.json` (wave `mori-r23-build`) and `wave2-spec.json` (wave `mori-r23-falsify`) each resolve to a started ledger, so no spec reason is raised.

A4 check: dispatch commit `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687` has committer time 2026-10-21T15:10:59-03:00, which is 18:10:59Z (`git log -1 --format=%cI,%ct`). The eight `wave1-ledger.json` rows are at 17:03:11.644975Z through 17:24:14.626546Z, which is 46.7 to 67.8 minutes earlier. The A4 statement reproduces.

### 2.2 Runs B and E (c725aa37, round 24): one reason, `no_round_ledger`

No `.ufo/waves/round-24/` ledgers or specs exist at `c725aa37`. This absence is what the declared before-value measures (F10).

### 2.3 Runs C, D, F, G, K and L (landed tip and HEAD, round 24): R4 held

- One ledger at a730: `.ufo/waves/round-24/wave1-attempts.json`. Verify exit 0, status clean, finding `LEDGER_CLEAN`.
- One row: `at` 2026-10-22T05:14:13.926366-03:00 (epoch 1792656853). Dispatch `wave1-run.json`, last changed by commit `06d4f4d` at 2026-10-22T05:13:57-03:00 (epoch 1792656837). Status `bound_before_call`. Margin 16 s.
- Spec `wave1-spec.json` (wave `mori-r24-w1`) maps to `wave1-attempts.json`, whose last row result is `started`.
- At HEAD `89849a7` (run K), a second ledger `wave2-attempts.json` has one row: `at` 05:56:44.920676-03:00, dispatch commit at 05:56:36-03:00, margin 8 s, clean. Spec `wave2-spec.json` is started.

The pass is substantive, not vacuous. The verifier reads the committed dispatch payload at REV and checks each row's `payload_sha256`, `payload_bytes` and `tasks_count` (`tools/mori-dispatch-ledger.py:120-164`, `218-240`). That identity covers `context` and `tasks` only (F8).

## 3. Declared values

| Declared value | Where declared | Reproduced? | Evidence |
|---|---|---|---|
| Before: `--rev c725aa37 --round 24` gives held 3 (no round-24 ledger) | `.ufo/waves/round-24/contract.md:43` (C1 Before; kept by A4) | Yes | B, E |
| Before: "3 of 4 held (no round-24 pre-call ledger)" | `SCORECARD.md:1501` | Yes | E |
| A4 real defect: `--rev c725aa37 --round 23`, R4 red, eight rows precede the dispatch commit | `contract.md:150-151` | Yes | A and section 2.1 |
| After-value: prints held 4 of items 4, exit 0, at the landed tip | `contract.md:44-45` (C1); A4 says unchanged; `SCORECARD.md:1501` | Values yes; literal text no | D: held 4, items 4, exit 0. `grep -c '"held": 4'` on C returns 0 (F2) |
| R4 predicate: the last-changed commit time is at or before `at` | `contract.md:146-149` | Implemented as stated | `tools/mori-routed-check.py:300-315`, `606-614` |
| QUALITY criteria 72-75 tagged `routed r23-R1` to `R4`, naming the check | `corpus/QUALITY.md:308-332` | Present | read |

The contract's R4 table row (`contract.md:25`) still says "first added" (F3).

## 4. Findings

### F1. Medium (latent; not triggered at the tip). The R2 added-line scan drops content lines that begin with "++ "

- Mechanism. `_added_lines` treats any diff line starting with `+++ ` as a file header (`tools/mori-routed-check.py:249-257`). That branch runs before the added-content test (`260-261`). A content line `++ X` appears in the diff as `+++ X`, so it is dropped. The R2 regex runs only on the lines `_added_lines` returns (`428-437`).
- Probe (neutral text only; scratch clone, scratch commit `365e13c4` on top of a730). The added lines of `corpus/knowledge/parser-probe.md` were `plain probe line`, `++ parser probe line` and `after probe line`. `git diff` shows the middle line as `+++ parser probe line`. `_added_lines` returned `('corpus/knowledge/parser-probe.md', 'plain probe line')` and `('parser probe line', 'after probe line')`. The middle line vanished, and the last line was attributed to the path `parser probe line`, because `current` was overwritten (`254-256`).
- Tip status. `git diff c725aa37 a730ecfe` over the R2 scope (SCORECARD.md, PROVINCE.md, SKILL.md, LOG.md, README.md, corpus/) has 0 added content lines beginning `+++ ` and 0 added lines containing `privacy_clearance` in any case. The tip result is not affected.
- Impact. R2 can report held while a line in the R2 scope would match the R2 regex, provided its content begins with `++ `. QUALITY criterion 73 ("no added line ... asserts privacy clearance") and the after-value's `held: 4` then overstate R2.
- Direction for the lane: track hunk line counts from each `@@` header, or compare per-file blobs. Add a selftest with a content line that begins `++ `.

### F2. Low. The declared after-value text does not occur in the output

The tool prints compact JSON (`tools/mori-routed-check.py:654`, `separators=(",", ":")`), so the output has `"held":4,"items":4`, never `"held": 4`. The values reproduce, but a literal match returns no hits. Fix the SCORECARD or contract wording to name the JSON fields, or pretty-print the output.

### F3. Low. Stale R4 predicate in the contract table

`contract.md:25` still says "the committer time of the commit that first added its `dispatch_path`". A4 (`contract.md:146`) and the code (`_last_change_epoch`, `tools/mori-routed-check.py:300-315`, `606-614`) use the commit that last changed it. SKILL.md:642, QUALITY.md:327-328 and BuildRoutedCheck.md:208 all say last-changed. The table row was never amended. The strict rule is the implemented one, so this is a documentation defect.

### F4. Low. The mutant count does not match its table

QUALITY.md:312 and SKILL.md:642 say "thirteen sandbox mutants ... turn the named row red". `.ufo/waves/round-24/w1/BuildRoutedCheck.md:194-210` marks 12 rows red (M1, M1b, M1c, M2, M2d, M2e, M3, M3b, M4, M5, M6, M7), two green negative controls (M2b, M2c) and one control (M0). The battery ran on a clone checked out at `4059ffb` (`BuildRoutedCheck.md:190-191`), not at the landed tip. I did not re-run it.

### F5. Low (rule check; for the lead to decide). A `.ufo` report quotes a privacy-clearance key set to the true value

`.ufo/waves/round-24/w1/BuildRoutedCheck.md:200` has a table cell that quotes such a line as a mutant example. Amendment A1 puts `.ufo/**` outside the R2 scan, and a quotation does not assert clearance. The run rule in this assignment forbids writing such lines, though. I did not reproduce the line here.

### F6. Informational. The after-value rests on one dispatch

Run C checks one row (wave1) with a 16-second margin. HEAD adds one row (wave2) with an 8-second margin. The pass is substantive (section 2.3), but thin.

### F7. Informational. Time-predicate limits (A4 discloses both)

(a) `int(at.timestamp())` drops the microseconds (`tools/mori-routed-check.py:608`, `612`). Git committer times have whole-second resolution, so a commit in the row's own second passes "at or before". Not exercised. (b) Both times are lane-written, so R4 proves recorded ordering, not harness-observed ordering.

### F8. Informational. Payload identity covers `context` and `tasks` only

`tools/mori-dispatch-ledger.py:120-164`. Other dispatch fields can change without R4 noticing. `BuildRoutedCheck.md:229-230` discloses this.

### F9. Informational. R2 scope excludes `.ufo/**` and `tools/**` (A1)

`tools/mori-routed-check.py:54-64`. Controls M2b and M2c in `BuildRoutedCheck.md:201-202` stay green, as designed. This is disclosed, and QUALITY criterion 73 names only self-assessment and knowledge surfaces, which is accurate.

### F10. Informational. The before-value is absence-based

The 3-of-4 in runs B and E comes from `no_round_ledger`, not from the defect. `SCORECARD.md:1501` and A4 disclose this. The informative before-measure is run A.

### F11. Informational. Lane HEAD moved; the checked tools did not

Between `a730ecfe` and `a536b18` the commits are `753d227`, `13208d2`, `89849a7`, `6a344d2` and `a536b18`. `tools/mori-routed-check.py` (blob `3337232b...`) and `tools/mori-dispatch-ledger.py` (blob `b86525c6...`) are byte-identical to a730 at HEAD and in the working tree. Their sha256 values are 64921a0c... and 9ec14ed3..., which match the a730 blob contents. The committed evidence `c1-before-round23.json` and `c1-before-round24.json` (HEAD) match runs A and B row for row. `c1-after-13208d2.json` records rev 13208d2 with held 4, items 4.

## 5. Not tested or residual

- Mutant battery and C2 (`MORI_PRESSURE_SELFTEST`, live bracket check): not re-run here.
- Same-second tie (F7a): not exercised.
- Pathspec magic: `git log -1 --format=%ct <rev> -- <dispatch_path>` (`tools/mori-routed-check.py:306-310`) treats the path as a pathspec. [INFERENCE: a committed dispatch file whose name contains glob characters could take another file's commit time.] Not tested.
- The base-unreadable exit 2 path and a non-integer `--round` usage error were not run.
- Regex variants of the R2 pattern (`tools/mori-routed-check.py:49-52`) were not tested.

## 6. Method, tooling and integrity

- Tools: `python3` 3.14.8 (for the `-I` runs and the probe). `jq` reports as jaq 3.1.1 (used for reading JSON only). `git` was read-only (`log`, `show`, `diff`, `cat-file`, `rev-parse`, `status`, `grep`), plus `clone` from the lane. No installs or updates: no pacman, uv, cargo or npm commands. There is nothing for the install table.
- Environment: `PYTHONDONTWRITEBYTECODE=1` was set on all runs except the first three. The routed-check tool imports no local module and the ledger tool runs from stdin, so no cache write was expected. `tools/__pycache__/mori-dispatch-ledger.cpython-314.pyc` is untracked and dated 05:19:16 -03:00, before this review. I did not create it. The `tools/` directory mtime stayed at 05:45:30.
- Lane writes: this report only. No git add, commit, stash, checkout, reset, pull or push in the lane. Sibling-owned tracked edits (PROVINCE.md, corpus/SOURCES.md, corpus/knowledge/system-pressure-r24.md, corpus/lessons/round-24.md) were not touched.
- Scratch: the pinned tool copy, a no-checkout clone (135 MB), and a probe clone with one neutral scratch commit. No mutant touched the lane.
