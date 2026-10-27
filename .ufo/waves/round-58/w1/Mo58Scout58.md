# Mo58Scout58 — C1 pointer-resolution probes

**Scope/revision.** Read the frozen contract and `.ufo/waves/round-58/count-c1.py` at freeze `fe8801120a67c1a6b8899d7d0423839caa09e7d0`; counter SHA-256: `6ecdb627bb55522c258dc484ed5c530cfd6f7c57c6a89b4c38179df4c0f84e4b`. No production or lane files were changed. Fixtures were created under `/fast/scratch/hyaku/mori-r58/Mo58Scout58/` and used the frozen `measure()` implementation with only `LANE` and `FLEET` redirected to fixture repos.

**Observed baseline.** Running the frozen counter against both freeze and entering revisions returned `C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none`, exit 0. All four actual row pointers (`tools/mori-vote-bind.py`, `tools/mori-driver-liveness.py`, and the two round-56 evidence files) exist at both revisions.

**Fixture results.** Each fixture had an active-register-shaped scorecard, ten padding rows, two C1 rows, and a fixture MANIFEST; verdicts below are the exact counter output class for the tested first-row pointer (second pointer remained valid).

| Pointer in fixture row | Verdict | Observation |
|---|---|---|
| `tools/mori-vote-bind.py` | `C1=met ... pointers=ok`, rc 0 | Valid positive control. |
| `tools/no-such-tool.py` | `C1=unmet ... pointers=bad ... failed=pointers`, rc 1 | Missing in-tree pointer is rejected (also covered by frozen selftest). |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-vote-bind.py` | `C1=met ... pointers=ok`, rc 0 | Absolute existing path bypasses the prefix gate; it is not resolved by the counter. |
| `/no/such/abs/path.py` | `C1=met ... pointers=ok`, rc 0 | Absolute nonexistent path also bypasses resolution. |
| `./tools/mori-vote-bind.py` | `C1=met ... pointers=ok`, rc 0 | Leading `./` bypasses required-prefix gate. |
| `Tools/mori-vote-bind.py` | `C1=met ... pointers=ok`, rc 0 | Case-variant prefix bypasses the case-sensitive gate. |
| `README.md` | `C1=met ... pointers=ok`, rc 0 | Suffix qualifies for first gate, but no permitted prefix, so skipped. |
| `tools/` | `C1=met ... pointers=ok`, rc 0 | Prefix passes, but trailing-slash tree path is not rejected as a pointer. |
| `tools/../tools/mori-vote-bind.py` | `C1=unmet ... pointers=bad ... failed=pointers`, rc 1 | Git path lookup rejected this traversal spelling in the fixture. |
| `tools/../../etc/hostname` | `C1=unmet ... pointers=bad ... failed=pointers`, rc 1 | Traversal/out-of-tree spelling rejected. |
| `tools//mori-vote-bind.py` | `C1=unmet ... pointers=bad ... failed=pointers`, rc 1 | Duplicate separator rejected. |
| `tools/mori-vote-bind.py:HEAD` | `C1=unmet ... pointers=bad ... failed=pointers`, rc 1 | Colon suffix is treated as part of path and fails lookup. |
| `tools/later-only.py`, present only in a later commit but measured at its parent | `C1=unmet ... pointers=bad ... failed=pointers`, rc 1 | Wrong-tree/nonexistent-at-measured-revision pointer rejected. |

**Finding.** The frozen check is not an unconditional “every evidence pointer resolved” check: it only invokes `git cat-file -e` when the literal captured string starts with `.ufo/`, `tools/`, or `corpus/`. Absolute paths, leading `./`, case variants, `README.md`, and `tools/` therefore score as met without any pointer lookup. The fixture evidence for this finding is the measured verdict table above; all fixture revisions and the probe driver are reproducible in the named scratch directory. `cat-file -e` correctly rejected the tested missing and wrong-tree pointers that did enter the gate.

**Evidence locations.** Frozen contract: `mori-shokunin/.ufo/waves/round-58/contract.md` (§ C1). Frozen counter: `mori-shokunin/.ufo/waves/round-58/count-c1.py`, `measure()` pointer loop (lines 64–80 in the frozen file). Probe implementation: `/fast/scratch/hyaku/mori-r58/Mo58Scout58/probe.py`; fixture repos: `/fast/scratch/hyaku/mori-r58/Mo58Scout58/case-0` through `case-11`, and `wrong-tree`.
