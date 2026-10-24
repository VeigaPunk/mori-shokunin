measured 2026-10-23T11:50:44Z
control K3 shape rule-level skip (sha-only)
control_sha256 c1af37d976e3c21bda8933422bc50ddc045460b31f8291fb12c2c39cd2a79f29
counter_sha256 ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145

Axes: exact defect shape, detector sensitivity, containment.
Lane-relative paths below are rooted at /home/vgpnk/Projects/shokunin/mori-shokunin.

## Control and expected detector

K3 fetches each row having both URL and newest copy. Equal sha256 means fresh; unequal bytes or a fetch error mean drifted. It retains the specified no-copy behavior, row order, summary and drift-based exit status. The only behavior changed from the pristine scratch classifier is its classify function: excerpt and unavailable become drifted. Sources: .ufo/waves/round-36/contract.md:33-47,101; .ufo/waves/round-36/c0/controls/K3.py:17-65.

Expected detector: the frozen 40-row blind arm should report exactly 16 mismatches: eight excerpt rows and eight unavailable rows, all printed drifted. The remaining states should match. Sources: .ufo/waves/round-36/count-c1.py:70-72,378-488,537-560.

## Frozen hash verification

Before scoring, ran `timeout 20 sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py` (exit 0). Output:

```text
ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
```

Both match .ufo/waves/round-36/evidence/freeze.txt:3-4. The same sha256sum check was repeated immediately before scoring and after restoration, unchanged.

## Full scored counter receipt

Environment: MORI_R36_SCRATCH=/fast/scratch/hyaku/mori-r36/CtlK3, TMPDIR=/fast/scratch/hyaku/mori-r36/CtlK3, PYTHONDONTWRITEBYTECODE=1. These contain temporary writes; the frozen counter is unmodified (.ufo/waves/round-36/count-c1.py:60,529-539).

Command (no --seed):

```text
timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py 6bd57097 --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K3.py
```

Full stdout:

```text
P-C1: at revision R, tools/mori-source-drift.py classifies every row of a 40-row blind fixture drawn at run time exactly as the counter's hidden truth, and on the lane's own corpus/SOURCES.md at R it agrees with the counter's independent live oracle on every row the oracle classified, with at least 10 oracle-fetched rows including at least one oracle-fresh and one oracle-drifted row.
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=16
blind_mismatch S022 tool=drifted truth=unavailable
blind_mismatch S025 tool=drifted truth=unavailable
blind_mismatch S031 tool=drifted truth=unavailable
blind_mismatch S039 tool=drifted truth=unavailable
blind_mismatch S041 tool=drifted truth=unavailable
blind_mismatch S045 tool=drifted truth=unavailable
blind_mismatch S093 tool=drifted truth=unavailable
blind_mismatch S102 tool=drifted truth=excerpt
blind_mismatch S120 tool=drifted truth=excerpt
blind_mismatch S165 tool=drifted truth=excerpt
blind_mismatch S184 tool=drifted truth=unavailable
blind_mismatch S192 tool=drifted truth=excerpt
blind_mismatch S202 tool=drifted truth=excerpt
blind_mismatch S216 tool=drifted truth=excerpt
blind_mismatch S241 tool=drifted truth=excerpt
blind_mismatch S271 tool=drifted truth=excerpt
real_arm=skipped
C1=unmet
seed=12343793994693165550
```

Stderr: empty. Counter exit: 1. The real arm was not exercised.

## Pristine / mutated / restored probe

The same bounded command ran in all three phases, against the same scratch path. probe.py loads the frozen counter's unchanged blind_arm and uses local replay seed 371036; this is separate from the unseeded scored run above. Source: /fast/scratch/hyaku/mori-r36/CtlK3/probe.py:1-22.

```text
timeout --kill-after=5 120 env MORI_R36_SCRATCH=/fast/scratch/hyaku/mori-r36/CtlK3 TMPDIR=/fast/scratch/hyaku/mori-r36/CtlK3 PYTHONDONTWRITEBYTECODE=1 python3 /fast/scratch/hyaku/mori-r36/CtlK3/probe.py /fast/scratch/hyaku/mori-r36/CtlK3/source.py
```

Pristine output:

```text
tool_sha256 dc4eec402e43eac280ace1e6682cbc518a13900ed5e75cb0ec34d8c20949ae54
probe_seed=371036 (local probe only; scored run has no --seed)
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
blind_probe=pass
```

Mutated only /fast/scratch/hyaku/mori-r36/CtlK3/source.py:62-70 to K3's sha-only classifier. Mutant output:

```text
tool_sha256 c1af37d976e3c21bda8933422bc50ddc045460b31f8291fb12c2c39cd2a79f29
probe_seed=371036 (local probe only; scored run has no --seed)
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=16
blind_mismatch S002 tool=drifted truth=excerpt
blind_mismatch S021 tool=drifted truth=excerpt
blind_mismatch S040 tool=drifted truth=excerpt
blind_mismatch S070 tool=drifted truth=unavailable
blind_mismatch S083 tool=drifted truth=unavailable
blind_mismatch S087 tool=drifted truth=unavailable
blind_mismatch S117 tool=drifted truth=unavailable
blind_mismatch S168 tool=drifted truth=unavailable
blind_mismatch S194 tool=drifted truth=excerpt
blind_mismatch S200 tool=drifted truth=unavailable
blind_mismatch S237 tool=drifted truth=unavailable
blind_mismatch S250 tool=drifted truth=excerpt
blind_mismatch S259 tool=drifted truth=unavailable
blind_mismatch S280 tool=drifted truth=excerpt
blind_mismatch S290 tool=drifted truth=excerpt
blind_mismatch S298 tool=drifted truth=excerpt
blind_probe=fail
probe_exit=1
mutant_equals_control=true
```

Restored the exact pristine classifier. Restored output:

```text
tool_sha256 dc4eec402e43eac280ace1e6682cbc518a13900ed5e75cb0ec34d8c20949ae54
probe_seed=371036 (local probe only; scored run has no --seed)
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
blind_probe=pass
probe_exit=0
```

Mutation result: killed by the blind detector; pristine and restored baselines pass. This is not a claim that the full live predicate passed for the pristine program.

## Restoration and containment evidence

Ran `timeout 20 sha256sum /fast/scratch/hyaku/mori-r36/CtlK3/source.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K3.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py` (exit 0):

```text
dc4eec402e43eac280ace1e6682cbc518a13900ed5e75cb0ec34d8c20949ae54  /fast/scratch/hyaku/mori-r36/CtlK3/source.py
c1af37d976e3c21bda8933422bc50ddc045460b31f8291fb12c2c39cd2a79f29  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K3.py
ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
```

The scratch source's before/after hashes match exactly; its temporary mutant hash matches the retained K3 control. All detector subprocesses completed. No background jobs or services were started. The counter shuts down its local server and removes its fixture (.ufo/waves/round-36/count-c1.py:546-548,561-562). A final read of /fast/scratch/hyaku/mori-r36/CtlK3 listed only source.py (3.0 KB) and probe.py (888 B), with no fixture directories. Lane writes are only the assigned K3.py and this report; no git writes. Tools installed or updated: none.

VERDICT: K3 unmet exit 1
