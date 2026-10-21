# C1 frozen-population adjudication — round-2 interactive-cutover evidence

## Scope and result

Reviewed the six frozen hit rows for the five assigned files at base `29b0dc7` (the two WWKD rows refer to the same line). The frozen policy allows a hit only when its line has no private-source values and qualifies under A, B, or C. The five evidence/artifact records do not qualify as surface-only instructions, lane tool code/contracts/synthetic fixtures, or non-author files. The single WWKD line is a boundary statement naming an authority surface and its key names without exposing values; those two rows are allowable under A.

Result for this scope: **4 redact rows; 2 allow-a rows**. The WWKD allow decisions apply only to line 29, not to other configuration-derived values later in the file. The frozen summary reports 119 total hits, 3 non-author hits, and 116 metric hits; this is a scoped adjudication, not a new metric run.
## Findings by severity

- **High — redact:** the four evidence/output rows listed below expose or point to operator configuration; their adjacent or serialized metadata also contains route values/fingerprints. The whole-file sweep found concrete alias/provider/model-route values beyond the C1 regex hits.
- **Allowed — no line-level redaction:** the two WWKD hits at line 29 only name an authority surface and key names in a read-only boundary statement. This does not clear WWKD lines 31–34.
- **Medium — privacy metadata outside the metric:** the sweep found event/run timestamps, a generic session-material location/status, an external workspace location, and an operator-config-derived route-mismatch fact. The report identifies each by path and line without reproducing values.

## Residual risk and verification gaps

This is limited to the five assigned blobs at the frozen base; the C1 policy itself treats regex classes as a recall floor, and no claim is made about other paths or the post-redaction metric. The gate was not run and no artifact was modified. No build/test/lint/formatter was run; none was required for this read-only adjudication.


## Per-row decisions and minimal replacements

- `.ufo/round-2/interactive-cutover/wave/admission.json:12` — **R7, redact**. This is an evidence-record value identifying operator configuration, not a contract naming a surface. Preserve the non-sensitive blocked verdict and plan counts (planned/unique/dispatched/task-batch), plus a generic route-preflight state. Remove the configuration locator and its paired configuration fingerprint at line 13; remove the concrete role-to-alias/fallback mapping and config-derived mismatch details elsewhere in this record (listed below). Preserve the original frozen C1 class and line digest in the sanitized provenance/report rather than retaining the private configuration fingerprint.
- `.ufo/round-2/interactive-cutover/wave/plan-command.json:15` — **R7, redact**. This is serialized command output, not an instruction or synthetic fixture. Preserve the command result/exit status and non-sensitive planned-wave totals. Replace the embedded private route-preflight material with a redacted projection: remove the configuration locator/fingerprint, alias and provider/model hop values, and the role-to-family routing map. Preserve the original C1 class and line digest in the report/retention record.
- `.ufo/round-2/interactive-cutover/wwkd.md:29` — **R7, allow-a**; **R8, allow-a**. The line is a read-only boundary statement that names an authority surface and key names without their values. No routing table values occur on that line. No broader exemption applies to the file.
- `corpus/evidence/round-1-cgroup-dispatch.json:11` — **R7, redact**. This is an evidence-record pointer to operator configuration, not a surface-only contract statement. Preserve the dispatch scope/outcome/counts; remove the locator and its paired configuration fingerprint at line 12. Keep the original C1 class and line digest in the provenance/report.
- `corpus/evidence/round-2/dispatch.json:7` — **R7, redact**. This is an evidence-record authority pointer. Preserve round/transport/dispatch outcome and non-sensitive counts; remove the locator and paired configuration fingerprint at line 8, as well as the specific operator-override mismatch detail at line 10. Keep the original C1 class and line digest in the provenance/report.

The C1 `line_sha256` values below are frozen hashes of the pre-redaction lines; they are distinct from configuration-file fingerprints, which must not be retained in sanitized artifacts. No files other than this report were changed.

## Whole-file sweep: private context missed by frozen regexes

The following are outside the frozen C1 metric; each entry gives only a path, line, and kind, not the sensitive value.

| Path:line | Missed context kind |
|---|---|
| `.ufo/round-2/interactive-cutover/wave/admission.json:2` | Run-specific event timestamp / history metadata; the frozen session-identity pattern does not cover this timestamp form. |
| `.ufo/round-2/interactive-cutover/wave/admission.json:18-19,24-25,30-31,36-37,42-43,48-49,54-55,60` | Concrete actual/required role aliases and connector fallback routing values; the regexes detect routing-table keys, not these values. |
| `.ufo/round-2/interactive-cutover/wave/admission.json:65` | Config-derived routing mismatch/status fact, without the key token that triggers the frozen classes. |
| `.ufo/round-2/interactive-cutover/wave/plan-command.json:11` | Local workspace path outside the lane (filesystem-location metadata). |
| `.ufo/round-2/interactive-cutover/wave/plan-command.json:12-13` | Command start/finish timestamps, a historical execution fact not covered by the session-identity pattern. |
| `.ufo/round-2/interactive-cutover/wave/plan-command.json:15` | Serialized stdout contains concrete route-family aliases, provider/model hop identifiers, role-to-family mappings and related routing detail; the C1 hit detects the embedded config reference but not these values. |
| `.ufo/round-2/interactive-cutover/wwkd.md:9` | Generic session-material location and commit-status metadata; no session-specific filename is reproduced here. |
| `.ufo/round-2/interactive-cutover/wwkd.md:31-34` | Concrete configured/required role aliases, fallback and role binding state, plus the derived mismatch fact; the frozen routing-key class does not match these values. |
| `corpus/evidence/round-1-cgroup-dispatch.json:4` | Timestamped historical run label / history metadata, not matched by the frozen session-identity pattern. |
| `corpus/evidence/round-1-cgroup-dispatch.json:12` | Configuration fingerprint adjacent to the matched authority pointer; the digest alone does not match the path class. |
| `corpus/evidence/round-2/dispatch.json:8` | Configuration fingerprint adjacent to the matched authority pointer; the digest alone does not match the path class. |
| `corpus/evidence/round-2/dispatch.json:10` | Operator-config-derived role-override mismatch fact, without a matched routing key or explicit alias value. |

No transcript-body excerpt or numbered tool-output artifact identity was observed in these five files. The historical dispatch records and serialized plan output are evidence/planning data, not transcript bodies; their private routing and history metadata are identified above.

## Read-only method and command evidence

Read the round contract first, then frozen C1 population/policy and the C2/C3 frozen inputs. The frozen rows were selected with `jq '.hits[] | select(.path=="<assigned-path>")'` for each of the five paths. Each hit context was opened at base `29b0dc7` using `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 29b0dc7:<path> | sed -n '<line-range>p'`, with three lines of surrounding context. Each of the five complete blobs was then read using `git show 29b0dc7:<path>`; the long plan stdout was continued from the returned artifact so the file was reviewed in full. Read-only line-numbered views were used to locate the additional metadata rows above. All commands produced output without a reported tool failure; the shell interface did not emit numeric exit statuses, so **exit 0 is inferred from successful completion**. No tests, build, lint, formatter, install, or mutation was run.

## Frozen population rows

```json
[
  {"path":".ufo/round-2/interactive-cutover/wave/admission.json","line":12,"class":"R7","line_sha256":"3d1896a836062a52dae07cde08930676b1e833af5bc95dccb244fdcc1139760a","decision":"redact","reason":"Evidence-record value identifies private operator configuration; neither a surface-only instruction nor an eligible field/key-name fixture."},
  {"path":".ufo/round-2/interactive-cutover/wave/plan-command.json","line":15,"class":"R7","line_sha256":"39ddf124c7175a0984c165105af858c5dcf434d1089a7e302eb48ae62bd831ba","decision":"redact","reason":"Serialized plan output contains a private configuration reference and route data; it is not an instruction, contract, or synthetic fixture."},
  {"path":".ufo/round-2/interactive-cutover/wwkd.md","line":29,"class":"R7","line_sha256":"d211e02da331900c57ac61fa5148ced3e06a0bc39472930a0258757141ee8ae8","decision":"allow-a","reason":"Read-only boundary statement names the authority surface without exposing its contents."},
  {"path":".ufo/round-2/interactive-cutover/wwkd.md","line":29,"class":"R8","line_sha256":"d211e02da331900c57ac61fa5148ced3e06a0bc39472930a0258757141ee8ae8","decision":"allow-a","reason":"Same boundary statement names configuration keys only; no routing-table values appear on this line."},
  {"path":"corpus/evidence/round-1-cgroup-dispatch.json","line":11,"class":"R7","line_sha256":"4b68e5fa88138342a7e7de6168308da19c54abab3c16acb224d0221d7fa25d11","decision":"redact","reason":"Evidence-record pointer to operator configuration, not a surface-only instruction or non-author file."},
  {"path":"corpus/evidence/round-2/dispatch.json","line":7,"class":"R7","line_sha256":"3ae95c1d81070f85f246facae78576a6c32ddfe2c582be8e52308f56a6fa36f8","decision":"redact","reason":"Evidence-record authority pointer to operator configuration; related private route state is also present in the file."}
]
```