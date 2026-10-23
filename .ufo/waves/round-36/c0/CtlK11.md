measured 2026-10-23T11:49:27Z
control K11 shape content-free / no decision
control_sha256 1039f3a7e1f2c0502e4a6f38fc5d5b3b98699932baf87f1df7fc5f00b2d1dec9
counter_sha256 ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145

Axes: shape fidelity, detector rejection, frozen-byte preservation.

Control: `.ufo/waves/round-36/c0/controls/K11.py:9-19` accepts `--root DIR`, reads the registry in order, emits each registry id with state `unknown`, prints the summary with every count zero, and returns 0. It does not fetch URLs or inspect copies. Assigned shape: `.ufo/waves/round-36/contract.md:93`.

Expected detector: reject all undecided rows. The counter accepts only the five contract states (`.ufo/waves/round-36/count-c1.py:65,287-305`), so `unknown` produces absent classifications. The blind failure skips the real arm (`count-c1.py:699-706`).

Scored command (no `--seed`; scratch contained in this seat):
```sh
env MORI_R36_SCRATCH=/fast/scratch/hyaku/mori-r36/CtlK11 TMPDIR=/fast/scratch/hyaku/mori-r36/CtlK11 PYTHONDONTWRITEBYTECODE=1 timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py 6bd57097 --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K11.py
```

Full counter output:
```text
P-C1: at revision R, tools/mori-source-drift.py classifies every row of a 40-row blind fixture drawn at run time exactly as the counter's hidden truth, and on the lane's own corpus/SOURCES.md at R it agrees with the counter's independent live oracle on every row the oracle classified, with at least 10 oracle-fetched rows including at least one oracle-fresh and one oracle-drifted row.
blind_rows=40 tool_exit=0 tool_rows=0 mismatches=40
blind_mismatch S005 tool=<absent> truth=no-copy
blind_mismatch S027 tool=<absent> truth=no-copy
blind_mismatch S038 tool=<absent> truth=unavailable
blind_mismatch S043 tool=<absent> truth=drifted
blind_mismatch S049 tool=<absent> truth=fresh
blind_mismatch S054 tool=<absent> truth=no-copy
blind_mismatch S066 tool=<absent> truth=excerpt
blind_mismatch S071 tool=<absent> truth=unavailable
blind_mismatch S072 tool=<absent> truth=drifted
blind_mismatch S076 tool=<absent> truth=no-copy
blind_mismatch S081 tool=<absent> truth=fresh
blind_mismatch S087 tool=<absent> truth=unavailable
blind_mismatch S090 tool=<absent> truth=excerpt
blind_mismatch S095 tool=<absent> truth=no-copy
blind_mismatch S125 tool=<absent> truth=unavailable
blind_mismatch S129 tool=<absent> truth=fresh
blind_mismatch S131 tool=<absent> truth=excerpt
blind_mismatch S135 tool=<absent> truth=unavailable
blind_mismatch S156 tool=<absent> truth=drifted
blind_mismatch S158 tool=<absent> truth=unavailable
real_arm=skipped
C1=unmet
seed=7275836658844107176
```
Counter exit code: 1. Control exit code: 0, as reported above. The counter rejected K11 with 40 blind mismatches; no real-arm result is claimed.

VERDICT: K11 unmet exit 1

Before/after evidence: both invocations of the following bounded command returned the identical output below, once before scoring and once after scoring:
```sh
timeout 10 sha256sum .ufo/waves/round-36/c0/controls/K11.py .ufo/waves/round-36/contract.md .ufo/waves/round-36/count-c1.py .ufo/waves/round-36/count-c2.py
```
```text
1039f3a7e1f2c0502e4a6f38fc5d5b3b98699932baf87f1df7fc5f00b2d1dec9  .ufo/waves/round-36/c0/controls/K11.py
d903c67950a081c3e25d19a208f79c84ab6e34f99680acea31d3f8590eaa431a  .ufo/waves/round-36/contract.md
ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145  .ufo/waves/round-36/count-c1.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  .ufo/waves/round-36/count-c2.py
```
These frozen-file hashes match `.ufo/waves/round-36/evidence/freeze.txt:2-4` and the assigned counter hashes.

Restoration: no existing target or frozen-counter bytes were edited; the new substitute control is intentionally retained. The supplied baseline receipt records tool absence and an unmet result (`evidence/freeze.txt:5`), so this rejection is not reported as a pristine-target mutant kill. Only the assigned substitute-control detector run was performed.

Containment: `read /fast/scratch/hyaku/mori-r36/CtlK11` after scoring returned `(empty directory)`. The bounded scoring command exited; no background jobs were launched. The counter closes its local server and removes its fixture in finally blocks (`count-c1.py:546-548,561-562`). No lane git writes or tool installations/updates were performed.
