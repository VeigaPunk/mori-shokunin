# RevScorecardClaims — kill-rule control coverage (C1 survivors, C2 DAGs)

Seat: read-only reviewer. Scope: the claimed kill rules —

- **C1**: "a do-nothing control cannot print `CONFORM=met`" — is the
  r39-checker-on-survivors control committed for **every** survivor?
- **C2**: "a do-nothing control cannot print the fixture verdicts" — is the
  v2-on-DAGs control committed for **n/p/r**?

Ground truth: the committed tree (instruments at `265a955cc`, evidence at
`8d3badd`, both on `origin/master`), plus first-hand replays written only under
`.scratch/rev-scorecard-claims/`. No production file, lane index, jj state, or
fleet path was touched.

## Bottom line

- **C1 coverage is complete.** All 10 generated survivor fixtures — the nine
  named in C1 plus the tenth `survivor-barecomm` multi-counter control — have a
  committed red receipt (v2 bytes on the survivor) and a committed after
  receipt (v3 bytes, `CONFORM=unmet`). All 10 survivor/multi-counter red
  controls, the 3 DAG red controls, and the conjunct red control are
  tracked on `origin/master` at `8d3badd`; none is untracked. The survivor/DAG
  red controls are clean in the working tree; the conjunct red is one of the
  three drifted files noted in F8.
- **The C1 control is not a `met` control for `divzero`.** 8 of the 9 named
  survivors print `CONFORM=met` exit 0; `c10-red-divzero.txt` prints
  `conformance setup error: division by zero` / `EXIT=2`. The contract's
  "print `CONFORM=met` exit 0 on nine survivor fixtures" (contract.md:78) and
  the claim-admission hygiene sentence "it prints `met` where v3 must print
  `unmet`" are false for 1 of 9. The fixture still discriminates (exit 2 vs
  `CONFORM=unmet` exit 1), but it is a crash control, not a survivor.
- **C2 coverage is complete.** The three committed red receipts name the
  extracted v2 gate whose sha256 equals `git show bb1f2457:tools/…`; my replay
  reproduces every verdict line. The v2-on-DAGs control does **not** reproduce
  the v3 timing verdicts on any of n/p/r, though individual printed lines
  overlap (`changed S001` on dag-p, `round_changed=[S008]` on dag-r).
- **Two C2 Before phrases overstate what the receipts show.** The dag-p
  "fabricates a `changed` line" is not in the receipt (the one `changed S001`
  line is the legitimate side-branch edit and is present in v3 too); the dag-r
  "prints a `changed` event" is not a printed line in either version. The real
  discriminators are the `supersede_timing` fields (`superseded_as_of`,
  `stale_supersede`) and, for dag-r, `superseded`. The kill rules still have
  teeth through the gate selftest's hand-written expected dicts.
- **One number attached to the C2 kill rule is wrong three ways:** the contract
  says "the declared 19 ids", the wave context says 34, and the committed
  receipt has **35** `superseded_as_of` ids (v2 before: 18). The discriminator
  (S226 present under v3, absent under the edit-bounded set) is intact.
- **No control is missing.** The gaps are claim wording / observability and one
  commit-ordering gap (the v3 conjunct-gutted fixture exists at `ede486b`, not
  at `265a955cc`).

## Committedness of the controls

Run from the lane root:

```text
$ git log --oneline origin/master -4
ede486b round-40: repair S229 registry placement (E12: row inside ## Registry) + commit referenced gutted-conjunct fixture
8d3badd round-40: evidence receipts, wave spec (66-seat v2, validated), SCORECARD/LOG/lesson
265a955 round-40: instruments — conform v3 (P-C10), gate v3 (P-C11), S229, r39 erratum
bb1f245 round-39 verifier spot-check (integrator, hyaku): non-author admit/reject

$ git merge-base --is-ancestor 8d3badd origin/master && echo on-origin
on-origin

$ for f in .ufo/waves/round-40/evidence/c10-red-{cond,decoy,divzero,inf,second-popen,shadow-neg,shadow-none,tuple,underscore,multicounter}.txt \
           .ufo/waves/round-40/evidence/c11-red-{neveredited,firstparent,readd}.txt; do
    git cat-file -e origin/master:$f && echo "on-origin $f"; done
on-origin … (all 13 lines)

$ git ls-tree -r --name-only 265a955cc -- .ufo/waves/round-40/fixtures/generated/
… survivor-barecomm.py … survivor-underscore.py, conform-r39-conjunct-gutted.py
# NOTE: conform-v3-conjunct-gutted.py is ABSENT here (see F7).

$ git cat-file -e 265a955cc:.ufo/waves/round-40/fixtures/generated/conform-v3-conjunct-gutted.py
fatal: path … exists on disk, but not in '265a955cc'
$ git log --oneline --all -- .ufo/waves/round-40/fixtures/generated/conform-v3-conjunct-gutted.py
ede486b round-40: repair S229 registry placement (…) + commit referenced gutted-conjunct fixture
```

The evidence directory itself does not exist at `265a955cc` (that is the
instruments-only tip); all receipts are first committed at `8d3badd`, which is
an ancestor of `origin/master`. The survivor red receipts were measured when
HEAD was `bb1f2457` (their `head_pin` lines say `pin=bb1f2457 … tip=bb1f2457`),
and the DAG red receipts name the v2 bytes in their command path; the after
receipts were measured when HEAD was `265a955cc`
(`pin=265a955cc … tip=265a955cc`).

### C1 matrix (every generated survivor)

| fixture | committed red control | red verdict | committed after | v3 FAIL checks |
|---|---|---|---|---|
| `shadow-none` | `c10-red-shadow-none.txt` | `CONFORM=met` exit 0 | `c10-after-shadow-none.txt` | `timeout_scope` |
| `shadow-neg` | `c10-red-shadow-neg.txt` | `CONFORM=met` exit 0 | `c10-after-shadow-neg.txt` | `timeout_scope` |
| `cond` | `c10-red-cond.txt` | `CONFORM=met` exit 0 | `c10-after-cond.txt` | `timeout_scope` |
| `inf` | `c10-red-inf.txt` | `CONFORM=met` exit 0 | `c10-after-inf.txt` | `timeout_scope` |
| `divzero` | `c10-red-divzero.txt` | **setup error exit 2** | `c10-after-divzero.txt` | `predicate`, `head_pin`, `tool_resolve`, `timeout_scope`, `timeout_state` |
| `decoy` | `c10-red-decoy.txt` | `CONFORM=met` exit 0 | `c10-after-decoy.txt` | `drain_bind` |
| `underscore` | `c10-red-underscore.txt` | `CONFORM=met` exit 0 | `c10-after-underscore.txt` | `drain_bind` |
| `second-popen` | `c10-red-second-popen.txt` | `CONFORM=met` exit 0 | `c10-after-second-popen.txt` | `drain_bind` |
| `tuple` | `c10-red-tuple.txt` | `CONFORM=met` exit 0 | `c10-after-tuple.txt` | `drain_bind` |
| `barecomm` (10th, multi-counter) | `c10-red-multicounter.txt` | `CONFORM=met` exit 0 | `c10-after-multicounter.txt` | `drain_bind`, `selftest_conjunct` |

Control instrument identity: the extracted v2 checker
`fixtures/extracted/conform-v2-r39.py` has
`sha256 fe0be179aba9df7150f0b6cdb50a5f9bbdb411efb1263b46ffa6b21d46ef7987`,
equal to `git show bb1f2457:.ufo/waves/round-39/conform.py | sha256sum` and the
freeze pin. The after checker `.ufo/waves/round-40/conform.py` has
`sha256 5025b966…` equal to `git show 265a955cc:.ufo/waves/round-40/conform.py`
and the freeze pin. The survivor fixture files are identical at `265a955cc`
and `HEAD` (`git diff --stat 265a955cc HEAD -- fixtures/generated/` reports only
the later-added v3 gutted copy).

### C2 matrix (n/p/r)

| DAG | committed red control (v2) | v2 verdict lines | committed after (v3) | v3 verdict lines |
|---|---|---|---|---|
| `dag-n` | `c11-red-neveredited.txt` | `superseded=[] round_changed=[]`; `as_of=[] stale=[]`; exit 0 | `c11-after-fixture-n.txt` | `superseded=[S001] round_changed=[]`; `as_of=[S001] stale=[]`; exit 0 |
| `dag-p` | `c11-red-firstparent.txt` | `changed S001`; `superseded=[S001] round_changed=[S001]`; `as_of=[] stale=[S001]`; exit 1 | `c11-after-fixture-p.txt` | `changed S001`; `superseded=[S001] round_changed=[S001]`; `as_of=[S001] stale=[]`; exit 1 |
| `dag-r` | `c11-red-readd.txt` | `superseded=[] round_changed=[S008]`; `as_of=[] stale=[]`; exit 1 | `c11-after-fixture-r.txt` | `superseded=[S008] round_changed=[S008]`; `as_of=[S008] stale=[]`; exit 1 |

Red instrument identity: `fixtures/extracted/gate-v2-bb1f2457.py` has
`sha256 62cd4132dbe141538371f79723c3caff66670fab9076494cd9cf65efccfc01e7`,
equal to `git show bb1f2457:tools/mori-sources-appendonly.py | sha256sum`.
After gate bytes: `tools/mori-sources-appendonly.py` has
`sha256 bde5a9a3…`, equal to `git show 265a955cc:tools/mori-sources-appendonly.py`
and the freeze pin.

## Commands run and observed output

Working directory `/home/vgpnk/Projects/shokunin/mori-shokunin` for all.

1. **Survivor replay** (same argv shape as the red/after receipts; output in
   `.scratch/rev-scorecard-claims/survivor-*.replay.txt`):

   ```sh
   for f in .ufo/waves/round-40/fixtures/generated/survivor-*.py; do
     python3 .ufo/waves/round-40/fixtures/extracted/conform-v2-r39.py bb1f2457 --counter "$f"
     python3 .ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --counter "$f"
   done
   ```

   Result: `CONFORM=met`/`EXIT=0` for shadow-none, shadow-neg, cond, inf, decoy,
   underscore, second-popen, tuple, barecomm; `conformance setup error:
   division by zero`/`EXIT=2` for divzero; `CONFORM=unmet`/`EXIT=1` for all ten
   on v3. Against the committed receipts, every replay was byte-identical
   except the `check head_pin` line (the check reads the repo HEAD, now
   `ede486b` rather than the receipt-time `bb1f2457`/`265a955cc`); the divzero
   *red* receipt has no check lines and matched exactly. This is a replay
   limitation, not a receipt defect.

2. **Multi-counter replay** (exact argv of the receipt, not the single-counter
   loop):

   ```sh
   python3 .ufo/waves/round-40/fixtures/extracted/conform-v2-r39.py bb1f2457 \
     --counter .ufo/waves/round-40/count-c8.py \
     --counter .ufo/waves/round-40/fixtures/generated/survivor-barecomm.py
   python3 .ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b \
     --counter .ufo/waves/round-40/count-c8.py \
     --counter .ufo/waves/round-40/fixtures/generated/survivor-barecomm.py
   ```

   Result: red `CONFORM=met` exit 0; after `CONFORM=unmet` exit 1 with
   `drain_bind FAIL` and `selftest_conjunct FAIL` for `survivor-barecomm.py`.
   Only the HEAD-derived `head_pin` line differs from the committed receipts.

3. **DAG replay** (output in `.scratch/rev-scorecard-claims/dags-{v2,v3}.txt`):

   ```sh
   python3 .ufo/waves/round-40/fixtures/run-c11-dags.py \
     .ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py "$PWD" \
     "$PWD/.scratch/rev-scorecard-claims/dags-v2.txt" dag-n dag-p dag-r
   python3 .ufo/waves/round-40/fixtures/run-c11-dags.py \
     tools/mori-sources-appendonly.py "$PWD" \
     "$PWD/.scratch/rev-scorecard-claims/dags-v3.txt" dag-n dag-p dag-r
   ```

   The verdict lines for all three DAGs matched the committed red and after
   receipts exactly (only the `command:` path argument differs).

4. **Selftests at the scored tip** (aggregate controls the kill rules lean on):

   ```sh
   $ python3 tools/mori-sources-appendonly.py --selftest
   MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0        # EXIT=0
   $ python3 .ufo/waves/round-40/conform.py 265a955cc… --selftest
   CONFORM_SELFTEST pass=11 fail=0                        # EXIT=0, 58.02 s wall
   ```

5. **Lane-line count** (receipt parse):

   ```sh
   python3 - <<'EOF'
   # regex parse of evidence/c11-{before-lane,after-lane,after-e37dcc6}.txt
   EOF
   as_of count = 35   # c11-after-lane, includes S226
   before as_of count = 18
   added = 17 (S226 + S067,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140)
   e37: as_of 33 + stale [S069] = 34
   ```

No LSP device is exposed in this runtime (`read xd://lsp` → "No such tool");
semantic coverage was done by executing both instrument versions and the
selftests, not by static text search.

## Findings

### F1 — MEDIUM (C1 control definition): `divzero` is not a `met` survivor; the "nine" count is off by one

Evidence: `c10-red-divzero.txt:3-4` —
`conformance setup error: division by zero` / `EXIT=2`; contract.md:78-80 lists
it inside "print `CONFORM=met` exit 0 on nine survivor fixtures" and then
parenthesises `(exit 2, no FAIL line)`. Claim-admission hygiene repeats the
false premise: "it prints `met` where v3 must print `unmet`".
Consequence: 8/9 survivors are met→unmet discriminators; `divzero` is an
exit-2→exit-1 discriminator. The control exists and is committed, so the
literal kill rule ("cannot print `CONFORM=met`") is vacuously true for it, but
the prose misclassifies it. The after receipt also shows four collateral FAILs
(`predicate`, `head_pin`, `tool_resolve`, `timeout_state`) because the
module-level `NAME = 1/0` kills the counter before `--print-predicate` /
`--pin-only`; only `timeout_scope` is the intended new-check signal.
Fix (erratum/SCORECARD, not a counter edit): say "eight of nine print met; the
ninth is a crash control (exit 2), rejected by v3 as `timeout_scope`-violation
exit 1", and keep `divzero` labelled a crash fixture rather than a survivor.

### F2 — MEDIUM (C1 kill-rule wording): the shadow-only clause is inverted

Contract.md:97-99: "a checker that only adds function-local shadowing still
accepts the decoy drain → `CONFORM=unmet`". A checker that *accepts* the decoy
drain prints `CONFORM=met`; the r39 decoy red receipt proves it
(`c10-red-decoy.txt:8` `check drain_shape PASS (violations=[])`, line 12
`CONFORM=met`). Adding only the shadow arm to v2 leaves `drain_shape` untouched,
so the partial checker still prints met. The arrow as written describes the
fixture's required v3 verdict, not the partial checker's output; a reviewer
testing it literally would score the control backwards.
Fix: "… still accepts the decoy drain → prints `CONFORM=met`, so the frozen
decoy after-verdict (`unmet`, `drain_bind` FAIL) fails it." The decoy fixture
does discriminate v3 from the partial checker.

### F3 — MEDIUM (C2 Before wording): dag-p "fabricates a `changed` line" is not observable

`c11-red-firstparent.txt:5` and `c11-after-fixture-p.txt:5` both print
`changed S001 superseded_by=S002`. That line is the legitimate edit from the
DAG's side commit `s1` (the hand-written dag-p expectation in
`tools/mori-sources-appendonly.py:612-614` includes
`round_changed: ["S001"]`). The v2 merge fall-through does not add a printed
`changed` line; it flips the timing classification to
`as_of=[] stale=[S001]` (red lines 6-7) where v3 prints
`as_of=[S001] stale=[]` (after lines 6-7). The same observation is in the peer
report `ExeDagP.md`: "No additional changed line is attributed to the merge."
The kill rule ("the frozen fixture fails") still works, because the dag-p
selftest arm compares `superseded_as_of`/`stale_supersede` against the
hand-written expected dict (`check_one`, gate lines 806-830). Correct the
Before cell to "fabricates the merge edit, flipping S001 stale" rather than
"fabricates a changed line".

### F4 — LOW (C2 Before wording): dag-r "prints a `changed` event" is invisible in the receipt

`c11-red-readd.txt` prints no `changed S008` line:
`appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[S008]`
(line 5), `supersede_timing superseded_as_of=[] stale_supersede=[]` (line 6).
v3 prints the same `round_changed=[S008]` and additionally
`superseded=[S008]` / `as_of=[S008]`; the visible discriminator is the
superseded/as-of membership, not a changed event. The lesson already records
this honestly (`corpus/lessons/round-40.md:26-32`: the changed event is
"invisible at the frozen bytes"; the fixture was redesigned so v2's
edit-bounded set visibly omits S008). The SCORECARD's restatement is accurate
("a gate keeping the re-add changed event prints `stale=[S008]` on dag-r",
SCORECARD:2241-2242); the contract's Before sentence should be brought in line.
The kill rule's teeth are the hand-written dag-r expected dict
(`superseded_as_of: ["S008"]`, `stale_supersede: []`), which a kept re-add
changed event would fail (`last_edit = r2`, landing `s1` → stale).

### F5 — LOW (C2 kill-rule number): "declared 19 ids" is wrong; measured 35, v2 18

Contract.md:143-145 says "mismatches the declared 19 ids"; the wave context
says 34; `c11-after-lane.txt` parses to **35** as-of ids (S226 present), while
`c11-before-lane.txt` has 18 (S226 absent) and `c11-after-e37dcc6.txt` has
33 as-of + `[S069]` = 34. The 17 newcomers are S226 plus the 16 never-edited
ids enumerated in the lane-line count above; SCORECARD:2231-2236 and lesson M24
change the number to 34 but also undercount by one ("S226 plus 15 earlier").
The count in the kill rule is claim-sizing, already handled by the sibling
report `CritPredParenthetical.md`. Cross-reference rather than re-litigate; do
not copy "34" into any consolidated report without correcting it to 35
(or quoting the receipt).

### F6 — LOW (C2 receipt discipline): after DAG receipts do not name the gate revision

The red receipts name their instrument in the path
(`fixtures/extracted/gate-v2-bb1f2457.py`); the after receipts run
`tools/mori-sources-appendonly.py` with only `HEAD`/`--round-base` as the gate
arguments and no rev/sha for the script bytes. The freeze pin plus
`sha256`/`git show 265a955cc` bind the disk bytes to the scored tip (verified),
but the receipt alone does not name the measured gate revision. Under the r39
finding-9 discipline a one-line `gate_sha256:`/`rev:` header would close this.
The `c11-after-lane`/`c11-after-e37dcc6` receipts do pass the measured rev
argument, so this is specific to the three DAG receipts.

### F7 — LOW (C1 conjunct control provenance): the v3 gutted fixture postdates the receipt

`c10-after-conjunct.txt` (committed at `8d3badd`) runs
`.ufo/waves/round-40/fixtures/generated/conform-v3-conjunct-gutted.py`, which is
absent at the scored tip `265a955cc` and first committed at `ede486b`
(command output above). The receipt is committed before its fixture. The r39
gutted copy is present at `265a955cc`; the freeze pins cover the builders
(`make-survivor-fixtures.py`, `run-c11-dags.py`) but not the gutted payloads.
The committed receipt records `pass=0 fail=10` with `selftest_conjunct` in
every arm's failing list (I did not re-run the gutted copy; peer seat
`ExeConjunctAfter` owns that replay), so this is provenance ordering, not a
false receipt. If the integration commit is `ede486b` or later, no action; if the
round is scored strictly at `265a955cc`, the C1 conjunct kill-rule control's
fixture is not in the scored tree.

### F8 — NOTE (evidence drift, peer-reported): three c10 receipts differ in the working tree

`git status --porcelain -- .ufo/waves/round-40/evidence` shows modified
`c10-after-conjunct.txt`, `c10-after-selftest.txt`, `c10-red-conjunct.txt`
(command-path/timing edits made during wave 1). This is the same drift reported
by `RevC1Receipts.md` F1 (HIGH there); I read and compared the **committed**
blobs at `8d3badd`, so none of my verdicts depends on the working-tree copies.
The main agent should revert or intentionally commit those three files before
integration. Also untracked at the lane root: a 24-byte file `265a955`
containing `=== GATE DELTA bb1f245-` (mtime 03:07, not written by this seat —
likely a peer's truncated redirect); it is not under `.scratch/` and should be
deleted before any integration commit.

## Residual risk / verification gaps

- **Replay HEAD:** exact byte replay of the receipts is impossible at the
  current detached HEAD `ede486b`, because `head_pin` reads the repo HEAD; only
  that line differs in my replays. The verdict lines all match. A checkout to
  `265a955cc` would mutate lane state and was not done.
- **DAG builder dependency:** `run-c11-dags.py` builds the DAGs by importing the
  v3 gate module's `_selftest_dag_cases`/`_make_dag_repo`. The red and after runs
  therefore share a builder; the frozen builder is the committed
  `run-c11-dags.py`, and my current-byte replay reproduced both receipts, so no
  builder drift is observable. A truly independent builder would be stronger,
  but is not what the claim's scope requires.
- **Selftest oracles:** the gate selftest compares `ids`, `deleted`,
  `superseded`, `round_changed`, `superseded_as_of`, `stale_supersede`,
  `superseded_by`, and exit against hand-written dicts (`check_one`, gate lines
  798-830), so the C2 kill rules are not just receipt-vs-receipt. The conform
  selftest has 11 mutation arms and does not run the survivor fixtures; the
  survivor controls are receipt-only (as the contract declares).
- **No LSP:** not available; caller/definition checks were execution-based
  (both instrument versions, both selftests, the DAG runner).
- **Tooling:** no installs or upgrades were needed; no pacman invocation.

## Verdict

C1: **control committed for every survivor (10/10 generated, 9/9 named), with
one misclassified control (`divzero`, exit 2 not met) and one inverted
kill-rule clause.** C2: **control committed for all three DAGs (3/3), with the
discriminator correctly reproduced but two Before phrases and the "19 ids"
count misdescribing what the receipts show.** No missing control; no acceptance
failure found in the covered sets.
