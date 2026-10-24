# Round-18 trend falsification — CriticTrendVerdicts-2

**Review target:** attacked tip `e2bfbd6f8dccc51fc06455efc41f720301112dd4`. The lane checkout's current `git log -1` was later (`95c615836c2cf74ee11539c4289a1ce06a81cfcb`), so findings below are anchored to the attacked tip with read-only `git show`, not inferred from the later worktree.

## Verdicts

| Trend / axis | Verdict | Finding |
|---|---|---|
| Expansion | **unchanged** | The new entries are real and their `source:` fields cite mined rows, but the required coverage-map evidence is absent; the draft's `improved` verdict does not meet the LEARNING bar. I found no content falsifier sufficient to call the trend harmed. |
| Quality | **unchanged** | The draft cites privacy minimization and a tool-rule correction, not a re-verification, deepening, or stronger replacement of an existing knowledge entry as required for `improved`. No admitted knowledge entry shown here fails a recheck, so I do not call quality harmed. |
| Discernment | **harmed** | At the attacked tip, round-18 criteria cite a missing round-18 lesson, and no round-18 outside admit/reject spot-check is recorded. The same-round scribe disagreement is not a non-author check. |
| Axis no-harm / adjacency (C1) | **harmed** | The frozen-class C1 metric may have improved at its stated scope, but the L1 triage explicitly retains unresolved out-of-metric private-context items. Adjacency therefore remains harmed; the provisional no-harm reading is not supportable and the round is not admission-ready. |

### Expansion — draft `improved` rejected

`LEARNING.md:31-33` requires a net new admitted entry on uncovered ground, with each entry tied to its coverage-map row. The three round-18 notes exist and have provenance fields (`corpus/knowledge/evidence-minimization-r18.md:1-3`, `freeze-order-r18.md:1-3`, `dispatch-ledger-r18.md:1-3`); `SOURCES.md:55-69,98` records the round's mined/rejected/queued sources and source decisions. However, the coverage map at `corpus/README.md:3-42` has no round-18 rows; its only later additions are explicitly the three round-17 rows at `:351-357`. Thus the entries are not shown against uncovered map ground, and opening S049–S063 is not itself expansion under the protocol. **Smallest correction:** add a coverage-map row for each counted entry that names the uncovered ground, or report expansion `unchanged` until that evidence exists.

### Quality — draft `improved` rejected

The draft's stated evidence is round-17 handoff minimization and a tool correction (`draft-verdicts.md:15-17`). Under `LEARNING.md:34`, those do not establish a quality improvement unless a knowledge entry is re-verified, deepened, or superseded by a stronger entry (or a stale entry re-verifies) with no admitted entry failing re-check. The three round-18 notes are new admissions, not evidence of such an existing-entry recheck. I found no basis in the reviewed artifacts to say an admitted knowledge claim was found false/stale and left unmarked; therefore use `unchanged`, not `harmed`. **Smallest correction:** retain `unchanged` unless a specific existing entry and its before/after recheck or stronger replacement are cited.

### Discernment — draft `improved` falsified

`LEARNING.md:35,42-46` requires either outside agreement on at least one admit and one reject, or a disagreement turned into a lesson that adds a grounded QUALITY criterion. The draft cites QUALITY 51/52 and the GDPR source disagreement (`draft-verdicts.md:17-19`), but `corpus/QUALITY.md:154-180` points the round-18 criteria to `lessons/round-18.md#M1`–`#M5`, and that lesson is absent from the attacked commit. The exact command `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show e2bfbd6f8dccc51fc06455efc41f720301112dd4:corpus/lessons/round-18.md` failed with exit **128** (path absent at the target). `SOURCES.md:98` records an internal scribe disagreement and the L1 decision, but that is not the required outside check; there is no committed round-18 `## Gate` spot-check record. At minimum, QUALITY 55's only lesson pointer (`QUALITY.md:176-180`) is unresolved at this revision, meeting the stated harm condition that a criterion is added without its lesson. **Smallest correction:** do not claim discernment improved; land the actual lesson and a non-author admit/reject spot-check with reasons, restore resolvable criterion pointers, then re-evaluate.

## Axis no-harm attack — adjacency is still harmed

The C1 draft carefully narrows its metric to frozen classes and itself labels the whole-round repair partial (`draft-verdicts.md:8`). That qualification does not close the adjacency axis: the retention policy/knowledge note says the classes are a recall floor (`frozen/c1-policy.json:29`; `corpus/knowledge/evidence-minimization-r18.md:35-46`), and the attacked out-of-metric triage still has admitted-but-pending material at `out-of-metric-triage.md:25-26`. The draft's known-open summary names six session-derived plus two host-config reports refused by the process job cap (`draft-verdicts.md:21-22`), while the triage also leaves three additional host/config line-edit items conditional and not marked complete (`out-of-metric-triage.md:26`). It separately carries one earlier-round finding to a future pass (`out-of-metric-triage.md:30`). These are explicit unresolved items, not speculative risk; the frozen C1 count cannot clear them.

Privacy-safe reference to the carried older finding: `.ufo/waves/round-16/build/SiblingScope.md:20`; class **out-of-metric private-context finding** (no R1–R9 class is assigned in the triage); count **1 carried triage finding**; SHA-256 of the complete file at the attacked tip: `760a4e871f069ac4b3c767b486a6ae2c904f4b58e30d3ab835a36274948f6df6`. No line content is reproduced.

**Smallest safe correction:** keep C1's bounded frozen-class result as a scoped measurement, but mark adjacency `harmed` and withhold no-harm/admission until every pending and carried current-tip copy is minimized and the whole-tree reading sweep is clean. Preserve history; this is a current-tip minimization, not a history rewrite. Do not infer that the unresolved out-of-metric items were cleared by the gate.

## Scope and evidence record

- Protocol criteria used: `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md:31-46`; axis no-harm requirement: `AXES.md:25-38`.
- Read-only target reads: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show e2bfbd6f8dccc51fc06455efc41f720301112dd4:.ufo/waves/round-18/draft-verdicts.md` and the corresponding `out-of-metric-triage.md`, `corpus/README.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, and three named round-18 knowledge notes — exit **0**. The read-only target hash comparisons for README, QUALITY and SOURCES matched the checkout copies; those are the line-number sources cited above.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin log -1 --format=%H` — exit **0**, observed later checkout HEAD `95c615836c2cf74ee11539c4289a1ce06a81cfcb`; review stayed pinned to the assigned `e2bfbd6` revision.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show e2bfbd6f8dccc51fc06455efc41f720301112dd4:.ufo/waves/round-16/build/SiblingScope.md | sha256sum` — exit **0**; digest reported above, no content emitted.
- No external URLs were opened for this review; no URL access dates apply. No tools were installed or updated. No selftests, builds, linters, or formatters were run.
