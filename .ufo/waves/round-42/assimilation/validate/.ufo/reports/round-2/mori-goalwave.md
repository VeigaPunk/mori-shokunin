# mori round 2 — goal-wave delivery report

Status: **ADMITTED** (round 2; the blocked-attempt report `mori.md` in this
directory remains the prior record, untouched — blob `0387b6f7…`).
Lane baseline entering the wave: `e30b2e3` · wave: one batched 13-seat flash
AgentSwarm call (12 completed, 1 seat lost to a provider content-inspection
400 — no lane artifact affected) · report time: 2026-10-15 ~16:05Z.
Integration: parent (L1) — acceptance re-run, defect fixes, commit under the
mori lane identity. No push: the lane repo has no remote configured.

## Work performed

- Selected axis **coverage** (lower owned LIVE axis per the SCORECARD round-2
  blocked section) and declared the falsifiable claim (before → after) recorded
  in the SCORECARD verdict section.
- Diagnosed the quarantined oracle candidate `tools/mori-silence-cases.sh`
  (sha `61db3df3…`): `gc()` chained `commit --allow-empty -am || add && commit`,
  which bash binds as `(A||B)&&C`; on a fresh repo A succeeds as an **empty
  root commit**, the add is skipped, the trailing commit fails — exit 1 before
  case 1, no tally. Reproduced independently by three seats; minimal repros
  receipts in seat reports.
- Reconciled the three named debts: deterministic stage-then-commit `gc` with
  `die` → exit 2 (`505a7504…`); fixtures bound to the **live** watchdog-log
  grammar (`pid=`/`runId=`/`mission=` tails exercised) instead of the synthetic
  `TIMESTAMP … ts=` ledger; fixtures use the live report path
  `.ufo/reports/round-<N>/<lane>.md`.
- Landed the coverage artifacts (below); parent acceptance re-ran every load
 -bearing command instead of quoting the seats.

## Landed changes

- `tools/mori-silence-cases.sh` → revision `505a7504…` (sha256
  `505a7504811401b13fd96f8925605e744fbb54970c8ac65ac331b053d647e580`).
- `corpus/knowledge/observability-surfaces-r2.md` — seven per-surface notes
  (watchdog, waves, journal, cgroup, disk, silence, tmux) + six measured census
  defects at path:line; supersedes the "six surfaces" framing.
- `corpus/knowledge/silence-grading-r2.md` — launch-aware, authorship-aware
  decision table; every rule `proven` (pointer) or `proposed` (precondition);
  named admission checklist (integration-fixed: identity recipe `>`, tail
  arithmetic, revision-scope annotation).
- `corpus/knowledge/progressing-weak-r2.md` — authorship discrimination proof:
  extractable 10-case check, `MORI_AUTHORSHIP_CHECK: matched=10 total=10`
  exit 0; production admission explicitly deferred with preconditions.
- `corpus/evidence/watch-r2-20261015T152746Z.log`, `…152855Z.log`,
  `…153003Z.log` + `corpus/evidence/README.md` — three dated live-census
  receipts, hash-pinned, re-runnable, method stated (sampling; no watch mode).
- `corpus/knowledge/lane-silence-r2.md` (precursor candidate, integrated with
  the byte-defective recipe fixed), `corpus/lessons/2026-10-15-oracle-honesty-crash-masking.md`,
  `corpus/README.md` (coverage rows + six→seven surfaces + gaps update),
  SCORECARD round-2 verdict section, this report.

## Before → after measurements (parent acceptance, 2026-10-15T16:0xZ)

| Command | Before | After | Exit |
|---|---|---|---|
| `bash tools/mori-silence-cases.sh` | exit 1 in fixture setup, 0.012 s, no tally (`61db3df3…`) | `MORI_SILENCE_CASES: matched=10 total=27`, deterministic reruns | 1 |
| `bash tools/mori-census.sh --selftest` | `PASS (14 cases, 14 passed, 0 failed)` | unchanged — census untouched (`e3073a2b…`) | 0 |
| Authorship check (extract sha `9c91e0a0…`) | `progressing-weak` deferred, no runnable proof | `MORI_AUTHORSHIP_CHECK: matched=10 total=10` | 0 |
| Watch receipts | none | 3 dated, hash-pinned, indexed | — |

Tally semantics: 10/27 is the **honest, pre-registered** gradient against the
still-r1 census — 16 FAILs are the r2 contract gap (launch/closure/authorship
semantics the r1 census cannot satisfy), 1 FAIL (`unreadable-git-unavailable`)
is a measured r1 defect: `tools/mori-census.sh:517` assigns a
`find … | sort | tail | cut` pipeline under `set -euo pipefail`; an unreadable
lane `.git` makes `find` return 1 and the census aborts after its header — no
`MORI_CENSUS` verdict. Minimal repro recorded by three seats. Anti-weakening
evidence: the falsifier's crash-masked variant and a genuine repair produce the
identical tally (lesson landed), so the wave also pre-registered the gradient,
ran mutant censuses (no-op → `matched=1`; all-zero → `matched=4`; mutator →
`readonly-no-mutation` caught), and the shipped `assert_case` table was verified
byte-identical to the pre-registered registry.

## SHONEN

- [ ] SKILL.md decision tables/error patterns with cited sources — r1 tables
  exist; verification owed (no named non-author verifier yet).
- [ ] End-to-end domain task executed and logged — r1 census + r2 oracle land;
  verification owed.
- [ ] Instructions executable by an agent without oral context — verification owed.
- [ ] No cross-domain bleed (PROVINCE.md still accurate) — scope-sentinel
  evidence this round; verification owed.

All four remain unchecked by rule: the wave's seats are the lane
(`PROTOCOL.md`: a dispatched subagent is still the lane), so no box is self-attested.

## Cross-domain evidence and named debt (carried to round 3)

1. **r2 census cutover** — land r2 `probe_silence` in `tools/mori-census.sh`
   per `silence-grading-r2.md`'s output contract; passing tally
   `matched=N total=M, N=M` registered as the falsifiable claim
   (`progressing-weak-r2.md` claim block).
2. **Census crash defect** — `:517` (and the same construct at `:283`,
   `probe_waves`): unreadable subtrees abort the census instead of grading
   `unavailable`. Fix with selftest coverage.
3. **Other census defects measured (report-only)** — unreachable
   `WATCHDOG_LOG_UNAVAILABLE` (`:198-200`); pgrep substring false positive
   (`:190-194`); cgroup local/service counter invisibility (`:399-404`,
   `:421-428`); count-only `state_rounds` (`:220`). Detection/report only —
   fixes land as their own rounds if selected.
4. **Framing debt retired** — six→seven surfaces recorded in `corpus/README.md`.
5. **Receipt-identity debt unchanged** — no lane remote, no Sightings; the
   round's proof remains protocol artifacts (this report, SCORECARD, LOG).

Boundaries held: detection and report only; no kill/pkill/systemctl/config
edits; fixtures under `/tmp` only; no seat commits; blocked attempt's report,
SCORECARD history and LOG history untouched except append-only entries.
