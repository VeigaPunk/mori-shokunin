# Wave 2 falsification — JSON token redactions

Scope: read-only diff of `d005cdd..e2bfbd6` for the four assigned JSON files. The lane tip was inspected through commit-addressed reads; no VCS mutation, install, build, test, or LSP operation was performed.

## Findings by severity

### Medium — operator routing values remain in the admission record

`.ufo/round-2/interactive-cutover/wave/admission.json:18-19,24-25,30-31,36-37,42-43,48-49,54-55,60` contains **15 `@`-prefixed route-handle values**: seven actual/required role pairs plus the connector fallback requirement. The adjacent configuration-path value at line 12 was redacted, but the assignment values themselves remain. These are routing values, not name-only mentions; the L1 triage calls operator OMP configuration/routing values private (`.ufo/waves/round-18/out-of-metric-triage.md:10-13`). The frozen C1 rule permits name-only material only when the line carries no private-source value (`.ufo/waves/round-18/frozen/c1-policy.json:27`). This finding is outside the frozen R1–R9 regex classes, not an R8 key hit. **Do not quote or allowlist the alias values.**

### Medium — command-capture metadata retains a home-rooted working directory and run timestamps

`.ufo/round-2/interactive-cutover/wave/plan-command.json:11-13` retains the command `cwd` value and its start/finish times immediately before the redacted `stdout` value at line 15. The `cwd` is a home-rooted workspace path outside the reviewed Mori lane and exposes an account/path identifier; the timestamp fields are captured run-record values. `.ufo/round-2/interactive-cutover/wave/admission.json:2` also retains an `observedAt` timestamp in the same admission record. These are not C1 regex hits. **[INFERENCE]** The account component is operator-identifying and the timestamps are session/run-derived; this classification follows the round-18 out-of-metric rule for personal identities and session-record values (`out-of-metric-triage.md:10-13`), but no source configuration or session material was inspected.

## Redaction, allowlist, and technical checks

- The frozen C1 population records one baseline R7 (`operator_config_ref`) hit in each assigned file: `admission.json:12` (line SHA-256 `3d1896a836062a52dae07cde08930676b1e833af5bc95dccb244fdcc1139760a`); `plan-command.json:15` (`39ddf124c7175a0984c165105af858c5dcf434d1089a7e302eb48ae62bd831ba`); `round-1-cgroup-dispatch.json:11` (`4b68e5fa88138342a7e7de6168308da19c54abab3c16acb224d0221d7fa25d11`); and `round-2/dispatch.json:7` (`3ae95c1d81070f85f246facae78576a6c32ddfe2c582be8e52308f56a6fa36f8`). The corresponding path/config-line references were replaced with an explicit withheld-value placeholder. A read-only frozen-regex scan of the four `e2bfbd6` blobs returned **0** matches. Separate pattern counts: route-handle values **15**, ISO timestamps **3**, retry-named JSON key/value matches **0**, email-shaped values **0**.
- All four tip blobs parse as JSON with `python3 -m json.tool` (each command used `set -o pipefail` and exited 0): admission 1,950 formatted bytes; plan-command 46,420; round-1 dispatch 2,736; round-2 dispatch 1,490. The replacements preserve string-valued fields and do not break JSON structure. The captured `stdout` is intentionally no longer byte-faithful to the original output at the redacted reference; no other technical break was observed.
- L1's decision to retain **field/key names, record-type names, role labels, surface/transport names, and lane seat names** is allowlistable: these are structural or lane-local names without private source values under the frozen adjudication rule and triage (`c1-policy.json:27`; `out-of-metric-triage.md:14-16`). The route-handle strings above are value-bearing role-to-route assignments, so they do not qualify for that allowance.

## Residual risk [INFERENCE]

The config-path redactions leave the same 64-hex config digest in `admission.json:13`, `corpus/evidence/round-1-cgroup-dispatch.json:12`, and `corpus/evidence/round-2/dispatch.json:8`. This is a stable content fingerprint rather than a name-only mention and permits cross-record correlation of the config version. It is not a frozen C1 hit, and this review did not inspect the source config; the remaining risk is correlation, not demonstrated recovery of config contents. Retain it only with an explicit provenance justification, otherwise redact it as well.

## Evidence identity and commands

SHA-256 of the four `e2bfbd6` blobs (for the line references above):

| Lane-relative path | SHA-256 |
|---|---|
| `.ufo/round-2/interactive-cutover/wave/admission.json` | `40dbdc79f4146165cefb5e14adee2ee42e3988e2d302c3880dc519862e95282b` |
| `.ufo/round-2/interactive-cutover/wave/plan-command.json` | `353fb542eb25d882be0dcd7202224c35f43c92bba16cd4844a0a3283e1154d45` |
| `corpus/evidence/round-1-cgroup-dispatch.json` | `6e940f55156c772c1dd087b31622f6073f056c9b971b011b7d776185305b44a8` |
| `corpus/evidence/round-2/dispatch.json` | `0f706e4f7e02435d8c0f839d7719eaaea78f0c62b436f51426291ee3ef71e812` |

Read-only diffs were run for each requested path with `git diff -U6 d005cdd e2bfbd6 -- <path>` from the lane repository; all completed successfully (exit 0). JSON validation commands were `git show e2bfbd6:<path> | python3 -m json.tool | wc -c` with `set -o pipefail`; all exited 0. Read-only `git grep` pattern/count checks and `sha256sum` commands also completed; no installs or updates were made. No LSP device was available in the tool inventory; the reviewed artifacts are JSON records, not source definitions with caller/diagnostic semantics. The command summary was rewritten before handoff to remove an unnecessary absolute checkout path; no route aliases or config-fingerprint values were quoted.
