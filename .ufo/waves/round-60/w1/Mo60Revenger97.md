# Mo60Revenger97 — r59 absent-set arrival reconstruction (read-only)

Seat: `Mo60Revenger97` (revenger, leaf). Scope: reconstruct *when* each of the five
frozen seat files (`Mo59Executor40`, `Mo59MutationTester31`,
`Mo59MutationTester32`, `Mo59Critic29`, `Mo59Reviewer16`) actually landed, and
compare that against what the r59 report and the r59 lesson each claimed; return
the reconciled timeline. No production file, SCORECARD, LOG, corpus registry or
lane VCS was touched. Scratch `/fast/scratch/hyaku/mori-r60/Mo60Revenger97/`
created, used only as `TMPDIR`, left empty.

All reads are `git show` / `git ls-tree` / `git cat-file -e` / `stat` at named
revisions. No counter was executed for this seat (see §7).

## 1. Reference points (committer date = landing; author date is not)

`git log -1 --format='author=%ai committer=%ci parents=%p' <rev>`

| rev | author | committer | note |
|---|---|---|---|
| `7b86704d` | 03:00:09 | **03:00:51** | r59 frozen DATA rev (K11→prose) |
| `bf6c0ad3` | 03:00:51 | **03:12:38** | r59 integration: 62 `.md` + `swarm-registry.json` |
| `08127c99` | 03:12:38 | **03:12:53** | orchestrator dispatched marker (w1 tree unchanged) |
| `9e9973ed` (fleet) | 02:35:23 | **03:13:02** | r59 report FILED |
| `f091bd77` | 03:12:53 | **07:42:42** | adds Ex40+MT31, modifies MT32, adds `w1-results.json` |
| `56a2beff` (fleet) | 07:42:03 | **07:43:54** | r59 report AMENDED (64/64) |
| `a86e5f83` | 07:42:42 | **07:43:47** | r59 lesson rewritten ("all 64 after WAVE-DONE") |
| `ddfb12fb` | 07:43:47 | **07:48:31** | r60 entering (spot-check committed here) |
| `398d3225` | 12:53:13 | **12:58:36** | r60 C1 data: absent-set table lands |

Methodological finding, stated once here and used throughout: **every commit's
author date equals its parent's committer date** (`be737211`→`7b86704d`→
`bf6c0ad3`→`08127c99`→`f091bd77`→`a86e5f83`→`ddfb12fb` all chain exactly). The
author timestamps are therefore export artefacts, not content-arrival times.
This is not academic: `f091bd77`'s **author date 03:12:53 precedes the report
filing 03:13:02 by 9 s**, so a verifier reading `%ai` would conclude the late
files arrived *pre*-filing and would contradict the frozen table. Landing must
be read with `%ci`. [INFERENCE on the cause: jj/git export rewrites the chain;
OBSERVED: the exact author==parent-committer equality for all seven.]

Corroborating filesystem mtimes (`stat -c '%y'`, working copy never re-checked-out,
so these are content-write times):

```
2026-10-28 03:11:11.725795038  w1/Mo59Reviewer16.md
2026-10-28 03:11:48.101808161  w1/Mo59Critic29.md
2026-10-28 03:13:08.870235577  w1/Mo59MutationTester32.md
2026-10-28 03:13:49.955910629  w1/Mo59MutationTester31.md
2026-10-28 03:17:30.208841892  w1/Mo59Executor40.md
2026-10-28 02:52:21.776834990  w1/swarm-registry.json
2026-10-28 07:42:05.898036451  w1-results.json
```

## 2. Arrival ledger (git truth)

`git ls-tree -r --name-only <rev> .ufo/waves/round-59/w1/` → `.md` counts:
`7b86704d` **0** (the `w1/` directory does not exist at that revision),
`bf6c0ad3` **62**, `08127c99` **62**, `f091bd77` **64**, `HEAD` **64**.

`git diff --name-status bf6c0ad3 f091bd77` scoped to the dir:
`A w1/Mo59Executor40.md`, `A w1/Mo59MutationTester31.md`,
`M w1/Mo59MutationTester32.md` — nothing else.
`git diff --stat bf6c0ad3 08127c99 -- .ufo/waves/round-59/` → only
`w1.ready.dispatched | 2 ++` (the 62-file tree is byte-identical).

| file | first appears | later change | at filing (03:13:02) | at r60 tip |
|---|---|---|---|---|
| `Mo59Executor40.md` | `f091bd77` (07:42:42) | — | **absent** (written 03:17:30) | present |
| `Mo59MutationTester31.md` | `f091bd77` (07:42:42) | — | **absent** (written 03:13:49.9) | present |
| `Mo59MutationTester32.md` | `bf6c0ad3` (03:12:38) | `M` at `f091bd77`, 3+/2− | **present, pre-edit bytes** (edit written 03:13:08.9, +6.9 s) | present |
| `Mo59Critic29.md` | `bf6c0ad3` (03:12:38) | — | **present** (written 03:11:48) | present |
| `Mo59Reviewer16.md` | `bf6c0ad3` (03:12:38) | — | **present** (written 03:11:11) | present |

Also: `swarm-registry.json` was added at **`bf6c0ad3`** (mtime 02:52:21), not at
`f091bd77`; `w1-results.json` was added at `f091bd77` (mtime 07:42:05.9).
`HEAD` adds nothing else to the dir (`swarm-registry.json` is the only non-`.md`).
Dispatch/settlement completeness: 64 names extracted from
`.ufo/waves/round-59/w1-dispatch.json`, and *every* filed `.md` basename is a
dispatched name (`filed-but-not-dispatched = []`), all 64 dispatched names filed
by `f091bd77`.

## 3. What each document claimed

1. **r59 lesson @ `bf6c0ad3`** — `git show bf6c0ad3:corpus/lessons/round-59.md`,
   line 77: *"Reports absent at filing: Mo59Critic29, Mo59Executor40,
   Mo59MutationTester31, Mo59MutationTester32, Mo59Reviewer16"* → a **5-name**
   absent set.
2. **r59 report @ `9e9973ed`** (fleet `.ufo/reports/round-59/mori.md`, lines 74-75):
   *"64 seats dispatched, 62 report files present at filing (missing:
   Mo59Executor40, Mo59MutationTester31, Mo59MutationTester32 — partial; missing
   reports are not labeled dead)."* → 62 present, **3-name** "missing" set.
3. **r59 report amendment @ `56a2beff`** (lines 75-79): *"all 64 report files
   present after WAVE-DONE"*, *"Late-arriving seats (Mo59Executor40,
   Mo59MutationTester31/32)"*; and (lines 37-38) *"`w1-results.json` + late
   reports + swarm-registry `f091bd77…`"*.
4. **r59 lesson @ `a86e5f83` / HEAD** (line 77-78): *"**All 64 reports landed
   after WAVE-DONE** (`w1-results.json` 64/64 members); the three late seats
   (Mo59Executor40, Mo59MutationTester31/32)"* — the two extra names are silently
   dropped, not corrected.
5. **r59 spot-check @ `ddfb12fb`** (`corpus/lessons/round-59-verifier-spotcheck.md`,
   line 8: watchdog `complete` 07:41:41; lines 18-20: uncommitted `M MT32` (03:13),
   untracked `Ex40` (03:17), `MT31` (03:13), `w1-results.json` (07:42); lines
   99-101: *"lesson's 'absent at filing' set adds {Critic29, Reviewer16} which are
   committed"*).
6. **r60 correction** — `evidence/r59-absent-set.md` (5 rows, all
   `late-committed`) + `corpus/lessons/round-60.md:44-60`.

## 4. Reconciled timeline

```
02:52:21  swarm-registry.json written           (committed later at bf6c0ad3)
03:00:51  7b86704d  data rev: .ufo/waves/round-59/w1/ DOES NOT EXIST
03:11:11  Reviewer16 content written
03:11:48  Critic29 content written
03:12:38  bf6c0ad3  INTEGRATION lands 62 .md (incl. Critic29, Reviewer16, MT32)
                    and publishes the lesson line "absent at filing: {5 names}"
03:12:53  08127c99  dispatched marker; w1 tree unchanged (62)
03:13:02  9e9973ed  REPORT FILED: "62 present; missing {Ex40, MT31, MT32 — partial}"
03:13:08  MT32 edit written                      (6.9 s AFTER filing)
03:13:49  MT31 content written                   (47 s after filing)
03:17:30  Executor40 content written             (4 m 28 s after filing)
07:41:41  watchdog `complete`
07:42:05  w1-results.json written
07:42:42  f091bd77  +Ex40 +MT31, MT32 updated → 64 .md (+ w1-results.json)
07:43:47  a86e5f83  lesson rewritten: "All 64 reports landed after WAVE-DONE;
                    the three late seats"
07:43:54  56a2beff  report amended: all 64 present; swarm-registry credited to f091bd77
07:48:31  ddfb12fb  r60 entering; spot-check (defect 3) committed
12:58:36  398d3225  r60 absent-set table lands (unchanged through HEAD)
```

**Verdict.** The frozen table is correct on every checkable cell: all five are
absent at `7b86704d` and present at `398d3225`/HEAD; Critic29 and Reviewer16
are in `bf6c0ad3`; MT32 is in `bf6c0ad3` and modified in `f091bd77`; Ex40 and
MT31 are in `f091bd77` with committer date 07:42:42. The r60 table's prose note
("the report's missing set was correct about which files were late, not about
the count") is accurate. The r59 *lesson* claim was false for two of its five
names, and the r59 *amended lesson* replaced it with a different over-claim.

## 5. Divergences (severity: low unless marked)

**D1 (medium) — lesson@`bf6c0ad3`:5-name absent set is false for 2/5.**
`git cat-file -e bf6c0ad3:.ufo/waves/round-59/w1/Mo59Critic29.md` → PRESENT;
same for `Mo59Reviewer16.md`. Both were written at 03:11:11 / 03:11:48, i.e.
before the 03:13:02 filing, and were published *by the same commit* that carries
the claim. The claim was already falsified by its own tree. (Corrected in
`round-60.md:50-54`; correction verified.)

**D2 (low) — report@`9e9973ed` count vs set.** "62 present" is exact; the 3-name
"missing" list contains one file that was present-but-pre-edit (MT32), so
62 + 3 = 65 > 64. The parenthetical "— partial" acknowledges this, so the set is
right and only the word "missing" conflates *absent* with *stale*. Ground truth
at filing: 2 absent (Ex40, MT31) + 1 partial (MT32) + 2 present-and-final
(Critic29, Reviewer16).

**D3 (medium) — lesson@`a86e5f83`: "All 64 reports landed after WAVE-DONE" is false.**
62 of the 64 landed at `bf6c0ad3` (03:12:38), i.e. before WAVE-DONE (07:41:41).
Only Ex40 + MT31 (added) and MT32 (edited) satisfy "after WAVE-DONE". The same
commit silently deletes the two wrongly-named seats from the absent list
instead of superseding them explicitly — the mutation that made the r60
reconciliation harder.

**D4 (low) — report amendment credits `swarm-registry.json` to `f091bd77`.**
`git log --diff-filter=A -- .ufo/waves/round-59/w1/swarm-registry.json` → `bf6c0ad3`
(03:12:38); its mtime is 02:52:21. Attribution off by one commit; `w1-results.json`
and the three seat files are correctly attributed.

**D5 (low, precision) — r60 lesson anchors "filed" at 07:41.**
`corpus/lessons/round-60.md:75-76` says the late files landed "after the r59
report was filed (07:41)". 07:41:41 is the watchdog `complete` line
(spot-check line 8), not a filing event; the report commit is **03:13:02** and
the amendment **07:43:54**. The conclusion holds under either anchor, but the
anchor should be a commit timestamp — 07:41 is not one.

**D6 (medium, calibration) — the ABSENT-SET ARM is non-discriminating at the frozen rev.**
At `7b86704d` the whole `w1/` directory is absent, so
`truth_data = exists(repo, R59_DATA, …)` (`count-c1.py:194,222`) is False for
**every** seat name, and `want_disp` (`:202`) forces `late-committed` for all
five. Consequence: the arm cannot distinguish the report's 3-name set from the
lesson's 5-name set, cannot detect the D1 error, and — because the at-data cell
is forced to `absent` and the disposition to `late-committed` for **all 64**
seat names — would pass for any five of the round-59 seat names that are present
at R. Conformance to the
frozen predicate is exact (§1/§2); discriminating power against routed defect 3
is nil. The reconciliation's real content lives in the landing-pointer cells and
the lesson text, which the counter only greps (D7).

**D7 (medium) — the lesson requirement is document-scoped, not per-name.**
`count-c1.py:228`: `if not (name in lt and R59_LANDING[:8] in lt)` — `lt` is the
whole file. `Mo59Critic29` (line 50) and `Mo59Reviewer16` (line 53) carry **no**
landing pointer to `f091bd77` in their own bullets (false on the line, verified);
they pass only because `f091bd77` appears in the Ex40/MT31 bullets at lines 58-59.
Contract prose (`contract.md:56-57`) says "naming every … name with landing
pointer"; the implementation tests co-occurrence. Contrast C2's H4 per-copy row
binding — C1's absent-set arm has no equivalent binding, so a lesson that names a
late seat with a *wrong* pointer still passes.

**D8 (informational) — timestamp discipline.** See §1: `%ai` on `f091bd77`
(03:12:53) precedes the 03:13:02 filing and would invert the verdict. Any seat
re-deriving this arm must use `%ci`; the frozen table already does.

No divergence found in: the table's 5 rows vs `git cat-file -e` at both
references; the table bytes from `398d3225` to HEAD (unchanged); the "present at
r60 tip" cells at `398d3225` and HEAD; the frozen `NAMES` list, which is exactly
the union of the report's 3 and the lesson's 5 (both claims are fully covered).

## 6. Confidence

- Commit-level timeline and presence matrix: **high** — derived from git object
  bytes at named revisions, re-checkable with the commands quoted above.
- Content-write times: **medium** — filesystem mtimes of a working copy that was
  never re-checked-out (they match the spot-check's independently observed
  03:11/03:13/03:17 values), used only as corroboration of *ordering*, never as
  primary evidence.
- Author dates as authoring evidence: **rejected** (§1).
- The claim that the r59 lesson author *believed* the set at authoring time:
  not reconstructible; only the published bytes are scored. Marked as
  [INFERENCE] nowhere in the verdicts above.

## 7. Not run / handoff

- No counter was executed (`count-c1/c2/c3 --selftest|measure`), no fixture repo
  created, no `git` write anywhere; all git invocations were read-only against
  the lane. Scratch left empty.
- Main should run, once, after the wave: `python3 .ufo/waves/round-60/count-c1.py HEAD --scratch <dir>`
  to confirm `absent-set=5/5` under the frozen predicate, and treat D6/D7 as
  calibration findings (they do not flip the cell; they bound what the cell
  proves). D1-D5 are record corrections only; D4/D5 are the two lines I would
  re-word if the L1 wants the record exact.
