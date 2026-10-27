# Mo56ScribeScorecard — round-56 SCORECARD section draft (w1 scribe)

Scope: draft the `SCORECARD.md` round-56 section in the round-55 shape, with the
Before cells taken from the do-nothing lines in `evidence/controls.txt` at
`5b295eee` and the After cells from `evidence/c1-at-freeze.txt` /
`evidence/c2-at-freeze.txt` (landed `8be2717b`, stamped `3f494b49`), plus the
`Planned (round 57)` line. Read-only over the lane repo; no product, counter,
contract or SCORECARD file was modified. The section text is fenced here for the
L1 to integrate.

## What was checked before drafting (observed)

All commands run from `/home/vgpnk/Projects/shokunin/mori-shokunin` with
`TMPDIR=/fast/scratch/hyaku/mori-r56/Mo56ScribeScorecard/tmp`; scratch removed
after each batch.

| # | Command | Output | rc |
|---|---|---|---|
| 1 | `python3 .ufo/waves/round-56/count-c1.py 3f494b49cde612d929e82887a48e1660c022c359` | `C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=3f494b49cde612d929e82887a48e1660c022c359` | 0 |
| 2 | `python3 .ufo/waves/round-56/count-c1.py 8be2717b0809281d07dffe83dad424a4859e0747` | same tokens, `rev=8be2717b…` | 0 |
| 3 | `python3 .ufo/waves/round-56/count-c2.py 3f494b49…` | `C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=3f494b49…` | 0 |
| 4 | `python3 .ufo/waves/round-56/count-c2.py 8be2717b…` | same tokens, `rev=8be2717b…` | 0 |
| 5 | `python3 .ufo/waves/round-56/count-c1.py 5b295eee…` | `C1=unmet selftest=bad fixtures=bad entry=bad row=bad norem=bad failed=tool_absent rev=5b295eeebd87ebd610d8d39bfe2035742f740cfa` | 1 |
| 6 | `python3 .ufo/waves/round-56/count-c2.py 5b295eee…` | `C2=unmet selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=5b295eee… failed=tool_absent` | 1 |
| 7 | `python3 .ufo/waves/round-56/controls/controls.py 5b295eee…` | two `PASS` do-nothing lines + 8 `KILLED` mutation arms (identical to `evidence/controls.txt`) | 0 |
| 8 | `python3 tools/mori-driver-liveness.py --selftest` | `DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0` | 0 |
| 9 | `python3 tools/mori-vote-bind.py --selftest` | `VOTE_BIND_SELFTEST pass=16 fail=0` | 0 |
| 10 | `python3 tools/mori-vote-bind.py tally --ledger corpus/knowledge/kernel-v7.3-recheck-r55.md --results .ufo/waves/round-55/w1-results.json --verb RECHECK --voter Mo55Rc01 … Mo55Rc16` | `TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15` | 0 |
| 11 | `git show <rev>:tools/mori-driver-liveness.py \| sha256sum` at `6ced9da9`, `8be2717b`, `acc62f54` | `6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997` (equals C1 `PIN`); at `c419fe6d` = `5befd490…` (pre-correction) | 0 |
| 12 | `git show <rev>:tools/mori-vote-bind.py \| sha256sum` at `c419fe6d`, `8be2717b`, `acc62f54` | `8be1acdbb36cd68deba005e21a4a8679534ab5a5099a787aa9335d288dfa6bca` (equals C2 `PIN`) | 0 |
| 13 | `git ls-tree -r --name-only 8be2717b .ufo/waves/round-56/fixtures/driver` | 12 files: 9 `watchdog.log` (one per fixture dir) + 3 `state-shapes/state/*` | 0 |
| 14 | `git show 8be2717b:corpus/SOURCES.md` row grep | S544 and S545 rows exist, each carrying `corpus/knowledge/driver-liveness-r56.md` / `corpus/knowledge/vote-binding-r56.md` in used-by | 0 |
| 15 | `git show 5b295eee:corpus/SOURCES.md \| grep -cE '^\s*\| S[0-9]+ \|'` → 316; same at `8be2717b` → 318; added rows `+| S544`, `+| S545` | 316 → 318 | 0 |
| 16 | `grep -c $'\tW04\t' evidence/census-start.txt` | 23 W04 lines, last lines `… ok <path>` and `exit=0` | 0 |

Notes carried into the draft:

* `evidence/c1-at-freeze.txt`, `c2-at-freeze.txt` and `controls.txt` do **not**
  exist at `3f494b49` (`git show 3f494b49:<path>` → `exists on disk, but not in
  '3f494b49'`); they first land at `8be2717b` and stamp the measured rev
  `3f494b49`, which is what the contract says receipts do (“receipts here stamp
  the measured revision themselves”). The After cells therefore cite the stamped
  rev and name the landing commit.
* Both counters reproduce their receipt lines at **both** `3f494b49` and
  `8be2717b`, so the claim does not depend on the controls commit for its data
  arms; the `rev=` token follows R as designed.
* The 110-char truncation in `controls.py` (`verdict[:110]`, line 92) is why
  `evidence/controls.txt` shows short revs: do-nothing-c1 ends
  `rev=5b295eeebd87ebd610d8d39b` (24 hex) and do-nothing-c2 ends
  `rev=5b295eeebd87ebd610d8d39bfe2035742` (33 hex). Both are unique prefixes of
  `5b295eeebd87ebd610d8d39bfe2035742f740cfa` (row 5/6 re-runs above).

## Draft SCORECARD.md round-56 section (fenced, for L1 integration)

```markdown
## Round 56 — C1 coverage (FR5 driver-liveness probe) and C2 operability (dual-shape vote binder)

Measured at `<AT-LANDED-R>` (w1 settlement integration). Entering `5b295eee`; freeze `3f494b49`; controls and at-freeze receipts `8be2717b`; data `c419fe6d` + `6ced9da9`; dispatch `acc62f54`. Scores entering: coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6. C1 coverage (the lowest owned axis) and C2 operability work owned axes; no scalar score delta.

| Claim | Axis | Counting command | Before | After |
|---|---|---|---|---|
| C1: the FR5 driver-liveness probe is landed with frozen sha, 13-case selftest, 9 frozen fixtures at their frozen malformed counts, the S544-sourced entry naming it, and no health-verdict string ahead of its selftest block | coverage 6 | `python3 .ufo/waves/round-56/count-c1.py R` | `C1=unmet selftest=bad fixtures=bad entry=bad row=bad norem=bad failed=tool_absent rev=5b295eee…`, rc 1 — `evidence/controls.txt` (do-nothing-c1) at `5b295eee` | `C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=3f494b49cde612d929e82887a48e1660c022c359`, rc 0 — `evidence/c1-at-freeze.txt` (stamped `3f494b49`, landed `8be2717b`); at-landed `AT-LANDED-C1`, rc `AT-LANDED-RC` — `evidence/c1-at-landed.txt` at `<AT-LANDED-R>` |
| C2: the dual-shape seat-output vote binder is landed with frozen sha, 16-case selftest, and re-binds the round-55 RECHECK tally over committed bytes to the frozen line while the frozen r55 counter reads voted=0 on the same bytes | operability 7 | `python3 .ufo/waves/round-56/count-c2.py R` | `C2=unmet selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok failed=tool_absent rev=5b295eee…`, rc 1 — `evidence/controls.txt` (do-nothing-c2) at `5b295eee` | `C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=3f494b49cde612d929e82887a48e1660c022c359`, rc 0 — `evidence/c2-at-freeze.txt` (stamped `3f494b49`, landed `8be2717b`); at-landed `AT-LANDED-C2`, rc `AT-LANDED-RC` — `evidence/c2-at-landed.txt` at `<AT-LANDED-R>` |

Limits (at freeze, observed): both counters reproduce their receipt lines at `3f494b49` and at `8be2717b` (rc 0 both), and the C2 tally line re-runs from the worktree tool over the committed round-55 ledger and results (`TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15`, rc 0). C1's 9 fixture expectations are one `malformed=5` and eight `malformed=0`; the fixtures are 9 `watchdog.log` files plus a `state-shapes/state/` tree. The `norem` arm reads only the tool text before its `# selftest` marker (`count-c1.py:162`), and the tool does carry the literals `healthy`, `unhealthy`, `failed lane` at `tools/mori-driver-liveness.py:422` inside the case `t_no_health_verdict`; the whole-file reading of P-C1 is therefore false while the implemented arm is green — a wording limit, routed below, not a data defect. C2's do-nothing line prints `selftest=ok tally=ok control=ok entry=ok row=ok` at a tip where the tool is absent (`count-c2.py:69` short-circuits to `["tool_absent"]`, and no printed token maps that name), so the Before cell discriminates only through `failed=tool_absent` and rc 1; C1's do-nothing branch prints all arms `bad` (`count-c1.py:189`). Both do-nothing revs are truncated by the control harness to 110 chars (`controls.py:92`), so the receipt carries 24- and 33-hex prefixes of `5b295eeebd87ebd610d8d39bfe2035742f740cfa`; the full rev is what the re-run prints. The census receipt `evidence/census-start.txt` records 23 W04 lines, `ok <path>` and `exit=0`, but no row-count token; 316 is re-derived by counting `| S<nnn> |` rows at `5b295eee` (318 at `8be2717b`, +S544 +S545).

Wave: one v2 `w1`, 64 seats (contract: build and falsification, attack seats ≥16 / ≥25%) — settlement `AT-LANDED`. Census: start receipt exit 0, 23 W04, 316 rows at `5b295eee`; end census `AT-LANDED`. C2 leaves 10 single-voted rows in the round-55 tally; the binder now reports them as `single=10` instead of zeroing the arm.

Planned (round 57): the dispatch-coverage validator (≥2 settled voters per scoped row, closing the `single=10` rows the binder now surfaces honestly); the four other release-triggered artefacts outside C1's claim-table scope; the S508/S520 append-only superseding anchors; durable control-tree witnesses; C2 re-wording of the round-55 8 dissenting rows with re-vote under the ruled binding; full 40-char revs in control receipts (`controls.py:92` truncates to 110 chars); the C2 do-nothing token shape (`count-c2.py:69`, arms print `ok` when no arm ran) and the C1 predicate wording `no health-verdict string ahead of its selftest block` (`count-c1.py:162`, `tools/mori-driver-liveness.py:422`).
```

## Touched surfaces

* Wrote only `.ufo/waves/round-56/w1/Mo56ScribeScorecard.md` (this file).
* Read (git read-only): `SCORECARD.md` (working-tree diff and round-55 section),
  `.ufo/waves/round-56/{contract.md, count-c1.py, count-c2.py, controls/controls.py,
  evidence/*, fixtures/driver}`, `corpus/SOURCES.md`, `corpus/knowledge/driver-liveness-r56.md`,
  `corpus/knowledge/vote-binding-r56.md`, `tools/*`, `git log`/`show`/`ls-tree`.
* Scratch `/fast/scratch/hyaku/mori-r56/Mo56ScribeScorecard/` created and removed
  in each batch. No clone, no fixture repo, no commit, no jj command.
* No installs. No `/proc`, `/sys` or journal reads were needed. No network access.

## Out of scope (not done here, by seat rule)

* Did not edit `SCORECARD.md`, `LOG.md`, `SHONEN.md`, the contract, counters,
  controls, tools, corpus or the lesson; the working-tree round-56 section
  visible at draft time is the L1's, not mine.
* Did not settle the wave, score the axes, or fill `AT-LANDED*` placeholders.
* No vote lines are carried by this report (w1 has no vote items).

## Findings

1. **MED — P-C1's norem sentence is false for the whole tool file, true only for
   the pre-selftest region.** `count-c1.py:162` scans
   `tool_src.split("# selftest", 1)[0]`, while
   `tools/mori-driver-liveness.py:422` (at `6ced9da9`) contains the literals
   `"healthy"`, `"failed lane"`, `"unhealthy"` inside `t_no_health_verdict`.
   Receipt `norem=ok` is honest for the implemented arm; the claim wording and
   the contract sentence (contract.md C1 target) are broader than the arm. The
   drafted row says “ahead of its selftest block” to match. Counters are frozen:
   routed to round 57, not fixed here.
2. **MED — C2's do-nothing output prints five arms `ok` when none ran.**
   `count-c2.py:69` returns `["tool_absent"]`; the print map at
   `count-c2.py:156-166` marks `bad` only for named failures, so
   `evidence/controls.txt:2` reads `selftest=ok tally=ok control=ok entry=ok
   row=ok … failed=tool_absent` at `5b295eee`, where the tool does not exist.
   The Before cell therefore looks token-identical to the After cell on five
   arms; only `failed=` and rc 1 separate them. C1's branch (`count-c1.py:189`)
   prints all arms `bad`, so the two Before cells are asymmetric. Routed.
3. **LOW — control receipts carry truncated revisions.**
   `controls/controls.py:92` stores `verdict[:110]`, so `evidence/controls.txt:1`
   ends at a 24-hex prefix and line 2 at a 33-hex prefix of
   `5b295eeebd87ebd610d8d39bfe2035742f740cfa`; round-55 routed defect 2 asks a
   before→after row to cite the receipt's stamped revision, and the stamp here is
   only a prefix. Both prefixes are unique and the full value re-runs (rows 5/6
   above); the SCORECARD Before cells elide the rev and cite the receipt path.
4. **LOW — census receipt carries no row-count token.** `evidence/census-start.txt`
   (exit 0) has 23 W04 lines, a final `ok <path>` line and `exit=0`; the
   contract's “316 rows” is re-derived (316 at `5b295eee`, 318 at `8be2717b`).
   Round-55 routed defect 1 asked for captured bytes *or* the counting command;
   the counting command is stated in the draft's census sentence but not in the
   receipt itself.
5. **LOW — at-freeze receipts post-date the rev they stamp.**
   `evidence/c1-at-freeze.txt`/`c2-at-freeze.txt`/`controls.txt` do not exist at
   `3f494b49`; they land at `8be2717b` while stamping `rev=3f494b49`. This is
   contract-consistent (“receipts here stamp the measured revision themselves”)
   and both counters reproduce at both revs, but the SCORECARD After cell must
   cite the stamped rev (`3f494b49`) and the landing commit (`8be2717b`)
   separately, or a reader will look for the files at the wrong commit.
6. **INFO — C2 tally line re-runs from the worktree, not only the counter.**
   Direct invocation over the committed round-55 ledger and results prints the
   frozen line with rc 0 (row 10), so `contrast=voted0` is the whole difference
   between the two binding shapes on identical bytes.
