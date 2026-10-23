measured 2026-10-23T09:13:31Z

# JudgeRowsR26 — register rows for mori round 26 at cedb0ec4

Scope: rows keyed `rounds[462].capabilities_added[0]` in the final `## Capabilities` section of
SCORECARD.md at `cedb0ec4f3a4f672804deac388b7191258f01fcd`. That key is confirmed unique: `rounds[462]` is the only
mori round-26 closure in MANIFEST.json@37b51a24 (`python3` index check prints `[462]`).

Row under test (SCORECARD.md at cedb0ec4, the row is one line; shown here split for readability):

- key: `rounds[462].capabilities_added[0]`
- capability: `userspace OOM killer one-shot read`
- what: `Reads earlyoom and systemd-oomd unit state, earlyoom startup thresholds, counts of earlyoom send,
  escalation, failed-kill and low-memory lines this invocation and oomd kill notices this boot; KILLER_ACTED,
  KILLERS_UNKNOWN or KILLERS_QUIET; counts are log lines, not processes.`
- evidence: `` `tools/mori-oom-killers.py` `` (single backticked path, nothing else in the cell)
- first-working round: `26`

Record: MANIFEST rounds[462].capabilities_added[0] @37b51a24: "userspace OOM killer one-shot read
(tools/mori-oom-killers.py, blob 3fb78bbc): earlyoom 1.9.0 and systemd-oomd unit state, earlyoom version and four
startup thresholds, counts of earlyoom send/escalation/failed-kill/low-memory lines for the current invocation,
oomd kill notices this boot, KILLER_ACTED/KILLERS_UNKNOWN/KILLERS_QUIET verdict; frozen selftest PASS 32/32 over
cases blob 5b4dcee7 landed at 5b10649d before the tool c2fdd929 (evidence-verified at 950d8a56, tool and cases
bytes equal at head); amendment-A2 rules pinned by no case file (detector inputs only); counts are log lines, not
processes killed". Closure record also: fleet report .ufo/reports/round-26/mori.md @37b51a24 and
corpus/lessons/round-26-verifier-spotcheck.md @fc09f96c.

## (a) Sentence-by-sentence faithfulness

1. Capability cell `userspace OOM killer one-shot read` — verbatim prefix of the MANIFEST string. Supported.
2. `Reads earlyoom and systemd-oomd unit state` — record: "earlyoom 1.9.0 and systemd-oomd unit state". The register
   drops the `1.9.0` qualifier; weaker, not broader. Spot-check (host probe: earlyoom active/enabled, oomd
   inactive/disabled) confirms unit state is what the tool reads. Supported.
3. `earlyoom startup thresholds` — record: "earlyoom version and four startup thresholds". The register omits the
   version and the count four; strictly a subset of the record's claim, no overclaim. Supported.
4. `counts of earlyoom send, escalation, failed-kill and low-memory lines this invocation` — record: "counts of
   earlyoom send/escalation/failed-kill/low-memory lines for the current invocation". Same items, same bound
   (current invocation ≙ "this invocation"). Supported.
5. `oomd kill notices this boot` — verbatim from the record. Supported.
6. `KILLER_ACTED, KILLERS_UNKNOWN or KILLERS_QUIET` — the record's three verdicts, re-spelled as a disjunction.
   Supported.
7. `counts are log lines, not processes` — record bound: "counts are log lines, not processes killed". The register's
   weaker spelling does not claim a count the record does not give. Supported.

Facts in the record not restated by the row (selftest 32/32, freeze order, blob ids, A2 disclosure): omissions are
permitted by the rule — it requires every stated fact to be recorded, not completeness. No stated fact in either cell
is absent from the record, and no stated fact exceeds the record's bounds.

## (b) Evidence cell contents

The cell holds exactly one backticked path and nothing else. Supported.

## (c) Pointer relevance (outside the rule)

`git rev-parse ef9dbee1:tools/mori-oom-killers.py` = `3fb78bbc2612c38e463e04083bdb213954647568` — byte-identical to
the blob the capability string names. The file's docstring ("Read-only survey of this host's userspace OOM killers
(FR10)... round 26, claim C2") and code implement THIS capability: `unit_state()` reads both units'
LoadState/ActiveState/UnitFileState (lines 191–214); `read_inputs()` counts sigterm/sigkill/escalation/kill_failed/
low-memory classes for the current invocation and oomd notices this boot (lines 240–372); verdict emitted as
KILLER_ACTED/KILLERS_UNKNOWN/KILLERS_QUIET with matching exit codes (lines 461–465). The pointer is not to another
round-26 artifact (the round's other artifact is the C1 corpus entry, not the evidence named here).

## Verdicts

VERDICT: rounds[462].capabilities_added[0] supported
VERDICT: rounds[462].capabilities_added[0] pointer-relevance holds

## Residual risk / gaps

- Wording drift `not processes` vs `not processes killed` and the dropped `1.9.0`/`four`/`version` qualifiers are
  weakenings, not defects; a reader wanting the selftest and A2-disclosure facts must go to the record. [INFERENCE]
- Checks exercised: MANIFEST string read at 37b51a24; row read at cedb0ec4; tool read and blob-hashed at ef9dbee1;
  spot-check and fleet report read. No selftest was run (none required by the rule).
- Installs: none.
