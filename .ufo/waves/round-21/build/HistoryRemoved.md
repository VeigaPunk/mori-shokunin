# Round 21 — historical wave removal findings

## Finding

**Classification: marker/evidence loss from the current wave tree; settlement remains UNKNOWN.** The sweep has an itemized cleanup receipt, but the checked evidence does not establish an independent per-wave settlement or disposition. The baseline acceptance gate should therefore treat `aggregator-r10` and `aggregator-r10-resume` as unresolved, consistent with the round-21 C1 contract (`.ufo/waves/round-21/contract.md:7`). This is not a live census.

## Deletion commit

Observed with `git -C /home/vgpnk/Projects/shokunin show -s --format=... e20f4fa` and `git show --name-status e20f4fa -- .ufo/waves/aggregator-r10 .ufo/waves/aggregator-r10-resume`:

- Commit: `e20f4fa3fd3fc9550641af38da3eddcf3d35f528` (short `e20f4fa`), parent `7aea421049170270a6f9a6cc6388be8da0763936`.
- Author/committer: `souji-shokunin <souji@shokunin.local>`, 2026-10-18 23:58:39 -0300.
- Subject: `souji: remove 96 pushed-receipt checkpoint artifacts (operator sweep 2026-10-18)`.
- It deletes exactly 18 tracked paths from these wave directories: 10 under `aggregator-r10-resume`, 8 under `aggregator-r10`. `git ls-tree -r e20f4fa^` lists these as the full tracked preimage contents of the two directories. Git ancestry preserves the deleted blobs; the loss is from the current wave tree and its marker-based observation, not demonstrated irretrievability from history.

## The 18 deleted paths and classification

All 18 are removed wave markers or supporting historical work/measurement artifacts. **None is an independent settlement record.** The two `dispatch.json` files are the direct census markers; the other 16 are evidence/context, measurements, plans, source, or seat outputs whose loss reduces the retained wave record but does not itself prove settlement.

| Deleted path (fleet-root relative) | Classification |
|---|---|
| `.ufo/waves/aggregator-r10-resume/CONTEXT.md` | Wave context/custody record removed; not a settlement marker. |
| `.ufo/waves/aggregator-r10-resume/before.json` | Historical metadata recount of an inherited measurement, not a new run or settlement. |
| `.ufo/waves/aggregator-r10-resume/critic.md` | Advisory falsifier/review work product; not an independent disposition. |
| `.ufo/waves/aggregator-r10-resume/dispatch.json` | **Census marker removed** (`disp=1` at the r10 observation); dispatch metadata is not settlement evidence. |
| `.ufo/waves/aggregator-r10-resume/evidence.md` | Evidence/status report removed. It records unmeasured after-state and parent-owned unfinished items, rather than a settlement result (preimage report: `git show e20f4fa^:.ufo/waves/aggregator-r10-resume/evidence.md`, especially its work-status and before/after sections). |
| `.ufo/waves/aggregator-r10-resume/measure-corpus.mjs` | Collector source, not an executed result or settlement record. |
| `.ufo/waves/aggregator-r10-resume/plan.md` | Advisory plan, not evidence of completion. |
| `.ufo/waves/aggregator-r10-resume/preservation-pins.json` | Historical preservation inputs; the JSON explicitly says `Historical preservation inputs, not verification results`. |
| `.ufo/waves/aggregator-r10-resume/selection.md` | Change/selection record, not a wave disposition. |
| `.ufo/waves/aggregator-r10-resume/surfaces.md` | Advisory surface reconnaissance, not a settlement record. |
| `.ufo/waves/aggregator-r10/before-summaries.log` | Inherited measurement summaries; not settlement evidence. |
| `.ufo/waves/aggregator-r10/before.json` | Historical baseline measurement record; not settlement evidence. |
| `.ufo/waves/aggregator-r10/count-before.log` | Measurement count/exit metadata; not settlement evidence. |
| `.ufo/waves/aggregator-r10/dispatch.json` | **Census marker removed** (`disp=1` at the r10 observation); dispatch metadata is not settlement evidence. |
| `.ufo/waves/aggregator-r10/seats/critic.md` | Inherited advisory critic output; not an independent disposition. |
| `.ufo/waves/aggregator-r10/seats/plan.md` | Inherited planning output; not a settlement record. |
| `.ufo/waves/aggregator-r10/seats/scout.md` | Inherited reconnaissance output; not a settlement record. |
| `.ufo/waves/aggregator-r10/seats/scribe.md` | Inherited evidence/report-shape output; not a settlement record. |

## Marker loss is distinct from settlement

- The r10 observation is explicit: `corpus/knowledge/observability-surfaces-r2.md:60-61` records separate `WAVE_UNSETTLED_AGE` rows for both waves with `reg=0 disp=1 run=0 settle=0` at `2026-10-15T15:27:57Z`. Thus the census had seen each dispatch marker and reported each as unsettled then.
- The census settlement checks are in `tools/mori-census.sh:857-897`; its unsettled/empty branch is at `:917-927`. The committed pre-deletion tree contains no `results.json`, `closeout.json`, `mission-result.json`, `closeout.md`, `swarm-registry.json`, `run.json`, or `spec.json` in either wave directory. The baseline `settle=0` is the direct observation; the preimage tree shows the removal set was not itself a set of typed closeout files.
- `FamWavesIo.md:26-29` records the deletion count and the replay result: the two `dispatch.json` markers disappeared, leaving no regular files in either directory, so the unchanged empty branch emitted no row. This explains disappearance; it does **not** show that either wave settled between the r10 observation and the 2026-10-18 deletion.
- The resume evidence report itself says the collector was not executed, the reviewer output was absent, the after measurements were `NOT MEASURED`, and final report/commit work was the parent's duty (deleted preimage `evidence.md`, work-status and before/after sections; also summarized in `FamWavesIo.md:26-29`). This is evidence of incomplete/unverified work at that report's observation, not proof of state at deletion time.

## Cleanup receipt: useful accounting, not independent settlement

`souji-shokunin/census/operator-sweep-20261018/approval-list.tsv:56-73` contains exactly the 18 deleted wave paths, each with receipt value `pushed`. The receipt was committed in the nested Souji repository as `2f303dc6e30d7650e1e513e3cbad75412efdc353`, authored by the same Souji identity on 2026-10-19 00:02:43 -0300—after the deletion commit. It supports path-specific sweep/cleanup accounting. It does not name an independent per-wave settlement decision; the receipt's `pushed` field has no defined settlement meaning in that file. The same-author, post-deletion receipt therefore cannot establish an independent disposition (cf. `FamWavesIo.md:33-37,59-61`).

## Evidence boundaries

**Observed:** commit identity/date/message; 18 deletion paths; two dispatch markers present with `settle=0` in the r10 observation; exact-path `pushed` receipt entries committed afterward by the same author; no typed closeout file in the committed pre-deletion tree.

**Inference:** the sweep removed marker/evidence artifacts under its stated pushed-receipt cleanup, which explains why the marker-based census stopped reporting these wave identities. `pushed` is not interpreted as settlement.

**Unresolved:** whether either wave received a valid settlement or other independent disposition after the 2026-10-15 baseline observation and before/after deletion. No such distinct-actor, explicit per-wave disposition was found in the checked evidence. Keep both identities visible as unresolved; do not infer settlement from empty directories or the cleanup receipt.

No live census, source edits, installs, or updates were performed.