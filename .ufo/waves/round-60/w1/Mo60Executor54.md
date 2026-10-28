# Mo60Executor54 — C1 progress probe at the lane tip (round 60, w1)

Role: executor, leaf. Work mode: read-only (no VCS mutation, no production edits). Seat task:
run `count-c1` at the current lane tip and return the exact line + rc; repeat once only if the
C1 data had not landed. It had landed, so runs 1-2 below are at the tip and are identical.

Host guard: `disk-guard.sh status` green before work (`/fast/scratch/hyaku` use 26%, 600.0G free;
`/tmp` 14% 111.2G; `/var/tmp` 38%). No pacman, no installs, so no tool/version/channel record owed.

## Pins (every number below is re-derivable from these)

| Item | Value |
|---|---|
| Lane repo | `/home/vgpnk/Projects/shokunin/mori-shokunin` |
| Lane HEAD at measurement (unmoved before and after all runs) | `b3c256138f00c704d5aa56eb0332d74506502ef2` |
| Entering revision (contract) | `ddfb12fb0838b4307c445194a844f0c4b1950195` |
| Freeze revision (contract) | `ac496c7cde8cad965079858accae3bedfe4a73f2` |
| C1 data-landing commit | `398d32252d5495f362c4e7d66b5dd48426dca0bc` ("round-60: land C1 data …") |
| r59 data revision (frozen) | `7b86704d7c0754a09958d131b64dbfa2a6d3eaed` |
| `count-c1.py` sha256 | `795c1f3193a76406a40561ac60fedb3eee75fc38df2b2efb3fc5295d617ddbae` |
| `count-c2.py` sha256 | `8c4814f54c564a7f00beec5249de092a2d3b2c4043e07be773d80e8e3ccdf976` |
| `count-c3.py` sha256 | `fabde06c9d0a94a8487e5de45be3e413f6084816fb0507a71fd335bad5153514` |
| `tools/mori-entry-claims-check.py` sha256 | `cffe9f3359097277a7ea39729309efdc5831a1738994ceb30ee023ac0eae6e69` |
| Scratch | `/fast/scratch/hyaku/mori-r60/Mo60Executor54` (TMPDIR=…, `--scratch` per run; 27M peak, cleaned) |

Pin check against the contract: `count-c1` `795c1f31…617ddbae` = contract `795c1f31…ddbae`;
`count-c2` `8c4814f5…ccdf976` = contract `8c4814f5…df976`; entry-claims tool
`cffe9f33…ac0eae6e69` = contract `cffe9f33…e6e69`. `count-c3.py:51-52` also pins those exact
two counter shas (`PIN_C1`, `PIN_C2`), so the post-freeze data landing did **not** move any
instrument byte: for all four instruments `git show HEAD:<path>` sha256 == on-disk sha256
(`SAME` for all four, measured after the runs).

## Command 1 — count-c1 at the lane tip (the seat ask)

Run from the lane root, contract counting command form, HEAD resolved by `git rev-parse`:

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin
TMPDIR=/fast/scratch/hyaku/mori-r60/Mo60Executor54 \
python3 .ufo/waves/round-60/count-c1.py b3c256138f00c704d5aa56eb0332d74506502ef2 \
        --scratch /fast/scratch/hyaku/mori-r60/Mo60Executor54/c1-tip
```

Output, verbatim, one line; **exit status 0**:

```text
C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=b3c256138f00c704d5aa56eb0332d74506502ef2
```

This is byte-for-byte the contract's frozen target output
(`C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=R`, exit 0) with `R` bound
to the tip.

## Command 2 — repeat at the same tip (determinism / race check)

```
TMPDIR=… python3 .ufo/waves/round-60/count-c1.py b3c256138f00c704d5aa56eb0332d74506502ef2 \
        --scratch …/c1-tip-repeat
```

Output identical to Command 1 (same 5-field line, same `rev`); **exit 0**. `git rev-parse HEAD`
before and after all runs = `b3c25613…`, so the lane did not move under the measurement.

Independent corroboration already on disk: the pre-existing untracked file
`.ufo/waves/round-60/evidence/c1-at-data.txt` (not written by this seat) contains exactly the
same line, and I did not create or modify it.

## Command 3 — selftest (contract expects `pass=6 fail=0`, exit 0)

```
python3 .ufo/waves/round-60/count-c1.py --selftest
C1_SELFTEST pass=6 fail=0        # exit 0
```

## Command 4 — do-nothing control at the entering revision (falsification that the arms are non-vacuous)

```
python3 .ufo/waves/round-60/count-c1.py ddfb12fb0838b4307c445194a844f0c4b1950195 --scratch …/c1-control
```

Output, verbatim; **exit status 1** (contract §9 control for C1):

```text
C1=unmet dead-uncorrected=2 receipts=0/2 absent-set=0/5 lesson=absent rev=ddfb12fb0838b4307c445194a844f0c4b1950195 failed=absent_set=0/5,absent_table_absent,correction_incomplete,dead=2,lesson_absent,receipt_absent:.ufo/waves/round-60/evidence/r59-c1-met.txt,receipt_absent:.ufo/waves/round-60/evidence/r59-c2-met.txt,receipts=0/2
```

The five contract fields match the frozen control (`dead-uncorrected=2 receipts=0/2
absent-set=0/5 lesson=absent`, rc 1); the ` failed=` member is the counter's unmet-only suffix.
This shows the DEAD-NAME arm is not vacuous — it counts the two real dead-name occurrences that
existed at entering — and that the RECEIPTS/ABSENT-SET/LESSON arms go from 0 to full only
because the data landed.

## Command 5 — same counter at the C1 data-landing commit

```
python3 .ufo/waves/round-60/count-c1.py 398d32252d5495f362c4e7d66b5dd48426dca0bc --scratch …/c1-datarev
C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=398d32252d5495f362c4e7d66b5dd48426dca0bc
# exit 0
```

So C1 flips met at `398d3225` itself; the later tip `b3c25613` (which only moved S561–S564 rows
into the Registry table for a census E12 fix) keeps it met.

## Independent re-derivation of the RECEIPTS arm (not via the counter's own comparison)

Materialized the r59 counters from the pinned blob at `7b86704d` into scratch, ran each with
`--repo <lane> --scratch <scratch>`, and `cmp`-ed stdout against the committed receipt blob at
HEAD:

| Receipt (at HEAD) | Fresh re-run rc | `cmp` vs receipt | Receipt line |
|---|---|---|---|
| `.ufo/waves/round-60/evidence/r59-c1-met.txt` (sha256 `167c9fed…bcdee4`) | 0 | **0 = byte-equal** | `C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=7b86704d…` |
| `.ufo/waves/round-60/evidence/r59-c2-met.txt` (sha256 `4859d5ca…6caecb7`) | 0 | **0 = byte-equal** | `C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 rev=7b86704d…` |

Both re-runs exit 0, which is the contract's own requirement.

## Arm inventories (direct reads, same revisions)

DEAD-NAME arm at tip (`git show HEAD:SCORECARD.md`):

- lines containing `c1-entering.txt`/`c2-entering.txt`: **2** (lines 2950, 2951) — exactly the two
  C1/C2 rows; of those, lines **outside** the `r60-correction:` marker: **0**.
- both corrected lines carry the marker **and** the real pointer
  (`.ufo/waves/round-59/evidence/control-c1-do-nothing.txt` on 2950,
  `…control-c2-do-nothing.txt` on 2951).
- both real pointer blobs exist at tip: `git cat-file -e HEAD:.ufo/waves/round-59/evidence/control-c{1,2}-do-nothing.txt` → present.

ABSENT-SET arm truth matrix, `git cat-file -e <rev>:.ufo/waves/round-59/w1/<name>.md` — all five
frozen names are absent at `7b86704d` and present at tip, i.e. disposition `late-committed` for
all five; `.ufo/waves/round-60/evidence/r59-absent-set.md` (sha256 `0f881eb9…6650b24`) states
exactly that, including the nuance that Critic29/Reviewer16 were committed pre-filing in
`bf6c0ad3` while still absent at the data revision.

LESSON arm: `corpus/lessons/round-60.md` exists at tip and names each frozen name with the
required binding — `Mo59Critic29` l.50 / `Mo59Reviewer16` l.53 (`supersedes`, r59 claim wrong),
`Mo59MutationTester32` l.55-56 (`f091bd77` on the continuation line), `Mo59Executor40` l.58
(`f091bd77`), `Mo59MutationTester31` l.59 (`f091bd77`), plus heading l.44
`## Round-59 absent-set correction (supersedes round-59)` for the literal
`supersedes round-59`.

Read-only proof: after every run, `git status --porcelain` shows only the pre-existing untracked
entries (`evidence/c1-at-data.txt`, `w1.ready`, `w1.ready.dispatched`, `w1/`); no tracked file
modified, no commit made, HEAD unchanged.

## Findings

1. **C1 is met at the current lane tip** `b3c25613…`: exact line
   `C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=b3c256138f00c704d5aa56eb0332d74506502ef2`,
   rc 0. The line equals the contract's frozen target with `R` bound.
2. **The data landed in this wave**, at `398d3225`, and C1 already reads met at that commit; the
   tip commit `b3c25613` does not disturb it (both revisions measured, both met, rc 0).
3. **The instrument bytes are the frozen bytes**: `count-c1` sha `795c1f31…617ddbae` (pinned),
   `count-c2` `8c4814f5…ccdf976` (pinned), entry-claims tool `cffe9f33…6e69` (pinned),
   `count-c3` `fabde06c…` with `PIN_C1`/`PIN_C2` matching. On-disk and HEAD blobs are identical,
   so the met result is not a dirty-worktree artefact.
4. **The control still falsifies**: at `ddfb12fb` the same counter returns the frozen unmet line
   with `dead-uncorrected=2` and rc 1 — the dead-name arm is exercised, not vacuous.
5. **Receipts reproduce independently**: both r59 receipts byte-equal fresh revision-pinned
   re-runs at `7b86704d`, re-runs exit 0.
6. **Selftest** `C1_SELFTEST pass=6 fail=0`, rc 0, as the contract requires.

## Observations (advisory, code-read — not exercised, out of this seat's probe scope)

Recorded for the C1 reviewer/critic seats, not asserted as a claim failure; the current data
passes anyway:

- `count-c1.py:228` — for late-committed names the lesson check is two global predicates
  (`name in lt` and `R59_LANDING[:8] in lt`), so a lesson naming a name in one place and
  `f091bd77` in another place would pass without per-name binding. The real lesson binds
  per line (l.55-59), so the present pass is genuine; the predicate is weaker than the contract
  sentence "every late-committed name with landing pointer `f091bd77`".
- `count-c1.py:81` — `dead_uncorrected` skips a whole line once the marker is present, so an
  unpointed stray dead name sharing a marker line would escape that arm; `corrected_lines_name_real`
  (`:88-96`) requires each (name, real pointer) pair on one marker line but does not forbid extras
  on the same line. At tip the accounting is exact (2 dead-name lines, both marker lines, 0
  outside), so this is latent only.

## Scope / non-actions

Read-only, single seat. No commits, no VCS mutation, no fixture repos, no subagent dispatch.
Nothing written outside this report and `/fast/scratch/hyaku/mori-r60/Mo60Executor54` (cleaned
before yielding; all quoted receipts are inlined above). No production files, corpus registry,
SCORECARD, LOG, lane VCS, fleet or sibling repo touched. Scratch was created with `mkdir -p`,
`TMPDIR` set there, `--scratch` passed to every counter invocation.

## Blockers / risks

None. Residual risk for the closing seat: the lane tip moved twice after entering
(`76904b21` → `398d3225` → `b3c25613`), so any later C1 re-derivation must name its revision —
this report pins `b3c25613…` and, as a cross-check, `398d3225…`; both met.
