# C1 retention-gate mutation probe

## Scope and axes

Date: 2026-10-21. Advisory falsification only; no integration or round-admission judgment.

- **Coverage:** whether the existing bounded selftest rejects each assigned behavioral defect.
- **Calibration:** distinguish an observed selftest pass from coverage of every frozen C1 rule.
- **Adjacency:** preserve the no-private-text reporting boundary.
- **Operability:** run one mutant at a time, with passing pristine/restored detectors and exact restoration hashes.

Attacked revision: `e2bfbd6f8dccc51fc06455efc41f720301112dd4`. Requirement freeze: `29b0dc79e193b9d67845e39850a091a84bad66bd`. The only source edited was the assigned isolated clone's `tools/mori-retention-gate.py`:

`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/MutRetentionGate/tools/mori-retention-gate.py`

The lane checkout's source was not edited. Each edit was reversed before applying the next mutant. No subagents, additional behavioral harness, live host probes, installations, or upgrades were used.

## Authorities read

All references here are lane-relative unless an absolute clone path is stated.

- `.ufo/waves/round-18/contract.md:24-29,47-61`: C1 metric, failure capability, exit conventions, privacy boundary, allowlist binding and snapshot integrity.
- `.ufo/waves/round-18/frozen/c1-policy.json:5-29`: any-NUL binary exclusion, per-class hits, non-author exclusion, mandatory-redaction paths and recall-floor qualification.
- `.ufo/waves/round-18/frozen/c1-population.json:1-10`: frozen enumeration metadata, 119 total / 3 non-author / 116 metric hits, including 40 mandatory-redaction hits. These are read input values, not measurements rerun by this probe.
- `.ufo/waves/round-18/frozen/c2-register.json:1-43` and `frozen/c3-ledger-format.json:1-22` were read for the shared contract; neither tool was executed or modified.
- `.ufo/waves/round-18/draft-verdicts.md:6-10,21-23` and `out-of-metric-triage.md:3-6,20-31`: L1's provisional reading and separately carried reading-sweep debt.

The findings below qualify the retention selftest's behavioral coverage. They do not independently remeasure C1 at the attacked revision or adjudicate L1's claimed before/after improvement. The policy's out-of-metric reading-sweep limitation remains distinct from the in-metric selftest gaps found here.

## Commands and original result

Every detector invocation used this exact command, with working directory `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/MutRetentionGate` and a 60-second command deadline:

```sh
TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/MutRetentionGate/.scratch GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 PYTHONDONTWRITEBYTECODE=1 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/MutRetentionGate/tools/mori-retention-gate.py --selftest
```

**Original, pristine result B0:** stdout `SELFTEST retention-gate PASS 19/19`; exit **0**.

The selftest itself creates throwaway Git fixture repositories beneath the assigned `$TMPDIR`, using isolated Git configuration (`tools/mori-retention-gate.py:398-418,457-500,517`). No direct VCS mutation command was run against either the lane or clone repository.

The exact hashing command was run on B0, every mutant, and every restoration; all 17 invocations exited **0**:

```sh
sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/MutRetentionGate/tools/mori-retention-gate.py
```

A read-only pin check also exited **0** and produced the same original digest:

```sh
git -C /home/vgpnk/Projects/shokunin/mori-shokunin show e2bfbd6f8dccc51fc06455efc41f720301112dd4:tools/mori-retention-gate.py | sha256sum
```

Original SHA-256, called **H0** below:

`9d42f403373d976405e804251ed4a5d010eb648f05c05e02cd909d08a8e52d05`

## Mutant table and actual outputs

All source locations refer to the original tool at the attacked revision. Each mutant changed only the listed expression, guard, or insertion point; selftest assertions were not edited. The expected arm is source-derived **[INFERENCE]**: the detector prints an aggregate result, not individual failed-arm names.

| ID | Single-point mutant | Expected detector / source arm [INFERENCE] | Actual mutant stdout | Exit | Verdict |
|---|---|---|---|---:|---|
| M1 | At `tools/mori-retention-gate.py:96`, require `class_id != "R9"` in addition to the regex match, dropping R9 hits. | Positive R9 arm in `:520-528` requires one R9 hit and `RETENTION_FINDINGS`. | `SELFTEST retention-gate FAIL 18/19` | 1 | **Killed** |
| M2 | At `:264`, remove `not` from the non-author exclusion predicate, retaining non-author hits instead of author hits in the metric. | Non-author exclusion arm at `:613-631`, plus the author-hit positives, should reject inverted metric membership. | `SELFTEST retention-gate FAIL 8/19` | 1 | **Killed** |
| M3 | At `:241`, make the mandatory-path allowlist guard `False and row["path"] in must_paths`, bypassing `allowlist_forbidden`. | Forbidden allowlist arm at `:564-589` requires exit 1, stable finding ID, metric/routed 1 and one forbidden row. | `SELFTEST retention-gate FAIL 18/19` | 1 | **Killed** |
| M4 | At `:265`, replace tuple membership with `and hit["path"] not in {key[0] for key in allowed_keys}`. An accepted row suppresses every hit in that path, ignoring class and digest on the hit-side comparison. Row validation itself remains unchanged. | A same-path, different-hit binding arm is needed; the existing allowlist-match/stale arms (`:539-562,591-611`) do not distinguish this defect. | `SELFTEST retention-gate PASS 19/19` | 0 | **Survived** |
| M5 | Insert `break` immediately after the append at `:102`, counting only the first matched class on each line. | A textual multi-class-line arm is needed; individual class positives (`:520-528`) and the binary-skipped combination (`:536-537`) do not distinguish this defect. | `SELFTEST retention-gate PASS 19/19` | 0 | **Survived** |
| M6 | Insert `"matched_text": line,` in the hit dictionary after `:101`, exposing matched line content in emitted JSON. | Output-minimization arm at `:649-660` checks its synthetic marker against stdout and stderr. | `SELFTEST retention-gate FAIL 18/19` | 1 | **Killed** |
| M7 | At `:344`, change snapshot digest comparison from `!=` to `==`, allowing the whitespace-tampered snapshot past the digest check. | Tampered snapshot arm at `:642-647` requires exit 2 and `snapshot_tampered`. | `SELFTEST retention-gate FAIL 18/19` | 1 | **Killed** |
| M8 | At `:90`, change the binary signature from `b"\0"` to `b"\0\0"`, treating the existing single-NUL binary fixture as text. | Binary-skip arm at `:536-537` requires a clean result with no hits. | `SELFTEST retention-gate FAIL 18/19` | 1 | **Killed** |

Observed totals: **8 mutants; 6 killed; 2 survived; 0 inconclusive**. The result is scoped to these eight mutations and this detector. No baseline failed.

## Pristine/restored sequence

The execution order was `B0, M1, R1, M2, R2, M3, R3, M4, R4, M5, R5, M6, R6, M7, R7, M8, R8`: **17 detector invocations**. A restored run doubles as the next mutant's pristine run, avoiding an identical redundant invocation without omitting either side of any probe.

| Mutant | Pristine detector run | Restored detector run | Actual stdout for both pristine/restored runs | Both exits |
|---|---|---|---|---:|
| M1 | B0 | R1 | `SELFTEST retention-gate PASS 19/19` | 0 |
| M2 | R1 | R2 | `SELFTEST retention-gate PASS 19/19` | 0 |
| M3 | R2 | R3 | `SELFTEST retention-gate PASS 19/19` | 0 |
| M4 | R3 | R4 | `SELFTEST retention-gate PASS 19/19` | 0 |
| M5 | R4 | R5 | `SELFTEST retention-gate PASS 19/19` | 0 |
| M6 | R5 | R6 | `SELFTEST retention-gate PASS 19/19` | 0 |
| M7 | R6 | R7 | `SELFTEST retention-gate PASS 19/19` | 0 |
| M8 | R7 | R8 | `SELFTEST retention-gate PASS 19/19` | 0 |

## Before / mutant / after SHA-256

H0 means the full original digest printed above, not an omitted measurement. Every before/after entry is supported by that run's hashing command. Mutant digests differ from H0; every inverse edit restored H0 before the next mutation.

| Mutant | Before | Mutated tool SHA-256 | Restored after |
|---|---|---|---|
| M1 | H0 | `0d91436c40fc75e7a20b9d4e97ffd8e3a03064615cdeff02d97c5d07024a56da` | H0 |
| M2 | H0 | `ac5e606a91531dcc58678328ec140bba0bf006c4a5757060e96abd4520e3c81f` | H0 |
| M3 | H0 | `196f327f60fa1b1dc02925440ab8d1978d42b3743fd302846b112254246919ed` | H0 |
| M4 | H0 | `ef4071ea97b8bbd182fe4c15314d1c5e06f8ee57eac6835be30760b7ea233aaa` | H0 |
| M5 | H0 | `413286837349e3af75ba893eabdd982d8041afebb4586711947e27b03dd8fd15` | H0 |
| M6 | H0 | `b0d6262a83c13742e31ec4a03a7042372d0bcfb0ed110fe9ffc754ea8ebef90a` | H0 |
| M7 | H0 | `c6651bc1dddf39ea3c0425a723ea23d0f8911b1380a69ee40b3117301f608d8e` | H0 |
| M8 | H0 | `3f285aa71d08d289e8c6b7a84bd8da649e14e38329ff2909c3a70a146bfe5788` | H0 |

**Final restoration evidence:** R8 passed 19/19 with exit 0; the final tool SHA-256 is H0, also matching the read-only hash of the attacked revision's original blob. Restoration used inverse surgical edits, not Git checkout/reset or repository-state mutation.

## Survivors: missing detector arms

These are proposed detector obligations **[INFERENCE]**, not new tests implemented or exercised in this assignment.

### M4 — path-only allowlist suppression

The current matching arm supplies one hit and its exact allowlist row; the stale arm points at an absent path. Neither checks that other hits in an already-allowlisted file remain findings (`tools/mori-retention-gate.py:539-562,591-611`).

**Missing arm:** commit one synthetic file with two distinct lines matching the same class and allowlist only the first line's exact digest. Require exit **1**, finding ID `RETENTION_FINDINGS`, metric **1**, exactly one allowlisted hit and exactly the second hit unallowlisted. A companion variant with different classes in the same file can independently exercise the class dimension.

**[INFERENCE] Expected discriminatory behavior:** the original tuple comparison keeps the second hit; M4's path-only predicate suppresses both, incorrectly making the metric zero. This challenges frozen exact row binding, not the policy's outside-regex recall floor (`contract.md:55-60`).

### M5 — first class only per line

Each positive fixture is tested separately. The existing fixture containing multiple class tokens is intentionally binary and must be skipped before any textual matching (`tools/mori-retention-gate.py:505-537`).

**Missing arm:** use a single textual line matching two different classes. The existing binary-skip fixture with its NUL removed would supply such a synthetic case. Require exit **1**, finding ID `RETENTION_FINDINGS`, metric **2**, and two hit records with the same path, line and line digest but different class IDs. Do not assert only a nonzero exit or the finding ID: both remain identical under M5.

**[INFERENCE] Expected discriminatory behavior:** the original class loop reports both hits; the inserted `break` reports only the first. This is a missing assertion of per-class counting within the frozen metric (`c1-policy.json:28`; `tools/mori-retention-gate.py:94-103`).

## Handoff

The existing selftest catches the assigned single-class omission, exclusion inversion, forbidden-allowlist bypass, matched-text emission, snapshot-integrity inversion, and weakened binary check. It does **not** catch the two assigned semantic weakenings above. A 19/19 selftest pass therefore cannot by itself establish exact allowlist binding or multi-class-per-line counting.

No contract changes, tool fixes, or new selftest arms were made. The source is restored; this report is the only retained deliverable outside the assigned clone. No tool installation/update occurred. Further detector changes and any round-level disposition remain with L1.
