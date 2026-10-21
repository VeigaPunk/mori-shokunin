# C3 artifact privacy review

## Verdict

**Low severity: limited operational/workspace metadata exposure; no confirmed private-session, credential, operator-configuration-value, or other-lane-private-state disclosure in the refusal texts, slot-grant fields, responses, or registry.** Most observed detail is same-lane agent identifiers and counts, as asked about. The residual task-call also persists the lane workspace's absolute path and revision context; that is a host-location disclosure beyond IDs/counts, but not an environment/config value.

## Evidence by path and line

- `.ufo/waves/round-18/wave1-attempts.json:10` — one slot-grant record with wave/lane labels and aggregate live/pending/cap counts. **Kind:** scheduler occupancy/capacity metadata; no individual other-lane identity or private host setting.
- `.ufo/waves/round-18/wave1-task-response.txt:1-70` — spawn acknowledgement and same-lane agent/job identifiers; line 1 gives the total. `:71` is coordination text, not a private value. **Kind:** IDs/count and workflow instruction only.
- `.ufo/waves/round-18/residual-drafting-attempts.json:10,24,37,50,63,76,89` — initial and repeated slot-grant references with aggregate counts. `:12,26,39,52,65,78,91` — refusal text repeats same-lane job identifiers and a generic background-job-cap rejection. **Kind:** IDs, retry/capacity counts, and scheduler saturation status; no session identifiers, host environment values, or operator config values observed.
- `.ufo/waves/round-18/residual-drafting-response.txt:1-13` — seven refusal records/headings repeat the same job identifiers and scheduler-cap rejection. **Kind:** same-lane IDs and process-capacity status only; no other-lane state observed.
- `.ufo/waves/round-18/residual-drafting-taskcall.json:5` — persisted task context includes the workspace's absolute home-directory path and branch/revision provenance. `:10-45` — per-item prompts identify lane work items and source/report paths. **Kind:** workspace-location and lane-provenance metadata beyond IDs/counts; no personal-document path, credential, email, or operator configuration value found. A scan for the frozen C1 marker families matched only instruction text that names restricted categories, not private values.
- `.ufo/waves/round-18/build/swarm-registry.json:8-415` — registry members are same-lane IDs with role/kind and null item fields; `:4-6` contains build time/report-directory metadata. **Kind:** same-lane roster and build metadata, not another lane's private state or session-record content.

The frozen C3 contract at `.ufo/waves/round-18/frozen/c3-ledger-format.json:14-19` requires an exact `refused_text` and defines slot-grant/attempt fields, which explains the raw scheduler message being retained; it does not make the scheduler-cap detail private configuration.

## Exploit path and impact

A reader of the committed lane artifacts can correlate the workspace location/revision context with aggregate queue counts and the reported job-cap rejection to infer where this worktree resides and when the shared runner was saturated. This is minor operational reconnaissance; these artifacts do not provide credentials, session identities, personal-document contents, operator routing values, or identities/state from other lanes. No evidence supports a stronger claim.

## Smallest remediation

For future dispatch payloads, replace persisted absolute workspace paths with lane-relative/opaque paths. If the scheduler-cap detail is not needed for adjudication, revise the next frozen C3 schema to store a normalized refusal category (and necessary count) instead of backend refusal prose; retain the current committed ledger unchanged because its exact-text binding is part of the frozen contract. No remediation edit was in scope here.

## Provenance and checks

SHA-256 of reviewed artifacts:

- `.ufo/waves/round-18/wave1-attempts.json` — `88556dc335acd7994820cd31b97a34f77174baaf249f10d277f83a752d5c7bfc`
- `.ufo/waves/round-18/wave1-task-response.txt` — `f4c880e7a196a3e22b6b199991792d3db3d8c3d637e95e66453f328ecbd9c2d2`
- `.ufo/waves/round-18/residual-drafting-attempts.json` — `0e330c333b04f1acc49c19ab4a60f2314e4f23c894ecba58d337b0b97c426f55`
- `.ufo/waves/round-18/residual-drafting-response.txt` — `4226b8178455ace76a330a0a1913184dbbc62a250deb4046e8a3eaf8dde20cc0`
- `.ufo/waves/round-18/residual-drafting-taskcall.json` — `9fbd918af8b7ac1f9d7bff1f070c38e83726797bb2540dd7906b5216402fc68e`
- `.ufo/waves/round-18/build/swarm-registry.json` — `942fce91a6010bfcd7cac8b7c0451891b596ac49e628ba41e80655a45d098bdc`

`sha256sum` completed with exit code 0. Static reads/search only; no tests, VCS operations, or tool installs were run.