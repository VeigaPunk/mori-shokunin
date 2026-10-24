# FixToolResidual — R4 judged tool repair

## Scope and implementation

Edited only `tools/mori-oom-killers.py` in the assigned sandbox clone at `/fast/scratch/hyaku/mori-r30/FixToolResidual/lane`, checked out at `58b61681a0e3f3b821a17d38a4e713ccd9921615` (clone/checkout command output: `HEAD is now at 58b6168`). No fixture was edited; the full unified diff lists only the tool (`/fast/scratch/hyaku/mori-r30/FixToolResidual/tool.diff:1-4`).

For a readable show with `ActiveState` present and a nonzero retained `ActiveEnterTimestampMonotonic`, the reader now scopes diagnostic parsing to records at or after that boundary for non-active states too. It keeps `actions: null` and `scope_complete: false`, reports the in-scope version/grammar and the separate dry-run/process-group line counters, and leaves malformed-timestamp records uncounted. A non-active in-scope send/escalation remains positive evidence, so moving it out of the earlier-invocation bucket does not erase the `KILLER_ACTED` verdict (diff: `/fast/scratch/hyaku/mori-r30/FixToolResidual/tool.diff:9-42,46-82`). The boundary/version behavior follows `rule-text.md:25-30,37-42`; A2-03/A2-04 line counters are at `:73-78,107-108`; A2-06 earlier sends and non-active verdict use are at `:84-88`; A2-10 unplaceable records are at `:95-97`; positive evidence stands at `:44-45`.

## Selftest evidence

Command in the sandbox: `python3 -I -B tools/mori-oom-killers.py --selftest --cases <file>` for each listed fixture. Exact markers captured before and after:

| File | Before | After |
|---|---|---|
| `cases.json` | `MORI_OOM_KILLERS_SELFTEST: PASS 32/32` | `MORI_OOM_KILLERS_SELFTEST: PASS 32/32` |
| `cases-supplementary.json` | `MORI_OOM_KILLERS_SELFTEST: PASS 32/32` | `MORI_OOM_KILLERS_SELFTEST: PASS 32/32` |
| `cases-a2.json` | `MORI_OOM_KILLERS_SELFTEST: PASS 30/30` | `MORI_OOM_KILLERS_SELFTEST: PASS 30/30` |
| `cases-a2-r29.json` | `MORI_OOM_KILLERS_SELFTEST: FAIL 21/24` | `MORI_OOM_KILLERS_SELFTEST: PASS 24/24` |

The final tool sha256 is `9c88ef272dbe3e07eb87e40f10faaedb82584df0d9f21e78e3d8764400da0fe1` (command output from `sha256sum tools/mori-oom-killers.py`). No install/update was performed.

## Full-output differential

Driver compared `--inputs` outputs and exit/stderr for every case input: 118 total (32 + 32 + 30 + 24); full JSON before/after for each changed output is retained in `/fast/scratch/hyaku/mori-r30/FixToolResidual/differential.txt:1-52`. Summary: 5 changed outputs; no exit-code or stderr changes; `OLDER_KILLER_ACTED_VERDICT_FLIPS=[]` (`differential.txt:51-52`). The full unified diff is retained privately at `/fast/scratch/hyaku/mori-r30/FixToolResidual/tool.diff` (85 lines); it is not pasted into this non-writer report.

| Changed case | Every changed field (before → after) | Rule-text basis |
|---|---|---|
| `cases-a2.json` `a2-02-earlyoom-activestate-deactivating` | `dryrun_send_lines` null→0; `grammar` unverified→verified-1.9.0; `process_group_lines` null→0; `version` null→1.9.0 (`differential.txt:3-11`) | A2b maps non-steady `ActiveState` to unavailable (`:71-72`); scope/version/output fields `:25-30,37-42`; line counters `:73-78,107-108`. |
| `cases-a2.json` `a2-06-inactive-earlier-invocation-sends-acted` | Same four fields (`differential.txt:12-20`); earlier-send count remains 3 and verdict/exit remain `KILLER_ACTED`/1. | Scope/version `:25-30,37-42`; line counters `:73-78,107-108`; earlier-invocation count and non-active positive-evidence rule `:84-88`. |
| `cases-a2-r29.json` `r29-a2-10-inactive-lone-missing-stamp` | `dryrun_send_lines` null→0; `grammar` unverified→verified-1.9.0; `process_group_lines` null→0; `version` null→1.9.0 (`differential.txt:22-30`). | Scope/version/output `:25-30,37-42`; line counters `:73-78,107-108`; malformed timestamp `:95-97`; Judge11 confirms each field ruling (`.ufo/waves/round-29/w2/Judge11.md:33-37`). |
| `cases-a2-r29.json` `r29-a2-10-failed-stamped-positive` | Same four fields plus `earlier_invocation_send_lines` 1→0 (`differential.txt:31-40`); verdict/exit remain `KILLER_ACTED`/1. | Scope/version `:25-30,37-42`; A2-06 and A2-10 `:84-88,95-97`; positive evidence `:44-45`; Judge12 field rulings `.ufo/waves/round-29/w2/Judge12.md:30-35`. |
| `cases-a2-r29.json` `r29-a2-10-not-found-earlier-stamped-positive` | `dryrun_send_lines` null→0; `grammar` unverified→verified-1.9.0; `process_group_lines` null→0; `version` null→1.9.0 (`differential.txt:41-49`); earlier-send count remains 1 and verdict/exit remain `KILLER_ACTED`/1. | Scope/version `:25-30,37-42`; A2-06/A2-09 `:84-92`; A2-10 `:95-97`; Judge13 field rulings `.ufo/waves/round-29/w2/Judge13.md:38-43`. |

## Risks and blockers

- The fix follows Judges 11–13, despite the residual dissent that these non-active expectations should not be tool-fixed (`.ufo/waves/round-29/residual/ReviewLandedFix.md:36-66`; contrasting feasibility result in `CriticC2Verdict.md:23-33`). The broad wording `actions: null ... never zero counts` at `rule-text.md:49-51` could be read to cover the separate dry-run/process-group counters; this fix leaves the `actions` object null and adopts the judges' zero values for those separate line-count fields (`rule-text.md:73-78,107-108`).
- No blocker. No LSP tool was available in this seat's provided tool inventory; no symbol refactor was needed. No packages/tools were installed or updated.
