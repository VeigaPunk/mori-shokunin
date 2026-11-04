# Mo83E04Snap — C2 snapshot provenance binding (round 83, wave w1)

Seat: bind the round-82 drift classification to its committed raw snapshot.
Frozen authority: `.ufo/waves/round-83/contract.md` P-C2; grader `.ufo/waves/round-83/count-c2.py`.
Freeze commit `9075c72995095de97babb3d06e3f2d3b2f168062`; entering worktree tip `466d28bc229f13106e9fa1d3d65221b19a58e120`.

## What I changed (absolute paths)

1. `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/drift-classification-r82.txt` —
   added exactly three lines to the existing leading `#` header block (lines 6–8), before the
   first `DRIFT_CLASS` line; no `DRIFT_CLASS` line, no token, and no existing header line touched:
   ```
   # Snapshot: .ufo/waves/round-82/evidence/drift-r82-live.txt
   # Snapshot-sha256: 6091bc46cba5ef6e73f882f035f234d0ece023e6e12d98ca92368e2039bf9a5d
   # As-of: 2026-11-04T07:45:13Z
   ```
2. `/home/vgpnk/Projects/shokunin/mori-shokunin/SCORECARD.md` — `## Retired` row `drift-pin-r10`
   (line 60) now also names the snapshot path; every pre-existing word, the baseline path and the
   classification path are retained. The inserted span is
   `, bound to the committed raw snapshot `.ufo/waves/round-82/evidence/drift-r82-live.txt`,`
   between the classification path and ", graded by".
3. The `freshness` `## Axes` cell is byte-unchanged: it already carries `r10 pin retired` and
   `corpus/evidence/drift-classification-r82.txt` and does not contain `round-10 drift pin still
   red`, which is exactly the end state the seat spec and the counter require; the counter's
   `cell_state` grades only those three facts, so no edit was needed and none was made.

## Hash and as-of derivation (my own measurements)

```
$ sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/evidence/drift-r82-live.txt
6091bc46cba5ef6e73f882f035f234d0ece023e6e12d98ca92368e2039bf9a5d  .../drift-r82-live.txt
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 9075c72995095de97babb3d06e3f2d3b2f168062:.ufo/waves/round-82/evidence/drift-r82-live.txt | sha256sum
6091bc46cba5ef6e73f882f035f234d0ece023e6e12d98ca92368e2039bf9a5d  -        # file bytes == freeze-rev blob
$ grep -m1 '^# run-start:' .../drift-r82-live.txt
# run-start: 2026-11-04T07:45:13.552564+00:00
```
`2026-11-04T07:45:13.552564+00:00` normalized to UTC whole seconds (the counter's own
`run_start`: `fromisoformat` → `astimezone(utc)` → `%Y-%m-%dT%H:%M:%SZ`) = `2026-11-04T07:45:13Z`.

## Commands run and outputs

Entering control (committed bytes; my worktree edits are not yet a commit — this is the control
and it held at every point while I edited):

```
$ python3 -I .ufo/waves/round-83/count-c2.py 9075c72995095de97babb3d06e3f2d3b2f168062 --scratch $S/ct
C2=unmet snapshot=absent tokens=0 agreed=0 residual=0 live=unavailable rev=9075c7299509   rc=1
$ python3 -I .ufo/waves/round-83/count-c2.py 466d28bc229f13106e9fa1d3d65221b19a58e120 --scratch $S/ct
C2=unmet snapshot=absent tokens=0 agreed=0 residual=0 live=unavailable rev=466d28bc229f   rc=1
```

Counter selftest: `C2_COUNTER_SELFTEST pass=10 fail=0`, rc 0 (scratch under
`/fast/scratch/hyaku/mori-r83/Mo83E04Snap/ct`).

Pre-verification that these exact bytes grade met, without committing in the lane: fixture at
`/fast/scratch/hyaku/mori-r83/Mo83E04Snap/fixture` = `git archive 9075c729 | tar -x` + my two
edited worktree files; `git init -q`; asserted `git -C "$D" rev-parse --show-toplevel` == `$D`;
single throwaway-identity commit; then

```
$ python3 -I .ufo/waves/round-83/count-c2.py HEAD --repo <fixture> --scratch <mine> \
      --fleet-root /home/vgpnk/Projects/shokunin
C2=met snapshot=bound asof=1 tokens=64 agreed=64 residual=0 live=derived live_tokens=64 live_agree=64 rev=45b7c668e17f
rc=0
```

The live re-derivation in that run is a real census run at the fleet root (`MORI_DRIFT:` list,
exit 1): measured `live_tokens=64`, `live_agree=64` — an observation recorded as measured, and it
happens to equal the frozen target.

## What I verified / could not verify

- Verified: header parse (one each of the three lines inside the leading `#` block), hash equality
  file-vs-blob, as-of equality with the counter's own normalization, retired row contains all
  three paths, freshness cell facts unchanged, selftest green, fixture-grade `met` with 64/64.
- Not verifiable by this seat: the lane-revision `C2=met` reading itself — it exists only after
  the L1 commits these worktree bytes; the counter grades `git show <rev>:…` exclusively. The
  fixture run is byte-faithful (archived freeze tree + verbatim copies) but is not a lane commit.
- Snapshot file `.ufo/waves/round-82/evidence/drift-r82-live.txt`: never edited (byte-unchanged,
  hash re-read identical after edits).

## Defects in other seats' bytes

None observed. Other seats' in-flight worktree changes were visible (`corpus/QUALITY.md`,
`corpus/SOURCES.md` modified; untracked round-83 paths) and were not touched, read in depth, or
judged here.

## Tooling / hygiene

No tool installed or upgraded; no pacman transaction; no mutating git/jj command anywhere (the
only commits were inside the disposable fixture); scratch `/fast/scratch/hyaku/mori-r83/Mo83E04Snap`
deleted before yield; no subagent spawned.
