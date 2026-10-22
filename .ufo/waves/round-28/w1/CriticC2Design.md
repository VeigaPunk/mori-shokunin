# Round 28 wave 1 — CriticC2Design: attack on C2 design and the required-field map, before any case exists

Seat: MoriR28.CriticC2Design (critic, leaf). Written 2026-10-22, last clock read `2026-10-22T18:03:45Z`.
At that time `.ufo/waves/round-28/w1/` held no CaseA2r* report (`ls -la` shows only ScoutSurfaceRecon.md and
swarm-registry.json), so the assembly findings are about the design, not about real cases.

**Blind-seat warning: this report quotes the tool's behaviour on invented A2-shaped inputs. The CaseA2r* writers
must not open it before the freeze commit.** If a writer's transcript shows a read of this file, that writer's
cases are tainted (see F5).

## Verdict in one paragraph

The required-field map is right for 6 of 10 rules. It is wrong for A2-07: the named field takes the same value with
and without the A2-07 fix, and for the stopped-unit shape that motivated the rule it is absent from the result. It
names an input echo, not the decided output, for A2-08 and A2-09. The two-cases-per-rule floor counts volume, not
discrimination. The rule A2-10 text and the tool disagree on three shapes, and no frozen round-26 case blocks a
tool change there. So the contract's only mismatch rule ("the L1 may change the tool, never the case file") pushes
the L1, who is not blind, toward removing positive evidence from the tool to meet C2. Blindness of the writers is
self-reported. The non-blind L1 assembles the file, and nothing checks the assembled bytes against the writers'
reports.

## Method (read-only; nothing written outside this report)

The tool was loaded in memory from git blobs (`git show <rev>:tools/mori-oom-killers.py`, `exec`, `python3 -I -B`).
Its pure reader `read_inputs` ran on nine invented inputs at the tip `079a47c` and at the commit before each A2 rule
landed. The commit order comes from `git log --follow -- tools/mori-oom-killers.py`:

| rule ids | landed in | pre-rule blob used |
|---|---|---|
| A2-01..A2-04 | `825f988` | `278f02e` |
| A2-05 | `93aa1b9` | `825f988` |
| A2-06 | `738eec1` | `93aa1b9` |
| A2-07, A2-08, A2-09 | `f1efb46` | `738eec1` |
| A2-10 | `950d8a5` | `f1efb46` |

The inputs are invented: an active unit with an `ActiveEnterTimestampMonotonic` (AETM) of 5000 or 0, an inactive
unit, a `not-found` unit, a `failed` unit, version lines, `dryrun mode enabled`, and send lines with or without
`__MONOTONIC_TIMESTAMP`. Output columns: `state`, `scope_complete`, `actions.sigterm`, `dryrun_send_lines`,
`earlier_invocation_send_lines`, `verdict`. `MISSING` means `_lookup` (tool :610-618) finds no such path, so a
case that pins that path fails with "missing in result" (tool :705-710).

## Findings, ranked

### F1 (high, fail-open in the counter and blocks the writer): the A2-07 required field does not decide A2-07

- Rule: "one dry-run invocation does not zero another invocation's real sends" (r27 contract :55). Earlier
  invocations are counted only in `earlyoom.earlier_invocation_send_lines` (r26 contract :175-176). An inactive
  or absent killer reports `actions: null` (r26 contract :102).
- Run E1, active unit with a real earlier invocation, a dry-run earlier invocation and a real current invocation:
  tip `sigterm 1`, `earlier_invocation_send_lines 1`, `KILLER_ACTED`; pre-A2-07 blob `738eec1` `sigterm 1`,
  `earlier_invocation_send_lines 0`, `KILLER_ACTED`. `actions.sigterm` is 1 on all six blobs, back to `278f02e`.
- Run E2, the Y1 shape (inactive unit, real invocation then dry-run invocation): tip `actions.sigterm MISSING`,
  `earlier 1`, `KILLER_ACTED`; pre-A2-07 `earlier 0`, `KILLERS_QUIET`.
- Consequence: a case that meets the map ("pins actions.sigterm or actions.sigkill") is either blind to A2-07 (E1)
  or fails on the correct tool (E2). Under the map, a post-freeze tool change that reverts A2-07 keeps `C2=met`.
- Smallest correction: A2-07 required field = `earlyoom.earlier_invocation_send_lines`, with at least one A2-07
  case whose value is greater than 0 and whose journal holds a dry-run invocation outside the current one. Change
  `count-c2.sh` and tell CaseA2r07 before the freeze.

### F2 (high, predicted mismatch with no safe outcome): A2-10 text and the tool disagree on three shapes

- Text: a record without a numeric `__MONOTONIC_TIMESTAMP` "is now left uncounted and makes the scope incomplete;
  positive evidence elsewhere still stands" (r26 contract :186-187; r27 contract :58). The text has no condition.
- The tool skips such a record only for an active unit with a bounded invocation (tool :288-297). Elsewhere it
  counts the record:
  - E3, active unit, AETM 0, one untimestamped send: tip `sigterm 1`, `KILLER_ACTED`. By the text: uncounted, no
    positive evidence, scope incomplete, so `KILLERS_UNKNOWN`.
  - E4, inactive unit, one untimestamped send: tip `earlier_invocation_send_lines 1`, `KILLER_ACTED`. By the text:
    uncounted, so not `KILLER_ACTED`.
  - E5, active unit, bounded, one untimestamped send: tip `sigterm 0`, `earlier_invocation_send_lines 1`,
    `KILLERS_UNKNOWN`. The record is counted as an earlier-invocation send (tool :310-331). By the text: 0.
- The A2-10 writer prompt says "vary state, invocation boundaries" (`wave1-spec.json`, CaseA2r* prompt). So a
  faithful blind writer is likely to produce E3, E4 or E5 [INFERENCE].
- No frozen case can block a tool change here. The scan of `cases.json` (32 cases) finds no record without a
  numeric timestamp; only `cases-supplementary.json` c35 (active, bounded) has one. The contract's backstop
  (r28 contract :56-57) therefore never fires.
- So the contract lets the L1 make the tool read an untimestamped real SIGTERM of a stopped earlyoom as quiet
  (E4). That hides evidence to fit an over-broad changelog sentence. The tool's branch is defensible: an unbounded
  or stopped invocation needs no placement (comment at tool :280-286).
- This is a text-versus-tool question for a judge, not for the L1. Axes: operability, discernment.
- Smallest correction: see F6 (adjudication before any tool change, plus a no-evidence-removal rule).

### F3 (medium, non-discriminating map entries): A2-08 and A2-09 pin an input echo; A2-02/01/05/10 pin presence, not value

- A2-09: `state` is `absent` on every blob, because `not-found` maps to `absent` in tool :201-202, which predates
  A2. In E8 the A2-09 change shows only in the verdict (`KILLERS_QUIET` before, `KILLER_ACTED` after) and in
  `earlier_invocation_send_lines` (`null` before, 1 after).
  - The verdict is always pinned, so this entry is redundant rather than fail-open.
  - The r26 contract never says that `not-found` maps to `absent`. A writer can learn it only from frozen `c07`.
- A2-08: E7 (inactive unit, null journal) gives `KILLERS_QUIET` before the change and `KILLERS_UNKNOWN` after;
  `state` is `inactive` on both. "A value other than active" also admits `unavailable`, which reads
  `KILLERS_UNKNOWN` on every blob since `825f988` (E9). An `unavailable` case therefore meets the map and pins
  nothing.
- Presence only: a writer's control case can be the only case that pins the field. Examples: A2-01 with
  `scope_complete: true` and no Suppressed line in scope, or A2-02 with `state: active`. The tag-trust gap of r27
  F1 (`round-27/w1/CriticC2Counter.md:56-67`) survives the r28 hardening.
- Smallest correction (value constraints, at least one case per rule):

| rule | constraint on at least one case |
|---|---|
| A2-01, A2-05, A2-10 | `scope_complete` = false |
| A2-02 | `state` = `unavailable` |
| A2-03, A2-04, A2-06, A2-07 | the named count > 0 |
| A2-08 | `state` in {`inactive`, `absent`}, verdict `KILLERS_UNKNOWN` |
| A2-09 | pin `earlier_invocation_send_lines` > 0, verdict `KILLER_ACTED` |

### F4 (medium): "at least 20 cases and 2 per rule with distinct inputs" counts volume, not pinning

- "Distinct" is satisfied by a one-microsecond timestamp change. Two cases can sit on the same branch.
- The counter requires none of the branches the text names: A2-06 active versus not active (r27 :54), A2-10
  positive evidence elsewhere versus none (r27 :58), A2-08 "any earlyoom state" (r27 :56).
- The pinning test is discrimination. Each rule needs at least one case that the tool passes at the tip and that
  fails on the pre-rule blob in the Method table. The blobs are fixed hashes, so a later tool change cannot move
  this test.
- Pre-rule blob differences seen: E2, E7 and E8 differ in verdict; E9 (A2-02) in state (`inactive` on `278f02e`,
  `unavailable` after); E1 only in `earlier_invocation_send_lines`.
- Limit: A2-01..A2-04 share one pre-rule blob, so a case can "discriminate" through a sibling rule. Disclose it, or
  use in-memory single-rule reverts like r27 S11.
- Smallest correction: `count-c2.sh` runs `read_inputs` from each pre-rule blob on `cases-a2.json` and requires,
  per rule, at least one case of that rule that fails there. Twenty cases then becomes a floor, not the proof.

### F5 (medium): blindness is asserted, not evidenced, and the assembler is not blind

- What the writers are told (`wave1-spec.json`, CaseA2r* prompt): forbidden are the tool, `round-26/evidence/`
  and the round-26 and round-27 `w1` and `w2` directories; allowed only are the r27 contract :40-80, the r26
  contract, `cases.json` and upstream earlyoom; required is a self-reported list of the files they opened.
- Channels the prompt does not name, which only the "ONLY" whitelist blocks: SKILL.md :698 and :716 (the tool's
  earlier-invocation semantics); commit subjects (`738eec1`: "a stopped earlyoom with sends this boot reads
  KILLER_ACTED"); `cases-supplementary.json`; LOG.md; sibling round-28 `w1` reports, including this one and
  ReviewA2SpecVsTool; a sandbox clone, which carries the tool.
- The whitelisted r26 contract :183-184 points into the forbidden `evidence/a2-detectors/`.
- The r26 report directories are named, so a writer could have seen the tool through r26 reports only by breaking
  the prompt. A self-report would not show that.
- Assembly: L1 MoriR28 has read the tool and the A2 detectors, and transcribes the writers' fenced arrays into one
  file. An edited expectation during assembly would leave the file "blind" in name only. Nothing in the counter
  (r28 contract :49-53) compares the file to the writer reports.
- Tradeoff, not defect: the A2 rule text is the tool author's changelog, written "after the tool landed" (r26
  :152). Blind cases test the tool against its author's description. F2 is exactly where that is still worth doing.
- Smallest correction, all before the freeze commit:
  1. A non-author seat reads each writer transcript (`history://MoriR28.CaseA2rNN`). It commits a per-writer list
     of paths read, grepped or run: paths only, no session fields. Any touch of the tool, of a forbidden directory,
     of `git log` or `git show` on the tool, or of a round-28 `w1` report taints that writer.
  2. The counter or a committed receipt checks that every case in `cases-a2.json` is JSON-canonical-equal to a case
     in that writer's committed report, and that the case's `rule` matches the writer's seat.
  3. A dead or tainted writer leaves its rule uncovered, which is a miss. A replacement is valid only under the same
     audit; an L1-written case is never valid (r27 W1 precedent).

### F6 (medium): the mismatch rule has one exit (change the tool), and the decider is the non-blind L1

- r28 contract :56-57: "the L1 may change the tool (never the case file)"; breaking a frozen r26 case is a miss.
- No path exists for a case error. Example E6: inactive unit, null journal, `oomd_notices` 2. A literal A2-08
  reader expects `KILLERS_UNKNOWN`. The tool gives `KILLER_ACTED`, by rule 1 precedence ("Positive evidence
  stands", r26 :97-98).
- No path exists for text ambiguity (F2).
- The backstop covers only the 32 frozen shapes. The A2 shapes are unpinned by definition (r27 :43-44).
- Smallest correction, declared before the freeze:
  1. A non-author adjudicator, neither the L1 nor the writer, classifies each failing case before any tool edit.
     The classes are tool error, case error and text ambiguous. The record cites the r26 contract line that decides
     the case.
  2. A tool error allows a tool change only if:
     - `cases.json`, `cases-supplementary.json` and the `evidence/a2-detectors` inputs keep their outputs, or each
       change is disclosed;
     - no change turns a `KILLER_ACTED` input into `KILLERS_QUIET`.
  3. A case error or a text ambiguity makes C2 a reported miss, routed as a text amendment. Neither cases nor the
     counter are touched.
  4. The outside verifier re-runs the counter. Any post-freeze change to `cases-a2.json`, `count-c2.sh` or this
     rule is narrowing.

### F7 (medium, carried from r27 F4 and not covered by the listed hardening): the comparator is part of the changeable tool

- The tool may change after the freeze (r28 :56). PASS is decided by the tool's own `run_selftest`, `_lookup` and
  `_values_equal` (tool :610-733).
- Example: a `_values_equal` that returns True prints one `PASS N/N` line and exits 0. That meets "exit 0 and
  exactly one SELFTEST line" (r28 :52).
- r27 `CriticC2Counter.md:107-109` says no counter can catch this. A counter can. Smallest correction, in
  `count-c2.sh`: diff those three functions against the `079a47c` blob and require no change, or drive the landed
  `read_inputs` with the counter's own comparator.

### F8 (low): assembly clashes

- Ids cannot clash across writers, because the prompt fixes the prefix `a2-NN-<slug>`. Within one writer, a
  duplicate is caught by the counter's unique-id check.
- Same inputs under two rules: with equal `expect`, the case is double-counted toward the 20; with different
  `expect`, at most one can pass, so C2 is unmet. That is real signal about the text and must not be resolved by
  dropping one.
- The predicted overlaps are A2-05 with A2-10 (E3) and A2-06 with A2-10 (E5).
- Smallest correction: the freeze LOG lists the canonical-inputs duplicates across rules. They are counted once
  toward the 20, and contradictory pairs are routed to F6.

### F9 (low): A2-06 wording differs between the two whitelisted texts

- r27 :54 says "send lines". r26 :176 says "send and escalation lines", and the tool counts escalations
  (tool :329). A writer who works from the table alone misses escalations.
- Correction: none needed if the adjudicator (F6) treats r26 :176 as deciding. State that in the adjudication rule.

## Required-field map, judged

| rule | map | decides the rule? | evidence |
|---|---|---|---|
| A2-01 | `scope_complete` | yes (needs value false) | r27 :49 |
| A2-02 | `state` | yes (needs `unavailable`) | E9: `inactive` on `278f02e`, `unavailable` after |
| A2-03 | `process_group_lines` | yes (needs > 0) | r27 F2/S11 |
| A2-04 | `dryrun_send_lines` | yes (needs > 0) | r26 :166-167 |
| A2-05 | `scope_complete` | yes (needs false) | r26 :173-174 |
| A2-06 | `earlier_invocation_send_lines` | yes (needs both branches) | r27 :54 |
| A2-07 | `actions.sigterm` / `.sigkill` | **no** | E1 same value pre and post; E2 MISSING |
| A2-08 | `state` not active | input echo; verdict decides | E7, E9 |
| A2-09 | `state` | input echo; verdict and earlier count decide | E8 |
| A2-10 | `scope_complete` | yes, but text and tool conflict on 3 shapes | E3-E5 |

## Run record (command abbreviated; the inputs are invented; no file written)

```text
python3 -I -B - (load blobs 079a47c 738eec1 f1efb46 93aa1b9 825f988 278f02e; read_inputs on E1..E9)
E1 tip sigterm=1 earlier=1 ACTED | 738eec1 sigterm=1 earlier=0 ACTED
E2 tip sigterm=MISSING earlier=1 ACTED | 738eec1 earlier=0 QUIET
E3 tip scope=False sigterm=1 ACTED (A2-10 text: uncounted -> UNKNOWN)
E4 tip inactive earlier=1 ACTED (text: uncounted)
E5 tip sigterm=0 earlier=1 UNKNOWN (text: earlier 0)
E6 tip inactive null journal + oomd 2 -> ACTED on all blobs
E7 tip inactive null journal -> UNKNOWN | 738eec1 QUIET
E8 tip absent earlier=1 ACTED | 738eec1 absent earlier=null QUIET
E9 tip failed -> unavailable UNKNOWN | 278f02e inactive QUIET
frozen cases.json: 0 records without a numeric timestamp (supplementary c35 only)
```

## Smallest safe correction set (before any case is frozen)

```text
1. count-c2.sh: A2-07 required field -> earlyoom.earlier_invocation_send_lines (>0 in >=1 case); per-rule value
   constraints of F3; per-rule discrimination against the pre-rule blobs of the Method table (F4); the comparator
   functions are unchanged from 079a47c, or the counter uses its own comparator (F7).
2. Tell CaseA2r07, CaseA2r08 and CaseA2r09 the corrected pins now. Status 18:06Z (MoriR28 reply): A2-07 field
   adopted, CaseA2r07 and BuildCountC2 told; A2-10 held for a post-freeze judgment, but item 4 must precede the freeze.
3. Freeze batch: a non-author transcript audit per writer; each case canonical-equal to its writer's report; the
   cross-rule duplicate list (F5, F8).
4. Contract amendment (dated, before the freeze): non-author mismatch adjudication; no tool change may turn
   KILLER_ACTED into KILLERS_QUIET; a case error or text ambiguity is a reported miss (F2, F6).
```

## Impacted axes

Operability, C2's substance (F1, F3, F4, F7); discernment, a hidden tool regression under the mismatch rule (F2,
F6); calibration, a claim met while overstated (F1, F3, F4); provenance, blindness and assembly (F5, F8).

## Tooling and bounds

No tool installed or updated; no subagent; no file written outside this report; only read-only git (`show`, `log`,
`grep`) in the lane; no unit, host value or session field read or copied. One message sent to agent://MoriR28.
