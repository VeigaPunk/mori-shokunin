# RevScorecard — round-39 SCORECARD declaration re-derivation at `13bfba23`

Seat: independent leaf reviewer (wave 1). Target: every counting command in the
`SCORECARD.md` round-39 declaration rows (`:2190-2214`), re-run at
`13bfba23b7ca063c76d3504a2ff6eb7b6a294932`, literals compared verbatim.

Instruments were run from the worktree after proving the worktree bytes are the
scored bytes (`git diff --stat 13bfba2 HEAD -- <path>` empty and
`sha256sum` of worktree == `git show 13bfba2:<path> | sha256sum`):

- `.ufo/waves/round-39/count-c7.py` `b92c65f2…0520`
- `.ufo/waves/round-39/conform.py` `fe0be179…7987`
- `tools/mori-sources-appendonly.py` `62cd4132…f01e7`
- `.ufo/waves/round-39/fixtures/run-c9-dags.py` `d75d7740…59b8`

All fixture re-runs were executed on copies under
`.ufo/waves/round-39/scratch/RevScorecard/` (clone sandbox, M19 bypass build,
DAG harness output, red-receipt writes). No lane file was written; the only
writes outside that dir were the counters' own transient `mori-c7-*` temp dirs
under the lane scratch root (created and removed by `count-c7.py:475-476`;
verified absent afterwards). No tool install or upgrade was needed.

`lsp` device was not present in this seat's tool inventory, so caller /
definition / diagnostics checks were done over git objects and counter runs.
Every claim below cites a path:line or a command whose output I observed; an
unrun literal is marked as such.

## Verdict

**C2's before cell fails its own cited receipt.** Everything else declared in the
round-39 rows reproduces, with two receipt-level accuracy defects (C1 before
literal; clone receipt line) and citation/consistency gaps.

## claim → declared vs observed

| Cell | Declared literal | Observed at `13bfba2` (command) | Verdict |
|---|---|---|---|
| C1 after | five checks PASS, four negatives rejected, `C7=met`, exit 0 | `python3 .ufo/waves/round-39/count-c7.py 13bfba2… --seed 20261024` → `negative witness-* rejected` ×4, `check anchors_v2/capability_v2/live_rows_v2/named_row_drift/drift_kill_v2 PASS`, `C7=met`, `EXIT=0` | **PASS** |
| C1 after (clone) | `live_rows_v2 FAIL … no_copy=['S103']`, `C7=unmet` | sandbox clone re-built from `13f3db7e` (`run-c7-reds.py`, seed 7) → `check live_rows_v2 FAIL (… no_copy=['S103'])`, `C7=unmet`, `exit=1`; r38 counter on same clone → `C4=met`, `exit=0` | **PASS** (see F3 for one unreproducible receipt line) |
| C1 before | four receipts "each end `RED (bypass accepted)`"; clone shows `C4=met` exit 0 | one-char / comment / classifier receipts end with that literal (`grep -l` matches 3 files); `c7-red-clone.txt` contains **0** occurrences of it (`grep -c` = 0) — it ends `verdict round-39: rejected (live_rows_v2 copy rule)` (`:27`) after `verdict r38: RED (fabricated binding accepted)` (`:15`). `C4=met` exit 0 re-derived. | **FAIL (literal)** — substantive RED reproduced, quoted literal is not in 4/4 receipts |
| C2 after | `CONFORM=met` exit 0 | `python3 .ufo/waves/round-39/conform.py 13bfba2…` → 9/9 `check … PASS`, `CONFORM=met`, `EXIT=0` | **PASS** |
| C2 after | `--selftest` → `CONFORM_SELFTEST pass=9 fail=0` | `conform.py 13bfba2 --selftest` → nine `PASS <name>`, `CONFORM_SELFTEST pass=9 fail=0`, `EXIT=0` | **PASS** |
| C2 after | both bypass fixtures → `CONFORM=unmet` with `timeout_value`/`drain_shape` FAIL | r39 conform at `13bfba2`: bypass-none → `timeout_value FAIL`, `drain_shape PASS`, `CONFORM=unmet` exit 1; bypass-wait → `timeout_value PASS`, `drain_shape FAIL`, `CONFORM=unmet` exit 1 | **PASS only distributively** (see F8) |
| C2 before | bypass-none → `CONFORM=met` exit 0 | r38 conform bytes (`git show 13f3db7e:.ufo/waves/round-38/conform.py`, `580a0bf1…01e`) on rebuilt bypass-none → `CONFORM=met`, exit **0** | **PASS** |
| C2 before | "bypass-wait likewise" → `CONFORM=met` exit 0 | same r38 bytes on rebuilt bypass-wait → `check bounded_reads FAIL (popen=False)`, `check timeout_state FAIL`, `CONFORM=unmet`, exit **1**; committed receipt agrees: `evidence/c8-red-wait.txt:10-11` `CONFORM=unmet` / `verdict: not reproduced` | **FAIL** (own receipt refutes the cell) |
| C2 before | r38 selftest never mutates a communicate timeout | r38 conform at `13f3db7e` has one `bounded_reads` mutation, targeting `proc = run([...], timeout=timeout …)` (`git show 13f3db7e:.ufo/waves/round-38/conform.py:229`); no mutation string references `communicate` | **PASS** |
| C3 before | r38 gate fabricates `round_changed=[S001]` on fixture C (exit 1) | `run-c9-dags.py` with `gate-r38.py` (sha `9a6164e3…09fa` == `git show 13f3db7e:tools/…`) → dag-c `round_changed=[S001]`, `EXIT=1` | **PASS** |
| C3 before | `stale_supersede=[S001]` on fixture D, predicate reads as-of | dag-d → `superseded_as_of=[] stale_supersede=[S001]`, `EXIT=1`; matches `evidence/c9-red-a.txt` | **PASS** |
| C3 before | walk drops `6531ac60` (53 vs 52) | at `13f3db7e`: `git rev-list --count --full-history` = 53, default = 52; `6531ac60` present in full-history (1), absent under default (0) | **PASS at entering tip**; the counts are **54/53** at `13bfba2` (see F7) |
| C3 after | `--selftest` → `pass=12 fail=0` | `python3 tools/mori-sources-appendonly.py --selftest` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=12 fail=0`, `EXIT=0` | **PASS** |
| C3 after | v2 gate: A `stale_supersede=[S001]`, C `round_changed=[]` exit 0, D `superseded_as_of=[S001]` | re-derived exactly: A → stale=[S001] EXIT=1; C → `round_changed=[]` EXIT=0; D → as-of=[S001] EXIT=1 | **PASS** (D literal's receipt uncited — F6) |
| C3 after | lane receipts byte-identical to r38 at the tip and `e37dcc6` | v2 at `13bfba2` vs `.ufo/waves/round-38/evidence/gate-after.txt` (minus `command:`/`P-C`/`EXIT` lines): `diff` empty → BODY-IDENTICAL; at `e37dcc6` vs `gate-after-e37dcc6.txt`: BODY-IDENTICAL (`stale_supersede=[S069]` both) | **PASS** |

## Findings by severity

### F1 — HIGH: C2 before cell's `bypass-wait` clause is false, and its own receipt says so

`SCORECARD.md:2199` declares "bypass-wait likewise (`evidence/c8-red-wait.txt`)" under
"→ `CONFORM=met` exit 0". Re-run of the r38 checker bytes at the entering tip on the
rebuilt fixture:

```
check bounded_reads    FAIL (bypass-wait.py: run=True popen=False cap=True mkdtemp=True scratch=True)
check timeout_state    FAIL (exit=None timeout_reason=False pass=False)
CONFORM=unmet      EXIT_WAIT=1
```

The cited receipt states the same thing: `evidence/c8-red-wait.txt:7` `bounded_reads FAIL`,
`:10` `CONFORM=unmet`, `:11` `verdict: not reproduced`. The r38 `bounded_reads` conjunct
requires a detected `Popen` drain (`popen=False`), so the wait+read hang never passed the
r38 checker through this fixture. Consequence for the claim chain: the r38-M19 premise
"the `wait`+`read` drain passes the r38 checker" is not established by any shipped
artifact, while the after-side (r39 `drain_shape` rejects it) is established. Scanning a
`met` literal on the before side needs a fixture that actually reaches r38's
`bounded_reads` pass path; today only bypass-none does.

### F2 — MEDIUM: C1 before cell quotes a verdict string 3 of its 4 receipts do not all contain

`SCORECARD.md:2198` says the four receipts "each end 'RED (bypass accepted)'".
`grep -c "RED (bypass accepted)" evidence/c7-red-clone.txt` = **0**; that receipt ends on the
round-39 block (`:27` `verdict round-39: rejected (live_rows_v2 copy rule)`) and its r38
verdict reads `RED (fabricated binding accepted)` (`:15`). The substantive claim (r38
accepts the fabrications; clone prints `C4=met` exit 0) is re-derived and true, so this is a
declaration-accuracy defect, not a false claim about the instrument.

### F3 — MEDIUM: one line of `c7-red-clone.txt` cannot be produced by any counter blob at the tip

`evidence/c7-red-clone.txt:25` prints
`check drift_kill_v2    FAIL (mutation anchor or table unparsable)`.
The tip counter has no such string: its failure branch is
`check("drift_kill_v2", False, "mutation anchor absent")` (`count-c7.py:513`), and
`git show 13bfba2:.ufo/waves/round-39/count-c7.py | grep -c unparsable` = 0. Re-running the
same clone at the receipt's own seed (`--seed 7`) with tip bytes prints
`check drift_kill_v2    PASS (drawn=unavailable … flips_ok=True)` and `C7=unmet`.
So the receipt line comes from counter bytes that are **not** at `13bfba2` (a pre-freeze
counter revision), and the drift-kill arm's verdict on the clone is not reproducible in
shape — only the declared `live_rows_v2 FAIL … no_copy=['S103']` / `C7=unmet` literals are.
This is independent corroboration of the ScribeLesson M22 finding, now with the
tip-counter branch line cited.

### F4 — MEDIUM: the C2 before command as written cannot run

`SCORECARD.md:2199` quotes `--counter fixtures-derived/bypass-none.py`. No such path
exists at the scored tip (`ls -d fixtures-derived` → absent; no committed file references
it). Run verbatim, the command dies before printing any `check`/`CONFORM` line, so the
declared literal is only reachable by substituting a rebuilt fixture
(`fixtures/make-m19-bypass.py 13f3db7e <lane> <out>`). The cell should cite that build
command or a committed fixture path.

### F5 — MEDIUM: the frozen contract's C3 "Before" and "After" paragraphs contradict the receipts

- `contract.md` C3 Before: "the round-38 gate bytes … print `superseded_as_of=[S001]` for a
  superseder that never descends from the edit (fixture A)". Observed (and in
  `c9-red-a.txt`): fixture A prints `superseded_as_of=[] stale_supersede=[S001]`; it is
  fixture **C** that prints `superseded_as_of=[S001]`. The SCORECARD row states the correct
  fixtures (C → `round_changed`, D → `stale_supersede`), so the row is sound and the
  contract paragraph is the wrong artifact. The P-C9 rationale line that the round-38
  bytes "print as-of …" on the side-branch fixture therefore rests on a mis-stated example.
- `contract.md` C3 After declares `MORI_SOURCES_APPENDONLY_SELFTEST pass=11 fail=0`; the
  gate prints `pass=12 fail=0` (and `SCORECARD.md:2201` and
  `evidence/gate-selftest-after.txt` both say 12). The contract literal is stale.

### F6 — LOW: fixture-D literal is uncited; five contract-listed evidence paths are absent

`SCORECARD.md:2201` names three fixture verdicts but cites only
`c9-after-fixture-a.txt`, `c9-after-fixture-c.txt`; the `superseded_as_of=[S001]` on D
literal exists only in `evidence/c9-after-fixture-d.txt` (confirmed byte-for-byte).
Separately, the contract's "P-C7/P-C8/P-C9 evidence paths" list cites
`evidence/c7-red-anchors.txt`, `c7-before.txt`, `c8-before.txt`, `c9-red-c.txt`,
`c9-before-lane.txt` — none of these exist at `13bfba2`
(`git ls-tree 13bfba2 .ufo/waves/round-39/evidence/` has no such entries). They are not
load-bearing for the scorecard rows, but the frozen evidence list over-promises.

### F7 — LOW: `c9-after-lane.txt` walk counts are the entering-tip counts at the revision it names

`evidence/c9-after-lane.txt` claims "v2 walk commits (full-history): 53 / v1 walk … 52"
for `f920eaf7`. Recomputed per revision:

| rev | `--full-history` | default | `6531ac60` in full / default |
|---|---|---|---|
| `13f3db7e` (entering) | 53 | 52 | 1 / 0 |
| `f920eaf7` | 54 | 53 | 1 / 0 |
| `13bfba2` | 54 | 53 | 1 / 0 |

The r38-before literal (53 vs 52) is right **for the entering tip**; the after receipt's
numbers are stale by one (S228's data commit added a `corpus/SOURCES.md` revision after the
counts were taken). The substantive claim the counts support — default simplification drops
`6531ac60` — is confirmed at every revision tested.

### F8 — LOW: C2 after cell's two-check phrasing is conjunctive but each fixture fails exactly one

`SCORECARD.md:2199` "both bypass fixtures → `CONFORM=unmet` with `timeout_value`/`drain_shape`
FAIL" reads as two failures each. Observed: bypass-none fails `timeout_value` and **passes**
`drain_shape`; bypass-wait passes `timeout_value` and fails `drain_shape`. Both exit 1 with
`CONFORM=unmet`, so the operational claim holds; the sentence should say "the named conjunct
per fixture" to match the receipts.

### F9 — INFO: `head_pin` is tip-relative, so the "at R" pin does not bind to the requested revision

`conform.py 13bfba2` prints `pin=5561819… tip=5561819…` (HEAD today, one commit past the
scored tip), while `evidence/c8-after.txt` recorded `pin=f920eaf7…`; on the rebuilt bypass
fixtures the pin printed `0662ddbe…`. The `CONFORM=met` literal is unaffected (both sides
move together), but a reader should not treat `head_pin PASS` as evidence that the counter
bytes are the scored revision's.

## Residual risk

- **The one substantive claim defect is on the before side.** C2's after-side instrument
  (nine checks, `timeout_value` + `drain_shape` with the value-constant fold) is verified by
  run at the scored tip; the r38-M19 "two bypasses pass" motivation is half-unsupported
  (F1). A closure that accepts C2 on the after-side literals is not admitting a false
  discrimination claim; a closure that quotes "both bypasses passed r38" would be.
- **C7's clone receipt is partly irreproducible** (F3): the shipped `C7=unmet` verdict is
  reproducible, the `drift_kill_v2 FAIL` line is not, and the drift arm's outcome on the
  clone changed with counter revision (not with seed alone). The seed-drawn arm is
  intentional per P-C7; the `mutation anchor absent` vs `unparsable` divergence is an
  instrument-history artifact, not a predicate failure at the tip.
- **No mutation testing was performed by this seat** (owned by the mutation-tester seats).
  F1 and F3 show that receipt text and instrument bytes can drift apart; only mutation
  seats can bound how far.
- **Lane-history verdicts are unchanged in body, not in counts** (F7). Anyone re-checking
  the C3 "byte-identical" claim must strip the `command:` / `P-C` / `EXIT=` chrome; the
  per-id and summary lines do diff clean at both `13bfba2` and `e37dcc6`.

## Verification gaps

- `lsp` unavailable in this seat's inventory → no semantic reference/definition pass; all
  cross-artifact links checked via `git show` / `grep` / `diff` and counter execution.
- The C1 clone re-derivation used the fixture script's fixed `--seed 7`; the main C7 run
  used the contract's `--seed 20261024` (`drawn=fresh`). Other seeds' drawn states were not
  exhaustively swept here.
- `contract.md`'s cited P-C7/P-C8/P-C9 evidence files that are absent (F6) were not
  reconstructed; I recorded them as missing rather than guessed.
