# Mo61ConnSibling — sibling-overlap scan

## Scope and axes

Read the frozen round-61 contract first. Axes declared there: C1 calibration, C2 freshness, C3 operability; adjacency is the cross-lane no-harm constraint. This is read-only source inspection, not a claim verdict, admission, counter execution, or source adoption. No contract/counter change is proposed.

All paths below are absolute. Evidence describes the observed local sibling files, not a verified immutable sibling revision.

## Findings

| Sibling surface and exact evidence | What it holds | Relation to mori round 61 |
|---|---|---|
| `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/memory-pressure-r25.md:1-3,34-39,48-56` | Six host memory/oomd reading rules. Explicitly cites mori's generic PSI semantics at `4f05dd5a`, does not absorb them; owns the systemd-oomd consequence and OS triage. Recheck requires a new capture and separate live authorization. | Real semantic overlap, explicitly divided ownership. Mori's v7.3 quote-location ledger stays internal; it neither refreshes tsukuroi's old host capture nor measures present oomd configuration. |
| `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh:1236-1250,1268` | Reads some/full avg300 and full total from the configured PSI file; reports named unknown on unreadable PSI. | Runtime overlap on pressure readings, not on the r61 source ledger. Ledger completion must not be described as a new host-pressure reading or event detection. |
| `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md:121-125,131,133` | Linux v7.2 PSI/cgroup/OOM primary rows plus sibling mori boundary citations. | Shared upstream material, distinct source versions and source registries. Do not renumber, refresh, or claim these rows through mori's C2. |
| `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/adjacency-anchors-r19.md:119-121,153-155,162-171` | Historical eight-column gate-table precedent and existing mori correlation handoff anchors; some anchors explicitly marked DRIFTED. | Registry shape precedent is not current ownership or evidence of r61 row correctness. Existing handoffs remain correlation/report-only. |
| `/home/vgpnk/Projects/shokunin/kama-shokunin/tools/gate-registry-check.py:10-30,43-57` | Own instrument population, five-column SKILL tables, row/path checks and selftest; default can read working-tree bytes. | Conceptual overlap with C1, not a shared registry. Explicit schema mismatch: kama five columns vs mori eight required cells. Its green cannot certify mori's 25 frozen paths. Do not import or execute this gate. |
| `/home/vgpnk/Projects/shokunin/kama-shokunin/corpus/SOURCES.md:559-571` | Round-45 recheck ledger with pinned/current bytes and machine witnesses; S048 rechecks Linux tcp_ipv6.c v7.2→v7.3 and unchanged in6.h. | Actual kernel-source recheck precedent, but not PSI rechecking. Its v7.3 result does not discharge any mori PSI anchor. |
| `/home/vgpnk/Projects/shokunin/kumitate-shokunin/corpus/QUALITY.md:1066-1070` | Q62: capability registry home spans its SKILL gate row, QUALITY criterion and SCORECARD capability row, same round. | Own orchestration capability governance. Mori C1's manifest/one-round-lag rule is different; do not silently import Q62 or require new frozen-scope rows. |
| `/home/vgpnk/Projects/shokunin/kumitate-shokunin/corpus/lessons/round-41.md:168-170` | Records that anchor-truth `--open` cannot bind a review committed after the open revision (`REVIEW_UNBOUND`), and the honest re-measure was not done. | Related historical review-binding concern, not proof of a current vote-binder implementation. Mori C2 explicitly has no frozen vote arm; do not add one. |
| `/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/bind-oracle.mjs:3-9,21-31` | Child mount-namespace oracle for cap-run requested directories; explicitly limited by child's output honesty. | Name collision only: filesystem binds, not vote binding. Related execution-substrate topic, but cannot certify mori C3's byte-pin refusal or token conjunctions. |
| `/home/vgpnk/Projects/shokunin/souji-shokunin/tools/souji-registry-agreement.py:8-23` | Committed SOURCES↔knowledge used-by agreement and append-only stale-statement correction checks. | Own corpus source-registry semantics, not mori C1's gate registry. Its counter materialization is a distinct consumer, not evidence for mori C3. |
| `/home/vgpnk/Projects/shokunin/souji-shokunin/tools/souji-gate-check.py:4-24` | Assimilation predicate with ≤25-word located quotes, whitespace-collapsed snapshot matching, source-ID resolution and verdict slice. | Content-validation overlap only. Mori C2 requires byte-located, pairwise-distinct spans at frozen pins; souji's weaker/different normalization is not interchangeable. |
| `/home/vgpnk/Projects/shokunin/souji-shokunin/corpus/QUALITY.md:177-179` | Q73 checks byte-pinning consumers; Q74 preserves scratch/refusal guards when TMPDIR becomes caller-controlled. | Useful existing boundary concerns, still souji-owned. Neither criterion nor its historical evidence can establish r61 C3 met. |

## One bounded proposed move: source-version and authority firewall in the report

Suggested draft block for L1's report, not production edits by this seat:

> The v7.3 PSI ledger refreshes only mori's source-pointer evidence. It does not refresh tsukuroi's v7.2 host capture or oomd policy reading, and does not adopt sibling source IDs. Tsukuroi already cites mori for generic PSI semantics and retains OS triage; wave attribution remains report-only mori work. Kama's TCP v7.3 ledger and five-column gate checker, kumitate's orchestration registries/mount-bind oracle, and souji's source/quote gates are neighboring precedents, not r61 certification inputs. C1 certifies only its 25-path own-lane population; C2 has no vote arm; C3 concerns only its frozen own-counter boundary.

[INFERENCE] This improves calibration/adjacency clarity without changing frozen freshness or operability targets, running another runtime, adding an execution dependency, or expanding ownership. Second-order effects: runtime remains unchanged; contract predicates stay frozen; sibling byte-pin consumers remain untouched; verification continues to use only mori's pinned copies and own counters.

## Contradictions and risks

- Five-column kama registration and eight-cell mori registration are not equivalent; a shared 'registry green' label would conceal a schema contradiction.
- Souji whitespace-normalized quote acceptance and mori byte-location acceptance are not equivalent.
- Kernel v7.3 TCP rechecking does not imply PSI rechecking; source freshness does not imply current host-state freshness.
- `bind-oracle` is not a vote binder. No exact vote-binder implementation was located by the bounded tool scans below; this is not an exhaustive absence claim across every artifact.
- Historical sibling citations can drift (tsukuroi's adjacency ledger already records DRIFTED rows). Report them as observed local evidence, not adoption or a new ownership ruling.

## Evidence method and receipts

Tool calls used absolute paths. `functions.grep` searches (case-insensitive, gitignore respected) over each sibling's `tools/` and `corpus/` used:

`(?i)\bPSI\b|pressure stall|psi\.rst|gate.registry|vote.bind|recheck.ledger|kernel.source`

Kumitate's directory listing showed runnable instruments in `scripts/`, not `tools/`; its `scripts/` was additionally inspected. Focused corpus search:

`(?i)recheck.ledger|kernel.*recheck|recheck.*kernel|v7\.3|psi-v73`

returned tsukuroi recheck procedures and kama S048 v7.3 rows quoted above. Focused tool search:

`(?i)vote[-_ ]?bind|vote binder|vote.*sha|review.*bind`

across tsukuroi/kama/souji `tools/` and kumitate `scripts/` returned only kumitate cap-run's mount-bind comment (false positive), not a vote binder. A further search for `REVIEW_UNBOUND|review.*(sha|commit|bind)|bind.*review|vote` in kumitate's `anchor-truth.mjs` and `claims-check.mjs` returned `No matches found`; historical review-binding evidence is therefore labeled historical above. Broad searches were paginated/truncated; negative findings are bounded to these patterns, not universal claims.

Host guard command executed:

`/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`

Output before 30-second timeout: `/tmp 24% 97.5G free`; `/var/tmp 41% 533.8G free`; `/fast/scratch/hyaku 54% 371.7G free`; then `top consumers /tmp`. No heavy work followed. Created only the empty seat scratch directory `/fast/scratch/hyaku/mori-r61/Mo61ConnSibling` and removed it with `rmdir`; no temporary files or counter invocations needed TMPDIR. No tools installed, no VCS calls/mutations, no sibling/fleet writes, no production edits, no external fetches, no service/config changes.

## Verification handoff

Performed: read-only grep and exact ranged source reads. Not performed: counters, selftests, runtime probes, immutable sibling-revision binding. L1 should compare the proposed report paragraph against frozen contract lines 34-49 (C1), 61-79 (C2), and 90-109 (C3); any scoring remains with the round's authorized verifier. No new verification gate or contract amendment is requested.
