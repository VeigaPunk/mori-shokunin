measured 2026-10-23T11:49:31Z
control K2 shape generic rows
control_sha256 0a08726cf6b2c496d38ba55047208e49a21f47a8dd50cefdf6e213c859704709
counter_sha256 ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145

Axes: freshness discrimination, CLI/output fidelity, containment.

Mutant: the substitute reads the registry, emits every matched id as fresh in registry order, prints an all-fresh summary, and exits 0. It does not inspect copies or fetch URLs. Evidence: `.ufo/waves/round-36/c0/controls/K2.py:7-24`. This is the assigned generic-row defect, not a target implementation judgment.

Expected detector: the blind arm has eight rows per state; an all-fresh substitute should mismatch the 32 non-fresh rows and be scored unmet before the real arm. Evidence: `.ufo/waves/round-36/contract.md:49-58`; `.ufo/waves/round-36/count-c1.py:537-562,699-706`.

Freeze verification before scoring used `timeout 30 sha256sum` on both counters; both matched `.ufo/waves/round-36/evidence/freeze.txt:3-4`. The following four-file command was also run immediately before and after scoring, with identical output both times:

```text
timeout 30 sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K2.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/contract.md

0a08726cf6b2c496d38ba55047208e49a21f47a8dd50cefdf6e213c859704709  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K2.py
ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
d903c67950a081c3e25d19a208f79c84ab6e34f99680acea31d3f8590eaa431a  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/contract.md
```

Scoring command, run once without --seed:

```text
timeout 900 env MORI_R36_SCRATCH=/fast/scratch/hyaku/mori-r36/CtlK2 TMPDIR=/fast/scratch/hyaku/mori-r36/CtlK2 PYTHONDONTWRITEBYTECODE=1 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py 6bd57097 --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K2.py
```

Full counter output:

```text
P-C1: at revision R, tools/mori-source-drift.py classifies every row of a 40-row blind fixture drawn at run time exactly as the counter's hidden truth, and on the lane's own corpus/SOURCES.md at R it agrees with the counter's independent live oracle on every row the oracle classified, with at least 10 oracle-fetched rows including at least one oracle-fresh and one oracle-drifted row.
blind_rows=40 tool_exit=0 tool_rows=40 mismatches=32
blind_mismatch S008 tool=fresh truth=no-copy
blind_mismatch S016 tool=fresh truth=no-copy
blind_mismatch S024 tool=fresh truth=drifted
blind_mismatch S039 tool=fresh truth=unavailable
blind_mismatch S040 tool=fresh truth=excerpt
blind_mismatch S043 tool=fresh truth=drifted
blind_mismatch S046 tool=fresh truth=no-copy
blind_mismatch S068 tool=fresh truth=excerpt
blind_mismatch S078 tool=fresh truth=no-copy
blind_mismatch S080 tool=fresh truth=drifted
blind_mismatch S082 tool=fresh truth=drifted
blind_mismatch S085 tool=fresh truth=excerpt
blind_mismatch S086 tool=fresh truth=excerpt
blind_mismatch S087 tool=fresh truth=drifted
blind_mismatch S092 tool=fresh truth=excerpt
blind_mismatch S093 tool=fresh truth=no-copy
blind_mismatch S107 tool=fresh truth=unavailable
blind_mismatch S112 tool=fresh truth=excerpt
blind_mismatch S113 tool=fresh truth=drifted
blind_mismatch S117 tool=fresh truth=drifted
real_arm=skipped
C1=unmet
seed=16420465132592349921
```

Counter exit code: 1 (command result: Command exited with code 1). The control exited 0 and produced all 40 row decisions; the counter rejected 32 of them. The real arm was skipped, not passed (full output above).

Restoration evidence: this was a retained --tool substitute, not an edit to an existing implementation. No production source was mutated and no restoration was required. Control, counters, and contract hashes were identical before and after scoring, as recorded above. A post-run directory read of `/fast/scratch/hyaku/mori-r36/CtlK2/` returned `(empty directory)`. All commands ran in the foreground and completed; no background jobs were launched.

No tools were installed or updated. Timestamp source: `timeout 30 date -u +%FT%TZ` returned `2026-10-23T11:49:31Z`.

VERDICT: K2 unmet exit 1
