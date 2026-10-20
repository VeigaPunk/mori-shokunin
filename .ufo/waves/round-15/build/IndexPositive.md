# IndexPositive — corpus index for round-15 mixed-class positive evidence

Scope: `corpus/README.md` only. No production, tool, source, registry, fleet, MANIFEST, SHONEN,
verifier or aggregator file was edited. No commits, builds, tests, linters, formatters or smoke
runs were executed. No tools were installed or upgraded; the host-safety directive (sync DB ~413
packages ahead) was received and no package-manager command was run.

## Files changed

| path | change |
|---|---|
| `corpus/README.md` | additive: coverage-map row for `knowledge/journal-positive-evidence-r15.md` (line 40); Known gaps bullet "Mixed-class positive preservation (round 15, decision table)" (lines 311-325); FR1 boundary sentence in the Frontier table (line 331) |

All earlier rows, bullets and Frontier rows are byte-preserved; every historical record remains.

## What the index says (behavior)

- Covered note: `corpus/knowledge/journal-positive-evidence-r15.md`, verified present at 302 lines
  after the creator confirmed landing (`MoriR15.KnowledgePositive` message, 2026-10-20). Read the
  whole note before indexing.
- Coverage-map "Holds" is the interface the note defines: the four per-scope tokens
  `positive_kernel_oom`, `positive_unit_oom`, `positive_unit_signal`, `positive_process_sigkill`
  count only object records with scalar matching `MESSAGE_ID` and scalar current `_BOOT_ID`
  (unit result exactly `oom-kill`/`signal`; process exactly `killed`+status 9), from the same
  single captured stream. A valid current-boot witness still raises the one critical
  `OOM_KILL_JOURNAL` line or the one user `KILL_SIGNAL_JOURNAL` WARN while an adjacent
  malformed/nonmatching/foreign-boot record leaves the raw aggregate/split class
  `unavailable:<reason>`. Raw counters and the INFO routing partition keep authority; positives
  are additive evidence.
- The qualifier states exactly what the round does not claim: decision table only, not full
  parsing, not completeness, not authenticated `MESSAGE_ID`s, not unique victims, not fleet
  membership; arbitrary malformed JSON is not repaired; a stream-level parse/capture failure or an
  identity-invalid sole positive still loses the alarm; no measurement is claimed and L1 owns
  delivered bytes.
- FR1 boundary row gains one appended sentence: round 15 adds mixed-class failure-mode coverage
  only, alarm preservation rather than full parsing or completeness. The pre-existing FR1 text
  is unchanged, so the round-13 advance and the kernel/fleet frontier stay on record.

## Exact retained evidence

- `ls`/`read` of `corpus/knowledge/journal-positive-evidence-r15.md`: present, 302 lines; Claim,
  Evidence 1–6, Decision table, alarm contract, INFERENCE/UNKNOWN, "What it changes for mori",
  "Delivery paths this cannot see", "Fills", "Provenance limits" all read.
- Creator reply (`agent://MoriR15.KnowledgePositive`, 2026-10-20): landed at the exact path; no
  measured receipt, no predicted tally, no journal/census/fixture/gate run by that seat; sources
  S014/S015/S037/S038 reopened 2026-10-20 with quotes <=25 words.
- `corpus/SOURCES.md` S014/S015/S037/S038 used-by cells already carry
  `corpus/knowledge/journal-positive-evidence-r15.md` (updated by `MoriR15.RegistryFrontier`);
  the README source cell records that, not a measurement.
- Note's `## Fills`: the r15 failure-mode row is coverage-map ground; FR1 itself (kernel
  event-time attribution, fleet correlation, unique victims) remains frontier.

## Risks / limits

- The indexed row deliberately describes an interface/decision table, not delivered or measured
  behavior; the note itself says the delivered census/gate is L1-owned. If L1 later lands a
  measured receipt, the note (not this row) should carry it; this index must not be read as a
  tally.
- FR1 wording was appended to a live Frontier boundary row, not to a historical Known gaps
  bullet; the historical bullet list is additive-only in this change.
- `positive_* = 0` on an unavailable aggregate is explicitly an observed-witness count, not a
  class total or evidence of absence; the README wording preserves that distinction.

## Blockers

None. The only dependency (new note exists) was verified before indexing; creator coordinated
directly and confirmed. L1 can run the post-integration gate (README renders, table row count
increased by one, no unrelated diff).
