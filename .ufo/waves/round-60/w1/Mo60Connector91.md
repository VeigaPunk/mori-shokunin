# Mo60Connector91 — cross-claim pattern scan (read-only)

Scope: the three frozen r60 counters + their frozen targets in `contract.md`, plus the
r59 counters they re-run and the evidence receipts the claims consume. Findings below
are cross-claim pattern defects (token drift, pin disagreement, path spelling) with
reproduction. No production/lane/repo writes; every re-derivation is revision-pinned.

## Pins used for this scan

| reference | value | check |
|---|---|---|
| lane tip at read | `b3c256138f00c704d5aa56eb0332d74506502ef2` | `git rev-parse HEAD` |
| amended freeze | `ac496c7cde8cad965079858accae3bedfe4a73f2` | ancestor of HEAD (verified) |
| entering | `ddfb12fb0838b4307c445194a844f0c4b1950195` | ancestor of freeze (verified) |
| r59 data | `7b86704d7c0754a09958d131b64dbfa2a6d3eaed` | constant identical in contract:48, count-c1.py:55, count-c3.py:59 |
| count-c1/c2/c3 @ freezE=@HEAD=worktree | `795c1f31…ddbae` / `8c4814f5…df976` / `fabde06c…5153514` | `git show <rev>:path \| sha256sum` |
| entry tool / scan tool @ freeze=@HEAD | `cffe9f33…e6e69` / `4c04bf21…ac9a9` | matches `PIN_EC` / `PIN_SCAN` |

Nothing named in the contract disagrees with those values. The lane tip moved during the
wave (`ddfb12f`→`4d036fb0`→`772b2b4b`→`ac496c7c`→`76904b21`→`398d3225`→`b3c25613`) and a
sibling had `corpus/lessons/round-60.md` dirty in the worktree while I read; all lesson
reads below are `git show HEAD:…`, never the working tree.

## C1 — calibration: contract↔counter drifts

**C1-a (medium, contradiction).** Contract requires the lesson to name *every*
late-committed name with landing pointer `f091bd77` (contract:57-58). The counter checks
the file, not the name: `if not (name in lt and R59_LANDING[:8] in lt)` (count-c1.py:227-229).
At `b3c2561` the lesson names `f091bd77` in only 3 of the 5 required bullets:

```
50:- Mo59Critic29 — supersedes the round-59 lesson claim of absent-at-filing:
    … committed pre-filing in `bf6c0ad3` …            (no f091bd77)
53:- Mo59Reviewer16 — … committed pre-filing in `bf6c0ad3`.   (no f091bd77)
55:- Mo59MutationTester32 — … modified post-filing in `f091bd77`   (yes)
58:- Mo59Executor40 — … landed post-filing in `f091bd77`          (yes)
59:- Mo59MutationTester31 — … in `f091bd77`                        (yes)
```

This is not merely a coarse check: the frozen rule is self-contradictory. The absent-set
disposition rule anchors on the data revision (`absent at 7b86704d ⇒ late-committed`),
so all five rows are `late-committed`; but `git log --diff-filter=A` shows Critic29 /
Reviewer16 / MutationTester32 were added in `bf6c0ad3`, whose truthful landing pointer is
`bf6c0ad3` (the receipt's own cell 5 says so: `r59-absent-set.md` rows 4-5). The predicate
therefore demands `f091bd77` for names whose honest pointer is `bf6c0ad3`, and `C1=met`
is reached only because the counter's file-level check papers over the conflict. The
receipt even states the conflict in prose ("Disposition grammar note…").

**C1-b (low, exploitable drift).** Contract: "every corrected line names the real
committed pointer it supersedes the dead name with" (contract:52-54). Counter checks
*existence* of one such line per name (`corrected_lines_name_real`, count-c1.py:88-98).
Falsified with the frozen functions:

```
$ python3 -c 'import count_c1; print(count_c1.corrected_lines_name_real(two_good_lines_plus_one_marker_line_without_pointer))'
True   dead_uncorrected=0
```

A `r60-correction:` line can therefore cite a dead name and no replacement and still
pass `dead-uncorrected=0`.

**C1-c (low).** `parse_absent_table` validates cells 1-3 only (count-c1.py:100-118).
Cell 5 (landing pointer) may be empty — `| Mo59Critic29 | absent | present |
late-committed | |` parses to a valid row — and rows with ≠5 cells are silently dropped
rather than flagged; duplicate rows are last-wins (`rows[cells[0]] = …`). The claim's
"one 5-cell row per frozen name" is satisfied by a row whose evidence cell is blank.

**C1-d (medium, environment pin).** The receipts arm's "fresh re-run" executes
repo-supplied r59 bytes whose `main()` hardcodes absolute host paths —
`.ufo/waves/round-59/count-c1.py:246-247`:
`repo = "/home/vgpnk/Projects/shokunin/mori-shokunin"`, `fleet = "/home/vgpnk/Projects/shokunin"`.
`count-c1.py:131-133` passes `--repo` but never `--fleet`, so the receipt's byte-equality
depends on the host filesystem layout and on a second git repo (fleet) that the C1
predicate never names. Reproduction (same r59 bytes at `R59_DATA`, lane repo pinned):

```
default            rc=0  byte_equal_receipt=True  C1=met  selftest=ok fixtures=ok real=ok pointers=ok
--fleet <bogus>    rc=1  byte_equal_receipt=False C1=unmet … real=bad pointers=bad failed=manifest,real,pointers
```

So the arm is currently met, but portability is accidental. Related: the contract's
"no r60 instrument carries an absolute host path" (contract:142) is true for the six r60
files (grep found none) yet the executed r59 bytes carry two, and the C3 kill rule's
"count-c1 executes no repo-supplied tool blob (its re-runs are revision-pinned)"
(contract:123-124) is imprecise: c1 executes two repo-supplied *counter* blobs pinned by
revision, which in turn execute repo *tool* blobs with pin-as-bookkeeping — r59
count-c1.py:105,110 and r59 count-c2.py:205,209 run the tool `if tool_b is not None`,
not `if tool_ok`. Integrity holds only because `R59_DATA` is immutable.

**C1-e (low, symmetry).** C2 and C3 have committed after-state receipts
(`c2-at-freeze.txt`, `c3-at-freeze.txt`), C1 does not: at `b3c2561`,
`evidence/c1-at-data.txt` is untracked (`git ls-files --error-unmatch` → "Did you forget
to 'git add'?") and no committed file under `.ufo/` contains
`C1=met dead-uncorrected=0` (only the target text in contract/spec). The predicate does
not require it, but the round therefore reproduces routed defect 4's shape for its own
C1 after-state unless the wave commits that receipt.

## C2 — depth: contract↔counter drifts

**C2-a (medium, vacuous universal + dead gate).**
`count-c2.py:209`: `if not (ec_ok is not None and scan_ok_sha) or not rfiles:` —
`ec_ok` is a bool, so `ec_ok is not None` is always true; the intended entry-tool gate is
a no-op (observable: `control-c2-do-nothing.txt` reports `scan=ok` alongside
`failed=…,tool_absent,…` at `ddfb12f`). No predicate impact (the contract gates the scan
arm on `PIN_SCAN` only), but the selftest has no case for it.
`count-c2.py:220-224`: `all(f.get("members") == f.get("seats") for f in out.get("files", []))`
is vacuously true for `files: []`, and the arm never asserts the five-file cardinality the
contract states ("over the five REAL_SCAN files", contract docstring line 18). Both
demonstrated: `all([]) → True`.

**C2-b (low, token aliasing).** `count-c3.py:174`: `gated = "tool_sha" in out and
"tool_absent" not in out`. `count-c2` emits both `tool_sha` (entry tool) and
`scan_tool_sha` (scan tool), so the substring matches the scan tool's reason. PoC in
scratch (entry tool = real pinned bytes, scan tool = unpinned marker-writing blob,
`d677610e`):

```
C2=unmet … failed=…,scan,scan_absent:…,scan_tool_sha,…
tool_sha in out -> True | tool_absent in out -> False | gated -> True
scan_tool_sha present -> True
```

The arm cannot distinguish which gate fired; the frozen PoC masks this only because it
puts the evil blob at both tool paths. Compounding it, the marker scan is scoped to
`s_new` (`count-c3.py:173,181`) while the executed counter inherits the caller's CWD
(`run_counter`, count-c3.py:122-128, no `cwd=`), and `count-c2:212` runs the scan tool
without `--scratch` — a blob executed there writes to CWD, outside the scanned root.

**C2-c (low, duplicate frozen table).** The expect table exists twice: `FROZEN_EXPECTS`
(count-c2.py:98-112) and `.ufo/waves/round-60/trees-c2h-expects.json`. They are equal
today, and all 13 committed `expect.txt` equal both (machine-compared). But the json has
no consumer in the claim path and is not pinned by anything; only a builder rerun would
surface a drift.

**C2-d (low, hidden cross-arm state).** The hostile-tree arm consumes
`scratch/"artifacts.json"` (count-c2.py:385-386) which is created only by the entry arm
(count-c2.py:308-313). If the entry arm short-circuits, all 13 tree verdicts are computed
against a missing path; fail-safe today (trees would be `bad`), but the tree arm's
meaning silently depends on an earlier arm's side effect.

## C3 — operability: tokens not bound to their predicates

**C3-a (high, clearest drift).** The frozen target line
`C3=met toolgate=ok containment=ok expectgate=ok cases=6` is computed from `failed`
membership for strings that are never appended:

```
$ grep -n "failed.append" count-c3.py   # lines 143-253
  count_c2_absent, count_c2_sha, count_c1_absent, count_c1_sha, r59_counter_absent,
  poc:…, g1_new_no_tool_sha, g1_new_executed:…, g1_new_skipped,
  g1_old_control_did_not_reproduce, g1_old_skipped,
  g2_parent_escape, g2_inside_rejected, g2_symlink_escape, g2_escape_written, g2_skipped,
  poc2:…, g3_no_tamper_flag, g3_skipped
```

None of `toolgate` / `containment` / `expectgate` appears in that set, so the token
expression (count-c3.py:300-305) yields `ok` for every real failure mode except its
`*_skipped` sibling. Evaluated against the frozen expression:

```
['g1_new_no_tool_sha']            -> toolgate=ok containment=ok expectgate=ok  (C3=unmet)
['g1_new_executed:x/EXEC-MARKER'] -> toolgate=ok containment=ok expectgate=ok  (C3=unmet)
['g2_parent_escape','g2_escape_written'] -> toolgate=ok containment=ok expectgate=ok
['g3_no_tamper_flag']             -> toolgate=ok containment=ok expectgate=ok
['g1_old_control_did_not_reproduce'] -> toolgate=ok containment=ok expectgate=ok
```

Consequence: `C3=unmet toolgate=ok containment=ok expectgate=ok cases=6` is printable, and
the three tokens collapse to one bit ("did `c2_ok` hold"). C1 and C2 bind their tokens to
state (`detail[...]`, direct counts); C3 does not — the shared pattern is broken in
exactly one instrument.

**C3-b (observation).** `met` requires `old_hole` (count-c3.py:255), i.e. C3 can only be
met while the r59 counter remains exploitable. That is the contract's design, but it makes
the claim non-monotone: improving the old instrument would flip C3 to unmet.

## Cross-claim checks that hold (no drift)

- Receipt/pointer spellings agree between contract and counters for all six paths
  (`r59-c1-met.txt`, `r59-c2-met.txt`, `r59-absent-set.md`, `corpus/lessons/round-60.md`,
  both `round-59/evidence/control-c{1,2}-do-nothing.txt`); both round-59 controls exist
  at the entering revision.
- Selftest labels reproduce the contract exactly: `C1_SELFTEST pass=6 fail=0`,
  `C2_SELFTEST pass=8 fail=0`, `C3_SELFTEST pass=3 fail=0` (exit 0).
- C1 target reproduces byte-exact at `b3c2561` and is identical to the uncommitted
  `c1-at-data.txt`; `receipts=2/2` proves both r59 receipts byte-equal fresh re-runs at
  `R59_DATA` (with the default fleet path — see C1-d).
- Absent-set cells 1-3 match `git cat-file -e` truth for all five names (absent at
  `7b86704d`, present at `ddfb12f`/`b3c2561`). Cell-5 timestamps are *committer* dates
  (`f091bd77`=07:42:42, `bf6c0ad3`=03:12:38) and match `git log --format=%cd`; a check
  against author dates would falsely flag them.
- 13/13 committed `expect.txt` == counter `FROZEN_EXPECTS` == `trees-c2h-expects.json`.
- Revision pins agree: `R59_DATA` identical in contract and both counters; freeze and
  entering are ancestors of tip; counter/tool bytes identical at freeze, HEAD and worktree.

## Severity order for follow-up

1. C3-a (target line not bound to its predicates) — a closure could print all-`ok`
   sub-tokens with the claim unmet.
2. C1-a (frozen rule contradicts the truthful record; `met` depends on a coarse check).
3. C1-d (receipt reproducibility tied to an unnamed fleet repo and an absolute host path
   inside the executed bytes).
4. C2-a / C2-b (vacuous universal, dead gate, `tool_sha` aliasing, marker scope outside
   `s_new` and CWD).
5. C1-b / C1-c / C2-c / C2-d (coarse or unvalidated cells; duplicate table; cross-arm
   state).

Scratch: `/fast/scratch/hyaku/mori-r60/Mo60Connector91` (probe scripts, PoC repo
`d677610e`, scratch counter copies) — removed before yielding. Lane untouched: no
commits, no VCS mutation, no writes outside the report; the only lane-side change on
disk is this file plus the sibling-modified lesson.
