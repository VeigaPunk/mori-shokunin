measured 2026-10-23T11:51:11Z
control K4 shape copying-the-observed-column/no-reader
control_sha256 07c40adeafbd5a22b9cf74bbef60b706f8eee44264ec5362b9f6b25f2bd51bdb
counter_sha256 ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145

Axes: shape fidelity, detection, containment.

Mutant: replace the copy-content classifier with unconditional fresh after a successful GET. K4 checks copy presence using directory entries and file metadata, never opens a copy file, preserves no-copy without fetching, and preserves unavailable on failed GETs. Evidence: `.ufo/waves/round-36/c0/controls/K4.py:18-55`; CLI, setup handling and summary: the same file at lines 58-88. This implements the assigned defect without changing the frozen contract (`.ufo/waves/round-36/contract.md:33-58,94`).

Expected detector: the frozen C1 blind arm rejects excerpt and drifted rows mislabeled fresh; the fixture has eight of each (`count-c1.py:70-72,388-392,428-453,537-560`, relative to `.ufo/waves/round-36/`). A pristine failure would make the mutation probe inconclusive; the pristine probe below passed.

## Frozen-counter verification

Before scoring and again after scoring, `timeout 30 sha256sum` on both absolute counter paths returned the following hashes, matching `.ufo/waves/round-36/evidence/freeze.txt:3-4`:

```text
ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145  count-c1.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  count-c2.py
```

## Scored command and full counter output

Working directory: `/home/vgpnk/Projects/shokunin/mori-shokunin`. No seed override was supplied. The environment confines generated fixtures to this seat and disables bytecode writes.

```sh
timeout 900 env PYTHONDONTWRITEBYTECODE=1 MORI_R36_SCRATCH=/fast/scratch/hyaku/mori-r36/CtlK4 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py 6bd57097 --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K4.py
```

```text
P-C1: at revision R, tools/mori-source-drift.py classifies every row of a 40-row blind fixture drawn at run time exactly as the counter's hidden truth, and on the lane's own corpus/SOURCES.md at R it agrees with the counter's independent live oracle on every row the oracle classified, with at least 10 oracle-fetched rows including at least one oracle-fresh and one oracle-drifted row.
blind_rows=40 tool_exit=0 tool_rows=40 mismatches=16
blind_mismatch S001 tool=fresh truth=excerpt
blind_mismatch S005 tool=fresh truth=excerpt
blind_mismatch S012 tool=fresh truth=drifted
blind_mismatch S023 tool=fresh truth=drifted
blind_mismatch S041 tool=fresh truth=drifted
blind_mismatch S050 tool=fresh truth=drifted
blind_mismatch S055 tool=fresh truth=drifted
blind_mismatch S088 tool=fresh truth=drifted
blind_mismatch S117 tool=fresh truth=excerpt
blind_mismatch S145 tool=fresh truth=excerpt
blind_mismatch S192 tool=fresh truth=excerpt
blind_mismatch S206 tool=fresh truth=excerpt
blind_mismatch S213 tool=fresh truth=drifted
blind_mismatch S245 tool=fresh truth=excerpt
blind_mismatch S253 tool=fresh truth=drifted
blind_mismatch S299 tool=fresh truth=excerpt
real_arm=skipped
C1=unmet
seed=2640188673096554099
```

Counter exit code: 1. The real arm was skipped; this receipt makes no live-oracle assertion.

VERDICT: K4 unmet exit 1

## Pristine / mutated / restored behavioral probe

The same bounded detector invoked the unchanged frozen counter's blind arm with the same local seed and 40-row fixture on all three byte states. This auxiliary seed was not passed to the scored counter. Detector source: `/fast/scratch/hyaku/mori-r36/CtlK4/blind-detector.py:9-28`; SHA-256: `20d6162bf80c7b9885e9c78f8c5c6dcf5c13d4a2a47c2e02d6132c3e8375fee2` (measured with `timeout 30 sha256sum`). Only the scratch program's `classify_fetched` function was mutated, then restored; the retained lane control is the required defective substitute.

Commands, each run synchronously:

```sh
timeout 120 env PYTHONDONTWRITEBYTECODE=1 MORI_R36_SCRATCH=/fast/scratch/hyaku/mori-r36/CtlK4 python3 /fast/scratch/hyaku/mori-r36/CtlK4/blind-detector.py /fast/scratch/hyaku/mori-r36/CtlK4/probe.py pristine
timeout 120 env PYTHONDONTWRITEBYTECODE=1 MORI_R36_SCRATCH=/fast/scratch/hyaku/mori-r36/CtlK4 python3 /fast/scratch/hyaku/mori-r36/CtlK4/blind-detector.py /fast/scratch/hyaku/mori-r36/CtlK4/probe.py mutated
timeout 120 env PYTHONDONTWRITEBYTECODE=1 MORI_R36_SCRATCH=/fast/scratch/hyaku/mori-r36/CtlK4 python3 /fast/scratch/hyaku/mori-r36/CtlK4/blind-detector.py /fast/scratch/hyaku/mori-r36/CtlK4/probe.py restored
```

Actual pristine output (detector exit 0):

```text
phase=pristine
tool_sha256=2585c6a60a7a03e38fc664f4198a524b7c2ea5f810db6039d6d5366a1126879f
detector=frozen_C1_blind_arm seed=3604 rows=40
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
blind_pass=true
```

Actual mutated output (detector exit 1):

```text
phase=mutated
tool_sha256=07c40adeafbd5a22b9cf74bbef60b706f8eee44264ec5362b9f6b25f2bd51bdb
detector=frozen_C1_blind_arm seed=3604 rows=40
blind_rows=40 tool_exit=0 tool_rows=40 mismatches=16
blind_mismatch S013 tool=fresh truth=drifted
blind_mismatch S028 tool=fresh truth=drifted
blind_mismatch S036 tool=fresh truth=drifted
blind_mismatch S049 tool=fresh truth=drifted
blind_mismatch S060 tool=fresh truth=excerpt
blind_mismatch S061 tool=fresh truth=excerpt
blind_mismatch S063 tool=fresh truth=excerpt
blind_mismatch S071 tool=fresh truth=drifted
blind_mismatch S091 tool=fresh truth=drifted
blind_mismatch S098 tool=fresh truth=excerpt
blind_mismatch S105 tool=fresh truth=excerpt
blind_mismatch S188 tool=fresh truth=excerpt
blind_mismatch S235 tool=fresh truth=drifted
blind_mismatch S254 tool=fresh truth=excerpt
blind_mismatch S274 tool=fresh truth=drifted
blind_mismatch S297 tool=fresh truth=excerpt
blind_pass=false
```

Actual restored output (detector exit 0):

```text
phase=restored
tool_sha256=2585c6a60a7a03e38fc664f4198a524b7c2ea5f810db6039d6d5366a1126879f
detector=frozen_C1_blind_arm seed=3604 rows=40
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
blind_pass=true
```

Mutation result: killed, not inconclusive. Before and restored scratch hashes are identical; the mutated scratch hash equals the retained K4 control hash. A final `timeout 30 sha256sum` independently returned:

```text
07c40adeafbd5a22b9cf74bbef60b706f8eee44264ec5362b9f6b25f2bd51bdb  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K4.py
2585c6a60a7a03e38fc664f4198a524b7c2ea5f810db6039d6d5366a1126879f  /fast/scratch/hyaku/mori-r36/CtlK4/probe.py
```

Containment: all invoked commands completed; no persistent service or background job was started. No git writes, commits, index changes or tool installations were performed. `timeout 10 df -h /fast` reported 70G available before fixture writes. The counter invocation's tool wrapper reported terminal allocation unavailable and ran without a terminal; this did not change the observed counter exit 1. That fallback was reported through `xd://report_issue`.
