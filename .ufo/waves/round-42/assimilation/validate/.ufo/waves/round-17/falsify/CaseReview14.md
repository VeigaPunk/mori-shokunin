# CaseReview14 — C1 MaxFiles cases

## Axes and scope

This review attacks **C1 coverage (axis 6)** only: `max_files_exceeded` and `max_files_two_allowed`, their `MaxFiles` source bytes, expected rows, classifier, gate comparison, and retained before/after receipts. C2 (7) and C3 (5) were not reviewed here. The contract describes this tool as detection/report-only, never editing, resuming, or rerouting sessions (`.ufo/waves/round-17/contract.md:9-14`); canonical-runtime, rerouting, and resume-preflight properties therefore are not exercised by these two cases.

LSP availability was checked first: `read xd://lsp` returned “No such tool” and listed no LSP device. I used source reads for semantic review; grep, where used, was only for locating code.

## Findings (by severity)

### Medium — `max_files_exceeded` accepts an unrelated setup failure

The fixture is a genuine overflow input: `MaxFiles` contains exactly `max-a.jsonl` and `max-b.jsonl` (both are pinned in `fixtures/seat/expected.json:28-29`); the case sets `--max-files 1` (`expected.json:730-741`). The contract specifically requires this condition to stop with `rc2` and `reason=too-many-files` (`contract.md:39-40`). The current implementation does take the right branch: `_scan` appends regular `.jsonl` paths and raises `_SetupError("too-many-files", ...)` when `len(discovered) > max_files` (`tools/mori-seat-terminal.py:420-439`); the retained stdout is `{"files_seen":2,...,"max_files":1,"reason":"too-many-files",...}` (`evidence/seat-after/runs/max_files_exceeded.stdout:1`). The after manifest records `status=match`, `rc=2`, and `finding_id=MORI_SEAT_TERMINAL_SETUP` (`evidence/seat-after/run-manifest.json:1`).

However, the case oracle only requires `rc=2` and `finding_id=MORI_SEAT_TERMINAL_SETUP`; it has no expected reason (`expected.json:738-741`). The gate cannot express one: `WANT_KEYS` is only `rc`, `finding_id`, `totals`, and `seats` (`tools/mori-round17-seat-regressions.py:214-216`). For `rc2`, the gate explicitly allows implementation-defined diagnostics and does not require totals/seats (`.../mori-round17-seat-regressions.py:104-107`, `:657-695`). In `evaluate`, rc2 bypasses top-level-key restrictions (`:1301-1305`), and comparison checks schema/finding/optional `sessions_dir` but never checks `reason` (`:1297-1325`, `:1449-1458`).

**Static counterexample:** for this case's correct sandbox and `rc=2`, an implementation returning `{"schema":"mori-seat-terminal-v1","finding_id":"MORI_SEAT_TERMINAL_SETUP","reason":"invalid-max-files","sessions_dir":"<the expected sandbox>"}` satisfies every comparison this row declares. It would still match even though it rejected the bound for an unrelated reason rather than detecting two files above a limit of one. Thus this case does not falsify a broken overflow branch; current output is correct, but its recorded `match` does not prove the specific setup condition. The tool's own static selftest does expect `reason=too-many-files` (`tools/mori-seat-terminal.py:1192-1210`), but the measured per-case gate does not use that assertion; no selftest was run in this review.

### No finding — `max_files_two_allowed` has source-backed, non-vacuous class assertions

The pinned source bytes support the independently declared expected classes. `max-a.jsonl` has a v3 session header followed by an assistant `stop` (`fixtures/seat/MaxFiles/max-a.jsonl:1-2`), which is `completed` (`tools/mori-seat-terminal.py:247-255`). `max-b.jsonl` has a v3 header and a terminal assistant error at `completedAt=1760998000000`, with status 429 and `429 rate_limit` (`fixtures/seat/MaxFiles/max-b.jsonl:1-2`). The fixed `--now-ms 1761000000000` and default 900-second settle window make that error 2,000 seconds old; the classifier therefore reaches the rate-limit branch and returns `dead_rate_limit` (`tools/mori-seat-terminal.py:257-273`; `expected.json:744-768`). The expected row explicitly pins all eight totals, including zeroes, and both seat classes, rather than accepting an empty class result.

The retained after stdout has `files_scanned=2`, `rc=1`, `MORI_SEAT_TERMINAL_DEAD`, exactly the declared two seat classes, and the expected totals (`evidence/seat-after/runs/max_files_two_allowed.stdout:1`). The manifest records `status=match`, `seat_count=2`, `files_scanned=2`, `now_ms=1761000000000`, and the same totals (`evidence/seat-after/run-manifest.json:1`). The gate checks exact declared totals and seats and validates files-scanned count (`tools/mori-round17-seat-regressions.py:1215-1260`, `:1428-1436`). This is a real boundary control at two files allowed; taken with the overflow input, it distinguishes the exact `1`/`2` thresholds, subject to the missing reason assertion above.

Current inputs are independently pinned: `PINNED_INPUTS.json:13` pins `expected.json`; the after receipt says 81 pins verified, with no missing, extra, or mismatched inputs (`evidence/seat-after/run-manifest.json:1`). The before receipt has the same two case IDs as `capability_absent` with `observed=null`; the after receipt has both as `match` (`evidence/seat-before/run-manifest.json:1`, `evidence/seat-after/run-manifest.json:1`). Before is capability absence, not a behavioral baseline for these inputs.

## Read-only receipt count

Command:

```sh
jq -s '[.[].cases[] | select(.id == "max_files_exceeded" or .id == "max_files_two_allowed")] | {records:length, counts:(group_by(.status) | map({status:.[0].status,count:length})), rows:map([.id,.status])}' \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-before/run-manifest.json \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-after/run-manifest.json
```

Observed `jq_rc=0`; output:

```json
{"records":4,"counts":[{"status":"capability_absent","count":2},{"status":"match","count":2}],"rows":[["max_files_exceeded","capability_absent"],["max_files_two_allowed","capability_absent"],["max_files_exceeded","match"],["max_files_two_allowed","match"]]}
```

## Residual risk and verification gaps

The actionable falsifier is limited to the `max_files_exceeded` **gate oracle**: its current tool output is correct, but the gate accepts unrelated rc2 setup diagnostics. `max_files_two_allowed` is supported and fully class-asserted. No tool invocation, selftest, build, or lint was run; the only command executed was the read-only receipt count above. LSP was unavailable as noted. These cases establish no behavior about production routing, same-identity rerouting, resume continuity, or a broader saturation policy.