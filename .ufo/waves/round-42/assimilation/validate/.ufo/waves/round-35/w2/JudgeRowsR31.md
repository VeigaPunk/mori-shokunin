measured 2026-10-23T09:17:33Z

# JudgeRowsR31 — mori round-31 register rows (wave 2, non-author)

Scope: final `## Capabilities` section of SCORECARD.md@cedb0ec4f3a4f672804deac388b7191258f01fcd, rows
`rounds[495].capabilities_added[0]` (SCORECARD.md:1977) and `rounds[495].capabilities_added[1]` (SCORECARD.md:1978) —
the last two lines of the section. Closure record: fleet MANIFEST.json@37b51a24 `rounds[495]` (admitted, mori
`lane_round` 31, commit `mori-shokunin@52435f2f425c2b4a5e7ba63d7abc1292b8736367`), spotcheck
`corpus/lessons/round-31-verifier-spotcheck.md@641a6e86`, fleet report `.ufo/reports/round-31/mori.md`@37b51a24.
Rule (c1-controls.txt:41-42 verbatim): (a) non-empty, closure-faithful capability and what cells; (b) evidence cells
holding only backticked paths; judged `supported`/`unsupported`. (c) pointer-relevance judged separately.
Lane and fleet were read-only; copies of every artifact in /fast/scratch/hyaku/mori-r35/JudgeRowsR31/.

## Row [0] — `blind-writer gate` / `tools/mori-blind-check.sh`

MANIFEST `capabilities_added[0]`: tools/mori-blind-check.sh (blind-writer gate, --selftest; supersedes round-30 wave
gate, routed D1).

(a) Capability cell `blind-writer gate` is non-empty and matches the record's own wording. What cell, sentence by
sentence:

- "passing --selftest" — fleet report: "C2 landed `458ff1c3` … `--selftest` PASS"; committed receipt
  `.ufo/waves/round-31/evidence/c2-tool-selftest-and-r30.txt`@52435f2f shows `PASS`, `exit=0`; spotcheck §3 C2
  "Self-test: `--selftest` → `PASS exit=0`". Reproduced this seat: `bash mori-blind-check.sh --selftest` on the
  closure blob (sha256 `79b774f7…beb8`, blob `3c26ef69…`, both matching the spotcheck's digests) → `PASS`, exit=0.
- "on the round-30 inputs it reports three missing-list hits" — fleet report: "round-30 writer wave → the three
  missing-list hits wave-1 RealBriefsR30 derived by hand"; spotcheck: "the round-30 writer wave at `5c99f2d4` gives
  `scanned=4 blind_violations=3 exit=1`"; receipt lines are exactly three `writer-missing-files-opened-list` hits
  (CaseR30a.md:1, CaseR30b.md:1, CaseR30d.md:1). Reproduced this seat: closure tool + closure-committed allow file
  `.ufo/waves/round-31/evidence/allow-r30.txt` over rev `5c99f2d4` → `scanned=4`, `blind_violations=3`, the same
  three missing-list lines, exit=1.
- "no longer flags CaseR30a.md:105" — fleet report: "`CaseR30a.md:105` no longer a hit"; in my rerun CaseR30a is hit
  only at `:1` (missing-list), no `:105` hit.
- "supersedes the round-30 wave gate (routed D1)" — the MANIFEST string itself; spotcheck §3 C2: the claim
  supersedes the round-30 gate (routed D1), and the prior checks were only wave-local
  `.ufo/waves/round-{29,30}/check-blind-wave.sh`.

All four facts are stated by the record and bounded as the record bounds them (fixture/wave behavior only; no live
coverage claim).

(b) Evidence cell is exactly one backticked path, `` `tools/mori-blind-check.sh` ``. Holds.

VERDICT: rounds[495].capabilities_added[0] supported

(c) Pointer-relevance: `tools/mori-blind-check.sh`@52435f2f IS this capability — a committed wave-report
blind-writer gate (`run_gate` scans a committed wave-report dir for writer-typed files, detecting
`writer-missing-files-opened-list`, `writer-forbidden-opened-path`, `writer-tool-source-citation`,
`writer-tool-run-output`; `usage` and `--selftest` in-file). This is the MANIFEST/C2 capability, not the C1 table.

VERDICT: rounds[495].capabilities_added[0] pointer-relevance holds

## Row [1] — `watchdog identity decision table` / `corpus/knowledge/watchdog-identity-r31.md`

MANIFEST `capabilities_added[1]`: corpus/knowledge/watchdog-identity-r31.md (pid-probe watchdog-identity decision
table, S161-S174).

(a) Capability cell non-empty, faithful. What cell, sentence by sentence:

- "A sourced FR5 table (S161-S174)" — artifact@52435f2f title line 5: "Watchdog identity from a pid probe — what
  each observation can and cannot establish (FR5)"; `source:` line :1 lists S161–S165, S167, S169–S174 plus prior
  S027. The record itself bounds the label inclusively ("S161-S174" in the MANIFEST string); the fleet report Gate
  discloses "12 admitted, 2 rejected" (S166, S168). Cell matches the record's own bound.
- "on what pid probes can and cannot establish about watchdog liveness" — entry :5 and :14-17 (each row: what a
  probe sees, what it does and does not establish, the census verdict); fleet report C1: "a sourced decision table
  … how a pid probe can and cannot establish that the fleet watchdog is alive"; spotcheck §3 C1. Faithful.
- "measurements used throwaway processes" — entry :2: "live probes wave-1 LiveCommProbe and LiveArgvProbe on
  throwaway processes only"; fleet report: "live probes on throwaway processes". Faithful.
- "did not change the census probe" — entry :62: "No row changes the census probe"; fleet report: "the census probe
  is unchanged"; spotcheck §8 carry-over names the unchanged FR5 census probe. Faithful.

All four facts stated by the record, bounded as bounded there.

(b) Evidence cell is exactly one backticked path, `` `corpus/knowledge/watchdog-identity-r31.md` ``. Holds.

VERDICT: rounds[495].capabilities_added[1] supported

(c) Pointer-relevance: `corpus/knowledge/watchdog-identity-r31.md`@52435f2f (blob `21a17445…`) IS this capability —
a 14-row `observation|reading|verdict|sources` decision table (:19-34) on pid-probe watchdog liveness, FR5-scoped,
with the S161–S174 source list. MANIFEST/C1 capability, not the gate tool.

VERDICT: rounds[495].capabilities_added[1] pointer-relevance holds

## Residual notes (not defects under this rule)

- Entry row 9 carries an `[INFERENCE]` marker (judged unsupported by the round-31 row judge and disclosed by the
  closure); the register cell claims the table exists and what it covers — which the record states — not that every
  row is supported.
- Verification gaps closed here: `--selftest` and the round-30 writer-wave run reproduced first-hand on the exact
  closure bytes, matching the committed receipts verbatim.
- Installs: none. No lane/fleet writes; all commands capped with timeout.
