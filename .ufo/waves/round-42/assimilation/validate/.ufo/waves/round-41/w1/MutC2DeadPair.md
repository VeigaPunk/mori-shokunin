measured 2026-10-24; lane root /home/vgpnk/Projects/shokunin/mori-shokunin

# C2 mutation probe — superseder-in-tip condition on dag-z

Axes named before mutation: (1) eligibility must require both the superseded id and its
superseding row to be present at R; (2) the timing line must therefore be empty on dag-z,
whose only `supersedes S001` row lives on a discarded side branch; (3) the frozen 22-arm
selftest must fail any gate that drops the superseder half of that condition; (4) exact-byte
restoration and lane containment.

Scope: `tools/mori-sources-appendonly.py` eligibility filter at line 362
(`tools/mori-sources-appendonly.py:355-365`) in an isolated clone
`/tmp/mut-c2-deadpair/repo` checked out detached at
`7450722e5f3b4fc6df3d719386ed643af59630e3`. The gate bytes are identical at the
`control-after.txt` receipt revision `aa161e998eb22282e3d96ed2710bb0b39e5163de`
(`git show <rev>:tools/mori-sources-appendonly.py | sha256sum` =
`75af8f6fc63dc736f07c02617bed4bf6c1ad7f880ffb49849b065b4d40d8f76b` for both).

## Detector and baseline qualification

Frozen DAG builder `repo/.ufo/waves/round-41/fixtures/c2/build-dags-r40.py` `build_dag_z`
built `fixture-dag-z`; the assigned detector is the gate run on that fixture, with the
frozen selftest as the second, contract-level detector (C2 frozen target is
`MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0`):

```sh
python3 GATE 01e6c5684606262b7198fe0cbd310e27af40822b \
  --repo /tmp/mut-c2-deadpair/fixture-dag-z \
  --round-base 3e5442dae5f58b0715a81863768025f0dad6b156
python3 GATE --selftest
```

Pristine gate, sha256 `75af8f6fc63dc736f07c02617bed4bf6c1ad7f880ffb49849b065b4d40d8f76b`:

```text
EXIT=0
appendonly_violations=1 ids=[] deleted=[S002] superseded=[] round_changed=[]
supersede_timing superseded_as_of=[] stale_supersede=[]
MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0
```

This reproduces `evidence/control-after.txt:166-173` byte for byte, including the fixture
SHAs (`b0=3e5442da…`, `m=01e6c568…`, `s1=024f6d7f…`, `c1=f29c20f3…`) and matching
`control-before.txt:113-119`. Baseline is green; a mutant is judgeable.

## Mutant — remove the superseder-in-tip condition

Single-line, behavior-bearing change at `tools/mori-sources-appendonly.py:362`:

```diff
-        if target in tip and by in tip:
+        if target in tip:
```

The comment above it ("Only pairs whose target and superseder both survive at R are
eligible.") was deliberately left untouched: it is not behavior-bearing, so the mutation
stays minimal. Mutated sha256 `9e154b2cf3085a450f12c745dcb37e7849d952378f6a56995208bdacee5ca395`.

Expected: S002 is deleted at R, so its discarded landing makes (S001, S002) eligible under
the weakened filter; S001 was first sighted at `b0`, which is an ancestor of the side
landing `s1` (`024f6d7f…`), so S001 must come back as **as-of**, not stale.

Observed mutant:

```text
EXIT=0
appendonly_violations=1 ids=[] deleted=[S002] superseded=[S001] round_changed=[]
supersede_timing superseded_as_of=[S001] stale_supersede=[]
```

S001 returns on the timing line, and the tuple is exactly the v3 defect signature in
`evidence/control-before.txt:119-120` (`superseded=[S001]`,
`superseded_as_of=[S001] stale_supersede=[]`) — the mutated gate reverts dag-z to the
pre-fix behaviour while still exiting 0.

Frozen selftest on the mutant:

```text
FAIL discarded superseder is ineligible at R: superseded: want [] got ['S001']; superseded_as_of: want [] got ['S001']
FAIL discarded edit and superseder do not decide timing: superseded: want [] got ['S001']; superseded_as_of: want [] got ['S001']
MORI_SOURCES_APPENDONLY_SELFTEST pass=20 fail=2
```

Both r41 dag-z/z2 arms (`tools/mori-sources-appendonly.py:862-874`) fire; no other arm
regressed, so the two failures localize the removed condition rather than a broad breakage.

VERDICT: **killed** — by the frozen selftest's dag-z/z2 expectations (2/22 fail; contract
frozen target 22/0 is violated). The external dag-z run alone is discriminating but not
sufficient: pristine and mutant both exit 0 and both keep
`appendonly_violations=1 ids=[] deleted=[S002]`; only the timing line separates them, and
the selftest is the frozen instrument that encodes that line.

## Restoration

`cp -p pristine-gate.py repo/tools/mori-sources-appendonly.py` restored exact bytes:
sha256 back to `75af8f6fc63dc736f07c02617bed4bf6c1ad7f880ffb49849b065b4d40d8f76b`, equal to
the preserved pristine copy and to the receipt-revision blob. Re-run on restored bytes:

```text
EXIT=0
appendonly_violations=1 ids=[] deleted=[S002] superseded=[] round_changed=[]
supersede_timing superseded_as_of=[] stale_supersede=[]
MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0
```

Restored output is identical to the baseline run, so the mutant read is attributable to the
one-line change and not to fixture or environment drift.

## Containment

All writes were under `/tmp/mut-c2-deadpair` (clone, fixture, receipts, pristine copy) plus
this report. No lane file, Git index, jj state, `.ufo/state` or watchdog file was touched;
no sibling repo was opened; no subagent was dispatched; no tool was installed or updated.
The scratch copy was restored anyway, so it is byte-equal to the lane tip for this file.
