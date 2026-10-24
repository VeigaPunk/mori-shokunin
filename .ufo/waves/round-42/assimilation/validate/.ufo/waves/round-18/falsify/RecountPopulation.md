# C1 frozen-baseline independent recount

## Reconstructed contract and scope

C1 measures class-regex hits in tracked blobs at the measured revision, excluding files matched by the non-author globs; the routed sub-count is hits in the three `must_redact_paths` files. The frozen policy defines the blob/binary/line-decoding scope and all nine regex classes (`frozen/c1-policy.json:5-15`), the routed paths and non-author globs (`:17-25`), and the metric (`:28`). The contract freezes the before count at d005cdd as 116, with 40 routed hits (`contract.md:24-29`). This assignment independently recounts that baseline only; it does not run or validate the retention gate, later revisions, allowlist decisions, or the out-of-metric reading sweep.

## Evidence chain and method

- Inputs: policy `frozen/c1-policy.json` and population `frozen/c1-population.json`, whose declared commit is `d005cdde0e009dea6c0cc29b37163de536528658` (`c1-population.json:2-10`). The policy SHA-256 recomputed from its bytes was `db06e9810bbfd243fb0a753a46960573df39083ea90174ce463cf2a0ab523128`, equal to the digest recorded in the population (`c1-population.json:4`).
- Ran a throwaway Python standard-library enumeration with `TMPDIR` removed from the process environment; no scratch or output files were created. It used the policy's regexes and classifications, `re`/`json`/`hashlib`/`fnmatch`, and retained output in memory. It enumerated the revision's 5,105 blob entries, skipped NUL-containing binary blobs, decoded UTF-8 with replacement, split on LF, and recorded one hit for each matching `(path, line, class)`.
- Read-only Git commands (both exit 0): `git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree -r -z d005cdd`; `git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file --batch`.
- Comparison was exact for all 119 hit records, including `(path, line, class, line_sha256)`: no frozen records missing from the enumeration and no extra enumerated records. The frozen summary and independent summary agree in every requested aggregate (`c1-population.json:5-10`).

## Recount

Total hits: **119** across **28** files; non-author: **3**; `must_redact`: **40**; metric before: **116** (`119 - 3`). The 40 routed hits are the three policy-listed files: PacmanActorTrace **18**, OmpRetryConfig **17**, SessionExitCorrelation **5** (`c1-policy.json:17-21`). The three non-author hits are in `corpus/lessons/round-17-verifier-spotcheck.md`.

Per class:

| Class | Hits |
|---|---:|
| R1 | 22 |
| R2 | 30 |
| R3 | 9 |
| R4 | 3 |
| R5 | 4 |
| R6 | 6 |
| R7 | 13 |
| R8 | 11 |
| R9 | 21 |
| **Total** | **119** |

Per file (lane-relative path, hit count):

| File | Hits |
|---|---:|
| `.ufo/round-2/interactive-cutover/wave/admission.json` | 1 |
| `.ufo/round-2/interactive-cutover/wave/plan-command.json` | 1 |
| `.ufo/round-2/interactive-cutover/wwkd.md` | 2 |
| `.ufo/waves/round-16/build/AttackPermission.md` | 2 |
| `.ufo/waves/round-17/build/CriticC1.md` | 2 |
| `.ufo/waves/round-17/build/DeadSeatCrossCheck.md` | 6 |
| `.ufo/waves/round-17/build/OmpRetryConfig.md` | 17 |
| `.ufo/waves/round-17/build/OmpRetryDocs.md` | 3 |
| `.ufo/waves/round-17/build/OverlapTsukuroi.md` | 1 |
| `.ufo/waves/round-17/build/PacmanActorTrace.md` | 18 |
| `.ufo/waves/round-17/build/PacmanTxnToday.md` | 1 |
| `.ufo/waves/round-17/build/RetryRecoveryShape.md` | 2 |
| `.ufo/waves/round-17/build/ReviewC1Contract.md` | 2 |
| `.ufo/waves/round-17/build/ReviewSchemaDrift.md` | 1 |
| `.ufo/waves/round-17/build/ReviewSeatBreachDetect.md` | 3 |
| `.ufo/waves/round-17/build/SeatNaming.md` | 3 |
| `.ufo/waves/round-17/build/SentinelTranscripts.md` | 2 |
| `.ufo/waves/round-17/build/SessionExitCorrelation.md` | 5 |
| `.ufo/waves/round-17/build/TranscriptShapes.md` | 5 |
| `.ufo/waves/round-17/build/TranscriptTailBounds.md` | 2 |
| `.ufo/waves/round-17/evidence/seat-live.json` | 4 |
| `.ufo/waves/round-17/falsify/ConformanceAudit.md` | 8 |
| `.ufo/waves/round-17/wave1-dispatch.json` | 11 |
| `.ufo/waves/round-17/wave1-spec.json` | 11 |
| `corpus/evidence/round-1-cgroup-dispatch.json` | 1 |
| `corpus/evidence/round-2/dispatch.json` | 1 |
| `corpus/lessons/round-17-verifier-spotcheck.md` | 3 |
| `corpus/lessons/round-17.md` | 1 |

## Divergence from L1 and confidence

No disagreement: the independent recount confirms the `116` before metric, `40` routed hits, and `population_match true` stated in the provisional C1 row (`draft-verdicts.md:8`). No differing `path:line:class` exists to report. The out-of-metric triage explicitly treats its reading-sweep disposition as separate from C1 (`out-of-metric-triage.md:3-6`); its substantive decisions, and the later C1 after-state, are not tested here.

Confidence is high for the frozen regex population and arithmetic: the recorded policy digest and every hit record matched. This is not evidence that the regex metric detects all private context; the policy describes the classes as a recall floor and says reading-sweep findings remain outside the metric (`c1-policy.json:28-29`). No tools were installed or updated.
