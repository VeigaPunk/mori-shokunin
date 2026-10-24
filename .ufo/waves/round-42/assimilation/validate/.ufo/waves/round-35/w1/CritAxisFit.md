measured 2026-10-23T08:54:27Z
# CritAxisFit — C1 admissibility attack

Advisory criticism only: no admission, integration, runtime judgment, counter execution, or lane edit beyond this report. Existing control outcomes below are receipt evidence, not runs performed by this seat.

## Axes and scope

Primary axis: calibration of the current SCORECARD repertoire register against admitted historical closures. Coverage, depth and operability are not acquired by indexing capabilities already demonstrated. This distinction follows `../AXES.md:11-15,57-64` and the frozen scope at `.ufo/waves/round-35/contract.md:14-31`.

## Requested questions

VERDICT: holds — Q1, calibration rather than mere assertion-counting, at the frozen structural scope. The counter compares a self-assessment register with admitted fleet records and lane history, then counts missing, bad and extra bindings; it does not simply count assertions added. That meets the necessary mismatch-counting condition in `../.ufo/prompts/mori-round-35.md:348-349`. Evidence: `.ufo/waves/round-35/count-c1.py:103-133,141-198`; before receipt `.ufo/waves/round-35/evidence/c1-before.txt:1-26` records 23 mismatches, including 18 missing keys. This is register/closure consistency, not a demonstration that every capability statement is true or that a tool still works today.

VERDICT: holds — Q2, the axis is named by the changed surface. The changed object is the lane's self-assessment in SCORECARD, not an expanded observability surface or a new runnable operation. Calibration matches `../AXES.md:15`; the repertoire table's separate role does not forbid correcting its self-assessment. The contract explicitly excludes coverage/depth/operability credit (`.ufo/waves/round-35/contract.md:16-20`). Do not convert eighteen historical entries into eighteen round-35 capability acquisitions: `../AXES.md:57-64` and `../.ufo/prompts/mori-round-35.md:361-365` do not support that inference.

VERDICT: holds — Q3, the observed do-nothing and ID/label-only controls do not meet the frozen binding target. Base is unmet; absent/empty sections are unmet; correct keys/rounds with generic SCORECARD, LOG or spot-check paths match zero rows; generic SOURCES matches only four. Capability-blind and round-wide artifact reuse also fail. These are bounded observations, not proof that no possible shortcut exists. Evidence: `.ufo/waves/round-35/evidence/c1-controls.txt:9-30`; `.ufo/waves/round-35/c0/CtlLabelKeyed.md:5-20`.

VERDICT: fails — Q3's stronger interpretation, that a met counter excludes shortcuts omitting useful self-assessment content. A tested control has eighteen empty capability cells and eighteen empty action cells, yet prints matched=18, mismatches=0, C1=met, exit 0. Its actual construction still performs per-capability strong-path binding, so it is not an ID-only bypass of literal P-C1. Evidence: `.ufo/waves/round-35/c0/CtlSkipDesign-register.md:5-22`; generator `.ufo/waves/round-35/c0/CtlSkipDesign.md:184-207`; recorded output `:210-231`. This is the strongest local counterexample to treating P-C1 as semantic calibration.

The positive-control distinction predates these results: `.ufo/waves/round-35/contract.md:95-99` explicitly permits oracle-derived strong bindings and leaves prose judgment outside the counter. I also read that classification with `git show f2d28711ee723c969b6c2008d32df498192f9e7b:.ufo/waves/round-35/contract.md`; the frozen output contains that same residual. The later ruling at `.ufo/waves/round-35/evidence/c1-controls.txt:32-44` therefore does not itself establish an after-data predicate change. However, calling a control positive cannot override the calibration rule in `../.ufo/prompts/mori-round-35.md:348-356`; whether the structural improvement is enough remains the canonical judge's decision.

VERDICT: holds — Q4, the numerical target is sized for one-command re-derivation. It enumerates the complete, pinned admitted-mori oracle, enforces one matched row per key and rejects extras, producing a concrete mismatch value. Target and command: `.ufo/waves/round-35/contract.md:33-54,67-75`; enumeration and decision: `.ufo/waves/round-35/count-c1.py:103-133,192-207`. Positive-control output shows the exact 18/18 target was reachable (`.ufo/waves/round-35/c0/CtlPositive.md:119-141`). No landed round-35 after-value was measured by this seat. One-command counting is not one-command proof of prose truth or of the separate control-classification/byte-identity kill rule (`contract.md:95-104`).

## Strongest closure objection

Counterexample: CtlSkipDesign B, clone revision `3336047c1be4e0ed5217ec57abcbd8df693224f2`, is a met register without human-readable capability or action assertions (`.ufo/waves/round-35/c0/CtlSkipDesign.md:153-157,210-231`).

Mechanism: the row checker examines shape, key, round and evidence but never compares cells 2–3 with the oracle capability text (`.ufo/waves/round-35/count-c1.py:141-191`). [INFERENCE] Replacing those empty cells with false non-pipe prose would preserve its result. I did not execute that substitution.

The closure can therefore object: zero structural mismatches can coexist with an unusable or misleading self-assessment. Artifact existence, change-in-round and mention in closure text establish provenance, not semantic entailment. For capabilities without a named path, the check is round-wide rather than statement-specific (`count-c1.py:125-132,181-186`). This threatens calibration, not coverage or operability; no new operational behavior is being claimed (`contract.md:16-20`).

This is a frozen measurement limitation, not an observed violation of its literal predicate. It is fixable in the delivered register and supporting review, but not by quietly adding semantic conditions to this round's counter or reclassifying a control after scoring. The prohibition is explicit in `../.ufo/prompts/mori-round-35.md:351-360`.

## Evidence that would answer it

- A committed eighteen-row register whose actual capability/action cells preserve the original closures' qualifications, with row-specific demonstration pointers. A path merely passing the provenance filter is insufficient to answer the semantic objection (`../AXES.md:61-64`; `contract.md:95-99`).
- A closure reviewer independently checking those literal statements against the original admitted demonstrations, recording supported/unsupported per row. Keep that evidence beside P-C1, not retroactively inside it (`.ufo/waves/round-35/evidence/c1-controls.txt:40-44`).
- An after receipt from the byte-identical frozen counter at the exact landed revision; do not claim this review supplied it (`.ufo/waves/round-35/contract.md:103-104`; frozen identities `.ufo/waves/round-35/evidence/c1-freeze.txt:1-6`).

These would answer whether the actual table is a useful, faithful correction. They would not make P-C1 alone a semantic truth test. If the canonical judge finds that missing distinction essential to admissibility, preserve the frozen claim and record the miss rather than changing the target (`../.ufo/prompts/mori-round-35.md:351-360`).

## Smallest safe correction

Do not amend the frozen counter, oracle, predicate, axis or first-working rounds. Make the new section's authority and limits explicit, and supply the separate row review already anticipated by the frozen residual. This also avoids treating the earlier none-yet table and round-12 table as competing current authorities: both remain in `SCORECARD.md:586-592,627-635`, while the parser selects only the last capabilities section (`count-c1.py:65-87`).

```DRAFT SCORECARD.md current-register preamble
This is the current closure-bound capabilities register; earlier capabilities sections are historical snapshots. P-C1 measures key, round and evidence-provenance mismatches against the pinned closure record. Capability/action prose is assessed separately. Restoring historical entries does not acquire new round-35 capabilities or demonstrate current runtime correctness.
```

The draft restates the frozen scope and residual, rather than narrowing the predicate after data (`.ufo/waves/round-35/contract.md:16-31,95-99`).

## Inspection record

- Read the scoped prompt, axes, frozen contract/counter, before/freeze/control receipts and cited C0 reports; no counter or test was rerun.
- Read fleet MANIFEST using `timeout 120 prlimit --as=536870912 --cpu=110 git -C /home/vgpnk/Projects/shokunin show 37b51a243302e8009c7067431e8a47f9a722fd14:MANIFEST.json`, piped to a timeout/memory-bounded jq projection of admitted mori capability-bearing entries. Output indices: 313, 339, 345, 353, 386, 398, 427, 443, 455, 462, 476, 495; respective capability counts: 1, 1, 1, 1, 3, 1, 1, 2, 2, 1, 2, 2, totaling 18.
- Timestamp command: `timeout 10 prlimit --as=268435456 --cpu=5 date -u +%FT%TZ` returned `2026-10-23T08:54:27Z`.
- Tools installed/updated: none. No scratch files, background jobs or subagents were created. All started foreground commands completed; no process tree remains to stop.
