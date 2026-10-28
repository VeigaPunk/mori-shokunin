# Mo60Reviewer15 — C2/C3 do-nothing control replay at the entering revision (round 60, w1)

Seat scope: replay `count-c2.py` and `count-c3.py` at entering revision
`ddfb12fb0838b4307c445194a844f0c4b1950195`, confirm both are `unmet`, and confirm the
`failed=` token sets match `.ufo/waves/round-60/evidence/control-c2-do-nothing.txt` and
`control-c3-do-nothing.txt` (modulo `rev=`). Read-only review; no lane/VCS/fleet writes.

## Verdict

**CONFIRMED.** Both do-nothing controls reproduce at `ddfb12fb…` **byte-for-byte modulo the
rev token**, with identical `failed=` token sets, exit 1. The same frozen instrument bytes
report `met` at the freeze revision `ac496c7c…` and reproduce the committed at-freeze
receipts byte-exactly, so the `unmet` readings are discriminating, not a broken counter.

## Pinned inputs (no unpinned working-tree read)

| Item | Value |
|---|---|
| Entering rev | `ddfb12fb0838b4307c445194a844f0c4b1950195` (`git rev-parse` identical; ancestor of tip `b3c25613`) |
| Freeze rev | `ac496c7cde8cad965079858accae3bedfe4a73f2` |
| `count-c1.py` (freeze, = tip, = PIN_C1) | `795c1f3193a76406a40561ac60fedb3eee75fc38df2b2efb3fc5295d617ddbae` |
| `count-c2.py` (freeze, = tip, = PIN_C2) | `8c4814f54c564a7f00beec5249de092a2d3b2c4043e07be773d80e8e3ccdf976` |
| `count-c3.py` (freeze, = tip) | `fabde06c9d0a94a8487e5de45be3e413f6084816fb0507a71fd335bad5153514` |
| `contract.md` (freeze, = tip) | `a444e270957b957875b667b3cd226b965234deda242db12a81df597e2c15441d` |
| `evidence/control-c2-do-nothing.txt` (committed at freeze; = worktree) | `625a912156c5f4811bff3b3b4558a2796e844bcfc61e6cd1b578b70e3a9d591f` |
| `evidence/control-c3-do-nothing.txt` (committed at freeze; = worktree) | `51152f0c262ae440811deb1ba218e758ac07c7d97332b2fdc5968618a48bd2aa` |

Counter bytes were extracted with `git -C <lane> show ac496c7c:.ufo/waves/round-60/count-cN.py`
into the seat scratch and executed from there. Working-tree/tip bytes are identical to the
freeze bytes for all three counters (sha table above), so the replay used the frozen
instruments, not a tip-drifted copy.

Scratch: `/fast/scratch/hyaku/mori-r60/Mo60Reviewer15` (created with `mkdir -p`, `TMPDIR`
pointed at it, `--scratch` passed explicitly). Disk guard checked before work: `/fast/scratch/hyaku`
26% used, 600.0G free (green).

## Commands and literal outputs

```sh
S=/fast/scratch/hyaku/mori-r60/Mo60Reviewer15; L=/home/vgpnk/Projects/shokunin/mori-shokunin
ENTER=ddfb12fb0838b4307c445194a844f0c4b1950195
git -C "$L" show ac496c7c:.ufo/waves/round-60/count-c2.py > "$S/count-c2.py.freeze"
git -C "$L" show ac496c7c:.ufo/waves/round-60/count-c3.py > "$S/count-c3.py.freeze"
TMPDIR="$S" python3 "$S/count-c2.py.freeze" "$ENTER" --repo "$L" --scratch "$S/c2run"
TMPDIR="$S" python3 "$S/count-c3.py.freeze" "$ENTER" --repo "$L" --scratch "$S/c3run"
```

Replay at `ddfb12fb…` (exit 1 for both):

```
C2=unmet selftest=bad scan=ok drift=ok trees=bad entry=bad rows=bad pins=bad tree=ok claims=0 files=0 spans=0 rev=ddfb12fb0838b4307c445194a844f0c4b1950195 failed=entry,pins,rows,selftest,tool_absent,trees,trees_set
C3=unmet toolgate=bad containment=bad expectgate=bad cases=1 rev=ddfb12fb0838b4307c445194a844f0c4b1950195 failed=count_c1_absent,count_c2_absent,g1_new_skipped,g2_skipped,g3_skipped
```

Committed evidence at the freeze commit (`git show ac496c7c:.ufo/waves/round-60/evidence/…`),
after substituting the rev token on both sides with `sed "s/$ENTER/REV/g"`:

```
diff -u ev-c2.mod out-c2.mod   ->  C2 evidence MATCH
diff -u ev-c3.mod out-c3.mod   ->  C3 evidence MATCH
```

Full-line equality (not just token sets) holds after the rev substitution; evidence and
replay are both 215 bytes (C2) and 182 bytes (C3).

## Token-set comparison (modulo rev)

| Control | Replay `failed=` | Evidence `failed=` | Identical | Symmetric difference |
|---|---|---|---|---|
| C2 | `entry,pins,rows,selftest,tool_absent,trees,trees_set` | same | **yes** | none |
| C3 | `count_c1_absent,count_c2_absent,g1_new_skipped,g2_skipped,g3_skipped` | same | **yes** | none |

Contract §C1/§C2/§C3 do-nothing expectations are met as written: C2 carries
`tool_absent,selftest,trees,trees_set`; C3 carries the exact five tokens with `cases=1`.

## Why the controls are real, not vacuous

State at `ddfb12fb…` (checked with `git -C "$L" cat-file -e "$ENTER:<path>"`):

- `tools/mori-entry-claims-check.py` **ABSENT** → `tool_absent`; the selftest, entry/rows/pins
  and per-tree arms are gated off (`count-c2.py:161-169`, `:183-190`, `:307`, `:378`).
- `.ufo/waves/round-60/trees-c2h` **ABSENT** → `trees_set` (`count-c2.py:345-355`).
- Entry payload is otherwise present at ENTER (`corpus/knowledge/wave-settlement-artifacts-r59.md`,
  `corpus/SOURCES.md`, all six `corpus/evidence/sources-r59/*` copies), so `entry=bad rows=bad
  pins=bad` derives solely from the missing pinned tool, not from missing inputs.
- `tools/mori-settlement-scan.py` **present and pinned at ENTER**, so `scan=ok drift=ok tree=ok`
  are genuinely exercised arms; the counter did real work and still could not reach `met`.
- `count-c1.py` / `count-c2.py` **ABSENT** at ENTER → `count_c1_absent,count_c2_absent`, which
  correctly skips G1-new/G2/G3 (`count-c3.py:140-146, 183, 202-203, 233-234`) and yields
  `cases=1` from the old-counter arm alone.
- Old-counter hole reproduced: the r59 counter materialized at `7b86704d…` executed the
  unpinned PoC blob and wrote
  `SCRATCH/c3run/g1-old/st2/EXEC-MARKER` with body
  `executed --selftest --scratch /fast/scratch/…/g1-old/st2` (`count-c3.py:186-199`).

Discrimination check — same frozen bytes, freeze rev:

```
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13 rev=ac496c7cde8cad965079858accae3bedfe4a73f2   (exit 0)
C3=met toolgate=ok containment=ok expectgate=ok cases=6 rev=ac496c7cde8cad965079858accae3bedfe4a73f2                                           (exit 0)
```

Both byte-equal the committed `evidence/c2-at-freeze.txt` / `c3-at-freeze.txt`. At freeze the
G1 gate is active: `c3freeze/g1-new` contains **0** entries (no EXEC-MARKER), while the old
arm again writes exactly one marker under `c3freeze/g1-old/st2`, so the toolgate token is a
real gate, not a constant.

Frozen-byte selftests also reproduce: `C2_SELFTEST pass=8 fail=0`, `C3_SELFTEST pass=3 fail=0`
(both exit 0).

## Isolation / determinism

- Second replay of both counters at ENTER with fresh scratch dirs: outputs byte-identical
  (`diff out-c2.txt out-c2b.txt`, `diff out-c3.txt out-c3b.txt` both clean).
- All lane reads go through `git show` / `ls-tree` / `cat-file`; the counters never read lane
  worktree files (only scratch materializations). `--repo` was passed as an absolute path.
- Fixture repos exist only under scratch and their `rev-parse --show-toplevel` equals the
  fixture path; at ENTER no `poc-expect` fixture is created, consistent with `g3_skipped`.
- No `EXEC-MARKER` anywhere in the lane; no `mori-r60-*` temp dirs appeared under `/tmp`
  (TMPDIR honored). Lane `git status --porcelain` shows only the pre-existing wave artifacts
  (`evidence/c1-at-data.txt`, `w1.ready*`, `w1/`) — the replay added nothing.
- Evidence files carry no absolute host paths or secrets (`grep -E '/(home|fast|tmp|var)/'`
  over both control receipts: none).

## Findings

Severity order. Nothing blocking; the controls hold as claimed.

1. **[informational, no verdict impact] `count-c2.py:209` dead condition.**
   `if not (ec_ok is not None and scan_ok_sha)` — `ec_ok` is a `bool` (line 162), so
   `ec_ok is not None` is always true; the scan arm is gated only by `scan_ok_sha`. This does
   not change any verdict: the scan tool is separately G1-gated in `run_pinned` with `PIN_SCAN`
   (`:212-213`) and `met` still requires `ec_ok` (`:410`). Observable effect at ENTER is
   `scan=ok drift=ok` while `tool_absent`, which is exactly the committed control line. Safe
   to leave; only relevant if counters are ever amended pre-data (post-freeze edits are
   invalidating by the kill rule).

2. **[informational] At-freeze receipts are latched one commit after the freeze.**
   `evidence/c2-at-freeze.txt` / `c3-at-freeze.txt` were introduced by dispatch commit
   `76904b21`, not inside freeze `ac496c7c`. They byte-reproduce from the freeze revision with
   the frozen bytes, so the provenance is sound; recorded only so the pointer is not mistaken
   for a freeze-commit artifact. Control receipts themselves are committed at the freeze
   commit (`4d036fb0`).

## Residual risk and verification gaps

- The C3 control at ENTER cannot exercise G1-new/G2/G3 by construction (the round-60 counters
  are absent there); those gates are evidenced only by the at-freeze `met` run replayed above.
- C1 was not re-derived (out of this seat's scope); C3's control only requires c1/c2 absence at
  ENTER, which was checked directly with `cat-file -e`.
- No residual risk found for the C2/C3 control claim: output identity is exact (full line, not
  only token set), deterministic across reruns, and discriminating at the freeze revision.
