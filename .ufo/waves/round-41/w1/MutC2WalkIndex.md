# MutC2WalkIndex — C2 landing-arbitration mutation probe

Seat: L1-mori-r41-attempt2.MutC2WalkIndex (mutation tester, leaf).
Scope: C2 only (P-C12 depth). Read-only lane: no source, fixture, Git index or jj state changed.
Probe: in an isolated gate copy, restore the v3 **latest-first-appearance walk-index**
arbitration in place of P-C12's maximal-candidate selection, then run both `dag-2l`
date variants and check whether the outputs diverge.

## Instrument

| Item | Value |
|---|---|
| Lane gate (unmodified) | `tools/mori-sources-appendonly.py` |
| Lane gate sha256 (before, after) | `75af8f6fc63dc736f07c02617bed4bf6c1ad7f880ffb49849b065b4d40d8f76b` (both) |
| Isolated copy root | `/tmp/mutc2-walkindex.37L9WRtl` (`gate/gate.py`, `gate/gate.pristine.py`, `gate/builder.py`, `gate/probe.py`) |
| Builder | `.ufo/waves/round-41/fixtures/c2/build-dags-r40.py`, sha256 `6e3daa507f598cee8b5257a32934a550ca1f4f4fc078bb76e6d8ad49fce246ac` |
| Detector | run gate subprocess on `dag-2l-early` and `dag-2l-late` (same DAG/contents, side commit dated `2026-01-01T01:00:00Z` vs `2026-01-01T03:30:00Z`); compare exit + non-predicate output lines; plus the gate's own `--selftest` r41 arms |

Expected detector under P-C12: both variants produce the **same** verdict — date must not
decide the landing (`superseded_by=S002`, `superseded_as_of=[]`, `stale_supersede=[S001]`).
`DIVERGES=True` is the kill signal.

## Mutant

File: `/tmp/mutc2-walkindex.37L9WRtl/gate/gate.py` (line 373 block).
Replaced P-C12's maximal-candidate selection:

```python
    supersede_landing = {}
    sup_map = {}
    for target, candidates in eligible.items():
        maximal = []
        for landing, by in candidates:
            has_descendant = any(
                landing != other_landing and ancestor(landing, other_landing)
                for other_landing, _ in candidates)
            if not has_descendant:
                maximal.append((landing, by))
        landing, by = min(maximal, key=lambda candidate:
                          (candidate[1], candidate[0]))
        supersede_landing[target] = landing
        sup_map[target] = by
```

with the v3 behaviour:

```python
    supersede_landing = {}
    sup_map = {}
    walk_index = {commit: index for index, commit in enumerate(commits)}
    for target, candidates in eligible.items():
        # Mutant: restore v3 latest-first-appearance walk-index arbitration.
        landing, by = max(candidates, key=lambda candidate:
                          walk_index[candidate[0]])
        supersede_landing[target] = landing
        sup_map[target] = by
```

Latest walk index == commit-date order (`git log --reverse`), so the side supersede (S002)
and the main-chain supersede (S003) swap places when only the side date changes.
Mutant sha256: `ed4dc5502be7c1eb0554fd35863d4e3859abd5fa4b52588f4a92c4fb93028096`.

## Outputs

### Baseline (pristine gate, `repos/pristine`)

```
## dag-2l-early exit=1 shas={'b0':'3e5442dae5','s1':'024f6d7f3d','c1':'25ff69f83b','c2':'e3bf2735bd','m':'050883e5d0'}
   changed S001 superseded_by=S002
   appendonly_violations=1 ids=[S001] deleted=[] superseded=[S001] round_changed=[S001]
   supersede_timing superseded_as_of=[] stale_supersede=[S001]
## dag-2l-late exit=1 shas={'b0':'3e5442dae5','s1':'4704030c69','c1':'25ff69f83b','c2':'e3bf2735bd','m':'a26f088aa2'}
   changed S001 superseded_by=S002
   appendonly_violations=1 ids=[S001] deleted=[] superseded=[S001] round_changed=[S001]
   supersede_timing superseded_as_of=[] stale_supersede=[S001]
DIVERGES=False
SELFTEST exit=0  MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0
```

Baseline fixture `m` shas `050883e5d0` / `a26f088aa2` match the revs in
`evidence/control-after.txt`, so the isolated fixture reproduces the frozen one.
The baseline is a genuine pass (not an inconclusive one).

### Mutated (latest-walk-index arbitration, `repos/mutant`)

```
## dag-2l-early exit=1 shas={'b0':'3e5442dae5','s1':'024f6d7f3d','c1':'25ff69f83b','c2':'e3bf2735bd','m':'050883e5d0'}
   changed S001 superseded_by=S003
   appendonly_violations=1 ids=[S001] deleted=[] superseded=[S001] round_changed=[S001]
   supersede_timing superseded_as_of=[S001] stale_supersede=[]
## dag-2l-late exit=1 shas={'b0':'3e5442dae5','s1':'4704030c69','c1':'25ff69f83b','c2':'e3bf2735bd','m':'a26f088aa2'}
   changed S001 superseded_by=S002
   appendonly_violations=1 ids=[S001] deleted=[] superseded=[S001] round_changed=[S001]
   supersede_timing superseded_as_of=[] stale_supersede=[S001]
DIVERGES=True
SELFTEST exit=1
   FAIL incomparable superseders resolve independently of early date: superseded_as_of: want [] got ['S001']; stale_supersede: want ['S001'] got []; superseded_by[S001]: want S002 got 'S003'
   MORI_SOURCES_APPENDONLY_SELFTEST pass=21 fail=1
```

Identical DAG and registry contents; only the side commit date differs; the verdict flips
`superseded_by=S003`/as-of ↔ `S002`/stale. This diverging pair is exactly the
`control-before.txt` v3 signature (`early as_of=[S001]`, `late stale=[S001]`), confirming
the mutant restores the routed date-sensitivity defect rather than inventing a new one.

### Restored (exact pristine bytes, `repos/restored`)

```
DIVERGES=False
EARLY: changed S001 superseded_by=S002 | ... | supersede_timing superseded_as_of=[] stale_supersede=[S001]
LATE : changed S001 superseded_by=S002 | ... | supersede_timing superseded_as_of=[] stale_supersede=[S001]
SELFTEST exit=0  MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0
```

## Verdict

**KILLED.** The date-invariance detector (`DIVERGES=True`) and the gate's own
`r41-dag-2l-early` selftest arm both reject latest-walk-index arbitration. The
`r41-dag-2l-late` arm passes under the mutant by coincidence (its max-index landing is
`s1`, which happens to yield the P-C12 verdict), so the cross-variant comparison is the
strictly stronger detector; the in-tree arm alone is sufficient but single-sided.
The kill is a positive result for P-C12's arbitration: it is the mechanism that removes
the date dependence, not an incidental difference in fixture construction.

## Restoration evidence

| Check | Result |
|---|---|
| `cp -p gate/gate.pristine.py gate/gate.py` | done |
| `sha256sum gate/gate.py` | `75af8f6fc63dc736f07c02617bed4bf6c1ad7f880ffb49849b065b4d40d8f76b` |
| `sha256sum gate/gate.pristine.py` | `75af8f6fc63dc736f07c02617bed4bf6c1ad7f880ffb49849b065b4d40d8f76b` |
| `cmp gate/gate.py gate/gate.pristine.py` | clean (`BYTES_IDENTICAL`) |
| Lane `tools/mori-sources-appendonly.py` sha256 | `75af8f6f…d8f76b` — unchanged |
| `git status --porcelain -- tools/mori-sources-appendonly.py .ufo/waves/round-41/fixtures` | empty |
| Mutant bytes retained | only in `/tmp/mutc2-walkindex.37L9WRtl` (disposable); not in lane |

No tool installs or updates were performed (none needed). No sibling repo, PROVINCE.md
Adjacent entry, lane Git index, jj state or `.ufo/state` was read or written outside this
report.
