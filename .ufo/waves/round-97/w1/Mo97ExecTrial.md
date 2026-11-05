# Mo97ExecTrial — domain trial run of the four newly registered tools

Seat: Mo97ExecTrial (executor). Tree: `git archive e85ed91249953094b067554bfa79fcdc65791f8e`
extracted to scratch `$S=/fast/scratch/hyaku/mori-r97/Mo97ExecTrial/tree` (15,107 files).
All commands run from `cd "$S/tree"`, `TMPDIR="$S"`. Full outputs in `$S/out/`.
No tools installed or upgraded (python3 only). Own cgroup from `/proc/self/cgroup`:
`0::/user.slice/user-1000.slice/user@1000.service/app.slice/app-graphical.slice/app-Hyprland-xdg\x2dterminal\x2dexec-30b98c4e.scope`
(disk dir exists as `.../app-Hyprland-xdg\x2dterminal\x2dexec-30b98c4e.scope`, verified with `ls -d`).

## 1. mori-cgroup-pressure (row 1)

Cell (verdict): one JSON object (schema `mori-cgroup-pressure-v1`) then a
`MORI_CGROUP_PRESSURE:` verdict line · 0 -> ok or high-guarded · 1 -> high ·
2 -> partial or unavailable. Self-test cell: `--selftest` ->
`MORI_CGROUP_PRESSURE_SELFTEST: pass=12 fail=0`. Write scope: stdout only;
reads cgroupfs read-only, registers no PSI trigger; selftest output under
`--scratch` or TMPDIR.

Observed (default root):
```
$ TMPDIR="$S" python3 tools/mori-cgroup-pressure.py   # exit=0
{ ..., "root": "/sys/fs/cgroup", "schema": "mori-cgroup-pressure-v1", "verdict": "PRESSURE_OK" }
MORI_CGROUP_PRESSURE: PRESSURE_OK (group=user.slice ok=4 absent=0 unreadable=0 malformed=0 findings=0)
```
Observed (`--group` = own cgroup **without** leading slash):
```
$ python3 tools/mori-cgroup-pressure.py --group 'user.slice/user-1000.slice/user@1000.service/app.slice/app-graphical.slice/app-Hyprland-xdg\x2dterminal\x2dexec-30b98c4e.scope'  # exit=0
MORI_CGROUP_PRESSURE: PRESSURE_OK (group=user.slice/user-1000.slice/user@1000.service/app.slice/app-graphical.slice/app-Hyprland-xdg\x2dterminal\x2dexec-30b98c4e.scope ok=4 absent=0 unreadable=0 malformed=0 findings=0)
```
Caveat observed: `--group` **with** a leading slash produces `//user...` and
`PRESSURE_UNAVAILABLE` / exit=2 with `group_present=false` (enosnt against the
real cgroupfs path, which exists). I.e. the leading slash from `/proc/self/cgroup`
must be stripped before passing as `--group`. This is a usage/format caveat, not a
contradiction of the row's verdict map (`2 -> ... unavailable` matched the
unavailable verdict; `0 -> PRESSURE_OK` matched both valid runs).

Selftest:
```
$ TMPDIR="$S" python3 tools/mori-cgroup-pressure.py --selftest   # exit=0
... case threshold-low: pass ... case dup-some: pass
MORI_CGROUP_PRESSURE_SELFTEST: pass=12 fail=0
```
Matches the self-test cell exactly.

## 2. mori-drift-recheck (row 2)

Cell (verdict): per row `<id> fresh/excerpt/time-churn/... as-of=T`, then
`MORI_DRIFT_RECHECK rows=N adjudicated=D ... window=...` · 0 -> every considered
copy-bearing row carries a token · 1 -> any unresolved · 2 -> setup. Self-test
cell: `MORI_DRIFT_RECHECK_SELFTEST: PASS (10 cases)`. Write scope: stdout only;
read-only under DIR; fresh fetches held in memory.

Observed:
```
$ TMPDIR="$S" python3 tools/mori-drift-recheck.py --root "$S/tree" --only S615,S616,S623,S577   # exit=0
# MORI_DRIFT_RECHECK second_ua=curl/8.21.0 only=S577,S615,S616,S623 from-sweep=- findings=- run-start=2026-11-05T20:53:34Z stamp-class=python-docs-page-stamp asset-class=learn-microsoft-asset-build-id
S577 fresh as-of=2026-11-05T20:53:34Z
S615 time-churn as-of=2026-11-05T20:53:34Z
S616 time-churn as-of=2026-11-05T20:53:34Z
S623 time-churn as-of=2026-11-05T20:53:35Z
MORI_DRIFT_RECHECK rows=4 adjudicated=4 fresh=1 excerpt=0 time-churn=3 asset-churn=0 receipt-open=0 receipt-stale=0 ua-serving=0 content-drift=0 gate=0 unavailable=0 window=2026-11-05T20:53:34Z..2026-11-05T20:53:35Z
```
Exit 0 matches the map's 0-branch (all four considered copy-bearing rows carry a
token; S615/S616/S623 = time-churn = docs.python.org 'Last updated on' stamp only,
consistent with the C2 claim wording). Output format matches the cell (header,
per-row tokens with as-of, summary line with window).

Selftest:
```
$ TMPDIR="$S" python3 tools/mori-drift-recheck.py --selftest   # exit=0
selftest row_tokens               PASS (got={...} want={...})
selftest as_of_on_every_row       PASS (...)
selftest summary                  PASS (...)
selftest exit_code                PASS (rc=0 want 0)
selftest header_disclosure        PASS (...)
selftest window_same_run          PASS (...)
selftest parse_sweep_rows_not_summary PASS (...)
selftest from_sweep_selects_drifted PASS (...)
selftest from_sweep_malformed_exit2 PASS (...)
selftest missing_sources_exit2    PASS (rc=2 want 2)
MORI_DRIFT_RECHECK_SELFTEST: PASS (10 cases)
```
Matches the self-test cell exactly.

## 3. mori-scorecard-calibration (row 3)

Cell (verdict): per-axis `axis <name> cell=... expect=... state=...`, then
`C1=met` or `C1=unmet axes=6 mismatches=M columns_unchanged=yes/no rows=R rev=<sha12>`
· 0 -> met · 1 -> unmet · 2 -> setup. Self-test cell: `CALIB_SELFTEST pass=11 fail=0`.
Write scope: stdout only; selftest fixtures in TMPDIR, removed.

Observed:
```
$ TMPDIR="$S" python3 tools/mori-scorecard-calibration.py e85ed91249953094b067554bfa79fcdc65791f8e --repo /home/vgpnk/Projects/shokunin/mori-shokunin   # exit=0
axis coverage cell=round_80_improved expect=round_80_improved state=ok
axis operability cell=round_93_improved expect=round_93_improved state=ok
axis depth cell=round_86_improved expect=round_86_improved state=ok
axis freshness cell=round_82_improved expect=round_82_improved state=ok
axis calibration cell=round_93_improved expect=round_93_improved state=ok
axis adjacency cell=round_19_improved expect=round_19_improved state=ok
C1=met axes=6 mismatches=0 columns_unchanged=yes rows=6 rev=e85ed9124995
```
Format and exit/verdict mapping match the cell (C1=met, exit 0).

Selftest:
```
$ TMPDIR="$S" python3 tools/mori-scorecard-calibration.py --selftest   # exit=0
arm conformant_met: pass ... (11 arms)
CALIB_SELFTEST pass=11 fail=0
```
Matches the self-test cell exactly.

## 4. mori-source-digest (row 4)

Cell (verdict): per row `DIGEST <id> ok/mismatch/prefix-only/unpinned recorded=...
actual=...`, then `DIGEST_CHECK rows=N ok=A mismatch=B superseded=S prefix_only=C
unpinned=D` · 0 -> mismatch=0, prefix_only=0 and unpinned=0 · 1 -> any mismatch,
prefix-only or unpinned row · 2 -> setup. Self-test cell:
`DIGEST_SELFTEST pass=11 fail=0`. Write scope: stdout and stderr only; selftest
fixtures in a TemporaryDirectory under TMPDIR.

Observed:
```
$ TMPDIR="$S" python3 tools/mori-source-digest.py corpus/SOURCES.md corpus/evidence   # exit=1
DIGEST S125 ok recorded=e60f1bbc... actual=e60f1bbc...
DIGEST S235 superseded-by S349
...
DIGEST S623 ok recorded=90ac3b25cb2dd28192a5d1c7d45da5ef966d32666d0c583a13eb2ec6f4831ad0 actual=90ac3b25cb2dd28192a5d1c7d45da5ef966d32666d0c583a13eb2ec6f4831ad0
DIGEST S628 ok recorded=0ae6b8806cbb28edd4f8b1ae98ac5045ced71234ba8c81dfa3bf7312eccac618 actual=0ae6b8806cbb28edd4f8b1ae98ac5045ced71234ba8c81dfa3bf7312eccac618
DIGEST_CHECK rows=125 ok=92 mismatch=0 superseded=2 prefix_only=31 unpinned=0
```
(126 lines total: 125 rows + summary.) Exit 1 matches the map's 1-branch because
prefix_only=31 > 0, even though mismatch=0 and unpinned=0. Format matches the cell.
This is an observation, not a mismatch: the gate exit correctly reflects the
31 prefix-only rows in the tree. S615/S616/S623/S628 all `ok` here (spot-verified
S623 and S628 lines above; full per-row output in `$S/out/digest.txt`).

Selftest:
```
$ TMPDIR="$S" python3 tools/mori-source-digest.py --selftest   # exit=0
DIGEST_SELFTEST pass=11 fail=0
```
Matches the self-test cell exactly.

## 5. Write scope (tree before/after)

`find` inventory of the tree before the runs vs after all runs: identical except
two additions, both Python bytecode:

```
1006a1007,1008
> /fast/scratch/hyaku/mori-r97/Mo97ExecTrial/tree/tools/__pycache__/mori-drift-adjudicate.cpython-314.pyc
> /fast/scratch/hyaku/mori-r97/Mo97ExecTrial/tree/tools/__pycache__/mori-source-drift.cpython-314.pyc
```
All other 15,105 paths identical (212 `__pycache__` entries already exist in the
archive itself; only these 2 are new). No other new, modified, or deleted files
detected (no non-pycache file has mtime after extraction). No writes outside
stdout/TMPDIR except these two `.pyc` bytecode files under `tools/__pycache__/`,
produced by `mori-drift-recheck.py` importing its sibling modules. The rows all
claim stdout-only/TMPDIR-only write scope; the drift-recheck row's "stdout only;
read-only under DIR" cell does not mention `.pyc` side-effects. This is the sole
write-scope mismatch, recorded below.

## Mismatches & caveats

1. (write scope) Drift recheck writes `tools/__pycache__/*.pyc` under the tree
   (2 new files, listed above), versus the row cell "stdout only; read-only under
   DIR; fresh fetches held in memory". No other writes outside stdout/TMPDIR
   were observed for any of the four tools (modulo the same bytecode effect on
   the other tools' own `__pycache__` additions being absent — only
   drift-recheck imports sibling modules, hence only it left pyc).
2. (usage caveat, not a mismatch) The cgroup row's entry `[--group PATH]`
   does not state that a leading slash must NOT be passed; with a leading slash
   the tool reports `PRESSURE_UNAVAILABLE` (exit 2, `group_present=false`) even
   though the cgroup exists. Verdict map itself is obeyed in both cases.

## Unrun checks

- `--cases`/`--scratch` fixture battery invocation for mori-cgroup-pressure: unrun
  (not in the task list; selftest already covers the 12 cases).
- The digest tool's `superseded=` predecessor-byte check (deferred to
  `count-c2.py` per the row's known-limit note): unrun here.
- Drift recheck with `--from-sweep` / `--second-ua`: unrun (task asked only
  `--root --only`).

Note: `S577` adjudicates `fresh` here (exit 0). No verdict fabricated beyond the
outputs above. Scratch retained at
`/fast/scratch/hyaku/mori-r97/Mo97ExecTrial/` (`tree/`, `out/`, before/after
inventories).
