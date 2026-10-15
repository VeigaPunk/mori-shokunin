# Round 10 verdict — integration draft (scribe seat, goal wave)

Integration target: append as a `## Round 10 verdict — 2026-10-15 (goal wave)` section in
`SCORECARD.md` (parent-owned; append-only — the round-9 section `SCORECARD.md:439-478` and
everything above it stay untouched). Verdict vocabulary only (`improved` / `harmed` /
`unchanged` / `unprovable-but-better`); no scalar scores. Every figure below is bound to a
landed artifact, a receipt, or a command run at a pinned SHA; `[PARENT: …]` marks values only
the integration commit or the parent's acceptance re-run can bind; `[PENDING: …]` marks values
unlanded at this draft's clock (v1.2, 2026-10-15T22:37Z).

- Evidence commit: `[PARENT: wave integration commit hash under the mori identity]`
- Lane baseline entering the wave: `6a549b9` (round-9 records; evidence `cffb37e`).
- Round-count claim: `[PARENT: verified-round accounting 9 → 10 on admission]`
- Before-side: first-hand at census
  `1c49238a7fd87277151ff5776acfb4d62fadd9d69764a02f0ede03ef0d3902d2`
  (`VERSION=census-r5`, 2394 lines) / oracle
  `448f77238c73a5c929a898dad0f0c495fd2a66cc4b90a00ae84ede69a86beeb5`, 21:50–21:55Z.
- After-side: census `d7710981aa1c7571ff9d6fd7f75822811173010e5f4e298ac3c47fab274a0b20`
  (2833 lines; `git diff --numstat` 475+/36−; settled 22:12:09Z, stable through the
  after-side battery); oracle `448f7723…` **byte-frozen** (sha re-checked before/after);
  lane baseline `corpus/evidence/baseline-r10-20261015T2231Z.json` sha `0993b235…`
  (pinned at the settled bytes; the interim pre-settlement pin `bdf46496…` was consolidated
  into it mid-battery). Scratch `/tmp/mori-scribe-r10/`.

## Round 10 verdict

Round scope: the freshness item carried since round 2 and registered by the round-9 verdict
(`SCORECARD.md:475-478`: "the long-carried **drift pin** (freshness) — a committed behavioral
baseline plus a `--drift` mode with a declared volatile-fields list, so census behavioral
drift is itself detected"). Entering state, first-hand: `--pin` and `--drift` both rejected
(`mori-census: unknown argument: --pin`, exit 2), and `ls corpus/evidence/ | grep -i
'baseline\|pin'` → `NONE`.

Registered claim (round brief): after — (1) `--pin <path>` writes a normalized full-output
baseline with an explicit VOLATILE-field contract (time/age/counter fields masked); (2)
`--drift <path>` reports `MORI_DRIFT: none` (exit 0) or names the changed non-volatile fields
(exit 1); baseline-missing → exit 2; (3) the LANE commits its own live baseline under
`corpus/evidence/` with a re-run recipe; (4) default census output byte-unchanged (oracle
28/28, wants unchanged); (5) selftest covers pin→drift-clean, injected-regression detection
(names the field), volatile churn staying clean, and missing-baseline exit 2.

**Before** (entering bytes; first-hand):

- No capability: both flags exit 2 as unknown arguments; no baseline artifact exists.
- Live census `MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)` exit 1,
  stderr 0 B; per-surface key sets captured as the default-output reference.
- The lessons-distiller's landed lesson quantified why a naive baseline cannot work:
  a live census pair 72 s apart differs on 32 of 33 lines; 6 of 79 field tokens churned;
  a pinned fixture is byte-identical (churn is host inputs, not gate nondeterminism).

**After** (census `d7710981…`; oracle `448f7723…` byte-frozen; all first-hand):

- **The mechanism** (landed in ten visible revisions 21:57–22:12Z; the two structurally
  significant: `1ddb7ff8…` the whole mechanism, `d7710981…` +14 lines adding the
  baseline-volatile-list comparison). `--pin` runs the census read-only, masks the declared
  volatile fields (`ts`, `age_s`, `mtime_age_s`, `*_epoch`, `mem_peak_anchor`, PSI gauges,
  `io_avg_since_boot` with the device name kept, `state_val_unread_reasons`, `script_sha256`,
  `example`, plus the `DRIFT_COUNTER_KEYS` class), and writes the baseline with a header
  recording `census_sha256`, `pinned_ts` and the `volatile_fields` list verbatim; the pin's
  exit is 0 whatever the census's own roll is; write failure → exit 2. `--drift` re-runs,
  re-normalizes with the current list and compares: equal → `MORI_DRIFT: none` exit 0;
  different → exit 1 naming changed keys, `-key`/`+key`, `-FINDING:<id>`/`+FINDING:<id>`,
  `output-order`, or `volatile_fields`; missing/unreadable/malformed → exit 2 (65 ms, no
  census run).
- **Scope proof (default path untouched):** no diff hunk touches old lines 299–1568 — the
  `emit_*` helpers, all probe functions and the `run_census` body are byte-identical; the
  deletions are confined to the usage text, the selftest runner and `main()`. Behaviorally:
  oracle `matched=28 total=28` exit 0 (28 `^PASS ` lines) at the settled bytes with the oracle
  file byte-frozen; default live output's per-surface key sets identical to the entering
  capture; and the strongest live check: the entering r9 bytes' live capture (21:50Z) and the
  settled bytes' live capture (22:17:57Z) are **identical after applying the shipped
  normalization** (raw diff 64 changed lines → masked diff empty) — the volatile contract
  absorbs 27 minutes of live churn and the revisions produce the same canonical output.
- **Claim legs, first-hand at the settled bytes** (verbatim in
  `.ufo/round-10/goal-wave/measurements-ledger.md`): pin→drift `none` (32 s); churn drift
  ~4 min later `none` (55 s); injected one-field regression (Disk warn 85→84) → `MORI_DRIFT:
  warn_pct` exit 1; renamed finding id → `MORI_DRIFT:
  +FINDING:KILL_SIGNAL_JOURNAL_X -FINDING:KILL_SIGNAL_JOURNAL` exit 1; rewritten volatile
  list → `MORI_DRIFT: volatile_fields` exit 1; missing baseline → exit 2 (65 ms); malformed
  variants → exit 2; `--pin` write failure → exit 2; flags without path → exit 2.
- **The lane baseline:** `corpus/evidence/baseline-r10-20261015T2231Z.json` (6779 B, 39
  lines; sha `0993b235…`; header `census_sha256=d7710981…`, `pinned_ts=2026-10-15T22:26:29Z`)
  — pinned **at the settled bytes**; my independent `--drift` against it → `MORI_DRIFT: none`
  exit 0 (32 s). An interim pin (`…T2210Z.json`, sha `bdf46496…`, pinned at the
  pre-settlement `1ddb7ff8…`) also read `none` from the settled bytes (mine, 39 s, 22:20Z,
  reproducing the note-writer's 22:12Z reading) — that is the cross-revision
  behavioral-stability datum; the interim file was consolidated into the 2231Z baseline at
  ~22:26:58Z, which is the reference going forward. Both are `mori-drift-baseline v1` text
  format despite the `.json` suffix. Re-run recipe: note `corpus/knowledge/drift-pin-r10.md`
  §4 (`[PENDING: the r10 `corpus/evidence/README.md` index section]`).
- **Selftest:** `PASS (66 cases, 66 passed, 0 failed)` exit 0 ×2, stderr 0 B, the two output
  files byte-identical — 56 → 66 (+10 r10 pin/drift arms, `:2722-2798`: pin writes baseline;
  baseline records the volatile contract; pin→drift clean; volatile churn stays clean;
  one-field regression names the field; removed finding named; missing baseline exit 2;
  changed volatile contract reported; `--pin`/`--drift` arity exit 2).

| axis | verdict | before → after evidence |
|---|---|---|
| freshness | **improved** *(selected axis)* | Before: no baseline existed; behavioral regressions in future census edits were catchable only by seat discipline (rounds 2–9). After: the capability + a committed live baseline at the settled bytes (`0993b235…`, re-run recipe in note §4) reading `MORI_DRIFT: none`, plus the cross-revision reading (a pre-settlement pin also read `none` from the settled bytes) and an admission ritual recorded (pin on admit / drift first / re-pin as a recorded act with a reason). One carried freshness item closed. |
| operability | **improved** | Two new modes with a three-value exit contract (0 none / 1 named drift / 2 cannot-compare); error paths measured at 65 ms with diagnostics and no census run; 10 new selftest arms (56 → 66) with the two runs byte-identical; `--drift` writes nothing; no stray writes in the lane after ~14 census-equivalent runs. Direction of safety: false red preferred to false green (a drift report is a named artifact). |
| coverage | **unchanged** | No new domain surface; the live schema's key set and finding multiset are identical to the entering capture. The pin is coverage-of-self, not of the fleet: it compares the census's own output. |
| depth | **improved** | `corpus/knowledge/drift-pin-r10.md`: contract, the measured churn rationale (three seats' windows), the over-mask blind spots in priority order (counter magnitudes first), the under-mask env caveat, mask-shape experiments (key-scoped vs digit-blanking), and the admission ritual; lesson `corpus/lessons/2026-10-15-volatile-contract-behavioral-baselines.md`; `corpus/README.md` r10 rows. |
| calibration | **improved narrowly** | The volatile set is measured, not guessed (three independent same-env holdout pairs normalize clean); the blind spot is demonstrated rather than declared (my `count=1→5` mutant returns `none` while a finding rename is caught); the env caveat and the "revision ≠ behavior" boundary are stated; thresholds stay labeled local. |
| adjacency | **unchanged** | Detection/report only; oracle byte-frozen (sha re-checked); no remediation/kill/config content; `--pin` writes exactly the named path and `--drift` nothing; fixtures and baselines written by this seat live only under `/tmp`. |

Admission: `[PARENT: bind the admission and round-count at integration. Expected disposition
on the evidence above: **ADMIT** — the claim's five legs are receipt-backed and reproduced
first-hand, the default path is byte-unchanged by code scope and by live masked-identity, the
oracle is byte-frozen and green, the lane baseline is committed at the settled bytes and reads
`none`, and the selftest carries every required arm. The honest boundaries to carry: the
counter-magnitude blind spot (demonstrated), the env-not-recorded caveat, the mid-wave
revision history (ten revisions; battery binds `d7710981…`), and the `SKILL.md:75` "65 cases"
staleness (settled is 66 — a named defect for its owner, not a claim.)]`
No scalar score.

Learning trends (lane idiom):

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | **improved** | Note `corpus/knowledge/drift-pin-r10.md` + lesson `corpus/lessons/2026-10-15-volatile-contract-behavioral-baselines.md` landed; `corpus/README.md` r10 rows landed (correct settled numbers); `SKILL.md` r10 row landed (`[DEFECT: SKILL.md:75 says "56 → 65 cases"; settled is 66 — stale against `d7710981…`]`); `[PENDING: corpus/evidence/README.md r10 section]`. |
| quality | **improved** | Three seats' independent drift readings agree (note-writer 22:12Z; mine 22:20Z against the interim pin and 22:31Z against the current baseline — both `none`); the mask's detection and its blind spot are both measured with mutants instead of asserted; the revision progression was tracked by a 20 s poller and the battery binds the settled SHA. |
| discernment | **unchanged** | No outside spot-check of an admit/reject exists — the wave's seats are the lane per protocol. `[PARENT: bind]` |

Named debt for round 11:

1. **Counter-magnitude blind spot** (`drift-pin-r10.md` §3.1, demonstrated by my mutant):
   a `count=`/`size=`/`rowb_files=` magnitude change behind an existing finding id reads
   `none`; ≈47% of the schema sits in the counter class. Options: a shape check on known
   counter ranges, or a severity/count-aware second pass — a round-sized decision.
2. **Env not recorded in the baseline** (§3.2): pin and drift must share the invocation;
   a `MORI_*` override difference reports as drift. Recipe-level today; could be recorded.
3. **Adoption:** run `--drift <lane baseline>` as the first measurement of each round
   (ritual §5), against the settled-bytes baseline `baseline-r10-20261015T2231Z.json`, and
   re-pin only as a recorded act with a reason.
4. Carried: production `:1322` same-class SIGPIPE site (needs a production-touching round +
   oracle re-verification); tmux per-session freshness live-proof (no tmux server); the
   instantaneous disk-rate deferral (measured grounds); row-6 report-body presence-only
   residual; the blocked-attempt receipt-binding and role-routing debts
   (`SCORECARD.md:128-131`); memory thresholds remain labeled local; an admission-time
   determinism gate.

`[PARENT: bind the integration commit and round-count; re-run `bash tools/mori-census.sh
--selftest` (expect `PASS (66 cases, 66 passed, 0 failed)` exit 0), `bash
tools/mori-silence-cases.sh` (expect `matched=28 total=28` exit 0; oracle sha must equal
`448f7723…`), `bash tools/mori-census.sh --drift
corpus/evidence/baseline-r10-20261015T2231Z.json` (expect `MORI_DRIFT: none` exit 0 at the
final bytes; if red, name the aged fields and re-pin as a recorded act with a reason — do not
re-pin to silence), and the live census. If the final census SHA moved past `d7710981…`,
re-run the battery's first legs (pin → drift → one mutant) at the final bytes.]`