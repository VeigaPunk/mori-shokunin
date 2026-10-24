# QualityCriteria — round 14

Seat: MoriR14.QualityCriteria (executor, leaf). Owned file: `corpus/QUALITY.md` only.
Assignment: append lesson-backed admission criteria Q29+ for (a) no-harm alarm/severity+owner
equivalence after a selector cutover, (b) UNKNOWN for missing unit attribution, (c) gate registry
and self-test on actually delivered bytes, (d) mutation attribution precision; and append an
explicit qualifier beneath the retained historical Q16 5/7/9 quote without rewriting it.

No build, test, lint, format or smoke command was run (contract). No tool was installed or updated.
No commit, push, sibling-file or protected-verifier write was made.

## Files changed

### 1. `corpus/QUALITY.md` — Q16 qualifier (appended at :33; original quote :32 unchanged)

- Existing line :32 (round-12 historical quote, kept byte-identical):
  `- "5 kernel kills vs 7 user + 9 system fe6faa94… notices, same boot" (round-12.md#M19)`
- New indented sub-bullet at :33 qualifies it: the 5/7/9 sample is text-selected because
  `journalctl --grep` matches `MESSAGE` and `--output-fields` restricts output, not matching; the
  "5 kernel kills" figure is a retained-journal record count, not a MESSAGE-free structured count,
  unique-victim tally, or structured gate.
- Anchors: `corpus/lessons/round-14.md#M6` (:19; its fix cell explicitly says to qualify the
  retained historical quote and never rewrite old append-only lessons) and
  `corpus/knowledge/kill-classes-by-message-id-r12.md` §"Round-13 correction — matching MESSAGE is
  not structured counting", which states the same measured fact. External confirmation:
  `corpus/lessons/round-13-verifier-spotcheck.md:137` (routed defect 6).

### 2. `corpus/QUALITY.md` — new section `## Criteria added round 14` (:69) with Q29–Q32 (:71–:74)

Q29 (:71) — no-harm alarm/severity+owner behavioral equivalence after selector cutover. A cutover
keeps, for every alarm it replaces: the same stable finding id, severity no lower, its prior verdict
effect on the roll, and the same named adjacent-owner route; a correct new typed counter does not
substitute for a discarded alarm unless before/after equivalence is measured on both revisions.
Anchors: `lessons/round-14.md#M1/M2` (:14–:15); evidence pointer
`round-13-verifier-spotcheck.md:72–89`, where the delivered cutover demoted critical
`OOM_KILL_JOURNAL` to INFO and dropped the tsukuroi-routed non-fleet finding.

Q30 (:72) — UNKNOWN for missing unit attribution. Classification reads the failed subject's own
`UNIT`/`USER_UNIT` structured metadata, never manager emitter fields; missing, malformed or
unreadable subject metadata is an explicit UNKNOWN/unavailable class and is never counted as fleet,
non-fleet or zero. Anchors: `lessons/round-14.md#M2` (:15) and its Gate rejection row
(:31: "Missing UNIT/USER_UNIT proves non-fleet membership | rejected | Missing evidence is unknown.
_SYSTEMD_UNIT describes emitter, not necessarily the failed subject."); external pointer
`round-13-verifier-spotcheck.md:86`.

Q31 (:73) — gate registry and self-test on delivered bytes. A verdict-producing gate carries its
PROTOCOL §Gate standard registry row at the lane registry home before results are cited, and any
self-test tally names the revision and is measured on the actually delivered gate bytes; an earlier
revision's tally or a predicted total is not a delivered-gate self-test. Anchors:
`lessons/round-14.md#M4` (:17); `PROTOCOL.md:375-421` §Gate standard (Registry, Self-test,
Two evidences); external observation `round-13-verifier-spotcheck.md:25,70` — 24 checks at
`80bd58a`, not the delivered `c13df48`.

Q32 (:74) — mutation attribution precision. A witness states the exact code delta (whole-function
transplant, reconstructed shim, or byte-exact original) and the causal scope it does not establish;
historical failures come from original frozen-byte runs, and a reconstruction never reads as
original-byte single-locus causality. Anchors: `lessons/round-14.md#M5` (:18); external observation
`round-13-verifier-spotcheck.md:57` — F01 whole `grade_lane`, F02 `frozen_source=null`
prefix-presence shim.

## Retained evidence

| Observation | Pointer |
|---|---|
| Q16 quote preserved; qualifier inserted immediately beneath it | `corpus/QUALITY.md:32-33` |
| New criteria section and numbering contiguous with Q28 | `corpus/QUALITY.md:63-74` (Q26–Q28 at :65–:67, heading at :69, Q29–Q32 at :71–:74) |
| Lesson mistake attribution used by the criteria | `corpus/lessons/round-14.md:14-19` (M1–M6 rows) |
| Gate-standard row fields and two-evidence/self-test obligations | `PROTOCOL.md:375-421` |
| External r13 closure pointers reused verbatim from the lesson evidence cells | `corpus/lessons/round-13-verifier-spotcheck.md:25,57,70,72-89,86,137` |
| Text-selection ground for the Q16 qualifier | `corpus/knowledge/kill-classes-by-message-id-r12.md` §"Round-13 correction"; `corpus/QUALITY.md:33` |

Criterion semantics stay at the claim-admission layer: they do not restate implementation, do not
waive Q3/Q15/Q16, and do not convert a notice count into victim or fleet-causation evidence. Q29
explicitly admits an alarm-preserving cutover while retaining the round-13 lesson's rejection of
cgroup-counter substitution (`lessons/round-14.md:31`).

## Risks

1. `AGENTS.md` requires every change to append a `LOG.md` entry. This seat does not own `LOG.md`;
   L1 must append the round-14 entry citing both QUALITY.md edits, or the change log will lag the
   file.
2. Criterion numbering is now fixed at Q29–Q32; any concurrent seat that cited "Q29+" for different
   subject matter must reconcile with these four operational meanings.
3. The criteria cite lesson mistake ids (`#M1`–`#M6`), which survive line edits; the external
   spotcheck pointers are line ranges in an append-only lesson file and remain valid unless that
   historical file is rewritten, which Q4/Q9 and the lesson itself forbid.
4. Q31 constrains registration and self-test provenance but deliberately does not name the new
   round-14 gate; the SkillRegistry/HarnessMigration seats own those bytes, and L1's post-integration
   measurement must supply the delivered-revision tally.

## Blockers

None. All named inputs resolved: lane AGENTS.md, round-14 lesson M1–M6, external r13 verifier
spotcheck, PROTOCOL §Gate standard, r12 kill-classes correction, and the r13 knowledge scope note.
