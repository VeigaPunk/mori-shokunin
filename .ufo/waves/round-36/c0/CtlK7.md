measured 2026-10-23T11:49:36Z
control K7 shape off-topic
control_sha256 9c7933bc6b21b1c554595e933953945c319e34828538158eda2d003c01f0fa14
counter_sha256 ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145

## Control and expected detector

Axes: exact defect shape, frozen-detector rejection, isolated writes.

K7 implements the C1 `--root DIR` interface, registry-order row output, summary and drift-based exit code, but classifies each row's own status: mined→fresh, queued→excerpt, rejected→drifted, anything else→no-copy. It only reads SOURCES.md; it never fetches or reads copies. Evidence: `.ufo/waves/round-36/c0/controls/K7.py:10-42`; interface: `.ufo/waves/round-36/contract.md:33-47`; assigned shape: `contract.md:97`.

Expected detector: C1=unmet. The blind fixture writes mined in every row (`count-c1.py:490-497`) while assigning eight rows to each of five truth states (`count-c1.py:70-72`). K7 therefore reports fresh for all 40 rows; the expected mismatch count is 32.

## Scored command and full output

Working directory: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Environment: `MORI_R36_SCRATCH=/fast/scratch/hyaku/mori-r36/CtlK7`, `TMPDIR=/fast/scratch/hyaku/mori-r36/CtlK7`, `PYTHONDONTWRITEBYTECODE=1`.
No seed argument was supplied.

```text
timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py 6bd57097 --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K7.py
```

Full stdout:
```text
P-C1: at revision R, tools/mori-source-drift.py classifies every row of a 40-row blind fixture drawn at run time exactly as the counter's hidden truth, and on the lane's own corpus/SOURCES.md at R it agrees with the counter's independent live oracle on every row the oracle classified, with at least 10 oracle-fetched rows including at least one oracle-fresh and one oracle-drifted row.
blind_rows=40 tool_exit=0 tool_rows=40 mismatches=32
blind_mismatch S004 tool=fresh truth=no-copy
blind_mismatch S005 tool=fresh truth=drifted
blind_mismatch S007 tool=fresh truth=drifted
blind_mismatch S009 tool=fresh truth=no-copy
blind_mismatch S017 tool=fresh truth=excerpt
blind_mismatch S018 tool=fresh truth=no-copy
blind_mismatch S027 tool=fresh truth=no-copy
blind_mismatch S031 tool=fresh truth=drifted
blind_mismatch S042 tool=fresh truth=no-copy
blind_mismatch S045 tool=fresh truth=no-copy
blind_mismatch S060 tool=fresh truth=excerpt
blind_mismatch S101 tool=fresh truth=excerpt
blind_mismatch S119 tool=fresh truth=unavailable
blind_mismatch S121 tool=fresh truth=drifted
blind_mismatch S127 tool=fresh truth=excerpt
blind_mismatch S146 tool=fresh truth=unavailable
blind_mismatch S152 tool=fresh truth=drifted
blind_mismatch S156 tool=fresh truth=excerpt
blind_mismatch S166 tool=fresh truth=no-copy
blind_mismatch S170 tool=fresh truth=excerpt
real_arm=skipped
C1=unmet
seed=15049172438623310773
```

Stderr: empty. Counter exit: 1. The counter rejected the off-topic substitute; the real arm was not exercised. Evidence: command and full output above. This is a control-rejection receipt, not a claim that a passing pristine tool was mutation-tested.

## Hashes and restoration evidence

Before scoring and after scoring, this command returned identical bytes below:
```text
timeout 120 sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K7.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
9c7933bc6b21b1c554595e933953945c319e34828538158eda2d003c01f0fa14  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K7.py
ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
```

Both counter hashes were verified before scoring against `evidence/freeze.txt:3-4` and remained unchanged afterward. No production tool or frozen source was edited; the assigned standalone substitute is retained at its required path, so there were no overwritten source bytes to restore. No pristine/restored behavioral runs were performed for this standalone control.

After the completed counter subprocess returned exit 1, reading `/fast/scratch/hyaku/mori-r36/CtlK7` returned `(empty directory)`. The counter shuts down and closes its local server, then removes its fixture (`count-c1.py:545-562`). No background jobs were started. Lane writes were limited to this report and K7.py. Tool installations/updates: none.

VERDICT: K7 unmet exit 1
