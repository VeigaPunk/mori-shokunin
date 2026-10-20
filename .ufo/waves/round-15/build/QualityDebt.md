# QualityDebt — round-15 admission criteria for C1 coverage

Seat: `MoriR15.QualityDebt` (executor, leaf). Axes: **coverage** (judged) — retain validated
positive OOM/signal evidence without fabricated totals; **operability** (protected) — raw
tokens and unavailable semantics unchanged.

Timestamp: `2026-10-20T07:37:07Z`. No gate, test, build, formatter, or smoke run was executed
by this seat; nothing here is a measured behavioral result. No installs or upgrades; no
credential, auth, or `~/.omp/agent/agent.db*` access; no separate omp process; no commits.

## Files changed

| Path | Change |
|---|---|
| `corpus/QUALITY.md` | Appended `## Criteria added round 15` with Q33–Q36. Criteria 1–32 untouched (append-only). File is 92 lines, sha256 `e3f14e8c323e581940f63b738c20fb102d9d36542370d02ca130d32ffca446e8` (prefix `e3f14e8c`) after the edit. |
| `.ufo/waves/round-15/build/QualityDebt.md` | This report only. |

No source, gate, fixture, verifier, aggregator, MANIFEST, SHONEN, skill, or sibling report was
edited; the only corpus edit is `QUALITY.md`.

## What was appended (4 criteria, each falsifiable)

- **Q33 (M1, dirty-path provenance).** A receipt's provenance is exact input identity/content,
  not `dirty` or a porcelain line: porcelain carries status+path, never content, so an edit to
  an already-dirty input leaves the line byte-identical while a scope-only delta says
  `moving:false`. Required: hash each declared input at load and end, record observed
  `rev-parse HEAD` rather than an asserted pin, and say `moving:false` only when scope and all
  input digests are equal; otherwise the run is a working-tree observation, not committed bytes.
- **Q34 (M2, class-count vs record wording).** Raw class tokens count records that survived the
  aggregate validation (or are `unavailable:<reason>`); positive tokens count only records
  individually satisfying the typed predicate; neither is a kill/victim/event/completeness
  total. A positive 0 is a record count, never a no-event/health claim; positives are not
  renamed into raw tokens, summed across scopes, or treated as class totals.
- **Q35 (M2/M3, independent known-positive witness).** One mixed case per alarm path: a valid
  scalar current-boot record (exact `MESSAGE_ID` plus exact `UNIT_RESULT`/`EXIT_CODE`/
  `EXIT_STATUS`) beside a malformed/nonmatching/foreign-boot record must yield raw tokens
  `unavailable:<reason>` (never 0), positive integer ≥1, exactly one crit OOM line for that OOM
  witness or one user warn line for that signal witness; red on frozen pre-fix bytes, green on
  delivered bytes. No inference from an unavailable aggregate, `MESSAGE`, a second journal
  query, a failed scalar guard, or subject metadata; a capture with no valid positive must not
  fire.
- **Q36 (M3, fixture vector labelling).** A nonzero positive vector names its source: fixture
  case/pack vs live boot/scope/window/receipt. A fixture vector is never live positive load, a
  class total, or census completeness.

## Falsifiers / red-state linkage (not executed)

- **Q35 is the criterion the planned r15 regression gate can encode as red/green**: the frozen
  pre-fix census must fail the mixed valid+invalid case before integration; the delivered
  census must fire the expected one line with raw unavailable and positive ≥1. If the frozen
  case does not fail, or the positive token is missing/0, the claim is red or rejected.
  `tools/mori-round15-regressions.py` did not exist at observation, so this is a required gate
  shape, not a run result.
- **Q34 fails on an inspectable row**: any finding/surface that prints a positive value under a
  raw token, sums user+system, or reads positive 0 as no-event/health.
- **Q33 fails on a receipt**: `moving:false` with an already-dirty input whose content changed.
  AttackProvenance CE1 observed exactly this live this wave.
- **Q36 fails on wording**: a fixture vector cited as live load or as a total.

## Retained evidence (read-only observations)

| Anchor | Observed |
|---|---|
| `corpus/lessons/round-15.md:19` (M1) | “Retain start/end porcelain path scope in new receipts and hash verdict-driving inputs; freeze committed input before measurement. This does not reconstruct unknown historical dirty paths.” |
| `corpus/lessons/round-15.md:20` (M2) | “The r14 phrase “fail-loud on positive validated records” meant positive validated **class counts**, not every record; mixed invalid records could suppress otherwise valid positives. … The r15 frozen-red comparison must fail that suppression case before repair counts.” |
| `corpus/lessons/round-15.md:21` (M3) | “Legacy KILL_SIGNAL `count`/`process_sigkill` can be `unavailable:<reason>` while an independently available user-unit signal arm raises WARN. Neither unavailable nor the distinct unit-signal count is a fabricated process zero.” |
| `corpus/lessons/round-15.md:23-25` | “The prior raw nonzero vectors in SCORECARD.md round-14 (`3/0/2/1/2/1` user and `2/1/4/3/0/2` system) are **fixture vectors**, not live positive load.” |
| `corpus/lessons/round-14-verifier-spotcheck.md:83` | “Exact contemporary porcelain was not retained; untracked output receipts are a supported explanation, not a proved complete dirty-path list.” |
| `.ufo/waves/round-15/build/AttackProvenance.md` CE1 | “The status line stayed byte-identical the whole time.” A content edit to an already-dirty harness input still yields `moving:false` under a scope-only comparison. |
| `tools/mori-census.sh:969-990` | Positive interface block: four scope-local tokens, `unavailable:<reason>` on capture/stderr/parse failure, “a parsed stream with no individually valid record is a real 0 for the positive token (it is NOT a class total)”, alarm/fields/non-claims. |
| `tools/mori-census.sh:981-984` | “real 0 for the positive token (it is NOT a class total)”; “OOM_KILL_JOURNAL fires once if ANY positive_kernel_oom or positive_unit_oom is > 0, even while the matching raw counter is `unavailable:<reason>`.” |
| `tools/mori-census.sh:1033-1036` | Per-record positive predicates: object, scalar string `_BOOT_ID == $boot`, scalar string `MESSAGE_ID == $id`; unit exact `oom-kill`/`signal`; process exact `killed` + scalar string/number `9`. |
| `tools/mori-census.sh:1109-1131` | `journal_positive_scan` over the same captured `$raw`, no second journalctl; empty `JQ_POS_VEC` means positives unavailable, never 0-by-default. |

## In-flight worktree observations (not verdicts)

- `tools/mori-census.sh` was being edited concurrently during this seat's read. Positive
  predicates and scan exist, but the alarm wiring observed at `:1420-1433` (OOM) and
  `:1450-1455` (KILL) still gates only on raw `ko`/`uo`/`ps`/`us`, and the finding lines at
  `:1435`/`:1457` did not yet carry positive fields. Line numbers may move under the concurrent
  writer; anchor by symbol/quote as well as line.
- `tools/mori-round15-regressions.py` was absent at observation; the fixture directory contained
  at least `KernelSystem.json` (4 cases, unique ids) but no pack was validated or executed here.
- `tools/mori-round14-regressions.py` still hashes `__file__` at emit time only
  (`:2432-2434`); no `sha256_loaded`/start-end input digest was found by grep. Therefore the
  current harness does **not** yet meet Q33's content-identity bar, even though it records
  start/end porcelain and a delta (`capture_revision`, `revision_delta`). This is routed, not
  repaired here.

## Risks / blockers

1. **Q33 is currently unmet by the r14 harness as observed.** If L1 cites the r15 receipt as
   committed-byte provenance, an already-dirty input can change between load and emit without
   moving the porcelain line. ProvenanceCapture/HarnessBuild must add load/end content digests
   (including the importlib-loaded r14 module and every fixture pack), or Q33 must reject that
   reading. Not a blocker to appending the criterion; a blocker to claiming it satisfied.
2. **Q34/Q35/Q36 are admission rules, not measured behavior.** No gate was run; the red/green
   mixed case remains L1's post-integration measurement. Positive fields observed in comments
   and predicates are not evidence that the alarm wiring is complete.
3. **Concurrent line drift.** `tools/mori-census.sh` grew from 3842 to 3900+ lines during this
   wave; exact anchors above are the observation point, not a frozen pin.
4. **Fixture coverage unknown.** Only one pack was observed; no id uniqueness or expected-literal
   sweep was performed by this seat.

## Non-actions

No commits, pushes, deployments, installs, service restarts, or external-state remediation.
No verification commands run. The only writes are `corpus/QUALITY.md` and this report.
