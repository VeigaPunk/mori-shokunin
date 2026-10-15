# LOG.md entry draft — append-only (scribe seat, goal wave)

Integration target: append to `LOG.md` at EOF, after the round-4 goal-wave entry —
parent-owned, append-only. Suggested heading:
`## Round 5 — run-order spoofing channel closed (goal wave)`
`[PARENT: keep or rename the heading; bind the commit hash(es), the acceptance re-run
outputs and the round-count line]`.

Draft status: **v4 2026-10-15T18:22Z** by the scribe seat — this revision folds the
**corrected scope**: the landed lesson
`corpus/lessons/2026-10-15-run-order-spoofing-shuffle-nonce-limits.md` (measured
~18:02–18:25Z) falsifies the claim's general form, and this seat independently reproduced
both residual forgers. The note `corpus/knowledge/verdict-machine-r5.md` (sha
`0ef76e9e…`) also landed, with the residuals as witnesses R1–R4. After-side bound to the landed oracle
`7143ccc2a14221713334c33ade56e24ca711fbd0d3d17f31d33e151be544f017` (970 lines; arrived
18:03:25Z; census still frozen `af2d4e79…`) and the receipt set
`corpus/evidence/order-r5-20261015T180431Z-{oracle-1,oracle-2,oracle-3,selftest,live,sniffer}.log`
(indexed in `corpus/evidence/README.md`). Scribe scratch: `/tmp/mori-scribe-r5/`.

---

## Round 5 — run-order spoofing channel closed (goal wave)   `[PARENT: heading]`

**Round 5 — goal-wave admission (2026-10-15).** Motivating evidence: the round-4
correction (`SCORECARD.md:229-238`; admission commit `7a3629a` records / `5b62c897`
evidence) — the claim that a sniffer cannot fake a pass held only for the case-id/path
channel; a run-order sniffer (canned grades keyed on deterministic invocation order,
zero fixture bytes) still reached `matched=28 total=28` exit 0
(`corpus/knowledge/verdict-machine-r4.md` §2.4). Registered round-5 claim:
seeded-shuffled case order (seed logged; same seed ⇒ same order) **and** an unpredictable
per-run nonce injected into fixtures requiring it in census output (stale/missing nonce
fails), so every zero-logic/replay spoof class fails to reach 28/28 while the honest
census holds `matched=28 total=28` exit 0 across shuffled runs with byte-identical
per-case grade tuples. Census frozen this round — only the oracle changes.

Measured before-states at the pinned round-4 SHAs (scribe 17:56:57–17:56:58Z;
receipts-writer 17:59:18–17:59:19Z):

- **Fixed registry order, no per-run secret** — cases ran at source level in registry
  order (`tools/mori-silence-cases.sh:430-672` at `be0e28b8…`; shape pair `:720-725`;
  `assert_case` runs the census inline `:358-360`); `grep -nE
  'seed|shuffle|nonce|SRANDOM|RANDOM'` → no hits; census env `:279-306` carried no run
  secret.
- **Zero-logic order sniffer fakes a full pass** — critic v3
  (`/tmp/mori-critic-r4/sniffer-v3.sh`, sha `ba2a11ba…`; scribe copy counter-path-only
  `66d9b64e…`) → `matched=28 total=28` exit 0; admission seat's `sniffer-order.sh`
  (sha at capture `22d298f8…`) also → `28/28` exit 0; receipts v3a/v3b/v3c each `28/28`
  exit 0 at the same snapshot.

**Landed** (evidence commit `[PARENT: bind]`). `tools/mori-silence-cases.sh` sha256
`7143ccc2a14221713334c33ade56e24ca711fbd0d3d17f31d33e151be544f017` (was `be0e28b8…`;
+423/−198 lines; only order-impl wrote it):

- **Seeded shuffle** — `CASE_IDS` (`:902-931`), xorshift32 (`:936-942`), Fisher–Yates
  (`:944-951`), runner shuffles then logs `SHUFFLE_SEED=` / `RUN_NONCE=` / `CASE_ORDER=`
  (`:953-956`) and dispatches (`:958-960`); seed pinned via `MORI_SHUFFLE_SEED`
  (`:155-160`), not exported to the census env (`:352-353`).
- **Per-run nonce** — generated independently of the seed (`:124-167`); reaches the
  census via env `MORI_RUN_NONCE`, fixture file `$CASE_DIR/run-nonce`, and disk-target
  dir `$CASE_DIR/nonce-<N>` (`:222-227`, `:377-378`); the current token is required in
  every case (`:422-427`, `:490-494`), the read-only guard (`:836-837`) and both shape
  runs (`:885-886`); stale/missing → FAIL with reason
  `run-nonce want=[nonce-…] missing (canned/replayed output?)`.
- Census `tools/mori-census.sh` **unchanged** `af2d4e79e69b70bb0b5aecd6acc9608fc7c16b0716766d4a60310e0689d350d7`
  (`VERSION=census-r3`; sha re-verified before/after every run on both seats).
- Supporting: `SKILL.md:53-64` r5 contract row **landed** (sha `88182790…`); six
  receipts + `corpus/evidence/README.md` round-5 index **landed**; lesson
  `corpus/lessons/2026-10-15-run-order-spoofing-shuffle-nonce-limits.md` **landed**
  (sha `d47492d1…`); note `corpus/knowledge/verdict-machine-r5.md` **landed**
  (sha `0ef76e9e…`); `corpus/README.md` r5 rows **landed** (its anti-sniff bullet
  carries the same scoped correction).

**Acceptance evidence** (two independent seats at pinned shas; parent re-run
`[PARENT: bind]`):

- Honest: `matched=28 total=28` exit 0 across shuffled runs — scribe (random seed
  `1321678548`; `MORI_SHUFFLE_SEED=12345` ×2 identical `CASE_ORDER`; seed `777` different
  order) and receipts `…-oracle-1/2/3.log` (fresh `1612512038`, fresh `1323201475`,
  pinned `1612512038`: `CASE_ORDER` identical to oracle-1, `diff` = `RUN_NONCE` line
  only). Sorted per-case tuples sha `a70af583…` identical across all runs, both seats.
- Enumerated attacker classes fail at the landed oracle (receipts `…-sniffer.log`:
  v3a/v3b/v3c `0/28`, v3d live-nonce echo `6/28`, v3e stale token `0/28`, all exit 1;
  same v3a/b/c `28/28` exit 0 at `be0e28b8…`; scribe: v3-class `0/28`, admission order
  `0/28`, stale replay of a full passing run `0/28`, nonce-aware canned `6/28`).
- Census selftest: `PASS (30 cases, 30 passed, 0 failed)` exit 0 (receipt
  `…-selftest.log`; scribe agrees). Live: receipt `…-live.log` two spots identical
  finding-id sets, `DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)`, tmux-only
  unavailable.
- **Correction (folded same-round): the claim's general form is false.** The lesson
  `2026-10-15-run-order-spoofing-shuffle-nonce-limits.md` names two forgers that still
  reach `28/28` exit 0 at the landed oracle, both reproduced by this seat: the
  **content-keyed memorizer** (`3e0fa4c7…`) — learns fixture fingerprints from one run,
  zero grading logic, immune to shuffle+nonce because the correct answers are constant
  (`/tmp/mori-scribe-r5/after/fp-attacker-check.out`: `28/28` exit 0) — and the
  **`/proc` run-header leak** (`3f05915c…`) — reads `CASE_ORDER`/seed from the oracle's
  own stdout via `/proc/<gp>/fd/1` when stdout is a regular file (the receipt/log
  pattern), replays the public table with the env nonce, no fixture reads
  (`/tmp/mori-scribe-r5/after/leak-attack-check.out`: `28/28` exit 0; piped stdout →
  0/28 per lesson). Lesson also: pinned `MORI_SHUFFLE_SEED` readable via
  `/proc/<gp>/environ` in any mode; env-echo attacker with known seed 777 → `28/28`.
  So the honest scope: the enumerated classes are closed and measured; the general
  "no zero-logic/replay spoof" statement is false, with both counterexamples measured
  and their countermeasures named (randomize state-bearing fixture parameters; treat
  the run's process surface as SUT-readable; log entropy after the run). The note
  `corpus/knowledge/verdict-machine-r5.md` §4 (sha `0ef76e9e…`) records the same
  channels as witnessed residuals: R1 pinned seed via `/proc/<ppid>/environ`
  (`3969ce3b…` → `28/28` pinned / `1/28` unpinned), R2 logged seed via a captured
  stdout fd (`fc26c9f3…` → `28/28` ×3 file capture / `1/28` pipe), plus R3 (nonce gate
  thin) and R4 (content memorization carried).

**Verdicts** `[PARENT: bind]`. Expected shape: operability **improved narrowly** (the
registered class is closed; two wider forgers remain), coverage **unchanged**,
depth/calibration/freshness **improved**, adjacency **unchanged**; on the round-4
precedent the disposition is **ADMIT-with-correction** — the correction is folded
same-round and registered as round-6 debt. Learning trends: expansion/quality
**improved**, discernment **unchanged**. Full per-axis before→after: the `SCORECARD.md`
Round 5 section.

**Carried debt (named, not silently dropped).** **Content-keyed memorization** (lesson
§A) and the **process-surface leak of run secrets** (lesson §B, including file-stdout
receipts and the pinned-seed environ channel); keep the capability-indexed forgery
repertoire current. Carried unchanged: frozen-behavioral drift pin
(`corpus/knowledge/silence-cutover-r3.md:253-254`); row-6 report-body presence-only
residual (`silence-cutover-r3.md:250-252`); blocked-attempt receipt-binding and
role-routing debts (`SCORECARD.md:128-131`).

**Boundaries held.** Detection and report only: fixtures under `/tmp`; no remediation, no
kill/pkill of real processes, no systemctl or host config edits; no lane-side commits by
seats (the parent integrates under the mori identity); fleet root read-only for seats;
oracle and census shas verified before/after every run. `[PARENT: confirm from the
integration diff]`

Round report: `[PARENT: .ufo/reports/round-5/mori-goalwave.md or equivalent]` · Verified
lane rounds: `[PARENT: 4 → 5 on admission]`