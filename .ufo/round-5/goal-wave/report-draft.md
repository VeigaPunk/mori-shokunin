# mori round 5 — goal-wave report draft (scribe seat)

Integration target: the round report (idiom of `.ufo/reports/round-4/mori-goalwave.md`;
final path `[PARENT]`, likely `.ufo/reports/round-5/mori-goalwave.md`). Parent owns the
final path, the identity and the commit binding. Every figure is bound to a landed
artifact or receipt at a cited path; `[PARENT: …]` marks what only the integration commit,
the acceptance re-run, or another seat's ownership can bind; `[PENDING: …]` marks values
unlanded at this draft's clock.

- Status: `[PARENT: completion statement + verified-round-count claim 4 → 5]`
- Evidence commit: `[PARENT: wave integration commit hash under the mori identity]`
- Lane baseline entering the wave: `7a3629a` (round-4 records; `5b62c897` evidence)
- Report time: `[PARENT]`
- Draft status: **v4 2026-10-15T18:23Z** by the scribe seat — this revision folds the
  **corrected scope**: the landed lesson
  `corpus/lessons/2026-10-15-run-order-spoofing-shuffle-nonce-limits.md` falsifies the
  claim's general form, and this seat independently reproduced both residual forgers
  (`/tmp/mori-scribe-r5/after/{fp-attacker-check,leak-attack-check}.out`). After-side
  bound to the landed oracle `7143ccc2…` (970 lines; arrived 18:03:25Z), the frozen
  census `af2d4e79…`, and the receipt set
  `corpus/evidence/order-r5-20261015T180431Z-{oracle-1,oracle-2,oracle-3,selftest,live,sniffer}.log`
  (indexed in `corpus/evidence/README.md`).

## Work performed

- Selected axis **operability** — close the **run-order spoofing channel** (registered
  round-4 correction, `SCORECARD.md:229-238`; mechanism `verdict-machine-r4.md` §2.4).
  Registered claim: before — fixed registry order, no per-run secret, so a zero-logic
  invocation-count replay scores `matched=28 total=28` exit 0; after — seeded-shuffled
  order (seed logged; same seed ⇒ same order) AND a per-run nonce required in census
  output (stale/missing fails); every zero-logic/replay spoof class fails, honest
  `28/28` exit 0 across shuffles with byte-identical per-case tuples. Census frozen — only
  the oracle changes.
- Wave: `[PARENT: bind the wave record — batch shape, seat completion/loss counts, any
  backfill]`.
- Seats evidenced in the landed artifacts: `order-impl` (the oracle revision; sole writer
  of `tools/mori-silence-cases.sh`), `receipts-writer` (six receipts +
  `corpus/evidence/README.md` round-5 index — landed), `lessons-distiller`
  (`corpus/lessons/2026-10-15-run-order-spoofing-shuffle-nonce-limits.md` — landed; it
  carries the correction this report folds), `skill-row-updater` (`SKILL.md:53-64` —
  landed, sha `88182790…`), `note-writer` (`corpus/knowledge/verdict-machine-r5.md` —
  landed, sha `0ef76e9e…`), `readme-updater` (`corpus/README.md` r5 rows — landed), and this scribe
  seat (`.ufo/round-5/goal-wave/{scorecard-verdict-draft,log-entry-draft,report-draft}.md`;
  sha-verified `/tmp/mori-scribe-r5/` probes: before-state, after-state, stale/nonce-aware
  probes, and the two correction counterexamples).

## Landed changes

- `tools/mori-silence-cases.sh`: `be0e28b8…` → `7143ccc2a14221713334c33ade56e24ca711fbd0d3d17f31d33e151be544f017`
  (+423/−198 lines, 970 lines): run entropy (`:124-167` — `rand32` /dev/urandom,
  `MORI_SHUFFLE_SEED` pin, `RUN_NONCE` independent of the seed, token `nonce-<N>`);
  per-run nonce artifacts in every fixture (`:222-227`) and three census channels
  (`:377-378`) with the current token required by every case (`:422-427`, `:490-494`),
  readonly (`:836-837`) and shape (`:885-886`); seed not exported to the census env
  (`:352-353`); same 28 case ids (`:902-931`); xorshift32 + Fisher–Yates (`:936-951`);
  header logs `SHUFFLE_SEED=` / `RUN_NONCE=` / `CASE_ORDER=` (`:953-956`); shuffled
  dispatch (`:958-960`).
- `tools/mori-census.sh`: **unchanged** `af2d4e79e69b70bb0b5aecd6acc9608fc7c16b0716766d4a60310e0689d350d7`
  (`VERSION=census-r3`; frozen — sha re-verified before/after every run, both seats).
- `corpus/evidence/order-r5-20261015T180431Z-{oracle-1,oracle-2,oracle-3,selftest,live,sniffer}.log`
  + `corpus/evidence/README.md` round-5 index/recipes — landed.
- `corpus/lessons/2026-10-15-run-order-spoofing-shuffle-nonce-limits.md` — landed (the
  correction: two forgers still reach 28/28; pattern "hardening moves the attack";
  countermeasures).
- `SKILL.md:53-64` r5 run-order contract row — landed (sha `88182790…`).
- `corpus/knowledge/verdict-machine-r5.md` — landed (sha `0ef76e9e…`: mechanism §2,
  SUT-visibility/reachability table §3, residuals R1–R4 §4 with witnesses); `corpus/README.md`
  r5 rows — landed (anti-sniff bullet scoped the same way).

## Before → after measurements

| Check | Before (round-4 SHAs `be0e28b8…`; scribe 17:56:57Z, receipts 17:59:18Z) | After (landed `7143ccc2…`; scribe 18:04:02–18:21Z, receipts 18:04:31–18:06:58Z) | Exit |
|---|---|---|---|
| honest census | `matched=28 total=28` exit 0 | `matched=28 total=28` exit 0 across shuffled runs — scribe (random, `12345`×2 identical order, `777` different) and receipts oracle-1/2/3 (fresh `1612512038`, fresh `1323201475`, pinned `1612512038`: order identical to run 1, `diff` = `RUN_NONCE` only); sorted tuples sha `a70af583…` all runs, both seats | 0 |
| enumerated replay classes | v3-class + admission order + receipt v3a/v3b/v3c each `28/28` exit 0 | receipts: v3a/v3b/v3c `0/28`, v3d live-nonce echo `6/28`, v3e stale token `0/28` — exit 1 each; scribe: v3-class `0/28`, admission `0/28`, stale replay of a full passing run `0/28`, nonce-aware canned `6/28` | 0 → 1 |
| **correction: two forgers still pass** | n/a | content-keyed memorizer (`3e0fa4c7…`, lesson + scribe spot) `matched=28 total=28` exit 0; `/proc` header-leak attacker (`3f05915c…`, lesson + scribe spot) `28/28` exit 0 with stdout redirected to a file (the receipt/log pattern) — piped stdout closes it (lesson 0/28); pinned-seed environ leak readable in any mode (lesson) | `[n/a]` → 0 |
| selftest (frozen census) | `PASS (30 cases, 30 passed, 0 failed)` exit 0 | `PASS (30 cases, 30 passed, 0 failed)` exit 0 (receipt + scribe) | 0 |
| live census | honest round-4 shape | receipt `…-live.log` two spots, identical finding-id sets: `DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)` exit 1; tmux-only unavailable; scribe single-lane spot same shape | 1 |

Acceptance re-run at integration `[PARENT: re-run and bind; expected 28/28 exit 0 at the
landed oracle across seeds, 30/30 selftest exit 0, honest live verdict]`. Re-run recipes:
`corpus/evidence/README.md` round-5 section; correction repro: lesson's Repro section.

## Axis and learning verdicts

Expected shape `[PARENT: bind]`: operability **improved narrowly** (registered class
closed; two wider forgers measured open); coverage **unchanged** (census frozen; same 28
case ids); depth/freshness/calibration **improved**; adjacency **unchanged**; on the
round-4 precedent the disposition is **ADMIT-with-correction**, the correction folded
same-round. Learning trends: expansion and quality **improved**; discernment
**unchanged**. Per-axis before→after evidence: `scorecard-verdict-draft.md` (this
directory), to be appended to `SCORECARD.md` by the parent.

## Cross-domain evidence and named debt

- **Enumerated replay classes closed** — measured by two seats (receipts + scribe,
  agreeing figures); nonce isolation proven (stale-token runs fail 100% on `run-nonce`,
  0% on state — lesson).
- **Correction folded same-round — two forgers still reach 28/28 at the landed oracle:**
  (A) fixture-content memorizer (one observed run suffices; states are constant, so
  shuffle+nonce are irrelevant to it; countermeasure: randomize state-bearing fixture
  parameters); (B) `/proc` run-header leak (oracle stdout read through
  `/proc/<gp>/fd/1` when stdout is a regular file — every `> log` receipt — replays the
  public table with the env nonce, no fixture reads; piped stdout closes it; pinned seed
  readable via `/proc/<gp>/environ` in any mode; countermeasures: keep run entropy out of
  file-bound streams while grading, log it after the run, treat the process surface as
  SUT-readable). Lesson: `corpus/lessons/2026-10-15-run-order-spoofing-shuffle-nonce-limits.md`;
  note `corpus/knowledge/verdict-machine-r5.md` §4 (sha `0ef76e9e…`) records the same
  channels as witnessed residuals R1 (`3969ce3b…` → `28/28` pinned / `1/28` unpinned)
  and R2 (`fc26c9f3…` → `28/28` ×3 file capture / `1/28` pipe), plus R3 (nonce gate
  thin) and R4 (content memorization carried).
- **Known limit pattern** — "each hardening closes the class it aimed at and moves the
  attack to the next SUT-visible regularity" (lesson); keep the capability-indexed
  forgery repertoire current.
- **Frozen-behavioral drift pin** — still absent (carried; `silence-cutover-r3.md:253-254`).
- **Row-6 report-body conformance residual** — presence + window only
  (`silence-cutover-r3.md:250-252`).
- **Blocked-attempt debts** — receipt-binding and role-routing (`SCORECARD.md:128-131`)
  `[PARENT: status]`.
- Out-of-province, reported not absorbed (receipt live + scribe spot): 1 ×
  `KILL_SIGNAL_JOURNAL`, 1 × `SEGFAULT_JOURNAL`, 1 × `WATCHDOG_ABSENT`, 1 ×
  `WATCHDOG_STALE`, 11 × `WAVE_UNSETTLED_AGE`; tmux `unavailable` (counted, never DRIFT).

Boundaries held: detection and report only — fixtures under `/tmp`, no kill/pkill of real
processes, no systemctl or host config edits, no lane-side commits (parent integrates);
fleet root read-only for seats; oracle+census shas verified before/after every run.
`[PARENT: confirm from the integration diff]`