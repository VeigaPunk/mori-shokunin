measured 2026-10-23T11:49:21Z
control K8 shape label- or id-keyed
control_sha256 6c3dc0ee89c6c56dbeb84d3f9d4ac06b09faae75daab44cd35508e9b6a93c02f
counter_sha256 ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145

## Control and expected detector

Axes: shape fidelity, CLI fidelity, blind-arm rejection.

The substitute accepts `--root DIR`, reads registry ids, and enumerates copy filenames without fetching URLs or reading copy bytes. It resolves the highest numbered copy directory, then selects from `(fresh, excerpt, drifted, unavailable, no-copy)` using `(id_number % 5 + sum(extension_codepoints) + directory_number % 5) % 5`. Missing copies use directory number 0 and an empty extension. No URL, status, body, file-size, root-path or port information enters this decision. Source: `.ufo/waves/round-36/c0/controls/K8.py:9-38,41-66`.

Expected detector: any incorrect row produces a blind mismatch and `C1=unmet`, exit 1; the real arm is then skipped. Sources: `.ufo/waves/round-36/count-c1.py:298-312,537-560,695-706`; CLI: `.ufo/waves/round-36/contract.md:33-47`.

## Frozen-byte check

Command, run before scoring and again after scoring:

```text
timeout 30 sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K8.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
```

Identical output on both runs, exit 0:

```text
6c3dc0ee89c6c56dbeb84d3f9d4ac06b09faae75daab44cd35508e9b6a93c02f  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K8.py
ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
```

Both counter hashes match `.ufo/waves/round-36/evidence/freeze.txt:3-4` and the task's pinned hashes.

## Scored command and full counter output

Working directory: `/home/vgpnk/Projects/shokunin/mori-shokunin`. No seed supplied. The environment confines counter fixtures to this seat's scratch directory and disables bytecode writes.

```text
timeout 900 env MORI_R36_SCRATCH=/fast/scratch/hyaku/mori-r36/CtlK8 PYTHONDONTWRITEBYTECODE=1 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py 6bd57097 --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K8.py
```

```text
P-C1: at revision R, tools/mori-source-drift.py classifies every row of a 40-row blind fixture drawn at run time exactly as the counter's hidden truth, and on the lane's own corpus/SOURCES.md at R it agrees with the counter's independent live oracle on every row the oracle classified, with at least 10 oracle-fetched rows including at least one oracle-fresh and one oracle-drifted row.
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=30
blind_mismatch S018 tool=fresh truth=no-copy
blind_mismatch S032 tool=drifted truth=no-copy
blind_mismatch S059 tool=fresh truth=drifted
blind_mismatch S063 tool=fresh truth=unavailable
blind_mismatch S080 tool=drifted truth=excerpt
blind_mismatch S086 tool=drifted truth=unavailable
blind_mismatch S087 tool=fresh truth=excerpt
blind_mismatch S088 tool=unavailable truth=excerpt
blind_mismatch S092 tool=unavailable truth=drifted
blind_mismatch S098 tool=unavailable truth=fresh
blind_mismatch S123 tool=excerpt truth=drifted
blind_mismatch S126 tool=excerpt truth=unavailable
blind_mismatch S138 tool=fresh truth=unavailable
blind_mismatch S149 tool=no-copy truth=fresh
blind_mismatch S155 tool=drifted truth=unavailable
blind_mismatch S164 tool=fresh truth=excerpt
blind_mismatch S170 tool=drifted truth=no-copy
blind_mismatch S190 tool=fresh truth=no-copy
blind_mismatch S201 tool=no-copy truth=fresh
blind_mismatch S204 tool=no-copy truth=fresh
real_arm=skipped
C1=unmet
seed=11560148011178037586
```

Counter exit code: 1. The counter itself prints at most 20 mismatch details (`.ufo/waves/round-36/count-c1.py:554-557`); the output above is complete.

## Outcome and restoration evidence

The counter rejected the label-keyed substitute: 30 of 40 blind rows mismatched; the real arm was not exercised. This is the assigned substitute-control probe, not a pristine/mutated/restored target experiment; no killed-mutant claim is made without a passing pristine baseline. The requested new control is retained. Its before/after SHA-256 is identical, as are both frozen counter hashes above. No production tool bytes were edited.

No tools were installed or updated. No background jobs were launched. The bounded counter command returned exit 1.

VERDICT: K8 unmet exit 1
