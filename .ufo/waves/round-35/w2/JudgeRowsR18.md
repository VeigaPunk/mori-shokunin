measured 2026-10-23T09:16:31Z

# JudgeRowsR18 — register rows for mori round 18

Seat: MoriR35.JudgeRowsR18 (wave-2 non-author reviewer, leaf).
Rule (verbatim, `.ufo/waves/round-35/evidence/c1-controls.txt` via assignment): each row is judged on
"(a) non-empty, closure-faithful capability and what cells and (b) evidence cells holding only
backticked paths". Register under attack: final `## Capabilities` section of
`SCORECARD.md@cedb0ec4f3a4f672804deac388b7191258f01fcd` (section opens line 1941; table rows
1956–1978). Closure record: fleet `MANIFEST.json@37b51a24` `.rounds[386]` (round=18, lane=mori,
verdict=admitted, commit=3786f3f1bde2fbcc5ce617e35e8c9becdbf9d9e8,
verification.spotcheck=corpus/lessons/round-18-verifier-spotcheck.md@b3602869dadd4016675aeba8db2adf3fa1e1b531),
fleet `.ufo/reports/round-18/mori.md@37b51a24`, lane closure commit `3786f3f1`.

## Row `rounds[386].capabilities_added[0]` — SCORECARD.md@cedb0ec4:1965

- Capability cell `retention gate`: non-empty; identical to MANIFEST
  `.rounds[386].capabilities_added[0]` name ("retention gate (tools/mori-retention-gate.py; …)").
- What cell: "Scans lane revisions under the retention policy and reports metric and routed counts;
  selftest 21/21; after-metric 0 and routed 0 at 3127c3a."
  - "Scans lane revisions under the retention policy": closure command is
    `scan --repo . --rev <rev> --policy .ufo/waves/round-18/frozen/c1-policy.json`
    (fleet report@37b51a24 line 44); every recorded run is a lane revision — d005cdd, 3127c3a,
    3786f3f (spotcheck@b3602869dadd lines 47–48).
  - "reports metric and routed counts": the tool emits `metric`/`routed` fields
    (blob@3786f3f1 lines 267–268, 293–294); the record carries exactly those counts (report line 45).
  - "selftest 21/21": MANIFEST capabilities_added[0]; report lines 21 and 49.
  - "after-metric 0 and routed 0 at 3127c3a": MANIFEST "C1 after metric 0, routed 0 at 3127c3a";
    report line 45; spotcheck lines 50–51 (`evidence/c1-after.json`, rev 3127c3a, metric 0, routed 0).
  - No fact beyond the record; bounds match (counts only, revision pinned).
- Evidence cell: single backticked path `tools/mori-retention-gate.py` — (b) met.

VERDICT: rounds[386].capabilities_added[0] supported

## Row `rounds[386].capabilities_added[1]` — SCORECARD.md@cedb0ec4:1966

- Capability cell `freeze-order check`: non-empty; matches MANIFEST `.capabilities_added[1]` name
  ("freeze-order check (tools/mori-freeze-order.py; …)").
- What cell: "Checks frozen claim inputs against implementation history and counts overclaims;
  selftest 12/12; overclaims 4 to 0 at 3127c3a."
  - "Checks frozen claim inputs against implementation history": the tool's own description is
    "measure frozen-input timing against implementation history" (blob@3786f3f1 line 583);
    `check` takes `--register`, `--corrections`, `--tip-for` (lines 588–592); overclaim/oracle
    totals at lines 275–294. Record command at report line 46.
  - "counts overclaims": `totals.overclaims` (blob lines 275, 294); record uses the term verbatim
    (report line 47, spotcheck lines 81–83).
  - "selftest 12/12": MANIFEST [1]; report lines 21, 49; blob prints `PASS %d/12` (line 576).
  - "overclaims 4 to 0 at 3127c3a": MANIFEST "overclaims 4->0 at 3127c3a"; report line 47
    ("overclaims 4 → overclaims 0"); spotcheck lines 81–83.
  - Caveat, not a defect under the rule: the spotcheck qualifies the flat 4→0 as "one historical
    correction plus three pre-build verifications" (spotcheck lines 91–94; routed defect 5 at
    lines 177–179). The register cell bounds the figure exactly as the MANIFEST string and the
    report do, so it is closure-faithful; the qualifier lives in the record's defect list.
- Evidence cell: single backticked path `tools/mori-freeze-order.py` — (b) met.

VERDICT: rounds[386].capabilities_added[1] supported

## Row `rounds[386].capabilities_added[2]` — SCORECARD.md@cedb0ec4:1967

- Capability cell `dispatch-attempt ledger verify`: non-empty; matches MANIFEST
  `.capabilities_added[2]` name.
- What cell: "Verifies that dispatch attempts bind their payloads: round-18 wave 1 1/1 and wave 2
  2/2 bound clean, residual 7/7 bound with STARTED_MISSING; selftest 14/14."
  - "Verifies that dispatch attempts bind their payloads": docstring "Bind and verify per-attempt
    dispatch payload identities" (blob@3786f3f1 line 2); `verify` recomputes committed dispatch
    payload identity and compares `payload_sha256`/`payload_bytes`/`tasks_count` to ledger rows
    (lines 200–240).
  - "w1 1/1 and w2 2/2 bound clean": MANIFEST "w1 1/1 and w2 2/2 bound clean"; report line 48
    (rc0); spotcheck lines 101–102 (`LEDGER_CLEAN`, exit 0).
  - "residual 7/7 bound with STARTED_MISSING": MANIFEST and report line 48 verbatim;
    spotcheck lines 103–104 (exit 1).
  - "selftest 14/14": MANIFEST [2]; report lines 21, 49; spotcheck line 105.
  - No fact beyond the record; failure shape (STARTED_MISSING) carried, not elided.
- Evidence cell: single backticked path `tools/mori-dispatch-ledger.py` — (b) met.

VERDICT: rounds[386].capabilities_added[2] supported

## Pointer relevance — (c), artifacts opened at closure commit 3786f3f1

- `tools/mori-retention-gate.py`@3786f3f1 (33,923 B, 762 lines, cat-file rc 0): implements the
  `scan` subcommand over a Git revision's tree/blobs with `--policy`, `--allowlist`,
  `--expect-population` (lines 310–324, 714–719); emits `metric`, `routed`, `RETENTION_CLEAN`;
  `--selftest` present (line 711; `selftest()` line 457). Implements THIS capability.
- `tools/mori-freeze-order.py`@3786f3f1 (23,388 B, 609 lines): `check` subcommand over
  `--register`/`--corrections`/`--tip-for` (lines 588–592) computing frozen-vs-implementation
  ordering, `overclaim`, `oracle_disagreement` (lines 246–294); `--selftest` reports PASS 12
  (line 576). Implements THIS capability.
- `tools/mori-dispatch-ledger.py`@3786f3f1 (23,729 B, 576 lines): `bind` and `verify` subcommands
  (lines 555–562); payload identity via SHA-256/bytes/tasks_count (lines 120–164); findings
  `STARTED_MISSING`, `LEGACY_ROW_UNBOUND`, `LEDGER_CLEAN` (lines 291, 308, 322). Implements THIS
  capability.

VERDICT: rounds[386].capabilities_added[0] pointer-relevance holds
VERDICT: rounds[386].capabilities_added[1] pointer-relevance holds
VERDICT: rounds[386].capabilities_added[2] pointer-relevance holds

## Residual risk and verification gaps

- The 4→0 overclaim figure is bounded exactly as the record bounds it; the spotcheck's "1
  historical + 3 prospective" qualification (routed defect 5) is inherited by the record, not
  introduced by the register — noted, no rule failure.
- Register preamble names "the artifact that round landed and the closure names" as the evidence
  contract (SCORECARD.md@cedb0ec4:1945–1946); the record names the three tools (MANIFEST
  capabilities_added strings; report line 21), so tool-path evidence cells fit the stated contract.
- Not run: the tools' `--selftest` arms and the C1/C2/C3 commands were not re-executed by this
  seat (fixture TMPDIR and counter bounds); row verdicts rest on the committed record text and
  blob inspection at the pinned revisions, all quoted above. Unrun checks are not passes.
- Cosmetic, inside artifact, out of row scope: `mori-freeze-order.py` failure branches print
  `FAIL 0/11` (lines 404, 411, 417) while the pass total is 12 — message inconsistency only.
- Method note: no `lsp` device is exposed to this seat; all caller/artifact checks were done by
  `git cat-file` at the pinned revisions plus content grep on the extracted blobs — recorded as
  the literal fallback it is.
- Tool installs: none.
