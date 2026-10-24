# MutGateTiming — C3 timing-logic mutation probe

Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` (read-only; every run below is a read of
git history plus copies under scratch). Scored tip `f725f3076972e6e70595b5ac8279be524a111ff8`,
entering tip `e33bb561712b32f46861362a3fa43762fa70ae4f`, do-nothing control `e37dcc6`,
round base `f10a320d`. Scratch: `.ufo/waves/round-38/scratch/MutGateTiming/r38w2-200351/`.
Date: 2026-10-23.

## Verdict

**KILLED — PASS.** The primary mutation (presence-based classification) is killed by the frozen
stale-set at `e37dcc6` **and** by the selftest's `supersede before edit` fixture, and the lane
tool was never modified (hash unchanged before/after, `git status --porcelain tools/` empty).

## Mutation M1 (primary): presence-based classification

Smallest behavior-bearing point: the per-id classification at
`tools/mori-sources-appendonly.py:284-289`, where the shipped gate requires
`landing > last_edit[cid]` (the superseding row's first landing commit must be a descendant of the
id's last immutable edit). The mutant treats presence alone as discharge, ignoring commit order.

Diff against the byte-identical pristine copy (`gate-pristine.py` → `gate-m1.py`):

```diff
--- gate-pristine.py
+++ gate-m1.py
@@ -283,7 +283,1 @@
     for cid in superseded:
-        landing = supersede_landing[cid][0]
-        if cid in last_edit and landing > last_edit[cid]:
-            superseded_as_of.append(cid)
-        else:
-            stale_supersede.append(cid)
+        superseded_as_of.append(cid)   # mutant M1: presence alone discharges
```

sha256 `gate-m1.py` = `e31237d38475f7f33b7d300445cb48440a3cd096dd9d1a6d521fa5bfe60af289`.

## Detector (same bounded commands on pristine / mutant / restored)

Run from the lane root so the copy reads the lane's history:

1. `python3 <gate> e37dcc6 --round-base f10a320d` — the final `supersede_timing` line is the
   frozen reading: `stale_supersede=[S069]` and S069 absent from `superseded_as_of`.
2. `python3 <gate> f725f3076972e6e70595b5ac8279be524a111ff8 --round-base f10a320d` — S069 in
   `superseded_as_of`, `stale_supersede=[]`, `changed S069 superseded_by=S226`.
3. `python3 <gate> --selftest` — exit 0, `pass=9 fail=0`.

Kill condition is the contract's C3 kill rule (contract.md "Kill rule"): a gate that derives the
field from row presence lists S069 in `superseded_as_of` at `e37dcc6`.

## Pristine (shipped lane bytes) — control

`python3 tools/mori-sources-appendonly.py e37dcc6 --round-base f10a320d` (exit 1, round_changed
non-empty):

```
supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] stale_supersede=[S069]
```

`python3 tools/mori-sources-appendonly.py f725f307… --round-base f10a320d` (exit 1):

```
changed S069 superseded_by=S226
supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] stale_supersede=[]
```

`python3 tools/mori-sources-appendonly.py --selftest` → exit 0,
`MORI_SOURCES_APPENDONLY_SELFTEST pass=9 fail=0`
(receipts: `shipped-e37dcc6.txt`, `shipped-tip.txt`, `shipped-selftest.txt`).

## Mutant M1 — actual outputs

`python3 gate-m1.py e37dcc6 --round-base f10a320d` (exit 1):

```
supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] stale_supersede=[]
```

**Yes: the mutation lists S069 in `superseded_as_of` at `e37dcc6`** and empties the stale set —
the exact defect class the contract predicts. `diff` against the shipped run differs on one
content line only (the timing line; `mutant-m1.diff`).

`python3 gate-m1.py f725f307… --round-base f10a320d` (exit 1): byte-identical to the shipped tip
run, timing line included (`stale_supersede=[]`, `changed S069 superseded_by=S226`). The mutant
is invisible at the scored tip; only the `e37dcc6` reading discriminates.

`python3 gate-m1.py --selftest` → **exit 1**:

```
FAIL supersede before edit: superseded_as_of: want [] got ['S001']; stale_supersede: want ['S001'] got []
MORI_SOURCES_APPENDONLY_SELFTEST pass=8 fail=1
```

Kill channels: (a) frozen stale-set at `e37dcc6` — expected `stale_supersede=[S069]`, got `[]`;
(b) selftest fixture `supersede before edit` — expects `stale_supersede=["S001"]`, got
`superseded_as_of=["S001"]`. Either suffices; both fired.

## Secondary M2: the lesson-M3 overwrite (`setdefault` → assignment)

Authorized alternate in the tasking ("the buggy `if index > previous[0]` overwrite quoted in
lesson M3", `corpus/lessons/round-38.md:27` — a landing index updated to the newest state instead
of the first landing). One line at `:254`:

```diff
-                supersede_rows.setdefault((m.group(1), cells[0].strip()), index)
+                supersede_rows[(m.group(1), cells[0].strip())] = index  # newest state, not first landing
```

sha256 `gate-m2.py` = `1bb53b8dd38bcf4ec75f13f6208db4aad70a741a5800b8b117be673c00c4dca5`.

- `e37dcc6` (exit 1): `superseded_as_of=[…,S069,…] stale_supersede=[]` — S069 listed as-of;
  **killed by the stale-set** (identical flip to M1 on the timing line).
- tip (exit 1): timing line equals the shipped one, but the per-id line regresses to
  `changed S069 superseded_by=S073` (shipped: `S226`) — second kill channel at the scored tip.
- `--selftest`: **exit 0, `pass=9 fail=0` — survives.** Coverage finding, not a contract change:
  the `supersede before edit` fixture is two-state (`with_old_superseder` then
  `old_superseder_then_edit`, `tools/mori-sources-appendonly.py:415-418`), so a newest-state
  overwrite that still lands *after* the edit index is not discriminated; lesson M3 states this
  ("the selftest fixture passed because it has only two states"). M2 is caught only by the
  lane-history reading — the stale-set at `e37dcc6` and the latest-superseder line at the tip.

## Restoration evidence

The lane tool was never edited; only byte-identical copies under my scratch were mutated.

| file | sha256 |
|---|---|
| lane `tools/mori-sources-appendonly.py` (before and after all runs) | `9a6164e391479bcc9e50487f9eabbc95d4f25d57793f77575d33f8520fdb09fa` |
| `gate-pristine.py` (copy, `cmp` identical to lane) | `9a6164e391479bcc9e50487f9eabbc95d4f25d57793f77575d33f8520fdb09fa` |
| `gate-restored.py` (re-copied after the probe) | `9a6164e391479bcc9e50487f9eabbc95d4f25d57793f77575d33f8520fdb09fa` |

Restored bytes re-run at `e37dcc6` reproduce the shipped output on every content line
(`diff` of `shipped-e37dcc6.txt` vs `restored-e37dcc6.txt` ignoring the header label: empty,
`RESTORED_CONTENT_DIFF=0`; `restored-e37dcc6.txt`). `git status --porcelain tools/` is empty and
`git diff --stat f725f307… -- tools/mori-sources-appendonly.py` is empty (`TIP_WORKTREE_DIFF=0`).

## Commit-order ground truth (re-derived)

- `git log -1 71abd41` → `2026-10-21T08:18:29-03:00` (S073's `supersedes S069` row lands here);
  `git log -1 62db24c` → `2026-10-22T23:55:24-03:00` (S069's in-place edit).
- `git merge-base --is-ancestor 71abd41 62db24c` → true (exit 0); reverse → false (exit 1).
  So the only superseder present at `e37dcc6` predates the edit → S069 is stale there.
- `git log --format='%h %cI' -S'supersedes S069' --reverse -- corpus/SOURCES.md` →
  `71abd41 2026-10-21…`, `daa1d4d 2026-10-23T17:55:25-03:00`. `daa1d4d` (S226) is a descendant
  of `62db24c` and an ancestor of the scored tip (`--is-ancestor` exit 0 both ways). That is why
  the maximum-across-superseders rule yields `superseded_by=S226` and `stale_supersede=[]` at
  the tip, and why the M2 tie collapses to S073 in insertion order.

## Cross-check against the frozen receipts

Live re-derivation matches the committed evidence: `evidence/gate-after-e37dcc6.txt:2` and
`evidence/gate-after.txt:22` are byte-identical to my timing lines above, and
`evidence/gate-selftest-after.txt` ends `pass=9 fail=0` matching my live selftest. Nothing was
read-only-trusted; each line above was produced by a command run in this seat.

## Tooling

No installs or upgrades; no network use. Tools used: system `python3`, `git`, `sha256sum`,
`diff` — all already present.

## Scratch inventory

`r38w2-200351/`: `gate-pristine.py`, `gate-m1.py`, `gate-m2.py`, `gate-restored.py`,
`mutant-m1.diff`, `mutant-m2.diff`, `shipped-e37dcc6.txt`, `shipped-tip.txt`,
`shipped-selftest.txt`, `m1-e37dcc6.txt`, `m1-tip.txt`, `m1-selftest.txt`, `m2-e37dcc6.txt`,
`m2-tip.txt`, `m2-selftest.txt`, `restored-e37dcc6.txt`. A dead wave-1 seat's earlier
`MutGateTiming/` files remain untouched and were not used as evidence.
