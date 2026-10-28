# Mo60Reviewer14 — C1 do-nothing control replay (round 60, w1)

Seat scope: replay `count-c1.py` at entering revision
`ddfb12fb0838b4307c445194a844f0c4b1950195` and byte-compare with
`.ufo/waves/round-60/evidence/control-c1-do-nothing.txt` (line and exit 1).
Read-only; freeze `ac496c7cde8cad965079858accae3bedfe4a73f2`.

## Verdict

**PASS — control reproduces byte-for-byte with exit 1; no defect found in
scope.** All four failing arms were independently re-derived from git truth at
the entering revision, so the control is not vacuous.

## Pin integrity (before running)

Commands run from the lane repo, read-only:

```
git show ac496c7c...:.ufo/waves/round-60/count-c1.py | sha256sum
  -> 795c1f3193a76406a40561ac60fedb3eee75fc38df2b2efb3fc5295d617ddbae
sha256sum .ufo/waves/round-60/count-c1.py
  -> 795c1f3193a76406a40561ac60fedb3eee75fc38df2b2efb3fc5295d617ddbae
```

Counter bytes at the freeze revision equal the worktree bytes and the
contract's pin (`795c1f31…ddbae`, count-c1 kill rule). The 331-byte control
evidence is likewise identical at freeze, at current tip
`b3c256138f00c704d5aa56eb0332d74506502ef2` (blob `a3f1a364…`), and in the
worktree: sha256 `b95a788ee1c439da92f02a3b6fe58501473eb8a7b69a830df7426364a45014a0`.
It is tracked and unmodified (`git diff` empty). Because the lane tip was
moving during w1 (untracked `evidence/c1-at-data.txt` appeared, rev
`b3c2561…`), the replay used the *freeze-pinned* counter bytes materialized
into seat scratch, never the worktree file.

## Replay

```
S=/fast/scratch/hyaku/mori-r60/Mo60Reviewer14   # TMPDIR="$S/tmp"
python3 "$S/count-c1-pinned.py" ddfb12fb0838b4307c445194a844f0c4b1950195 \
  --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch "$S/run-c1"
exit=1 ; stderr = 0 bytes
```

stdout (331 bytes, byte-identical to the committed control, `cmp -s` →
`BYTE-EQUAL`; sha256 both `b95a788e…5014a0`):

```
C1=unmet dead-uncorrected=2 receipts=0/2 absent-set=0/5 lesson=absent rev=ddfb12fb0838b4307c445194a844f0c4b1950195 failed=absent_set=0/5,absent_table_absent,correction_incomplete,dead=2,lesson_absent,receipt_absent:.ufo/waves/round-60/evidence/r59-c1-met.txt,receipt_absent:.ufo/waves/round-60/evidence/r59-c2-met.txt,receipts=0/2
```

This matches the contract's §9 control sentence exactly (`C1=unmet
dead-uncorrected=2 receipts=0/2 absent-set=0/5 lesson=absent`, exit 1).

Reproducibility checks:
- second run, different scratch dir (`--scratch "$S/run-c1b"`): exit 1,
  `BYTE-EQUAL`;
- documented usage from the lane root with default `--repo .`
  (`TMPDIR` set to an existing dir, `count-c1.py ddfb12fb…`): exit 1,
  `BYTE-EQUAL`, stderr 0. (An earlier 654-byte traceback was my harness
  pointing `TMPDIR` at a non-existent dir — `tempfile.mkdtemp` needs it to
  exist; not a counter defect.)
- pinned counter `--selftest`: `C1_SELFTEST pass=6 fail=0`, exit 0.

## Independent re-derivation of every failing arm at `ddfb12fb…`

| Arm | Counter token | Independent check |
|---|---|---|
| rev valid / SCORECARD readable | (no `scorecard_absent`) | `git cat-file -e ddfb12fb…` and `…:SCORECARD.md` both succeed |
| DEAD-NAME ARM | `dead=2` | SCORECARD at E has exactly 1 line each naming `c1-entering.txt` and `c2-entering.txt`, both without `r60-correction:` |
| correction marker arm | `correction_incomplete` | no `r60-correction:` line exists at E (expected pre-fix) |
| RECEIPTS ARM | `receipts=0/2` + 2× `receipt_absent:` | `git cat-file -e E:.ufo/waves/round-60/evidence/r59-c{1,2}-met.txt` → both absent |
| ABSENT-SET ARM | `absent-set=0/5`, `absent_table_absent` | `git cat-file -e E:.ufo/waves/round-60/evidence/r59-absent-set.md` → absent |
| LESSON ARM | `lesson=absent` | `git cat-file -e E:corpus/lessons/round-60.md` → absent |

So the control reaches a real pre-fix state, not a broken-revision state: the
counter's arms fail for the reasons the fix addresses, which is the contract's
"surface a do-nothing control cannot reach" requirement.

## Execution boundary / side effects

- The RECEIPTS arm short-circuits before `rerun_receipt`
  (`count-c1.py:121-141`), so no r59 counter blob is materialized or executed
  in the control run: `run-c1/` and `run-c1b/` are empty (0 entries). This
  matches the contract's G1-structural note for count-c1.
- No mutation of the lane: `git status --porcelain` after the run shows only
  the pre-existing untracked wave files (`evidence/c1-at-data.txt`,
  `w1.ready*`, `w1/`), none produced by this seat.
- Pinned counter carries no absolute host path (grep for `/home/`, `/fast/`,
  `/tmp/`, `/var/tmp/` → none), consistent with the 2026-10-26 reflection item.
- Met path stays revision-pinned: `measure` (`count-c1.py:143`) reads via
  `git_show`/`git cat-file -e` at the named rev, and the r59 counter
  materialized at `R59_DATA` (`count-c1.py:48`) itself reads through
  `git_show`/`materialize` (`count-c1.py:77-89` of the r59 counter), so
  `--repo .` working-tree drift cannot leak into a re-run.

## Line pointers (frozen counter bytes, sha `795c1f31…ddbae`)

- `dead_uncorrected` — `count-c1.py:77`
- `corrected_lines_name_real` — `count-c1.py:88`
- `rerun_receipt` (short-circuits on absent receipt) — `count-c1.py:121`
- `measure` — `count-c1.py:143`; `absent_set` append — `:211`
- `selftest` — `count-c1.py:240`
- `main`, line assembly, exit code — `count-c1.py:276`, `:296`, `:303`

## Observations (non-findings)

1. `failed=` carries both `absent_table_absent` and `absent_set=0/5` when the
   table is missing — redundant but intentional given the frozen 331-byte
   evidence; no change proposed (kill rule freezes counter bytes).
2. When `--scratch` is omitted the counter leaves its `mkdtemp` dir behind
   under `TMPDIR`; hygiene nicety only, outside the frozen output contract.
3. Untracked `evidence/c1-at-data.txt` (rev `b3c2561…`, `C1=met`) exists at the
   lane tip and is not part of the committed evidence set; the C1 after-state
   still requires the committed receipts/absent-set/lesson at R. Flagged for
   the L1/other seats, unverified here (outside this seat's scope).

## Residual risk / verification gaps

- I did not replay the *met* path (post-fix revision) — that is other seats'
  scope; this seat verifies only that the control discriminates and reproduces.
- The control's rev token is part of the bytes, so reproduction requires
  passing exactly `ddfb12fb…`; verified.
- Free space at run time: `/fast/scratch/hyaku` 26% used, 600G free; disk guard
  green. No ENOSPC encountered.
- Tools installed/updated: none.
