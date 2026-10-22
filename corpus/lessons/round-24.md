# Round 24 (attempt 2) — routed repair and system pressure

author: MoriR24 (L1, fresh in-session lane subagent); wave-1 seat reports under
`.ufo/waves/round-24/w1/`. Entering tip `c725aa37aa3c9ec4f34e3c2abc8ca1b616c7c130`.
Contract and amendments A1–A4: `.ufo/waves/round-24/contract.md`.

## Claims and authority

- C1 (calibration): `tools/mori-routed-check.py` checks the four byte-checkable items
  routed by `corpus/lessons/round-23-verifier-spotcheck.md:60-66`. R4 (dispatch bound
  before the call) is the repair; R1–R3 are regression guards (amendment A4). Routed
  item 5 is an adjacency boundary without a byte predicate and is not counted.
- C2 (coverage, FR12 one-shot part): `tools/mori-pressure.py` reads system
  `/proc/pressure/{cpu,memory,io,irq}`; knowledge entry
  `corpus/knowledge/system-pressure-r24.md`; sources S090–S096 opened this round.
- Nothing here is admission. A non-author closure judges the round.

## Gate

Every row below was opened this round by a wave-1 scribe seat; the digest is SHA-256 of
the fetched bytes (first 16 hex). Quotes are copied exactly and are at most 25 words.

| id | URL | accessed (UTC) | anchors verified | located quote |
|---|---|---|---|---|
| S090 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst | 2026-10-22T08:14:33Z (sha256 11c6b7129103b454) | 37-38, 40-43, 57-58, 60-65, 102-110, 181-185 | 57–58: "CPU full is undefined at the system level, but has been reported since 5.13, so it is set to zero for backward compatibility." |
| S091 | https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c | 2026-10-22T08:14:54Z (sha256 452318beaca3e6d1) | 1257-1263, 1273-1291, 1710-1721 | 1282-1283: "/* CPU FULL is undefined at the system level */ if (!(group == &psi_system && res == PSI_CPU && full)) {" |
| S092 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst | 2026-10-22T08:15:00Z (sha256 a9433bb0e16a67f0) | 1066-1087, 1215-1221, 1911-1915, 2171-2175 | 1073-1074: "This control attribute is not hierarchical, so disable or enable PSI accounting in a cgroup does not affect PSI accounting in descendants" |
| S093 | https://raw.githubusercontent.com/torvalds/linux/v7.2/init/Kconfig | 2026-10-22T08:14:40Z (sha256 a43f09d89309a6bd) | 615-624, 723-760 | 730–733: "If you say Y here, the kernel will create /proc/pressure/ with the pressure statistics files cpu, memory, and io." |
| S094 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/kernel-parameters.txt | 2026-10-22T08:15:07Z (sha256 23b1a690210b6884) | 5505-5507 | 5505: "psi= [KNL] Enable or disable pressure stall information" |
| S095 | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/psi_types.h | 2026-10-22T08:14:51Z (sha256 483269b27c82b438) | 41-49, 51-56, 57-70 | 54-55: "SOME: Stalled tasks & working tasks" / "FULL: Stalled tasks & no working tasks" |
| S096 | https://github.com/torvalds/linux/commit/52b1364ba0b105122d6de0e719b36db705011ac1 | 2026-10-22T08:15:40Z | commit message paragraphs 3-4; psi_show only_full hunk | "IRQ/SOFTIRQ always happen in the current task on the CPU, make nothing productive could run even if it were runnable, so we only use PSI_IRQ_FULL." |
| S097 (rejected) | https://man7.org/linux/man-pages/man5/proc_pressure.5.html | 2026-10-22T08:21:46Z (HTTP 404, sha256 80c3fe2ae1062abf) | 404 body lines 3, 5, 6 | "The requested URL was not found on this server." |

Registry changes, old → new (all new rows; no older row changed):

- S090–S096: absent → `mined`, tier A, recheck `on-release`, used-by
  `corpus/knowledge/system-pressure-r24.md, corpus/lessons/round-24.md`.
- S097: absent → `rejected`, tier C, used-by `corpus/lessons/round-24.md`. Reason: the
  manual page the contract named does not exist (man-pages 6.20 has none). Flip: the
  man-pages project publishes a `proc_pressure` page.
- S001 (docs.kernel.org `psi.html`, opened 2026-10-19) is unchanged; S090 is the tag-pinned
  raw source of the same document with different line anchors, kept as a separate row
  because its URL and anchors differ (no duplicate-URL warning).
- New reading path "system pressure one-shot reading" in `## Paths`.

## Mistakes

| ID | Class | Evidence pointer | Captured-by | Fix / able to fail |
|---|---|---|---|---|
| M1 | lexical boundary loss in the record (word and number fused: `exit0`, `operability7/depth5`, `original25/26→26/26`) | `git show c725aa37:SCORECARD.md`; seat MineMistake counted 256 fused tokens in the file and 53 in the round-23 section (`.ufo/waves/round-24/w1/MineMistake.md`) | none (QUALITY 19 covers the regex side of word boundaries, not the record side) | `.ufo/waves/round-24/evidence/prose-fused-check.py`: exit 1 with 53 hits on the round-23 section, exit 0 on the same text after mechanical separation, exit 1 on one injected `exit1`. Applied as a ratchet to this round's added lines (result in the round-24 SCORECARD section). Round-23 bytes are not rewritten. |
| M2 | a frozen register the instrument cannot read | `.ufo/waves/round-24/frozen/c2-freeze-register.json` landed with `"tip": null`; `tools/mori-freeze-order.py check` exited 2 `invalid-register` | none before the run; the tool's own validator caught it (`tools/mori-freeze-order.py:183-196`) | measurement copy `.ufo/waves/round-24/evidence/c2-freeze-check-register.json` with the tip set; the frozen bytes stay unchanged; check exits 0 `pre-build`. Able to fail: the original register itself produced exit 2. |
| M3 | a pre-registration cited a source nobody had opened | contract C2 "Sourced" clause named proc_pressure(5); seat SrcProcPressureMan got HTTP 404 | SOURCES contract v1: a row is written only after its source is opened | rejection row S097; the knowledge entry cites only S090–S096. |
| M4 | a cause read into an error code | contract C2 said EOPNOTSUPP means PSI disabled; v7.2 removes `/proc/pressure` when PSI is boot-disabled (S091 1710-1721), and EOPNOTSUPP is a read-time return (S091 1257-1263) | none | amendment A2 before the tool landed: `unsupported` carries no cause; knowledge entry decision table row says so. |
| M5 | a before-value fixed by construction | CriticC1Vacuity: at `c725aa37` R1–R3 compare objects with themselves and R4 fails only for lack of a round-24 directory | QUALITY 70 (population identity) in spirit; no criterion on predicate vacuity | amendment A4: R4 is measured on the real round-23 defect (`--round 23`), R1–R3 relabeled regression guards. |
| M6 | a quoted pattern would have tripped its own predicate | ScoutRoutedBytes: 9 quoted hits of the privacy-clearance pattern under `.ufo/waves/` at base; wave reports quote it | none | amendment A1 limits R2 to self-assessment and knowledge surfaces. |
| M7 | seat scratch outside the session scratch root | seats SrcKconfig, SrcKernelParams, SrcPsiC, SrcProcPressureMan, CriticIntervalBoundary and FreezePressureCases wrote under `/tmp`; the wave-1 context did not name `/fast/scratch/hyaku/` as the only scratch root | session Boundaries ("Scratch goes under /fast/scratch/hyaku/") | wave-2 context names the scratch root; the round's `/tmp` residue is listed in the report. |
