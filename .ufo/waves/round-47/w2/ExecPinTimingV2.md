# ExecPinTimingV2 — falsification report, wave w2 (round 47)

Seat: ExecPinTimingV2 (leaf executor, no subagents). Target: **P-C1 C timing/determinism of the **v2** `tools/mori-pin-check.py` at the landed tip T = `68d66ca53d89be5c34a62f46af7c37449d9f9b63` — run it twice with the claim's own flags, time both runs, diff the per-pin `observed=` values, and check the final verdict line.

Verdict: **holds** (deterministic). Both runs exit 0, print byte-identical output (28/28 tally-pin `observed=` values identical, same `rc=` per pin), and the final verdict line is identical: `PIN_CHECK=met …`.

## Instrument

- v2 bytes at T, extracted read-only from git into scratch (never touched the tracked file):
  - command: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 68d66ca53d89be5c34a62f46af7c37449d9f9b63:tools/mori-pin-check.py > .scratch/r47w2-ExecPinTimingV2/mori-pin-check-v2.py`
  - sha256 of used copy: `9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6` (differs from frozen v1 `e3ef425a…`; contains the v2 hardening: SAFE_PATH/argv allow-list, exact tail equality, `fail=0` conjunct + rc check, rebound/duplicate counters — see `mori-pin-check-v2.py:87-92,350-366`).
- Environment: `python3` 3.14.8; `git` 2.56.0. All reads of the lane repo were read-only (`git rev-parse --verify`, `git archive`, `git show E:SKILL.md` — `export_rev`/`main`, `mori-pin-check-v2.py:397-415,457-467`). The tool itself creates and removes a transient `pin-check-*` dir under `<repo>/.scratch` (its own scratch), and runs each pinned command with `cwd=` the freshly exported T tree and `TMPDIR=` inside that tree (`run_cmd`).

## Runs (identical command, twice)

Command (both runs):

```
TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-ExecPinTimingV2 \
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-ExecPinTimingV2/mori-pin-check-v2.py \
  --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
  --rev 68d66ca53d89be5c34a62f46af7c37449d9f9b63 \
  --min-tally-pins 26 \
  --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53
```

Wall time (external `date +%s.%N` ticks around the process; includes `git archive` export + all pinned selftest executions):

| run | wall seconds | exit | stdout | stderr |
|---|---|---|---|---|
| 1 | 77.699 | 0 | `run1.out` (34 lines) | `run1.err` (empty) |
| 2 | 75.810 | 0 | `run2.out` (34 lines) | `run2.err` (empty) |

Scratch evidence: `.scratch/r47w2-ExecPinTimingV2/{run1.out,run2.out,run1.err,run2.err,run1.time,run2.time}`.

## Comparison

- `sha256sum run1.out run2.out` → `aa0fcf6e6e74e793398de91fe625a4db024f2016bc209bcdcb860307406e128c` for **both** (byte-identical).
- `diff -u run1.out run2.out` → exit 0, no differences.
- Per-pin `observed=` values: 28 tally-pin lines with `observed=` in each run; multiset identical (21 unique values — repeat values across rows are identical too).
- `rc=` per pin identical (all `rc=0` except the two intentional mutant pins at line 190/192 with `rc=1`).
- Final verdict line (identical in both runs):

```
PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 min_tally_pins=26 rev=68d66ca53d89be5c34a62f46af7c37449d9f9b63 baseline=yes
```

## Nondeterministic pins

None observed. Every per-pin `observed=` value and `rc=` matched exactly across the two runs, including the environment-sensitive candidates (e.g. line 912 `MORI_SOURCES_APPENDONLY_SELFTEST` → `observed='pass=22 fail=0'`, line 911 CONFORM with rev arg, line 938 PIN_CHECK self-test → `observed='pass=34 fail=0'`).

## Notes / unverified

- Per-command wall times inside a run were not isolated (the tool runs each command once, output merged); only total wall time per run is reported. The ~2 s run-to-run spread is attributed to host load, not output variation (outputs are byte-identical).
- The two runs are the only evidence for this seat; "deterministic" is scoped to these two executions (claim's named limit: "does not prove a selftest is deterministic" applies to a single check run; this seat's two-run comparison directly tests reproducibility).
- `PIN_CHECK=met` reproduces at T under the v2 tool, consistent with the receipt `evidence/after-c1-v2.txt` (measured at af2250d8, whose tree equals T for every measured file; same 28 tally pins, same verdict line modulo `rev=`).
- No repo/lane/jj state was mutated; no tools installed (nothing beyond the host's `python3.14.8` + `git` was needed — no install record required).
