measured 2026-10-23T08:55:05Z

# CritSkipLoophole — strong provenance is not capability evidence

Axes: calibration (does this pointer substantiate this capability?), operability (can a reader find the relevant behavior?), and evidence identity/scope (do not substitute another claim from the same round). Calibration is the declared C1 axis; the contract does not claim an operability improvement (`.ufo/waves/round-35/contract.md:14-20`).

VERDICT: fails — the positive control's classification establishes capability-relevant evidence, rather than merely a closure-to-artifact join. Its existing register already contains two wrong-capability pointers, despite its recorded 18/18 meet (`.ufo/waves/round-35/c0/CtlPositive-register.md:5,19`; `.ufo/waves/round-35/c0/CtlPositive.md:119-141`).
VERDICT: holds — the narrower frozen classification that these rows perform P-C1's key/round/round-artifact binding. The contract expressly reserves pointer/prose review for humans; I do not redefine P-C1, convert its recorded meet into an unmet, or issue a canonical admission/kill-rule judgment (`.ufo/waves/round-35/contract.md:28-44,95-104`).

## Strongest counterexample: no new control required

The positive generator uses capability text only to extract named paths, then chooses a candidate by path-prefix rank; unnamed capabilities receive no semantic evidence matching (`.ufo/waves/round-35/c0/CtlPositive.md:63-69,91-106`). Its actual round-28 C1 row sends a reader seeking eight source-row repairs to the round-28 C2 OOM fixture pack. This is not a merely less convenient pointer to the same capability (`.ufo/waves/round-35/c0/CtlPositive-register.md:19-20`; `tools/fixtures/mori-oom-killers/cases-a2.json:2-4`).

The mechanism is explicit: the counter constructs one record text from the entire round's verification, reports and capabilities, then gives that same text and changed-file set to each capability. Only capabilities naming tool/knowledge paths get a capability-specific path restriction (`.ufo/waves/round-35/count-c1.py:113-132,181-186`). Co-change and co-mention therefore establish provenance, not relevance.

## Per-row counterexamples and row-only corrections

### rounds[476].capabilities_added[0] — round 28 source repairs

VERDICT: unsupported — `tools/fixtures/mori-oom-killers/cases-a2.json` as evidence of the source-repair capability.
- Strong membership and actual selection: `.ufo/waves/round-35/c0/CtlPositive.md:160`; `.ufo/waves/round-35/c0/CtlPositive-register.md:19`.
- Why misleading: the fixture identifies itself as C2 and tests OOM amendment-A2 rules (`tools/fixtures/mori-oom-killers/cases-a2.json:2-9`). The closure separately measures C1 as three original-row restorations, eight superseding source rows and reader-citation migration; C2 is the 30-case pack (`corpus/lessons/round-28-verifier-spotcheck.md:45-74`).
- Smallest correction: replace the fixture pointer with `corpus/SOURCES.md:102-158`; name S145-S152, the three restored IDs, and repointed readers in the what-cell. A second pointer may show an actual migrated reader, e.g. `corpus/knowledge/oom-victim-selection-r27.md:72-85`. Do not imply that this one example re-measures the complete reader sweep; its historical census is in the closure (`corpus/lessons/round-28-verifier-spotcheck.md:50-58`).

### rounds[313].capabilities_added[0] — round 12 source registry

VERDICT: unsupported — `tools/mori-census.sh` as the sole evidence of the sources-registry capability.
- Actual positive selection: `.ufo/waves/round-35/c0/CtlPositive-register.md:5`. The same candidate set also admits the drift receipt, roster live/mutation receipts, roster knowledge and kernel-OOM-counter knowledge (`.ufo/waves/round-35/c0/CtlPositive.md:146`).
- Why misleading: mori-census is the fleet/host observability product, not the source-registry validator (`tools/mori-census.sh:2-51`). The frozen round-12 report separates source-registry claim 1 from roster/census claim 3 and names a different source-census validator in its final acceptance; see the read-only command below. The roster note documents a config/state union; the OOM note documents counter semantics, neither the 34-row registry (`corpus/knowledge/roster-truth-r12.md:5-25`; `corpus/knowledge/oom-kill-counter-kernel-only-r12.md:5-18`).
- Smallest correction: cite `corpus/SOURCES.md:3-40`, not an unrelated artifact from the same round. State that the registry first worked in round 12 with 34 rows at that closure, not that today's accumulating registry still has only 34. The capability identity is frozen at `rounds[313]` (manifest extraction below); S001-S034 occupy the cited registry slice.

### rounds[353].capabilities_added[0] — round 16 exact-start journal window

VERDICT: unsupported — `tools/mori-round16-context-check.py` as evidence of the journal-window capability.
- Strong membership: `.ufo/waves/round-35/c0/CtlPositive.md:149`.
- Why misleading: this tool checks wave-spec context strings and explicitly disclaims runtime prevention; it does not implement the journal window (`tools/mori-round16-context-check.py:2-9,35-62`). The closure records its context results separately from the window's 64-case measurement (`corpus/lessons/round-16-verifier-spotcheck.md:79-90,113-116`).
- Smallest correction: cite `tools/mori-journal-window.py:304-325` and, optionally, `corpus/knowledge/journal-cursor-window-r16.md:7-11`. The what-cell must identify exact first-record cursor/boot validation, whole-window refusal and no cursor-state advance. Preserve the finite-fixture and anchor-only-live bounds rather than implying demonstrated positive live load (`corpus/knowledge/journal-cursor-window-r16.md:43-48`; `corpus/lessons/round-16-verifier-spotcheck.md:115-119`).

### rounds[398].capabilities_added[0] — round 19 content-review coverage

VERDICT: unsupported — `tools/mori-freeze-order.py` as evidence of the content-review capability.
- Strong membership: `.ufo/waves/round-35/c0/CtlPositive.md:153`.
- Why misleading: the round itself identifies C1 as content-review coverage and C2 as freeze-receipt provenance (`corpus/lessons/round-19.md:8-11`). Freeze-order checks timing/register provenance, not review dispositions (`tools/mori-freeze-order.py:2,676-689`); the content-review gate actually binds blobs and rejects stale, unresolved, provenance-only or missing reviews (`tools/mori-content-review.py:271-282,309-333`).
- Smallest correction: cite `tools/mori-content-review.py:271-333`; describe that behavior rather than freeze ordering. Keep the closure's real-population warning: 194 paths, 155 unresolved, RED, not privacy clearance (`.ufo/waves/round-35/c0/CtlPositive-register.md:12`).

### rounds[345].capabilities_added[0] — round 15 partial positives

VERDICT: unsupported — `tools/mori-round13-regressions.py` alone as evidence of the newly added mixed-invalid-stream behavior.
- Strong membership: `.ufo/waves/round-35/c0/CtlPositive.md:148`.
- Why misleading: its declared claims cover the restored alarm/routing behavior and F01/F02, rather than the new positive-subset-versus-invalid-total distinction (`tools/mori-round13-regressions.py:9-64`). The round-15 change to this file adds receipt/revision provenance without changing its C1 fixture checker (read-only diff below). The closure calls its result preservation, separately from the new invalid-aggregate witnesses (`corpus/lessons/round-15-verifier-spotcheck.md:118-127,157-168`). This is relevant old-behavior evidence, but not evidence of the distinguishing new capability.
- Smallest correction: select `tools/mori-round15-regressions.py:17-43`, whose assertions explicitly pair retained alarms with unavailable raw totals. Preserve finite-fixture scope and the no-live-positive-load limit (`corpus/lessons/round-15-verifier-spotcheck.md:167-168`).

## What the L1 must add to its own register

The five corrections above are independent: improve semantic provenance without changing capability identities, first-working rounds, row population, counter bytes or the 1-2-path evidence bound (`.ufo/waves/round-35/contract.md:35-47,95-99`). Do not copy the positive control as a human-approved register.

```DRAFT SCORECARD.md
For each capability row, the what-cell names the specific behavior demonstrated
and its material scope limit. Its evidence pointer leads to the implementation,
fixture assertions, or registry entries for THAT behavior, not merely another
artifact changed and mentioned in the same closure. The accompanying rationale
identifies what the cited lines establish and where the closure records the
historical demonstration. P-C1 checks structural provenance; human row review
checks this semantic link. A met receipt alone is not a supported-row verdict.
```

This extends the stated human review obligation, not the frozen predicate: the controls receipt already requires faithful prose and separately reported supported/unsupported row judgments (`.ufo/waves/round-35/evidence/c1-controls.txt:40-44`). The additional check needed is relevance of the pointer itself, not another ranking heuristic.

Boundary: I found concrete unrelated candidates for five keys, not a reason to reject every candidate set. For example, the round-14 gate actually names alarm and subject-routing assertions, and the round-15 migration in that gate explicitly covers a mixed-valid/invalid stream (`tools/mori-round14-regressions.py:23-56,108-119`). A file's older round number alone does not make it misleading.

## Evidence method, commands and limits

All paths above are lane-relative unless a fleet revision is stated. Candidate membership is read from the existing full-choice-set receipt, as permitted by this assignment; no new swapped-pointer control was scored. The two actual wrong selections are backed by the already recorded positive-control run, not by a run of mine (`.ufo/waves/round-35/c0/CtlPositive.md:119-163`). [INFERENCE] Replacing a row with another listed strong candidate would meet the same structural path tests; that inference is not a fresh measured pass.

Commands exercised, each bounded by timeout and address-space limits:
- `timeout 30 prlimit --as=1073741824 git -C /home/vgpnk/Projects/shokunin show 37b51a243302e8009c7067431e8a47f9a722fd14:MANIFEST.json`, then the same read piped to bounded jq selectors: output lists 18 admitted mori capability keys; rounds[313] is the source registry, rounds[345] partial positives, rounds[353] the journal window, rounds[398] content review, and rounds[476][0] source repairs versus [1] A2 cases.
- `timeout 30 prlimit --as=536870912 git -C /home/vgpnk/Projects/shokunin show 37b51a243302e8009c7067431e8a47f9a722fd14:.ufo/reports/round-12/mori.md`: output separates source-registry claim 1 and roster claim 3; final acceptance names `scripts/sources-census.sh validate` with recorded exit 0, not `tools/mori-census.sh` as registry validation.
- `timeout 30 prlimit --as=536870912 git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --no-ext-diff 0fa5e0de194bcc270a927a166664113e6821442b b83edc6ee3db6822382ab673d7e6e984e420f22f -- tools/mori-round13-regressions.py`: output adds revision/status/script-digest evidence handling; no C1 fixture-checker change.
- `timeout 30 prlimit --as=536870912 git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --no-ext-diff 3786f3f1bde2fbcc5ce617e35e8c9becdbf9d9e8 2061780117e6ca637725004897bd288d3ba7e988 -- tools/mori-freeze-order.py`: output adds resolved revision/input hashes and provenance binding, consistent with C2, not content-review disposition logic.
- `timeout 10 prlimit --as=67108864 date -u +%FT%TZ` returned `2026-10-23T08:55:05Z`.

No counter, gate, selftest, live journal query, canonical judge or other agent runtime was invoked. No installs/updates, scratch files, clones, commits, index/jj writes or background jobs. Only this assigned report was written; all commands completed. No new test pass or axis score is claimed.
