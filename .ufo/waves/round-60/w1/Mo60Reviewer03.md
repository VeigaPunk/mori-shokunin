# Mo60Reviewer03 — C1 re-derivation at the current lane tip

Scope: re-run and independently falsify the frozen C1 predicate at the lane tip,
read-only. Freeze `ac496c7cde8cad965079858accae3bedfe4a73f2`, entering
`ddfb12fb0838b4307c445194a844f0c4b1950195`. No lane writes, no VCS mutation
(one throwaway `git clone --shared` under scratch for mutation probes;
`git rev-parse --show-toplevel` asserted that clone). Scratch:
`/fast/scratch/hyaku/mori-r60/Mo60Reviewer03` (cleaned after filing).

Tip at scoring: **`b3c256138f00c704d5aa56eb0332d74506502ef2`** (tracked tree clean;
`git status --porcelain` shows only the pre-existing untracked `w1/`, `w1.ready*`,
`evidence/c1-at-data.txt`). Tip was unchanged at the start and end of the run and
already carries the C1 data (landed at `398d3225`), so no 10-minute retry was needed.

## Verdict

`C1=met` reproduces **byte-exactly**, deterministic, exit 0, with the counter bytes
frozen at the contract pin. Two instrument laxities were demonstrated as met-flips
in a scratch clone; one of them (F1) means the published `lesson=ok` token is only
valid under the *collective* reading of the lesson clause — under the distributive
reading the tip data scores `lesson=3/5` and C1 would be `unmet`.

## Re-derivation (all reproduced, exact outputs)

```
$ python3 .ufo/waves/round-60/count-c1.py b3c256138f00c704d5aa56eb0332d74506502ef2 --scratch <scratch>/c1
C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=b3c256138f00c704d5aa56eb0332d74506502ef2
EXIT=0
```
Second run (`<scratch>/rerun2`): identical bytes, `rc=0`; byte-equal to the untracked
working-tree receipt `.ufo/waves/round-60/evidence/c1-at-data.txt` (`cmp` → equal).

```
$ sha256sum .ufo/waves/round-60/count-c1.py      → 795c1f3193a76406a40561ac60fedb3eee75fc38df2b2efb3fc5295d617ddbae
$ git show ac496c7c:.ufo/waves/round-60/count-c1.py | sha256sum  → same
$ git diff --name-only ac496c7c..b3c25613 -- count-c1.py count-c2.py count-c3.py contract.md tools/mori-entry-claims-check.py trees-c2h build-fixtures-r60.py
(empty)
```
Counter sha equals the contract's `795c1f31…ddbae`; no r60 instrument/contract/tool/tree
bytes moved between freeze and tip (kill rule intact).

```
$ python3 .ufo/waves/round-60/count-c1.py --selftest
C1_SELFTEST pass=6 fail=0   EXIT=0
```
```
$ python3 .ufo/waves/round-60/count-c1.py ddfb12fb0838b4307c445194a844f0c4b1950195
C1=unmet dead-uncorrected=2 receipts=0/2 absent-set=0/5 lesson=absent rev=ddfb12fb… failed=absent_set=0/5,absent_table_absent,correction_incomplete,dead=2,lesson_absent,receipt_absent:…r59-c1-met.txt,receipt_absent:…r59-c2-met.txt,receipts=0/2
EXIT=1
```
byte-equal to committed `.ufo/waves/round-60/evidence/control-c1-do-nothing.txt`
(`cmp` → equal). The do-nothing arm is real, not vacuous.

### Arm-by-arm independent checks

1. **DEAD-NAME ARM** — `git show b3c25613:SCORECARD.md | grep -n 'c1-entering\.txt\|c2-entering\.txt'`
   yields exactly 2 hits, SCORECARD.md **lines 2950 and 2951**; both lines carry
   `r60-correction:` and the matching real pointer (`control-c1-do-nothing.txt` /
   `control-c2-do-nothing.txt`). Strict universal sweep (every marked line carrying a
   dead name must also carry its real pointer): `STRICT_DEAD_ROGUE_LINES=0`,
   `marker_lines=2`. Both real files resolve at R (`git cat-file -e`).
2. **RECEIPTS ARM** — materialized the r59 counters from `7b86704d` and ran them at
   `7b86704d` myself (not via count-c1):
   ```
   C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=7b86704d…      rc=0 stderr empty
   C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 rev=7b86704d…
   ```
   stdout sha256 vs committed receipts: `167c9fed65ce5bd5aef6b3487d07f25eae237fd073a003877668e67a79bcdee4`
   and `4859d5ca7226aad23ab97b537b6c75ca1c73449ba7fc98211079cc2fb6caecb7` — **byte-equal**
   to both committed receipts.
3. **ABSENT-SET ARM** — `git cat-file -e 7b86704d:.ufo/waves/round-59/w1/<name>.md`
   is ABSENT for all five names; at tip present for all five. Table disposition
   `late-committed` for all five therefore matches the frozen grammar. Landing-pointer
   cells verified with `git log --diff-filter=A`: Executor40 → `f091bd77`,
   MutationTester31 → `f091bd77`, MutationTester32 → `bf6c0ad3`, Critic29 → `bf6c0ad3`,
   Reviewer16 → `bf6c0ad3`; the table's timestamps are the **committer** dates
   (`f091bd77 ci=07:42:42 -0300`, `bf6c0ad3 ci=03:12:38 -0300`) and are accurate.
4. **LESSON** — `corpus/lessons/round-60.md` at R contains all five names (lines
   50, 53, 55, 58, 59), `f091bd77`, and the literal `supersedes round-59` (line 44).

## Findings

### F1 — HIGH · `lesson=ok` does not entail the frozen lesson clause (predicate deviation, claim-relevant)
Frozen clause: "…naming every wrong-superseded name with `supersedes`, **every
late-committed name with landing pointer `f091bd77`**". The counter
(`count-c1.py:213-233`) checks only (a) each name appears *somewhere* in the file and
(b) the literal `f091bd77` appears *somewhere* in the file — line 228:
`if not (name in lt and R59_LANDING[:8] in lt):`. No name↔pointer adjacency is bound.

All five names are `late-committed` under the frozen disposition rule, so the clause
demands `f091bd77` per name. Strict per-entry check at tip:

```
Mo59Executor40        entry_has_f091bd77=True
Mo59MutationTester31  entry_has_f091bd77=True
Mo59MutationTester32  entry_has_f091bd77=True
Mo59Critic29          entry_has_f091bd77=False   (names bf6c0ad3 only)
Mo59Reviewer16        entry_has_f091bd77=False   (names bf6c0ad3 only)
STRICT_LESSON=3/5
```
So under the distributive reading the tip scores `lesson=bad` and **C1=unmet**; the
counter prints `lesson=ok` because `f091bd77` occurs elsewhere (lesson lines 56, 58,
59, 60, 75). Root cause is contract-level, not lane fabrication: `7b86704d`
(ci 03:00:51) predates the r59 integration commit `bf6c0ad3` (ci 03:12:38), so
"absent at the data revision ⇒ late-committed" mislabels two pre-filing landings and
then demands a pointer that would be *false* for them. The table's own grammar note
(`r59-absent-set.md`, "Disposition grammar note") and the lesson acknowledge this
honestly. Required: the lane must record which reading is scored (distributive vs
collective); if distributive, C1 is unmet at this tip; if collective, the contract
sentence should be read as such and that must be stated in the report/lesson. I do
not decide the ruling — flagging the deviation.

### F2 — HIGH · met-flip demo: dropping a landing pointer keeps `C1=met`
Scratch clone (`git clone --shared`, toplevel asserted), branch from `b3c25613`,
mutation `6be28e4d` = remove `` `f091bd77` `` from the **Mo59Executor40** entry only
(every other occurrence, including the global ones, left intact):
```
C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=6be28e4d26588b01808d1c0195e10c5729632057
EXIT=0
```
Control mutation `124f3a77` = rename the same entry to `Mo59Exec40` (pointer restored):
```
C1=unmet … lesson=bad rev=124f3a7716f1a0bd76481de05a807d73f3f43eb2 failed=lesson:Mo59Executor40
EXIT=1
```
Pair isolates the defect exactly: name presence is checked, pointer binding is not.
Same class as the r59-routed entry defects that C2 hardened (H4 per-copy row binding);
C1's lesson arm was not hardened.

### F3 — MEDIUM · met-flip demo: a rogue corrected line passes the dead-name arm
Contract: "every corrected line names the real committed pointer it supersedes the
dead name with" (universal). `corrected_lines_name_real` (`count-c1.py:88-98`) is
existential: it needs **one** marked line per dead name that also carries the real
pointer. Mutation `52210ee9` = append to SCORECARD at a fresh branch from `b3c25613`:
```
| r60 rogue | `.ufo/waves/round-59/evidence/c1-entering.txt` | r60-correction: pending |
```
```
C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=52210ee9fd988262e7282c43df2192cb0163ca9b
EXIT=0
```
i.e. a marked line citing the dead name with no superseding pointer is accepted.
No claim-level impact at the real tip (`STRICT_DEAD_ROGUE_LINES=0`), but the arm is
weaker than the frozen sentence for any future state of the tree.

### F4 — LOW (latent) · the `wrong-superseded` branch is both unexercised and global
`count-c1.py:224` (`name in lt and "supersedes" in lt`) has the same global-presence
shape as F1, and **no name exercises it this round** — all five names are
`late-committed`, so the only lesson branch actually executed is the loose one.
A pool-of-one: a future round that legitimately marks a name `wrong-superseded` gets
no binding check at all.

### F5 — INFO · receipts-arm reproducibility is host/path dependent
`rerun_receipt` (`count-c1.py:121-140`) passes `--repo` but **not** `--fleet`; the r59
counter then falls back to its hard-coded `/home/vgpnk/Projects/shokunin` (`r59
count-c1.py:247`) and to fleet rev `2807c6ab…` for `MANIFEST.json`. Byte-equality of
the two receipts therefore holds only while that fleet path and that fleet revision
resolve. It held for this run; it is not a portable property of revision-pinned lane
bytes. (Contract's "no r60 instrument carries an absolute host path" still holds —
the absolute path lives in the r59 artifact, not the r60 counter.)

### F6 — INFO · at-data receipt not committed
`.ufo/waves/round-60/evidence/c1-at-data.txt` is untracked at `b3c25613` (working tree
only). The frozen predicate does not require it, and my independent re-run is
byte-identical to it, so this is a housekeeping note: if the round commits the tip
without it, the at-data receipt will not exist in-tree.

### F7 — INFO (observed, not mine) · a PoC marker landed in the lane working tree
While this seat ran read-only C1 work, an untracked `EXEC-MARKER` appeared at the lane
root:
```
-rw-r--r-- 1 vgpnk vgpnk 92 2026-10-28 13:16:28.226888946 -0300 EXEC-MARKER
executed /fast/scratch/hyaku/mori-r60/Mo60Executor58/full-old/real2/round-53/w1-results.json
```
It is attributable to another seat's PoC scratch path (`Mo60Executor58`), not to this
seat: my only subprocess executions were `git` reads plus `count-c1.py` (which executes
only revision-pinned r59 counters materialized from `7b86704d`). It does not affect the
C1 verdict (the counter reads git blobs at `b3c25613`; untracked files cannot reach it),
but it is a live hygiene risk: it is untracked at the tip, so a later `git add -A`
would commit a control marker into the round. Detection only — I did not delete or
modify it, and I flag it for the integrator's sweep gate. (Lifecycle note: the file was
present at 13:16:28 and already absent — removed by another process, not this seat — at
13:17:17, so the window for a stray `git add -A` was ~49 s.)

## Residual risk

- **Predicate ambiguity is now load-bearing for the verdict.** `C1=met` at
  `b3c25613` is exact and reproducible, but its `lesson=ok` token rests on the
  collective reading. If the round later rules distributive, the same command returns
  `unmet` — not because bytes moved, but because the predicate was under-implemented.
- **Absent-set classification is data-revision-relative.** The five names were absent
  at `7b86704d` simply because that commit precedes the r59 integration commit; the
  `late-committed` label is correct under the frozen grammar but carries no claim
  about filing time. The table and lesson say this explicitly; they do not overclaim.
- **`c1-entering.txt` remains cited in the r59 report and in unmodified historical
  artifacts** (`git grep` at tip, e.g. `.ufo/waves/round-50/a2w1/…:253`). The predicate
  scopes only `SCORECARD.md`, and both dead names survive in `build-w1-spec.py` /
  `w1-dispatch.json` as task text. No overclaim, but a future "no dead names anywhere"
  predicate would fail today.
- **Mutation probes used a `--shared` clone of the lane `.git`.** All five clone-side
  commits are inside the throwaway scratch dir; `git rev-parse --show-toplevel` printed
  that clone before every git write. Nothing was written to the lane, fleet, or
  sibling repos.

## Verification gaps

- I did not re-derive C2 or C3 (out of seat scope) and did not score them.
- I did not exercise the `wrong-superseded` lesson branch with a mutation (F4 is
  analytic: no real name reaches it, so a probe would require also fabricating table
  dispositions whose git truth disagrees).
- I did not test `parse_absent_table` against duplicate rows or a cell-count-varied row
  beyond the committed selftest cases; the arm's cells were verified against git truth
  directly, which is the stronger check.
