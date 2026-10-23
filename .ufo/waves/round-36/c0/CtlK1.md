measured 2026-10-23T11:49:15Z
control K1 shape skip-work / do-nothing
control_sha256 648ade0ec5ef86eae13caad129bf800da9a3fefe436de952c6e081f886b36300
counter_sha256 ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145

Axes: exact defect shape, detector sensitivity, byte integrity, containment.

Control: `.ufo/waves/round-36/c0/controls/K1.py:1-8` accepts the required `--root DIR`, prints nothing and exits normally without reading or fetching anything. This is the specified K1 shape (`.ufo/waves/round-36/contract.md:92`).

Expected detector: `C1=unmet`, exit 1, because every required row classification is absent (`.ufo/waves/round-36/contract.md:21,35-47`; `.ufo/waves/round-36/count-c1.py:551-560,702-706`).

Scored command (no seed supplied; environment confines temporary writes to this seat):
```sh
timeout 900 env MORI_R36_SCRATCH=/fast/scratch/hyaku/mori-r36/CtlK1 TMPDIR=/fast/scratch/hyaku/mori-r36/CtlK1 PYTHONDONTWRITEBYTECODE=1 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py 6bd57097 --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K1.py
```
Full counter output:
```text
P-C1: at revision R, tools/mori-source-drift.py classifies every row of a 40-row blind fixture drawn at run time exactly as the counter's hidden truth, and on the lane's own corpus/SOURCES.md at R it agrees with the counter's independent live oracle on every row the oracle classified, with at least 10 oracle-fetched rows including at least one oracle-fresh and one oracle-drifted row.
blind_rows=40 tool_exit=0 tool_rows=0 mismatches=40
blind_mismatch S002 tool=<absent> truth=drifted
blind_mismatch S009 tool=<absent> truth=unavailable
blind_mismatch S013 tool=<absent> truth=drifted
blind_mismatch S023 tool=<absent> truth=fresh
blind_mismatch S030 tool=<absent> truth=unavailable
blind_mismatch S032 tool=<absent> truth=no-copy
blind_mismatch S036 tool=<absent> truth=unavailable
blind_mismatch S039 tool=<absent> truth=fresh
blind_mismatch S049 tool=<absent> truth=excerpt
blind_mismatch S054 tool=<absent> truth=no-copy
blind_mismatch S059 tool=<absent> truth=fresh
blind_mismatch S064 tool=<absent> truth=no-copy
blind_mismatch S068 tool=<absent> truth=drifted
blind_mismatch S072 tool=<absent> truth=no-copy
blind_mismatch S079 tool=<absent> truth=unavailable
blind_mismatch S086 tool=<absent> truth=drifted
blind_mismatch S090 tool=<absent> truth=drifted
blind_mismatch S095 tool=<absent> truth=unavailable
blind_mismatch S107 tool=<absent> truth=fresh
blind_mismatch S112 tool=<absent> truth=drifted
real_arm=skipped
C1=unmet
seed=4935616154607398373
```
Counter exit code: 1.

Byte integrity / restoration evidence:
- Before scoring, `timeout 120 sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py` returned the frozen hashes below, matching `.ufo/waves/round-36/evidence/freeze.txt:3-4`.
- Before scoring, `timeout 120 sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K1.py` returned the control hash above.
- After scoring, `timeout 120 sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K1.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py` returned:
```text
648ade0ec5ef86eae13caad129bf800da9a3fefe436de952c6e081f886b36300  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K1.py
ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
```
- This was a new substitute program, not an in-place target mutation; no original source bytes required restoration. The requested control remains as the deliverable. No passing-pristine/restored detector claim or conventional killed-mutant claim is made.
- After the synchronous counter exited, reading `/fast/scratch/hyaku/mori-r36/CtlK1/` returned `(empty directory)`. Counter cleanup is at `.ufo/waves/round-36/count-c1.py:546-548,561-562`; no background jobs were started.
- No tools were installed or updated. No lane git writes were run.

VERDICT: K1 unmet exit 1
