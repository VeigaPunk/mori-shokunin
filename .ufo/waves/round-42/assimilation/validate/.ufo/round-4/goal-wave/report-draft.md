# mori round 4 — goal-wave report draft (scribe seat)

Integration target: the round report (idiom of `.ufo/reports/round-3/mori-goalwave.md`;
final path `[PARENT]`, likely `.ufo/reports/round-4/mori-goalwave.md`). Parent owns the
final path, the identity and the commit binding. Every figure is bound to a landed artifact
or a cited path/receipt; `[PARENT: …]` marks what only the integration commit, the
acceptance re-run, or another seat's ownership can bind.

- Status: `[PARENT: completion statement + verified-round-count claim 3 → 4]`
- Evidence commit: `[PARENT: wave integration commit hash under the mori identity]`
- Lane baseline entering the wave: `bbcc1ad` (round-3 records; `1439c47` evidence)
- Report time: `[PARENT]`
- Draft status: **v3 2026-10-15T17:56Z** by the scribe seat — after-side bound to oracle
  `be0e28b8…` / census `af2d4e79…`, the receipts
  `corpus/evidence/verdict-r4-20261015T173551Z-{selftest,oracle,canary227,sniffer-v2,live}.log`,
  and the verdict note `corpus/knowledge/verdict-machine-r4.md` (sha
  `aab4b62c35e4b01606bda9b10877cc7ce7122ac3c21c589e16cf2dedaf58e28e`). v3 carries the
  note's §2.4 residual (self-consistent order-replay still fakes a pass); v1/v2 predated
  the note and are superseded.

## Work performed

- Selected axis **operability** — make the verdict machine trustworthy end-to-end: the
  round-3 registered debt (`SCORECARD.md:185-191`) — (a) frozen-oracle matcher fix,
  (b) oracle anti-sniff hardening (opaque per-case dirs, drop `MORI_FIXTURE`, add a
  shape-invariance case), (c) census `:227` `state_n` pipefail hardening, (d) per-anchor
  close tracking; end-goal `matched=N total=M`, `N=M`, at pinned SHAs, selftest green,
  live census honest, zero regression.
- Wave: `[PARENT: bind the wave record — batch shape, seat completion/loss counts, any
  backfill]`.
- Seats evidenced in the landed artifacts: `oracle-impl` (the oracle revision; write
  ownership held), `census-impl` (the census revision), `receipts-writer` (five receipts +
  `corpus/evidence/README.md` index), `lessons-distiller`
  (`corpus/lessons/2026-10-15-forgeable-oracle-visible-fixtures.md`), `verdict-note-writer`
  (`corpus/knowledge/verdict-machine-r4.md`, landed 17:47Z — including the §2.4 residual
  this report carries), `readme-updater` (`corpus/README.md` knowledge-table + known-gaps
  update, landed), and this scribe seat
  (`.ufo/round-4/goal-wave/{scorecard-verdict-draft,log-entry-draft,report-draft}.md`;
  sha-verified `/tmp` probes used as pre-landing before-evidence). `[PARENT:
  skill-row-updater (SKILL.md) — confirm in the integration diff]`

## Landed changes

- `tools/mori-silence-cases.sh` → sha256
  `be0e28b8bf3cc34e2a35e6cea7c05bffff376111b42d985b6bec7f0e21f59456` (was frozen at
  `505a7504…`): alternation-safe `want_match` replacing `case "$obs" in $want)`
  (assert_case want-strings and case ids byte-identical to the frozen revision); opaque
  per-case trees (`CASE_DIR=$(mktemp -d "$WORK/case.XXXXXXXX")`) so no path handed to the
  census encodes the case id; `MORI_FIXTURE` removed from the census env; new case 28
  `shape-invariance` (same fixture bytes under two random dir names → identical grade +
  normalized stdout).
- `tools/mori-census.sh` → sha256
  `af2d4e79e69b70bb0b5aecd6acc9608fc7c16b0716766d4a60310e0689d350d7` (`VERSION=census-r3`,
  was `fe22a14f…` census-r2): `:227` `state_n` rc-gated (`cap find` + `state_rounds=unavailable
  state_unreadable=1` disclosure; readable dirs keep the r2 row bytes), close tracking per
  anchor round (close pairs; any later same-round close closes the anchor; other-round
  closes irrelevant), selftest 25 → 30 (3 watchdog rc-gate cases + 2 close cases).
- `corpus/lessons/2026-10-15-forgeable-oracle-visible-fixtures.md` — the class: identity
  leak + non-state matcher compose into a forgeable oracle; measured rows (frozen honest
  25/27, frozen sniffer 27/27, hardened 28/28, hardened sniffer 1/28).
- `corpus/knowledge/verdict-machine-r4.md` — sha
  `aab4b62c35e4b01606bda9b10877cc7ce7122ac3c21c589e16cf2dedaf58e28e`: the matcher fix,
  the sniffer channel table + closed channels + **§2.4 order-replay residual**, the `:227`
  rc-gate, per-round close tracking, selftest inventory, final tallies.
- `corpus/evidence/verdict-r4-20261015T173551Z-{selftest,oracle,canary227,sniffer-v2,live}.log`
  + `corpus/evidence/README.md` round-4 index (re-run recipes, preconditions, not-claimed).
- `corpus/README.md` — knowledge-table + known-gaps update (landed).
- `SKILL.md` rows `[PARENT: skill-row-updater — confirm in the integration diff]`.

## Before → after measurements (all figures receipt/note-bound)

| Defect | Before (round-3 SHAs) | After (landed SHAs) | Exit |
|---|---|---|---|
| (a) matcher: `\|`-set wants | frozen oracle vs census-r2: `matched=25 total=27` exit 1; bash 5.3.15 probe `x\|y: MATCH`, `x: no-match`; counterfactual `27/27` exit 0 (scratch `ae95b601…`) | `matched=28 total=28` exit 0 — 27 contract cases all PASS (the two r3 FAILs now PASS), case 28 PASS; deterministic rerun diffed empty (`verdict-r4-…-oracle.log`) | 1 → 0 |
| (b) fixture leak / sniffer | no-logic case-id sniffer fakes `matched=27 total=27` exit 0; 27/27 runs saw `MORI_FIXTURE=1` + case id in `MORI_SHOKUNIN_ROOT` (`:149`, `:269`, `:270`) | case-id channel closed: m4b/m4c verbatim `1/28` exit 1; first order-replay variant `27/28` exit 1 caught by `shape-invariance` (`verdict-r4-…-sniffer-v2.log`); leak log now `MORI_FIXTURE=unset` + random `case.XXXXXXXX` paths. **Residual (§2.4):** a self-consistent order-replay attacker still reaches `28/28` exit 0 — "no sniffer can fake a pass" is false in general; unblock named (randomize case order / decoys) | 0 → 1 (self-consistent variant: still 0) |
| (c) `:227` unreadable `.ufo/state` | rc 1, header only (1 line), 0 verdicts, 0 B stderr; control CLEAN 11 lines | rc 0, full verdict (10 lines), `SURFACE watchdog: ok (… state_rounds=unavailable state_unreadable=1 …)`, every other surface reporting; readable control `state_rounds=1` (`verdict-r4-…-canary227.log`) | 1 → 0 |
| (d) close tracking | `launch r7; complete r7; complete r5` → `silent` + `LANE_SILENT` rc 1; r7-last control → `not-open` rc 0 | selftest cases `silence: close r7 then close r5 -> r7 anchor stays closed` + `silence: close for another round does not close the anchor` PASS; scribe canary at `af2d4e79…` → `not-open (… basis=row-4)` rc 0, control identical (`verdict-r4-…-selftest.log:42-43`) | 1 → 0 |
| selftest | `PASS (25 cases, 25 passed, 0 failed)` exit 0 (round-3 receipt) | `PASS (30 cases, 30 passed, 0 failed)` exit 0 | 0 → 0 |
| live census | honest at round 3 (9/9 progressing, 0 `LANE_SILENT`) | honest at round 4: 9/9 progressing (8 × row-A; aggregator row-B `attribution=inference`), `silence: ok`, 0 `LANE_SILENT`, `DRIFT (findings=15 drift=14 unavailable=1)` tmux-only unavailable; reverify identical finding-id set (`verdict-r4-…-live.log`) | 1 → 1 |

Acceptance re-run at integration `[PARENT: re-run and bind; expected 30/30 exit 0, 28/28
exit 0, honest live verdict]`. Re-run recipes and preconditions are recorded in
`corpus/evidence/README.md` (round-4 section); canary/sniffer scripts are embedded verbatim
inside their receipts and the note; the hermetic receipts reproduce only at the two pinned
SHAs.

## Axis and learning verdicts

Expected shape `[PARENT: bind]`: operability (selected) **improved**; coverage
**unchanged** (no census contract change; verification coverage grew 27→28 oracle cases,
25→30 selftest); depth and freshness **improved narrowly**; calibration **improved**
(adversarial probes, including the residual the first probe missed, are measured and
named); adjacency **unchanged**; none harmed → **ADMIT**, with the parent weighing the
scoped anti-sniff sub-claim (case-id channel closed; general no-sniffer guarantee false —
`verdict-machine-r4.md` §2.4). Learning trends: expansion and quality **improved**;
discernment **unchanged**. Per-axis before→after evidence: `scorecard-verdict-draft.md`
(this directory), to be appended to `SCORECARD.md` by the parent.

## Cross-domain evidence and named debt

- **Order-replay sniffer residual (measured, named)** — a counter-table attacker that
  answers identically on both shape runs reaches `matched=28 total=28` exit 0
  (`verdict-machine-r4.md` §2.4; scratch sha `29cb09ce…`); unblock: randomize case order
  per invocation and/or interleave decoy fixtures. An adversary can also still detect that
  it runs under a fixture tree; `shape-invariance` neutralizes grade branching, not
  detection (`verdict-r4-…-sniffer-v2.log:192-201`).
- **Frozen-behavioral drift pin** — still absent (carried; `silence-cutover-r3.md:253-254`).
- **Row-6 report-body conformance residual** — presence + window only; spec-declared risk
  (`silence-cutover-r3.md:250-252`).
- **Blocked-attempt debts** — receipt-binding and role-routing (`SCORECARD.md:128-131`)
  `[PARENT: status]`.
- Out-of-province, reported not absorbed: live findings on watchdog/waves/journal
  (WATCHDOG_STALE/ABSENT, 11 × WAVE_UNSETTLED_AGE, KILL_SIGNAL_JOURNAL warn,
  SEGFAULT_JOURNAL info) and the tmux `unavailable` (counted, never DRIFT).

Boundaries held: detection and report only — fixtures under `/tmp`, no kill/pkill of real
processes, no systemctl or host config edits, no lane-side commits (parent integrates);
fleet root read-only for seats; the frozen-oracle edit was the registered,
owner-authorized unfreeze (only oracle-impl writes that file).
`[PARENT: confirm from the integration diff]`