# Mo60Reviewer09 — receipts arm (C1): r59 counters re-run at `7b86704d`

**Seat:** Mo60Reviewer09 (leaf reviewer, no subagents). **Scope:** receipts arm only —
re-run the committed r59 counters at the frozen r59 data revision and byte-compare each
stdout with the committed receipts. Read-only on the lane; no commits, no VCS mutation,
no fleet/sibling writes.

**Revision pins used for every derivation**

| role | revision |
|---|---|
| frozen contract / amended freeze | `ac496c7cde8cad965079858accae3bedfe4a73f2` |
| entering revision | `ddfb12fb0838b4307c445194a844f0c4b1950195` |
| r59 data revision (`R59_DATA`) | `7b86704d7c0754a09958d131b64dbfa2a6d3eaed` |
| lane tip `R` at review time | `b3c256138f00c704d5aa56eb0332d74506502ef2` |
| receipt landing commit | `398d3225` |

Lane tip moved during the wave as expected (`398d3225` landed C1 data, `b3c25613` moved the
S561–S564 rows). Every read below is either a pinned `git show`/`git cat-file`/`git ls-tree`
or a fresh run of a counter materialized **from a pinned revision**, so the moving worktree
cannot influence any result.

---

## Verdict

**Receipts arm: PASS — 2/2 receipts byte-equal to fresh re-runs at `7b86704d`, both re-runs
exit 0.** No blocking finding. Three low/informational observations, none of which touches
the scored predicate.

---

## Evidence — the assigned check

Counters materialized with
`git show 7b86704d7c0754a09958d131b64dbfa2a6d3eaed:.ufo/waves/round-59/count-c{1,2}.py`
into `$HYAKU_SCRATCH/mori-r60/Mo60Reviewer09/`, `chmod +x`, `TMPDIR` set to that scratch,
`--scratch` a fresh directory per run, run from the scratch cwd so no relative path can
reach the lane:

```
python3 r59-count-c1.py 7b86704d… --repo <lane> --fleet <fleet> --scratch <scratch>/scratch-c1
python3 r59-count-c2.py 7b86704d… --repo <lane>                  --scratch <scratch>/scratch-c2
```

| arm | counter | rc | fresh stdout | committed receipt | cmp |
|---|---|---|---|---|---|
| C1 | `.ufo/waves/round-59/count-c1.py` (blob `251d4de216c7`) | **0** | `C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=7b86704d…` | `.ufo/waves/round-60/evidence/r59-c1-met.txt` | **identical** |
| C2 | `.ufo/waves/round-59/count-c2.py` (blob `260ac526c5bc`) | **0** | `C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 rev=7b86704d…` | `.ufo/waves/round-60/evidence/r59-c2-met.txt` | **identical** |

sha256 of the fresh stdout equals sha256 of the **committed blob** (not merely the worktree
copy — both were compared, and `git hash-object evidence/…` equals
`git rev-parse HEAD:evidence/…` for both files):

```
167c9fed65ce5bd5aef6b3487d07f25eae237fd073a003877668e67a79bcdee4  r59-c1-met.txt   (96 B, ends 0a)
4859d5ca7226aad23ab97b537b6c75ca1c73449ba7fc98211079cc2fb6caecb7  r59-c2-met.txt  (141 B, ends 0a)
```

`git show HEAD:.ufo/waves/round-60/evidence/r59-c1-met.txt | sha256sum` and
`…r59-c2-met.txt | sha256sum` reproduce those two digests exactly. Each receipt is a
single line (line 1) and a complete stdout — byte equality rules out truncation, extra
tokens or a hand-edited stamp.

**Receipt existence at `R`:** present at `398d3225` and at `b3c25613`
(blobs `85615ab4cf87…`, `8e7305be62ab…`); absent at `ac496c7c` and at the entering
`ddfb12fb`. That is the intended "landed during the wave" shape, and it means the receipts
arm is a genuinely post-freeze delta rather than a pre-seeded file.

**Counter identity:** `count-c1.py`/`count-c2.py` blobs are byte-identical at
`7b86704d`, `bf6c0ad3`, `f091bd77`, `a86e5f83`, `ddfb12fb`, `ac496c7c`, `b3c25613`
(`git log 7b86704d..HEAD -- <both paths>` is empty), so "the committed r59 counter" and
"the counter at the data revision" are the same bytes. The `rev=` field is bound implicitly
and soundly: `rerun_receipt` compares the **whole stdout**, and the counter echoes
`R59_DATA` into that line, so a receipt carrying any other revision cannot byte-match.

**Pinned tools match their PINs at `7b86704d`:**

```
tools/mori-register-check.py     38b733d896f880f5b7ecb464848b80798810ab052fcf0a8afb320918151472b8  == PIN (r59 c1)
tools/mori-settlement-scan.py    4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9  == PIN (r59 c2)
```

**Determinism:** three independent runs per counter with three *different* fresh `--scratch`
directories produced byte-identical stdout each time (`cmp` clean, rc 0). No timestamp,
host path or scratch path leaks into the output line.

**Read-only audit of the counters:** the only git invocations are `show`, `ls-tree` and
`cat-file` (`r59-count-c1.py:60,124,145,189`; `r59-count-c2.py:96,320,336`). Every write
target is under `--scratch` (`r59-count-c1.py:86-87,93,106,142-144,176-180`;
`r59-count-c2.py:195,206,229-230,256-257,293-294,335,344-345`). Running them cannot mutate
the lane, the corpus or the fleet.

---

## Gate-can-fail controls (the receipts are not a constant)

A receipt that reproduces is worthless if the counter prints `met` unconditionally, so I
ran the same counters at adjacent revisions:

| revision | counter | rc | output |
|---|---|---|---|
| `be737211` = `7b86704d^` | c2 | **1** | `C2=unmet selftest=ok scan=ok drift=ok trees=ok **entry=bad** rows=ok pins=ok tree=ok **claims=14 files=7** rev=be737211 failed=entry` |
| `be737211` = `7b86704d^` | c1 | 0 | `C1=met … rev=be737211` |
| `2b9f0397` (pre-r59-freeze) | c1 | **1** | `C1=unmet … failed=tool_absent,selftest,fixtures_absent,real,pointers` |
| `2b9f0397` | c2 | **1** | `C2=unmet … failed=copy_absent:…(6),drift,entry_absent,scan,selftest,tool_absent,tree,trees,trees_absent` |

The `be737211` row is the sharpest control: it is exactly the defect `7b86704d` corrected —
at the parent, `K11` was still a claim citing `corpus/evidence/sources-r59/w1-results-r53.json`,
a file outside the frozen `ARTIFACTS` set, so `claims=14 files=7` and the entry arm fails on
`files:outside`. `7b86704d` demotes that claim to prose (the diff shows the `- **K11** …`
line removed and folded into prose), restoring `claims=13 files=6` and `entry=ok`. So the
C2 receipt is **revision-discriminating against its own parent**, and the `claims=13 files=6`
in the receipt is load-bearing, not decorative.

---

## Corroboration of the scoring counter (`count-c1.py` receipts token)

The r60 counter's receipts arm (`count-c1.py:121-139`) materializes the r59 counter from
`R59_DATA` (`:123`), runs it with `sys.executable` and `--repo <resolved lane> --scratch …`
(`:131-133`), requires `returncode == 0` (`:136`) and `p.stdout == receipt_bytes` (`:138`),
via the loop at `:165-177`. That is the same comparison I performed independently.

```
$ python3 .ufo/waves/round-60/count-c1.py b3c25613 --scratch …
C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=b3c25613      rc=0
```

This equals the contract's frozen target output
(`C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=R`) with `R` = the
invoked revision, and confirms `receipts=2/2` from the receipt bytes themselves.

Do-nothing control reproduced byte-for-byte at the entering revision:

```
$ python3 .ufo/waves/round-60/count-c1.py ddfb12fb0838b4307c445194a844f0c4b1950195 --scratch …
C1=unmet dead-uncorrected=2 receipts=0/2 absent-set=0/5 lesson=absent rev=ddfb12fb… failed=absent_set=0/5,absent_table_absent,correction_incomplete,dead=2,lesson_absent,receipt_absent:…r59-c1-met.txt,receipt_absent:…r59-c2-met.txt,receipts=0/2
rc=1  →  cmp with evidence/control-c1-do-nothing.txt: IDENTICAL
```

`count-c1.py --selftest` → `C1_SELFTEST pass=6 fail=0`, rc 0; a second run at HEAD was
byte-identical (no run-to-run drift in the receipts arm).

Kill-rule spot check (bytes frozen since the amended freeze): `git log ac496c7c..HEAD --
contract.md count-c1.py` is empty; blobs are `b4bb16c833c2…` (contract) and
`54a38e13e73c…` (count-c1) at **both** `ac496c7c` and `HEAD`.

---

## Findings by severity

### Blocking
None.

### Low

**L1 — the receipts arm is not hermetic with respect to the fleet root; `count-c1.py`
delegates to an r59 counter that hardcodes it.**
`r59-count-c1.py:246-247` defaults `repo = "/home/vgpnk/Projects/shokunin/mori-shokunin"`
and `fleet = "/home/vgpnk/Projects/shokunin"` (both overridable by `--repo`/`--fleet`).
`count-c1.py:131-133` passes `--repo` and `--scratch` but **not** `--fleet`, so the c1
receipt re-run resolves `MANIFEST.json` at the pinned `MANIFEST_REV` through the hardcoded
host path. Probe:

```
$ python3 r59-count-c1.py 7b86704d --repo <lane> --fleet /nonexistent/fleet --scratch …
C1=unmet selftest=ok fixtures=ok real=bad pointers=bad rev=7b86704d failed=manifest,real,pointers   rc=1
```

So the receipt is location-dependent: it is correct **on this host**, and the predicate
("byte-equals a fresh re-run at `7b86704d`") is satisfied there, but the
"no r60 instrument carries an absolute host path" property holds only for r60 code bytes —
the arm inherits one at runtime through delegation. Fix is one line: pass
`--fleet str(Path(repo).resolve().parent)` in `rerun_receipt`. Not a predicate violation;
recorded because the contract's absolute-path item is otherwise claimed by construction.

### Informational

**I1 — c1 is not discriminating at `7b86704d^`.** `C1=met … rev=be737211` with every token
identical apart from the echoed revision. This is expected — `7b86704d` touches only the
C2 entry (`git show --stat` reports 1 file, `wave-settlement-artifacts-r59.md`) — and c1's
ability to fail is independently shown at `2b9f0397` (`tool_absent`). Recorded only so no
reader mistakes the c1 receipt for a revision-sensitive artifact: its discriminating power
against this particular delta is nil.

**I2 — `--scratch`/`--repo` value parsing is unbounded.** `r59-count-c1.py:257` and
`r59-count-c2.py:445` advance `i += 2` without checking that a value follows, so a trailing
`--scratch` raises `IndexError` instead of exiting 2. Unreachable from the scored path
(`count-c1.py:131-133` always supplies values); robustness only.

**I3 — absolute host paths in the r59 counters.** `r59-count-c1.py:246-247`,
`r59-count-c2.py:437`. Same substance as L1, listed separately because these are the r59
bytes, not r60.

---

## Residual risk

- **R moves.** `receipts=2/2` is proven at `b3c25613`. The receipt blobs were still
  `85615ab4`/`8e7305be` there; if a later commit rewrites either receipt, the arm must be
  re-scored at that revision. I verified existence and byte values at `398d3225` and
  `b3c25613` only.
- The C2 receipt's stability depends on the r59 entry remaining frozen. It is anchored by
  `7b86704d`, so this is structural, not observational.
- L1 means a host relocation would silently degrade `receipts` to `1/2` (c1 only) rather
  than fail loudly at the delegation boundary. It would still fail closed (C1 `unmet`), so
  the risk is usability, not false-pass.

## Verification gaps

- I did **not** score the absent-set arm (`r59-absent-set.md` vs `git cat-file -e` truth),
  the SCORECARD dead-name/marker arm, or the `round-60.md` lesson arm. My `absent-set=5/5`
  and `lesson=ok` tokens are quoted from the counter's output, not independently
  re-derived — another seat owns them.
- I did **not** run `count-c2.py`/`count-c3.py` in r60, nor the G1/G2/G3 PoC replays.
- I did **not** run the r59 counters' own `--selftest` (the arm I re-ran exercises their
  `measure` path end-to-end and both gates demonstrably fail on adjacent revisions, which
  is stronger evidence than the selftest for this predicate).
- Tool availability was not an issue; nothing was installed or updated, so no tool
  record is due.

## Cleanup

All work under `$HYAKU_SCRATCH=/fast/scratch/hyaku`, seat root
`/fast/scratch/hyaku/mori-r60/Mo60Reviewer09/` (49 MB), removed after this report; no lane,
fleet or sibling path was written. Disk guard was green before and during the run
(`/tmp` 14 %, `/var/tmp` 38 %, `/fast/scratch/hyaku` 26 %). No pacman, no network install,
no fixture repo needed (no git write was required: every command was `show`/`ls-tree`/
`cat-file`).
