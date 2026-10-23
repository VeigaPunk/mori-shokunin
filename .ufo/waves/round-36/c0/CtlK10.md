measured 2026-10-23T11:50:43Z
control K10 shape server echo / length-only
control_sha256 755b63929ce3cabf52036ca2e0db9fbc49d2e538857d1af789345e5aaddeb720
counter_sha256 ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145

## Mutation and expected detector

Axes: defect fidelity, detector sensitivity, exact restoration.

The control compares fetched body length with copy length: equal becomes fresh, longer becomes excerpt, shorter becomes drifted. It retains the latest-copy selection, no-copy handling, GET-error classification, registry-order output, summary and CLI. The only behavior mutation is the classifier function at `.ufo/waves/round-36/c0/controls/K10.py:40-45`; body length is the permitted alternative to Content-Length in the assigned shape.

Expected detector: the frozen blind arm should reject same-length changed bytes reported as fresh and unrelated longer bodies reported as excerpt. The contract requires byte equality or actual contiguous excerpt membership, not size agreement (`.ufo/waves/round-36/contract.md:39-47`). The blind generator creates both drift shapes (`.ufo/waves/round-36/count-c1.py:439-453`).

## Frozen-counter scoring

Both counter hashes matched the supplied freeze before scoring. Command (exit 0):

```text
timeout 20 sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
```

Scored command, without --seed:

```text
env MORI_R36_SCRATCH=/fast/scratch/hyaku/mori-r36/CtlK10 PYTHONDONTWRITEBYTECODE=1 timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py 6bd57097 --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K10.py
```

Full counter output:

```text
P-C1: at revision R, tools/mori-source-drift.py classifies every row of a 40-row blind fixture drawn at run time exactly as the counter's hidden truth, and on the lane's own corpus/SOURCES.md at R it agrees with the counter's independent live oracle on every row the oracle classified, with at least 10 oracle-fetched rows including at least one oracle-fresh and one oracle-drifted row.
blind_rows=40 tool_exit=0 tool_rows=40 mismatches=8
blind_mismatch S001 tool=fresh truth=drifted
blind_mismatch S007 tool=excerpt truth=drifted
blind_mismatch S018 tool=excerpt truth=drifted
blind_mismatch S038 tool=fresh truth=drifted
blind_mismatch S066 tool=fresh truth=drifted
blind_mismatch S140 tool=excerpt truth=drifted
blind_mismatch S247 tool=excerpt truth=drifted
blind_mismatch S265 tool=excerpt truth=drifted
real_arm=skipped
C1=unmet
seed=8768210406604010270
```

Counter process exit: 1. The real arm was skipped, not passed.

## Paired mutation probe and exact restoration

The isolated scratch implementation began with the contract-correct hash/subsequence classifier. Only that function was replaced by the submitted length-only classifier, then restored. All three phases used the same frozen `blind_arm`, seed 3610 and 30-second tool timeout. This paired detector is separate from the unseeded scored receipt above. Driver: `/fast/scratch/hyaku/mori-r36/CtlK10/detect.py` (SHA-256 49a97e5b65367ce5fe4f59d7bf5e547412056f8b7d48bc0b8d905ee6971063f6).

Each phase ran this command with the indicated final argument:

```text
timeout 120 env PYTHONDONTWRITEBYTECODE=1 MORI_R36_SCRATCH=/fast/scratch/hyaku/mori-r36/CtlK10 python3 /fast/scratch/hyaku/mori-r36/CtlK10/detect.py pristine
```

Actual pristine output; process exit 0:

```text
phase=pristine
tool_sha256=c0d6af1c543829a5771e7c70b042877770565dea9e6c6dd6c26482d128793b03
detector=frozen_count_c1.blind_arm seed=3610 tool_timeout=30
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
detector=pass
detector_exit=0
```

Same command with final argument mutated; process exit 1:

```text
phase=mutated
tool_sha256=755b63929ce3cabf52036ca2e0db9fbc49d2e538857d1af789345e5aaddeb720
detector=frozen_count_c1.blind_arm seed=3610 tool_timeout=30
blind_rows=40 tool_exit=0 tool_rows=40 mismatches=8
blind_mismatch S071 tool=excerpt truth=drifted
blind_mismatch S096 tool=excerpt truth=drifted
blind_mismatch S130 tool=fresh truth=drifted
blind_mismatch S137 tool=fresh truth=drifted
blind_mismatch S172 tool=excerpt truth=drifted
blind_mismatch S238 tool=excerpt truth=drifted
blind_mismatch S247 tool=excerpt truth=drifted
blind_mismatch S250 tool=excerpt truth=drifted
detector=fail
detector_exit=1
```

Same command with final argument restored; process exit 0:

```text
phase=restored
tool_sha256=c0d6af1c543829a5771e7c70b042877770565dea9e6c6dd6c26482d128793b03
detector=frozen_count_c1.blind_arm seed=3610 tool_timeout=30
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
detector=pass
detector_exit=0
```

Mutation outcome: killed. Pristine and restored phases both passed; neither was an inconclusive baseline failure. The mutated scratch hash exactly matches the submitted K10 control hash. The restored scratch hash exactly matches its pristine hash; the requested defective lane control remains available for integration-owner review.

Post-score command and output (exit 0):

```text
timeout 20 sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K10.py /fast/scratch/hyaku/mori-r36/CtlK10/probe-tool.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
755b63929ce3cabf52036ca2e0db9fbc49d2e538857d1af789345e5aaddeb720  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K10.py
c0d6af1c543829a5771e7c70b042877770565dea9e6c6dd6c26482d128793b03  /fast/scratch/hyaku/mori-r36/CtlK10/probe-tool.py
ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
```

All invoked foreground commands returned. The detector and counter close their local server and reap the tested subprocess before returning (`.ufo/waves/round-36/count-c1.py:277-284,537-562`). No background job or git write was started. No tools were installed or updated.

VERDICT: K10 unmet exit 1
