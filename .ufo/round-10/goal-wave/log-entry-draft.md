# Round 10 log-entry draft (scribe seat, goal wave)

Integration target: append as a `## Round 10 — … (goal wave)` entry at the end of `LOG.md`
(parent-owned; append-only — nothing above the new section changes). `[PARENT: …]` marks what
only the integration commit/acceptance can bind; `[PENDING: …]` marks values unlanded at this
draft's clock (v1.2, 2026-10-15T22:35Z).

---

## Round 10 — drift pin: the census's own behavioral baseline + `--drift` (goal wave)

**Round 10 — goal-wave admission (2026-10-15).** Motivating evidence: the freshness item
carried since round 2 and registered by the round-9 verdict (`SCORECARD.md:475-478`).
Entering bytes: census `1c49238a…` (r9, 2394 lines), oracle `448f7723…` (byte-frozen this
round; wants unchanged). Before, first-hand: `--pin` and `--drift` both exit 2 as unknown
arguments, and no baseline artifact exists under `corpus/evidence/` — behavioral regressions
in future census edits were catchable only by seat discipline.

Landed (evidence commit `[PARENT]`): `tools/mori-census.sh` → `d7710981…` (2833 lines;
`git diff --numstat` 475+/36−; `VERSION` stays `census-r5`, distinguished by SHA), written in
ten visible revisions 21:57–22:12Z (the mechanism at `1ddb7ff8…`; `d7710981…` adds the
baseline-volatile-list comparison + one selftest arm). No diff hunk touches old lines
299–1568 — the `emit_*` helpers, all probe functions and the `run_census` body are
byte-identical; deletions are confined to the usage text, the selftest runner and `main()`.
`--pin <path>` runs the live census read-only, normalizes the full output (one `sed` pass over
a captured variable — no live pipes), and writes a `mori-drift-baseline v1` file whose header
records `census_sha256`, `pinned_ts` and the `volatile_fields` list verbatim; the pin exits 0
whatever the census's own roll is (a DRIFT host still pins); write failure → exit 2.
`--drift <path>` re-runs, re-normalizes with the current list, and compares: equal →
`MORI_DRIFT: none` exit 0; changed non-volatile fields are named — changed keys, `-key`/`+key`,
`-FINDING:<id>`/`+FINDING:<id>`, `output-order`, `volatile_fields` (a baseline pinned under a
different masked set) — exit 1; missing/unreadable/malformed → exit 2 in ~65 ms with no census
run. `--drift` writes nothing.

**Scribe battery, first-hand at the settled bytes `d7710981…`** (the one pin taken at
`1ddb7ff8…` is labelled): `--pin` → `MORI_PIN: ok` exit 0 (32 s; baseline 6779 B, 39 lines);
`--drift` same-revision → `MORI_DRIFT: none` exit 0 (32 s); churn ~4 min later, cross-revision
→ `none` (55 s); injected one-field regression (`DISK_WARN_PCT` 85→84) → `MORI_DRIFT: warn_pct`
exit 1; renamed finding id → `MORI_DRIFT: +FINDING:KILL_SIGNAL_JOURNAL_X
-FINDING:KILL_SIGNAL_JOURNAL` exit 1; rewritten `volatile_fields` → `MORI_DRIFT:
volatile_fields` exit 1; missing baseline → exit 2 (65 ms); malformed variants (marker
absent / volatile contract absent / empty block) → exit 2; `--pin` write failure → exit 2;
flags without a path → exit 2. Default-path invariance: oracle `matched=28 total=28` exit 0
(28 `^PASS ` lines; oracle sha before=after) at the settled bytes; default live
`MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)` exit 1 with per-surface
key sets identical to the entering capture; and the entering r9 live capture (21:50Z) vs the
settled live capture (22:17:57Z) are **identical after the shipped normalization** (raw diff 64
changed lines → masked diff empty). selftest `PASS (66 cases, 66 passed, 0 failed)` exit 0 ×2
(the two output files byte-identical; 56 → 66 with the 10 r10 pin/drift arms at `:2722-2798`).

**The lane baseline** (receipts-writer): `corpus/evidence/baseline-r10-20261015T2231Z.json`
(sha `0993b235…`; 6779 B, 39 lines; header `census_sha256=d7710981…` — pinned **at the settled
bytes**, `pinned_ts=2026-10-15T22:26:29Z`), reading `MORI_DRIFT: none` exit 0 (mine, 32 s).
An interim pin at the pre-settlement bytes (`…T2210Z.json`, `1ddb7ff8…`) also read `none`
from the settled bytes (mine, 39 s; the note-writer's 22:12Z reading agrees) — that is the
cross-revision behavioral-stability datum; the interim file was consolidated into the
2231Z baseline before this clock, which is the reference for future rounds. Both are the
`mori-drift-baseline v1` text format despite the `.json` suffix. Note
`corpus/knowledge/drift-pin-r10.md` (contract, measured churn rationale, over/under-mask
risks, the re-run recipe §4, the admission ritual); lesson
`corpus/lessons/2026-10-15-volatile-contract-behavioral-baselines.md` (why a raw baseline
cannot be stable, why line-level masking is vacuous, the counter-class blind spot);
`corpus/README.md` r10 rows; `SKILL.md` r10 row (`[DEFECT: `SKILL.md:75` says "56 → 65
cases"; the settled file is 66 — stale against the final revision]`);
`[PENDING: corpus/evidence/README.md r10 section]`.

**Verdicts.** `[PARENT: bind — expected ADMIT on the evidence above; no scalar score.]` Read:
freshness **improved** (the carried item closed: a committed baseline at the settled bytes
reading `none`, plus the cross-revision reading, with an admission ritual), operability
**improved** (two modes, three-value exit contract, 10 new selftest arms, 66/66 ×2
deterministic), coverage **unchanged** (no new domain surface; key set and finding multiset
identical), depth **improved** (note + lesson + README/SKILL rows), calibration **improved
narrowly** (measured churn set with holdout pairs; the blind spot and its bound demonstrated
with mutants), adjacency **unchanged** (detection/report only; oracle byte-frozen; no
remediation). No scalar score.

**Honest boundaries carried:** counter magnitudes inside an existing finding id read `none`
by construction (demonstrated: a `count=1→5` mutant returned `none` while a finding rename
was caught; ≈47% of the schema is in the counter class); the baseline records no `MORI_*`
env, so pin and drift must share the invocation; the mid-wave revision history (ten
revisions; the battery binds `d7710981…`). Named debt for round 11: the counter-magnitude
blind spot, env recording, per-round drift adoption — plus the carried `:1322` production
SIGPIPE site, tmux freshness live-proof, instantaneous disk-rate deferral, row-6 residual,
receipt-binding/role-routing debts, labeled-local memory thresholds, and an admission-time
determinism gate.

**Boundaries held.** Detection/report only; no remediation/kills/config edits; oracle
byte-frozen; `--pin` wrote exactly the named `/tmp` paths and `--drift` nothing; fixtures and
baselines of this seat under `/tmp`; seats committed nothing; parent integrates under the
mori identity. `[PARENT: confirm from the integration diff]`

Round report: `[PARENT: .ufo/reports/round-10/mori-goalwave.md]` · Verified lane rounds:
`[PARENT: 9 → 10]`.