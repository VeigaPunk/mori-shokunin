# MutPsiEnoentZero — C2 selftest sensitivity probe (wave 2)

**Attack:** C2 `tools/mori-pressure.py` selftest sensitivity — mutant: a missing file
reported as ok with zero values.

**Seat:** MoriR24.MutPsiEnoentZero (leaf, no subagents).

**Lane tip tested:** `a730ecfefbdb5c31b1db13aca2c40eecd5e97abc` (checkout of
`/home/vgpnk/Projects/shokunin/mori-shokunin`, detached, in scratch clone).

**Scratch clone:** `/fast/scratch/hyaku/mori-r24-a2/w2/MutPsiEnoentZero/lane`
(`git clone --no-hardlinks`; `git checkout --detach a730ecf`).

## Mutant

Smallest behavior-bearing point: the ENOENT branch of the read path in
`tools/mori-pressure.py` (function `_read_resource`, `except OSError` block, lines 159-164).

Pristine bytes (lines 159-161):

```python
    except OSError as exc:
        state, note = _state_for_oserror(exc)
        return state, None, None, [note]
```

Mutated bytes (same block):

```python
    except OSError as exc:
        state, note = _state_for_oserror(exc)
        if exc.errno == errno.ENOENT:
            zero = {"avg10": 0.0, "avg60": 0.0, "avg300": 0.0, "total": 0}
            return STATE_OK, zero, zero, [note]
        return state, None, None, [note]
```

Effect: a missing file (ENOENT) is reported as state `ok` with zero-valued `some`/`full`
dicts instead of state `absent` (never zero). EOPNOTSUPP/EACCES/EPERM handling untouched.

## Detector and runs

Detector: `python3 -I tools/mori-pressure.py --selftest` (frozen `tools/fixtures/mori-pressure/cases.json`,
12 cases P01-P12), run from the scratch clone root. Python 3.14.8; no tool installs
or upgrades performed this probe.

| Copy | SHA-256 of `tools/mori-pressure.py` | Output | Exit |
|---|---|---|---|
| Pristine (before) | `852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5` | `MORI_PRESSURE_SELFTEST: PASS 12/12` | 0 |
| Mutated | `64897f6a13251e0e0c10ce58f0b0882b6e8761bd9ac6819bf0fba7c6cafe84f0` | `MORI_PRESSURE_SELFTEST: FAIL 11/12` (detail below) | 1 |
| Restored (after) | `852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5` | `MORI_PRESSURE_SELFTEST: PASS 12/12` | 0 |

Mutated run output (verbatim):

```
MORI_PRESSURE_SELFTEST: FAIL 11/12
P04: verdict PRESSURE_OK != PRESSURE_PARTIAL; irq.state is 'ok', expected 'absent'; irq.some is {'avg10': 0.0, 'avg60': 0.0, 'avg300': 0.0, 'total': 0}, expected null; irq.full is {'avg10': 0.0, 'avg60': 0.0, 'avg300': 0.0, 'total': 0}, expected null
exit=1
```

## Verdict: KILLED by P04

The frozen case P04 ("irq file is absent (ENOENT); irq is absent, never zero, and one
unavailable resource leaves the verdict PRESSURE_PARTIAL with exit 0") kills the mutant:
it expects `irq.state == "absent"`, `some: null`, `full: null` and verdict
`PRESSURE_PARTIAL`; the mutant yields `state "ok"`, zero-valued some/full and verdict
`PRESSURE_OK`. All other 11 cases still pass under the mutant (P05/P10 error injection and
P11/P12 interval cases are unaffected: every other case supplies all four files in every
snapshot, so ENOENT is only ever injected in P04). No survivor, so no new missing case to
name; P04 is precisely the missing-file case the selftest already pins.

## Restoration evidence

`git checkout -- tools/mori-pressure.py` in the scratch clone restored the exact pristine
bytes: SHA-256 matches the pre-mutation hash (`852d1ea7…`), `git status --porcelain` is
empty (clean tree), and the restored copy reruns the detector to `PASS 12/12`, exit 0.
No changes were made to the fleet repo, its jj state, or its Git index; the report file
here is the only file created in the lane.
