measured 2026-10-23T11:49:31Z
control K6 shape word bag
control_sha256 33e2e39f23cc62ea72c2b014ca77812e3a6f250046d7c3ff7b3d01f25bb07c71
counter_sha256 ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145

## Mutant and expected detector

Axes: row coverage, detector discrimination, byte integrity.

The only behavioral defect is choosing each row's state independently using `random.SystemRandom().choice` from the five contract states instead of classifying source/copy bytes. Registry order, per-row output, summary counts, drifted exit status, and unreadable-registry exit 2 are retained. Source: `.ufo/waves/round-36/c0/controls/K6.py:11-39`; interface: `.ufo/waves/round-36/contract.md:33-47`; assigned shape: contract line 96.

Expected detector: exact per-row comparison in `.ufo/waves/round-36/count-c1.py:545-560`. [INFERENCE] Random decisions should fail the blind arm; the frozen counter then skips the real arm (`count-c1.py:702-706`).

## Scored command and full counter output

No `--seed` was supplied. Both temporary-directory variables confine counter-created files to this seat's scratch directory.

```sh
timeout 900 env MORI_R36_SCRATCH=/fast/scratch/hyaku/mori-r36/CtlK6 TMPDIR=/fast/scratch/hyaku/mori-r36/CtlK6 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py 6bd57097 --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K6.py
```

```text
P-C1: at revision R, tools/mori-source-drift.py classifies every row of a 40-row blind fixture drawn at run time exactly as the counter's hidden truth, and on the lane's own corpus/SOURCES.md at R it agrees with the counter's independent live oracle on every row the oracle classified, with at least 10 oracle-fetched rows including at least one oracle-fresh and one oracle-drifted row.
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=31
blind_mismatch S007 tool=drifted truth=no-copy
blind_mismatch S030 tool=fresh truth=unavailable
blind_mismatch S034 tool=fresh truth=drifted
blind_mismatch S036 tool=fresh truth=excerpt
blind_mismatch S059 tool=unavailable truth=drifted
blind_mismatch S085 tool=excerpt truth=unavailable
blind_mismatch S111 tool=excerpt truth=unavailable
blind_mismatch S117 tool=drifted truth=fresh
blind_mismatch S128 tool=unavailable truth=excerpt
blind_mismatch S131 tool=unavailable truth=drifted
blind_mismatch S134 tool=no-copy truth=excerpt
blind_mismatch S135 tool=drifted truth=excerpt
blind_mismatch S136 tool=no-copy truth=drifted
blind_mismatch S140 tool=unavailable truth=excerpt
blind_mismatch S148 tool=drifted truth=unavailable
blind_mismatch S156 tool=drifted truth=no-copy
blind_mismatch S169 tool=fresh truth=drifted
blind_mismatch S180 tool=drifted truth=fresh
blind_mismatch S188 tool=fresh truth=no-copy
blind_mismatch S194 tool=unavailable truth=no-copy
real_arm=skipped
C1=unmet
seed=7206816400573689971
```

Counter exit code: 1. The blind arm rejected the control with 31 mismatches among 40 emitted rows; the output above is the complete counter output, which reports at most 20 individual mismatches (`count-c1.py:554-557`).

VERDICT: K6 unmet exit 1

## Baseline and restoration evidence

The control is an additive substitute, not a replacement of an existing tool. Before and after the scored run, the same frozen detector was run with its default pristine-tool selection:

```sh
timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py 6bd57097
```

Pristine-selection output, exit 1:

```text
P-C1: at revision R, tools/mori-source-drift.py classifies every row of a 40-row blind fixture drawn at run time exactly as the counter's hidden truth, and on the lane's own corpus/SOURCES.md at R it agrees with the counter's independent live oracle on every row the oracle classified, with at least 10 oracle-fetched rows including at least one oracle-fresh and one oracle-drifted row.
tool_absent
C1=unmet
```

Restored/default-selection output, exit 1:

```text
P-C1: at revision R, tools/mori-source-drift.py classifies every row of a 40-row blind fixture drawn at run time exactly as the counter's hidden truth, and on the lane's own corpus/SOURCES.md at R it agrees with the counter's independent live oracle on every row the oracle classified, with at least 10 oracle-fetched rows including at least one oracle-fresh and one oracle-drifted row.
tool_absent
C1=unmet
```

Thus a conventional pristine/mutated/restored killed-mutant classification is inconclusive: the pristine tool is absent, not passing. This is not reported as a killed mutant. The required substitute-control score is independently `unmet` as recorded above. No original program bytes existed to restore; no existing source bytes were changed. The assigned new control is retained as requested.

Before scoring, `timeout 30 sha256sum` on the two frozen counters produced the pinned hashes below, matching `.ufo/waves/round-36/evidence/freeze.txt:3-4`. The control was also hashed before scoring. After scoring, this command reproduced all three hashes exactly:

```sh
timeout 30 sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K6.py
```

```text
ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
33e2e39f23cc62ea72c2b014ca77812e3a6f250046d7c3ff7b3d01f25bb07c71  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K6.py
```

Scratch inspection with `read /fast/scratch/hyaku/mori-r36/CtlK6` returned `(empty directory)` after the scored command completed. Counter cleanup shuts down/closes its server and removes the fixture (`count-c1.py:546-548,561-562`). All launched commands completed synchronously; no background jobs were started. No git writes were issued. Tool installations/updates: none.
