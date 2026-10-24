# MutQuota — C1 quota-precedence mutation probe

## Scope and axes

- **Claim attacked:** C1 coverage, specifically quota classification taking precedence over generic HTTP429/rate-limit classification. This is a single assigned mutation probe, not independent round closure or an admission judgment.
- **Axes held:** behavioral discrimination (named cases reject the old false rate-limit result), reproducibility (pinned gate and unchanged fixtures), privacy (only derived detector outputs, no raw transcript fields), and isolation/restoration (one scratch-copy mutation; exact original bytes restored).
- Owner: `MoriR17.MutQuota-4`. Isolated clone: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota`.
- Contract authority: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/contract.md:109-123`, especially A1 quota-before-rate tokens at line112 and vendor codes1113/1308 before HTTP429 at line123. The original rate-before-quota language is superseded.
- Read the requested contract, pinned inputs and lesson, binding wave context, operator installation rules and applicable skill guidance before probing. No production implementation, sibling clone, VCS metadata, fleet script or admission state was modified.

## Mutant and expected detector

**Mutant:** move the existing four-line generic HTTP429/rate-token branch ahead of both vendor-code and quota-token tests in `_classify`. Role, stop reason, settle-window, schema, scanning and output behavior remain untouched. The behavior-bearing source span is `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/tools/mori-seat-terminal.py:259-273`.

The only edited executable was the additional copy at `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.scratch/quota-tool/mori-seat-terminal.py`; the clone's source tool remained pristine. A retained mutant snapshot is `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.scratch/quota-probe/mutant-mori-seat-terminal.py` (mutated branch at lines262-265).

**Expected detector:** run the unchanged committed seat-regression gate over the unchanged cloned fixtures. Cases `code_quota_1113_beats_429` and `code_quota_1308_beats_429` must reject the mutant's `dead_rate_limit` output because each expects `dead_quota`. Their persisted expectations are `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.ufo/waves/round-17/fixtures/seat/expected.json:1235-1284`.

The additional ordering case has the historical literal name `rate_limit_beats_quota_by_status_and_token`, but its actual expected values are **two dead_quota seats**, not rate-limit seats (`expected.json:262-287` at the same absolute fixture path). This report uses the persisted expected values, not the misleading case-name wording. `code_rate_1302_beats_quota_token` is the named unchanged rate-limit control (`expected.json:1285-1308`).

Exact mutation diff, also retained at `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.scratch/quota-probe/mutation.diff`:

```diff
--- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/tools/mori-seat-terminal.py
+++ /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.scratch/quota-tool/mori-seat-terminal.py
@@ -259,6 +259,10 @@
     terminal_ms = view["terminal_ms"]
     if terminal_ms is not None and terminal_ms > now_ms - settle_seconds * 1000:
         return "error_unsettled"
+    if view["error_status"] == 429 or any(
+        token in error_message for token in RATE_TOKENS
+    ):
+        return "dead_rate_limit"
     error_code = view["error_code"]
     if error_code in QUOTA_CODES:
         return "dead_quota"
@@ -266,10 +270,6 @@
         return "dead_rate_limit"
     if any(token in error_message for token in QUOTA_TOKENS):
         return "dead_quota"
-    if view["error_status"] == 429 or any(
-        token in error_message for token in RATE_TOKENS
-    ):
-        return "dead_rate_limit"
     return "dead_error_other"
```

## Executed commands, boundedness and actual outputs

All three runs used the same gate, tool-copy path and fixtures; only tool bytes and a fresh output directory differed. No selftest, build, linter or live transcript probe ran. Gate subprocesses have the committed gate's unchanged timeout/output caps; each outer invocation additionally had a180-second deadline. Execution was synchronous with no background jobs.

Working directory for every invocation: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota`.

Explicit environment supplied to each gate:

```json
{"PATH":"/usr/local/bin:/usr/bin:/bin","HOME":"/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.scratch/home","XDG_CONFIG_HOME":"/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.scratch/xdg-config","TMPDIR":"/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.scratch","LC_ALL":"C.UTF-8","PYTHONDONTWRITEBYTECODE":"1"}
```

Exact gate argv:

```json
["/usr/bin/python3","/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/tools/mori-round17-seat-regressions.py","--tool","/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.scratch/quota-tool/mori-seat-terminal.py","--fixtures","/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.ufo/waves/round-17/fixtures/seat","--output","/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.scratch/quota-probe/pristine"]
["/usr/bin/python3","/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/tools/mori-round17-seat-regressions.py","--tool","/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.scratch/quota-tool/mori-seat-terminal.py","--fixtures","/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.ufo/waves/round-17/fixtures/seat","--output","/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.scratch/quota-probe/mutated"]
["/usr/bin/python3","/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/tools/mori-round17-seat-regressions.py","--tool","/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.scratch/quota-tool/mori-seat-terminal.py","--fixtures","/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.ufo/waves/round-17/fixtures/seat","--output","/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.scratch/quota-probe/restored"]
```

| Stage | Gate rc | Actual stdout (one newline terminated line) | Actual stderr | Summary |
|---|---:|---|---|---|
| Pristine | 0 | `GATE ok: 54/54 cases matched (.scratch/quota-probe/pristine)` | empty |54 matched;0 mismatched;0 capability absent;0 packs changed |
| Mutated | 1 | `GATE mismatch: 51/54 cases matched (.scratch/quota-probe/mutated)` | empty |51 matched;3 mismatched;0 capability absent;0 packs changed |
| Restored | 0 | `GATE ok: 54/54 cases matched (.scratch/quota-probe/restored)` | empty |54 matched;0 mismatched;0 capability absent;0 packs changed |

Per-stage exact argv, rc, stdout/stderr bytes and stream digests are retained in:

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.scratch/quota-probe/pristine-command.json`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.scratch/quota-probe/mutated-command.json`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.scratch/quota-probe/restored-command.json`

The corresponding raw gate streams are retained alongside those receipts as `pristine.stdout`/`pristine.stderr`, `mutated.stdout`/`mutated.stderr` and `restored.stdout`/`restored.stderr`, all within the absolute quota-probe directory above. Detailed case manifests are:

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.scratch/quota-probe/pristine/run-manifest.json`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.scratch/quota-probe/mutated/run-manifest.json`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.scratch/quota-probe/restored/run-manifest.json`

## Named-case discrimination and safe stream excerpt

| Named case | Persisted expected class(es) | Pristine status | Mutated output class(es) / status | Restored status |
|---|---|---|---|---|
| `code_quota_1113_beats_429` | `code-1113: dead_quota` | match | `dead_rate_limit` / mismatch | match |
| `code_quota_1308_beats_429` | `code-1308: dead_quota` | match | `dead_rate_limit` / mismatch | match |
| `rate_limit_beats_quota_by_status_and_token` | `status-beats-quota` and `token-beats-quota`: both `dead_quota` | match | both `dead_rate_limit` / mismatch | match |
| `code_rate_1302_beats_quota_token` (control) | `code-1302-quota: dead_rate_limit` | match | `dead_rate_limit` / match | match |

Tool subprocess rc stayed1 for these error cases on all three stages. The kill is therefore the gate's rejection of incorrect classification, **not merely a changed subprocess exit code**. All named-case stderr streams were empty.

Sanitized excerpts projected from actual mutated stdout, containing only derived allowed output fields:

```json
{"case":"code_quota_1113_beats_429","finding_id":"MORI_SEAT_TERMINAL_DEAD","totals":{"aborted":0,"completed":0,"dead_error_other":0,"dead_quota":0,"dead_rate_limit":1,"error_unsettled":0,"incomplete":0,"unavailable":0},"seats":[{"seat":"code-1113","class":"dead_rate_limit","error_status":429,"error_code":"1113"}]}
{"case":"code_quota_1308_beats_429","finding_id":"MORI_SEAT_TERMINAL_DEAD","totals":{"aborted":0,"completed":0,"dead_error_other":0,"dead_quota":0,"dead_rate_limit":1,"error_unsettled":0,"incomplete":0,"unavailable":0},"seats":[{"seat":"code-1308","class":"dead_rate_limit","error_status":429,"error_code":"1308"}]}
```

Actual gate reasons for `code_quota_1113_beats_429` were `["want.totals.dead_rate_limit=1","want.totals.dead_quota=0","want.seat_class:code-1113","unexpected_seat:code-1113"]`. For1308 the same reason shapes named `code-1308`. The numeric reason suffixes are quoted exactly as emitted; the expected table still requires rate-limit0/quota1.

Complete generated stdout for the two examples is retained only in the clone:

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.scratch/quota-probe/mutated/runs/code_quota_1113_beats_429.stdout`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.scratch/quota-probe/mutated/runs/code_quota_1308_beats_429.stdout`

Exact reconstructed tool argv, output paths/digests, safe excerpts, rc and reasons for all four named cases across all three stages are retained in `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.scratch/quota-probe/named-case-excerpts.json`. This contains detector outputs, not raw transcript records.

## Hashes, pins and exact restoration

Initial `sha256sum` over the clone source tool, gate and expected table succeeded (rc0) and matched `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/PINNED_INPUTS.json:3-13`. The command was:

```text
sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/tools/mori-seat-terminal.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/tools/mori-round17-seat-regressions.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.ufo/waves/round-17/fixtures/seat/expected.json
```

| Bytes | SHA-256 |
|---|---|
| Pristine source and tested copy | `5819c3c06e4ceded02b043ef1edbe15043359f176f1b24830b4d3cae24adbdba` |
| **Mutant tested bytes and retained snapshot** | **`ac8769a260622cfeda85a937621ecdfb838c53df84c0f4e822e22fe8e8731d09`** |
| Restored tested copy | `5819c3c06e4ceded02b043ef1edbe15043359f176f1b24830b4d3cae24adbdba` |
| Unchanged gate, before and after | `21285c2b7000bf63cd9fd679f4b88a7d5d4ff250eee0279576d6d0dcb3b97f7a` |
| Unchanged expected table, before and after | `b684c63bf3cebe70f24d3d02f3f0df4f63aad3f547a365a3ca1864f5f57cb01f` |

The mutated run was wrapped in `try/finally`; the finally clause restored the held pristine bytes before the restored detector run. Exact byte equality with the original was observed as `true`, not only digest equality. The source tool's final digest also remained the pinned pristine digest.

All three gate manifests verified81 persisted fixture pins, reported `inputs_changed: []`, and recorded0 changed packs. The full fixture snapshots before and after were equal across all three runs. Gate metadata independently recorded branch `master`, receipt ref `refs/heads/master`, branch tip and HEAD `273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7` on all three stages; no additional VCS commands were invoked by this seat. The gate's own metadata commands are read-only and disable optional locking (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/tools/mori-round17-seat-regressions.py:1510-1573`).

Restoration and consolidated evidence:

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.scratch/quota-probe/restoration.json`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutQuota/.scratch/quota-probe/probe-summary.json`

No transient clone, mutant snapshot, script or receipt was removed; they remain for L1 integration. No tools were installed or updated. No pacman transaction, host service, live journal query, real transcript scan, other runtime invocation, VCS mutation or write outside the assigned clone and this report was performed.

## Verdict

**KILLED.** The pristine detector matched54/54, the one precedence mutant was rejected by three named cases (including both vendor quota-code/HTTP429 cases), and exact restoration returned54/54. No defect was found within the assigned quota-before-generic-rate mutation scope; this is neither a blanket C1 pass nor a C2/C3 or round-admission judgment. The assigned probe is complete.
