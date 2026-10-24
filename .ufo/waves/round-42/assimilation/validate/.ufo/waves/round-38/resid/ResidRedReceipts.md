# ResidRedReceipts — residual falsification of the M1/M3/M4/M5/M6 red receipts

Seat: `mori-r38.ResidRedReceipts` (reviewer, round 38, 2026-10-23). Detection only; nothing remediated.

## Scope and tip

- Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
- Tip under attack: `b6993744171a05efc627b5e0664489c31aa5214e`. The instructed check
  `git -C <lane> rev-parse mori` **fails** (`fatal: ambiguous argument 'mori'`): the repo is
  detached HEAD and no branch/tag contains the commit. Verified instead with
  `git rev-parse HEAD` and `git log -1` (subject: "round-38: instrument hardening …, w1+w2 seat
  reports, red receipts M1/M3/M4/M5/M6, LOG round-38 entry").
- Attacked committed bytes only, via `git show b6993744:<path>`. No lane ref, index, jj state,
  or working-tree file was written; this report is the only lane artifact.
- Lesson row under test: `corpus/lessons/round-38.md:47` (M16). Rows it cites:
  M1 `:32`, M3 `:34`, M4 `:35`, M5 `:36`, M6 `:37`.

## Verdict

**All five receipts reproduce in substance.** Each documented red line was reconstructed from
committed instrument bytes with the stated one-site change, run with the receipt's own
arguments, and produced the receipt's red line byte-for-byte (exact line equality except where
noted as an abridgement below). No receipt is vacuous and no receipt number is fabricated.

Two claims in the M16 fix column are nevertheless **not fully true**: M6 is not a mutation
reconstruction (F1), and the "shipped instruments … print the green lines" clause is wrong for
the M1 control and circular for M6 (F2). Two receipts are unmarked excerpts, one of which hides
the very count its lesson row cites (F3), and the M3 row misnames the load-bearing line (F5).

Receipt SHA-256 (committed bytes): m1 `60fba619…76bf521`, m3 `532e6d49…62eb3413`,
m4 `cb0daefa…e17e1e9e`, m5 `c5afa960…00b4a787`, m6 `32311782…85ce1d5e2`.

## Method

For each row I extracted the shipped instrument with `git show b6993744:<path>`, asserted the
mutation anchor occurs exactly once, applied the one-site change in `/tmp/r38v`, and ran the
receipt's command from the lane root with the same interpreter (`python3` 3.14.8, git 2.56.0).
Controls used the unmutated committed bytes with the same command. Scratch copies live under
`/tmp/r38v`; the counter's own `tempfile.mkdtemp` under the lane's round-38 scratch root was
created and removed by the instrument's `finally` — no `mori-c4-*` residue remained and
`git status` shows the five receipts unmodified.

| receipt | documented mutation | my one-site change (committed line) | rerun exit | red-line match | unmutated control |
|---|---|---|---|---|---|
| `m1-red.txt` | `token.strip(".,;)")` strips the leading dot | `count-c4.py:168` `strip().rstrip(".,;)")` → `strip(".,;)")` | 1 (`COUNTER_EXIT=1`) | capability line **byte-identical**; phantom `ufo/waves/round-37/evidence/c2-after.txt` reported missing while `.ufo/…` exists at `e37dcc6` | shipped line prints `.ufo/…`, missing only `evidence/drift-live-r37.txt`; still `C4=unmet` |
| `m3-red.txt` | landing index recorded at the newest state, not the first landing | `mori-sources-appendonly.py:254` `setdefault(...)` → `supersede_rows[(...)] = index` | 1 (`GATE_EXIT=1`) | timing line **byte-identical**: `stale_supersede=[]`, `S069` inside `superseded_as_of` | shipped: `stale_supersede=[S069]`; delta is exactly S069 |
| `m4-red.txt` | selftest grammar pass without the `PREDICATE` filter | `mori-sources-appendonly.py:482` drop `and l.strip() != PREDICATE` | 1 (`GATE_EXIT=1`) | the 6 receipt FAIL lines are the **first 6 of 9**, byte-identical, all `per-id line malformed: "P-C6: …"` | shipped: `MORI_SOURCES_APPENDONLY_SELFTEST pass=9 fail=0` |
| `m5-red.txt` | three semantic no-op mutations in the checker's mutation table | `conform.py:223-233`, three entries → whitespace-only predicate, `path.strip()` resolver, `int(args.tool_timeout)` | 1 (`CHECKER_EXIT=1`) | **all 7 lines byte-identical**: `FAIL predicate/tool_resolve/timeout_state -> failing=[]`, `CONFORM_SELFTEST pass=3 fail=3` | shipped: same six cases `pass=6 fail=0` |
| `m6-red.txt` | *none* — direct validator run | validator `SWARM_ROLES` check (`ufo-swarm-wave.mjs:913-915`) | 1 | stderr line exactly `{"schema":"ufo-swarm-wave-error-v1","code":"unknown_role",…}`, receipt body == `VALIDATOR_EXIT=1` + that line | no mutation to compare; role list excludes `planner` by design |

Exact mutations applied (reproducible from committed bytes):

```
count-c4.py:168
-        token = token.strip().rstrip(".,;)")
+        token = token.strip(".,;)")

mori-sources-appendonly.py:254
-                supersede_rows.setdefault((m.group(1), cells[0].strip()), index)
+                supersede_rows[(m.group(1), cells[0].strip())] = index

mori-sources-appendonly.py:482
-                         if l.strip() and l.strip() != PREDICATE]
+                         if l.strip()]

conform.py:223-233 (three entries of the mutation list)
- ("predicate", "head_at_measurement=<40-hex>.", "lane_tip=<40-hex>.", "predicate token changed")
+ ("predicate", "hidden truth for ids", "hidden  truth for ids", "predicate whitespace-only change")
- "return path", "relative resolution removed")
+ "return os.path.abspath(os.path.join(os.path.abspath(repo), path.strip()))", "semantic no-op mutation")
- "_TOOL_BUDGET[0] = TOOL_TIMEOUT_S", "budget flag ignored")
+ "_TOOL_BUDGET[0] = max(1, int(args.tool_timeout))", "semantic no-op mutation")
```

The three no-ops are genuinely semantic no-ops at the evaluated points: `normalise()` collapses
the doubled space; the resolver receives a space-free fixture path; `--tool-timeout` is declared
`type=int` (`count-c1.py:947`), so `int()` changes nothing. Each mutated counter survived every
check (`failing=[]`), which is exactly the pre-fix class.

M6 was reproduced twice: with the receipt's own (untracked) spec at its lane path, and with a
self-authored equivalent spec (`reportDir` relative) run from `/tmp`, so the result does not
depend on the seat's scratch file. Node runtimes 24.21.0 and 26.12.0 both emit the same line.
Validator file: `/home/vgpnk/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs`, sha256
`1d33a03ffb204bc499310589199590d305b677fbe4fb2dfdb924f7c0f5f09d0a`.

## Findings

### F1 (medium) — M16's uniform "one-spot mutation of the shipped instrument" is false for M6

M16 (`corpus/lessons/round-38.md:47`) states that "each row's pre-fix state is reconstructed by
a one-spot mutation of the shipped instrument and run to a committed receipt", and lists
`evidence/m6-red.txt` in that series. M6 is not a mutation and has no pre-fix state: the M6 row's
own fix is "recorded here and in the report; no planner role was dispatched" (`:37`), i.e. a
scope avoidance. `m6-red.txt` is a plain run of the shipped fleet validator against a spec whose
`items[0].role` is `"planner"`; the receipt demonstrates the role rule, not a repaired defect and
not an instrument mutation. Consequence: the M16 sentence cannot be read as an audit trail over
five mutation reconstructions; it covers four mutations plus one steady-state rejection.

Secondary to this: the m5 reconstruction is three edits inside one mutation table (4 changed
lines), not strictly one spot. M16's own parenthetical ("three non-load-bearing mutations")
states this correctly; only the blanket "one-spot" wording is imprecise.

### F2 (medium) — the "shipped instruments … print the green lines" clause is wrong for the M1 control and circular for M6

M16 lists `evidence/c4-before.txt`, `gate-after-e37dcc6.txt`, `gate-selftest-after.txt`,
`c5-after-selftest.txt` and "`evidence/m6-red.txt`'s validator rule" as the green counterparts.

- `c4-before.txt` is **not green**: it ends `C4=unmet` / `EXIT=1`. It is also **not the shipped
  instrument's output**: its check details lack the `empty=0 unique=True` and `unique=True`
  fields that the tip (post-hardening) counter prints, so it was produced by a pre-hardening
  `count-c4.py`. Side-by-side at `e37dcc6`: evidence `check anchors FAIL (anchors=0 missing=[])`
  vs shipped `check anchors FAIL (anchors=0 missing=[] empty=0 unique=True)`; evidence
  `check live_rows PASS (named=10 summary_drifted=10 unknown=[])` vs shipped `… unknown=[]
  unique=True`. The able-to-fail relation still holds — I verified it directly: the shipped
  counter prints `.ufo/waves/round-37/evidence/c2-after.txt`, the mutant prints
  `ufo/waves/round-37/evidence/c2-after.txt` — but the cited file is not that control.
- `evidence/m6-red.txt` is named as the green line for the same command whose red receipt it is.
  There is no green counterpart for M6 (there is nothing to be green about); the clause is
  circular for that row.

`gate-after-e37dcc6.txt` (timing line), `gate-selftest-after.txt` (`pass=9 fail=0`) and
`c5-after-selftest.txt` (`pass=6 fail=0`) do match my shipped-control runs (modulo those files'
`command:`/`EXIT=` wrappers).

### F3 (low) — `m4-red.txt` is an unmarked excerpt that omits the number the M4 row cites

The committed receipt shows 6 of the 9 failing selftest cases and stops; it contains neither
`MORI_SOURCES_APPENDONLY_SELFTEST pass=0 fail=9` nor any elision marker. The M4 row's evidence
cell cites "`--selftest` failed 9/9" (`:35`), and M16 repeats "per-id line malformed … exit 1"
without the count. My rerun confirms 9/9: the receipt's six lines are a byte-exact prefix of the
nine, and the omitted tail is `FAIL supersede before edit`, `FAIL row reorder`,
`FAIL whitespace padding`, `MORI_SOURCES_APPENDONLY_SELFTEST pass=0 fail=9`. The seat's own
untracked `scratch/red-receipts/m4-out.txt` does contain all nine plus the summary, so this is a
transcription cut, not a different run. A reader of the committed receipt cannot see the number
the lesson asserts without re-running.

### F4 (low) — `m1-red.txt` and `m3-red.txt` are also unmarked excerpts

- `m1-red.txt` drops the `P-C4:` predicate and the three `negative … rejected` lines that the
  house-style `c4-before.txt` includes.
- `m3-red.txt` drops the `P-C6:` predicate, all 18 `changed S… superseded_by=…` lines and the
  `appendonly_violations=…` line, keeping only the timing line.

Their red lines are byte-identical to my reruns, so substance is intact; the omissions are
provenance loss, not falsity. The convention in the round-38 evidence directory is otherwise to
include `command:` plus the full stdout (`c4-before.txt`, `c5-before.txt`); these two receipts
deviate silently.

### F5 (low) — the M3 row misnames the load-bearing line; the receipt's mutation is the correct one

The M3 evidence cell says "`if index > previous[0]` overwrote the first landing on every later
state" (`:34`). I mutated that line as literally as possible (unconditional
`supersede_landing[target] = (index, by)`, all else shipped) and ran the receipt's command:

```
supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] stale_supersede=[S069]
```

i.e. **green**. The lane has 34 supersede pairs at `e37dcc6` and no target with more than one
superseder, so with the first-landing key intact the comparison line cannot produce the claimed
drift. The red state requires the missing `setdefault` (pair index = last appearance), which is
exactly the mutation `m3-red.txt`'s header names and which I reproduced. So the receipt is the
right reconstruction and the M3 row's quoted mechanism is the wrong line. (The exact pre-fix
text was never committed, so the row's wording is an approximation that should be corrected to
name the first-landing record, not the comparison.)

### F6 (low) — none of the five receipts is replayable from the commit

Every `command:` line points into `.ufo/waves/round-38/scratch/red-receipts/`
(`git ls-files` → 0 tracked entries; `git check-ignore` → not ignored), or, for m6, at a
fleet-external script `~/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs` not pinned by this
lane. A clean checkout of `b6993744` cannot execute the stated command; the reader must re-derive
the mutation (as this seat did) or trust the transcript. This is the residual of the exact defect
M16 set out to cure — the receipts now exist and reproduce, but their recipes are still not part
of the commit. Committing the five mutant scripts plus the m6 spec (or inlining the one-hunk
diff in each receipt, as done above) would close it.

### F7 (info) — tip verification as instructed fails

`git -C <lane> rev-parse mori` errors (`unknown revision`), the repo is detached, and
`git branch --contains b6993744` returns no ref. I verified the tip via `HEAD` and the commit
subject. Not a receipts defect; a context/harness defect.

### F8 (info) — the M16 locator fix checks out

Lesson `:9` now reads `S226.src:657-659`; `RevS226Row.md` (committed, `w2/RevS226Row.md`) quotes
the pre-fix locator `657-658` and says the sentence runs to line 659; `corpus/evidence/sources-r38/S226.src:657-659`
holds exactly "Return the canonical path … (if they are supported by the operating system)." —
24 words, within the ≤25-word limit. The M16 evidence (RevS226Row verdict FAIL with a per-row
not-backed table for M1, M3–M6) matches the committed file.

## Residual risk

- **Counterfactual reconstructions.** No pre-fix instrument bytes exist in lane history: the gate
  at `e37dcc6` predates `supersede_timing` entirely; the gate at `daa1d4d` and the conform at
  `1f1e996`/`f725f307` already contain the fixed `setdefault`+filter and the strong mutation
  table. Every "pre-fix state" receipt is therefore a mutation-based counterfactual; the exact
  original defective text is unrecoverable. In particular M5's quoted original
  `CONFORM_SELFTEST pass=2 fail=4` cannot be reproduced from any committed bytes — only the
  class (`pass=3 fail=3` with three semantic no-ops) can, which is what the receipt says.
- **M1's verdict line is not mutation-specific.** At `e37dcc6` the shipped counter also reports
  `C4=unmet` (`anchors=0` is a property of that revision). The mutation-specific evidence is the
  capability line only; the receipt shows both and is therefore honest, but `C4=unmet` alone
  must not be read as proof of the strip defect.
- **M6 provenance.** The rejection depends on an external validator (sha256 recorded) and a node
  runtime; 24.21.0 and 26.12.0 agree today, but neither is pinned by the lane. The validator's
  own role list is the authority; the receipt is re-derivable only while that fleet path exists.
- **Out of scope / not judged:** M2 and M7–M9, the round's Gate admission decision, full round
  acceptance, and any integration/landing judgement. This seat neither edited nor remediated any
  file.

## Tooling

No tool was installed or upgraded; the environment already had Python 3.14.8, git 2.56.0, Node
24.21.0 (bash PATH) and 26.12.0 (eval PATH). No pacman transaction was attempted.

Report: .ufo/waves/round-38/resid/ResidRedReceipts.md
