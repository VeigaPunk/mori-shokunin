measured 2026-10-23T11:50:18Z
control K5 shape denial
control_sha256 e24689da7e1ae48d8cc1a0fe9cfda63bd45ae7b1cc77ec6b08667a2d7ebf0e3a
counter_sha256 ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145

Axes: contract fidelity, detector discrimination, exact-byte restoration, containment.

## Mutant and expected detector

Program: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K5.py`.
The single behavior-bearing mutation is its `LABEL_MAP` assignment at line 13: fresh→drifted, excerpt→drifted, drifted→fresh. Unavailable and no-copy are unchanged. Classification precedes the map; printed rows, summary counts and drifted exit status use the mapped states. The normal rules and CLI are frozen at `.ufo/waves/round-36/contract.md:33-47`; this denial shape is listed at line 95.
Expected rejection: the blind fixture has eight rows per state (`contract.md:49-52`), so the map should create 24 mismatches and leave the other 16 rows unchanged. A failed blind arm must skip the real arm (`contract.md:57-58`).

## Frozen hash gate

Before scoring, command `timeout 30 sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py` exited 0 and printed:

```text
ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
```

Both match `.ufo/waves/round-36/evidence/freeze.txt:3-4`; the same hashes were observed after scoring.

## Required scored run — full counter output

Command (no `--seed`):

```text
timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py 6bd57097 --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K5.py
```

```text
P-C1: at revision R, tools/mori-source-drift.py classifies every row of a 40-row blind fixture drawn at run time exactly as the counter's hidden truth, and on the lane's own corpus/SOURCES.md at R it agrees with the counter's independent live oracle on every row the oracle classified, with at least 10 oracle-fetched rows including at least one oracle-fresh and one oracle-drifted row.
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=24
blind_mismatch S001 tool=drifted truth=fresh
blind_mismatch S005 tool=fresh truth=drifted
blind_mismatch S011 tool=drifted truth=fresh
blind_mismatch S036 tool=fresh truth=drifted
blind_mismatch S043 tool=drifted truth=fresh
blind_mismatch S048 tool=drifted truth=excerpt
blind_mismatch S052 tool=drifted truth=fresh
blind_mismatch S054 tool=fresh truth=drifted
blind_mismatch S071 tool=fresh truth=drifted
blind_mismatch S094 tool=drifted truth=fresh
blind_mismatch S118 tool=drifted truth=excerpt
blind_mismatch S119 tool=fresh truth=drifted
blind_mismatch S130 tool=drifted truth=fresh
blind_mismatch S137 tool=drifted truth=fresh
blind_mismatch S145 tool=drifted truth=excerpt
blind_mismatch S166 tool=drifted truth=excerpt
blind_mismatch S184 tool=drifted truth=excerpt
blind_mismatch S210 tool=drifted truth=excerpt
blind_mismatch S216 tool=fresh truth=drifted
blind_mismatch S219 tool=fresh truth=drifted
real_arm=skipped
C1=unmet
seed=9998184821099527509
```

Counter exit: 1. No stderr was emitted. The counter prints only the first 20 mismatches (`count-c1.py:554-557`), accounting for the displayed list of 20 despite the total of 24. The real-input arm was not exercised.

## Pristine / mutated / restored probe

Isolated file: `/fast/scratch/hyaku/mori-r36/CtlK5/probe.py`. Pristine and restored bytes have `LABEL_MAP = {}`; only line 13 was changed for the mutation. Each command below runs the same `/fast/scratch/hyaku/mori-r36/CtlK5/detect.py`, calling the frozen counter's `blind_arm` with replay seed 360005 and a 30-second tool bound. This replay seed is supplemental, not the scored counter seed. Detector SHA256 from `timeout 30 sha256sum`: `1336ade0266b68a16c1b6d048fa24beb6b5974034f8100b40e8505e29fd5fb61`.

Command: `timeout 90 python3 /fast/scratch/hyaku/mori-r36/CtlK5/detect.py pristine`; exit 0:

```text
stage=pristine
probe_sha256=728a4691fd263baf9f838ab385b9689fba2b77175b4867cb69a8f9526eaf9eeb
counter_sha256=ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145 blind_seed=360005 timeout=30
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
blind_detector=met
detector_exit=0
```

Command: `timeout 90 python3 /fast/scratch/hyaku/mori-r36/CtlK5/detect.py mutated`; exit 1:

```text
stage=mutated
probe_sha256=e24689da7e1ae48d8cc1a0fe9cfda63bd45ae7b1cc77ec6b08667a2d7ebf0e3a
counter_sha256=ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145 blind_seed=360005 timeout=30
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=24
blind_mismatch S037 tool=drifted truth=excerpt
blind_mismatch S041 tool=drifted truth=fresh
blind_mismatch S051 tool=fresh truth=drifted
blind_mismatch S057 tool=drifted truth=fresh
blind_mismatch S059 tool=drifted truth=excerpt
blind_mismatch S076 tool=drifted truth=fresh
blind_mismatch S080 tool=drifted truth=excerpt
blind_mismatch S095 tool=drifted truth=fresh
blind_mismatch S108 tool=fresh truth=drifted
blind_mismatch S121 tool=drifted truth=excerpt
blind_mismatch S135 tool=fresh truth=drifted
blind_mismatch S137 tool=drifted truth=fresh
blind_mismatch S158 tool=fresh truth=drifted
blind_mismatch S174 tool=drifted truth=excerpt
blind_mismatch S183 tool=drifted truth=fresh
blind_mismatch S188 tool=drifted truth=excerpt
blind_mismatch S205 tool=fresh truth=drifted
blind_mismatch S209 tool=fresh truth=drifted
blind_mismatch S210 tool=drifted truth=fresh
blind_mismatch S225 tool=fresh truth=drifted
blind_detector=unmet
detector_exit=1
```

Command: `timeout 90 python3 /fast/scratch/hyaku/mori-r36/CtlK5/detect.py restored`; exit 0:

```text
stage=restored
probe_sha256=728a4691fd263baf9f838ab385b9689fba2b77175b4867cb69a8f9526eaf9eeb
counter_sha256=ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145 blind_seed=360005 timeout=30
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
blind_detector=met
detector_exit=0
```

Restoration evidence: `timeout 15 sha256sum /fast/scratch/hyaku/mori-r36/CtlK5/probe.py` exited 0 and independently printed `728a4691fd263baf9f838ab385b9689fba2b77175b4867cb69a8f9526eaf9eeb`, identical to the pristine hash. The mutated scratch hash equals the retained scored control hash. Pristine/restored pass, so this is not a baseline-failure finding.

All invoked commands completed in the foreground. No background jobs or services were retained; the blind detector closes its HTTP server and removes its fixture in `count-c1.py:546-548,561-562`. Lane writes were limited to this report and the assigned K5 control; probe files are in the assigned scratch directory. No git writes, lane commits, installations, or tool updates were performed.

VERDICT: isolated-mutation killed pristine-exit 0 mutated-exit 1 restored-exit 0
VERDICT: K5 unmet exit 1
