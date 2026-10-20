# MutContext — round-17 wave-2 context mutation probe

Seat: `MoriR17.MutContext-4`. Date: 2026-10-20. Scope: the two assigned single-clause deletions from a copied wave-2 JSON specification, using the unchanged committed context checker. This is mutation evidence for L1, not an admission or closure judgment.

## Axes and result

Probe axes: named missing-clause detection, byte-exact restoration, and isolated write scope. These are evaluation dimensions, not additional round claims or score changes.

- **Live-journal deletion: KILLED.** Pristine rc0; deletion rc1 with `CONTEXT_MISSING` and exactly `missing: ["no_live_journal_queries"]`; restored rc0.
- **No-background deletion: SURVIVED.** Pristine rc0; deletion still rc0 `CONTEXT_OK`; restored rc0. The requested named red for `no_background_jobs` was not produced. The remaining package-operation sentence satisfies the checker's host-service alternative.
- Both mutations changed only the copied specification's top-level `context` string at line 5. The checker, original specification, and all lane production bytes were left untouched. The active probe copy was restored exactly after each mutation. Retained mutant snapshots and raw receipts remain inside this seat's clone for L1 integration; nothing was deleted.

## Inputs and exact mutation points

Required context was read, including `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/contract.md:109-123` (Amendment A1), `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/PINNED_INPUTS.json:3-15`, `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-17.md:62-75,160-164`, and the binding wave-1 context. Operator tooling rules were read before execution; no installation or update was needed or performed.

Checker executed:

`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext/tools/mori-round17-context-check.py`

Its SHA-256 was `4bb17c3759f80b02f8426686ea60f4960be822aee8869b942460cadaa7bab2ae` before and after the probe, matching the measured-commit pin at `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/PINNED_INPUTS.json:3,11`. The production checker independently had this same digest before and after. This establishes the checker-byte pin, not a separately inspected whole-clone VCS identity.

Original specification:

`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/wave2-spec.json:5`

The already provided clone copy at `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext/.ufo/waves/round-17/wave2-spec.json:5` had identical bytes. A new, byte-exact probe copy was created at:

`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext/.scratch/wave2-probe.json:5`

The original and pristine copy were 73,322 bytes. Each surgical edit replaced only line 5 and was followed by an exact text/UTF-8 comparison against the original with only the assigned deletion. The rest of the JSON, including every item prompt, remained identical.

| Mutant | Exact deleted text, including final space | Mutant bytes | Expected detector |
|---|---|---:|---|
| J | `Never live journal queries (no journalctl). ` | 73,278 | rc1, `CONTEXT_MISSING`, exactly `no_live_journal_queries` |
| B | `No background jobs. ` | 73,302 | rc1, `CONTEXT_MISSING`, exactly `no_background_jobs` |

B was made from the restored original, not from J. The live-journal sentence was present during B. J retained the no-background sentence.

## Commands, bounds, and actual outputs

All detector invocations were foreground, `async=false`, `pty=false`, with a 15-second command timeout and working directory `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext`. No selftest was invoked. `TMPDIR` was set to the assigned clone's `.scratch` on every invocation; no probe output or scratch was written to `/tmp`.

**Command O — original specification** (one invocation):

```sh
env TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext/.scratch PYTHONDONTWRITEBYTECODE=1 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext/tools/mori-round17-context-check.py --spec /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/wave2-spec.json
```

**Command P — identical command for every pristine/mutated/restored probe-copy state**:

```sh
env TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext/.scratch PYTHONDONTWRITEBYTECODE=1 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext/tools/mori-round17-context-check.py --spec /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext/.scratch/wave2-probe.json
```

| Run order | Command / input state | Actual rc | Actual finding / missing | Verdict |
|---:|---|---:|---|---|
| 1 | O / original lane specification | 0 | `CONTEXT_OK` | Original green |
| 2 | P / pristine exact copy | 0 | `CONTEXT_OK` | Valid baseline for J |
| 3 | P / J, live-journal sentence deleted | 1 | `CONTEXT_MISSING`; `["no_live_journal_queries"]` | Killed |
| 4 | P / exact restoration after J | 0 | `CONTEXT_OK` | Restoration green; valid pristine baseline for B |
| 5 | P / B, no-background sentence deleted | 0 | `CONTEXT_OK`; no `missing` key | Survived |
| 6 | P / exact restoration after B | 0 | `CONTEXT_OK` | Restoration green |

The execution tool returns combined process output, not separately captured stdout/stderr. Its returned process text for runs 1, 2, 4, and 6 was identical:

```json
{"claims_runtime_prevention": false, "clause_ids": ["no_broadcast_exact_id", "lane_report_resolution", "no_verification_permission", "pacman_pause", "credential_prohibition", "write_scope", "no_live_journal_queries", "no_tmp_probe_outputs", "no_fleet_root_writes", "no_background_jobs", "no_vcs_mutation", "transcript_fields_only"], "clauses_checked": 12, "contexts": 1, "finding_id": "CONTEXT_OK", "spec_sha256": "6a2dc375e6131ac4c3b2fb342979ff920048e3ee0be9d295237b68ff6760cd2e", "static_only": true}
```

Run 3, J, actual process output (rc1):

```json
{"claims_runtime_prevention": false, "clause_ids": ["no_broadcast_exact_id", "lane_report_resolution", "no_verification_permission", "pacman_pause", "credential_prohibition", "write_scope", "no_live_journal_queries", "no_tmp_probe_outputs", "no_fleet_root_writes", "no_background_jobs", "no_vcs_mutation", "transcript_fields_only"], "clauses_checked": 12, "context_absent": false, "contexts": 1, "contexts_failing": 1, "finding_id": "CONTEXT_MISSING", "missing": ["no_live_journal_queries"], "spec_sha256": "d07b1b70a85cd9569eb26bd2d30611aa6787af267b4995315e5d295727651a49", "static_only": true}
```

The tool additionally reported `Command exited with code 1`; its structured receipt has `details.exitCode: 1` at `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext/.scratch/no-live-journal-run.json:6-12`.

Run 5, B, actual process output (rc0):

```json
{"claims_runtime_prevention": false, "clause_ids": ["no_broadcast_exact_id", "lane_report_resolution", "no_verification_permission", "pacman_pause", "credential_prohibition", "write_scope", "no_live_journal_queries", "no_tmp_probe_outputs", "no_fleet_root_writes", "no_background_jobs", "no_vcs_mutation", "transcript_fields_only"], "clauses_checked": 12, "contexts": 1, "finding_id": "CONTEXT_OK", "spec_sha256": "503cfd25456b32fe4cf0da0fe6c4ca9620de140da7735cddad255a96c6beb6c3", "static_only": true}
```

Raw execution-tool responses, command strings, and state digests are also retained at:

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext/.scratch/no-live-journal-run.json`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext/.scratch/journal-restored-run.json`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext/.scratch/no-background-run.json`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext/.scratch/background-restored-run.json`

## Surviving mutant: specific coverage finding

The production-pinned checker defines `no_background_jobs` with alternatives for background jobs, long-lived processes, **or host services**, at `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext/tools/mori-round17-context-check.py:270-289`. The mention group accepts `host service` at line 276. The prohibition group at lines 285-288 accepts a negative word within its sentence-bounded 60-character window before that term.

B's context contains no remaining `background jobs` phrase, but still contains this unmodified package-operation sentence at `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext/.scratch/wave2-no-background.json:5`:

> All pacman transactions are paused host-wide; never -S/-Sy/-Syu/-U/-R, downgrade, restart host service.

A bounded in-memory application of that exact source regex alternative to B's context returned the following match:

```text
never -S/-Sy/-Syu/-U/-R, downgrade, restart host service
```

The match and the observed absence of a `background jobs` phrase are retained in `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext/.scratch/background-regex-witness.json`. This explains why deleting the independent background-job prohibition does not trigger the requested named red: a narrower service-restart prohibition satisfies the broad host-service alternative. The checker also documents this disjunctive presence rule at its lines 43-45. The finding is therefore specifically that this checker/spec pair does **not independently detect loss of the explicit background-job ban**; it is not a claim that the checker provides runtime prevention or that its other clauses failed.

No additional wording was removed to force a kill, and no checker or contract change was made. A surviving mutant is a coverage finding for L1, not permission for this seat to change the acceptance contract.

## Hashes and exact restoration evidence

| State / artifact | SHA-256 |
|---|---|
| Original specification, before and after | `6a2dc375e6131ac4c3b2fb342979ff920048e3ee0be9d295237b68ff6760cd2e` |
| Provided clone specification, before and after | `6a2dc375e6131ac4c3b2fb342979ff920048e3ee0be9d295237b68ff6760cd2e` |
| Active probe copy, pristine and after each restoration | `6a2dc375e6131ac4c3b2fb342979ff920048e3ee0be9d295237b68ff6760cd2e` |
| J retained snapshot | `d07b1b70a85cd9569eb26bd2d30611aa6787af267b4995315e5d295727651a49` |
| B retained snapshot | `503cfd25456b32fe4cf0da0fe6c4ca9620de140da7735cddad255a96c6beb6c3` |
| Clone and production checker, before and after | `4bb17c3759f80b02f8426686ea60f4960be822aee8869b942460cadaa7bab2ae` |

Retained mutant JSON paths:

- J: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext/.scratch/wave2-no-live-journal.json:5`
- B: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext/.scratch/wave2-no-background.json:5`

Both restoration receipts contain `byte_equal_to_pristine: true`, computed by direct comparison with the original specification captured before mutation. The restored detector outputs independently report the original SHA. The final foreground hash command (rc0) was:

```sh
sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/wave2-spec.json /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext/.ufo/waves/round-17/wave2-spec.json /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext/.scratch/wave2-probe.json /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext/.scratch/wave2-no-live-journal.json /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext/.scratch/wave2-no-background.json /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext/tools/mori-round17-context-check.py /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-round17-context-check.py
```

Its output, in argument order, was:

```text
6a2dc375e6131ac4c3b2fb342979ff920048e3ee0be9d295237b68ff6760cd2e  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/wave2-spec.json
6a2dc375e6131ac4c3b2fb342979ff920048e3ee0be9d295237b68ff6760cd2e  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext/.ufo/waves/round-17/wave2-spec.json
6a2dc375e6131ac4c3b2fb342979ff920048e3ee0be9d295237b68ff6760cd2e  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext/.scratch/wave2-probe.json
d07b1b70a85cd9569eb26bd2d30611aa6787af267b4995315e5d295727651a49  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext/.scratch/wave2-no-live-journal.json
503cfd25456b32fe4cf0da0fe6c4ca9620de140da7735cddad255a96c6beb6c3  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext/.scratch/wave2-no-background.json
4bb17c3759f80b02f8426686ea60f4960be822aee8869b942460cadaa7bab2ae  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutContext/tools/mori-round17-context-check.py
4bb17c3759f80b02f8426686ea60f4960be822aee8869b942460cadaa7bab2ae  /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-round17-context-check.py
```

## Scope discipline and handoff

Only this report and files under the assigned clone's `.scratch` were written. No dispatch, background job, live journal query, build, lint, selftest, package transaction, VCS mutation, host-service action, or production edit was performed. No credentials or OMP transcripts were accessed. No installation/update occurred. No claim about overall C1/C2/C3 admission is made. The assigned mutation probe is complete; the no-background survivor is the strongest finding.
